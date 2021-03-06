import asyncio
import json
from typing import Any, Dict, List, Optional

import aredis
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import Response

from .common import current_round, redis
from .models import TeamState

app = FastAPI()
UPDATE_EVENT: asyncio.Event = asyncio.Event()
scoreboard_cache: Dict[int, bytes] = dict()


async def get_scoreboard(round: Optional[int] = None) -> Optional[bytes]:
    round = round or await current_round()
    if not round:
        return None

    if round in scoreboard_cache:
        return scoreboard_cache[round]

    entry = await redis.get(f"sb_{round}")
    if not entry:
        return None

    scoreboard_cache[round] = entry

    return entry


def get_team_state_from_scoreoard(
    scoreboard: bytes, team_id: int
) -> Optional[Dict[str, Any]]:
    sb = json.loads(scoreboard.decode())

    for t in sb["teams"]:
        if t["teamId"] != team_id:
            continue
        return {
            "round": sb["currentRound"],
            "totalPoints": t["totalPoints"],
            "attackPoints": t["attackPoints"],
            "lostDefensePoints": t["lostDefensePoints"],
            "serviceLevelAgreementPoints": t["serviceLevelAgreementPoints"],
            "serviceDetails": t["serviceDetails"],
        }

    return None


async def build_team_scoreboard(
    team_id: int, base: List[Dict[str, Any]], start: int, end: int
) -> Optional[bytes]:
    entry: Optional[bytes] = None
    last: Optional[int] = None
    for i in range(start + 1, end + 1):
        sb = await get_scoreboard(i)
        if not sb:
            continue
        state = get_team_state_from_scoreoard(sb, team_id)
        if not state:
            continue
        last = i
        base.append(state)
    if last is not None:
        entry = json.dumps(base).encode()
        await redis.set(f"team_{team_id}_round_{last}", entry)
        return entry
    return None


async def get_team_scoreboard(team_id: int) -> Optional[bytes]:
    round = await current_round()
    if not round:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CTF not yet started"
        )

    entry = await redis.get(f"team_{team_id}_round_{round}")
    if entry:
        return entry

    for i in range(round)[::-1]:
        entry = await redis.get(f"team_{team_id}_round_{i}")
        if entry:
            ret = await build_team_scoreboard(
                team_id, json.loads(entry.decode()), i, round
            )
            if ret:
                await redis.set(f"team_{team_id}_round_{i}", None)
            return ret

    return await build_team_scoreboard(team_id, [], 0, round)


@app.get("/api/scoreboard")
async def scoreboard() -> Response:
    sb = await get_scoreboard()
    if not sb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CTF not yet started"
        )
    return Response(content=sb, media_type="application/json")


@app.get("/api/scoreboard/history/{round_id}")
async def scoreboard_history(round_id: int) -> Response:
    sb = await get_scoreboard(round_id)
    if not sb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Round not found"
        )
    return Response(content=sb, media_type="application/json")


@app.get("/api/scoreboard/live")
async def scoreboard_live() -> Response:
    await UPDATE_EVENT.wait()
    sb = await get_scoreboard()
    if not sb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CTF not yet started"
        )
    return Response(content=sb, media_type="application/json")


@app.get("/api/teams/{team_id}", response_model=List[TeamState])
async def get_team(team_id: int) -> Response:
    if not await redis.get(f"team_exists_${team_id}"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No team details found"
        )

    sb = await get_team_scoreboard(team_id)
    if not sb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No team details found"
        )
    return Response(content=sb, media_type="application/json")


@app.get("/api/config")
async def get_config() -> Response:
    ti = await redis.get("config")
    if not ti:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No team info found"
        )
    return Response(content=ti, media_type="application/json")


@app.on_event("startup")
async def startup() -> None:
    asyncio.create_task(handle_updates_forever())


async def handle_updates_forever() -> None:
    while True:
        try:
            await handle_updates()
        except aredis.exceptions.ConnectionError:
            print("Failed to connect to redis...")
            await asyncio.sleep(1)


async def handle_updates() -> None:
    global UPDATE_EVENT
    p = redis.pubsub(ignore_subscribe_messages=True)
    await p.subscribe("notifications")
    while True:
        reply = await p.get_message()
        if not reply:
            continue
        old_event = UPDATE_EVENT
        UPDATE_EVENT = asyncio.Event()
        old_event.set()

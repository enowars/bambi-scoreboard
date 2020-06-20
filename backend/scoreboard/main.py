import asyncio
import json
import os
from typing import Any, Dict, List, Optional

import aredis
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel
from watchgod import Change, awatch

app = FastAPI()
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
DATA_DIR = os.getenv("DATA_DIR", "../data")
redis: aredis.StrictRedis = aredis.StrictRedis(host=REDIS_HOST)


class ServiceDetail(BaseModel):
    ServiceId: int
    AttackPoints: float
    LostDefensePoints: float
    ServiceLevelAgreementPoints: float
    ServiceStatus: str
    Message: str


class ScoreboardTeam(BaseModel):
    Name: str
    TeamId: int
    TotalPoints: float
    AttackPoints: float
    LostDefensePoints: float
    ServiceLevelAgreementPoints: float
    ServiceDetails: List[ServiceDetail]


class FirstBlood(BaseModel):
    TeamId: int
    Timestamp: str
    RoundId: int
    StoreDescription: Optional[str]
    StoreIndex: int


class ScoreboardService(BaseModel):
    ServiceId: int
    ServiceName: str
    MaxStores: int
    FirstBloods: List[FirstBlood]


class JsonScoreboard(BaseModel):
    CurrentRound: Optional[int]
    StartTimeEpoch: Optional[int]
    EndTimeEpoch: Optional[int]
    Services: List[ScoreboardService]
    Teams: List[ScoreboardTeam]


class TeamState(BaseModel):
    Round: int
    TotalPoints: float
    AttackPoints: float
    LostDefensePoints: float
    ServiceLevelAgreementPoints: float
    ServiceDetails: List[ServiceDetail]


async def current_round() -> Optional[int]:
    r = await redis.get("max_round")
    if not r:
        return None
    return int(r.decode())


async def get_scoreboard(round: Optional[int] = None) -> Optional[bytes]:
    round = round or await current_round()
    if not round:
        return None

    entry = await redis.get(f"sb_{round}")
    if not entry:
        return None

    return entry


def get_team_state_from_scoreoard(
    scoreboard: bytes, team_id: int
) -> Optional[Dict[str, Any]]:
    sb = json.loads(scoreboard.decode())

    for t in sb["Teams"]:
        if t["TeamId"] != team_id:
            continue
        return {
            "Round": sb["CurrentRound"],
            "TotalPoints": t["TotalPoints"],
            "AttackPoints": t["AttackPoints"],
            "LostDefensePoints": t["LostDefensePoints"],
            "ServiceLevelAgreementPoints": t["ServiceLevelAgreementPoints"],
            "ServiceDetails": t["ServiceDetails"],
        }

    return None


async def build_team_scoreboard(
    team_id: int, base: List[Dict[str, Any]], start: int, end: int
) -> Optional[bytes]:
    entry: Optional[bytes] = None
    for i in range(start + 1, end + 1):
        sb = await get_scoreboard(i)
        if not sb:
            continue
        state = get_team_state_from_scoreoard(sb, team_id)
        if not state:
            continue
        base.append(state)
        entry = json.dumps(base).encode()
        await redis.set(f"team_{team_id}_round_{i}", entry)
    return entry


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
            return await build_team_scoreboard(
                team_id, json.loads(entry.decode()), i, round
            )

    return await build_team_scoreboard(team_id, [], 0, round)


@app.get("/api/scoreboard")
async def scoreboard() -> Response:
    sb = await get_scoreboard()
    if not sb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CTF not yet started"
        )
    return Response(content=sb, media_type="application/json")


@app.get("/api/scoreboard/live")
async def scoreboard_live() -> Response:
    await asyncio.sleep(5)
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


@app.on_event("startup")
async def startup() -> None:
    base_path = os.path.join(DATA_DIR, "scoreboard.json")
    await parse_scoreboard(base_path)
    r = await current_round()
    if r is not None:
        for i in range(0, r + 1):
            sb_path = os.path.join(DATA_DIR, f"scoreboard{i}.json")
            await parse_scoreboard(sb_path)

    asyncio.create_task(create_watch())


async def create_watch() -> None:
    async for changes in awatch(DATA_DIR):
        for c in changes:
            if c[0] == Change.added or c[0] == Change.modified:
                await parse_scoreboard(c[1])


async def parse_scoreboard(file_: str) -> None:
    try:
        obj = json.load(open(file_, "r"))
        sb = JsonScoreboard(**obj)
        print(f"Loading scoreboard for round {sb.CurrentRound}")

        if not sb.CurrentRound:
            return

        entry = await redis.get(f"sb_{sb.CurrentRound}")
        print(f"previous: sb_{sb.CurrentRound}: {entry}")
        if not entry:
            await redis.set(f"sb_{sb.CurrentRound}", sb.json())

        entry = await redis.get("max_round")
        print(f"previous: max_round: {entry}")
        if not entry or int(entry.decode()) < sb.CurrentRound:
            await redis.set("max_round", sb.CurrentRound)

        for t in sb.Teams:
            await redis.set(f"team_exists_${t.TeamId}", True)
    except FileNotFoundError as e:
        print(f"Failed to load scoreboard: {file_}, {str(e)}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse scoreboard: {file_}, {str(e)}")

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
REDIS_HOST = os.getenv("REDIST_HOST", "127.0.0.1")
DATA_DIR = os.getenv("DATA_DIR", "../data")
redis: aredis.StrictRedis = aredis.StrictRedis(host=REDIS_HOST)


class ServiceDetail(BaseModel):
    ServiceId: int
    AttackPoints: float
    LostDefensePoints: float
    ServiceLevelAgreementPoints: float
    ServiceStatus: str


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
    CurrentRound: int
    StartTimeEpoch: int
    EndTimeEpoch: int
    Services: List[ScoreboardService]
    Teams: List[ScoreboardTeam]


class TeamState(BaseModel):
    Round: int
    TotalPoints: float
    AttackPoints: float
    LostDefensePoints: float
    ServiceLevelAgreementPoints: float
    ServiceDetails: List[ServiceDetail]


async def get_scoreboard(round: Optional[int] = None) -> bytes:
    if not round:
        r = await redis.get("max_round")
        if not r:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="CTF not yet started"
            )

        round = int(r.decode())

    entry = await redis.get(f"sb_{round}")
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CTF not yet started"
        )

    return entry


@app.get("/api/scoreboard")
async def scoreboard() -> Response:
    return Response(content=await get_scoreboard(), media_type="text/json")


@app.get("/api/scoreboard/live")
async def scoreboard_live() -> Response:
    await asyncio.sleep(5)
    return Response(content=await get_scoreboard(), media_type="text/json")


@app.get("/api/teams/{team_id}", response_model=List[TeamState])
async def get_team(team_id: int) -> List[Dict[str, Any]]:
    return [
        {
            "Round": 1,
            "TotalPoints": 12345,
            "AttackPoints": 100,
            "LostDefensePoints": 2000,
            "ServiceLevelAgreementPoints": 14245,
            "ServiceDetails": [
                {
                    "ServiceId": 1,
                    "AttackPoints": 100,
                    "LostDefensePoints": 2000,
                    "ServiceLevelAgreementPoints": 14245,
                    "ServiceStatus": "INTERNAL_ERROR",
                },
                {
                    "ServiceId": 2,
                    "AttackPoints": 100,
                    "LostDefensePoints": 2000,
                    "ServiceLevelAgreementPoints": 14245,
                    "ServiceStatus": "OK",
                },
                {
                    "ServiceId": 3,
                    "AttackPoints": 100,
                    "LostDefensePoints": 2000,
                    "ServiceLevelAgreementPoints": 14245,
                    "ServiceStatus": "RECOVERING",
                },
            ],
        },
        {
            "Round": 2,
            "Score": 123,
            "TotalPoints": 12445,
            "AttackPoints": 200,
            "LostDefensePoints": 2000,
            "ServiceLevelAgreementPoints": 14245,
            "ServiceDetails": [
                {
                    "ServiceId": 1,
                    "AttackPoints": 200,
                    "LostDefensePoints": 2000,
                    "ServiceLevelAgreementPoints": 14245,
                    "ServiceStatus": "MUMBLE",
                },
                {
                    "ServiceId": 3,
                    "AttackPoints": 100,
                    "LostDefensePoints": 2000,
                    "ServiceLevelAgreementPoints": 14245,
                    "ServiceStatus": "OFFLINE",
                },
                {
                    "ServiceId": 2,
                    "AttackPoints": 100,
                    "LostDefensePoints": 2000,
                    "ServiceLevelAgreementPoints": 14245,
                    "ServiceStatus": "INACTIVE",
                },
            ],
        },
    ]


@app.on_event("startup")
async def startup() -> None:
    asyncio.create_task(create_watch())


async def create_watch() -> None:
    async for changes in awatch(DATA_DIR):
        for c in changes:
            if c[0] != Change.added:
                continue
            await parse_scoreboard(c[1])


async def parse_scoreboard(file_: str) -> None:
    try:
        obj = json.load(open(file_, "r"))
        sb = JsonScoreboard(**obj)

        entry = await redis.get(f"sb_{sb.CurrentRound}")
        print(f"previous: sb_{sb.CurrentRound}: {entry}")
        if not entry:
            await redis.set(f"sb_{sb.CurrentRound}", sb.json())

        entry = await redis.get("max_round")
        print(f"previous: max_round: {entry}")
        if not entry or int(entry.decode()) < sb.CurrentRound:
            await redis.set("max_round", sb.CurrentRound)
    except json.JSONDecodeError as e:
        print(f"Failed to parse scoreboard: {file_}, {str(e)}")
    print(sb)

import asyncio
import datetime
import json
import time
from typing import Any, Dict, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel
from watchgod import awatch, Change

app = FastAPI()


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


def construct_scoreboard() -> JsonScoreboard:
    obj = json.load(open("scoreboard/test.json", "r"))
    sb = JsonScoreboard(**obj)
    sb.StartTimeEpoch = int(time.time()) - 90
    sb.EndTimeEpoch = int(time.time()) - 30
    return sb


@app.get("/api/scoreboard", response_model=JsonScoreboard)
async def scoreboard():
    return construct_scoreboard()


@app.get("/api/scoreboard/live", response_model=JsonScoreboard)
async def scoreboard_live():
    await asyncio.sleep(5)
    return construct_scoreboard()


@app.get("/api/teams/{team_id}", response_model=List[TeamState])
async def get_team(team_id: int):
    return [{
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
                "ServiceStatus": "INTERNAL_ERROR"
            },
            {
                "ServiceId": 2,
                "AttackPoints": 100,
                "LostDefensePoints": 2000,
                "ServiceLevelAgreementPoints": 14245,
                "ServiceStatus": "OK"
            },
            {
                "ServiceId": 3,
                "AttackPoints": 100,
                "LostDefensePoints": 2000,
                "ServiceLevelAgreementPoints": 14245,
                "ServiceStatus": "RECOVERING"
            }
        ]
    },{
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
                "ServiceStatus": "MUMBLE"
            },
            {
                "ServiceId": 3,
                "AttackPoints": 100,
                "LostDefensePoints": 2000,
                "ServiceLevelAgreementPoints": 14245,
                "ServiceStatus": "OFFLINE"
            },
            {
                "ServiceId": 2,
                "AttackPoints": 100,
                "LostDefensePoints": 2000,
                "ServiceLevelAgreementPoints": 14245,
                "ServiceStatus": "INACTIVE"
            }
        ]
    }]


@app.on_event("startup")
async def startup() -> None:
    asyncio.create_task(create_watch())


async def create_watch():
    async for changes in awatch("../data"):
        for c in changes:
            if c[0] != Change.added:
                continue
            await parse_scoreboard(c[1])


async def parse_scoreboard(file_):
    try:
        obj = json.load(open(file_, "r"))
        sb = JsonScoreboard(**obj)
    except json.JSONDecodeError as e:
        print(f"Failed to parse scoreboard: {file_}, {str(e)}")
    print(sb)

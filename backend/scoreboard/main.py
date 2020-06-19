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
    StartTime: int
    Services: List[ScoreboardService]
    Teams: List[ScoreboardTeam]


class TeamTask(BaseModel):
    id: int
    round: Optional[int]
    task_id: int
    team_id: int
    status: int
    sla: float
    attack: float
    defense: float
    message: str


class TeamState(BaseModel):
    Round: int
    TotalPoints: float
    AttackPoints: float
    LostDefensePoints: float
    ServiceLevelAgreementPoints: float
    ServiceDetails: List[ServiceDetail]


class GameState(BaseModel):
    round_start: int
    round: int
    team_tasks: List[TeamTask]


class GlobalConfig(BaseModel):
    id: Optional[int]
    flag_lifetime: int
    round_time: int
    timezone: str
    start_time: datetime.datetime


class Team(BaseModel):
    id: int
    name: str
    ip: str
    highlighted: bool
    active: bool


class TeamList(BaseModel):
    data: List[Team]


class Task(BaseModel):
    id: int
    name: str


class TaskList(BaseModel):
    data: List[Task]


class StateList(BaseModel):
    data: List[TeamTask]


class Scoreboard(BaseModel):
    state: GameState
    teams: List[Team]
    tasks: List[Task]
    config: GlobalConfig


async def construct_scoreboard_old():
    return {
        "state": {
            "round_start": int(time.time()) - 30,
            "round": 5,
            "team_tasks": [
                {
                    "id": 1237,
                    "round": 1,
                    "task_id": 1,
                    "team_id": 1,
                    "status": 101,
                    "sla": 51.5,
                    "attack": 13.37,
                    "defense": 5.0012378182,
                    "message": "Works for me!",
                },
                {
                    "id": 1238,
                    "round": 1,
                    "task_id": 2,
                    "team_id": 1,
                    "status": 101,
                    "sla": 51.5,
                    "attack": 13.37,
                    "defense": 5.0012378182,
                    "message": "Works for me!",
                },
                {
                    "id": 1239,
                    "round": 1,
                    "task_id": 3,
                    "team_id": 1,
                    "status": 101,
                    "sla": 51.5,
                    "attack": 13.37,
                    "defense": 5.0012378182,
                    "message": "Works for me!",
                },
                {
                    "id": 1240,
                    "round": 1,
                    "task_id": 4,
                    "team_id": 1,
                    "status": 101,
                    "sla": 51.5,
                    "attack": 13.37,
                    "defense": 5.0012378182,
                    "message": "Works for me!",
                },
                {
                    "id": 1241,
                    "round": 1,
                    "task_id": 5,
                    "team_id": 1,
                    "status": 101,
                    "sla": 51.5,
                    "attack": 13.37,
                    "defense": 5.0012378182,
                    "message": "Works for me!",
                },
                {
                    "id": 1242,
                    "round": 1,
                    "task_id": 6,
                    "team_id": 1,
                    "status": 101,
                    "sla": 51.5,
                    "attack": 13.37,
                    "defense": 5.0012378182,
                    "message": "Works for me!",
                },
                {
                    "id": 1243,
                    "round": 1,
                    "task_id": 7,
                    "team_id": 1,
                    "status": 101,
                    "sla": 51.5,
                    "attack": 13.37,
                    "defense": 5.0012378182,
                    "message": "Works for me!",
                },
            ],
        },
        "teams": [
            {
                "id": 1,
                "name": "Lol",
                "ip": "127.0.0.1",
                "highlighted": False,
                "active": True,
            },
            {
                "id": 2,
                "name": "Lol2",
                "ip": "127.0.0.2",
                "highlighted": False,
                "active": True,
            }
        ],
        "tasks": [
            {
                "id": 1,
                "name": "Task!",
            },
            {
                "id": 2,
                "name": "Another Task",
            },
            {
                "id": 3,
                "name": "Yet another task",
            },
            {
                "id": 4,
                "name": "moar tasks",
            },
            {
                "id": 5,
                "name": "LALALALAL"
            },
            {
                "id": 6,
                "name": "LAAAAAAAAAAAAAANGEEEEEER NAME"
            },
            {
                "id": 7,
                "name": "ok"
            }
        ],
        "config": {
            "id": 1337,
            "flag_lifetime": 10,
            "round_time": 60,
            "timezone": "CEST",
            "start_time": datetime.datetime(2020, 6, 19, 16, 0, 0)
        }
    }


def construct_scoreboard() -> JsonScoreboard:
    obj = json.load(open("scoreboard/test.json", "r"))
    sb = JsonScoreboard(**obj)
    return sb


@app.get("/api/config", response_model=GlobalConfig)
def config() -> Dict[str, Any]:
    return {
        "id": 1337,
        "flag_lifetime": 10,
        "round_time": 60,
        "timezone": "CEST",
        "start_time": datetime.datetime(2020, 6, 19, 16, 0, 0)
    }


@app.get("/api/scoreboard", response_model=JsonScoreboard)
async def scoreboard():
    return construct_scoreboard()


@app.get("/api/scoreboard/live", response_model=JsonScoreboard)
async def scoreboard_live():
    sb = construct_scoreboard()
    sb.StartTime = int(time.time())
    await asyncio.sleep(5)
    return sb


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

import asyncio
import datetime
import time
from typing import Any, Dict, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


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


async def construct_scoreboard():
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


@app.get("/api/config", response_model=GlobalConfig)
def config() -> Dict[str, Any]:
    return {
        "id": 1337,
        "flag_lifetime": 10,
        "round_time": 60,
        "timezone": "CEST",
        "start_time": datetime.datetime(2020, 6, 19, 16, 0, 0)
    }


@app.get("/api/scoreboard", response_model=Scoreboard)
async def scoreboard():
    return await construct_scoreboard()


@app.get("/api/scoreboard/live", response_model=GameState)
async def scoreboard_live():
    await asyncio.sleep(5)
    sb = await construct_scoreboard()
    return sb["state"]


@app.get("/api/tasks", response_model=List[Task])
async def get_tasks():
    sb = await construct_scoreboard()
    return sb["tasks"]


@app.get("/api/teams", response_model=List[Team])
async def get_teams():
    sb = await construct_scoreboard()
    return sb["teams"]


@app.get("/api/teams/{team_id}", response_model=List[TeamTask])
async def get_team(team_id: int):
    sb = await construct_scoreboard()
    base_task = {
        "id": 1239,
        "round": 1,
        "task_id": 3,
        "team_id": 1,
        "status": 101,
        "sla": 51.5,
        "attack": 13.37,
        "defense": 5.0012378182,
        "message": "Works for me!",
    }
    return sb["state"]["team_tasks"]

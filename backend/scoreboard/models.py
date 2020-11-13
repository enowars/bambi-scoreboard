from typing import List, Optional

from pydantic import BaseModel


class ServiceDetail(BaseModel):
    serviceId: int
    attackPoints: float
    lostDefensePoints: float
    serviceLevelAgreementPoints: float
    serviceStatus: str
    message: Optional[str]


class ScoreboardTeam(BaseModel):
    name: str
    teamId: int
    totalPoints: float
    attackPoints: float
    lostDefensePoints: float
    serviceLevelAgreementPoints: float
    serviceDetails: List[ServiceDetail]


class FirstBlood(BaseModel):
    teamId: int
    timestamp: str
    roundId: int
    storeDescription: Optional[str]
    storeIndex: int


class ScoreboardService(BaseModel):
    serviceId: int
    serviceName: str
    maxStores: int
    firstBloods: List[FirstBlood]


class JsonScoreboard(BaseModel):
    currentRound: Optional[int]
    startTimeEpoch: Optional[int]
    endTimeEpoch: Optional[int]
    services: List[ScoreboardService]
    teams: List[ScoreboardTeam]


class TeamState(BaseModel):
    round: int
    totalPoints: float
    attackPoints: float
    lostDefensePoints: float
    serviceLevelAgreementPoints: float
    serviceDetails: List[ServiceDetail]

from typing import List, Optional

from pydantic import BaseModel


class ServiceDetail(BaseModel):
    ServiceId: int
    AttackPoints: float
    LostDefensePoints: float
    ServiceLevelAgreementPoints: float
    ServiceStatus: str
    Message: Optional[str]


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

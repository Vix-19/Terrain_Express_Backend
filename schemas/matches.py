from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from schemas.pitches import Pitch

class MatchPlayer(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class MatchBase(BaseModel):
    pitch_id: int
    start_time: datetime
    level: str
    players_needed: int

class MatchCreate(MatchBase):
    pass

class Match(MatchBase):
    id: int
    creator_id: int
    players_joined: int
    status: str
    player_ids: List[int] = []
    players: List[MatchPlayer] = []
    rated_user_ids: List[int] = []
    pitch: Optional[Pitch] = None

    class Config:
        from_attributes = True

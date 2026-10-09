from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from schemas.pitches import Pitch

class BookingBase(BaseModel):
    pitch_id: int
    start_time: datetime
    end_time: datetime

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    user_id: int
    total_price: float
    status: str
    pitch: Optional[Pitch] = None
    player_name: Optional[str] = None

    class Config:
        from_attributes = True

class Slot(BaseModel):
    pitch_id: int
    start_time: datetime
    end_time: datetime
    price: float
    is_available: bool = True

    class Config:
        from_attributes = True

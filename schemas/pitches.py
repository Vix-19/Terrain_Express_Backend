from pydantic import BaseModel
from typing import Optional

class PitchBase(BaseModel):
    name: str
    address: str
    city: str = "Fès"
    size: str = "5v5"
    price_per_hour: float
    image_url: Optional[str] = None
    is_validated: bool = False

class PitchCreate(PitchBase):
    pass

class Pitch(PitchBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    pitch_id = Column(Integer, ForeignKey("pitches.id"), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    match_time = Column(DateTime, nullable=False)
    players_needed = Column(Integer, nullable=False)
    required_level = Column(String) # e.g., beginner, intermediate, advanced

    pitch = relationship("Pitch")
    creator = relationship("User")
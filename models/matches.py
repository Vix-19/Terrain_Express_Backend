from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

match_players = Table(
    'match_players',
    Base.metadata,
    Column('match_id', Integer, ForeignKey('matches.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    pitch_id = Column(Integer, ForeignKey("pitches.id"), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    level = Column(String, nullable=False)
    players_needed = Column(Integer, nullable=False)
    players_joined = Column(Integer, default=1)
    status = Column(String, default="open")

    pitch = relationship("Pitch")
    creator = relationship("User")
    players = relationship("User", secondary=match_players)
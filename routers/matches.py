from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
import models.matches as models
import schemas.matches as schemas
from models.users import User

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/matches", tags=["Matches"])

@router.get("/", response_model=List[schemas.Match])
def get_matches(db: Session = Depends(get_db)):
    matches = db.query(models.Match).all()
    # Pydantic model requires player_ids
    for match in matches:
        match.player_ids = [p.id for p in match.players]
    return matches

@router.post("/", response_model=schemas.Match)
def create_match(match: schemas.MatchCreate, creator_id: int, db: Session = Depends(get_db)):
    creator = db.query(User).filter(User.id == creator_id).first()
    if not creator:
        raise HTTPException(status_code=404, detail="User not found")

    db_match = models.Match(**match.model_dump(), creator_id=creator_id)
    db_match.players.append(creator)
    db_match.players_joined = 1
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    db_match.player_ids = [p.id for p in db_match.players]
    return db_match

@router.post("/{match_id}/join")
def join_match(match_id: int, user_id: int, db: Session = Depends(get_db)):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user in match.players:
        raise HTTPException(status_code=400, detail="User already joined")
        
    if match.players_joined >= match.players_needed:
        raise HTTPException(status_code=400, detail="Match is full")
        
    match.players.append(user)
    match.players_joined += 1
    if match.players_joined == match.players_needed:
        match.status = "full"
        
    db.commit()
    db.refresh(match)
    return {"message": "Successfully joined match"}

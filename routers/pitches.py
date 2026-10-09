from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
import models.pitches as models
import schemas.pitches as schemas

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/pitches", tags=["Pitches"])

@router.get("/", response_model=List[schemas.Pitch])
def get_pitches(db: Session = Depends(get_db)):
    return db.query(models.Pitch).all()

@router.get("/{pitch_id}", response_model=schemas.Pitch)
def get_pitch(pitch_id: int, db: Session = Depends(get_db)):
    pitch = db.query(models.Pitch).filter(models.Pitch.id == pitch_id).first()
    if not pitch:
        raise HTTPException(status_code=404, detail="Pitch not found")
    return pitch

@router.post("/", response_model=schemas.Pitch)
def create_pitch(pitch: schemas.PitchCreate, owner_id: int, db: Session = Depends(get_db)):
    db_pitch = models.Pitch(**pitch.model_dump(), owner_id=owner_id)
    db.add(db_pitch)
    db.commit()
    db.refresh(db_pitch)
    return db_pitch

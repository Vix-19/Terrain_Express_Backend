from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
import models.bookings as models
import schemas.bookings as schemas
from models.pitches import Pitch

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.get("/", response_model=List[schemas.Booking])
def get_bookings(db: Session = Depends(get_db)):
    return db.query(models.Booking).all()

@router.post("/", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, user_id: int, db: Session = Depends(get_db)):
    duration = (booking.end_time - booking.start_time).total_seconds() / 3600.0
    pitch = db.query(Pitch).filter(Pitch.id == booking.pitch_id).first()
    if not pitch:
        raise HTTPException(status_code=404, detail="Pitch not found")
    
    total_price = duration * pitch.price_per_hour
    
    db_booking = models.Booking(**booking.model_dump(), user_id=user_id, total_price=total_price)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

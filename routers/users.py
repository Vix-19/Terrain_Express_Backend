from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from models.users import User
from schemas.users import UserCreate, UserResponse
from database import SessionLocal

# Setup password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Setup the router
router = APIRouter(prefix="/users", tags=["Users"])

# Dependency to get a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email is already registered
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password
    hashed_password = pwd_context.hash(user.password)
    
    # Create the SQLAlchemy model instance
    new_user = User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password,
        is_pitch_owner=user.is_pitch_owner
    )
    
    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
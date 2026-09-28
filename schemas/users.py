from pydantic import BaseModel

# Base properties shared across multiple schemas
class UserBase(BaseModel):
    email: str
    name: str
    is_pitch_owner: bool = False

# Schema for creating a user (requires a password)
class UserCreate(UserBase):
    password: str

# Schema for returning user data (hides the password, includes the ID)
class UserResponse(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True # Tells Pydantic to read data even if it is an SQLAlchemy model
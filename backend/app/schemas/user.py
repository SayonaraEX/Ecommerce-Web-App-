# backend/app/schemas/user.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., max_length=255, description="Unique username for login")
    email: EmailStr = Field(..., max_length=255, description="User email address")
    first_name: Optional[str] = Field(None, max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)
    address: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=255)
    state: Optional[str] = Field(None, max_length=255)
    zip_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, max_length=50)
    role: str = Field("customer", pattern="^(customer|admin)$", description="User role: customer or admin")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User's password (will be hashed)")

class User(UserBase):
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None 

    class Config:
        from_attributes = True
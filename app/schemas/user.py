from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

class UserResponse(BaseModel):
    #Schema for user response
    id: UUID
    username: str
    email: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True) # Enable attribute access for ORM models

class Token(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "token_type": "bearer",
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "username": "aea79",
                    "email": "aea79@njit.edu",
                    "created_at": "2026-04-06T00:00:00",
                },
            }
        }
    )

class TokenData(BaseModel):
    """Schema for JWT token payload"""
    user_id: Optional[UUID] = None

class UserLogin(BaseModel):
    #Schema for user login
    username: str
    password: str

    
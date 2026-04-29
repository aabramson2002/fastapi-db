from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field, model_validator

class UserBase(BaseModel):
    #Base schema for user creation and response
    username: str = Field(min_length=3, max_length=50, example="aea79")
    email: EmailStr = Field(example="aea79@example.com")
    first_name: str = Field(min_length=1, max_length=50, example="Adam")
    last_name: str = Field(min_length=1, max_length=50, example="Abramson")
    model_config = ConfigDict(from_attributes=True) # Enable attribute access for ORM models

class UserCreate(UserBase):
    #Schema for user creation, inherits from UserBase
    password: str = Field(min_length=8, max_length=100, example="Strongpassword123")
    confirm_password: str = Field(min_length=8, max_length=100, example="Strongpassword123")

    @model_validator(mode='after')
    def passwords_match(self) -> "UserCreate":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
    
    @model_validator(mode='after')
    def validate_password_strength(self) -> "UserCreate":
        """Validate password strength requirements"""
        password = self.password
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")
        return self
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "aea79",
                "email": "aea79@example.com",
                "first_name": "Adam",
                "last_name": "Abramson",
                "password": "Strongpassword123",
                "confirm_password": "Strongpassword123"
            }
        }
    }

class UserResponse(BaseModel):
    #Schema for user response
    id: UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True) # Enable attribute access for ORM models

class UserLogin(BaseModel):
    #Schema for user login
    username: str = Field(min_length=3, max_length=50, example="aea79")
    password: str = Field(min_length=8, max_length=100, example="Strongpassword123")
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "aea79",
                "password": "Strongpassword123",
            }
        }
    }

class UserUpdate(BaseModel):
    #Schema for user updates
    username: str = Field(min_length=3, max_length=50, example="aea79")
    email: EmailStr = Field(example="aea79@example.com")
    first_name: str = Field(min_length=1, max_length=50, example="Adam")
    last_name: str = Field(min_length=1, max_length=50, example="Abramson")
    model_config = ConfigDict(from_attributes=True) # Enable attribute access for ORM models

class PasswordUpdate(BaseModel):
    current_password: str = Field(min_length=8, max_length=100, example="Oldpassword123")
    new_password: str = Field(min_length=8, max_length=100, example="Newpassword123")
    confirm_password: str = Field(min_length=8, max_length=100, example="Newpassword123")

    @model_validator(mode='after')
    def passwords_match(self) -> "PasswordUpdate":
        if self.new_password != self.confirm_password:
            raise ValueError("New passwords do not match")
        if self.new_password == self.current_password:
            raise ValueError("New password must be different from the current password")
        return self
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "current_password": "Oldpassword123",
                "new_password": "Newpassword123",
                "confirm_password": "Newpassword123"
            }
        }
    }
       


    
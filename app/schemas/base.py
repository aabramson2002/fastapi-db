from pydantic import BaseModel, EmailStr, Field, ConfigDict, ValidationError, model_validator
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    #Base schema for user creation and response
    username: str = Field(max_length=50, example="aea79")
    email: EmailStr = Field(example="aea79@example.com")
    first_name: str = Field(max_length=50, example="Adam")
    last_name: str = Field(max_length=50, example="Abramson")
    model_config = ConfigDict(from_attributes=True) # Enable attribute access for ORM models

class PasswordMixin(BaseModel):
    #Mixin for password validation
    password: str = Field(min_length=8, max_length=100, example="Strongpassword123")

    @model_validator(mode='before')
    def validate_password(cls, values: dict) -> dict:
        password = values.get('password')
        if not password:
            raise ValueError("Password is required", model=cls) # Not a ValidationError
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")
        return values
    
class UserCreate(UserBase, PasswordMixin):
    #Schema for user creation, inherits from UserBase and PasswordMixin
    pass

class UserLogin(PasswordMixin):
    #Schema for user login, only requires username and password
    username: str = Field(description="Username or email", min_length=3, max_length=50, example="aea79")
    password: str = Field(min_length=8, example="Strongpassword123")

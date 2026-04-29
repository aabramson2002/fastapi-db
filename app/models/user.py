#user model
from datetime import datetime, timedelta, timezone
import uuid
from typing import Optional, Dict, Any

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from passlib.context import CryptContext
from pydantic import ValidationError
import jwt
from app.schemas.base import UserCreate
from app.database import Base #using Base from database instead of from sqlalchemy.orm to avoid circular imports

# Move to config
SECRET_KEY = "your-secret-key"

#defines all of the data fields
class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    # Password hashing context
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # Relationship with Calculations
    """Calculation class connects back to the user"""
    calculations = relationship(
        "Calculation",
        back_populates="user",
        cascade="all, delete, delete-orphan"
    )

    def __init__(self, *args, **kwargs):
        """Initialize a new user, handling password hashing if provided."""
        if "hashed_password" in kwargs:
            kwargs["password"] = kwargs.pop("hashed_password")
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

    def update(self, **kwargs):
        """
        Update user attributes and ensure updated_at is refreshed.
        
        Args:
            **kwargs: Attributes to update
            
        Returns:
            User: The updated user instance
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)
        return self

    @staticmethod
    def hash_password(password: str) -> str:
        return User.pwd_context.hash(password)
    
    def verify_password(self, password: str) -> bool:
        return User.pwd_context.verify(password, self.password_hash)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=30))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")


    @staticmethod
    def verify_token(token: str) -> Optional[UUID]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
            user_id = payload.get("sub")
            if user_id is None:
                return None
            return uuid.UUID(user_id)
        except (jwt.InvalidTokenError, ValidationError):
            """Replaced JWT error from Jose with PyJWT error handling (InvalidTokenError)"""
            return None

    @classmethod
    def register(cls, db, user_data: Dict[str, Any]) -> "User":
        """Registers a new user in the database."""
        try:
            # Validate password length first
            password = user_data.get('password', '')
            if len(password) < 6:  # Strictly less than 6 characters
                raise ValueError("Password must be at least 6 characters long")
            
            # Check if email/username exists
            existing_user = db.query(cls).filter(
                (cls.email == user_data.get('email')) |
                (cls.username == user_data.get('username'))
            ).first()
            
            if existing_user:
                raise ValueError("Username or email already exists")

            # Validate using Pydantic schema
            user_create = UserCreate.model_validate(user_data)
            
            # Create new user instance
            new_user = cls(
                email=user_create.email,
                username=user_create.username,
                first_name=user_create.first_name,
                last_name=user_create.last_name,
                password_hash=cls.hash_password(user_create.password),
                is_active=True
            )
            
            db.add(new_user)
            db.flush()
            return new_user
            
        except ValidationError as e:
            raise ValueError(str(e)) # pragma: no cover
        except ValueError as e:
            raise e
        
    @classmethod
    def authenticate(cls, db, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user and return token with user data."""
        user = db.query(cls).filter(
            (cls.username == username) | (cls.email == username)
        ).first()

        if not user or not user.verify_password(password):
            return None # pragma: no cover

        # Create tokens
        access_token = cls.create_access_token({"sub": str(user.id)})
        refresh_token = cls.create_access_token({"sub": str(user.id), "type": "refresh"})
        
        # Calculate expiration
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)
        
        # Create token response using Pydantic models
        from app.schemas.token import TokenResponse
        token_response = TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_at=expires_at,
            user_id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active
        )

        return token_response.model_dump()
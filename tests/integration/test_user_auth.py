#tests user authentication and password hashing

# tests/integration/test_user_auth.py

import pytest
from uuid import UUID
from datetime import datetime, timezone

import pydantic_core
from sqlalchemy.exc import IntegrityError
from app.models.user import User

def test_password_hashing(db_session, fake_user_data):
    """Test password hashing and verification functionality"""
    original_password = "ValidPass123"  # Use known password for test (8+ chars, upper, lower, digit)
    hashed = User.hash_password(original_password)
    
    user = User(
        email=fake_user_data['email'],
        username=fake_user_data['username'],
        first_name=fake_user_data['first_name'],
        last_name=fake_user_data['last_name'],
        password_hash=hashed
    )
    
    assert user.verify_password(original_password) is True
    assert user.verify_password("WrongPass123") is False
    assert hashed != original_password

def test_user_registration(db_session, fake_user_data):
    """Test user registration process"""
    fake_user_data['password'] = "ValidPass123"
    
    user = User.register(db_session, fake_user_data)
    db_session.commit()
    
    assert user.email == fake_user_data['email']
    assert user.username == fake_user_data['username']
    assert user.first_name == fake_user_data['first_name']
    assert user.last_name == fake_user_data['last_name']
    assert user.is_active is True
    assert user.verify_password("ValidPass123") is True

def test_duplicate_user_registration(db_session):
    """Test registration with duplicate email/username"""
    # First user data
    user1_data = {
        "email": "unique.test@example.com",
        "username": "uniqueuser1",
        "first_name": "John",
        "last_name": "Doe",
        "password": "ValidPass123"
    }
    
    # Second user data with same email
    user2_data = {
        "email": "unique.test@example.com",  # Same email
        "username": "uniqueuser2",
        "first_name": "Jane",
        "last_name": "Smith",
        "password": "ValidPass123"
    }
    
    # Register first user
    first_user = User.register(db_session, user1_data)
    db_session.commit()
    db_session.refresh(first_user)
    
    # Try to register second user with same email
    with pytest.raises(ValueError, match="Username or email already exists"):
        User.register(db_session, user2_data)

def test_user_authentication(db_session, fake_user_data):
    """Test user authentication and token generation"""
    # Use fake_user_data from fixture
    fake_user_data['password'] = "ValidPass123"
    user = User.register(db_session, fake_user_data)
    db_session.commit()
    
    # Test successful authentication
    auth_result = User.authenticate(
        db_session,
        fake_user_data['username'],
        "ValidPass123"
    )
    
    assert auth_result is not None
    assert "access_token" in auth_result
    assert "token_type" in auth_result
    assert auth_result["token_type"] == "bearer"
    assert "first_name" in auth_result  # Check for user fields directly in result
    assert "last_name" in auth_result
    assert "email" in auth_result

def test_unique_email_username(db_session):
    """Test uniqueness constraints for email and username"""
    # Create first user with specific test data
    user1_data = {
        "email": "unique_test@example.com",
        "username": "uniqueuser",
        "first_name": "John",
        "last_name": "Doe",
        "password": "ValidPass123"
    }
    
    # Register and commit first user
    User.register(db_session, user1_data)
    db_session.commit()
    
    # Try to create user with same email
    user2_data = {
        "email": "unique_test@example.com",  # Same email
        "username": "differentuser",
        "first_name": "Jane",
        "last_name": "Smith",
        "password": "ValidPass123"
    }
    
    with pytest.raises(ValueError, match="Username or email already exists"):
        User.register(db_session, user2_data)

def test_short_password_registration(db_session):
    """Test that registration fails with a short password"""
    # Prepare test data with a 6-character password (min is 8)
    test_data = {
        "email": "short.pass@example.com",
        "username": "shortpass",
        "first_name": "John",
        "last_name": "Doe",
        "password": "Short1"  # 6 characters, should fail (min 8)
    }
    
    # Attempt registration with short password
    with pytest.raises(ValueError, match="Password must be at least 8 characters long"):
        User.register(db_session, test_data)

def test_invalid_token():
    """Test that invalid tokens are rejected"""
    invalid_token = "invalid.token.string"
    result = User.verify_token(invalid_token)
    assert result is None

def test_token_creation_and_verification(db_session, fake_user_data):
    """Test token creation and verification"""
    fake_user_data['password'] = "ValidPass123"
    user = User.register(db_session, fake_user_data)
    db_session.commit()
    
    # Create token
    token = User.create_access_token({"sub": str(user.id)})
    
    # Verify token
    decoded_user_id = User.verify_token(token)
    assert decoded_user_id == user.id

def test_authenticate_with_email(db_session, fake_user_data):
    """Test authentication using email instead of username"""
    fake_user_data['password'] = "ValidPass123"
    user = User.register(db_session, fake_user_data)
    db_session.commit()
    
    # Test authentication with email
    auth_result = User.authenticate(
        db_session,
        fake_user_data['email'],  # Using email instead of username
        "ValidPass123"
    )
    
    assert auth_result is not None
    assert "access_token" in auth_result

def test_missing_password_registration(db_session):
    """Test that registration fails when no password is provided."""
    test_data = {
        "email": "no.password@example.com",
        "username": "nopassworduser",
        "first_name": "John",
        "last_name": "Doe",
        # Password is missing
    }
    
    # Password validation will fail during Pydantic validation with a ValueError
    with pytest.raises(ValueError):
        User.register(db_session, test_data)
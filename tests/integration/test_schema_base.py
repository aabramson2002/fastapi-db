#tests pydantic schemas

import pytest
from pydantic import ValidationError
from app.schemas.base import UserBase, PasswordMixin, UserCreate, UserLogin


def test_user_base_valid():
    """Test UserBase with valid data."""
    data = {
        "email": "john.doe@example.com",
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
    }
    user = UserBase(**data)
    assert user.email == "john.doe@example.com"


def test_user_base_invalid_email():
    """Test UserBase with invalid email."""
    data = {
        "email": "invalid-email",
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
    }
    with pytest.raises(ValidationError):
        UserBase(**data)


def test_password_mixin_valid():
    """Test PasswordMixin with valid password."""
    data = {"password": "ValidPass123"}
    password_mixin = PasswordMixin(**data)
    assert password_mixin.password == "ValidPass123"


def test_password_mixin_invalid_short_password():
    """Test PasswordMixin with short password."""
    data = {"password": "Short1"}  # Only 6 characters
    with pytest.raises(ValidationError):
        PasswordMixin(**data)


def test_password_mixin_no_uppercase():
    """Test PasswordMixin with no uppercase letter."""
    data = {"password": "lowercase123"}
    with pytest.raises(ValidationError, match="Password must contain at least one uppercase letter"):
        PasswordMixin(**data)


def test_password_mixin_no_lowercase():
    """Test PasswordMixin with no lowercase letter."""
    data = {"password": "UPPERCASE123"}
    with pytest.raises(ValidationError, match="Password must contain at least one lowercase letter"):
        PasswordMixin(**data)


def test_password_mixin_no_digit():
    """Test PasswordMixin with no digit."""
    data = {"password": "NoDigitsHere"}
    with pytest.raises(ValidationError, match="Password must contain at least one digit"):
        PasswordMixin(**data)


def test_user_create_valid():
    """Test UserCreate with valid data."""
    data = {
        "email": "john.doe@example.com",
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
        "password": "ValidPass123",
    }
    user_create = UserCreate(**data)
    assert user_create.username == "johndoe"
    assert user_create.password == "ValidPass123"


def test_user_create_invalid_password():
    """Test UserCreate with invalid password."""
    data = {
        "email": "john.doe@example.com",
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
        "password": "short",
    }
    with pytest.raises(ValidationError):
        UserCreate(**data)


def test_user_login_valid():
    """Test UserLogin with valid data."""
    data = {"username": "johndoe", "password": "ValidPass123"}
    user_login = UserLogin(**data)
    assert user_login.username == "johndoe"


def test_user_login_invalid_username():
    """Test UserLogin with short username."""
    data = {"username": "jd", "password": "ValidPass123"}
    with pytest.raises(ValidationError):
        UserLogin(**data)


def test_user_login_invalid_password():
    """Test UserLogin with invalid password."""
    data = {"username": "johndoe", "password": "short"}
    with pytest.raises(ValidationError):
        UserLogin(**data)
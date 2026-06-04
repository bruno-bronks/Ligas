"""Auth schemas."""

from typing import Any, Optional

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Login credentials."""
    email: str
    password: str


class RegisterRequest(BaseModel):
    """Registration data."""
    email: str
    password: str
    full_name: Optional[str] = None


class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    """User profile response."""
    id: int
    email: str
    full_name: Optional[str] = None
    role: str
    favorite_teams: Optional[Any] = None
    is_active: bool

    model_config = {"from_attributes": True}

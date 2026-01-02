from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str
    software_experience: Optional[str] = None
    hardware_experience: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    expires_at: datetime


class UserProfile(BaseModel):
    id: str
    email: str
    name: str
    software_experience: Optional[str] = None
    hardware_experience: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class PasswordResetRequest(BaseModel):
    email: str


class PasswordReset(BaseModel):
    token: str
    new_password: str
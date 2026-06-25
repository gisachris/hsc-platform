import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr = Field(..., description="Registered email address")
    password: str = Field(..., description="Complexity validated password")
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
    device_name: Optional[str] = Field(None)
    device_type: Optional[str] = Field("desktop")


class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    avatar_url: Optional[str]
    status: str
    email_verified: bool
    last_login: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 900  # 15 minutes


class SelectOrganizationRequest(BaseModel):
    organization_id: uuid.UUID = Field(...)


class DeviceSessionResponse(BaseModel):
    id: uuid.UUID
    device_name: Optional[str]
    device_type: Optional[str]
    browser: Optional[Optional[str]]
    operating_system: Optional[str]
    ip_address: Optional[str]
    is_active: bool
    created_at: datetime
    last_activity: datetime

    class Config:
        from_attributes = True


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(...)
    new_password: str = Field(...)


class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(...)


class ResetPasswordRequest(BaseModel):
    token: str = Field(...)
    new_password: str = Field(...)

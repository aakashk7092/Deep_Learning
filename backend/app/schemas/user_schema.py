from datetime import datetime
from typing import Optional

from pydantic import AliasChoices, BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRegister(BaseModel):
    full_name: str = Field(..., validation_alias=AliasChoices("full_name", "name"), min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    avatar: Optional[str] = Field(default=None, max_length=500)

    @field_validator("full_name")
    @classmethod
    def clean_full_name(cls, value: str) -> str:
        return " ".join(value.strip().split())


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=128)


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    avatar: Optional[str] = Field(default=None, max_length=500)

    @field_validator("full_name")
    @classmethod
    def clean_full_name(cls, value: Optional[str]) -> Optional[str]:
        return " ".join(value.strip().split()) if value else value


class PasswordChange(BaseModel):
    current_password: str = Field(..., min_length=1, max_length=128)
    new_password: str = Field(..., min_length=8, max_length=128)


class TokenRefresh(BaseModel):
    refresh_token: str = Field(..., min_length=20)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    full_name: str
    email: EmailStr
    avatar: Optional[str] = None
    role: str
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None


class AuthResponse(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

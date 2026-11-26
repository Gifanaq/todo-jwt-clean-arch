from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Credentials(BaseModel):
    login: str = Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_.-]+$")
    password: str = Field(min_length=8, max_length=128)

    @field_validator("login")
    @classmethod
    def normalize_login(cls, value: str) -> str:
        return value.strip().lower()


class AuthResponse(BaseModel):
    user_id: UUID
    login: str
    access_token: str
    token_type: str = "bearer"  # noqa: S105


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    login: str

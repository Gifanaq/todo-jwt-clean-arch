from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from src.core.exceptions import ErrorMessage
from src.domain.entities.todo_item import TODO_TITLE_MAX_LENGTH


class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=TODO_TITLE_MAX_LENGTH)

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError(ErrorMessage.TITLE_CANNOT_BE_EMPTY)
        return normalized


class TodoUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=TODO_TITLE_MAX_LENGTH,
    )
    is_done: bool | None = None

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: str | None) -> str | None:
        if value is None:
            raise ValueError(ErrorMessage.TITLE_CANNOT_BE_NULL)
        normalized = value.strip()
        if not normalized:
            raise ValueError(ErrorMessage.TITLE_CANNOT_BE_EMPTY)
        return normalized

    @field_validator("is_done")
    @classmethod
    def require_boolean(cls, value: bool | None) -> bool:
        if value is None:
            raise ValueError(ErrorMessage.INVALID_TODO_FIELDS)
        return value

    @model_validator(mode="after")
    def require_changes(self) -> "TodoUpdate":
        if not self.model_fields_set:
            raise ValueError(ErrorMessage.TODO_UPDATE_REQUIRED)
        return self


class TodoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    title: str
    is_done: bool
    created_at: datetime
    updated_at: datetime

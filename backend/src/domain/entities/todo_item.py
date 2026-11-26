from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

TODO_TITLE_MAX_LENGTH = 200


@dataclass(frozen=True, slots=True)
class TodoItem:
    id: UUID
    user_id: UUID
    title: str
    is_done: bool
    created_at: datetime
    updated_at: datetime

from dataclasses import dataclass
from typing import Literal
from uuid import UUID


@dataclass(frozen=True, slots=True)
class TokenPayload:
    user_id: UUID
    token_type: Literal["access", "refresh"]
    login: str | None = None

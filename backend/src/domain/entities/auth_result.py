from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class AuthResult:
    user_id: UUID
    login: str
    access_token: str
    refresh_token: str

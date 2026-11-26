from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class IssuedToken:
    value: str
    expires_at: datetime

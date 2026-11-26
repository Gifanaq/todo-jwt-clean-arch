from abc import ABC, abstractmethod
from datetime import datetime

from src.domain.entities.refresh_token import RefreshToken


class RefreshTokenRepository(ABC):
    @abstractmethod
    def get_by_hash(self, token_hash: str) -> RefreshToken | None:
        raise NotImplementedError

    @abstractmethod
    def add(self, refresh_token: RefreshToken) -> None:
        raise NotImplementedError

    @abstractmethod
    def revoke_if_active(self, token_hash: str, revoked_at: datetime) -> bool:
        raise NotImplementedError

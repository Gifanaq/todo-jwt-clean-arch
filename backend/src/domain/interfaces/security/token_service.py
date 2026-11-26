from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.issued_token import IssuedToken
from src.domain.entities.token_payload import TokenPayload


class TokenService(ABC):
    @abstractmethod
    def issue_access(self, user_id: UUID, login: str) -> IssuedToken:
        raise NotImplementedError

    @abstractmethod
    def issue_refresh(self, user_id: UUID) -> IssuedToken:
        raise NotImplementedError

    @abstractmethod
    def decode_access(self, token: str) -> TokenPayload:
        raise NotImplementedError

    @abstractmethod
    def decode_refresh(self, token: str) -> TokenPayload:
        raise NotImplementedError

    @abstractmethod
    def hash_refresh(self, token: str) -> str:
        raise NotImplementedError

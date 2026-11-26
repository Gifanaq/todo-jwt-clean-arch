from datetime import UTC, datetime
from uuid import uuid4

from src.core.exceptions import ConflictError, ErrorMessage, UnauthorizedError
from src.domain.entities.auth_result import AuthResult
from src.domain.entities.refresh_token import RefreshToken
from src.domain.entities.token_payload import TokenPayload
from src.domain.entities.user import User
from src.domain.interfaces.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)
from src.domain.interfaces.repositories.user_repository import UserRepository
from src.domain.interfaces.security.password_hasher import PasswordHasher
from src.domain.interfaces.security.token_service import TokenService


class AuthService:
    def __init__(
        self,
        users: UserRepository,
        refresh_tokens: RefreshTokenRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ) -> None:
        self._users = users
        self._refresh_tokens = refresh_tokens
        self._password_hasher = password_hasher
        self._token_service = token_service

    def register(self, login: str, password: str) -> AuthResult:
        normalized_login = self._normalize_login(login)
        if self._users.get_by_login(normalized_login) is not None:
            raise ConflictError(ErrorMessage.LOGIN_ALREADY_REGISTERED)

        now = datetime.now(UTC)
        user = User(
            id=uuid4(),
            login=normalized_login,
            password_hash=self._password_hasher.hash(password),
            created_at=now,
        )
        self._users.add(user)
        return self._create_session(user, now)

    def login(self, login: str, password: str) -> AuthResult:
        user = self._users.get_by_login(self._normalize_login(login))
        if user is None or not self._password_hasher.verify(
            password,
            user.password_hash,
        ):
            raise UnauthorizedError(ErrorMessage.INVALID_LOGIN_OR_PASSWORD)
        return self._create_session(user, datetime.now(UTC))

    def refresh(self, token: str, payload: TokenPayload) -> AuthResult:
        if payload.token_type != "refresh":  # noqa: S105
            raise UnauthorizedError(ErrorMessage.INVALID_TOKEN_TYPE)

        now = datetime.now(UTC)
        token_hash = self._token_service.hash_refresh(token)
        stored_token = self._refresh_tokens.get_by_hash(token_hash)
        if (
            stored_token is None
            or stored_token.user_id != payload.user_id
            or stored_token.revoked_at is not None
            or not self._is_after(stored_token.expires_at, now)
        ):
            raise UnauthorizedError(ErrorMessage.REFRESH_TOKEN_INACTIVE)

        user = self._users.get_by_id(payload.user_id)
        if user is None:
            raise UnauthorizedError(ErrorMessage.REFRESH_TOKEN_INACTIVE)
        if not self._refresh_tokens.revoke_if_active(token_hash, now):
            raise UnauthorizedError(ErrorMessage.REFRESH_TOKEN_INACTIVE)
        return self._create_session(user, now)

    def logout(self, token: str, payload: TokenPayload) -> None:
        if payload.token_type != "refresh":  # noqa: S105
            raise UnauthorizedError(ErrorMessage.INVALID_TOKEN_TYPE)

        now = datetime.now(UTC)
        token_hash = self._token_service.hash_refresh(token)
        stored_token = self._refresh_tokens.get_by_hash(token_hash)
        if (
            stored_token is None
            or stored_token.user_id != payload.user_id
            or stored_token.revoked_at is not None
            or not self._refresh_tokens.revoke_if_active(token_hash, now)
        ):
            raise UnauthorizedError(ErrorMessage.REFRESH_TOKEN_INACTIVE)

    @staticmethod
    def _normalize_login(login: str) -> str:
        return login.strip().lower()

    @staticmethod
    def _is_after(value: datetime, reference: datetime) -> bool:
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value > reference

    def _create_session(self, user: User, now: datetime) -> AuthResult:
        access_token = self._token_service.issue_access(user.id, user.login)
        refresh_token = self._token_service.issue_refresh(user.id)
        self._refresh_tokens.add(
            RefreshToken(
                id=uuid4(),
                user_id=user.id,
                token_hash=self._token_service.hash_refresh(refresh_token.value),
                expires_at=refresh_token.expires_at,
                revoked_at=None,
                created_at=now,
            ),
        )
        return AuthResult(
            user_id=user.id,
            login=user.login,
            access_token=access_token.value,
            refresh_token=refresh_token.value,
        )

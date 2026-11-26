import hashlib
from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt

from src.core.exceptions import ErrorMessage, UnauthorizedError
from src.domain.entities.issued_token import IssuedToken
from src.domain.entities.token_payload import TokenPayload
from src.domain.interfaces.security.token_service import TokenService


class JWTService(TokenService):
    def __init__(
        self,
        access_secret: str,
        refresh_secret: str,
        access_ttl_minutes: int,
        refresh_ttl_days: int,
    ) -> None:
        self._access_secret = access_secret
        self._refresh_secret = refresh_secret
        self._access_ttl = timedelta(minutes=access_ttl_minutes)
        self._refresh_ttl = timedelta(days=refresh_ttl_days)

    def issue_access(self, user_id: UUID, login: str) -> IssuedToken:
        return self._issue(
            user_id=user_id,
            kind="access",
            secret=self._access_secret,
            lifetime=self._access_ttl,
            login=login,
        )

    def issue_refresh(self, user_id: UUID) -> IssuedToken:
        return self._issue(
            user_id=user_id,
            kind="refresh",
            secret=self._refresh_secret,
            lifetime=self._refresh_ttl,
        )

    def decode_access(self, token: str) -> TokenPayload:
        payload = self._decode(token, self._access_secret, "access")
        login = payload.get("login")
        if not isinstance(login, str) or not login:
            raise UnauthorizedError(ErrorMessage.INVALID_ACCESS_TOKEN)
        return TokenPayload(
            user_id=self._subject(payload),
            token_type="access",  # noqa: S106
            login=login,
        )

    def decode_refresh(self, token: str) -> TokenPayload:
        payload = self._decode(token, self._refresh_secret, "refresh")
        return TokenPayload(
            user_id=self._subject(payload),
            token_type="refresh",  # noqa: S106
        )

    def hash_refresh(self, token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    @staticmethod
    def _issue(
        user_id: UUID,
        kind: str,
        secret: str,
        lifetime: timedelta,
        login: str | None = None,
    ) -> IssuedToken:
        now = datetime.now(UTC)
        expires_at = now + lifetime
        payload: dict[str, str | int | float] = {
            "sub": str(user_id),
            "type": kind,
            "iat": now.timestamp(),
            "exp": expires_at.timestamp(),
        }
        if login is not None:
            payload["login"] = login
        return IssuedToken(
            value=jwt.encode(payload, secret, algorithm="HS256"),
            expires_at=expires_at,
        )

    @staticmethod
    def _decode(token: str, secret: str, expected_type: str) -> dict[str, object]:
        try:
            payload = jwt.decode(
                token,
                secret,
                algorithms=["HS256"],
                options={"require": ["sub", "type", "iat", "exp"]},
            )
        except jwt.InvalidTokenError as error:
            raise UnauthorizedError(ErrorMessage.INVALID_OR_EXPIRED_TOKEN) from error
        if payload.get("type") != expected_type:
            raise UnauthorizedError(ErrorMessage.INVALID_TOKEN_TYPE)
        return payload

    @staticmethod
    def _subject(payload: dict[str, object]) -> UUID:
        subject = payload.get("sub")
        if not isinstance(subject, str):
            raise UnauthorizedError(ErrorMessage.INVALID_TOKEN_SUBJECT)
        try:
            return UUID(subject)
        except ValueError as error:
            raise UnauthorizedError(ErrorMessage.INVALID_TOKEN_SUBJECT) from error

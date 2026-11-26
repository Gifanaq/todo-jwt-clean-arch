from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
import pytest

from src.core.exceptions import UnauthorizedError
from src.infrastructure.adapters.security.jwt_service import JWTService

ACCESS_SECRET = "test-access-secret-at-least-32-characters"  # noqa: S105
REFRESH_SECRET = "test-refresh-secret-at-least-32-characters"  # noqa: S105


@pytest.fixture
def token_service() -> JWTService:
    return JWTService(
        access_secret=ACCESS_SECRET,
        refresh_secret=REFRESH_SECRET,
        access_ttl_minutes=15,
        refresh_ttl_days=30,
    )


def test_tokens_have_distinct_types_and_secrets(token_service: JWTService) -> None:
    user_id = uuid4()
    access = token_service.issue_access(user_id, "alice")
    refresh = token_service.issue_refresh(user_id)
    next_refresh = token_service.issue_refresh(user_id)

    assert token_service.decode_access(access.value).user_id == user_id
    assert token_service.decode_refresh(refresh.value).user_id == user_id
    assert next_refresh.value != refresh.value
    with pytest.raises(UnauthorizedError):
        token_service.decode_access(refresh.value)
    with pytest.raises(UnauthorizedError):
        token_service.decode_refresh(access.value)


def test_expired_token_is_rejected(token_service: JWTService) -> None:
    user_id = uuid4()
    now = datetime.now(UTC)
    expired = jwt.encode(
        {
            "sub": str(user_id),
            "type": "access",
            "login": "alice",
            "iat": int((now - timedelta(minutes=20)).timestamp()),
            "exp": int((now - timedelta(minutes=5)).timestamp()),
        },
        ACCESS_SECRET,
        algorithm="HS256",
    )

    with pytest.raises(UnauthorizedError, match="expired"):
        token_service.decode_access(expired)

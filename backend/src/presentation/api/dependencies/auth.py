from typing import Annotated
from uuid import UUID

from fastapi import Cookie, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.composition import get_token_service
from src.core.exceptions import ErrorMessage, UnauthorizedError
from src.domain.entities.token_payload import TokenPayload
from src.domain.interfaces.security.token_service import TokenService

bearer_scheme = HTTPBearer(auto_error=False)


def get_bearer_token(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
) -> str:
    if credentials is None:
        raise UnauthorizedError(ErrorMessage.BEARER_TOKEN_REQUIRED)
    return credentials.credentials


def get_token_payload(
    token: Annotated[str, Depends(get_bearer_token)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
) -> TokenPayload:
    return token_service.decode_access(token)


def get_current_user_id(
    payload: Annotated[TokenPayload, Depends(get_token_payload)],
) -> UUID:
    return payload.user_id


def get_refresh_token(
    refresh_token: Annotated[str | None, Cookie()] = None,
) -> str:
    if refresh_token is None:
        raise UnauthorizedError(ErrorMessage.REFRESH_TOKEN_REQUIRED)
    return refresh_token


def get_refresh_payload(
    token: Annotated[str, Depends(get_refresh_token)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
) -> TokenPayload:
    return token_service.decode_refresh(token)

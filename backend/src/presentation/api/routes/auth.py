from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from src.application.services.auth_service import AuthService
from src.core.composition import get_auth_service
from src.core.config import Settings, get_settings
from src.core.exceptions import ErrorMessage, UnauthorizedError
from src.domain.entities.token_payload import TokenPayload
from src.presentation.api.dependencies.auth import (
    get_current_user_id,
    get_refresh_payload,
    get_refresh_token,
    get_token_payload,
)
from src.presentation.api.schemas.auth import AuthResponse, Credentials, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


def _set_refresh_cookie(
    response: Response,
    token: str,
    settings: Settings,
) -> None:
    response.set_cookie(
        key="refresh_token",
        value=token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        path="/auth",
        max_age=settings.refresh_ttl_days * 24 * 60 * 60,
    )


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    credentials: Credentials,
    response: Response,
    service: Annotated[AuthService, Depends(get_auth_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> AuthResponse:
    result = service.register(credentials.login, credentials.password)
    _set_refresh_cookie(response, result.refresh_token, settings)
    return AuthResponse(
        user_id=result.user_id,
        login=result.login,
        access_token=result.access_token,
    )


@router.post("/login")
def login(
    credentials: Credentials,
    response: Response,
    service: Annotated[AuthService, Depends(get_auth_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> AuthResponse:
    result = service.login(credentials.login, credentials.password)
    _set_refresh_cookie(response, result.refresh_token, settings)
    return AuthResponse(
        user_id=result.user_id,
        login=result.login,
        access_token=result.access_token,
    )


@router.post("/refresh")
def refresh(
    response: Response,
    token: Annotated[str, Depends(get_refresh_token)],
    payload: Annotated[TokenPayload, Depends(get_refresh_payload)],
    service: Annotated[AuthService, Depends(get_auth_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> AuthResponse:
    result = service.refresh(token, payload)
    _set_refresh_cookie(response, result.refresh_token, settings)
    return AuthResponse(
        user_id=result.user_id,
        login=result.login,
        access_token=result.access_token,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response,
    token: Annotated[str, Depends(get_refresh_token)],
    payload: Annotated[TokenPayload, Depends(get_refresh_payload)],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> Response:
    service.logout(token, payload)
    response.delete_cookie(key="refresh_token", path="/auth")
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get("/me")
def me(
    token_payload: Annotated[TokenPayload, Depends(get_token_payload)],
    user_id: Annotated[UUID, Depends(get_current_user_id)],
) -> UserResponse:
    if token_payload.login is None:
        raise UnauthorizedError(ErrorMessage.INVALID_ACCESS_TOKEN)
    return UserResponse(user_id=user_id, login=token_payload.login)

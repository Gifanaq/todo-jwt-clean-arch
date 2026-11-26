from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.services.auth_service import AuthService
from src.application.services.todo_service import TodoService
from src.core.config import Settings, get_settings
from src.domain.interfaces.security.token_service import TokenService
from src.infrastructure.adapters.repositories.refresh_token_repository import (
    SQLAlchemyRefreshTokenRepository,
)
from src.infrastructure.adapters.repositories.todo_repository import (
    SQLAlchemyTodoRepository,
)
from src.infrastructure.adapters.repositories.user_repository import (
    SQLAlchemyUserRepository,
)
from src.infrastructure.adapters.security.jwt_service import JWTService
from src.infrastructure.adapters.security.password_hasher import Pbkdf2PasswordHasher
from src.infrastructure.db.session import get_db


def get_token_service(settings: Settings = Depends(get_settings)) -> TokenService:
    return JWTService(
        access_secret=settings.access_secret.get_secret_value(),
        refresh_secret=settings.refresh_secret.get_secret_value(),
        access_ttl_minutes=settings.access_ttl_minutes,
        refresh_ttl_days=settings.refresh_ttl_days,
    )


def get_auth_service(
    session: Session = Depends(get_db),
    token_service: TokenService = Depends(get_token_service),
) -> AuthService:
    return AuthService(
        users=SQLAlchemyUserRepository(session),
        refresh_tokens=SQLAlchemyRefreshTokenRepository(session),
        password_hasher=Pbkdf2PasswordHasher(),
        token_service=token_service,
    )


def get_todo_service(session: Session = Depends(get_db)) -> TodoService:
    return TodoService(SQLAlchemyTodoRepository(session))

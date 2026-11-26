from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.exceptions import ConflictError, ErrorMessage
from src.domain.entities.user import User
from src.domain.interfaces.repositories.user_repository import UserRepository
from src.infrastructure.db.models.user_model import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, user_id: UUID) -> User | None:
        model = self._session.get(UserModel, user_id)
        return self._to_entity(model) if model is not None else None

    def get_by_login(self, login: str) -> User | None:
        model = self._session.scalar(
            select(UserModel).where(UserModel.login == login),
        )
        return self._to_entity(model) if model is not None else None

    def add(self, user: User) -> None:
        model = UserModel(
            id=user.id,
            login=user.login,
            password_hash=user.password_hash,
            created_at=user.created_at,
        )
        try:
            with self._session.begin_nested():
                self._session.add(model)
                self._session.flush()
        except IntegrityError as error:
            raise ConflictError(ErrorMessage.LOGIN_ALREADY_REGISTERED) from error

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        return User(
            id=model.id,
            login=model.login,
            password_hash=model.password_hash,
            created_at=model.created_at,
        )

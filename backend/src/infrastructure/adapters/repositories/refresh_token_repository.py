from datetime import datetime
from typing import Any, cast

from sqlalchemy import select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.orm import Session

from src.domain.entities.refresh_token import RefreshToken
from src.domain.interfaces.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)
from src.infrastructure.db.models.refresh_token_model import RefreshTokenModel


class SQLAlchemyRefreshTokenRepository(RefreshTokenRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_hash(self, token_hash: str) -> RefreshToken | None:
        model = self._session.scalar(
            select(RefreshTokenModel).where(
                RefreshTokenModel.token_hash == token_hash,
            ),
        )
        return self._to_entity(model) if model is not None else None

    def add(self, refresh_token: RefreshToken) -> None:
        self._session.add(
            RefreshTokenModel(
                id=refresh_token.id,
                user_id=refresh_token.user_id,
                token_hash=refresh_token.token_hash,
                expires_at=refresh_token.expires_at,
                revoked_at=refresh_token.revoked_at,
                created_at=refresh_token.created_at,
            ),
        )
        self._session.flush()

    def revoke_if_active(self, token_hash: str, revoked_at: datetime) -> bool:
        result = cast(
            CursorResult[Any],
            self._session.execute(
                update(RefreshTokenModel)
                .where(
                    RefreshTokenModel.token_hash == token_hash,
                    RefreshTokenModel.revoked_at.is_(None),
                    RefreshTokenModel.expires_at > revoked_at,
                )
                .values(revoked_at=revoked_at),
            ),
        )
        return result.rowcount == 1

    @staticmethod
    def _to_entity(model: RefreshTokenModel) -> RefreshToken:
        return RefreshToken(
            id=model.id,
            user_id=model.user_id,
            token_hash=model.token_hash,
            expires_at=model.expires_at,
            revoked_at=model.revoked_at,
            created_at=model.created_at,
        )

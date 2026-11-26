from typing import Any, cast
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.orm import Session

from src.domain.entities.todo_item import TodoItem
from src.domain.interfaces.repositories.todo_repository import TodoRepository
from src.infrastructure.db.models.todo_model import TodoModel


class SQLAlchemyTodoRepository(TodoRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_by_user(self, user_id: UUID) -> list[TodoItem]:
        models = self._session.scalars(
            select(TodoModel)
            .where(TodoModel.user_id == user_id)
            .order_by(TodoModel.created_at, TodoModel.id),
        )
        return [self._to_entity(model) for model in models]

    def get_by_id_and_user(self, todo_id: UUID, user_id: UUID) -> TodoItem | None:
        model = self._session.scalar(
            select(TodoModel).where(
                TodoModel.id == todo_id,
                TodoModel.user_id == user_id,
            ),
        )
        return self._to_entity(model) if model is not None else None

    def add(self, todo: TodoItem) -> None:
        self._session.add(
            TodoModel(
                id=todo.id,
                user_id=todo.user_id,
                title=todo.title,
                is_done=todo.is_done,
                created_at=todo.created_at,
                updated_at=todo.updated_at,
            ),
        )
        self._session.flush()

    def update(self, todo: TodoItem) -> bool:
        result = cast(
            CursorResult[Any],
            self._session.execute(
                update(TodoModel)
                .where(
                    TodoModel.id == todo.id,
                    TodoModel.user_id == todo.user_id,
                )
                .values(
                    title=todo.title,
                    is_done=todo.is_done,
                    updated_at=todo.updated_at,
                ),
            ),
        )
        return result.rowcount == 1

    def delete(self, todo: TodoItem) -> bool:
        result = cast(
            CursorResult[Any],
            self._session.execute(
                delete(TodoModel).where(
                    TodoModel.id == todo.id,
                    TodoModel.user_id == todo.user_id,
                ),
            ),
        )
        return result.rowcount == 1

    @staticmethod
    def _to_entity(model: TodoModel) -> TodoItem:
        return TodoItem(
            id=model.id,
            user_id=model.user_id,
            title=model.title,
            is_done=model.is_done,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

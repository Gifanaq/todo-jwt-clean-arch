from collections.abc import Mapping
from dataclasses import replace
from datetime import UTC, datetime
from uuid import UUID, uuid4

from src.core.exceptions import ErrorMessage, InvalidInputError, NotFoundError
from src.domain.entities.todo_item import TODO_TITLE_MAX_LENGTH, TodoItem
from src.domain.interfaces.repositories.todo_repository import TodoRepository


class TodoService:
    def __init__(self, todos: TodoRepository) -> None:
        self._todos = todos

    def list_for_user(self, user_id: UUID) -> list[TodoItem]:
        return self._todos.list_by_user(user_id)

    def create(self, user_id: UUID, title: str) -> TodoItem:
        normalized_title = title.strip()
        if not normalized_title or len(normalized_title) > TODO_TITLE_MAX_LENGTH:
            raise InvalidInputError(ErrorMessage.TODO_TITLE_LENGTH)

        now = datetime.now(UTC)
        todo = TodoItem(
            id=uuid4(),
            user_id=user_id,
            title=normalized_title,
            is_done=False,
            created_at=now,
            updated_at=now,
        )
        self._todos.add(todo)
        return todo

    def update(
        self,
        todo_id: UUID,
        user_id: UUID,
        changes: Mapping[str, object],
    ) -> TodoItem:
        if not changes:
            raise InvalidInputError(ErrorMessage.TODO_FIELDS_REQUIRED)
        todo = self._todos.get_by_id_and_user(todo_id, user_id)
        if todo is None:
            raise NotFoundError(ErrorMessage.TODO_NOT_FOUND)

        title = changes.get("title", todo.title)
        is_done = changes.get("is_done", todo.is_done)
        if not isinstance(title, str) or not isinstance(is_done, bool):
            raise InvalidInputError(ErrorMessage.INVALID_TODO_FIELDS)
        normalized_title = title.strip()
        if not normalized_title or len(normalized_title) > TODO_TITLE_MAX_LENGTH:
            raise InvalidInputError(ErrorMessage.TODO_TITLE_LENGTH)

        updated = replace(
            todo,
            title=normalized_title,
            is_done=is_done,
            updated_at=datetime.now(UTC),
        )
        if not self._todos.update(updated):
            raise NotFoundError(ErrorMessage.TODO_NOT_FOUND)
        return updated

    def delete(self, todo_id: UUID, user_id: UUID) -> None:
        todo = self._todos.get_by_id_and_user(todo_id, user_id)
        if todo is None or not self._todos.delete(todo):
            raise NotFoundError(ErrorMessage.TODO_NOT_FOUND)

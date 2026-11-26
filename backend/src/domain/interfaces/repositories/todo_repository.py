from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.todo_item import TodoItem


class TodoRepository(ABC):
    @abstractmethod
    def list_by_user(self, user_id: UUID) -> list[TodoItem]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id_and_user(self, todo_id: UUID, user_id: UUID) -> TodoItem | None:
        raise NotImplementedError

    @abstractmethod
    def add(self, todo: TodoItem) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, todo: TodoItem) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, todo: TodoItem) -> bool:
        raise NotImplementedError

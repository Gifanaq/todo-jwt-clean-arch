from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from src.application.services.todo_service import TodoService
from src.core.composition import get_todo_service
from src.presentation.api.dependencies.auth import get_current_user_id
from src.presentation.api.schemas.todo import TodoCreate, TodoResponse, TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("")
def list_todos(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    service: Annotated[TodoService, Depends(get_todo_service)],
) -> list[TodoResponse]:
    return [
        TodoResponse.model_validate(todo) for todo in service.list_for_user(user_id)
    ]


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def create_todo(
    data: TodoCreate,
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    service: Annotated[TodoService, Depends(get_todo_service)],
) -> TodoResponse:
    return TodoResponse.model_validate(service.create(user_id, data.title))


@router.patch("/{todo_id}")
def update_todo(
    todo_id: UUID,
    data: TodoUpdate,
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    service: Annotated[TodoService, Depends(get_todo_service)],
) -> TodoResponse:
    return TodoResponse.model_validate(
        service.update(
            todo_id,
            user_id,
            data.model_dump(exclude_unset=True),
        ),
    )


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: UUID,
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    service: Annotated[TodoService, Depends(get_todo_service)],
) -> Response:
    service.delete(todo_id, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

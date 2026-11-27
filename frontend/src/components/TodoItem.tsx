import { useState, type SubmitEvent } from 'react';

import type { Todo } from '../api/todos';
import { LoadingSpinner } from './LoadingSpinner';

type TodoItemProps = {
  todo: Todo;
  isPending: boolean;
  onToggle: (todo: Todo) => void;
  onDelete: (todoId: string) => void;
  onSave: (todoId: string, title: string) => Promise<boolean>;
  onValidationError: (message: string) => void;
  onClearError: () => void;
};

function EditIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="m15 5 4 4M4 20l4.3-.9L19 8.4a2.1 2.1 0 0 0-3-3L5.3 16.1 4 20Z" />
    </svg>
  );
}

function DeleteIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M4 7h16M10 11v6m4-6v6M6 7l1 14h10l1-14M9 7V4h6v3" />
    </svg>
  );
}

export function TodoItem({
  todo,
  isPending,
  onToggle,
  onDelete,
  onSave,
  onValidationError,
  onClearError,
}: TodoItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);

  async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();
    const title = editTitle.trim();

    if (!title) {
      onValidationError('Название задачи не может быть пустым.');
      return;
    }

    if (await onSave(todo.id, title)) {
      setIsEditing(false);
    }
  }

  if (isEditing) {
    return (
      <li className="todo-row">
        <form className="todo-edit-form" onSubmit={handleSubmit}>
          <input
            aria-label="Название задачи"
            autoFocus
            maxLength={200}
            value={editTitle}
            onChange={(event) => setEditTitle(event.target.value)}
            disabled={isPending}
          />
          <button type="submit" disabled={isPending}>
            Сохранить
          </button>
          <button
            className="edit-cancel"
            type="button"
            onClick={() => {
              setIsEditing(false);
              onClearError();
            }}
            disabled={isPending}
          >
            Отмена
          </button>
          {isPending && (
            <LoadingSpinner
              className="loading-spinner--compact"
              label="Сохраняем задачу"
            />
          )}
        </form>
      </li>
    );
  }

  return (
    <li className="todo-row">
      <label className={`todo-title${todo.is_done ? ' todo-done' : ''}`}>
        <input
          type="checkbox"
          checked={todo.is_done}
          onChange={() => onToggle(todo)}
          disabled={isPending}
          aria-label={`Отметить выполненной: ${todo.title}`}
        />
        <span>{todo.title}</span>
      </label>
      <div className="todo-actions">
        {isPending && (
          <LoadingSpinner
            className="loading-spinner--compact"
            label="Обновляем задачу"
          />
        )}
        <button
          className="todo-icon-button"
          type="button"
          aria-label={`Редактировать: ${todo.title}`}
          onClick={() => {
            setEditTitle(todo.title);
            setIsEditing(true);
            onClearError();
          }}
          disabled={isPending}
        >
          <EditIcon />
        </button>
        <button
          className="todo-icon-button"
          type="button"
          aria-label={`Удалить: ${todo.title}`}
          onClick={() => onDelete(todo.id)}
          disabled={isPending}
        >
          <DeleteIcon />
        </button>
      </div>
    </li>
  );
}

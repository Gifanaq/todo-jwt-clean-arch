import type { SubmitEvent } from 'react';

import { LoadingSpinner } from './LoadingSpinner';

type TodoCreateFormProps = {
  title: string;
  isCreating: boolean;
  onTitleChange: (title: string) => void;
  onSubmit: (event: SubmitEvent<HTMLFormElement>) => void;
};

export function TodoCreateForm({
  title,
  isCreating,
  onTitleChange,
  onSubmit,
}: TodoCreateFormProps) {
  return (
    <form className="todo-create-form" onSubmit={onSubmit}>
      <input
        aria-label="Новая задача"
        maxLength={200}
        placeholder="Что нужно сделать?"
        value={title}
        onChange={(event) => onTitleChange(event.target.value)}
        disabled={isCreating}
      />
      <button type="submit" disabled={isCreating || !title.trim()}>
        {isCreating && (
          <LoadingSpinner className="loading-spinner--inline" />
        )}
        {isCreating ? 'Добавляем…' : 'Добавить'}
      </button>
    </form>
  );
}

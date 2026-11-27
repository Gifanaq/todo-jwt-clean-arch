import type { Todo } from '../api/todos';
import { TodoItem } from './TodoItem';

type TodoListProps = {
  todos: Todo[];
  pendingIds: ReadonlySet<string>;
  onToggle: (todo: Todo) => void;
  onDelete: (todoId: string) => void;
  onSave: (todoId: string, title: string) => Promise<boolean>;
  onValidationError: (message: string) => void;
  onClearError: () => void;
};

export function TodoList({
  todos,
  pendingIds,
  onToggle,
  onDelete,
  onSave,
  onValidationError,
  onClearError,
}: TodoListProps) {
  return (
    <ul className="todo-list">
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          isPending={pendingIds.has(todo.id)}
          onToggle={onToggle}
          onDelete={onDelete}
          onSave={onSave}
          onValidationError={onValidationError}
          onClearError={onClearError}
        />
      ))}
    </ul>
  );
}

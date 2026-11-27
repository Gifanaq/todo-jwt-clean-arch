import { useEffect, useMemo, useState, type SubmitEvent } from 'react';

import {
  createTodo,
  deleteTodo,
  getTodos,
  updateTodo,
} from '../api/todos';
import { getApiErrorMessage } from '../api/errorMessage';
import type { Todo } from '../api/todos';
import { useAuth } from '../auth/AuthContext';
import { TodoCreateForm } from '../components/TodoCreateForm';
import { TodoFilters, type TodoFilter } from '../components/TodoFilters';
import { TodoHeader } from '../components/TodoHeader';
import { TodoList } from '../components/TodoList';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { withMinimumLoading } from '../utils/withMinimumLoading';

type TodoLoadState = 'loading' | 'ready' | 'error';

export function TodosPage() {
  const { user, logout } = useAuth();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loadState, setLoadState] = useState<TodoLoadState>('loading');
  const [filter, setFilter] = useState<TodoFilter>('all');
  const [newTitle, setNewTitle] = useState('');
  const [pendingIds, setPendingIds] = useState<Set<string>>(() => new Set());
  const [isCreating, setIsCreating] = useState(false);
  const [isLoggingOut, setIsLoggingOut] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    withMinimumLoading(getTodos)
      .then((items) => {
        if (active) {
          setTodos(items);
          setLoadState('ready');
        }
      })
      .catch((requestError: unknown) => {
        if (active) {
          setError(getApiErrorMessage(requestError));
          setLoadState('error');
        }
      });

    return () => {
      active = false;
    };
  }, []);

  const activeCount = useMemo(
    () => todos.filter((todo) => !todo.is_done).length,
    [todos],
  );

  const visibleTodos = useMemo(
    () =>
      todos.filter((todo) => {
        if (filter === 'active') {
          return !todo.is_done;
        }
        if (filter === 'completed') {
          return todo.is_done;
        }
        return true;
      }),
    [filter, todos],
  );

  async function handleRetryLoad() {
    setError(null);
    setLoadState('loading');

    try {
      setTodos(await withMinimumLoading(getTodos));
      setLoadState('ready');
    } catch (requestError) {
      setError(getApiErrorMessage(requestError));
      setLoadState('error');
    }
  }

  async function handleCreate(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();
    const title = newTitle.trim();

    if (!title) {
      setError('Введите название задачи.');
      return;
    }

    setIsCreating(true);
    setError(null);

    try {
      const created = await withMinimumLoading(() => createTodo(title));
      setTodos((current) => [...current, created]);
      setNewTitle('');
    } catch (requestError) {
      setError(getApiErrorMessage(requestError));
    } finally {
      setIsCreating(false);
    }
  }

  async function runItemAction<Result>(
    todoId: string,
    request: () => Promise<Result>,
    onSuccess: (result: Result) => void,
  ): Promise<boolean> {
    setError(null);
    setPendingIds((current) => new Set(current).add(todoId));

    try {
      const result = await withMinimumLoading(request);
      onSuccess(result);
      return true;
    } catch (requestError) {
      setError(getApiErrorMessage(requestError));
      return false;
    } finally {
      setPendingIds((current) => {
        const next = new Set(current);
        next.delete(todoId);
        return next;
      });
    }
  }

  function handleToggle(todo: Todo) {
    void runItemAction(
      todo.id,
      () =>
        updateTodo(todo.id, {
          is_done: !todo.is_done,
        }),
      (updated) => {
        setTodos((current) =>
          current.map((item) => (item.id === updated.id ? updated : item)),
        );
      },
    );
  }

  function handleDelete(todoId: string) {
    void runItemAction(
      todoId,
      () => deleteTodo(todoId),
      () => {
        setTodos((current) => current.filter((todo) => todo.id !== todoId));
      },
    );
  }

  function handleSave(todoId: string, title: string) {
    return runItemAction(
      todoId,
      () => updateTodo(todoId, { title }),
      (updated) => {
        setTodos((current) =>
          current.map((item) => (item.id === updated.id ? updated : item)),
        );
      },
    );
  }

  async function handleLogout() {
    setError(null);
    setIsLoggingOut(true);

    try {
      await logout();
    } catch (requestError) {
      setError(getApiErrorMessage(requestError));
    } finally {
      setIsLoggingOut(false);
    }
  }

  return (
    <main className="todo-page">
      <div className="todo-shell">
        <TodoHeader
          login={user?.login}
          isLoggingOut={isLoggingOut}
          onLogout={() => void handleLogout()}
        />

        <TodoCreateForm
          title={newTitle}
          isCreating={isCreating}
          onTitleChange={setNewTitle}
          onSubmit={(event) => void handleCreate(event)}
        />

        <div className="todo-toolbar">
          <TodoFilters filter={filter} onChange={setFilter} />
          <p className="todo-remaining">Осталось: {activeCount}</p>
        </div>

        {error && (
          <div className="todo-error" role="alert">
            <span>{error}</span>
            {loadState === 'error' && (
              <button type="button" onClick={() => void handleRetryLoad()}>
                Повторить
              </button>
            )}
          </div>
        )}

        {loadState === 'loading' ? (
          <div className="todo-empty" aria-live="polite">
            <LoadingSpinner className="loading-spinner--inline" />
            Загружаем задачи…
          </div>
        ) : loadState === 'error' ? null : visibleTodos.length === 0 ? (
          <p className="todo-empty">
            {todos.length === 0
              ? 'Пока нет задач. Добавьте первую выше.'
              : 'В этом списке пока нет задач.'}
          </p>
        ) : (
          <TodoList
            todos={visibleTodos}
            pendingIds={pendingIds}
            onToggle={handleToggle}
            onDelete={handleDelete}
            onSave={handleSave}
            onValidationError={setError}
            onClearError={() => setError(null)}
          />
        )}
      </div>
    </main>
  );
}

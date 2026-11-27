import { LoadingSpinner } from './LoadingSpinner';

type TodoHeaderProps = {
  login?: string;
  isLoggingOut: boolean;
  onLogout: () => void;
};

export function TodoHeader({
  login,
  isLoggingOut,
  onLogout,
}: TodoHeaderProps) {
  return (
    <header className="todo-header">
      <h1>Мои задачи</h1>
      <div className="todo-account">
        <span>{login}</span>
        <button
          className="logout-button"
          type="button"
          onClick={onLogout}
          disabled={isLoggingOut}
        >
          {isLoggingOut && (
            <LoadingSpinner className="loading-spinner--inline" />
          )}
          {isLoggingOut ? 'Выходим…' : 'Выйти'}
        </button>
      </div>
    </header>
  );
}

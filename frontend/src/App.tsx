import { useAuth } from './auth/AuthContext';
import { LoadingSpinner } from './components/LoadingSpinner';
import { AuthPage } from './pages/AuthPage';
import { TodosPage } from './pages/TodosPage';

function App() {
  const { status, error, retrySession } = useAuth();

  if (status === 'loading') {
    return (
      <main className="state-page">
        <section className="state-card" aria-live="polite">
          <LoadingSpinner label="Проверяем сессию" />
          <h1>Проверяем сессию</h1>
        </section>
      </main>
    );
  }

  if (status === 'error') {
    return (
      <main className="state-page">
        <section className="state-card">
          <h1>Не удалось подключиться</h1>
          <p role="alert">{error ?? 'Попробуйте повторить запрос.'}</p>
          <button
            className="state-retry"
            type="button"
            onClick={() => void retrySession()}
          >
            Повторить
          </button>
        </section>
      </main>
    );
  }

  if (status === 'unauthenticated') {
    return <AuthPage />;
  }

  return <TodosPage />;
}

export default App;

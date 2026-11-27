import { useState, type SubmitEvent } from 'react';

import { getApiErrorMessage } from '../api/errorMessage';
import { useAuth } from '../auth/AuthContext';
import { LoadingSpinner } from '../components/LoadingSpinner';

type AuthMode = 'login' | 'register';

export function AuthPage() {
  const { login, register } = useAuth();
  const [mode, setMode] = useState<AuthMode>('login');
  const [loginValue, setLoginValue] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirmation, setPasswordConfirmation] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const isRegister = mode === 'register';

  async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);

    if (isRegister && password !== passwordConfirmation) {
      setError('Пароли не совпадают.');
      return;
    }

    setIsSubmitting(true);

    try {
      if (isRegister) {
        await register(loginValue, password);
      } else {
        await login(loginValue, password);
      }
    } catch (requestError) {
      setError(getApiErrorMessage(requestError));
    } finally {
      setIsSubmitting(false);
    }
  }

  function changeMode(nextMode: AuthMode) {
    setMode(nextMode);
    setError(null);
  }

  return (
    <main className="auth-page">
      <section className="auth-card" aria-labelledby="auth-title">
        <h1 id="auth-title">{isRegister ? 'Регистрация' : 'Вход'}</h1>
        <p className="auth-subtitle">
          {isRegister
            ? 'Создайте аккаунт за пару секунд'
            : 'Войдите, чтобы увидеть свои задачи'}
        </p>

        <form className="auth-form" onSubmit={handleSubmit}>
          <label htmlFor="login">Логин</label>
          <input
            id="login"
            name="login"
            type="text"
            autoComplete="username"
            minLength={3}
            maxLength={50}
            pattern="[A-Za-z0-9_.-]+"
            required
            value={loginValue}
            onChange={(event) => setLoginValue(event.target.value)}
            disabled={isSubmitting}
          />

          <label htmlFor="password">Пароль</label>
          <input
            id="password"
            name="password"
            type="password"
            autoComplete={isRegister ? 'new-password' : 'current-password'}
            minLength={8}
            maxLength={128}
            required
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            disabled={isSubmitting}
          />

          {isRegister && (
            <>
              <label htmlFor="password-confirmation">Повторите пароль</label>
              <input
                id="password-confirmation"
                name="password-confirmation"
                type="password"
                autoComplete="new-password"
                minLength={8}
                maxLength={128}
                required
                value={passwordConfirmation}
                onChange={(event) =>
                  setPasswordConfirmation(event.target.value)
                }
                disabled={isSubmitting}
              />
            </>
          )}

          {error && (
            <p className="auth-error" role="alert">
              {error}
            </p>
          )}

          <button
            className="auth-submit"
            type="submit"
            disabled={isSubmitting}
          >
            {isSubmitting && (
              <LoadingSpinner className="loading-spinner--inline" />
            )}
            {isSubmitting
              ? 'Подождите…'
              : isRegister
                ? 'Создать аккаунт'
                : 'Войти'}
          </button>
        </form>

        <p className="auth-switch">
          {isRegister ? 'Уже есть аккаунт?' : 'Нет аккаунта?'}{' '}
          <button
            className="auth-link"
            type="button"
            onClick={() => changeMode(isRegister ? 'login' : 'register')}
            disabled={isSubmitting}
          >
            {isRegister ? 'Войти' : 'Зарегистрироваться'}
          </button>
        </p>
      </section>
    </main>
  );
}

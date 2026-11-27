import axios from 'axios';
import {
  useCallback,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react';


import { getApiErrorMessage } from '../api/errorMessage';
import { subscribeToSessionExpiry } from '../api/sessionEvents';
import {
  login as loginRequest,
  logout as logoutRequest,
  refreshSession,
} from '../api/auth';
import { register as registerRequest } from '../api/register';
import type { AuthResponse } from '../api/types';
import { withMinimumLoading } from '../utils/withMinimumLoading';
import { AuthContext } from './AuthContext';
import type { AuthStatus, AuthUser } from './AuthContext';

type AuthProviderProps = {
  children: ReactNode;
};

function toAuthUser(response: AuthResponse): AuthUser {
  return {
    user_id: response.user_id,
    login: response.login,
  };
}

async function loadSession(): Promise<AuthResponse | null> {
  try {
    return await refreshSession();
  } catch (sessionError) {
    if (
      axios.isAxiosError<unknown>(sessionError) &&
      sessionError.response?.status === 401
    ) {
      return null;
    }

    throw sessionError;
  }
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [status, setStatus] = useState<AuthStatus>('loading');
  const [user, setUser] = useState<AuthUser | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(
    () =>
      subscribeToSessionExpiry(() => {
        setUser(null);
        setError(null);
        setStatus('unauthenticated');
      }),
    [],
  );

  const retrySession = useCallback(async () => {
    setStatus('loading');
    setError(null);

    try {
      const response = await withMinimumLoading(loadSession);
      if (!response) {
        setUser(null);
        setStatus('unauthenticated');
        return;
      }

      setUser(toAuthUser(response));
      setStatus('authenticated');
    } catch (sessionError) {
      setUser(null);
      setError(getApiErrorMessage(sessionError));
      setStatus('error');
    }
  }, []);

  useEffect(() => {
    let active = true;

    void withMinimumLoading(loadSession)
      .then((response) => {
        if (!active) {
          return;
        }

        if (!response) {
          setUser(null);
          setStatus('unauthenticated');
          return;
        }

        setUser(toAuthUser(response));
        setStatus('authenticated');
      })
      .catch((sessionError: unknown) => {
        if (!active) {
          return;
        }

        setUser(null);
        setError(getApiErrorMessage(sessionError));
        setStatus('error');
      });

    return () => {
      active = false;
    };
  }, []);

  const authenticate = useCallback(
    async (request: () => Promise<AuthResponse>) => {
      setError(null);

      try {
        const response = await withMinimumLoading(request);
        setUser(toAuthUser(response));
        setStatus('authenticated');
      } catch (authError) {
        setError(getApiErrorMessage(authError));
        throw authError;
      }
    },
    [],
  );

  const login = useCallback(
    (loginValue: string, password: string) =>
      authenticate(() => loginRequest(loginValue, password)),
    [authenticate],
  );

  const register = useCallback(
    (loginValue: string, password: string) =>
      authenticate(() => registerRequest(loginValue, password)),
    [authenticate],
  );

  const logout = useCallback(async () => {
    setError(null);

    try {
      await withMinimumLoading(logoutRequest);
      setUser(null);
      setStatus('unauthenticated');
    } catch (logoutError) {
      setError(getApiErrorMessage(logoutError));
      throw logoutError;
    }
  }, []);

  const value = useMemo(
    () => ({
      status,
      user,
      error,
      login,
      register,
      logout,
      retrySession,
    }),
    [status, user, error, login, register, logout, retrySession],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

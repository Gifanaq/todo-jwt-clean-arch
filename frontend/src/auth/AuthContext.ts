import { createContext, useContext } from 'react';

import type { AuthResponse } from '../api/types';

export type AuthUser = Pick<AuthResponse, 'user_id' | 'login'>;
export type AuthStatus =
  | 'loading'
  | 'authenticated'
  | 'unauthenticated'
  | 'error';

export type AuthContextValue = {
  status: AuthStatus;
  user: AuthUser | null;
  error: string | null;
  login: (login: string, password: string) => Promise<void>;
  register: (login: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  retrySession: () => Promise<void>;
};

export const AuthContext = createContext<AuthContextValue | null>(null);

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }

  return context;
}

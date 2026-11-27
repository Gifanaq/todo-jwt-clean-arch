import { setAccessToken } from './accessToken';
import { api } from './axios';
import type { AuthResponse } from './types';

export { refreshSession } from './refresh';

export async function login(login: string, password: string) {
  const { data } = await api.post<AuthResponse>('/auth/login', {
    login,
    password,
  });

  setAccessToken(data.access_token);
  return data;
}

export async function logout() {
  await api.post('/auth/logout');
  setAccessToken(null);
}
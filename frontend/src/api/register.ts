import { setAccessToken } from './accessToken';
import { api } from './axios';
import type { AuthResponse } from './types';

export async function register(login: string, password: string) {
  const response = await api.post<AuthResponse>('/auth/register', {
    login,
    password,
  });

  setAccessToken(response.data.access_token);
  return response.data;
}
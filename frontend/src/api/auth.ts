import { api, setAccessToken } from './axios';

type AuthResponse = {
  user_id: string;
  login: string;
  access_token: string;
  token_type: 'bearer';
};

export async function login(login: string, password: string) {
  const { data } = await api.post<AuthResponse>('/auth/login', {
    login,
    password,
  });

  setAccessToken(data.access_token);
  return data;
}
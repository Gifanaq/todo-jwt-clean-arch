import axios from 'axios';

import { setAccessToken } from './accessToken';
import type { AuthResponse } from './types';

const refreshApi = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
});

let refreshPromise: Promise<AuthResponse> | null = null;

export function refreshSession(): Promise<AuthResponse> {
  if (!refreshPromise) {
    refreshPromise = refreshApi
      .post<AuthResponse>('/auth/refresh')
      .then(({ data }) => {
        setAccessToken(data.access_token);
        return data;
      })
      .catch((error: unknown) => {
        if (
          axios.isAxiosError<unknown>(error) &&
          error.response?.status === 401
        ) {
          setAccessToken(null);
        }

        throw error;
      })
      .finally(() => {
        refreshPromise = null;
      });
  }

  return refreshPromise;
}

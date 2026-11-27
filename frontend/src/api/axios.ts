import axios from 'axios';
import type { AuthResponse } from './types';

declare module 'axios' {
  interface AxiosRequestConfig {
    _retry?: boolean;
  }
}

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
});

const refreshApi = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
});

const authEndpoints = new Set([
  '/auth/login',
  '/auth/register',
  '/auth/refresh',
  '/auth/logout',
]);

let accessToken: string | null = null;
let refreshPromise: Promise<AuthResponse> | null = null;

export function setAccessToken(token: string | null) {
  accessToken = token;
}

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

api.interceptors.request.use((config) => {
  if (accessToken) {
    config.headers.set('Authorization', `Bearer ${accessToken}`);
  } else {
    config.headers.delete('Authorization');
  }

  return config;
});

api.interceptors.response.use((response) => response,
  async (error: unknown) => {
    if (!axios.isAxiosError<unknown>(error)) {
      return Promise.reject(error);
    }

    const originalRequest = error.config;
    const requestPath = originalRequest?.url?.split('?')[0];

    if (
      error.response?.status !== 401 ||
      !originalRequest ||
      originalRequest._retry ||
      (requestPath !== undefined && authEndpoints.has(requestPath))
    ) {
      return Promise.reject(error);
    }

    originalRequest._retry = true;

    try {
      await refreshSession();
    } catch (refreshError) {
      return Promise.reject(refreshError);
    }

    return api(originalRequest);
  },
);
import axios from 'axios';

import { getAccessToken } from './accessToken';
import { refreshSession } from './refresh';
import { notifySessionExpired } from './sessionEvents';

declare module 'axios' {
  interface AxiosRequestConfig {
    _retry?: boolean;
  }
}

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
});

const authEndpoints = new Set([
  '/auth/login',
  '/auth/register',
  '/auth/refresh',
  '/auth/logout',
]);

api.interceptors.request.use((config) => {
  const accessToken = getAccessToken();

  if (accessToken !== null) {
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
      if (
        axios.isAxiosError<unknown>(refreshError) &&
        refreshError.response?.status === 401
      ) {
        notifySessionExpired();
      }

      return Promise.reject(refreshError);
    }

    return api(originalRequest);
  },
);
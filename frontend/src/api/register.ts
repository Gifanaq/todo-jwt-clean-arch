import { api, setAccessToken } from './axios';

type RegisterResponse = {
    user_id: string;
    login: string;
    access_token: string;
    token_type: 'bearer';
}

export async function register(login: string, password: string) {
    const response = await api.post<RegisterResponse>('/auth/register', {
        login,
        password,
    });

    setAccessToken(response.data.access_token);
    return response.data;
}
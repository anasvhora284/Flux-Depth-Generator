import axios from 'axios';

export function resolveApiBaseUrl(): string {
    const raw = process.env.NEXT_PUBLIC_API_URL?.trim();
    if (!raw) return '/api/v1';
    const base = raw.replace(/\/$/, '');
    return base.endsWith('/api/v1') ? base : `${base}/api/v1`;
}

const api = axios.create({
    baseURL: resolveApiBaseUrl(),
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default api;

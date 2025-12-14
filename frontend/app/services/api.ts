import axios from "axios";

const API_URL = "http://localhost:5000";

const api = axios.create({
    baseURL: API_URL, timeout: 100000 // timeout em ms
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("token");
        if (token) {
            config.headers["Authorization"] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        const rejection = (error instanceof Error) ? error : new Error(error.message || 'Erro de requisição desconhecido');
        return Promise.reject(rejection);
    }
);

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            const currentPath = window.location.pathname;
            if (!currentPath.startsWith('/login')) {
                const returnTo = encodeURIComponent(currentPath);
                window.location.href = `/login?returnTo=${returnTo}`;
            }
        }
        const rejection = (error instanceof Error) ? error : new Error(error.message || 'Erro de resposta desconhecido');
        return Promise.reject(rejection);
    }
);

export default api;

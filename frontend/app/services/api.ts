import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || '__API_URL_PLACEHOLDER__';

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
    (error) => Promise.reject(error)
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
        return Promise.reject(error);
    }
);

export default api;

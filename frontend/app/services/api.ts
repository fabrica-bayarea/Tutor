import axios from "axios";

const API_URL = "http://localhost:5000";

const api = axios.create({
    baseURL: API_URL,
    timeout: 100000,
    withCredentials: true, 
});

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
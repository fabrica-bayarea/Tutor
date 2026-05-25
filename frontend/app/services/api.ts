import axios from "axios";
import { toastEmitter } from "./toastEmitter";
import { loadingEmitter } from "./loadingEmitter";

const API_URL = process.env.NEXT_PUBLIC_API_URL_RUNTIME;

const api = axios.create({
    baseURL: API_URL,
    timeout: 100000,
    withCredentials: true,
});

const PUBLIC_PATHS = ['/login', '/alterar-senha', '/token-validate', '/esqueci-senha'];

// Códigos tratados localmente pelos formulários — não emitir toast global
const LOCAL_ERROR_CODES = new Set([400, 409, 410, 422]);

api.interceptors.request.use((config) => {
    loadingEmitter.show();
    return config;
});

api.interceptors.response.use(
    (response) => {
        loadingEmitter.hide();
        return response;
    },
    (error) => {
        loadingEmitter.hide();
        const status: number = error.response?.status ?? 0;
        const currentPath = window.location.pathname;
        const isPublic = PUBLIC_PATHS.some(p => currentPath.startsWith(p));

        if (status === 401) {
            if (!isPublic) {
                const returnTo = encodeURIComponent(currentPath);
                window.location.href = `/login?returnTo=${returnTo}`;
            }
        } else if (!LOCAL_ERROR_CODES.has(status) && status > 0) {
            if (status === 403) {
                toastEmitter.emit('Sem permissão para realizar esta ação.', 'error');
            } else if (status === 404) {
                toastEmitter.emit('Recurso não encontrado.', 'error');
            } else if (status >= 500) {
                toastEmitter.emit('Erro interno do servidor. Tente novamente.', 'error');
            }
        }

        return Promise.reject(error);
    }
);

export default api;

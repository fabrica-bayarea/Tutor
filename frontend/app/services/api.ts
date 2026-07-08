import axios from "axios";
import { toastEmitter } from "./toastEmitter";
import { loadingEmitter } from "./loadingEmitter";

// Flags opt-in para uma requisição específica controlar os efeitos globais do
// interceptor, sem alterar o comportamento padrão das demais chamadas:
// - skipGlobalErrorToast: o próprio chamador já exibe a mensagem (formulários);
// - skipGlobalLoading: evita o overlay global em chamadas frequentes (polling).
declare module "axios" {
    // Repete o type parameter genérico da interface original do axios; sem isto o
    // declaration merging falha (TS2428: type parameters devem ser idênticos).
    export interface AxiosRequestConfig<D = any> {
        skipGlobalErrorToast?: boolean;
        skipGlobalLoading?: boolean;
    }
}

const API_URL = process.env.NEXT_PUBLIC_API_URL_RUNTIME;

const api = axios.create({
    baseURL: API_URL,
    timeout: 100000,
    withCredentials: true,
});

const PUBLIC_PATHS = ['/login', '/alterar-senha', '/token-validate', '/esqueci-senha'];

// basePath do Next.js — deve corresponder ao next.config.ts
const BASE_PATH = '/tutor';

// Códigos tratados localmente pelos formulários — não emitir toast global
const LOCAL_ERROR_CODES = new Set([400, 409, 410, 422]);

api.interceptors.request.use((config) => {
    if (!config.skipGlobalLoading) loadingEmitter.show();
    return config;
});

api.interceptors.response.use(
    (response) => {
        if (!response.config.skipGlobalLoading) loadingEmitter.hide();
        return response;
    },
    (error) => {
        if (!error.config?.skipGlobalLoading) loadingEmitter.hide();
        const status: number = error.response?.status ?? 0;
        const skipGlobalToast = error.config?.skipGlobalErrorToast === true;
        const currentPath = window.location.pathname;
        const isPublic = PUBLIC_PATHS.some(p => currentPath.startsWith(`${BASE_PATH}${p}`));

        if (status === 401) {
            if (!isPublic) {
                const returnTo = encodeURIComponent(currentPath);
                window.location.href = `${BASE_PATH}/login?returnTo=${returnTo}`;
            }
        } else if (!skipGlobalToast && !LOCAL_ERROR_CODES.has(status) && status > 0) {
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

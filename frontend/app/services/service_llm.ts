import api from "./api";
import { InterfaceLLM, PullProgress } from "../types";

const llm_url = "/llm";

/**
 * Lista todos os modelos de IA cadastrados.
 *
 * Retorna uma lista (vazia se não houver modelos ou em caso de falha). Erros
 * graves (5xx) ainda disparam o toast global do interceptor.
 */
export async function listarModelos(): Promise<InterfaceLLM[]> {
    try {
        const response = await api.get(llm_url);
        return response.data?.modelos ?? [];
    } catch (error: any) {
        if (error?.response?.status === 404) return [];
        console.error("Erro ao listar modelos de IA:", error);
        return [];
    }
}

export type AdicionarModeloResultado =
    | { ok: true; modelo: InterfaceLLM }
    | { ok: false; status: number; message: string };

/**
 * Cadastra um novo modelo e dispara o download (pull) no Ollama.
 *
 * O backend valida a existência do modelo no Ollama antes de confirmar: responde
 * 404 se ele não existir, 409 se já houver um com o mesmo nome e 503 se o Ollama
 * estiver fora. As mensagens são exibidas dentro do modal — por isso a chamada
 * usa `skipGlobalErrorToast` para não duplicar com o toast genérico do
 * interceptor.
 */
export async function adicionarModelo(nome: string): Promise<AdicionarModeloResultado> {
    try {
        const response = await api.post(
            llm_url,
            { nome },
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true,
                skipGlobalErrorToast: true,
            }
        );
        return { ok: true, modelo: response.data };
    } catch (error: any) {
        const status = error?.response?.status ?? 0;
        const message =
            error?.response?.data?.error ??
            error?.response?.data?.Error ??
            "Não foi possível adicionar o modelo. Tente novamente.";
        return { ok: false, status, message };
    }
}

export type AtivarModeloResultado =
    | { ok: true; modelo: InterfaceLLM }
    | { ok: false; status: number; message: string };

/**
 * Ativa um modelo, desativando todos os demais (apenas um ativo por vez).
 *
 * O resultado é tratado pela página (toast de sucesso/erro), então a chamada
 * suprime o toast global do interceptor.
 */
export async function ativarModelo(id: string): Promise<AtivarModeloResultado> {
    try {
        const response = await api.post(`${llm_url}/activate/${id}`, null, {
            withCredentials: true,
            skipGlobalErrorToast: true,
        });
        return { ok: true, modelo: response.data };
    } catch (error: any) {
        const status = error?.response?.status ?? 0;
        const message =
            error?.response?.data?.error ??
            "Não foi possível ativar o modelo. Tente novamente.";
        return { ok: false, status, message };
    }
}

/**
 * Consulta o progresso do download de um modelo (rota de polling).
 *
 * Aceita um `AbortSignal` para que o hook de polling cancele a requisição em voo
 * quando o componente desmonta. Em qualquer falha (cancelamento, 404 ou rede)
 * retorna `null` e deixa o chamador decidir o que fazer; nunca emite toast
 * global (o polling não deve poluir a tela a cada falha transitória).
 */
export async function obterStatusPull(
    id: string,
    signal?: AbortSignal
): Promise<PullProgress | null> {
    try {
        const response = await api.get(`${llm_url}/pull-status/${id}`, {
            signal,
            skipGlobalErrorToast: true,
            skipGlobalLoading: true,
        });
        return response.data;
    } catch {
        return null;
    }
}

import api from "./api";
import { InterfaceTurma } from "../types";

const turmas_url = "turmas";

export async function obterTurma(turma_id: string) {
    try {
        const response: { data: InterfaceTurma } = await api.get(`/${turmas_url}/turma/${turma_id}`);
        return response.data;
    } catch (error) {
        console.error("Erro ao buscar a turma:", error);
        throw error;
    }
}

export type ListarTurmasParams = {
    search?: string;
    semestre?: string;
    turno?: string;
    status?: string;
    page?: number;
    limit?: number;
};

export type ListarTurmasResultado = {
    turmas: InterfaceTurma[];
    pagination: { page: number; pages: number; total: number };
};

export async function listarTurmas(
    params: ListarTurmasParams = {}
): Promise<ListarTurmasResultado> {
    try {
        const response = await api.get(`${turmas_url}/admin/turma`, { params });
        const turmas: InterfaceTurma[] =
            response.data?.Turmas ?? response.data?.turmas ?? [];
        const pagination = response.data?.pagination ?? {
            page: 1,
            pages: 1,
            total: turmas.length,
        };
        return { turmas, pagination };
    } catch (error: any) {
        if (error?.response?.status === 404) {
            return { turmas: [], pagination: { page: 1, pages: 1, total: 0 } };
        }
        console.error("Erro ao listar turmas:", error);
        return { turmas: [], pagination: { page: 1, pages: 1, total: 0 } };
    }
}

export type CriarTurmaResultado =
    | { ok: true; turma: InterfaceTurma }
    | { ok: false; status: number; message: string };

export async function criarTurma(
    codigo: string,
    semestre: string,
    turno: string
): Promise<CriarTurmaResultado> {
    try {
        const response = await api.post(
            `${turmas_url}/admin/turma`,
            { codigo, semestre, turno },
            { headers: { "Content-Type": "application/json" }, withCredentials: true }
        );
        return { ok: true, turma: response.data };
    } catch (error: any) {
        const status = error?.response?.status ?? 0;
        const message =
            error?.response?.data?.Error ??
            error?.response?.data?.error ??
            "Erro ao criar a turma.";
        return { ok: false, status, message };
    }
}

export type AtualizarTurmaResultado =
    | { ok: true; turma: InterfaceTurma }
    | { ok: false; status: number; message: string };

export async function atualizarTurma(
    id: string,
    codigo: string,
    semestre: string,
    turno: string,
    status: string = "ATIVO"
): Promise<AtualizarTurmaResultado> {
    try {
        const response = await api.put(
            `${turmas_url}/admin/turma/${id}`,
            { codigo, semestre, turno, status },
            { headers: { "Content-Type": "application/json" }, withCredentials: true }
        );
        return { ok: true, turma: response.data };
    } catch (error: any) {
        const httpStatus = error?.response?.status ?? 0;
        const message =
            error?.response?.data?.Error ??
            error?.response?.data?.error ??
            "Erro ao atualizar a turma.";
        return { ok: false, status: httpStatus, message };
    }
}

export async function desativarTurma(
    id: string
): Promise<{ ok: boolean; status?: number; message?: string }> {
    try {
        await api.delete(`${turmas_url}/admin/turma/${id}`, { withCredentials: true });
        return { ok: true };
    } catch (error: any) {
        const status = error?.response?.status ?? 0;
        const message =
            error?.response?.data?.error ?? "Erro ao desativar a turma.";
        return { ok: false, status, message };
    }
}

export async function reativarTurma(
    id: string,
    codigo: string,
    semestre: string,
    turno: string
): Promise<{ ok: boolean; message?: string }> {
    const resultado = await atualizarTurma(id, codigo, semestre, turno, "ATIVO");
    if (resultado.ok) return { ok: true };
    return { ok: false, message: resultado.message };
}

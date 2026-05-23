import api from "./api";
import { InterfaceMateria } from "../types";

const materias_url = "materias";

export async function obterMateria(materia_id: string) {
    try {
        const response: { data: InterfaceMateria } = await api.get(`/${materias_url}/materia/${materia_id}`);
        return response.data;
    } catch (error) {
        console.error("Erro ao buscar a matéria:", error);
        throw error;
    }
}

export async function listarMaterias(): Promise<InterfaceMateria[]> {
    try {
        const response = await api.get(`admin/materia`);
        return response.data?.Materias ?? [];
    } catch (error: any) {
        if (error?.response?.status === 404) return [];
        console.error("Erro ao listar matérias:", error);
        return [];
    }
}

export type CriarMateriaResultado =
    | { ok: true; materia: InterfaceMateria }
    | { ok: false; status: number; message: string };

export async function criarMateria(
    codigo: string,
    nome: string
): Promise<CriarMateriaResultado> {
    try {
        const response = await api.post(
            `admin/materia`,
            { codigo, nome },
            { headers: { "Content-Type": "application/json" }, withCredentials: true }
        );
        return { ok: true, materia: response.data };
    } catch (error: any) {
        const status = error?.response?.status ?? 0;
        const message =
            error?.response?.data?.Error ??
            error?.response?.data?.error ??
            "Erro ao criar a matéria.";
        return { ok: false, status, message };
    }
}

export type AtualizarMateriaResultado =
    | { ok: true; materia: InterfaceMateria }
    | { ok: false; status: number; message: string };

export async function atualizarMateria(
    id: string,
    codigo: string,
    nome: string,
    status: string = "ATIVO"
): Promise<AtualizarMateriaResultado> {
    try {
        const response = await api.put(
            `admin/materia/${id}`,
            { codigo, nome, status },
            { headers: { "Content-Type": "application/json" }, withCredentials: true }
        );
        return { ok: true, materia: response.data };
    } catch (error: any) {
        const status = error?.response?.status ?? 0;
        const message =
            error?.response?.data?.Error ??
            error?.response?.data?.error ??
            "Erro ao atualizar a matéria.";
        return { ok: false, status, message };
    }
}

export async function desativarMateria(
    id: string
): Promise<{ ok: boolean; status?: number; message?: string }> {
    try {
        await api.delete(`admin/materia/${id}`, { withCredentials: true });
        return { ok: true };
    } catch (error: any) {
        const status = error?.response?.status ?? 0;
        const message =
            error?.response?.data?.error ?? "Erro ao desativar a matéria.";
        return { ok: false, status, message };
    }
}

export async function reativarMateria(
    id: string,
    codigo: string,
    nome: string
): Promise<{ ok: boolean; message?: string }> {
    const resultado = await atualizarMateria(id, codigo, nome, "ATIVO");
    if (resultado.ok) return { ok: true };
    return { ok: false, message: resultado.message };
}

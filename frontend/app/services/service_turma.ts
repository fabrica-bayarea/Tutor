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

export async function listarTurmas(): Promise<InterfaceTurma[]> {
    try {
        const response = await api.get(`${turmas_url}/admin/turma`);
        return response.data?.turmas ?? response.data?.Turmas ?? [];
    } catch (error: any) {
        if (error?.response?.status === 404) return [];
        console.error("Erro ao listar turmas:", error);
        return [];
    }
}

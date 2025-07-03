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

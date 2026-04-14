import api from "./api";
import { InterfaceMateria, InterfaceTurma } from "../types";

const url = "data";

export async function buscar_materias_usuario(user_id: string){
    try {
        const response: { data: InterfaceMateria[] } = await api.get(`/${url}/materia/${user_id}`);
        return response.data;
    } catch (error) {
        console.error("Erro ao buscar as matérias:", error);
        throw error;
    }
}

export async function buscar_turmas_usuario(user_id: string){
    try {
        const response: { data: InterfaceTurma[] } = await api.get(`/${url}/turma/${user_id}`);
        return response.data;
    } catch (error) {
        console.error("Erro ao buscar as turmas:", error);
        throw error;
    }
}

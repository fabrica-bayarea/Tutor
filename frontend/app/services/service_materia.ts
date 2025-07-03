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

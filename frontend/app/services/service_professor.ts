import api from "./api";
import { InterfaceProfessor } from "../types";

const professores_url = "professores";

export async function loginProfessor(matricula: string, senha: string){
    try {
        const response: { data: { token: string, professor: InterfaceProfessor }} = await api.post(`${professores_url}/login`, { matricula, senha });

        const token = response.data.token;
        localStorage.setItem("token", token);
        
        const professor = response.data.professor;
        localStorage.setItem("professor", JSON.stringify(professor));
        
        return professor;
    } catch (error) {
        console.error("Erro ao autenticar o professor:", error);
        throw error;
    }
}

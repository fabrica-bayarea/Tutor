import api from "./api";
import { InterfaceProfessor } from "../types";

interface InterfaceLoginResponse {
    token: string;
    professor: InterfaceProfessor;
}

const professores_url = "professores";

export async function loginProfessor(matricula: string, senha: string){
    try {
        const response: InterfaceLoginResponse = await api.post(`${professores_url}/login`, { matricula, senha });

        const token = response.token;
        localStorage.setItem("token", token);
        
        const professor = response.professor;
        return professor;
    } catch (error) {
        console.error("Erro ao autenticar o professor:", error);
        throw error;
    }
}

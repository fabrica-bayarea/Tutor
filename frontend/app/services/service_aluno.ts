import api from "./api";
import { InterfaceAluno } from "../types";

interface InterfaceLoginResponse {
    token: string;
    aluno: InterfaceAluno;
}

const alunos_url = "alunos";

export async function loginAluno(matricula_aluno: string, senha: string){
    try {
        const response: InterfaceLoginResponse = await api.post(`${alunos_url}/login`, { matricula_aluno, senha });

        const token = response.token;
        localStorage.setItem("token", token);
        
        const aluno = response.aluno;
        return aluno;
    } catch (error) {
        console.error("Erro ao autenticar o aluno:", error);
        throw error;
    }
}

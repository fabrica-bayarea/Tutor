import api from "./api";
import { InterfaceAluno } from "../types";

const alunos_url = "alunos";

export async function loginAluno(matricula: string, senha: string){
    try {
        const response: { data: { token: string, aluno: InterfaceAluno }} = await api.post(`${alunos_url}/login`, { matricula, senha });

        const token = response.data.token;
        localStorage.setItem("token", token);
        
        const aluno = response.data.aluno;
        localStorage.setItem("aluno", JSON.stringify(aluno));
        
        return aluno;
    } catch (error) {
        console.error("Erro ao autenticar o aluno:", error);
        throw error;
    }
}

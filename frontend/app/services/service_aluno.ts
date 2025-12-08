import api from "./api";
import { InterfaceAluno } from "../types";

const alunos_url = "usuario";

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

export async function criarAluno(matricula: string, nome: string, email: string, senha:string){
    try {
        const response: {data: {aluno: InterfaceAluno}} = await api.post(`${alunos_url}/criar`, { matricula, nome, email, senha });

        const aluno = response.data.aluno;
        localStorage.setItem("aluno", JSON.stringify(aluno));
        
        return aluno;
    } catch (error) {
        console.error("Erro ao autenticar o usuario:", error);
        throw error;
    }
}

export async function loginAlunoGoogle(googleToken: string) {
    try {
        const response = await fetch("http://seu-backend.com/aluno/google-login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ token: googleToken }),
        });

        if (!response.ok) return null;

        return await response.json();

    } catch (error) {
        console.error("Erro login Google:", error);
        return null;
    }
}

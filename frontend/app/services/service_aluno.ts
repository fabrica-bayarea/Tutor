import api from "./api";
import { InterfaceAluno, GooglePayload } from "../types";
import * as jwt_decode from 'jwt-decode';


const alunos_url = "usuario";

export async function loginAluno(matricula: string, senha: string): Promise<InterfaceAluno | null> {
    try {
        const response: { data: { token: string; aluno: InterfaceAluno } } = await api.post(
            `${alunos_url}/login`,
            { matricula, senha }
        );

        const token = response.data.token;
        localStorage.setItem("token", token);

        const aluno = response.data.aluno;
        localStorage.setItem("aluno", JSON.stringify(aluno));

        return aluno;
    } catch (error) {
        console.error("Erro ao autenticar o aluno:", error);
        return null;
    }
}

export async function criarAluno(matricula: string, nome: string, email: string, senha: string): Promise<InterfaceAluno | null> {
    try {
        const response: { data: { aluno: InterfaceAluno; token: string } } = await api.post(
            `${alunos_url}/criar`,
            { matricula, nome, email, senha }
        );

        const token = response.data.token;
        localStorage.setItem("token", token);

        const aluno = response.data.aluno;
        localStorage.setItem("aluno", JSON.stringify(aluno));

        return aluno;
    } catch (error) {
        console.error("Erro ao criar o aluno:", error);
        return null;
    }
}

export async function loginAlunoGoogle(googleToken: string): Promise<InterfaceAluno | null> {
    try {
        const response = await api.post(`${alunos_url}/login/google`, { token: googleToken });
        const aluno = response.data.aluno;
        const token = response.data.token;

        localStorage.setItem("token", token);
        localStorage.setItem("aluno", JSON.stringify(aluno));

        return aluno;
    } catch (error) {
        console.error("Erro login Google:", error);
        return null;
    }
}


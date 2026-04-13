import api from "./api";
import { InterfaceUsuario } from "../types";

const alunos_url = "usuario";

export async function criarAluno(matricula: string, nome: string, email: string, senha: string): Promise<InterfaceUsuario | null> {
  try {
        const response = await api.post(
        `${alunos_url}/criar`,
        { matricula, nome, email, senha },
        {
            headers: { 'Content-Type': 'application/json' },
            withCredentials: true,
        }
        );

        const aluno = response.data;

        localStorage.setItem("aluno", JSON.stringify(aluno));

        return aluno;
    } catch (error) {
        console.error("Erro ao criar o aluno:", error);
        return null;
    }
}

export async function loginAluno(matricula: string, senha: string): Promise<InterfaceUsuario | null> {
    try {
        const response = await api.post(
            `${alunos_url}/login`,
            { matricula, senha },
        );

        const aluno = response.data.aluno;

        return aluno;
    } catch (error) {
        console.error("Erro ao autenticar o aluno:", error);
        return null;
    }
}

export async function loginAlunoGoogle(googleToken: string): Promise<InterfaceUsuario | null> {
    try {
        const response = await api.post(
            `${alunos_url}/login/google`,
            { token: googleToken },
        );

        const aluno = response.data.aluno;

        return aluno;
    } catch (error) {
        console.error("Erro login Google:", error);
        return null;
    }
}

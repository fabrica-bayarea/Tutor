import axios from "axios";
import api from "./api";
import { InterfaceUsuario } from "../types";

const alunos_url = "alunos";

export type LoginErrorCode = "invalid_credentials" | "deactivated" | "unknown";

export type LoginResult =
    | { ok: true; aluno: InterfaceUsuario }
    | { ok: false; error: LoginErrorCode };

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

function parseLoginError(error: unknown): LoginErrorCode {
    if (axios.isAxiosError(error) && error.response) {
        const data = error.response.data as { error?: string; code?: string } | undefined;
        const code = (data?.code ?? "").toLowerCase();
        const message = (data?.error ?? "").toLowerCase();

        if (code === "deactivated" || message.includes("desativ") || message.includes("inativ")) {
            return "deactivated";
        }
        if (error.response.status === 401) {
            return "invalid_credentials";
        }
    }
    return "unknown";
}

export async function loginAluno(matricula: string, senha: string): Promise<LoginResult> {
    try {
        const response = await api.post(
            `${alunos_url}/login`,
            { matricula, senha },
        );

        return { ok: true, aluno: response.data.aluno };
    } catch (error) {
        console.error("Erro ao autenticar o aluno:", error);
        return { ok: false, error: parseLoginError(error) };
    }
}

export async function loginAlunoGoogle(googleToken: string): Promise<LoginResult> {
    try {
        const response = await api.post(
            `${alunos_url}/login/google`,
            { token: googleToken },
        );

        return { ok: true, aluno: response.data.aluno };
    } catch (error) {
        console.error("Erro login Google:", error);
        return { ok: false, error: parseLoginError(error) };
    }
}

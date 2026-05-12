import api from "./api";
import { Role } from "@/utils/roles";
import { InterfaceUsuario } from "../types";

const alunos_url = "alunos";

export type AlunoBackend = InterfaceUsuario & { status?: string };

export async function listarAlunos(): Promise<AlunoBackend[]> {
    try {
        const response = await api.get(`admin/usuarios/all`);
        const usuarios: AlunoBackend[] = response.data?.usuarios ?? [];
        return usuarios.filter((u) => u.role === Role.ALUNO);
    } catch (error) {
        console.error("Erro ao listar alunos:", error);
        return [];
    }
}

export type CriarAlunoResultado =
    | { ok: true; aluno: InterfaceUsuario }
    | { ok: false; status: number; message: string };

export async function criarAluno(
    matricula: string,
    nome: string,
    email: string,
    senha: string
): Promise<CriarAlunoResultado> {
    try {
        const response = await api.post(
            `admin/usuarios/criar`,
            { matricula, nome, email, senha },
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true,
            }
        );
        return { ok: true, aluno: response.data };
    } catch (error: any) {
        const status = error?.response?.status ?? 0;
        const message =
            error?.response?.data?.error ?? "Erro ao criar o aluno.";
        return { ok: false, status, message };
    }
}

export type LoginErrorCode = "invalid_credentials" | "deactivated" | "unknown";

export type LoginResultado =
    | { ok: true; aluno: InterfaceUsuario }
    | { ok: false; error: LoginErrorCode };

export async function loginAluno(matricula: string, senha: string): Promise<LoginResultado> {
    try {
        const response = await api.post(
            `${alunos_url}/login`,
            { matricula, senha },
        );
        return { ok: true, aluno: response.data.aluno };
    } catch (error: any) {
        const status = error?.response?.status ?? 0;
        if (status === 401) return { ok: false, error: "invalid_credentials" };
        if (status === 403) return { ok: false, error: "deactivated" };
        console.error("Erro ao autenticar o aluno:", error);
        return { ok: false, error: "unknown" };
    }
}

export async function loginAlunoGoogle(googleToken: string): Promise<LoginResultado> {
    try {
        const response = await api.post(
            `${alunos_url}/login/google`,
            { token: googleToken },
        );
        return { ok: true, aluno: response.data.aluno };
    } catch (error: any) {
        const status = error?.response?.status ?? 0;
        if (status === 401) return { ok: false, error: "invalid_credentials" };
        if (status === 403) return { ok: false, error: "deactivated" };
        console.error("Erro login Google:", error);
        return { ok: false, error: "unknown" };
    }
}

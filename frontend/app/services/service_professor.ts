import api from "./api";
import { Role } from "@/utils/roles";
import { InterfaceUsuario } from "../types";

export type ProfessorBackend = InterfaceUsuario;

export async function listarProfessores(): Promise<ProfessorBackend[]> {
    try {
        const response = await api.get(`alunos/professors`);
        return response.data?.Professores ?? [];
    } catch (error: any) {
        if (error?.response?.status === 404) return [];
        console.error("Erro ao listar professores:", error);
        return [];
    }
}

export type CriarProfessorResultado =
    | { ok: true; professor: InterfaceUsuario }
    | { ok: false; status: number; message: string };

export async function criarProfessor(
    matricula: string,
    nome: string,
    email: string
): Promise<CriarProfessorResultado> {
    let criado: InterfaceUsuario;
    try {
        const response = await api.post(
            `admin/usuarios/criar`,
            { matricula, nome, email },
            { headers: { "Content-Type": "application/json" }, withCredentials: true }
        );
        criado = response.data;
    } catch (error: any) {
        const status = error?.response?.status ?? 0;
        const message = error?.response?.data?.error ?? "Erro ao criar o professor.";
        return { ok: false, status, message };
    }

    try {
        const response = await api.put(
            `admin/usuarios/${criado.id}`,
            { matricula, nome, email, role: Role.PROFESSOR, status: "ATIVO" },
            { headers: { "Content-Type": "application/json" }, withCredentials: true }
        );
        return { ok: true, professor: response.data };
    } catch (error: any) {
        const status = error?.response?.status ?? 0;
        const message =
            error?.response?.data?.error ??
            "Usuário criado, mas não foi possível defini-lo como professor.";
        return { ok: false, status, message };
    }
}

export type AtualizarProfessorResultado =
    | { ok: true; professor: InterfaceUsuario }
    | { ok: false; status: number; message: string };

export async function atualizarProfessor(
    id: string,
    matricula: string,
    nome: string,
    email: string,
    status: string = "ATIVO"
): Promise<AtualizarProfessorResultado> {
    try {
        const response = await api.put(
            `admin/usuarios/${id}`,
            { matricula, nome, email, role: Role.PROFESSOR, status },
            { headers: { "Content-Type": "application/json" }, withCredentials: true }
        );
        return { ok: true, professor: response.data };
    } catch (error: any) {
        const httpStatus = error?.response?.status ?? 0;
        const message =
            error?.response?.data?.error ?? "Erro ao atualizar o professor.";
        return { ok: false, status: httpStatus, message };
    }
}

export async function desativarProfessor(
    id: string
): Promise<{ ok: boolean; message?: string }> {
    try {
        await api.delete(`admin/usuarios/delete/${id}`, { withCredentials: true });
        return { ok: true };
    } catch (error: any) {
        const message =
            error?.response?.data?.error ?? "Erro ao desativar o professor.";
        return { ok: false, message };
    }
}

export async function reativarProfessor(
    id: string
): Promise<{ ok: boolean; message?: string }> {
    try {
        await api.patch(
            `admin/usuarios/${id}/reativar`,
            { status: "ATIVO" },
            { headers: { "Content-Type": "application/json" }, withCredentials: true }
        );
        return { ok: true };
    } catch (error: any) {
        const message =
            error?.response?.data?.error ?? "Erro ao reativar o professor.";
        return { ok: false, message };
    }
}

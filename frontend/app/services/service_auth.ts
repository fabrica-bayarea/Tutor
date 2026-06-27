import api from "@/app/services/api";
import { RoleType } from "@/utils/roles";

export interface Usuario {
    id: string;
    nome: string;
    email: string;
    role: RoleType;
}

export interface DadosTokenValido {
    nome: string;
    email: string;
}

export type ValidarTokenResultado =
    | { ok: true; dados: DadosTokenValido }
    | { ok: false; status: number; message: string };

export type CriarSenhaResultado =
    | { ok: true; usuario: Usuario }
    | { ok: false; status: number; message: string };
    
export async function solicitarRecuperacaoSenha(email: string): Promise<{ ok: boolean }> {
    try {
        await api.post("/auth/forgot-password", { email }, {
            headers: { "Content-Type": "application/json" },
        });
        return { ok: true };
    } catch {
        return { ok: true }; // always ok — security: don't reveal if email exists
    }
}

export async function getCurrentUser(): Promise<Usuario | null> {
    try {
        const response = await api.get("/alunos/me", {withCredentials: true});
        return response.data;
    } catch {
        return null;
    }
}

export async function logout(): Promise<void> {
    try {
        await api.post("/alunos/encerrar-sessao", {}, { withCredentials: true });
    } catch (error) {
        console.error("Erro ao fazer logout:", error);
    }
}

/**
 * Renova a sessão por atividade (sliding expiration). Usado pelo chat a cada
 * envio de mensagem — como o WebSocket não pode reescrever o cookie httponly,
 * esta chamada HTTP mantém a sessão viva enquanto o aluno conversa.
 *
 * Usa fetch direto (sem o interceptor/spinner global do axios) e é best-effort:
 * a expiração efetiva é tratada pelo socket ("sessao_expirada") e pelo 401 das
 * demais chamadas.
 */
export async function touchSessao(): Promise<void> {
    const baseUrl = process.env.NEXT_PUBLIC_API_URL_RUNTIME ?? "";
    try {
        await fetch(`${baseUrl}/alunos/sessao/touch`, {
            method: "POST",
            credentials: "include",
        });
    } catch {
        // silencioso — renovação é best-effort
    }
}

export async function validarToken(token: string): Promise<ValidarTokenResultado> {
    try {
        const response = await api.get(`/auth/invite/validate/${encodeURIComponent(token)}`);
        return { ok: true, dados: response.data };
    } catch (error: any) {
        const status = error?.response?.status ?? 0;
        const message =
            error?.response?.data?.error ??
            "Este link já foi utilizado ou é inválido.";
        return { ok: false, status, message };
    }
}

export async function criarSenha(
    token: string,
    senha: string,
    confirmacao: string
): Promise<CriarSenhaResultado> {
    try {
        const response = await api.post(
            "/auth/invite/set-password",
            { token, senha, confirmacao },
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true,
            }
        );
        return { ok: true, usuario: response.data?.usuario };
    } catch (error: any) {
        const status = error?.response?.status ?? 0;
        const message =
            error?.response?.data?.error ?? "Erro ao criar a senha.";
        return { ok: false, status, message };
    }
}
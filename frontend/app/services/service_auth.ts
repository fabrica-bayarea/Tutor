import api from "@/app/services/api";

export interface Usuario {
    id: string;
    nome: string;
    email: string;
    role: '1' | '2' | '3';
}

export interface DadosTokenValido {
    nome: string;
    email: string;
}

export type ValidarTokenResultado =
    | { ok: true; dados: DadosTokenValido }
    | { ok: false; status: number; message: string };

export type CriarSenhaResultado =
    | { ok: true }
    | { ok: false; status: number; message: string };
    
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
    senha: string
): Promise<CriarSenhaResultado> {
    try {
        await api.post(
            "/auth/invite/set-password",
            { token, senha },
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true,
            }
        );
        return { ok: true };
    } catch (error: any) {
        const status = error?.response?.status ?? 0;
        const message =
            error?.response?.data?.error ?? "Erro ao criar a senha.";
        return { ok: false, status, message };
    }
}
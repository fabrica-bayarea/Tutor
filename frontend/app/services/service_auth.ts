import api from "@/app/services/api";

export interface Usuario {
    id: string;
    nome: string;
    email: string;
    role: '1' | '2' | '3';
}

export async function getCurrentUser(): Promise<Usuario | null> {
    try {
        const response = await api.get("/usuarios/me");
        return response.data;
    } catch {
        return null;
    }
}

export async function logout(): Promise<void> {
    try {
        await api.post("/usuarios/logout");
    } catch (error) {
        console.error("Erro ao fazer logout:", error);
    }
}

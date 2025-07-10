import { jwtDecode } from 'jwt-decode';

export interface TokenPayload {
    user_id: string;
    role: 'aluno' | 'professor';
    exp: number;
}

export function getToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('token');
}

export function getDecodedToken(): TokenPayload | null {
    const token = getToken();
    if (!token) return null;

    try {
        return jwtDecode<TokenPayload>(token);
    } catch (error) {
        console.error('Erro ao decodificar token:', error);
        return null;
    }
}

export function isAuthenticated(): boolean {
    const token = getDecodedToken();
    if (!token) return false;

    // Verifica se o token expirou
    return token.exp * 1000 > Date.now();
}

export function getUserRole(): 'aluno' | 'professor' | null {
    const token = getDecodedToken();
    return token?.role || null;
}

export function isStudent(): boolean {
    return getUserRole() === 'aluno';
}

export function isProfessor(): boolean {
    return getUserRole() === 'professor';
}

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { Role, homeForRole } from '@/utils/roles'

function getRoleFromToken(token: string): string | null {
    try {
        const payload = token.split('.')[1];
        const decoded = JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')));
        return decoded.role ? String(decoded.role) : null;
    } catch {
        return null;
    }
}

const PUBLIC_ROUTES = ['/login', '/alunos/login/google', '/alterar-senha', '/token-validate', '/esqueci-senha'];

/**
 * Helper para criar redirect respeitando o basePath.
 * Usa request.nextUrl.clone() para que o basePath seja preservado.
 */
function redirectTo(path: string, request: NextRequest, params?: Record<string, string>) {
    const url = request.nextUrl.clone();
    url.pathname = path;
    url.search = '';
    if (params) {
        for (const [key, value] of Object.entries(params)) {
            url.searchParams.set(key, value);
        }
    }
    return NextResponse.redirect(url);
}

export function middleware(request: NextRequest) {
    const token = request.cookies.get("token")?.value;
    const { pathname } = request.nextUrl;

    if (pathname === '/') {
        if (token) {
            const role = getRoleFromToken(token);
            return redirectTo(homeForRole(role), request);
        }
        return redirectTo("/login", request);
    }

    const isPublicRoute = PUBLIC_ROUTES.some(r => pathname.startsWith(r));

    if (isPublicRoute) {
        if (token) {
            const role = getRoleFromToken(token);
            return redirectTo(homeForRole(role), request);
        }
        return NextResponse.next();
    }

    if (!token) {
        return redirectTo("/login", request, { returnTo: pathname });
    }

    const role = getRoleFromToken(token);

    if (pathname.startsWith('/admin')     && role !== Role.ADMIN)     return redirectTo(homeForRole(role), request);
    if (pathname.startsWith('/professor') && role !== Role.PROFESSOR) return redirectTo(homeForRole(role), request);
    if (pathname.startsWith('/chat')      && role !== Role.ALUNO)     return redirectTo(homeForRole(role), request);

    return NextResponse.next();
}

export const config = {
    matcher: ["/((?!_next|favicon.ico|api).*)"],
};

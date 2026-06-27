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

export function middleware(request: NextRequest) {
    const token = request.cookies.get("token")?.value;
    const { pathname } = request.nextUrl;

    if (pathname === '/') {
        if (token) {
            const role = getRoleFromToken(token);
            return NextResponse.redirect(new URL(homeForRole(role), request.url));
        }
        return NextResponse.redirect(new URL("/login", request.url));
    }

    const isPublicRoute = PUBLIC_ROUTES.some(r => pathname.startsWith(r));

    if (isPublicRoute) {
        if (token) {
            const role = getRoleFromToken(token);
            return NextResponse.redirect(new URL(homeForRole(role), request.url));
        }
        return NextResponse.next();
    }

    if (!token) {
        const loginUrl = new URL("/login", request.url);
        loginUrl.searchParams.set("returnTo", pathname);
        return NextResponse.redirect(loginUrl);
    }

    const role = getRoleFromToken(token);

    if (pathname.startsWith('/admin')     && role !== Role.ADMIN)     return NextResponse.redirect(new URL(homeForRole(role), request.url));
    if (pathname.startsWith('/professor') && role !== Role.PROFESSOR) return NextResponse.redirect(new URL(homeForRole(role), request.url));
    if (pathname.startsWith('/chat')      && role !== Role.ALUNO)     return NextResponse.redirect(new URL(homeForRole(role), request.url));

    return NextResponse.next();
}

export const config = {
    matcher: ["/((?!_next|favicon.ico|api).*)"],
};

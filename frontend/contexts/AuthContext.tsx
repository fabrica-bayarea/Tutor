"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { Role } from "@/utils/roles";
import { getCurrentUser, logout as logoutService, Usuario } from "@/app/services/service_auth";

interface AuthContextType {
    user: Usuario | null;
    loading: boolean;
    isAuthenticated: boolean;
    isStudent: boolean;
    isProfessor: boolean;
    isAdmin: boolean;
    refreshUser: () => Promise<Usuario | null>;
    logout: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<Usuario | null>(null);
    const [loading, setLoading] = useState(true);

    async function loadUser(): Promise<Usuario | null> {
        setLoading(true);
        const data = await getCurrentUser();
        setUser(data);
        setLoading(false);
        return data;
    }

    useEffect(() => {
        loadUser();
    }, []);

    async function refreshUser(): Promise<Usuario | null> {
        return await loadUser();
    }

    async function logout() {
        await logoutService();
        setUser(null);
    }

    return (
        <AuthContext.Provider
            value={{
                user,
                loading,
                isAuthenticated: !!user,
                isStudent: user?.role === Role.ALUNO,
                isProfessor: user?.role === Role.PROFESSOR,
                isAdmin: user?.role === Role.ADMIN,
                refreshUser,
                logout
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

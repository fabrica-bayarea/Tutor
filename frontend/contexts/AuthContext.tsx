'use client';

import { createContext, useContext, useEffect, useState } from "react";
import { InterfaceUsuario } from "@/types";
import api from "@/app/services/api";

interface AuthContextType {
  aluno: InterfaceUsuario | null;
  setAluno: (aluno: InterfaceUsuario | null) => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [aluno, setAluno] = useState<InterfaceUsuario | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchUser() {
      try {
        const response = await api.get("/usuario/me", {
          withCredentials: true,
        });

        setAluno(response.data);
      } catch {
        setAluno(null);
      } finally {
        setLoading(false);
      }
    }

    fetchUser();
  }, []);

  return (
    <AuthContext.Provider value={{ aluno, setAluno, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth deve ser usado dentro do AuthProvider");
  return context;
};

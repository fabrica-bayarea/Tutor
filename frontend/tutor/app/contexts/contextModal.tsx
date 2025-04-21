"use client";

import React, { createContext, useState, ReactNode } from 'react';

interface MateriasDisponiveis {
  id: number;
  nome: string;
}
type arrayMaterias = MateriasDisponiveis[]
interface MateriasDisponiveisContext {
  itens: arrayMaterias;
}

interface ModalContextType {
  materias: arrayMaterias;
  menuEstaAberto: boolean;
  abrirMenu: () => void;
  fecharMenu: () => void;
  extracaoEstaAberto: boolean;
  abrirMenuExtracao: () => void;
  fecharMenuExtracao: () => void;
  materiaEstaAberto: boolean;
  abrirMenuMateria: () => void;
  fecharMenuMateria: () => void;
}

export const ModalContext = createContext<ModalContextType | undefined>(undefined);

interface ModalProviderProps {
  children: ReactNode;
}

export function ModalProvider({ children }: ModalProviderProps) {
  const [materias, setMaterias] = useState<arrayMaterias>([
    { id: 1, nome: 'Matéria A'},
    { id: 2, nome: 'Matéria B'},
  ]);

  const [menuEstaAberto, setmenuEstaAberto] = useState(false);
  const abrirMenu = () => {
    setmenuEstaAberto(true);
  };
  const fecharMenu = () => {
    setmenuEstaAberto(false);
  };

  const [extracaoEstaAberto, setextracaoEstaAberto] = useState(false);
  const abrirMenuExtracao = () => {
    setextracaoEstaAberto(true);
  };
  const fecharMenuExtracao = () => {
    setextracaoEstaAberto(false);
    setmenuEstaAberto(false)
  };

  const [materiaEstaAberto, setMateriaEstaAberto] = useState(false);
  const abrirMenuMateria = () => {
    setMateriaEstaAberto(true);
  };
  const fecharMenuMateria = () => {
    setMateriaEstaAberto(false);
    setmenuEstaAberto(false)
  };

  return (
    <ModalContext.Provider
      value={{
        materias,
        menuEstaAberto,
        abrirMenu,
        fecharMenu,
        extracaoEstaAberto,
        abrirMenuExtracao,
        fecharMenuExtracao,
        materiaEstaAberto,
        abrirMenuMateria,
        fecharMenuMateria
      }}
    >
      {children}
    </ModalContext.Provider>
  );
}

export default ModalProvider;
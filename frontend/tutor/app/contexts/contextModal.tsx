"use client";

import React, { createContext, useState, ReactNode } from 'react';

// Define a estrutura do contexto
interface ModalContextType {
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

// Cria o contexto com um valor padrão (pode ser null ou um objeto com valores iniciais)
export const ModalContext = createContext<ModalContextType | undefined>(undefined);

// Define as props do Provider
interface ModalProviderProps {
  children: ReactNode;
}

export function ModalProvider({ children }: ModalProviderProps) {
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
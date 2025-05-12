"use client"; // Este arquivo será executado no lado do cliente (Next.js)

import React, { createContext, useState, ReactNode } from 'react';


/**
 * Interface que representa uma matéria disponível.
 */
interface MateriasDisponiveis {
  id: number;
  nome: string;
}

// Tipo auxiliar para array de matérias
type arrayMaterias = MateriasDisponiveis[]

/**
 * Interface do contexto para consumo das matérias (não usado no provider principal).
 */
interface MateriasDisponiveisContext {
  itens: arrayMaterias;
}

/**
 * Interface que define o formato dos dados e funções disponíveis no contexto Modal.
 */
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

// Criação do contexto com o tipo definido
export const ModalContext = createContext<ModalContextType | undefined>(undefined);

/**
 * Props esperadas pelo ModalProvider (componente wrapper de contexto).
 */
interface ModalProviderProps {
  children: ReactNode;
}

/**
 * ModalProvider é responsável por gerenciar o estado global relacionado a:
 * - Exibição dos menus (perfil, extração, matéria)
 * - Lista de matérias disponíveis
 * Este provider disponibiliza esse estado via contexto para o app.
 */
export function ModalProvider({ children }: ModalProviderProps) {
  // Estado inicial com duas matérias fixas
  const [materias, setMaterias] = useState<arrayMaterias>([
    { id: 1, nome: 'Matéria A'},
    { id: 2, nome: 'Matéria B'},
  ]);

  // Controle do menu lateral (perfil)
  const [menuEstaAberto, setmenuEstaAberto] = useState(false);
  const abrirMenu = () => {
    setmenuEstaAberto(true);
  };
  const fecharMenu = () => {
    setmenuEstaAberto(false);
  };

  // Controle da janela de extração
  const [extracaoEstaAberto, setextracaoEstaAberto] = useState(false);
  const abrirMenuExtracao = () => {
    setextracaoEstaAberto(true);
  };
  const fecharMenuExtracao = () => {
    setextracaoEstaAberto(false);
    setmenuEstaAberto(false) // Fecha o menu junto
  };

  // Controle da lista de matérias
  const [materiaEstaAberto, setMateriaEstaAberto] = useState(false);
  const abrirMenuMateria = () => {
    setMateriaEstaAberto(true);
  };
  const fecharMenuMateria = () => {
    setMateriaEstaAberto(false);
    setmenuEstaAberto(false) // Fecha o menu junto
  };

  /**
   * Fornece o contexto para os componentes filhos com:
   * - Lista de matérias disponíveis
   * - Estados de visibilidade dos menus (perfil, extração, matéria)
   * - Métodos para abrir/fechar cada um desses menus
   * 
   * Isso permite que qualquer componente abaixo na árvore do React
   * possa acessar e manipular esses dados via useContext(ModalContext).
   */
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
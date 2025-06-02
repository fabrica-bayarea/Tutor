"use client";
import PaginaInicial from "./paginaInicial/paginaInicial";
import ExtratorWindow from "./professor/extratorMenu/ExtratorMenu";
import React from 'react';
import { Routes, Route, BrowserRouter } from 'react-router-dom';
import MainNavigator from "./components/mainNavigator"
import ModalProvider from "./contexts/contextModal";

// Página inicial da aplicação com contexto de modais aplicado
export default function Home() {
  return (
    <ModalProvider>
      <BrowserRouter>
          <MainNavigator />
          <div className="content">
            <Routes>
              <Route path="/" element={<PaginaInicial />} />
              <Route path="pagina inicial" element={<PaginaInicial />} />
              <Route path="pagina de extracao" element={<ExtratorWindow />} />
            </Routes>
          </div>
      </BrowserRouter>
    </ModalProvider>
  );
};
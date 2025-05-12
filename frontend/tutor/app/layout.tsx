// Importa o tipo Metadata usado para definir metadados da página
import type { Metadata } from "next";

// Importa estilos globais da aplicação
import "./globals.css";
import React from "react";

/**
 * Metadados básicos da aplicação definidos para o HTML <head>.
 * O Next.js usará esse objeto para gerar as tags correspondentes automaticamente.
 */
export const metadata: Metadata = {
  title: "Tutor",
};

/**
 * RootLayout define o layout base da aplicação Next.js.
 * Este componente é o contêiner principal que envolve todas as páginas.
 */
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-br"> {/* Define o idioma da página como português do Brasil */}
      <body>
        {children} {/* Renderiza o conteúdo da página */}
      </body>
    </html>
  );
}


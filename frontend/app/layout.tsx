import React from "react";
import type { Metadata } from "next";
import "./globals.css";
import { ModalProvider } from "../contexts/contextModal";
import { AuthProvider } from "../contexts/AuthContext";
import { DataProvider } from "../contexts/DataContext";

export const metadata: Metadata = {
    title: "Tutor",
};
export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="pt-br">
            <body>
                <AuthProvider>
                <DataProvider>
                <ModalProvider>
                    <main>{children}</main>
                </ModalProvider>
                </DataProvider>
                </AuthProvider>
            </body>
        </html>
    );
}

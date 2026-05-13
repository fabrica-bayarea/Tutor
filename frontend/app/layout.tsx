import React from "react";
import type { Metadata } from "next";
import "./globals.css";
import { ModalProvider } from "../contexts/contextModal";
import { AuthProvider } from "../contexts/AuthContext";
import { DataProvider } from "../contexts/DataContext";
import { LayoutProvider } from "@/contexts/LayoutContext";
import { ToastProvider } from "@/contexts/ToastContext";
import ToastContainer from "@/app/components/ToastContainer/ToastContainer";
import GlobalLoadingOverlay from "@/app/components/GlobalLoadingOverlay/GlobalLoadingOverlay";

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
                <ToastProvider>
                <LayoutProvider>
                <AuthProvider>
                <DataProvider>
                <ModalProvider>
                    <main>{children}</main>
                    <ToastContainer />
                    <GlobalLoadingOverlay />
                </ModalProvider>
                </DataProvider>
                </AuthProvider>
                </LayoutProvider>
                </ToastProvider>
            </body>
        </html>
    );
}

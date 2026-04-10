import React from "react";
import type { Metadata } from "next";
import "./globals.css";
import { ModalProvider } from "../contexts/contextModal";

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
                <ModalProvider>
                    <main>{children}</main>
                </ModalProvider>
            </body>
        </html>
    );
}

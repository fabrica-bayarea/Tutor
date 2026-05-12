"use client";

import React, { useEffect } from "react";
import { createPortal } from "react-dom";
import { X } from "lucide-react";
import styles from "./Modal.module.css";

type ModalProps = {
    open: boolean;
    onClose: () => void;
    title?: React.ReactNode;
    icon?: React.ReactNode;
    children: React.ReactNode;
    footer?: React.ReactNode;
    showCloseButton?: boolean;
    closeOnBackdrop?: boolean;
    closeOnEsc?: boolean;
    width?: string;
    accent?: boolean;
    className?: string;
};

export default function Modal({
    open,
    onClose,
    title,
    icon,
    children,
    footer,
    showCloseButton = false,
    closeOnBackdrop = true,
    closeOnEsc = true,
    width,
    accent = false,
    className,
}: ModalProps) {
    useEffect(() => {
        if (!open || !closeOnEsc) return;
        const handler = (e: KeyboardEvent) => {
            if (e.key === "Escape") onClose();
        };
        window.addEventListener("keydown", handler);
        return () => window.removeEventListener("keydown", handler);
    }, [open, closeOnEsc, onClose]);

    useEffect(() => {
        if (!open) return;
        const previous = document.body.style.overflow;
        document.body.style.overflow = "hidden";
        return () => {
            document.body.style.overflow = previous;
        };
    }, [open]);

    if (!open || typeof document === "undefined") return null;

    return createPortal(
        <div
            className={styles.backdrop}
            onClick={closeOnBackdrop ? onClose : undefined}
            role="dialog"
            aria-modal="true"
        >
            <div
                className={`${styles.panel} ${className ?? ""}`}
                style={width ? { maxWidth: width } : undefined}
                onClick={(e) => e.stopPropagation()}
            >
                {accent && <div className={styles.accent} />}
                {(title || icon || showCloseButton) && (
                    <div className={styles.header}>
                        <div className={styles.titleGroup}>
                            {icon && <span className={styles.icon}>{icon}</span>}
                            {title && <h2 className={styles.title}>{title}</h2>}
                        </div>
                        {showCloseButton && (
                            <button
                                type="button"
                                className={styles.closeBtn}
                                onClick={onClose}
                                aria-label="Fechar"
                            >
                                <X size={18} />
                            </button>
                        )}
                    </div>
                )}

                <div className={styles.body}>{children}</div>

                {footer && <div className={styles.footer}>{footer}</div>}
            </div>
        </div>,
        document.body
    );
}

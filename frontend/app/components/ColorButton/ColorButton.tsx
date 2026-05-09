"use client";

import React, { ButtonHTMLAttributes, CSSProperties } from "react";
import styles from "./ColorButton.module.css";

type ColorButtonProps = Omit<ButtonHTMLAttributes<HTMLButtonElement>, "color"> & {
    children: React.ReactNode;
    backgroundColor?: string;
    color?: string;
    onClick?: () => void;
};

export default function ColorButton({
    children,
    backgroundColor = "#0d9488",
    color = "#ffffff",
    onClick,
    type = "button",
    style,
    className,
    disabled,
    ...rest
}: ColorButtonProps) {
    const inlineStyle: CSSProperties = {
        backgroundColor,
        color,
        ...style,
    };

    return (
        <button
            type={type}
            onClick={onClick}
            disabled={disabled}
            className={`${styles.button} ${className ?? ""}`}
            style={inlineStyle}
            {...rest}
        >
            {children}
        </button>
    );
}

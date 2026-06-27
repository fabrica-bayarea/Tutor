"use client";

import { Search } from "lucide-react";
import styles from "./SearchInput.module.css";

type SearchInputProps = {
    value: string;
    onChange: (value: string) => void;
    placeholder?: string;
    className?: string;
};

export default function SearchInput({
    value,
    onChange,
    placeholder = "Buscar...",
    className,
}: SearchInputProps) {
    return (
        <div className={`${styles.wrapper} ${className ?? ""}`}>
            <Search size={16} className={styles.icon} />
            <input
                type="text"
                value={value}
                onChange={(e) => onChange(e.target.value)}
                placeholder={placeholder}
                className={styles.input}
            />
        </div>
    );
}

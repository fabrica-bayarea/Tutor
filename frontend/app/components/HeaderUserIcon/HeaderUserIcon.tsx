"use client";
import { useEffect, useRef, useState } from "react";
import { User, Settings, LogOut } from "lucide-react";
import styles from "./HeaderUserIcon.module.css";

interface HeaderUserIconInterface {
    onConfiguracoes: () => void,
    onSair: ()=> void
}

export default function HeaderUserIcon({ onConfiguracoes, onSair }:HeaderUserIconInterface) {
    const [open, setOpen] = useState(false);
    const wrapperRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        function handleClickOutside(e:any) {
            if (wrapperRef.current && !wrapperRef.current.contains(e.target)) {
                setOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    function handleConfiguracoes() {
        setOpen(false);
        onConfiguracoes?.();
    }

    function handleSair() {
        setOpen(false);
        onSair?.();
    }

    return (
        <div className={styles.wrapper} ref={wrapperRef}>
            <button
                className={styles.userButton}
                onClick={() => setOpen(prev => !prev)}
                aria-haspopup="true"
                aria-expanded={open}
                aria-label="Menu do usuário"
            >
                <User size={20} color="#0F766E" />
            </button>

            {open && (
                <div className={styles.dropdown} role="menu">
                    <button className={styles.dropdownItem} role="menuitem" onClick={handleConfiguracoes}>
                        <Settings size={15} />
                        Configurações
                    </button>
                    <button className={styles.dropdownItem} role="menuitem" onClick={handleSair}>
                        <LogOut size={15} />
                        Sair
                    </button>
                </div>
            )}
        </div>
    );
}
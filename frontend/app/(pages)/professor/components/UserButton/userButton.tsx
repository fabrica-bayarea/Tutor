"use client";

import { useState } from "react";
import styles from "./userButton.module.css";
import { UserRound } from "lucide-react";

export default function UserButton({ user = '' }) {
    const [open, setOpen] = useState(false);

    return (
        <>
        <div className={styles.wrapper}>
            <button 
                className={styles.btnUser} 
                onClick={() => setOpen(!open)}
            >
                <UserRound/>
            </button>

            {open && (
                <div className={styles.dropdown}>
                    <button>Perfil</button>
                    <button>Configurações</button>
                    <button>Sair</button>
                </div>
            )}
        </div>
        </>
    );
}

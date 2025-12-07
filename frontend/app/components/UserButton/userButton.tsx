"use client";

import { useState } from "react";
import styles from "./userButton.module.css";
import { Ban, Bolt, Coffee, UserRound } from "lucide-react";

export default function UserButton({ isProf = false, user='' }) {
    const [open, setOpen] = useState(false);
    const [eProfessor, seteProfessor] = useState(isProf)

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
                        <h1 className={styles.nomeUser}>{user}</h1>
                        <div className={styles.divAsideOtrButtonsProf}>
                            <div className={styles.asideOtrButtonProf}>
                                <a href="/configuracao">
                                <button className={styles.otrButtonProf}>
                                    <Bolt/>
                                    Configuração
                                </button>
                                </a>
                            </div>

                            {eProfessor &&
                            <div className={styles.asideOtrButtonProf}>
                                <div>
                                <a href="/professor">
                                <button className={styles.otrButtonProf}>
                                    <Coffee/>
                                    Área do Professor
                                </button>
                                </a>
                                </div>
                            </div>
                            }

                            <div className={styles.asideOtrButtonProf}>
                                <div>
                                <a href="/sair">
                                <button className={styles.otrButtonProf}>
                                    <Ban/>
                                    Sair
                                </button>
                                </a>
                                </div>
                            </div>
                        </div>
                </div>
            )}
        </div>
        </>
    );
}

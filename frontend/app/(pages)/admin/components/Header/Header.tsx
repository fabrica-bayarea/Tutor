"use client";

import styles from "./Header.module.css"
import { User, Bell, Menu } from "lucide-react";
import UrlChanfro from "./components/UrlChanfro";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { useAuth } from '@/utils/auth';

export default function Header(){
    const { user, isStudent, isProfessor, isAdmin } = useAuth();
    const url = usePathname();
    const [caminho, setCaminho] = useState("");
    
    useEffect(() => {
        const caminhoArray = url.split("/").at(-1) || "";
    setCaminho(caminhoArray);
    }, [url]);
    
    return(
        <header className={styles.headerConteiner}>
            <UrlChanfro/>
            <section className={styles.headerSectionUser}>
                <section className={styles.headerSectionUserMobileMenu}>
                    <Menu size={24}/>
                    <p>{caminho}</p>
                </section>
                <p>ADM - {user?.nome}</p>
                <button className={styles.bellButton}><Bell size={20} color="white"/></button>
                <button className={styles.userButton}><User size={20} color="#0F766E"/></button>
            </section>
        </header>
    )
}
"use client";

import styles from "./Header.module.css"
import { User, Bell, Menu } from "lucide-react";
import UrlChanfro from "./components/UrlChanfro";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from '@/utils/auth';
import HeaderUserIcon from "@/app/components/HeaderUserIcon/HeaderUserIcon";
import { logout } from "@/app/services/service_auth";

export default function Header(){
    const { user, isStudent, isProfessor, isAdmin } = useAuth();
    const url = usePathname();
    const router = useRouter();
    const [caminho, setCaminho] = useState("");

    useEffect(() => {
        const caminhoArray = url.split("/").at(-1) || "";
    setCaminho(caminhoArray);
    }, [url]);
    
    
    const handleSair = () => {
        router.push("/login")
        logout();
    }
    
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
                <HeaderUserIcon onConfiguracoes={()=>{console.log("config")}} onSair={handleSair}/>
            </section>
        </header>
    )
}
"use client"

import { MessageSquare, BookOpen, X} from "lucide-react";
import styles from "./Aside.module.css"
import { useRouter } from "next/navigation";
import { useContext, useEffect } from "react";
import { LayoutContext } from "@/contexts/LayoutContext";

interface ChatInterface {
    "id": string,
    "nome": string,
    "materia":string,
}

interface AsideProps {
    links: ChatInterface[],
    onNewChat: ()=>void
}

export default function Aside({links, onNewChat}:AsideProps){
    const router = useRouter();
    const { isMenuMobileAberto, setIsMenuAbertoMobile } = useContext(LayoutContext)!;
   
    useEffect(() => {
        const handleResize = () => {
            if (window.innerWidth >= 768) {
                setIsMenuAbertoMobile(true);
            }
        };

        handleResize(); 
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);


    const handleLink = (id:string) => {
        if (window.innerWidth <= 768) setIsMenuAbertoMobile(false)
        router.push(`/chat/${id}/historico`)
    }
    return (
        <nav className={isMenuMobileAberto ? styles.navAside : styles.navAsideHidden}>
            <section className={styles.sectionTitle}>
                <BookOpen color="#0D9488" />
                <h1>Tutor</h1>
            </section>
            <section className={styles.sectionButton}>
                <button onClick={onNewChat} type="submit">
                    <MessageSquare  className={styles.iconTitle}/>
                    Novo Chat
                </button>
            </section>
            <section className={styles.sectionSubTitle}>
                <p>RECENTES</p>
            </section>
            <section className={styles.sectionLink}>
                {links.map((chat:any,index:number)=>(
                    <button key={index} className={styles.linkChatAntigo} onClick={()=>{handleLink(chat.id)}}>
                        <p className={styles.titleLink}>{chat.nome}</p>
                        <p className={styles.subTitleLink}>{chat.materia}</p>
                    </button>
                ))}
            </section>
            <section className={styles.buttonClose}>
                <button onClick={() => setIsMenuAbertoMobile(false)}><X size={20} color="gray"/></button>
            </section>
        </nav>
    )
}
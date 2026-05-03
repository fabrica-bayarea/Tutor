"use client"

import { MessageSquare, BookOpen} from "lucide-react";
import styles from "./Aside.module.css"
import { useRouter } from "next/navigation";

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
    

    return (
        <nav className={styles.navAside}>
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
                    <button key={index} className={styles.linkChatAntigo} onClick={()=>{router.push(`/chat/${chat.id}/historico`)}}>
                        <p className={styles.titleLink}>{chat.nome}</p>
                        <p className={styles.subTitleLink}>{chat.materia}</p>
                    </button>
                ))}
            </section>
        </nav>
    )
}
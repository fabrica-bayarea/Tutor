import { MessageSquare, BookOpen} from "lucide-react";
import styles from "./Aside.module.css"
import { article, section } from "framer-motion/client";
import { useEffect, useState } from "react";


interface ChatInterface {
    "id": string,
    "nome": string,
    "materia":string
}

interface AsideProps {
    links: ChatInterface[];
}

export default function Aside({links}:AsideProps){
    return (
        <nav className={styles.navAside}>
            <section className={styles.sectionTitle}>
                <BookOpen color="#0D9488"/>
                <h1>Tutor</h1>
            </section>
            <section className={styles.sectionButton}>
                <button><MessageSquare  size={14} color="gray"/>Novo Chat</button>
            </section>
            <section className={styles.sectionSubTitle}>
                <p>RECENTES</p>
            </section>
            <section className={styles.sectionLink}>
                {links.map((chat:any,index:number)=>(
                    <a key={index} className={styles.linkChatAntigo} href={`/pages/${chat.id}/historico`}>
                        <p className={styles.titleLink}>{chat.nome}</p>
                        <p className={styles.subTitleLink}>{chat.materia}</p>
                    </a>
                ))}
            </section>
        </nav>
    )
}
'use client';

import { useState } from "react"
import styles from "./layout.module.css"
import Aside from "./components/Aside/Aside";
import { useRouter } from "next/navigation";

export default function AlunoLayout({ children }: { children: React.ReactNode }) {
    const [chatKey, setChatKey] = useState(0)
    const router = useRouter()

    const handleNewChat = ()=>{
        setChatKey(prev => prev + 1)
        router.push("/chat")
    }

    return (
        <section className={styles.mainSection}>
            <Aside links={[{"id":"1","materia":"Matemática","nome":"Quanto é 1 mais um?"}]}  onNewChat={handleNewChat}/>
            <section className={styles.pageMediaSection}>
                <section key={chatKey}>
                    {children}    
                </section>
            </section>
        </section>
    )
}
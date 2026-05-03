'use client';

import { useContext, useState } from "react"
import styles from "./layout.module.css"
import Aside from "./components/Aside/Aside";
import { useRouter } from "next/navigation";
import { LayoutContext } from "@/contexts/LayoutContext";

export default function AlunoLayout({ children }: { children: React.ReactNode }) {
    const [chatKey, setChatKey] = useState(0)
    const router = useRouter()
    const { isMenuMobileAberto, setIsMenuAbertoMobile } = useContext(LayoutContext)!;

    const handleNewChat = ()=>{
        setChatKey(prev => prev + 1)
        if (window.innerWidth <= 768) setIsMenuAbertoMobile(false)
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
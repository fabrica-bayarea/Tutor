'use client';

import { useContext, useState, useEffect } from "react"
import styles from "./layout.module.css"
import Aside from "./components/Aside/Aside";
import { useRouter } from "next/navigation";
import { LayoutContext } from "@/contexts/LayoutContext";
import { obterChats, obterMateriaId } from "@/app/services/service_chat";
import { useAuth } from "@/utils/auth";
import { obterMateria } from "@/app/services/service_materia";
import { InterfaceMateria } from "@/app/types";

interface InterfaceChatLink {
    id: string;
    materia: string;
    nome: string;
}

export default function AlunoLayout({ children }: { children: React.ReactNode }) {
    const [chatKey, setChatKey] = useState(0)
    const router = useRouter()
    const { isMenuMobileAberto, setIsMenuAbertoMobile } = useContext(LayoutContext)!;
    const { user } = useAuth();
    const [chatLinks, setChatLinks] = useState<InterfaceChatLink[]>([]);

    const handleNewChat = ()=>{
        setChatKey((prev: number) => prev + 1)
        if (window.innerWidth <= 768) setIsMenuAbertoMobile(false)
        router.push("/chat")
    }

    const getData = async () => {
        if (!user?.id) return;
        const chats = await obterChats(user?.id)

        const limitedChats = chats.slice(0, 5);

        const links = await Promise.all(
            limitedChats.map(async (el) => {
                const materiaId = await obterMateriaId(el.id);
                const materiaNome = await obterMateria(materiaId);
                return { id: el.id, materia: materiaNome.nome, nome: el.nome };
            })
        );

        setChatLinks(links);
    }

    useEffect(()=>{
        getData();
    },[user])

    return (
        <section className={styles.mainSection}>
            <Aside links={chatLinks}  onNewChat={handleNewChat}/>
            <section className={styles.pageMediaSection}>
                <section key={chatKey}>
                    {children}    
                </section>
            </section>
        </section>
    )
}

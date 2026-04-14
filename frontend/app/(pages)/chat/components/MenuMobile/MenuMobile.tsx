"use client";

import styles from "./MenuMobile.module.css";
import { Ban, Bolt, MessageCircleMore} from "lucide-react";

interface MenuMobileProps {
  onNovoChat?: () => void;
  onDash?: () => void;
  onConfig?: () => void;
  onSair?: () => void;
  isAdmin?: boolean;
}

export default function MenuMobile({ onNovoChat, onDash, onConfig, onSair, isAdmin=false }: MenuMobileProps){    
    return(
        <>
            <section className={styles.MenuMobileConteiner}>
                <article className={styles.MenuMobileArticle}>
                    <h3>Tutor AI</h3>
                    <button onClick={onNovoChat}><MessageCircleMore/>Novo Chat</button>
                    {isAdmin && ( 
                    <button onClick={onDash}><Bolt/>Dashboard</button>
                    )}
                    <button onClick={onConfig}><Bolt/>Configurações</button>
                    <button onClick={onSair}><Ban/>Sair</button>
                </article>
            </section>
        </>
    )
}

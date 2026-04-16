"use client";

import styles from "./MenuMobile.module.css";
import { Ban, Bolt, MessageCircleMore} from "lucide-react";
import { useRef } from "react";

interface MenuMobileProps {
  onNovoChat?: () => void;
  onDash?: () => void;
  onConfig?: () => void;
  onSair?: () => void;
  isAdmin?: boolean;
  onFechar?: () => void;
}

export default function MenuMobile({ onNovoChat, onDash, onConfig, onSair, isAdmin=false, onFechar }: MenuMobileProps){    
    const startY = useRef(0);

    const handleTouchStart = (e: React.TouchEvent) => {
        startY.current = e.touches[0].clientY;
    };

    const handleTouchEnd = (e: React.TouchEvent) => {
        const endY = e.changedTouches[0].clientY;
        const diff = startY.current - endY;

        if (diff > 50) {
            onFechar?.();
        }
    };

    return(
        <section 
        className={styles.MenuMobileConteiner}
        onTouchStart={handleTouchStart}
        onTouchEnd={handleTouchEnd}>
            <article className={styles.MenuMobileArticle}>
                <h3>Tutor AI</h3>
                <button onClick={onNovoChat}><MessageCircleMore/>Novo Chat</button>
                {isAdmin && ( 
                <button onClick={onDash}><Bolt/>Dashboard</button>
                )}
                <button onClick={onConfig}><Bolt/>Configurações</button>
                <button onClick={onSair}><Ban/>Desconectar</button>
            </article>
        </section>
    )
}

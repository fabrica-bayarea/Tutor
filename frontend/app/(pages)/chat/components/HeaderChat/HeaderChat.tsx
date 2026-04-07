import { Ban, Bolt, ChartArea, MessageCircleMore, User, ChevronDown } from "lucide-react";
import styles from "./HeaderChat.module.css";
import { useState } from "react";


interface HeaderChatProps {
  onNewChatClick?: () => void;
  onUserClick?: () => void;
  onNavItemClick?: (item: string) => void;
}

export default function HeaderChat({
  onNewChatClick,
  onUserClick,
  onNavItemClick,
}: HeaderChatProps) {
  const [navOpen, setNavOpen] = useState(false);

  const toggleNav = () => {
    setNavOpen((prev) => !prev);
  };

  return (
    <section className={styles.headerConteiner}>
      <section className={styles.headerDesktop}>
        <article>
          <h3>Tutor AI</h3>
          <button onClick={onNewChatClick}>
            <MessageCircleMore/>
            <p>Novo Chat</p>
          </button>
        </article>
        <button onClick={onUserClick}>
          <User/>
        </button>
        {navOpen && (
          <nav className={styles.navMenu}>
            <a href="#config" onClick={() => onNavItemClick?.("Configurações")}>
              <Bolt/>
              Configurações
            </a>
            <a href="#dashboard" onClick={() => onNavItemClick?.("Dashboard")}>
              <ChartArea />
              Dashboard
            </a>
            <a href="#sair" onClick={() => onNavItemClick?.("Sair")}>
              <Ban/>
              Sair
            </a>
          </nav>
        )}
      </section>
      <section className={styles.headerMobile}>
        <button onClick={toggleNav}>
          <ChevronDown />
        </button>
      </section>
    </section>
  );
}

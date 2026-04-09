import { Ban, Bolt, ChartArea, MessageCircleMore, User, ChevronDown } from "lucide-react";
import styles from "./HeaderChat.module.css";
import { useState, useEffect } from "react";
import MenuMobile from "../MenuMobile/MenuMobile";

interface HeaderChatProps {
  onNewChatClick?: () => void;
  onUserClick?: () => void;
  onNavItemClick?: (item: string) => void;
}

export default function HeaderChat({
  onNewChatClick,
  onNavItemClick,
}: HeaderChatProps) {
  const [navOpen, setNavOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth <= 768);
    checkMobile();
    window.addEventListener("resize", checkMobile);
    return () => window.removeEventListener("resize", checkMobile);
  }, []);

  const toggleNav = () => setNavOpen((prev) => !prev);

  return (
    <section className={styles.headerConteiner}>
      {!isMobile && (
        <section className={styles.headerDesktop}>
          <article>
            <h3>Tutor AI</h3>
            <button onClick={onNewChatClick}>
              <MessageCircleMore />
              <p>Novo Chat</p>
            </button>
          </article>
          <div className={styles.userMenuWrapper}>
            <button onClick={toggleNav}>
              <User />
            </button>
            {navOpen && (
              <nav className={styles.navMenu}>
                <a href="#config" onClick={() => onNavItemClick?.("Configurações")}>
                  <Bolt /> Configurações
                </a>
                <a href="#dashboard" onClick={() => onNavItemClick?.("Dashboard")}>
                  <ChartArea /> Dashboard
                </a>
                <a href="#sair" onClick={() => onNavItemClick?.("Sair")}>
                  <Ban /> Sair
                </a>
              </nav>
            )}
          </div>
        </section>
      )}

      {isMobile && (
        <section className={styles.headerMobile}>
          <button onClick={toggleNav}>
            <ChevronDown />
          </button>
          {navOpen && (
            <MenuMobile
              onNovoChat={onNewChatClick}
              onConfig={() => onNavItemClick?.("Configurações")}
              onSair={() => onNavItemClick?.("Sair")}
              onDash={() => onNavItemClick?.("Dashboard")}
            />
          )}
        </section>
      )}
    </section>
  );
}

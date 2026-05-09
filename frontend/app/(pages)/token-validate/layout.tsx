import { GraduationCap, MessageCircle, BarChart3, BookMarked } from 'lucide-react';
import styles from './layout.module.css';

export default function LoginLayout({ children }: { children: React.ReactNode }) {
    return (
        <main className={styles.pageContainer}>
            <aside className={styles.aside}>
                <div className={styles.asideCircleTop} aria-hidden="true" />
                <div className={styles.asideCircleBottom} aria-hidden="true" />

                <div className={styles.asideContent}>
                    <div className={styles.asideBrand}>
                        <div className={styles.asideLogo}>
                            <BookMarked size={22} strokeWidth={2.4} />
                        </div>
                        <span className={styles.asideBrandName}>Tutor</span>
                    </div>

                    <h1 className={styles.asideTitle}>
                        A plataforma de tutoria inteligente para sua instituição.
                    </h1>

                    <ul className={styles.asideFeatures}>
                        <li>
                            <GraduationCap size={20} />
                            <span>Respostas baseadas nos seus materiais didáticos</span>
                        </li>
                        <li>
                            <MessageCircle size={20} />
                            <span>Chat inteligente com contexto por matéria</span>
                        </li>
                        <li>
                            <BarChart3 size={20} />
                            <span>Dashboard analítico para professores</span>
                        </li>
                    </ul>
                </div>
            </aside>

            <h1 className={styles.mobileTitle}>
                A plataforma de tutoria inteligente para sua instituição.
            </h1>

            <div className={styles.contentWrapper}>
                {children}
            </div>
        </main>
    );
}

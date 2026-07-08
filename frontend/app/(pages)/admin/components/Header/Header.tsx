"use client";

import styles from "./Header.module.css"
import { Bell, Menu, Home } from "lucide-react";
import { usePathname } from "next/navigation";
import { useContext, useEffect, useState } from "react";
import { useAuth } from '@/utils/auth';
import { LayoutContext } from '@/contexts/LayoutContext';
import { Role } from '@/utils/roles';
import HeaderUserIcon from "@/app/components/HeaderUserIcon/HeaderUserIcon";
import Breadcrumb from "@/app/components/Breadcrumb/Breadcrumb";
import { logout } from "@/app/services/service_auth";

function slugToLabel(slug: string): string {
    return slug
        .replace(/([A-Z])/g, ' $1')
        .replace(/^./, s => s.toUpperCase())
        .trim();
}

const roleLabel: Record<string, string> = {
    [Role.ADMIN]:     'Administrador',
    [Role.PROFESSOR]: 'Professor',
    [Role.ALUNO]:     'Aluno',
};

export default function Header(){
    const { user } = useAuth();
    const pathname = usePathname();
    const { setIsMenuAbertoMobile } = useContext(LayoutContext)!;
    const [caminho, setCaminho] = useState("");

    const segments = (pathname ?? '').split('/').filter(s => s !== '' && s !== 'admin' && s !== 'pages');

    const breadcrumbItems = [
        { label: '', icon: <Home size={14} />, href: segments.length > 0 ? '/admin' : undefined },
        ...segments.map((seg, i) => ({
            label: slugToLabel(seg),
            href: i < segments.length - 1
                ? `/admin/pages/${segments.slice(0, i + 1).join('/')}`
                : undefined,
        })),
    ];

    useEffect(() => {
        setCaminho(segments.at(-1) ? slugToLabel(segments.at(-1)!) : '');
    }, [pathname]);

    const handleSair = async () => {
        await logout();
        // Redireciona com replace (recarrega e limpa o histórico) somente após o
        // cookie de sessão ser removido, evitando que o middleware reenvie o
        // usuário de volta à área autenticada (US-05-RN1).
        window.location.replace("/tutor/login");
    };

    return(
        <header className={styles.headerConteiner}>
            <div className={styles.breadcrumbWrapper}>
                <Breadcrumb items={breadcrumbItems} />
            </div>
            <section className={styles.headerSectionUser}>
                <section className={styles.headerSectionUserMobileMenu}>
                    <Menu size={24} style={{ cursor: 'pointer' }} onClick={() => setIsMenuAbertoMobile(true)} />
                    <p>{caminho}</p>
                </section>
                <p>{user?.role ? roleLabel[user.role] ?? user.role : ''} - {user?.nome}</p>
                <button className={styles.bellButton}><Bell size={20} color="white"/></button>
                <HeaderUserIcon onConfiguracoes={()=>{console.log("config")}} onSair={handleSair}/>
            </section>
        </header>
    )
}

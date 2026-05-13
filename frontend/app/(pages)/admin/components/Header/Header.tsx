"use client";

import styles from "./Header.module.css"
import { Bell, Menu, Home } from "lucide-react";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from '@/utils/auth';
import HeaderUserIcon from "@/app/components/HeaderUserIcon/HeaderUserIcon";
import Breadcrumb from "@/app/components/Breadcrumb/Breadcrumb";
import { logout } from "@/app/services/service_auth";

function slugToLabel(slug: string): string {
    return slug
        .replace(/([A-Z])/g, ' $1')
        .replace(/^./, s => s.toUpperCase())
        .trim();
}

export default function Header(){
    const { user } = useAuth();
    const pathname = usePathname();
    const router = useRouter();
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

    const handleSair = () => {
        router.push("/login");
        logout();
    };

    return(
        <header className={styles.headerConteiner}>
            <div className={styles.breadcrumbWrapper}>
                <Breadcrumb items={breadcrumbItems} />
            </div>
            <section className={styles.headerSectionUser}>
                <section className={styles.headerSectionUserMobileMenu}>
                    <Menu size={24}/>
                    <p>{caminho}</p>
                </section>
                <p>ADM - {user?.nome}</p>
                <button className={styles.bellButton}><Bell size={20} color="white"/></button>
                <HeaderUserIcon onConfiguracoes={()=>{console.log("config")}} onSair={handleSair}/>
            </section>
        </header>
    )
}

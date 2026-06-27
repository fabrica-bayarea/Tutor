"use client";

import styles from "./Header.module.css"
import { User, Bell, Menu } from "lucide-react";
import { useAuth } from "@/utils/auth";
import { useData } from "@/utils/data";
import { useContext } from "react";
import { LayoutContext } from "@/contexts/LayoutContext";
import HeaderUserIcon from "@/app/components/HeaderUserIcon/HeaderUserIcon";
import { logout } from "@/app/services/service_auth";

interface HeaderInterface {
    isSelectInactive: boolean;
    materiaName: string;
    onMateriaChange?: (materiaId: string) => void;
}

export default function Header({ isSelectInactive, materiaName, onMateriaChange }: HeaderInterface) {
    const { user } = useAuth();
    const { materias } = useData();
    const { setIsMenuAbertoMobile } = useContext(LayoutContext)!;

    const handleSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const selectedIndex = e.target.selectedIndex;
        const selectedMateria = materias[selectedIndex];
        if (selectedMateria && onMateriaChange) {
            onMateriaChange(selectedMateria.id);
        }
    };

    
    const handleSair = async () => {
        await logout();
        // Redireciona com replace (recarrega e limpa o histórico) somente após o
        // cookie de sessão ser removido, evitando que o middleware reenvie o
        // usuário de volta à área autenticada (US-05-RN1).
        window.location.replace("/login");
    }


    return (
        <section className={styles.headerConteiner}>
            <section className={styles.headerSectionUserMobileMenu}>
                <Menu size={24} onClick={() => setIsMenuAbertoMobile(true)} />
            </section>
            {materiaName !== "" ?
                <select
                    disabled={isSelectInactive}
                    className={styles.selectMateria}
                    onChange={handleSelectChange}
                >
                    <option>{materiaName}</option>
                </select>
                :
                <select
                    disabled={isSelectInactive}
                    className={styles.selectMateria}
                    onChange={handleSelectChange}
                >
                    {materias &&( materias.map((materia, index) => (
                        <option key={index} value={materia.id}>
                            {materia.nome}
                        </option>
                    )))}
                </select>
            }
            <section className={styles.headerSectionUser}>
                <p>ADM - {user?.nome}</p>
                <button className={styles.bellButton}><Bell size={20} color="white" /></button>
                <HeaderUserIcon onConfiguracoes={()=>{console.log("config")}} onSair={handleSair}/>
            </section>
        </section>
    )
}

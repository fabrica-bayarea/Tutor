import styles from "./Header.module.css"
import { User, Bell, Menu } from "lucide-react";
import { useAuth } from "@/utils/auth";
import { useData } from "@/utils/data";
import { useContext } from "react";
import { LayoutContext } from "@/contexts/LayoutContext";

interface HeaderInterface {
    isSelectInactive: boolean,
    materiaName: string
}

export default function Header({isSelectInactive, materiaName}:HeaderInterface){
    const { user } = useAuth();
    const { materias } = useData();
    const { setIsMenuAbertoMobile } = useContext(LayoutContext)!;
    
    return(
        <section className={styles.headerConteiner}>
            <section className={styles.headerSectionUserMobileMenu}>
                <Menu size={24} onClick={() => setIsMenuAbertoMobile(true)}/>
            </section>
            {materiaName !== "" ? 
                <select name="" id="" disabled={isSelectInactive} className={styles.selectMateria}>
                    <option>{materiaName}</option>
                </select>
            :
                <select name="" id="" disabled={isSelectInactive} className={styles.selectMateria}>
                    {Object.entries(materias).map((materia:any,index)=>(
                        <option key={index}>{materia?.nome}</option>
                    ))}
                </select>            
            }
            <section className={styles.headerSectionUser}>
                <p>ADM - {user?.nome}</p>
                <button className={styles.bellButton}><Bell size={20} color="white"/></button>
                <button className={styles.userButton}><User size={20} color="#0F766E"/></button>
            </section>
        </section>
    )
}
import styles from "./Header.module.css"
import { User, Bell, Menu } from "lucide-react";
import { useAuth } from "@/utils/auth";
import { useData } from "@/utils/data";
import { useContext } from "react";
import { LayoutContext } from "@/contexts/LayoutContext";

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
                    {materias.map((materia, index) => (
                        <option key={index} value={materia.id}>
                            {materia.nome}
                        </option>
                    ))}
                </select>
            }
            <section className={styles.headerSectionUser}>
                <p>ADM - {user?.nome}</p>
                <button className={styles.bellButton}><Bell size={20} color="white" /></button>
                <button className={styles.userButton}><User size={20} color="#0F766E" /></button>
            </section>
        </section>
    )
}

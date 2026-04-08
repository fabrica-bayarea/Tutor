"use client";

import { useState } from "react";
import styles from "./SelectMaterias.module.css";

interface SelectMateriasProps {
    materias: Record<string, string>;
    onChange?: (id: string, nome: string) => void;
}

export default function SelectMaterias({materias,onChange}: SelectMateriasProps){

    const [materiaSelecionada, setMateriaSelecionada] = useState<string>("");

    const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
      const id = event.target.value;
      const nome = materias[id];
      setMateriaSelecionada(id);
      if (onChange) {
        onChange(id, nome);
      }
    };

    return(
        <>
            <section className={styles.selectMateriasConteiner}>
                <article className={styles.articleSelectMaterias}>
                    <h1>Escolha a Matéria</h1>
                    <select className={styles.selectMaterias}>
                    <option value="" disabled>Selecione...</option>
                    {Object.entries(materias).map(([id, nome]) => (
                        <option key={id} value={id}>
                        {nome}
                        </option>
                    ))}
                    </select>
                </article>
            </section>
        </>
    )
}

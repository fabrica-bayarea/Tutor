import { usePathname } from "next/navigation";
import styles from "./UrlChanfro.module.css"
import { useEffect } from "react";
import { useState } from "react";
import { Home } from 'lucide-react'

export default function UrlChanfro(){
    const caminho = usePathname();
    const [caminhos, setCaminhos] = useState<string[]>([]);

    useEffect(() => {
        const caminhoArray = caminho.split("/").filter(el => el !== "" && el !== "admin" && el !== "pages");
    setCaminhos(caminhoArray);
    }, [caminho]);


    return (
    <section className={styles.chanfroConteiner}>
        {caminhos.length == 0 ? (
            <span className={styles.chanfroInicialCor}>
                <Home size={14} color="white"/>
            </span>
        ) :
        (
            <span className={styles.chanfroInicial}>
                <Home size={14} color="#14B8A6"/>
            </span>
        )}
        {caminhos.map((el, index) => {
        const isLast = index === caminhos.length - 1;

        return (
            <span
            key={index}
            className={`${styles.tab} ${isLast ? styles.active : ""}`}
            >
            {el}
            </span>
        );
        })}
    </section>
    )
}
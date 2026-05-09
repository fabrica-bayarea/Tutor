import { ReactNode } from "react"
import styles from "./Card.module.css"

interface Cardinterface {
    title: string,
    subtitle: string,
    children: ReactNode,
    onClick: ()=> void
}

export default function Card({title,subtitle,children, onClick}:Cardinterface){
    return(
        <button className={styles.buttonSection} onClick={onClick}>
            {children}
            <section>
                <p className={styles.buttonTitle}>{title}</p>
                <p className={styles.buttonSubTitle}>{subtitle}</p>    
            </section>
        </button>
    )
}
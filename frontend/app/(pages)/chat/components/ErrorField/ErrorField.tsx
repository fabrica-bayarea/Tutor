import { Ban } from "lucide-react"
import styles from "./ErrorField.module.css"

interface ErrorFieldProp{
    temErro: boolean
}

export default function ErrorField({temErro}:ErrorFieldProp){

    return (
        <footer className={styles.errorFieldFooter}>
            {!temErro &&
                <span>As respostas são baseadas nos materiais do professor.</span>
            }
            {temErro &&
                <section>
                    <Ban size={13} color="rgba(178, 64, 26, 1)"/>
                    <p>Envio bloqueado enquando a IA responde</p>
                </section>
            }
        </footer>
    )
}
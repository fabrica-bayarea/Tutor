import { BookOpen, MessageCircleQuestion, File, Lightbulb, Book } from "lucide-react"
import styles from "./NoMessageField.module.css"
import Card from "./components/Card"

export default function NoMessageField(){
    return(
        <section className={styles.NoMessageConteiner}>
            <section className={styles.NoMessageSection}>
                <BookOpen className={styles.titleIcon}/>
                <h1 className={styles.titleText}>Olá, Aluno!</h1>
                <p className={styles.subTitleText}>Como posso ajudá-lo hoje?</p>
                <article>
                    <Card onClick={()=>{}} title="Tirar Dúvida" subtitle="Explique um conceito da matéria">
                        <MessageCircleQuestion color="rgba(15, 118, 110, 1)"/>
                    </Card>
                    <Card onClick={()=>{}} title="Resumir Material" subtitle="Peça um resumo de um tema do conteúdo">
                        <File color="rgba(15, 118, 110, 1)"/>
                    </Card>
                    <Card onClick={()=>{}} title="Preparar para a prova" subtitle="Crie questões de estudo sobre um tema">
                        <Lightbulb color="rgba(15, 118, 110, 1)"/>
                    </Card>
                    <Card onClick={()=>{}} title="Aprofundar tema" subtitle="Informe um tema para explorar em detalhes">
                        <Book color="rgba(15, 118, 110, 1)"/>
                    </Card>
                </article>
            </section>
        </section>
    )
}
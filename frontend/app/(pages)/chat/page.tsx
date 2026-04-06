import socket from "@/libs/socket";
import { useEffect, useState } from "react";

export default function Home(){

    const [eProfessor, seteProfessor] = useState<boolean>(true);
    const [user, setUser] = useState<string>("");
    
    //estado para testar se a tela precisa pedir a matéria do chat
    const [novoChat, setNovoChat] = useState<boolean>(false);
    
    const [materia,setMateria] = useState<string>("")

    useEffect(()=>{
        //listener do evento de atualização de status(processando,gerando trechos,gerando resposta)
        socket.on("att_status",()=>{})

        //listener do evento de recebimento de chunk de resposta
        socket.on("chunk_resposta",()=>{})
     
        //listener do evento de recebimento da resposta completa
        socket.on("resposta_completa",()=>{})

        //listener do evento de erro recebido pelo back
        socket.on("erro",()=>{})

        return () => {
            // Limpeza para evitar múltiplos listeners em hot reload
            socket.off("att_status")
            socket.off("chunk_resposta")
            socket.off("resposta_completa")
            socket.off("erro")
            }
    },[]);

    const handleEnviar = "";
    
    const handleNovoChat = "";

    return(
        <div>
            <header>
                <section>
                    <h2>Tutor AI</h2>                
                    <button>
                        <img src="" alt="ícone de chat"/>
                        Novo Chat
                    </button>
                    <img src="" alt="seta"/>
                </section>
                <section>
                    <img src="" alt="ícone de usuário" />
                </section>
            </header>
            <nav>
                <h2>Tutor AI</h2>
                <section>
                    <button>
                        <img src="" alt="ícone de chat"/>
                        Novo Chat
                    </button>
                    <button>
                        <img src="" alt="ícone de chat"/>
                        Configuração
                    </button>
                    <button>
                        <img src="" alt="ícone de chat"/>
                        Sair
                    </button>
                </section>
            </nav>
            <main>
                <section>
                    {/** 
                     * 
                     * Aqui o código referente as mensagens recebidas/enviadas.
                     * 
                     * **/}
                </section>
                <section>
                    <h1>Olá, {"aluno"}!</h1>
                    <h2>Tutor AI</h2>
                    <p>Como posso ajudá-lo hoje?</p>
                </section>
                <section>
                    <img src="" alt="icone de adição" />
                    <article>
                        <textarea/>
                        <img src="" alt="icone de adição" />
                        <img src="" alt="imagem de enviar" />
                    </article>
                </section>
            </main>
            <footer>
                <p>A inteligência artificial pode cometer erros. Considere checar informações importantes.</p>
            </footer>
        </div>
)
}
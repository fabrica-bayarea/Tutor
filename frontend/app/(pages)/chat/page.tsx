"use client";

import socket from "@/libs/socket";
import { useEffect, useState } from "react";
import { Ban, Bolt, ChevronDown, MessageCircleMore, Plus, SendHorizonal, User } from "lucide-react";
import Head from 'next/head';
import TextAreaChat from "./Components/TextAreaChat/TextAreaChat";

export default function Home(){

    const [eProfessor, seteProfessor] = useState<boolean>(true);
    const [user, setUser] = useState<string>("");

    //handler do componente de textarea de envio de mensagens
    const [mensagemAtual, setMensagemAtual] = useState("");
    function handleSend() {
        console.log("Enviar:", mensagemAtual);
        setMensagemAtual("");
    }
    
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

    return (
    <>    
    <script src="https://cdn.tailwindcss.com"></script>
    <div className="flex flex-col min-h-screen">    

        <header className="flex-shrink-0 m-5">
            <section className="flex justify-center md:hidden">
            <button id="openNav" aria-label="Abrir menu" className="p-2">
                <ChevronDown width={6} height={6}/>
            </button>
            </section>

            <section className="hidden md:flex justify-between items-center">
            <article className="flex items-center">
                <h3 className="text-lg font-semibold">Tutor AI</h3>

                <button id="newChatBtn" className="ml-8 flex items-center gap-2 px-2 py-1 rounded-md border border-black bg-transparent">
                <MessageCircleMore width={5} height={5}/>
                <p className="text-sm">Novo Chat</p>
                </button>
            </article>

            <User className="w-10 h-10 rounded-full border border-black p-1"/>
            </section>
        </header>

        <nav id="navOverlay" className="hidden fixed inset-0 z-50 flex justify-center items-start backdrop-blur-sm pt-8">
            <section className="bg-white/90 rounded-xl flex flex-col max-w-md w-[90%] gap-4 text-center p-6">
            <div className="flex justify-center items-center">
                <h3 className="text-lg font-semibold">Tutor AI</h3>
            </div>

            <button className="flex items-center justify-center gap-2 p-2 border border-black rounded-md bg-transparent">
                <MessageCircleMore width={5} height={5}/>
                <p>Novo Chat</p>
            </button>

            <button className="flex items-center justify-center gap-2 p-2 border border-black rounded-md bg-transparent">
                <Bolt width={5} height={5}/>
                <p>Configurações</p>
            </button>

            <button className="flex items-center justify-center gap-2 p-2 border border-black rounded-md bg-transparent">
                <Ban width={5} height={5}/>
                <p>Sair</p>
            </button>
            </section>
        </nav>

        <main className="flex flex-col flex-1 m-2 relative">
            <section className="centerTitleNoMessage absolute inset-0 flex items-center justify-center">
            <div className="text-center w-[95%]">
                <h2 className="text-2xl tracking-wide">Bem-vindo [aluno]</h2>
                <p className="text-gray-400 mt-2">A inteligência artificial pode cometer erros. Considere checar informações importantes.</p>
            </div>
            </section>

            <section className="centerTitleMessage hidden absolute inset-0 flex items-center justify-center text-gray-400 tracking-wide">
            <div className="text-center w-[95%]">
                <h3 className="text-xl">Tutor AI</h3>
            </div>
            </section>

            <section id="chooseClass" className="hidden fixed inset-0 z-50 flex flex-col justify-center items-center backdrop-blur-sm gap-2 p-6">
            <div className="bg-white/90 rounded-lg w-[90%] max-w-md p-6 flex flex-col items-center gap-4">
                <h3 className="text-lg font-semibold">Escolha a Matéria</h3>
                <select className="select-chevron appearance-none bg-transparent border border-black rounded px-3 py-2 w-full max-w-md text-black">
                <option value="materia">Matéria</option>
                </select>
                <div className="w-full flex justify-end">
                <button id="closeChooseClass" className="mt-2 px-3 py-1 border border-black rounded">Fechar</button>
                </div>
            </div>
            </section>

            <section className="chatField flex-1 overflow-auto pt-4 pb-24">
            </section>
    
            <TextAreaChat
                value={mensagemAtual}
                onChange={setMensagemAtual}
                onSend={handleSend}
                onPlusClick={() => console.log("Abrir anexos")}
            />
        </main>

        <footer className="hidden md:flex flex-shrink-0 justify-center items-center m-1 text-gray-400">
            <p>A inteligência artificial pode cometer erros. Considere checar informações importantes.</p>
        </footer>
    </div>
    </>
);}

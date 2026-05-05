"use client"

import { useState, useRef, useEffect } from "react";
import { useParams } from "next/navigation";
import Header from "../../../components/Header/Header";
import MessageField, {MessageFieldRef} from "../../../components/MessageField/MessageField";
import { obterMateriaId } from "@/app/services/service_chat";
import { obterMateria } from "@/app/services/service_materia";
import { obterMensagens } from "@/app/services/service_mensagem";

export default function Historico(){
    const params = useParams();
    const id = params.id as string;

    const [temMensagem, setTemMensagem] = useState(true)
    const messageFieldRef = useRef<MessageFieldRef>(null);
    const [materia, setMateria] = useState("")

    useEffect(async ()=>{
        const carregarDados = async () => {
            let idMateria = await obterMateriaId(id);
            let registro_materia = await obterMateria(idMateria);
            setMateria(registro_materia["nome"]);

            let messages = await obterMensagens(id);
            messages.forEach((el) => {
                messageFieldRef.current?.addMessage(el["sender_type"], el["conteudo"]);
            });
        };

        carregarDados();
    },[id]);
    
    return(
        <>
            <Header isSelectInactive={temMensagem} materiaName={materia}/>
            <MessageField ref={messageFieldRef}/> 
        </>
    )
}

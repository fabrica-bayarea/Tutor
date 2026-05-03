"use client"

import { useEffect, useRef, useState } from "react";
import Header from "./components/Header/Header"
import MessageField, { MessageFieldRef } from "./components/MessageField/MessageField"
import TextArea from "./components/TextArea/TextArea"
import NoMessageField from "./components/NoMessageField/NoMessageField";

import { promptDeep, promptExam, promptQuestion, promptSummarize } from "./utils/prompts";
import ErrorField from "./components/ErrorField/ErrorField";
import { useData } from "@/utils/data";
import { useAuth } from "@/utils/auth";

export default function Chat(){
    const messageFieldRef = useRef<MessageFieldRef>(null);
    const [temMensagem, setTemMensagem] = useState(false);
    const [text,setText] = useState("");
    const [podeEnviarMensagem, setPodeEnviarMensagem] = useState(true);
    const [mensagemPendente, setMensagemPendente] = useState("");
    const [permitido, setPermitido] = useState(true);
    const { user } = useAuth();
    const { materias } = useData();

    const handleSend = () => {
        if (text.trim() === '') return;

        if (!temMensagem) {
            setMensagemPendente(text);
            setTemMensagem(true);
        } else {
            messageFieldRef.current?.addMessage("user", text);
        }

        setText("");
        setPodeEnviarMensagem(false);
    };

    useEffect(() => {
        if (temMensagem && mensagemPendente) {
            messageFieldRef.current?.addMessage("user", mensagemPendente);
            setMensagemPendente("");
        }
    }, [temMensagem, mensagemPendente]);

    useEffect(() => {
        messageFieldRef.current?.deleteAllMessages();
        setTemMensagem(false);
        setText("");
        setPodeEnviarMensagem(true);
        if(materias == null){
            setPermitido(false)
        }
    }, [])
    
    return(
        <>

            <Header isSelectInactive={temMensagem} materiaName=""/>
            { temMensagem 
            ? <MessageField ref={messageFieldRef}/> 
            : <NoMessageField
                onAskQuestion={() => {setText(promptQuestion)}}
                onSummarize={() => {setText(promptSummarize)}}
                onPrepareExam={() => {setText(promptExam)}}
                onDeepDive={() => {setText(promptDeep);}}
            />}
            <TextArea
                value={text}
                onChange={setText}
                onSend={handleSend}
                isDisabled={!podeEnviarMensagem}
            />
            <ErrorField temErro={!podeEnviarMensagem}/>
        </>
    )
}
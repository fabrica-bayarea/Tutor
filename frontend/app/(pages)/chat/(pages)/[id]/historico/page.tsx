"use client"

import { useState, useRef, useEffect } from "react";
import Header from "../../../components/Header/Header";
import MessageField, {MessageFieldRef} from "../../../components/MessageField/MessageField";
import { mockMessages } from "../../../utils/prompts";

export default function Historico(){
    const [temMensagem, setTemMensagem] = useState(true)
    const messageFieldRef = useRef<MessageFieldRef>(null);
    const [materia, setMateria] = useState("Matemática")

    useEffect(()=>{
        mockMessages.forEach((el)=>{
            if(el["type"] == "user") messageFieldRef.current?.addMessage("user",el["message"])
            else messageFieldRef.current?.addMessage("llm",el["message"])
        })
    },[])
    return(
        <>
            <Header isSelectInactive={temMensagem} materiaName={materia}/>
            <MessageField ref={messageFieldRef}/> 
        </>
    )
}
"use client"

import { useEffect, useRef, useState } from "react";
import Header from "./components/Header/Header"
import MessageField, { MessageFieldRef } from "./components/MessageField/MessageField"
import TextArea from "./components/TextArea/TextArea"
import NoMessageField from "./components/NoMessageField/NoMessageField";

export default function Chat(){
    const messageFieldRef = useRef<MessageFieldRef>(null);
    const [temMensagem, setTemMensagem] = useState(false);
    const [text,setText] = useState("")

    useEffect(()=>{
        messageFieldRef.current?.addMessage("user","Olá");
        messageFieldRef.current?.addMessage("llm","Olá");
    },[])

    const handleSend = () => {
        setText("")
    }

    return(
        <>
            <Header isSelectInactive={false}/>
            { temMensagem 
            ? <MessageField ref={messageFieldRef}/> 
            : <NoMessageField/>}
            <TextArea
                value={text}
                onChange={setText}
                onSend={handleSend}
                isDisabled={false}
            />
        </>
    )
}
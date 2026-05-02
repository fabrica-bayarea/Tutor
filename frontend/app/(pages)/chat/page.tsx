"use client"

import Header from "./components/Header/Header"
import MessageField from "./components/MessageField/MessageField"
import TextArea from "./components/TextArea/TextArea"

export default function Chat(){
    return(
        <>
            <Header isSelectInactive={false}/>
            <MessageField/>
            <TextArea/>
        </>
    )
}
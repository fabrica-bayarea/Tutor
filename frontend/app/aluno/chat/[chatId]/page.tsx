'use client';

import { useState } from 'react';

export default function Chat() {
    const [chat, setChat] = useState({});
    const [messages, setMessages] = useState([]);
    
    return (
        <div>
            <h1>Chat</h1>
        </div>
    );
}

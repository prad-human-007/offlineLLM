import { useEffect, useRef } from "react";
import Markdown from 'react-markdown'

export interface Msg {
    role: 'user' | 'assistant'
    content: string
}

interface MessageBoxProps {
    messages: Msg[];
}

export function MessageBox({ messages }: MessageBoxProps) {
    const endOfMessagesRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    return (
        <div className="flex flex-col flex-grow gap-2  overflow-y-auto p-2">
            {messages.map((message, idx) => (
                <Message key={idx} idx={idx} message={message}/>
            ))}
            <div ref={endOfMessagesRef} />
        </div>
    );
}

function Message({message, idx} : {message: Msg, idx: number}) {
    return (
        <div key={idx} className={`flex w-full p-1 ${message.role=='user'? 'justify-end text-right' : ''}`}>
            <div className={`flex flex-col w-fit p-1 px-3 ${message.role=='user'?'border border-gray-300 shadow-md rounded-2xl': ''} `}>
                <p className="text-lg"><Markdown>{message.content}</Markdown></p>
            </div>
        </div>
    )
}

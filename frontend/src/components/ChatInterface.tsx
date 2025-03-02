import { SendHorizonal } from "lucide-react";
import { useState } from "react";
import { Msg, MessageBox } from "./MessageBox";
const URL = '0.0.0.0:8000'


export function ChatInterface() {
    const [inputText, setInputText] = useState('')
    const [messages, setMessages] = useState<Msg[]>([])

    async function sendMessage() {
        if (!inputText) return;

        setMessages((prev) => [...prev, { role: "user", content: inputText }]);
        setInputText('');

        const response = await fetch(`http://${URL}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem("token")}`
            },
            body: JSON.stringify({ messages: [...messages, {role: 'user', content: inputText}] }),
        });

        const {message} = await response.json()
        setMessages((prev) => [...prev, {role: 'assistant', content: message}])
        
    }

    return (
        <div className="flex flex-col w-full h-full border border-gray-500 rounded-2xl">
            <MessageBox messages={messages}/>

            {/* Input Box */}
            <div className="flex flex-row items-center p-4 gap-2">
                <input 
                    type="text"
                    className="w-full border border-gray-400 rounded-lg p-2"
                    placeholder="Enter your Message here"
                    value={inputText}
                    onChange={(e) => {setInputText(e.target.value)}}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                            if(inputText)
                                sendMessage();
                        }
                    }}
                />

                <button onClick={sendMessage}>
                    <SendHorizonal />
                </button>
            </div>
        </div>       
    )
}
import { SendHorizonal } from "lucide-react";
import { useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";
import { Msg, MessageBox } from "./MessageBox";
const URL = '0.0.0.0:8000'

const users: any = {
    tony: 'CEO',
    sam: 'Manager',
    rob: 'Employee'
}

export function ChatInterface() {
    const [inputText, setInputText] = useState('')
    const [messages, setMessages] = useState<Msg[]>([])
    const [username, setUsername] = useState("");
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        const token = localStorage.getItem("token"); // Get JWT token
        if (token) {
            try {
                const decoded: any = jwtDecode(token); // Decode the token
                setUsername(decoded.subject.username)
            } catch (error) {
                console.error("Invalid token", error);
            }
        }
    }, []);

    async function sendMessage() {
        if (!inputText) return;

        setMessages((prev) => [...prev, { role: "user", content: inputText }]);
        setInputText('');
        setLoading(true)

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
        setLoading(false)
    }

    return (
        <div className="flex flex-col w-full h-full border border-gray-500 rounded-2xl">
            <div className="flex flex-row border-b-1 p-3 items-center justify-between">
                <div className="text-xl ">{`User:  ${username} - ${users[username]}`}</div>
                <a href="/login" >Login</a>
            </div>
            <MessageBox messages={messages} loading={loading}/>

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
import { SendHorizonal } from "lucide-react";
import { useState, useEffect, useRef } from "react";
import { Msg, MessageBox } from "./MessageBox";



export function ChatInterface() {
    const [inputText, setInputText] = useState('')
    const [messages, setMessages] = useState<Msg[]>([])

    function sendMessage() {
        setMessages([...messages, {role: 'user', content: inputText}])
        // Fetch ai for response
        // get response from AI and show streaming response. 
        setInputText('')
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
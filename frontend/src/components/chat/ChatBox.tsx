"use client";
import { useState } from "react";
import { chatStream } from "@/src/lib/api";

export default function ChatBox() {
    const [input, setInput] = useState("");
    const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const newMessages = [...messages, { role: "user", content: input }];
        setMessages(newMessages);
        setInput("");

        let aiResponse = "";
        setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

        await chatStream(input, (chunk) => {
            aiResponse += chunk;
            setMessages((prev) => {
                const newMessages = [...prev];
                newMessages[newMessages.length - 1].content = aiResponse;
                return newMessages;
            })
        })
    };

    return (
        <div className="flex flex-col h-[600px] w-full max-w-2xl border rounded-lg bg-white shadow-xl">
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((m, i) => (
                <div key={i} className={`p-3 rounded-lg ${m.role === "user" ? "bg-blue-100 ml-auto" : "bg-gray-100 mr-auto"} max-w-[80%]`}>
                    {m.content || "..."}
                </div>
                ))}
            </div>
            <div className="p-4 border-t flex gap-2">
                <input 
                className="flex-1 border rounded px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSend()}
                placeholder="Ask your question..."
                />
                <button onClick={handleSend} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition">
                Envoyer
                </button>
            </div>
        </div>
    );
}
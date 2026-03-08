"use client";
import { useState, useEffect, useRef } from "react";
import { chatStream } from "@/src/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Send, Bot, User } from "lucide-react";

export default function ChatBox() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    setMessages((prev) => [...prev, { role: "assistant", content: "" }]);
    let aiResponse = "";

    await chatStream(input, (chunk) => {
      aiResponse += chunk;
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1].content = aiResponse;
        return updated;
      });

    }, (error) => {
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1].content = error;
        return updated;
      });
    });
  };

  return (
    <Card className="h-[650px] flex flex-col shadow-lg border-slate-200">
      <CardHeader className="border-b bg-slate-50/50 py-4">
        <CardTitle className="text-lg flex items-center gap-2">
          <Bot className="w-5 h-5 text-blue-600" />
          AI Assistant
        </CardTitle>
      </CardHeader>
      
      <CardContent className="flex-1 p-0">
        <ScrollArea className="h-[500px] p-4">
          {messages.map((m, i) => (
            <div key={i} className={`flex mb-4 ${m.role === "user" ? "justify-end" : "justify-start"}`}>
              <div className={`flex gap-3 max-w-[85%] ${m.role === "user" ? "flex-row-reverse" : "flex-row"}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${m.role === "user" ? "bg-blue-600" : "bg-slate-200"}`}>
                  {m.role === "user" ? <User className="w-4 h-4 text-white" /> : <Bot className="w-4 h-4 text-slate-600" />}
                </div>
                <div className={`p-3 rounded-2xl text-sm ${m.role === "user" ? "bg-blue-600 text-white rounded-tr-none" : "bg-slate-100 text-slate-800 rounded-tl-none shadow-sm"}`}>
                  {m.content || <span className="animate-pulse">...</span>}
                </div>
              </div>
            </div>
          ))}
          <div ref={scrollRef} />
        </ScrollArea>
      </CardContent>

      <CardFooter className="p-4 border-t">
        <div className="flex w-full gap-2">
          <Input
            placeholder="Ask a question about the documents..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            className="focus-visible:ring-blue-500"
          />
          <Button onClick={handleSend} className="bg-blue-600 hover:bg-blue-700">
            <Send className="w-4 h-4" />
          </Button>
        </div>
      </CardFooter>
    </Card>
  );
}
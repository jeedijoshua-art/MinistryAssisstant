"use client";

import { useState, useRef, useEffect } from "react";
import { MessageList } from "@/components/chat/MessageList";
import { ChatInput } from "@/components/chat/ChatInput";
import { v4 as uuidv4 } from "uuid";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  tool_calls?: any[];
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  const handleSendMessage = async (content: string) => {
    const newMessage: Message = { id: uuidv4(), role: "user", content };
    setMessages((prev) => [...prev, newMessage]);
    setIsLoading(true);

    const aiMessageId = uuidv4();
    setMessages((prev) => [...prev, { id: aiMessageId, role: "assistant", content: "", tool_calls: [] }]);

    abortControllerRef.current = new AbortController();

    try {
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";
      const res = await fetch(`${API_BASE_URL}/api/v1/assistant/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: content,
          conversation_id: conversationId,
          stream: true
        }),
        signal: abortControllerRef.current.signal
      });

      if (!res.ok) throw new Error("Failed to connect to assistant stream.");
      if (!res.body) throw new Error("No response body.");

      const reader = res.body.getReader();
      const decoder = new TextDecoder("utf-8");
      
      let done = false;
      let streamedText = "";
      
      setIsLoading(false); // Text is arriving, stop pulse animation

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        if (value) {
          const chunk = decoder.decode(value, { stream: true });
          streamedText += chunk;
          
          setMessages((prev) => prev.map((msg) => {
            if (msg.id === aiMessageId) {
              return { ...msg, content: streamedText };
            }
            return msg;
          }));
        }
      }
    } catch (error: any) {
      if (error.name === "AbortError") {
        console.log("Stream aborted");
      } else {
        console.error(error);
        setMessages((prev) => prev.map((msg) => {
          if (msg.id === aiMessageId && msg.content === "") {
            return { ...msg, content: `**Error:** Failed to reach ZTP Assistant backend. Ensure the server is running on port 8000.` };
          }
          return msg;
        }));
      }
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  };

  const handleStop = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    setIsLoading(false);
  };

  return (
    <div className="flex flex-col h-full w-full absolute inset-0">
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto hide-scrollbar scroll-smooth"
      >
        <MessageList 
          messages={messages} 
          isLoading={isLoading} 
          onRegenerate={() => {}}
        />
      </div>
      
      <div className="w-full bg-gradient-to-t from-background via-background/95 to-transparent pt-6 pb-4">
        <ChatInput 
          onSendMessage={handleSendMessage} 
          isLoading={isLoading} 
          onStop={handleStop} 
        />
      </div>
    </div>
  );
}

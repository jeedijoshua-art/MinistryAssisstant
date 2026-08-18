"use client";

import { useState, useEffect, useRef, Suspense } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Image as ImageIcon, Mic, Send, Sparkles, Download, Share } from "lucide-react";
import { cn } from "@/lib/utils";
import { v4 as uuidv4 } from "uuid";
import { useSearchParams } from "next/navigation";
import Image from "next/image";

interface Message {
  id: string;
  role: "user" | "ai";
  content: string;
  action?: "poster" | "sermon" | "announcement" | null;
  generated_media_url?: string;
}

import { ChatAPI, CreativeStudioAPI } from "@/lib/api";

function AIChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [conversationId, setConversationId] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const searchParams = useSearchParams();
  const intent = searchParams.get("intent");
  const context = searchParams.get("context");

  useEffect(() => {
    // Create conversation on mount
    ChatAPI.createConversation({ title: "Chat Session" })
      .then((data) => setConversationId(data.id))
      .catch(console.error);
  }, []);

  useEffect(() => {
    if (intent && messages.length === 0) {
      if (intent === "poster") setInput("Generate a Facebook poster for John 3:16");
      if (intent === "sermon") setInput("Write a sermon about faith.");
      if (intent === "announcement") setInput("Prepare today's church announcement.");
      if (intent === "explain" && context) setInput(`Explain this Bible verse: ${context}`);
    }
  }, [intent, context, messages.length]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || !conversationId) return;

    const userMessage: Message = { id: uuidv4(), role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    const aiMessageId = uuidv4();
    setMessages((prev) => [...prev, { id: aiMessageId, role: "ai", content: "" }]);

    try {
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";
      const res = await fetch(`${API_BASE_URL}/api/v1/assistant/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ conversation_id: conversationId, message: userMessage.content }),
      });

      if (!res.body) return;
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let done = false;

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        if (value) {
          const chunk = decoder.decode(value);
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === aiMessageId ? { ...msg, content: msg.content + chunk } : msg
            )
          );
        }
      }
    } catch (err) {
      console.error(err);
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === aiMessageId ? { ...msg, content: "Error connecting to AI." } : msg
        )
      );
    }
  };

  return (
    <div className="flex h-[calc(100vh-9rem)] flex-col relative z-10">
      
      {/* Header */}
      <div className="px-4 pt-4 pb-2 flex justify-between items-center backdrop-blur-md sticky top-0 z-20 bg-background/50 border-b border-white/5">
        <h1 className="text-xl font-bold font-serif flex items-center">
          <Sparkles className="h-5 w-5 text-primary mr-2" />
          Assistant
        </h1>
      </div>

      <ScrollArea className="flex-1 px-4">
        <div className="flex flex-col space-y-6 py-6 pb-12">
          {messages.length === 0 && (
            <div className="text-center mt-20 space-y-4">
              <div className="mx-auto h-20 w-20 rounded-full bg-primary/20 flex items-center justify-center animate-pulse">
                <Sparkles className="h-10 w-10 text-primary" />
              </div>
              <h2 className="text-2xl font-serif font-bold text-white/90">How can I help your ministry today?</h2>
              <p className="text-sm text-muted-foreground max-w-xs mx-auto">
                Ask me to write a sermon, design a poster, or explain a Bible verse.
              </p>
            </div>
          )}
          
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={cn(
                "flex max-w-[90%] flex-col space-y-2 rounded-3xl px-5 py-4 text-sm shadow-sm backdrop-blur-md",
                msg.role === "user"
                  ? "self-end bg-primary/90 text-primary-foreground rounded-br-sm shadow-primary/20"
                  : "self-start bg-secondary/80 text-secondary-foreground rounded-bl-sm border border-border/30"
              )}
            >
              {(() => {
                let parsedMsg = null;
                if (msg.role === "ai" && msg.content) {
                  try {
                    parsedMsg = JSON.parse(msg.content);
                  } catch (e) {
                    // Not JSON, just normal text
                  }
                }
                
                if (parsedMsg && parsedMsg.type === "image") {
                  return (
                    <div className="mt-2 space-y-3">
                      <span className="text-xs font-semibold uppercase tracking-wider text-primary flex items-center gap-2"><ImageIcon className="w-4 h-4"/> Creative Studio Module</span>
                      <div className="w-full aspect-[4/5] relative rounded-xl overflow-hidden shadow-xl border border-white/10">
                        <Image src={parsedMsg.image_url} alt={parsedMsg.title || "Generated Poster"} fill className="object-cover" unoptimized />
                      </div>
                      <div className="flex items-center space-x-2">
                        <Button size="sm" className="flex-1 rounded-full bg-primary/20 text-primary hover:bg-primary/30">
                          <Download className="h-4 w-4 mr-2" /> Download
                        </Button>
                        <Button size="sm" variant="outline" className="flex-1 rounded-full bg-secondary/50 border-border/30">
                          <Share className="h-4 w-4 mr-2" /> Share
                        </Button>
                      </div>
                    </div>
                  );
                } else if (parsedMsg && parsedMsg.type === "error") {
                   return (
                     <div className="mt-2 space-y-3 p-4 bg-destructive/20 border border-destructive/50 rounded-xl">
                       <span className="text-xs font-semibold uppercase tracking-wider text-destructive flex items-center gap-2">Image Generation Failed</span>
                       <p className="text-sm text-destructive-foreground">{parsedMsg.error_message}</p>
                     </div>
                   );
                } else {
                  return (
                    <div className="whitespace-pre-wrap leading-relaxed">{msg.content || (msg.role === "ai" && <span className="animate-pulse">Thinking...</span>)}</div>
                  );
                }
              })()}

            </div>
          ))}
          <div ref={scrollRef} />
        </div>
      </ScrollArea>

      <div className="px-4 pb-4">
        <div className="flex items-center space-x-2 rounded-full border border-border/30 bg-secondary/70 backdrop-blur-xl px-2 py-2 pr-2 shadow-2xl focus-within:ring-2 focus-within:ring-primary/50 transition-all">
          <Button variant="ghost" size="icon" className="h-10 w-10 rounded-full text-muted-foreground shrink-0 hover:bg-secondary">
            <ImageIcon className="h-5 w-5" />
          </Button>
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Message Assistant..."
            className="border-0 bg-transparent px-2 shadow-none focus-visible:ring-0 focus-visible:ring-offset-0 text-base h-10 placeholder:text-muted-foreground/60"
          />
          {input.length > 0 ? (
            <Button size="icon" className="h-10 w-10 rounded-full shrink-0 bg-primary shadow-lg hover:scale-105 transition-transform" onClick={handleSend}>
              <Send className="h-4 w-4 ml-0.5 text-primary-foreground" />
            </Button>
          ) : (
            <Button variant="ghost" size="icon" className="h-10 w-10 rounded-full text-muted-foreground shrink-0 hover:bg-secondary">
              <Mic className="h-5 w-5" />
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}

export default function AIPage() {
  return (
    <Suspense fallback={<div className="p-4 text-center">Loading AI...</div>}>
      <AIChat />
    </Suspense>
  );
}

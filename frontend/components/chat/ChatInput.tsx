"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Send, StopCircle, Sparkles, Image as ImageIcon, BookOpen, Share2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
  onStop: () => void;
}

const QUICK_ACTIONS = [
  { label: "Explain Verse", icon: BookOpen, prompt: "Can you explain Genesis 1:1 to me?" },
  { label: "Prepare Sermon", icon: Sparkles, prompt: "Prepare a sermon on faith and trust in God." },
  { label: "Create Poster", icon: ImageIcon, prompt: "Generate a poster for this Sunday's youth meeting." },
  { label: "Write Announcement", icon: Share2, prompt: "Write a WhatsApp announcement for tomorrow's prayer service." },
];

export function ChatInput({ onSendMessage, isLoading, onStop }: ChatInputProps) {
  const [input, setInput] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [input]);

  const handleSend = () => {
    if (input.trim() && !isLoading) {
      onSendMessage(input.trim());
      setInput("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto flex flex-col space-y-3 p-4">
      {/* Quick Actions (only show if input is empty or just started typing) */}
      <div className="flex flex-wrap gap-2 justify-center">
        {QUICK_ACTIONS.map((action, i) => (
          <Button 
            key={i} 
            variant="outline" 
            size="sm"
            className="rounded-full bg-background/50 backdrop-blur-md border-border/50 text-xs text-muted-foreground hover:text-primary transition-colors"
            onClick={() => setInput(action.prompt)}
          >
            <action.icon className="w-3 h-3 mr-1.5" />
            {action.label}
          </Button>
        ))}
      </div>

      {/* Input Area */}
      <div className="relative flex items-end w-full rounded-3xl bg-secondary/30 backdrop-blur-xl border border-border/40 shadow-xl focus-within:ring-1 focus-within:ring-primary/50 transition-all p-2">
        <Textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Message ZTP Assistant..."
          className="min-h-[44px] max-h-[200px] w-full resize-none bg-transparent border-0 focus-visible:ring-0 p-3 py-3 shadow-none text-base md:text-sm"
          rows={1}
        />
        
        <div className="flex h-11 items-center px-2">
          {isLoading ? (
            <Button size="icon" variant="ghost" className="h-8 w-8 rounded-full text-muted-foreground hover:text-destructive transition-colors" onClick={onStop}>
              <StopCircle className="h-5 w-5" />
            </Button>
          ) : (
            <Button 
              size="icon" 
              className={cn(
                "h-8 w-8 rounded-full transition-all duration-300", 
                input.trim() ? "bg-primary text-primary-foreground hover:bg-primary/90" : "bg-muted text-muted-foreground cursor-not-allowed"
              )} 
              onClick={handleSend}
              disabled={!input.trim()}
            >
              <Send className="h-4 w-4 ml-0.5" />
            </Button>
          )}
        </div>
      </div>
      <div className="text-center text-[10px] text-muted-foreground/60 mt-2">
        ZTP Assistant can make mistakes. Verify important biblical doctrines.
      </div>
    </div>
  );
}

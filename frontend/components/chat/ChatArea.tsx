"use client";

import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { MessageBubble } from './MessageBubble';
import { useChatStream } from '../../hooks/useChatStream';

interface ChatAreaProps {
  conversationId: string | null;
  messages: { id: string; role: string; content: string }[];
  isStreaming: boolean;
  onSendMessage: (msg: string) => void;
}

export function ChatArea({ conversationId, messages, isStreaming, onSendMessage }: ChatAreaProps) {
  const [input, setInput] = useState('');
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isStreaming || !conversationId) return;
    
    onSendMessage(input.trim());
    setInput('');
  };

  if (!conversationId) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center bg-background/50 text-muted-foreground">
        <div className="text-center space-y-4">
          <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-2xl">🙏</span>
          </div>
          <h2 className="text-2xl font-semibold text-foreground">Welcome to ZTP Assistant</h2>
          <p className="max-w-md mx-auto">Select an existing conversation from the sidebar or create a new one to begin.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col h-screen bg-background relative overflow-hidden">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 md:p-8 scroll-smooth">
        <div className="max-w-3xl mx-auto flex flex-col pb-20">
          {messages.length === 0 ? (
            <div className="flex-1 flex items-center justify-center mt-32 text-muted-foreground">
              <p>Start a conversation...</p>
            </div>
          ) : (
            messages.map((msg, idx) => (
              <MessageBubble 
                key={msg.id} 
                role={msg.role} 
                content={msg.content} 
                isStreaming={isStreaming && idx === messages.length - 1 && msg.role === 'assistant'} 
              />
            ))
          )}
          <div ref={endOfMessagesRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-background via-background/90 to-transparent backdrop-blur-sm">
        <div className="max-w-3xl mx-auto relative">
          <form onSubmit={handleSubmit} className="relative flex items-end shadow-lg rounded-2xl bg-card border border-border overflow-hidden focus-within:ring-2 focus-within:ring-primary/50 transition-all">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
              placeholder="Message ZTP Assistant..."
              className="w-full max-h-48 p-4 pr-14 bg-transparent border-none resize-none focus:outline-none focus:ring-0 text-foreground text-sm"
              rows={1}
              style={{ minHeight: '56px' }}
            />
            <button
              type="submit"
              disabled={!input.trim() || isStreaming}
              className="absolute right-2 bottom-2 p-2 bg-primary text-primary-foreground rounded-xl disabled:opacity-50 disabled:cursor-not-allowed hover:bg-primary/90 transition-colors"
            >
              {isStreaming ? <Loader2 size={18} className="animate-spin" /> : <Send size={18} />}
            </button>
          </form>
          <div className="text-center mt-2">
            <span className="text-[10px] text-muted-foreground">ZTP Assistant may produce inaccurate information. Always refer to the Bible.</span>
          </div>
        </div>
      </div>
    </div>
  );
}

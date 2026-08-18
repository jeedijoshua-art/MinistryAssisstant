"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { cn } from "@/lib/utils";
import { Copy, RefreshCw, Sparkles, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ToolCardRenderer } from "./ToolCards";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  tool_calls?: any[];
}

interface MessageListProps {
  messages: Message[];
  isLoading: boolean;
  onRegenerate?: () => void;
}

export function MessageList({ messages, isLoading, onRegenerate }: MessageListProps) {
  
  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="flex flex-col space-y-6 pb-24 px-4 md:px-8 w-full max-w-4xl mx-auto pt-8">
      {messages.length === 0 && (
        <div className="flex flex-col items-center justify-center space-y-4 h-[50vh] text-center">
          <div className="h-16 w-16 bg-primary/10 rounded-full flex items-center justify-center mb-4">
            <Sparkles className="h-8 w-8 text-primary" />
          </div>
          <h2 className="text-2xl font-serif font-bold">How can I help your ministry today?</h2>
          <p className="text-muted-foreground max-w-md">
            I can explain verses, draft sermons, write prayers, create posters, and draft church communications.
          </p>
        </div>
      )}

      {messages.map((msg, idx) => {
        const isUser = msg.role === "user";
        
        return (
          <div key={msg.id || idx} className={cn("flex w-full", isUser ? "justify-end" : "justify-start")}>
            <div className="flex max-w-[85%] md:max-w-[80%] space-x-3">
              {!isUser && (
                <div className="flex-shrink-0 mt-1">
                  <div className="h-8 w-8 rounded-full bg-primary/20 border border-primary/30 flex items-center justify-center">
                    <Sparkles className="h-4 w-4 text-primary" />
                  </div>
                </div>
              )}
              
              <div className="flex flex-col space-y-2 w-full min-w-0">
                {/* Message Bubble */}
                <div 
                  className={cn(
                    "px-4 py-3 rounded-2xl w-full break-words shadow-sm",
                    isUser 
                      ? "bg-secondary text-secondary-foreground rounded-tr-sm" 
                      : "bg-background border border-border/40 rounded-tl-sm text-foreground"
                  )}
                >
                  <div className="prose prose-sm md:prose-base dark:prose-invert max-w-none prose-p:leading-relaxed prose-pre:bg-secondary/50 prose-pre:border prose-pre:border-border/40">
                    <ReactMarkdown 
                      remarkPlugins={[remarkGfm]}
                      components={{
                        p: ({children}) => <p className="last:mb-0 mb-3">{children}</p>,
                        a: ({node, ...props}) => <a className="text-primary hover:underline" {...props} />,
                        img: ({node, ...props}) => (
                          <a href={props.src} target="_blank" rel="noopener noreferrer" className="block my-4">
                            <img 
                              className="max-w-full h-auto rounded-lg shadow-md max-h-[500px] object-contain border border-border/40 hover:opacity-90 transition-opacity bg-black/5" 
                              {...props} 
                              alt={props.alt || "Generated Image"} 
                            />
                          </a>
                        ),
                        table: ({node, ...props}) => <div className="overflow-x-auto"><table className="w-full text-sm my-4 border-collapse" {...props} /></div>,
                        th: ({node, ...props}) => <th className="border border-border/50 bg-secondary/30 px-3 py-2 text-left font-semibold" {...props} />,
                        td: ({node, ...props}) => <td className="border border-border/50 px-3 py-2" {...props} />,
                      }}
                    >
                      {msg.content}
                    </ReactMarkdown>
                  </div>

                  {/* Render Tool Cards if applicable */}
                  {msg.tool_calls && msg.tool_calls.map((tool, i) => (
                    <ToolCardRenderer key={i} tool={tool} />
                  ))}
                </div>
                
                {/* Actions */}
                {!isUser && (
                  <div className="flex items-center space-x-2 text-muted-foreground/60 ml-2">
                    <Button variant="ghost" size="icon" className="h-6 w-6 hover:text-primary" onClick={() => handleCopy(msg.content)}>
                      <Copy className="h-3 w-3" />
                    </Button>
                    {idx === messages.length - 1 && onRegenerate && (
                      <Button variant="ghost" size="icon" className="h-6 w-6 hover:text-primary" onClick={onRegenerate}>
                        <RefreshCw className="h-3 w-3" />
                      </Button>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        );
      })}
      
      {isLoading && (
        <div className="flex w-full justify-start">
          <div className="flex max-w-[85%] space-x-3">
            <div className="flex-shrink-0 mt-1">
              <div className="h-8 w-8 rounded-full bg-primary/20 border border-primary/30 flex items-center justify-center">
                <Sparkles className="h-4 w-4 text-primary animate-pulse" />
              </div>
            </div>
            <div className="flex items-center px-4 py-3 bg-background border border-border/40 rounded-2xl rounded-tl-sm h-12 w-24">
              <div className="flex space-x-1.5 items-center justify-center w-full">
                <div className="w-2 h-2 bg-primary/50 rounded-full animate-bounce" style={{ animationDelay: "0ms" }}></div>
                <div className="w-2 h-2 bg-primary/50 rounded-full animate-bounce" style={{ animationDelay: "150ms" }}></div>
                <div className="w-2 h-2 bg-primary/50 rounded-full animate-bounce" style={{ animationDelay: "300ms" }}></div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

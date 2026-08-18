import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Copy, Bot, User } from 'lucide-react';
import { motion } from 'framer-motion';

interface MessageBubbleProps {
  role: string;
  content: string;
  isStreaming?: boolean;
}

export function MessageBubble({ role, content, isStreaming }: MessageBubbleProps) {
  const isAssistant = role === 'assistant';

  const copyToClipboard = () => {
    navigator.clipboard.writeText(content);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex w-full ${isAssistant ? 'justify-start' : 'justify-end'} mb-6`}
    >
      <div className={`flex max-w-[80%] ${isAssistant ? 'flex-row' : 'flex-row-reverse'} gap-4`}>
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${isAssistant ? 'bg-primary/20 text-primary' : 'bg-secondary text-secondary-foreground'}`}>
          {isAssistant ? <Bot size={18} /> : <User size={18} />}
        </div>
        
        <div className={`relative group px-5 py-4 rounded-2xl ${
          isAssistant 
            ? 'bg-card border border-border/50 text-card-foreground shadow-sm' 
            : 'bg-primary text-primary-foreground'
        }`}>
          <div className="prose prose-sm dark:prose-invert max-w-none break-words">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {content || (isStreaming ? '...' : '')}
            </ReactMarkdown>
          </div>
          
          {isAssistant && content && (
            <button
              onClick={copyToClipboard}
              className="absolute top-2 right-2 p-1.5 opacity-0 group-hover:opacity-100 transition-opacity rounded-md hover:bg-muted text-muted-foreground"
              title="Copy to clipboard"
            >
              <Copy size={14} />
            </button>
          )}
        </div>
      </div>
    </motion.div>
  );
}

import { useState } from 'react';

export function useChatStream() {
  const [messages, setMessages] = useState<{ id: string; role: string; content: string }[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = async (conversationId: string, messageContent: string) => {
    // Optimistically add user message
    const userMsg = { id: crypto.randomUUID(), role: 'user', content: messageContent };
    setMessages(prev => [...prev, userMsg]);
    
    // Add empty assistant message placeholder
    const assistantMsgId = crypto.randomUUID();
    setMessages(prev => [...prev, { id: assistantMsgId, role: 'assistant', content: '' }]);
    
    setIsStreaming(true);
    setError(null);

    try {
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";
      const response = await fetch(`${API_BASE_URL}/api/v1/assistant/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ conversation_id: conversationId, message: messageContent }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      if (!response.body) {
        throw new Error('ReadableStream not yet supported in this browser.');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        
        setMessages(prev => prev.map(msg => {
          if (msg.id === assistantMsgId) {
            return { ...msg, content: msg.content + chunk };
          }
          return msg;
        }));
      }
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message || 'An error occurred during chat.');
      } else {
        setError('An error occurred during chat.');
      }
    } finally {
      setIsStreaming(false);
    }
  };

  const loadMessages = (initialMessages: { id: string; role: string; content: string }[]) => {
    setMessages(initialMessages);
  };

  return { messages, sendMessage, isStreaming, error, loadMessages };
}

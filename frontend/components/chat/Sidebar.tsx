import React from 'react';
import { MessageSquare, Plus, Trash2, Edit2 } from 'lucide-react';

interface Conversation {
  id: string;
  title: string;
}

interface SidebarProps {
  conversations: Conversation[];
  activeId: string | null;
  onSelect: (id: string) => void;
  onNew: () => void;
  onDelete: (id: string) => void;
  onRename: (id: string, newTitle: string) => void;
}

export function Sidebar({ conversations, activeId, onSelect, onNew, onDelete, onRename }: SidebarProps) {
  return (
    <div className="w-64 bg-card border-r border-border h-screen flex flex-col">
      <div className="p-4">
        <button
          onClick={onNew}
          className="w-full flex items-center justify-center gap-2 bg-primary text-primary-foreground hover:bg-primary/90 py-2.5 rounded-lg transition-colors font-medium text-sm"
        >
          <Plus size={18} />
          New Chat
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto p-2 space-y-1">
        {conversations.length === 0 ? (
          <p className="text-muted-foreground text-sm text-center py-4">No conversations yet</p>
        ) : (
          conversations.map((conv) => (
            <div
              key={conv.id}
              className={`group flex items-center justify-between p-2 rounded-lg cursor-pointer transition-colors ${
                activeId === conv.id ? 'bg-accent text-accent-foreground' : 'hover:bg-accent/50 text-muted-foreground hover:text-foreground'
              }`}
              onClick={() => onSelect(conv.id)}
            >
              <div className="flex items-center gap-3 overflow-hidden">
                <MessageSquare size={16} className="flex-shrink-0" />
                <span className="text-sm truncate select-none">{conv.title}</span>
              </div>
              
              <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    const newTitle = prompt('New title:', conv.title);
                    if (newTitle) onRename(conv.id, newTitle);
                  }}
                  className="p-1 hover:bg-background rounded text-muted-foreground hover:text-foreground"
                >
                  <Edit2 size={14} />
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    if (confirm('Delete this conversation?')) onDelete(conv.id);
                  }}
                  className="p-1 hover:bg-destructive/10 rounded text-muted-foreground hover:text-destructive"
                >
                  <Trash2 size={14} />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

"use client";

import { 
  Plus, MessageSquare, BookOpen, ImageIcon, 
  Settings, User, FolderOpen, PanelLeftClose, 
  Search, Pin, MoreHorizontal
} from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Button, buttonVariants } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useState } from "react";

const WORKSPACE_LINKS = [
  { name: "Chat", href: "/", icon: MessageSquare },
  { name: "Projects", href: "/projects", icon: FolderOpen },
  { name: "Bible", href: "/bible", icon: BookOpen },
  { name: "Gallery", href: "/gallery", icon: ImageIcon },
];

const SETTINGS_LINKS = [
  { name: "Church Profile", href: "/profile", icon: User },
  { name: "Settings", href: "/settings", icon: Settings },
];

export function AppSidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div 
      className={cn(
        "hidden md:flex flex-col border-r border-border/40 bg-background/50 backdrop-blur-xl transition-all duration-300",
        collapsed ? "w-[80px]" : "w-[280px]"
      )}
    >
      {/* Header */}
      <div className="flex h-16 items-center justify-between px-4 border-b border-border/40">
        {!collapsed && <span className="font-serif font-bold text-lg text-primary">ZTP Assistant</span>}
        <Button variant="ghost" size="icon" onClick={() => setCollapsed(!collapsed)} className={cn(collapsed && "mx-auto")}>
          <PanelLeftClose className={cn("h-5 w-5 transition-transform", collapsed && "rotate-180")} />
        </Button>
      </div>

      {/* New Chat Button */}
      <div className="p-4">
        <Link 
          href="/" 
          className={cn(buttonVariants({ variant: "default" }), "w-full justify-start space-x-2 rounded-xl")}
        >
          <Plus className="h-5 w-5" />
          {!collapsed && <span>New Chat</span>}
        </Link>
      </div>

      <ScrollArea className="flex-1 px-3">
        {/* Workspace */}
        <div className="space-y-1 mb-6">
          {!collapsed && <div className="text-xs font-semibold text-muted-foreground mb-2 px-2 uppercase tracking-wider">Workspace</div>}
          {WORKSPACE_LINKS.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link key={link.name} href={link.href}>
                <div className={cn(
                  "flex items-center space-x-3 rounded-lg px-3 py-2 transition-all hover:bg-secondary/80",
                  isActive ? "bg-secondary text-primary font-medium" : "text-muted-foreground",
                  collapsed && "justify-center px-0"
                )}>
                  <link.icon className="h-4 w-4" />
                  {!collapsed && <span>{link.name}</span>}
                </div>
              </Link>
            );
          })}
        </div>

        {/* Recent Conversations Mock */}
        {!collapsed && (
          <div className="space-y-1 mb-6">
            <div className="flex items-center justify-between text-xs font-semibold text-muted-foreground mb-2 px-2 uppercase tracking-wider">
              <span>Recent</span>
              <Search className="h-3 w-3 cursor-pointer hover:text-primary" />
            </div>
            
            {/* Mock Item */}
            <div className="group flex items-center justify-between rounded-lg px-3 py-2 text-sm text-muted-foreground hover:bg-secondary/50 cursor-pointer">
              <div className="flex items-center space-x-2 truncate">
                <MessageSquare className="h-3 w-3 shrink-0" />
                <span className="truncate">Sermon on Grace</span>
              </div>
              <div className="opacity-0 group-hover:opacity-100 flex space-x-1">
                <MoreHorizontal className="h-3 w-3 hover:text-primary" />
              </div>
            </div>
            
            <div className="group flex items-center justify-between rounded-lg px-3 py-2 text-sm text-muted-foreground hover:bg-secondary/50 cursor-pointer">
              <div className="flex items-center space-x-2 truncate">
                <MessageSquare className="h-3 w-3 shrink-0" />
                <span className="truncate">Youth Meeting Poster</span>
              </div>
            </div>
          </div>
        )}
      </ScrollArea>

      {/* Settings */}
      <div className="p-3 border-t border-border/40 space-y-1">
        {SETTINGS_LINKS.map((link) => {
          const isActive = pathname === link.href;
          return (
            <Link key={link.name} href={link.href}>
              <div className={cn(
                "flex items-center space-x-3 rounded-lg px-3 py-2 transition-all hover:bg-secondary/80",
                isActive ? "bg-secondary text-primary font-medium" : "text-muted-foreground",
                collapsed && "justify-center px-0"
              )}>
                <link.icon className="h-4 w-4" />
                {!collapsed && <span>{link.name}</span>}
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
}

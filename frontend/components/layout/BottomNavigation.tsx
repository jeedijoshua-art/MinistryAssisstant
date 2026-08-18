"use client";

import { Home, BookOpen, MessageSquare, Image as ImageIcon, User } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { name: "Home", href: "/", icon: Home },
  { name: "Bible", href: "/bible", icon: BookOpen },
  { name: "AI", href: "/ai", icon: MessageSquare },
  { name: "Gallery", href: "/gallery", icon: ImageIcon },
  { name: "Profile", href: "/profile", icon: User },
];

export function BottomNavigation() {
  const pathname = usePathname();

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 flex h-20 items-center justify-between border-t border-border/40 bg-background/80 px-6 pb-safe backdrop-blur-lg">
      {NAV_ITEMS.map((item) => {
        const isActive = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));
        
        return (
          <Link
            key={item.name}
            href={item.href}
            className="flex flex-col items-center justify-center space-y-1 p-2"
          >
            <div
              className={cn(
                "flex h-10 w-10 items-center justify-center rounded-full transition-all duration-300",
                isActive ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:bg-secondary"
              )}
            >
              <item.icon className="h-5 w-5" />
            </div>
            <span
              className={cn(
                "text-[10px] font-medium transition-colors",
                isActive ? "text-primary" : "text-muted-foreground"
              )}
            >
              {item.name}
            </span>
          </Link>
        );
      })}
    </div>
  );
}

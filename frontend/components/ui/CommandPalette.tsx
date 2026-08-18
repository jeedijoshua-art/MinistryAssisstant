"use client";

import { useEffect, useState } from "react";
import { CommandDialog, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList, CommandShortcut } from "@/components/ui/command";
import { BookOpen, Sparkles, MessageSquare, ImageIcon, LayoutTemplate } from "lucide-react";
import { useRouter } from "next/navigation";

export function CommandPalette() {
  const [open, setOpen] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };
    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, []);

  const runCommand = (command: () => void) => {
    setOpen(false);
    command();
  };

  return (
    <CommandDialog open={open} onOpenChange={setOpen}>
      <CommandInput placeholder="Type a command or search..." />
      <CommandList>
        <CommandEmpty>No results found.</CommandEmpty>
        <CommandGroup heading="Suggestions">
          <CommandItem onSelect={() => runCommand(() => router.push("/bible"))}>
            <BookOpen className="mr-2 h-4 w-4" />
            <span>Read Bible</span>
            <CommandShortcut>⌘B</CommandShortcut>
          </CommandItem>
          <CommandItem onSelect={() => runCommand(() => router.push("/ai"))}>
            <Sparkles className="mr-2 h-4 w-4 text-primary" />
            <span>Ask AI Assistant</span>
          </CommandItem>
        </CommandGroup>
        <CommandGroup heading="Workspace">
          <CommandItem onSelect={() => runCommand(() => router.push("/sermons"))}>
            <MessageSquare className="mr-2 h-4 w-4" />
            <span>New Sermon</span>
            <CommandShortcut>⌘N</CommandShortcut>
          </CommandItem>
          <CommandItem onSelect={() => runCommand(() => router.push("/creative"))}>
            <LayoutTemplate className="mr-2 h-4 w-4" />
            <span>Creative Studio</span>
          </CommandItem>
          <CommandItem onSelect={() => runCommand(() => router.push("/media"))}>
            <ImageIcon className="mr-2 h-4 w-4" />
            <span>Media Gallery</span>
          </CommandItem>
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  );
}

"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ChevronDown, Search, Sparkles, Bookmark, Settings2 } from "lucide-react";
import { useQuery } from "@tanstack/react-query";

interface BibleVerse {
  id: string;
  book_id: string;
  chapter_number: number;
  verse_number: number;
  text: string;
}

import { useRouter } from "next/navigation";
import { BibleAPI } from "@/lib/api";

export default function BiblePage() {
  const [selectedVerse, setSelectedVerse] = useState<number | null>(null);
  const [reference, setReference] = useState("Genesis 1");
  const router = useRouter();

  const { data: verses, isLoading } = useQuery({
    queryKey: ["bible", reference],
    queryFn: async () => {
      return (await BibleAPI.getVerse(reference, "KJV")) as BibleVerse[];
    }
  });

  const handleExplain = () => {
    if (selectedVerse) {
      const fullReference = `${reference}:${selectedVerse}`;
      router.push(`/ai?intent=explain&context=${encodeURIComponent(fullReference)}`);
    }
  };

  return (
    <div className="flex h-[calc(100vh-9rem)] flex-col">
      {/* Top Controls */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-border/40">
        <Button variant="ghost" className="font-semibold text-lg hover:bg-secondary/50 rounded-xl px-3 py-1 h-auto">
          {reference} <ChevronDown className="ml-2 h-4 w-4 text-muted-foreground" />
        </Button>
        <div className="flex items-center space-x-1">
          <Button variant="ghost" size="icon" className="h-8 w-8 rounded-full">
            <Search className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="icon" className="h-8 w-8 rounded-full">
            <Settings2 className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Reading Area */}
      <ScrollArea className="flex-1 px-6 py-6 pb-20">
        <div className="max-w-2xl mx-auto space-y-4">
          <h1 className="text-3xl font-serif font-bold mb-6">{reference}</h1>
          
          <div className="text-lg leading-loose space-y-2 font-serif">
            {isLoading ? (
              <p className="text-muted-foreground text-sm">Loading verses...</p>
            ) : verses?.length ? (
              verses.map((verse) => (
                <span 
                  key={verse.id}
                  onClick={() => setSelectedVerse(selectedVerse === verse.verse_number ? null : verse.verse_number)}
                  className={`transition-colors cursor-pointer rounded px-1 ${selectedVerse === verse.verse_number ? 'bg-primary/20' : 'hover:bg-secondary/40'}`}
                >
                  <sup className="text-xs font-sans text-muted-foreground mr-1 font-bold">{verse.verse_number}</sup>
                  {verse.text}{" "}
                </span>
              ))
            ) : (
              <p className="text-muted-foreground text-sm">No verses found.</p>
            )}
          </div>
        </div>
      </ScrollArea>

      {/* Selected Verse Context Menu */}
      {selectedVerse && (
        <div className="absolute bottom-20 left-4 right-4 bg-popover border border-border shadow-xl rounded-2xl p-2 animate-in slide-in-from-bottom-2">
          <div className="flex justify-around items-center">
            <Button variant="ghost" className="flex flex-col items-center h-auto py-2 px-4 gap-1 text-xs" onClick={handleExplain}>
              <Sparkles className="h-5 w-5 text-primary" />
              Explain
            </Button>
            <div className="w-px h-8 bg-border/50"></div>
            <Button variant="ghost" className="flex flex-col items-center h-auto py-2 px-4 gap-1 text-xs">
              <Bookmark className="h-5 w-5" />
              Save
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}

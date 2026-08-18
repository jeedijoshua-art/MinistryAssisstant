"use client";

import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { BookOpen, ImageIcon, Edit3, Heart } from "lucide-react";
import { Button } from "@/components/ui/button";

export function ToolCardRenderer({ tool }: { tool: any }) {
  if (!tool) return null;

  const { tool_name, tool_args } = tool;
  
  if (tool_name === "sermon_tool") {
    return (
      <Card className="mt-4 border-primary/20 bg-primary/5">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-semibold flex items-center text-primary">
            <BookOpen className="w-4 h-4 mr-2" /> Sermon Generated
          </CardTitle>
        </CardHeader>
        <CardContent className="text-sm">
          A new sermon has been drafted and saved to your projects. You can view the full text above.
        </CardContent>
      </Card>
    );
  }
  
  if (tool_name === "prayer_tool" || tool_name === "devotional_tool") {
    return (
      <Card className="mt-4 border-green-500/20 bg-green-500/5">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-semibold flex items-center text-green-500">
            <Heart className="w-4 h-4 mr-2" /> Content Generated
          </CardTitle>
        </CardHeader>
      </Card>
    );
  }

  if (tool_name === "creative_studio_tool") {
    return (
      <Card className="mt-4 border-orange-500/20 bg-orange-500/5">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-semibold flex items-center text-orange-500">
            <ImageIcon className="w-4 h-4 mr-2" /> Poster Draft Generated
          </CardTitle>
        </CardHeader>
        <CardContent className="text-sm space-y-2">
          <div className="bg-background/80 p-3 rounded-lg border border-border/40 font-mono text-xs text-muted-foreground">
            {tool_args?.sermon_id ? "Linked to active Sermon context." : "Ready for image generation."}
          </div>
        </CardContent>
        <CardFooter>
          <Button variant="outline" size="sm" className="w-full">Open in Gallery</Button>
        </CardFooter>
      </Card>
    );
  }
  
  if (tool_name === "ministry_writing_tool") {
    return (
      <Card className="mt-4 border-blue-500/20 bg-blue-500/5">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-semibold flex items-center text-blue-500">
            <Edit3 className="w-4 h-4 mr-2" /> Communication Drafted
          </CardTitle>
        </CardHeader>
      </Card>
    );
  }

  return null;
}

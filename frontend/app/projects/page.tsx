"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BookOpen, FileText, Search, Sparkles } from "lucide-react";
import { Input } from "@/components/ui/input";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { formatDistanceToNow } from "date-fns";

const fetchProjects = async () => {
  const { data } = await axios.get("http://127.0.0.1:8000/api/v1/projects/");
  return data;
};

export default function ProjectsPage() {
  const { data: projects, isLoading } = useQuery({
    queryKey: ["projects"],
    queryFn: fetchProjects
  });

  const getIcon = (type: string) => {
    switch (type) {
      case "Sermon": return BookOpen;
      case "Prayer": return Sparkles;
      case "Devotional": return FileText;
      default: return FileText;
    }
  };

  return (
    <div className="flex flex-col space-y-6 px-4 md:px-8 max-w-6xl mx-auto pt-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold font-serif">Projects</h1>
          <p className="text-sm text-muted-foreground mt-1">Manage your sermons, prayers, and devotionals.</p>
        </div>
      </div>

      <div className="relative max-w-md">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input className="pl-9 bg-secondary/50 border-border/40 rounded-full" placeholder="Search projects..." />
      </div>

      {isLoading ? (
        <div className="text-muted-foreground">Loading projects...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {projects?.map((item: any, idx: number) => {
            const Icon = getIcon(item.type);
            return (
              <Card key={idx} className="bg-secondary/20 hover:bg-secondary/40 transition-colors border-border/40 cursor-pointer">
                <CardHeader className="pb-2">
                  <div className="flex items-center space-x-2">
                    <div className="p-2 bg-primary/10 rounded-lg text-primary">
                      <Icon className="w-4 h-4" />
                    </div>
                    <CardTitle className="text-sm font-semibold truncate">{item.title}</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex justify-between items-center text-xs text-muted-foreground mt-4">
                    <span>{item.type}</span>
                    <span>{formatDistanceToNow(new Date(item.date))} ago</span>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}

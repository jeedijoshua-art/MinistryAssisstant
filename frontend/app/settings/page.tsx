"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

export default function SettingsPage() {
  return (
    <div className="flex flex-col space-y-6 px-4 md:px-8 max-w-3xl mx-auto pt-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold font-serif">Settings</h1>
          <p className="text-sm text-muted-foreground mt-1">Manage workspace preferences.</p>
        </div>
      </div>

      <Card className="bg-secondary/20 border-border/40 rounded-2xl">
        <CardHeader>
          <CardTitle className="text-lg">Appearance</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between p-3 bg-background rounded-xl border border-border/40">
            <div className="space-y-0.5">
              <Label>Dark Mode</Label>
              <p className="text-xs text-muted-foreground">The workspace is optimized for dark mode.</p>
            </div>
            <Button variant="outline" size="sm" disabled>Enabled</Button>
          </div>
        </CardContent>
      </Card>

      <Card className="bg-secondary/20 border-border/40 rounded-2xl">
        <CardHeader>
          <CardTitle className="text-lg">AI Preferences</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between p-3 bg-background rounded-xl border border-border/40">
            <div className="space-y-0.5">
              <Label>Bible Translation</Label>
              <p className="text-xs text-muted-foreground">Default translation used by the AI.</p>
            </div>
            <select className="bg-secondary border-border/40 rounded-md p-1.5 text-sm">
              <option>KJV</option>
              <option>NIV</option>
              <option>ESV</option>
            </select>
          </div>
          
          <div className="flex items-center justify-between p-3 bg-background rounded-xl border border-border/40">
            <div className="space-y-0.5">
              <Label>AI Model</Label>
              <p className="text-xs text-muted-foreground">Model used for Generation.</p>
            </div>
            <select className="bg-secondary border-border/40 rounded-md p-1.5 text-sm">
              <option>Gemini 1.5 Pro</option>
              <option>Gemini 1.5 Flash</option>
            </select>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

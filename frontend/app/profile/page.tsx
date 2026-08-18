"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";

export default function ProfilePage() {
  return (
    <div className="flex flex-col space-y-6 px-4 md:px-8 max-w-3xl mx-auto pt-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold font-serif">Church Profile</h1>
          <p className="text-sm text-muted-foreground mt-1">Configure your church identity for AI context.</p>
        </div>
      </div>

      <Card className="bg-secondary/20 border-border/40 rounded-2xl">
        <CardHeader>
          <CardTitle className="text-lg">General Details</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>Church Name</Label>
            <Input defaultValue="Grace Community Church" className="bg-background" />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Lead Pastor</Label>
              <Input defaultValue="John Doe" className="bg-background" />
            </div>
            <div className="space-y-2">
              <Label>Website</Label>
              <Input defaultValue="https://gracecommunity.org" className="bg-background" />
            </div>
          </div>
          <div className="space-y-2">
            <Label>Church Address</Label>
            <Input defaultValue="123 Faith Avenue, New York, NY" className="bg-background" />
          </div>
          
          <div className="pt-4 flex justify-end">
            <Button>Save Profile</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "@/components/providers";
import { BottomNavigation } from "@/components/layout/BottomNavigation";
import { PremiumBackground } from "@/components/ui/PremiumBackground";
import { CommandPalette } from "@/components/ui/CommandPalette";
import { cn } from "@/lib/utils";

const inter = Inter({ subsets: ["latin"], display: "swap", fallback: ["system-ui", "arial"] });

export const metadata: Metadata = {
  title: "ZTP Assistant",
  description: "Premium AI-powered Ministry Workspace",
  appleWebApp: {
    capable: true,
    statusBarStyle: "black-translucent",
    title: "ZTP Assistant",
  },
};

export const viewport: Viewport = {
  themeColor: "#0a0f18",
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  viewportFit: "cover",
};

import { AppSidebar } from "@/components/layout/AppSidebar";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning>
      <body className={cn(inter.className, "min-h-[100dvh] antialiased bg-transparent overflow-hidden")}>
        <Providers>
          <PremiumBackground />
          <CommandPalette />
          <div className="flex h-[100dvh] w-full">
            <AppSidebar />
            <div className="flex-1 flex flex-col min-w-0">
              <main className="flex-1 overflow-y-auto hide-scrollbar relative">
                {children}
              </main>
              <div className="md:hidden">
                <BottomNavigation />
              </div>
            </div>
          </div>
        </Providers>
      </body>
    </html>
  );
}

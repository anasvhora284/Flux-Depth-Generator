import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Providers from "./providers";
import logo from "../public/logo.png"

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Flux Depth Generator - AI Depth Map & Flux Theme Tool",
  description: "Generate high-quality depth maps with Flux Depth Generator. The ultimate tool for depth generation, depth additions, and flux themes. Transform 2D images into 3D masterpieces instantly using advanced AI models.",
  keywords: ["flux", "flux theme", "depth", "depth generation", "depth additions", "ai depth", "depth map", "3d image", "depth anything v2", "flux wallpaper"],
  openGraph: {
    title: "Flux Depth Generator - AI Depth Map & Flux Theme Tool",
    description: "Generate high-quality depth maps with Flux Depth Generator.",
    type: "website",
  }
};

import StarBackground from "@/components/3d/StarBackground";

import { CustomCursor } from "@/components/ui/custom-cursor";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning>
      <head>
        <link rel="icon" href={logo.src} />
      </head>
      <body className={`${inter.className} bg-background text-foreground min-h-screen antialiased selection:bg-blue-500/30 font-sans cursor-none`} suppressHydrationWarning>
        <CustomCursor />
        <StarBackground />
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}

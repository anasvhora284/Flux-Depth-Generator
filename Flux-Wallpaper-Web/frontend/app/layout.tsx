import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Providers from "./providers";
import logo from "../public/logo.png"

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Flux Depth Generator",
  description: "Transform 2D images into 3D Depth Maps instantly.",
};

import StarBackground from "@/components/3d/StarBackground";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="icon" href={logo.src} />
      </head>
      <body className={`${inter.className} bg-background text-foreground min-h-screen antialiased selection:bg-blue-500/30`}>
        <StarBackground />
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}

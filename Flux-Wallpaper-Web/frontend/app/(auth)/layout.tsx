"use client";

import StarBackground from "@/components/3d/StarBackground";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";

export default function AuthLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="min-h-screen grid lg:grid-cols-2">
            {/* Visual Side - Hidden on mobile */}
            <div className="relative hidden lg:flex flex-col justify-between p-12 bg-black overflow-hidden">
                <div className="absolute inset-0 z-0">
                    <StarBackground />
                </div>

                {/* Overlay Gradient */}
                <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-black/40 z-10" />
                <div className="absolute inset-0 bg-blue-600/10 mix-blend-overlay z-10" />

                {/* Content */}
                <div className="relative z-20">
                    <Link href="/" className="flex items-center gap-3 mb-8 hover:opacity-80 transition-opacity">
                        <img src="/logo.png" alt="Flux Depth" className="h-10 w-10 rounded-xl" />
                        <span className="font-heading font-bold text-2xl tracking-tight text-white">Flux Depth</span>
                    </Link>
                </div>

                <div className="relative z-20 max-w-lg">
                    <h1 className="font-heading text-4xl font-bold text-white mb-6 leading-tight">
                        Transform Flat Images into <br />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">Immersive 3D Reality</span>
                    </h1>
                    <p className="text-lg text-gray-300 mb-8 leading-relaxed">
                        Join thousands of creators using Flux Depth to generate stunning depth maps, 3D photos, and spatial assets.
                        Completely Free & Open Source.
                    </p>

                    <div className="flex gap-4">
                        <div className="p-4 rounded-xl bg-white/5 backdrop-blur-md border border-white/10 flex-1">
                            <div className="text-2xl font-bold text-white mb-1">100%</div>
                            <div className="text-sm text-gray-400">Free to Use</div>
                        </div>
                        <div className="p-4 rounded-xl bg-white/5 backdrop-blur-md border border-white/10 flex-1">
                            <div className="text-2xl font-bold text-white mb-1">Open</div>
                            <div className="text-sm text-gray-400">Source Code</div>
                        </div>
                    </div>
                </div>

                <div className="relative z-20 text-sm text-gray-500">
                    © 2024 Flux Depth. Made with ❤️ by Anas.
                </div>
            </div>

            {/* Form Side */}
            <div className="relative flex flex-col min-h-screen bg-background">
                {/* Mobile Header */}
                <div className="flex items-center justify-between p-4 lg:hidden border-b border-white/10">
                    <Link href="/" className="flex items-center gap-2">
                        <img src="/logo.png" alt="Flux Depth" className="h-8 w-8 rounded-lg" />
                        <span className="font-heading font-bold text-lg">Flux Depth</span>
                    </Link>
                    <Link href="/">
                        <Button variant="ghost" size="sm" className="gap-1 text-muted-foreground">
                            <ArrowLeft className="h-4 w-4" />
                            Home
                        </Button>
                    </Link>
                </div>

                {/* Desktop Back Button */}
                <Link href="/" className="hidden lg:block absolute top-8 right-8">
                    <Button
                        className="cursor-pointer bg-transparent hover:bg-black/5 text-slate-600 hover:text-black border border-transparent hover:border-black/10 transition-all font-medium"
                    >
                        Back to Home
                    </Button>
                </Link>

                {/* Form Content */}
                <div className="flex-1 flex items-center justify-center p-6 sm:p-8">
                    <div className="w-full max-w-md">
                        {children}
                    </div>
                </div>

                {/* Mobile Footer */}
                <div className="lg:hidden p-4 text-center text-sm text-muted-foreground border-t border-white/10">
                    © 2024 Flux Depth. Made with ❤️ by Anas.
                </div>
            </div>
        </div>
    );
}

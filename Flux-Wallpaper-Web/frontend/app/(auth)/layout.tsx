"use client";

import StarBackground from "@/components/3d/StarBackground";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";
import { motion } from "framer-motion";

export default function AuthLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="min-h-screen grid lg:grid-cols-2 overflow-hidden">
            {/* Visual Side - Hidden on mobile */}
            <div className="relative hidden lg:flex flex-col justify-between p-12 bg-black">
                <div className="absolute inset-0 z-0">
                    <StarBackground />
                </div>

                {/* Animated Orbs */}
                <motion.div
                    animate={{ 
                        y: [0, -20, 0],
                    }}
                    whileHover={{ scale: 1.1 }}
                    transition={{ 
                        y: {
                            duration: 5, 
                            repeat: Infinity, 
                            ease: "easeInOut" 
                        },
                        scale: { duration: 0.4, ease: "easeOut" }
                    }}
                    className="absolute -top-40 -left-40 w-[600px] h-[600px] bg-[radial-gradient(circle_at_30%_30%,_rgba(165,243,252,0.9),_rgba(6,182,212,0.9),_rgba(14,116,144,0.9))] rounded-full z-[5]"
                />
                
                <motion.div
                    animate={{ 
                        y: [0, 30, 0],
                    }}
                    whileHover={{ scale: 1.1 }}
                    transition={{ 
                        y: {
                            duration: 7, 
                            repeat: Infinity, 
                            ease: "easeInOut" 
                        },
                        scale: { duration: 0.4, ease: "easeOut" }
                    }}
                    className="absolute -bottom-32 -right-32 w-[600px] h-[600px] bg-[radial-gradient(circle_at_30%_30%,_rgba(245,208,254,0.9),_rgba(217,70,239,0.9),_rgba(134,25,143,0.9))] rounded-full z-[5]"
                />

                {/* Small floating breathing particles */}
                <motion.div
                    animate={{ y: [0, -40, 0] }}
                    transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
                    className="absolute top-1/4 right-1/4 w-4 h-4 bg-[radial-gradient(circle_at_30%_30%,_#fff,_#22d3ee)] rounded-full z-[5]"
                />
                <motion.div
                    animate={{ y: [0, 30, 0] }}
                    transition={{ duration: 7, repeat: Infinity, ease: "easeInOut", delay: 2 }}
                    className="absolute bottom-1/3 left-1/3 w-6 h-6 bg-[radial-gradient(circle_at_30%_30%,_#fff,_#e879f9)] rounded-full z-[5]"
                />

                {/* Overlay Gradient & Glass Effect */}
                <div className="absolute inset-0 bg-black/10 backdrop-blur-[30px] z-10 pointer-events-none" />
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent z-10 pointer-events-none" />
                <div className="absolute inset-0 bg-blue-600/5 mix-blend-overlay z-10 pointer-events-none" />

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
                    <p className="flex items-center gap-1">
                        © 2024 Flux Depth. Made with <span className="animate-pulse text-transparent bg-clip-text bg-gradient-to-r from-red-500 via-pink-500 to-purple-500">❤️</span> by 
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-600 font-bold hover:drop-shadow-[0_0_10px_rgba(59,130,246,0.5)] transition-all cursor-default"> Anas</span>.
                    </p>
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
                <Link href="/" className="hidden lg:block absolute top-8 right-8 z-20">
                    <Button
                        variant="ghost"
                        className="cursor-pointer text-muted-foreground hover:text-white hover:bg-white/10 transition-all font-medium"
                    >
                        Back to Home
                    </Button>
                </Link>

                {/* Background Blobs */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-blue-500/10 blur-[100px] rounded-full pointer-events-none z-0" />
                <div className="absolute top-1/4 right-1/4 w-[300px] h-[300px] bg-purple-500/10 blur-[80px] rounded-full pointer-events-none z-0" />

                {/* Form Content */}
                <div className="flex-1 flex items-center justify-center p-6 sm:p-8 relative z-10">
                    <div className="w-full max-w-md">
                        {children}
                    </div>
                </div>

                {/* Mobile Footer */}
                <div className="lg:hidden p-4 text-center text-sm text-muted-foreground border-t border-white/10">
                    <p className="flex flex-wrap items-center justify-center gap-1">
                        Made with <span className="animate-pulse text-transparent bg-clip-text bg-gradient-to-r from-red-500 via-pink-500 to-purple-500">❤️</span> by 
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-600 font-bold hover:drop-shadow-[0_0_10px_rgba(59,130,246,0.5)] transition-all cursor-default"> Anas</span>.
                    </p>
                </div>
            </div>
        </div>
    );
}

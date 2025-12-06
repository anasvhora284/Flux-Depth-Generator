"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { CompareSlider } from "@/components/ui/compare-slider";
import Link from "next/link";
import { ArrowRight, Play } from "lucide-react";

export function HeroSection() {
    return (
        <section className="relative pt-40 pb-20 overflow-hidden">
            {/* Background Glows */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[500px] bg-blue-500/20 blur-[120px] rounded-full z-[-1]" />

            <div className="container px-4 mx-auto flex flex-col items-center text-center">
                {/* Badge */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                    className="mb-6 inline-flex items-center rounded-full border border-white/10 bg-white/5 px-3 py-1 text-sm font-medium text-blue-300 backdrop-blur-xl"
                >
                    <span className="flex h-2 w-2 rounded-full bg-blue-400 mr-2 animate-pulse"></span>
                    v2.0 Now Available with Batch Processing
                </motion.div>

                {/* Headline */}
                <motion.h1
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.1 }}
                    className="font-heading text-5xl md:text-7xl lg:text-8xl font-bold tracking-tight text-white mb-6 max-w-5xl"
                >
                    Turn Flat Images into <br className="hidden md:block" />
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500">Immersive 3D Reality</span>
                </motion.h1>

                {/* Subline */}
                <motion.p
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                    className="text-lg md:text-xl text-muted-foreground max-w-2xl mb-10 leading-relaxed"
                >
                    The world's most advanced AI depth map generator. Create cinematic 3D photos, parallax wallpapers, and spatial assets in seconds.
                </motion.p>

                {/* CTAs */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.3 }}
                    className="flex flex-col sm:flex-row gap-4 w-full justify-center"
                >
                    <Link href="/dashboard">
                        <Button size="lg" variant="premium" className="h-14 px-8 text-lg w-full sm:w-auto hover:scale-105 active:scale-95 transition-transform">
                            Start Creating Free <ArrowRight className="ml-2 h-5 w-5" />
                        </Button>
                    </Link>
                </motion.div>

                {/* Visual Mockup Layer */}
                <motion.div
                    initial={{ opacity: 0, y: 40, rotateX: 20 }}
                    animate={{ opacity: 1, y: 0, rotateX: 0 }}
                    transition={{ duration: 0.8, delay: 0.4, type: "spring" }}
                    className="mt-20 relative w-full max-w-5xl aspect-video mx-auto perspective-1000"
                >
                    <div className="relative w-full h-full rounded-2xl border border-white/10 bg-black/50 backdrop-blur-sm shadow-2xl overflow-hidden glass-card group">
                        <CompareSlider
                            original="/hero-original.png"
                            modified="/hero-depth.png"
                            originalAlt="Original Anime Hero"
                            modifiedAlt="Generated Depth Map"
                        />

                        {/* Floating Elements (Parallax feel) - Keeping these for extra layer depth */}
                        <motion.div
                            animate={{ y: [0, -10, 0] }}
                            transition={{ repeat: Infinity, duration: 4, ease: "easeInOut" }}
                            className="absolute top-1/4 left-10 p-4 rounded-xl glass border border-white/10 shadow-xl z-10 hidden md:block pointer-events-none"
                        >
                            <div className="flex items-center gap-3">
                                <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-green-400 to-emerald-600" />
                                <div>
                                    <div className="h-2 w-20 bg-white/20 rounded mb-2" />
                                    <div className="h-2 w-12 bg-white/10 rounded" />
                                </div>
                            </div>
                        </motion.div>

                        <motion.div
                            animate={{ y: [0, 15, 0] }}
                            transition={{ repeat: Infinity, duration: 5, ease: "easeInOut", delay: 1 }}
                            className="absolute bottom-1/4 right-10 p-4 rounded-xl glass border border-white/10 shadow-xl z-10 hidden md:block pointer-events-none"
                        >
                            <div className="flex items-center gap-3">
                                <div className="text-sm font-bold text-white">Depth Confidence</div>
                                <div className="text-green-400 font-mono">98.5%</div>
                            </div>
                        </motion.div>
                    </div>

                    {/* Glow under the card */}
                    <div className="absolute -inset-4 bg-gradient-to-r from-blue-500 to-purple-500 opacity-20 blur-3xl -z-10 rounded-[3rem]" />
                </motion.div>
            </div>
        </section>
    );
}

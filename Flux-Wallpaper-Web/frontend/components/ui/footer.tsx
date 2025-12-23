import Link from "next/link";
import { Layers, Send, Github, Linkedin } from "lucide-react";

export function Footer() {
    return (
        <footer className="border-t border-white/5 bg-black/40 backdrop-blur-xl">
            <div className="container mx-auto px-4 py-12">
                <div className="flex flex-col md:flex-row justify-between items-center gap-8 text-center md:text-left">
                    <div className="space-y-4">
                        <div className="flex items-center justify-center md:justify-start gap-2">
                            <img src="/logo.png" alt="Flux Depth Logo" className="h-6 w-6 rounded-md" />
                            <span className="font-bold text-xl font-heading">Flux Depth</span>
                        </div>
                        <p className="text-muted-foreground text-sm leading-relaxed max-w-xs mx-auto md:mx-0">
                            Open Source AI Depth Generation for everyone.
                        </p>
                    </div>

                    <div className="flex gap-6">
                        <Link href="https://github.com/anasvhora284" target="_blank" className="text-muted-foreground hover:text-white transition-colors flex items-center gap-2 group">
                            <Github className="h-5 w-5 group-hover:text-white transition-colors" />
                            <span className="hidden sm:inline">GitHub</span>
                        </Link>
                        <Link href="https://t.me/Anasvhora" target="_blank" className="text-muted-foreground hover:text-[#0088cc] transition-colors flex items-center gap-2 group">
                            <Send className="h-5 w-5 group-hover:text-[#0088cc] transition-colors" />
                            <span className="hidden sm:inline">Telegram</span>
                        </Link>
                        <Link href="https://in.linkedin.com/in/anas-vhora-28455a1a1" target="_blank" className="text-muted-foreground hover:text-[#0077b5] transition-colors flex items-center gap-2 group">
                            <Linkedin className="h-5 w-5 group-hover:text-[#0077b5] transition-colors" />
                            <span className="hidden sm:inline">LinkedIn</span>
                        </Link>
                    </div>
                </div>

                    <p className="flex flex-wrap items-center justify-center gap-1">
                        Made with <span className="animate-pulse text-transparent bg-clip-text bg-gradient-to-r from-red-500 via-pink-500 to-purple-500">❤️</span> by 
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-600 font-bold hover:drop-shadow-[0_0_10px_rgba(59,130,246,0.5)] transition-all cursor-default"> Anas</span>. 
                        100% Free & Open Source.
                    </p>
            </div>
        </footer>
    );
}


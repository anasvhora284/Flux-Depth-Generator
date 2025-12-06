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
                        <Link href="https://github.com/anasvhora284" target="_blank" className="text-muted-foreground hover:text-white transition-colors flex items-center gap-2">
                            <Github className="h-5 w-5" />
                            <span className="hidden sm:inline">GitHub</span>
                        </Link>
                        <Link href="https://t.me/Anasvhora" target="_blank" className="text-muted-foreground hover:text-blue-400 transition-colors flex items-center gap-2">
                            <Send className="h-5 w-5" />
                            <span className="hidden sm:inline">Telegram</span>
                        </Link>
                        <Link href="https://in.linkedin.com/in/anas-vhora-28455a1a1" target="_blank" className="text-muted-foreground hover:text-blue-500 transition-colors flex items-center gap-2">
                            <Linkedin className="h-5 w-5" />
                            <span className="hidden sm:inline">LinkedIn</span>
                        </Link>
                    </div>
                </div>

                <div className="pt-8 mt-8 border-t border-white/5 text-center text-sm text-muted-foreground">
                    <p>Made with ❤️ by Anas. 100% Free & Open Source.</p>
                </div>
            </div>
        </footer>
    );
}


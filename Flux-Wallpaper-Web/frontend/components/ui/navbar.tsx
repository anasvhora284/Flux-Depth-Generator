"use client";

import Link from "next/link";
import { Button } from "./button";
import { usePathname, useRouter } from "next/navigation";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { User, LogOut, Settings, ChevronDown } from "lucide-react";
import api from "@/lib/api";

export function Navbar() {
    const pathname = usePathname();
    const router = useRouter();
    const isAuthPage = pathname === "/login" || pathname === "/signup";
    const [user, setUser] = useState<any>(null);
    const [showDropdown, setShowDropdown] = useState(false);

    useEffect(() => {
        if (!isAuthPage) {
            checkAuth();
        }
    }, [pathname, isAuthPage]);

    const checkAuth = async () => {
        try {
            const token = localStorage.getItem('token');
            if (token) {
                const res = await api.get('/users/me');
                setUser(res.data);
            }
        } catch (err) {
            // Not logged in or invalid token
            setUser(null);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        setUser(null);
        router.push('/login');
    };

    if (isAuthPage) return null;

    return (
        <div className="fixed top-6 left-0 right-0 z-50 flex justify-center px-4 pointer-events-none">
            <motion.nav
                initial={{ y: -100, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.5 }}
                className="flex items-center justify-between px-6 py-3 rounded-full border border-white/10 bg-black/60 backdrop-blur-xl shadow-2xl w-full max-w-4xl pointer-events-auto"
            >
                <Link href="/" className="flex items-center gap-3">
                    <img src="/logo.png" alt="Flux Depth Logo" className="h-8 w-8 rounded-lg" />
                    <span className="font-heading font-bold text-xl tracking-tight hidden sm:block">Flux Depth</span>
                </Link>

                <div className="flex items-center gap-6">
                    <div className="hidden md:flex items-center gap-6 text-sm font-medium text-muted-foreground">
                        <Link href="/" className="hover:text-white transition-colors">Home</Link>
                        <Link href="/dashboard" className="hover:text-white transition-colors">Tool</Link>
                    </div>

                    <div className="flex items-center gap-3">
                        {user ? (
                            <div className="relative">
                                <button
                                    onClick={() => setShowDropdown(!showDropdown)}
                                    className="flex items-center gap-2 pl-2 pr-4 py-1.5 rounded-full hover:bg-white/5 border border-transparent hover:border-white/10 transition-all group"
                                >
                                    <div className="h-8 w-8 rounded-full bg-gradient-to-r from-blue-400 to-purple-500 flex items-center justify-center text-xs font-bold text-white uppercase">
                                        {user.full_name?.[0] || user.email?.[0] || 'U'}
                                    </div>
                                    <span className="text-sm font-medium text-white max-w-[100px] truncate hidden sm:block">
                                        {user.full_name?.split(' ')[0] || user.email?.split('@')[0]}
                                    </span>
                                    <ChevronDown className="h-4 w-4 text-muted-foreground group-hover:text-white transition-colors" />
                                </button>

                                {showDropdown && (
                                    <div className="absolute top-full right-0 mt-2 w-56 rounded-xl border border-white/10 bg-black/90 backdrop-blur-xl shadow-2xl py-2 overflow-hidden flex flex-col z-50">
                                        <div className="px-4 py-3 border-b border-white/5">
                                            <p className="text-sm font-bold text-white truncate">{user.full_name || 'User'}</p>
                                            <p className="text-xs text-muted-foreground truncate">{user.email}</p>
                                        </div>
                                        <Link
                                            href="/dashboard/settings"
                                            className="px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10 flex items-center gap-2 transition-colors"
                                            onClick={() => setShowDropdown(false)}
                                        >
                                            <Settings className="h-4 w-4" /> Settings
                                        </Link>
                                        <button
                                            onClick={handleLogout}
                                            className="px-4 py-2 text-sm text-red-400 hover:text-red-300 hover:bg-red-500/10 flex items-center gap-2 w-full text-left transition-colors"
                                        >
                                            <LogOut className="h-4 w-4" /> Log out
                                        </button>
                                    </div>
                                )}

                                {/* Click outside to close - simple implementation backdrop */}
                                {showDropdown && (
                                    <div className="fixed inset-0 z-40 bg-transparent" onClick={() => setShowDropdown(false)} />
                                )}
                            </div>
                        ) : (
                            <>
                                <Link href="/login">
                                    <Button variant="ghost" size="sm" className="rounded-full hover:bg-white/10">Log In</Button>
                                </Link>
                                <Link href="/signup">
                                    <Button className="rounded-full px-6 h-9 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white shadow-md transition-all hover:scale-105">Sign Up</Button>
                                </Link>
                            </>
                        )}
                    </div>
                </div>
            </motion.nav>
        </div>
    );
}

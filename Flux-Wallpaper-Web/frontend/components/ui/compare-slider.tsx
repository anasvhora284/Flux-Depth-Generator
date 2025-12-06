"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import Image from "next/image";
import { ChevronsLeftRight } from "lucide-react";
import { cn } from "@/lib/utils";

interface CompareSliderProps {
    original: string;
    modified: string;
    originalAlt?: string;
    modifiedAlt?: string;
    className?: string;
}

export function CompareSlider({
    original,
    modified,
    originalAlt = "Original",
    modifiedAlt = "Modified",
    className,
}: CompareSliderProps) {
    const [sliderPosition, setSliderPosition] = useState(50);
    const [isResizing, setIsResizing] = useState(false);
    const containerRef = useRef<HTMLDivElement>(null);

    const handleMouseDown = useCallback(() => setIsResizing(true), []);
    const handleMouseUp = useCallback(() => setIsResizing(false), []);

    const handleMouseMove = useCallback(
        (e: MouseEvent) => {
            if (!isResizing || !containerRef.current) return;
            const { left, width } = containerRef.current.getBoundingClientRect();
            const x = e.clientX - left;
            const position = Math.max(0, Math.min(100, (x / width) * 100));
            setSliderPosition(position);
        },
        [isResizing]
    );

    const handleTouchMove = useCallback(
        (e: TouchEvent) => {
            if (!isResizing || !containerRef.current) return;
            const { left, width } = containerRef.current.getBoundingClientRect();
            const touch = e.touches[0];
            const x = touch.clientX - left;
            const position = Math.max(0, Math.min(100, (x / width) * 100));
            setSliderPosition(position);
        },
        [isResizing]
    );

    useEffect(() => {
        window.addEventListener("mousemove", handleMouseMove);
        window.addEventListener("mouseup", handleMouseUp);
        window.addEventListener("touchmove", handleTouchMove);
        window.addEventListener("touchend", handleMouseUp);
        return () => {
            window.removeEventListener("mousemove", handleMouseMove);
            window.removeEventListener("mouseup", handleMouseUp);
            window.removeEventListener("touchmove", handleTouchMove);
            window.removeEventListener("touchend", handleMouseUp);
        };
    }, [handleMouseMove, handleMouseUp, handleTouchMove]);

    return (
        <div
            ref={containerRef}
            className={cn("relative w-full h-full overflow-hidden select-none group", className)}
        >
            {/* Underlying Image (Modified/Depth) */}
            <Image
                src={modified}
                alt={modifiedAlt}
                fill
                className="object-cover"
                priority
            />

            {/* Overlay Label (Right) */}
            <div className="absolute top-4 right-4 bg-black/50 backdrop-blur-md text-white text-xs font-bold px-2 py-1 rounded border border-white/10 z-10">
                Depth Map
            </div>

            {/* Clipped Image (Original) */}
            <div
                className="absolute inset-0"
                style={{ clipPath: `polygon(0 0, ${sliderPosition}% 0, ${sliderPosition}% 100%, 0 100%)` }}
            >
                <Image
                    src={original}
                    alt={originalAlt}
                    fill
                    className="object-cover"
                    priority
                />
                {/* Overlay Label (Left) */}
                <div className="absolute top-4 left-4 bg-black/50 backdrop-blur-md text-white text-xs font-bold px-2 py-1 rounded border border-white/10">
                    Original
                </div>
            </div>

            {/* Slider Handle */}
            <div
                className="absolute top-0 bottom-0 w-1 bg-white cursor-ew-resize z-20 shadow-[0_0_10px_rgba(0,0,0,0.5)]"
                style={{ left: `${sliderPosition}%` }}
                onMouseDown={handleMouseDown}
                onTouchStart={handleMouseDown}
            >
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 bg-white rounded-full flex items-center justify-center shadow-lg transform transition-transform group-hover:scale-110">
                    <ChevronsLeftRight className="w-5 h-5 text-gray-900" />
                </div>
            </div>
        </div>
    );
}

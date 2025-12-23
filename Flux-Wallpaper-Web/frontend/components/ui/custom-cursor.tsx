"use client";

import { useEffect, useState } from "react";
import { motion, useMotionValue, useSpring } from "framer-motion";

export const CustomCursor = () => {
  const [isHovering, setIsHovering] = useState(false);
  const cursorX = useMotionValue(-100);
  const cursorY = useMotionValue(-100);

  const springConfig = { damping: 25, stiffness: 700 };
  const cursorXSpring = useSpring(cursorX, springConfig);
  const cursorYSpring = useSpring(cursorY, springConfig);

  useEffect(() => {
    const moveCursor = (e: MouseEvent) => {
      cursorX.set(e.clientX);
      cursorY.set(e.clientY);
    };

    const handleMouseOver = (e: MouseEvent) => {
      if (
        (e.target as HTMLElement).tagName === "BUTTON" ||
        (e.target as HTMLElement).tagName === "A" ||
        (e.target as HTMLElement).closest("button") ||
        (e.target as HTMLElement).closest("a") ||
        (e.target as HTMLElement).classList.contains("cursor-pointer")
      ) {
        setIsHovering(true);
      } else {
        setIsHovering(false);
      }
    };

    window.addEventListener("mousemove", moveCursor);
    window.addEventListener("mouseover", handleMouseOver);

    // Hide default cursor
    document.documentElement.style.cursor = 'none';
    document.body.style.cursor = 'none';

    return () => {
      window.removeEventListener("mousemove", moveCursor);
      window.removeEventListener("mouseover", handleMouseOver);
      document.documentElement.style.cursor = 'auto';
      document.body.style.cursor = 'auto';
    };
  }, [cursorX, cursorY]);

  return (
    <>
      {/* Main Cursor Dot */}
      <motion.div
        className="hidden lg:block fixed top-0 left-0 w-4 h-4 rounded-full bg-white pointer-events-none z-[9999] mix-blend-difference"
        style={{
          boxShadow: "0 0 10px rgba(255, 255, 255, 0.5)",
          x: cursorXSpring,
          y: cursorYSpring,
          translateX: "-50%",
          translateY: "-50%",
        }}
        animate={{
            scale: isHovering ? 2.5 : 1,
        }}
        transition={{ type: "spring", stiffness: 300, damping: 20 }}
      />
      {/* Trailing Ring */}
      <motion.div 
        className="hidden lg:block fixed top-0 left-0 w-8 h-8 rounded-full border border-blue-400 pointer-events-none z-[9998] opacity-50"
        style={{
            x: cursorX,
            y: cursorY,
            translateX: "-50%",
            translateY: "-50%",
        }}
        animate={{
            scale: isHovering ? 1.5 : 1,
            borderColor: isHovering ? "#60a5fa" : "#ffffff",
        }}
        transition={{
            type: "tween",
            ease: "backOut",
            duration: 0.15
        }}
      />
    </>
  );
};

"use client";

import { motion } from "framer-motion";

export default function Template({ children }: { children: React.ReactNode }) {
    return (
        <>
            {/* The Page Content - slight delay to wait for curtain */}
            <motion.div
                initial={{ opacity: 0, scale: 0.98 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: 0.2, ease: "easeOut" }}
                className="w-full"
            >
                {children}
            </motion.div>

            {/* The Curtain Transition - Unveils the page */}
            <motion.div
                className="fixed inset-0 z-[9999] bg-black pointer-events-none"
                initial={{ scaleX: 1 }}
                animate={{ scaleX: 0 }}
                transition={{ duration: 0.8, ease: [0.76, 0, 0.24, 1] }}
                style={{ originX: 0 }} // Wipe from left to right (unveil)
            >
                {/* Optional: Add a "wave" or "curve" visual on the leading edge if possible with SVG, 
                    but pure CSS transform is smoother for performance. 
                    The 'originX: 0' makes it shrink to the left? No, originX:0 means left side is fixed.
                    So it shrinks *towards* the left (reveals from right)? 
                    Wait, if I want to "pull from left", it should start full and shrink to the right?
                    Let's stick to standard Wipe: origin: 1 (right) -> shrinks to right, revealing from left.
                */}
            </motion.div>
            
            {/* Let's try to add the 'Wave' curve overlay on the edge */}
            <motion.svg
                className="fixed top-0 left-0 w-[100px] h-full z-[9999] pointer-events-none text-black"
                style={{ left: "100%", x: "-1px" }} // Positioned just off the right edge of the curtain?
                // Actually, implementing a synced SVG wave with CSS transform is hard. 
                // Let's stick to a solid, professional eases. 
                // Color is Black (Site BG).
            />
            
            {/* 
               User asked for "wavy animation". 
               Let's add a second layer with a slight delay and opacity to create a "wave" motion effect.
            */}
            <motion.div
                className="fixed inset-0 z-[9998] bg-blue-600/20 pointer-events-none"
                initial={{ scaleX: 1 }}
                animate={{ scaleX: 0 }}
                transition={{ duration: 0.9, ease: [0.76, 0, 0.24, 1], delay: 0.05 }}
                style={{ originX: 0 }}
            />
             <motion.div
                className="fixed inset-0 z-[9997] bg-purple-600/20 pointer-events-none"
                initial={{ scaleX: 1 }}
                animate={{ scaleX: 0 }}
                transition={{ duration: 1.0, ease: [0.76, 0, 0.24, 1], delay: 0.1 }}
                style={{ originX: 0 }}
            />
        </>
    );
}

"use client";

import { motion } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";

const stats = [
    { label: "Images Processed", value: "1M+", delay: 0 },
    { label: "Active Users", value: "50k+", delay: 0.1 },
    { label: "Depth Accuracy", value: "99%", delay: 0.2 },
    { label: "Processing Time", value: "<2s", delay: 0.3 },
];

export function StatsSection() {
    return (
        <section className="py-20 relative z-10">
            <div className="container mx-auto px-4">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
                    {stats.map((stat, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, scale: 0.9 }}
                            whileInView={{ opacity: 1, scale: 1 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.5, delay: stat.delay }}
                        >
                            <div className="text-center space-y-2 group">
                                <h3 className="text-4xl md:text-5xl font-bold font-heading bg-clip-text text-transparent bg-gradient-to-b from-white to-white/60 group-hover:to-blue-400 transition-all">
                                    {stat.value}
                                </h3>
                                <p className="text-muted-foreground font-medium uppercase tracking-wider text-sm">
                                    {stat.label}
                                </p>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}

"use client";

import { Navbar } from '@/components/ui/navbar';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { HeroSection } from '@/components/sections/hero';
import { StatsSection } from '@/components/sections/stats';
import { Footer } from '@/components/ui/footer';
import Link from 'next/link';
import { ArrowRight, Upload, Layers, Download, Zap, Clock, Shield } from 'lucide-react';
import { motion, Variants } from 'framer-motion';

const fadeInUp: Variants = {
  hidden: { opacity: 0, y: 30 },
  show: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" } }
};

const staggerContainer: Variants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.15
    }
  }
};

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />

      <main className="flex-1">
        <motion.div 
          initial={{ opacity: 0 }} 
          animate={{ opacity: 1 }} 
          transition={{ duration: 1 }}
        >
          <HeroSection />
        </motion.div>

        {/* How it Works Section */}
        <section id="how-it-works" className="relative py-24 overflow-hidden">
          <div className="container relative mx-auto px-4 z-10">
            <motion.div 
              initial="hidden"
              whileInView="show"
              viewport={{ once: true, margin: "-100px" }}
              variants={fadeInUp}
              className="text-center mb-16"
            >
              <h2 className="font-heading text-3xl md:text-5xl font-bold mb-4">How It Works</h2>
              <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
                Transforming your images into 3D experiences is a simple 3-step process.
              </p>
            </motion.div>

            <motion.div
              variants={staggerContainer}
              initial="hidden"
              whileInView="show"
              viewport={{ once: true, margin: "-50px" }}
              className="grid gap-8 md:grid-cols-3"
            >
              {[
                { icon: Upload, title: "1. Upload", desc: "Drag & drop your 2D images. Supports batch processing up to 200 files.", color: "text-blue-400", bg: "bg-blue-500/10" },
                { icon: Layers, title: "2. AI Processing", desc: "Our advanced neural networks predict accurate depth maps in seconds.", color: "text-purple-400", bg: "bg-purple-500/10" },
                { icon: Download, title: "3. Export 3D", desc: "Download the result as a Depth Map or an interactive 3D Photo.", color: "text-pink-400", bg: "bg-pink-500/10" }
              ].map((step, i) => (
                <motion.div key={i} variants={fadeInUp}>
                  <Card className="h-full border-white/5 bg-white/5 backdrop-blur-sm hover:bg-white/10 transition-colors hover:border-blue-500/30 group">
                    <CardHeader>
                      <motion.div 
                        whileHover={{ scale: 1.1, rotate: 5 }}
                        className={`w-14 h-14 rounded-2xl ${step.bg} flex items-center justify-center mb-4 transition-transform`}
                      >
                        <step.icon className={`h-7 w-7 ${step.color}`} />
                      </motion.div>
                      <CardTitle>{step.title}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <CardDescription className="text-base">{step.desc}</CardDescription>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </motion.div>
          </div>

          {/* Background Mesh Gradients */}
          <div className="absolute top-1/2 left-0 w-1/3 h-1/3 bg-blue-500/10 blur-[100px] -z-10 rounded-full" />
          <div className="absolute bottom-0 right-0 w-1/3 h-1/3 bg-purple-500/10 blur-[100px] -z-10 rounded-full" />
        </section>

        {/* Features Section */}
        <section className="py-24 bg-secondary/30 relative">
          <div className="container mx-auto px-4">
            <motion.div 
              initial="hidden"
              whileInView="show"
              viewport={{ once: true }}
              variants={fadeInUp}
              className="text-center mb-16"
            >
              <h2 className="font-heading text-3xl md:text-5xl font-bold mb-4">Core Capabilities</h2>
              <p className="text-muted-foreground text-lg">Powerful tools for everyone. Completely Free & Open Source.</p>
            </motion.div>

            <motion.div 
              variants={staggerContainer}
              initial="hidden"
              whileInView="show"
              viewport={{ once: true }}
              className="grid gap-6 md:grid-cols-2 lg:grid-cols-3"
            >
              {[
                { icon: Zap, title: "Lightning Fast", desc: "Process hundreds of images in minutes with our optimized GPU pipeline." },
                { icon: Layers, title: "High Precision", desc: "State-of-the-art depth estimation for crisp edges and structural accuracy." },
                { icon: Clock, title: "History Retention", desc: "Access your generated files for up to 1 hour after processing." },
                { icon: Shield, title: "Secure & Private", desc: "Your photos are processed securely and deleted automatically." },
                { icon: ArrowRight, title: "Open API", desc: "Fully documented REST API for developers to build upon." },
                { icon: Download, title: "Multiple Formats", desc: "Export as PNG Depth Maps, 3D JPEGs, or Point Clouds." }
              ].map((feature, i) => (
                <motion.div key={i} variants={fadeInUp}>
                  <Card className="h-full border-white/5 bg-black/20 hover:border-blue-500/30 transition-all group hover:-translate-y-1 hover:shadow-lg hover:shadow-blue-500/10">
                    <CardHeader>
                      <feature.icon className="h-8 w-8 text-muted-foreground mb-2 group-hover:text-blue-400 transition-colors" />
                      <CardTitle className="text-xl group-hover:text-white transition-colors">{feature.title}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-muted-foreground">{feature.desc}</p>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </section>

        {/* Stats Section with simple fade */}
        <motion.div
           initial={{ opacity: 0 }}
           whileInView={{ opacity: 1 }}
           viewport={{ once: true }}
           transition={{ duration: 0.8 }}
        >
          <StatsSection />
        </motion.div>

        {/* CTA Section */}
        <section className="py-24 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-t from-blue-900/20 to-transparent -z-10" />
          <motion.div 
            initial={{ scale: 0.9, opacity: 0 }}
            whileInView={{ scale: 1, opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="container mx-auto px-4 text-center"
          >
            <h2 className="font-heading text-4xl md:text-6xl font-bold mb-8 drop-shadow-lg">Ready to create in 3D?</h2>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <Link href="/dashboard">
                <Button className="h-14 px-10 text-lg bg-blue-600 hover:bg-blue-700 text-white shadow-lg shadow-blue-500/25 transition-all hover:scale-105 hover:shadow-blue-500/50">
                  Start Creating Now
                </Button>
              </Link>
            </div>
          </motion.div>
        </section>
      </main>

      <Footer />
    </div>
  );
}

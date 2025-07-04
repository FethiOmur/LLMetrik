"use client"

import { useEffect, useRef, useState, useMemo } from "react"
import { motion, useScroll, useTransform, useMotionValue, useSpring } from "framer-motion"
import { Cpu, BarChart2, Users, Globe } from "lucide-react"
import { PlaceholdersAndVanishInputDemo } from "./PlaceholdersAndVanishInputDemo"
import { Button } from "@/components/ui/button"
import { ActionSearchBar } from "@/components/ui/action-search-bar"
import FloatingParticle from "./FloatingParticle"

// FloatingParticle artık ayrı dosyadan import ediliyor

export default function HeroSection() {
  const containerRef = useRef<HTMLDivElement>(null)
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end start"],
  })

  const y = useTransform(scrollYProgress, [0, 1], ["0%", "50%"])
  const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0])
  const [isHovered, setIsHovered] = useState(false)

  const stats = [
    { icon: <Cpu className="w-6 h-6" />, label: "Models Compared", value: "50+" },
    { icon: <BarChart2 className="w-6 h-6" />, label: "Benchmarks", value: "100+" },
    { icon: <Users className="w-6 h-6" />, label: "Happy Users", value: "2000+" },
    { icon: <Globe className="w-6 h-6" />, label: "Languages Supported", value: "30+" },
  ]

  // Responsive particle count memoization
  const particleCount = useMemo(() => {
    if (typeof window !== 'undefined') {
      return window.innerWidth < 768 ? 25 : 
             window.innerWidth < 1200 ? 35 : 40
    }
    return 35
  }, [])

  return (
    <section ref={containerRef} className="min-h-screen relative overflow-hidden">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-zinc-900/50 to-black"></div>
        {[...Array(particleCount)].map((_, i) => (
          <FloatingParticle key={i} delay={i * 120} />
        ))}
      </div>

      <motion.div style={{ y, opacity }} className="relative pt-32 pb-16 px-4">
        <div className="max-w-7xl mx-auto relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h1 className="text-7xl md:text-8xl font-bold mb-6 tracking-tight relative">
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-white to-zinc-500">
                Compare LLMs Easily
              </span>
              <motion.span
                className="absolute -inset-1 bg-white rounded-full blur-3xl"
                initial={{ opacity: 0 }}
                animate={{ opacity: [0, 0.1, 0] }}
                transition={{ duration: 3, repeat: Number.POSITIVE_INFINITY, repeatType: "reverse" }}
              />
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-zinc-400 max-w-3xl mx-auto">
              Analyze and compare different Large Language Models. From GPT to Llama, find the perfect model for your AI applications and make data-driven decisions.
            </p>
            
            <PlaceholdersAndVanishInputDemo />
            
            <div className="mt-6 flex justify-center gap-6 items-center">
              <div className="max-w-[320px] w-full"><ActionSearchBar /></div>
              
            <div className="relative inline-block">
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} className="relative z-10">
                <Button
                  size="lg"
                  className="bg-white text-black hover:bg-zinc-200 text-lg px-8 py-6 rounded-full transition-colors relative overflow-hidden group"
                  onMouseEnter={() => setIsHovered(true)}
                  onMouseLeave={() => setIsHovered(false)}
                  asChild
                >
                  <a href="/compare">
                      <span className="relative z-10">Compare Models</span>
                    <motion.span
                      className="absolute inset-0 bg-gradient-to-r from-zinc-200 to-white"
                      initial={{ x: "100%" }}
                      animate={{ x: isHovered ? "0%" : "100%" }}
                      transition={{ duration: 0.3 }}
                    />
                    <motion.span
                      animate={{ x: isHovered ? 5 : 0 }}
                      transition={{ duration: 0.2 }}
                      className="ml-2 relative z-10"
                    >
                      →
                    </motion.span>
                  </a>
                </Button>
              </motion.div>
              </div>
              
              <div className="max-w-[320px] w-full"><ActionSearchBar /></div>
            </div>
          </motion.div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 + index * 0.1 }}
                className="text-center"
              >
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  className="bg-zinc-900/50 rounded-xl p-6 backdrop-blur-lg border border-white/10 transition-colors hover:border-white/20"
                >
                  <div className="mb-2 text-white/70 flex justify-center">{stat.icon}</div>
                  <motion.div
                    className="text-3xl font-bold mb-1"
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    viewport={{ once: true }}
                  >
                    {stat.value}
                  </motion.div>
                  <div className="text-sm text-zinc-400">{stat.label}</div>
                </motion.div>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.div>
    </section>
  )
}

"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { motion, useAnimation } from "framer-motion"
import { useInView } from "react-intersection-observer"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Loader2, CheckCircle, Bell, ArrowRight, Sparkles } from "lucide-react"

export default function SubscribeSection() {
  const [email, setEmail] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [isHovered, setIsHovered] = useState(false)

  const controls = useAnimation()
  const [ref, inView] = useInView({
    triggerOnce: false,
    threshold: 0.2,
    rootMargin: "-100px 0px",
  })

  useEffect(() => {
    if (inView) {
      controls.start("visible")
    } else {
      controls.start("hidden")
    }
  }, [controls, inView])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    // Simulating an API call
    await new Promise((resolve) => setTimeout(resolve, 2000))
    console.log("Subscribed:", email)
    setIsSubmitting(false)
    setIsSubmitted(true)
    // Reset form after 3 seconds
    setTimeout(() => {
      setIsSubmitted(false)
      setEmail("")
    }, 3000)
  }

  const containerVariants = {
    hidden: { opacity: 0, y: 80 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.7,
        ease: [0.22, 1, 0.36, 1],
        staggerChildren: 0.1,
      },
    },
  }

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.5,
        ease: "easeOut",
      }
    },
  }

  // Parlayan arka plan için animasyon
  const glowVariants = {
    hidden: { opacity: 0, scale: 0.8 },
    visible: {
      opacity: [0, 0.3, 0.2],
      scale: 1,
      transition: {
        duration: 2,
        repeat: Infinity,
        repeatType: "reverse" as const,
      }
    }
  }

  return (
    <motion.section 
      id="subscribe" 
      ref={ref}
      initial="hidden"
      animate={controls}
      variants={containerVariants}
      className="py-32 relative overflow-hidden"
    >
      {/* Arka plan desenleri */}
      <div className="absolute inset-0 bg-grid-white/[0.02] bg-[size:40px_40px]" />
      <div className="absolute inset-0 bg-gradient-to-t from-black to-transparent" />
      
      {/* Parlayan efektler */}
      <motion.div 
        variants={glowVariants}
        className="absolute top-1/3 right-[20%] w-64 h-64 bg-white/5 rounded-full blur-3xl" 
      />
      <motion.div 
        variants={glowVariants}
        animate="visible"
        className="absolute bottom-1/4 left-[15%] w-80 h-80 bg-white/5 rounded-full blur-3xl" 
      />
      
      <motion.div
        className="container mx-auto px-4 relative z-10"
      >
        <div className="max-w-3xl mx-auto text-center">
          <motion.div variants={itemVariants} className="mb-3 flex justify-center">
            <span className="relative inline-block">
              <Bell className="text-white/70 mb-4" size={28} />
              <motion.span 
                className="absolute -top-1 -right-1 flex h-3 w-3"
                initial={{ scale: 0.8, opacity: 0.5 }}
                animate={{ scale: 1.2, opacity: 1 }}
                transition={{ duration: 1, repeat: Infinity, repeatType: "reverse" as const }}
              >
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-white"></span>
              </motion.span>
            </span>
          </motion.div>
          
          <motion.h2 variants={itemVariants} className="text-5xl md:text-6xl font-bold mb-6 text-center text-white tracking-tight">
            Never Miss an <span className="bg-clip-text text-transparent bg-gradient-to-r from-white to-zinc-500">Update</span>
          </motion.h2>
          
          <motion.p variants={itemVariants} className="text-xl text-zinc-400 mb-10 max-w-2xl mx-auto">
            Stay updated with the latest news, model releases, and benchmarks in the world of LLMs.
          </motion.p>
          
          <motion.div
            variants={itemVariants}
            className="max-w-xl mx-auto backdrop-blur-lg rounded-2xl p-2.5 shadow-2xl bg-zinc-900/50 border border-white/10"
          >
            <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-2">
              <div className="flex-grow">
                <Input
                  type="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={handleChange}
                  required
                  className="bg-black/50 border-zinc-800 text-zinc-200 placeholder-zinc-500 h-12 rounded-xl"
                />
              </div>
              <div className="relative inline-block">
                <motion.div 
                  whileHover={{ scale: 1.05 }} 
                  whileTap={{ scale: 0.95 }} 
                  className="relative z-10"
                  onMouseEnter={() => setIsHovered(true)}
                  onMouseLeave={() => setIsHovered(false)}
                >
              <Button
                type="submit"
                className="h-12 px-6 rounded-xl bg-white text-black hover:bg-zinc-200 transition-all relative overflow-hidden group"
                disabled={isSubmitting || isSubmitted}
              >
                <span className="relative z-10 flex items-center justify-center">
                  {isSubmitting ? (
                    <Loader2 className="animate-spin" size={20} />
                  ) : isSubmitted ? (
                    <CheckCircle size={20} />
                  ) : (
                    <>
                          Subscribe 
                          <motion.span
                            animate={{ x: isHovered ? 5 : 0 }}
                            transition={{ duration: 0.2 }}
                            className="ml-2 relative z-10"
                          >
                            <ArrowRight size={16} />
                          </motion.span>
                    </>
                  )}
                </span>
                    <motion.span
                      className="absolute inset-0 bg-gradient-to-r from-zinc-200 to-white"
                      initial={{ x: "100%" }}
                      animate={{ x: isHovered ? "0%" : "100%" }}
                      transition={{ duration: 0.3 }}
                    />
              </Button>
                </motion.div>
              </div>
            </form>
          </motion.div>
          
          {isSubmitted && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-4 text-white flex items-center justify-center gap-1"
            >
              <Sparkles size={16} className="text-white/70" />
              <span>Thank you for subscribing!</span>
              <Sparkles size={16} className="text-white/70" />
            </motion.div>
          )}
          
          <motion.p variants={itemVariants} className="text-zinc-500 text-sm mt-6">
            We respect your privacy. Unsubscribe at any time.
          </motion.p>
        </div>
      </motion.div>
    </motion.section>
  )
} 
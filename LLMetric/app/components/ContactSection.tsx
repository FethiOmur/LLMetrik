"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { motion, useAnimation } from "framer-motion"
import { useInView } from "react-intersection-observer"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Loader2, CheckCircle, Bell, ArrowRight } from "lucide-react"

export default function SubscribeSection() {
  const [email, setEmail] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)

  const controls = useAnimation()
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  })

  useEffect(() => {
    if (inView) {
      controls.start("visible")
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
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  }

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
    },
  }

  return (
    <section id="subscribe" ref={ref} className="py-24 bg-zinc-900 relative overflow-hidden">
      <div className="absolute inset-0 bg-grid-white/[0.02] bg-[size:40px_40px]" />
      <div className="absolute inset-0 bg-gradient-to-t from-zinc-900 to-transparent" />
      
      {/* Decorative elements */}
      <div className="absolute top-1/4 right-[15%] w-32 h-32 bg-white/5 rounded-full blur-3xl" />
      <div className="absolute bottom-1/3 left-[10%] w-40 h-40 bg-white/5 rounded-full blur-3xl" />
      
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate={controls}
        className="container mx-auto px-4 relative z-10"
      >
        <div className="max-w-3xl mx-auto text-center">
          <motion.div variants={itemVariants} className="mb-3">
            <Bell className="inline-block text-white/70 mb-4" size={28} />
          </motion.div>
          <motion.h2 variants={itemVariants} className="text-5xl font-bold mb-4 text-center text-zinc-200">
            Subscribe
        </motion.h2>
          <motion.p variants={itemVariants} className="text-xl text-zinc-400 mb-10 max-w-2xl mx-auto">
            Stay updated with the latest news, model releases, and benchmarks in the world of LLMs.
          </motion.p>
          
        <motion.div
          variants={itemVariants}
            className="max-w-xl mx-auto backdrop-blur-lg rounded-2xl p-2 shadow-2xl bg-gradient-to-r from-white/10 to-white/5"
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
                      Subscribe <ArrowRight className="ml-2" size={16} />
                  </>
                )}
              </span>
            </Button>
          </form>
        </motion.div>
          
          {isSubmitted && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-4 text-green-400"
            >
              Thank you for subscribing!
            </motion.div>
          )}
          
          <motion.p variants={itemVariants} className="text-zinc-500 text-sm mt-6">
            We respect your privacy. Unsubscribe at any time.
          </motion.p>
        </div>
      </motion.div>
    </section>
  )
}

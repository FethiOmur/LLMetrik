"use client"

import { motion } from "framer-motion"
import { useEffect, useState } from "react"

interface FloatingParticleProps {
  delay?: number
}

export default function FloatingParticle({ delay = 0 }: FloatingParticleProps) {
  const [isClient, setIsClient] = useState(false)
  const [particleProps, setParticleProps] = useState({
    x: "0%",
    y: "0%",
    animateX: "0%",
    animateY: "0%",
    duration: 20,
    opacity: 0.4
  })

  // Ensure client-side only rendering
  useEffect(() => {
    setIsClient(true)
    
    // Generate consistent values after hydration
    const randomSeed = delay || 0
    const x = ((randomSeed * 17) % 100).toString() + "%"
    const y = ((randomSeed * 23) % 100).toString() + "%"
    const animateX = (((randomSeed * 31) % 100)).toString() + "%"
    const animateY = (((randomSeed * 37) % 100)).toString() + "%"
    const duration = 15 + ((randomSeed * 13) % 10)
    const opacity = 0.2 + ((randomSeed * 7) % 30) / 100

    setParticleProps({
      x,
      y,
      animateX,
      animateY,
      duration,
      opacity
    })
  }, [delay])

  // Don't render on server or before hydration
  if (!isClient) {
    return null
  }

  return (
    <motion.div
      className="absolute w-1 h-1 bg-white rounded-full will-change-transform"
      initial={{
        x: particleProps.x,
        y: particleProps.y,
        opacity: 0
      }}
      animate={{
        x: particleProps.animateX,
        y: particleProps.animateY,
        opacity: particleProps.opacity
      }}
      transition={{
        duration: particleProps.duration,
        repeat: Infinity,
        repeatType: "reverse",
        ease: "linear",
        delay: delay / 1000
      }}
      style={{
        left: particleProps.x,
        top: particleProps.y
      }}
    />
  )
} 
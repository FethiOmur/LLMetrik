"use client"

import React, { useState } from "react"
import { motion } from "framer-motion"
import Link from "next/link"
import { cn } from "@/lib/utils"
import { ChevronRight } from "lucide-react"

interface ButtonCTAProps {
  text: string
  href: string
  variant?: "primary" | "secondary" | "outline"
  className?: string
  icon?: React.ReactNode
}

export function ButtonCTA({
  text,
  href,
  variant = "primary",
  className,
  icon = <ChevronRight className="ml-2 h-4 w-4" />
}: ButtonCTAProps) {
  const [isHovered, setIsHovered] = useState(false)

  return (
    <Link
      href={href}
      className={cn(
        "inline-flex items-center justify-center rounded-full px-6 py-2.5 text-sm font-medium transition-all duration-200 relative overflow-hidden",
        variant === "primary" && "bg-gradient-to-r from-zinc-800 to-zinc-900 text-white hover:from-zinc-700 hover:to-zinc-800",
        variant === "secondary" && "bg-white text-black hover:bg-zinc-100",
        variant === "outline" && "border border-zinc-700 text-white hover:bg-zinc-900/50",
        className
      )}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <span className="relative z-10 flex items-center">
        {text}
        <motion.span
          animate={{ x: isHovered ? 5 : 0 }}
          transition={{ duration: 0.2 }}
        >
          {icon}
        </motion.span>
      </span>
      <motion.span
        className="absolute inset-0 bg-gradient-to-r from-zinc-800 to-zinc-700"
        initial={{ x: "100%" }}
        animate={{ x: isHovered ? "0%" : "100%" }}
        transition={{ duration: 0.3 }}
        style={{ display: variant === "primary" ? "block" : "none" }}
      />
    </Link>
  )
} 
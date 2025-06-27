"use client"

import { useEffect, useState } from "react"
import { StarBorder } from "@/components/ui/star-border"
import { cn } from "@/lib/utils"

const LLM_NAMES = [
  "GPT-4",
  "Llama 3",
  "Claude 3",
  "Gemini",
  "Mistral"
]

export function RotatingLLMButton() {
  const [index, setIndex] = useState(0)
  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prev) => (prev + 1) % LLM_NAMES.length)
    }, 1500)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="px-4">
      <StarBorder as="div" className="w-full max-w-[180px] mx-auto" color="white">
        <button
          type="button"
          className={cn(
            "w-full rounded-full bg-zinc-900/80 px-5 py-3 text-base text-white outline-none transition-all duration-300 placeholder:text-zinc-400",
            "backdrop-blur-sm flex items-center justify-center font-semibold min-h-[48px]"
          )}
        >
          <span className="transition-all duration-500">{LLM_NAMES[index]}</span>
        </button>
      </StarBorder>
    </div>
  )
} 
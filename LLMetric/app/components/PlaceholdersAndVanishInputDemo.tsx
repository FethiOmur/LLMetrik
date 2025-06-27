"use client"

import type React from "react"

import { PlaceholdersAndVanishInput } from "@/components/ui/placeholders-and-vanish-input"
import { StarBorder } from "@/components/ui/star-border"

export function PlaceholdersAndVanishInputDemo() {
  const placeholders = [
    "Which model has the best reasoning capabilities?",
    "How does GPT-4 compare to Claude 3?",
    "What's the token limit for Llama 3?",
    "Which model is best for code generation?",
    "How to fine-tune an open source LLM?",
  ]

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value)
  }

  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    console.log("submitted")
  }

  return (
    <div className="px-4">
      <StarBorder 
        as="div" 
        className="w-full md:max-w-2xl mx-auto"
        color="white"
      >
        <PlaceholdersAndVanishInput 
          placeholders={placeholders} 
          onChange={handleChange} 
          onSubmit={onSubmit}
          className="w-full" 
          inputClassName="border-none shadow-none rounded-2xl"
        />
      </StarBorder>
    </div>
  )
}

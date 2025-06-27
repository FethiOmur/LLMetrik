"use client"

import type React from "react"

import { useState, useEffect, useRef } from "react"
import { cn } from "@/lib/utils"

interface PlaceholdersAndVanishInputProps {
  placeholders: string[]
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void
  onSubmit?: (e: React.FormEvent<HTMLFormElement>) => void
  className?: string
  inputClassName?: string
}

export function PlaceholdersAndVanishInput({
  placeholders,
  onChange,
  onSubmit,
  className,
  inputClassName,
}: PlaceholdersAndVanishInputProps) {
  const [currentPlaceholder, setCurrentPlaceholder] = useState(0)
  const [isFocused, setIsFocused] = useState(false)
  const [value, setValue] = useState("")
  const inputRef = useRef<HTMLInputElement>(null)

  const [typedPlaceholder, setTypedPlaceholder] = useState("")
  const [isTyping, setIsTyping] = useState(false)
  const [typeIndex, setTypeIndex] = useState(0)

  useEffect(() => {
    if (placeholders.length <= 1) return

    const interval = setInterval(() => {
      if (!isFocused && value === "") {
        setCurrentPlaceholder((prev) => (prev + 1) % placeholders.length)
        setTypedPlaceholder("")
        setTypeIndex(0)
        setIsTyping(true)
      }
    }, 3000)

    return () => clearInterval(interval)
  }, [isFocused, placeholders.length, value])

  useEffect(() => {
    if (!isTyping) return

    const currentFullPlaceholder = placeholders[currentPlaceholder]

    if (typeIndex < currentFullPlaceholder.length) {
      const timeout = setTimeout(() => {
        setTypedPlaceholder((prev) => prev + currentFullPlaceholder[typeIndex])
        setTypeIndex((prev) => prev + 1)
      }, 100) // Adjust speed as needed

      return () => clearTimeout(timeout)
    } else {
      setIsTyping(false)
    }
  }, [isTyping, typeIndex, currentPlaceholder, placeholders])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setValue(e.target.value)
    onChange?.(e)
  }

  const handleFocus = () => {
    setIsFocused(true)
  }

  const handleBlur = () => {
    setIsFocused(false)
  }

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    onSubmit?.(e)
    setValue("")
    if (inputRef.current) {
      inputRef.current.blur()
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className={cn("relative flex w-full items-center justify-center", className)}
    >
      <div className="relative w-full group">
      <input
        ref={inputRef}
        type="text"
        value={value}
        onChange={handleChange}
        onFocus={handleFocus}
        onBlur={handleBlur}
        placeholder={isTyping || typedPlaceholder === "" ? typedPlaceholder : placeholders[currentPlaceholder]}
        className={cn(
            "w-full rounded-full bg-zinc-900/80 px-5 py-3 text-base text-white outline-none transition-all duration-300 placeholder:text-zinc-400",
            "backdrop-blur-sm",
            "focus:shadow-inner focus:shadow-white/5",
          inputClassName,
        )}
      />
        <button
          type="submit"
          className="absolute right-2.5 top-1/2 -translate-y-1/2 rounded-full bg-gradient-to-r from-zinc-700 to-zinc-800 p-2 text-white transition-all duration-300 hover:from-zinc-600 hover:to-zinc-700 hover:shadow-[0_0_10px_rgba(255,255,255,0.15)]"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </button>
      </div>
    </form>
  )
}

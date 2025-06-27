"use client"

import Image from "next/image"

interface ExpandingCardProps {
  title: string
  description: string
  summary?: string
  image: string
}

export default function ExpandingCard({ title, description, summary, image }: ExpandingCardProps) {
  // Eğer özet belirtilmemişse açıklamayı kullan
  const displayText = summary || description

  return (
    <div className="relative overflow-hidden h-[300px] rounded-lg shadow-md group border border-zinc-700/50">
      <div className="relative h-full">
        <Image 
          src={image || "/placeholder.svg"} 
          alt={title} 
          fill
          className="object-cover"
        />
      </div>
      <div className="absolute bottom-0 left-0 right-0 bg-zinc-900/90 border-t border-zinc-700/50 transition-all duration-300 ease-in-out h-[100px] group-hover:h-[70%] overflow-hidden">
        <div className="p-4">
          <h2 className="text-xl font-semibold text-white mb-2">{title}</h2>
          <div className="transition-all duration-300 ease-in-out max-h-[40px] group-hover:max-h-[calc(100%-45px)] overflow-hidden">
            <p className="text-zinc-300 line-clamp-6">{displayText}</p>
          </div>
        </div>
      </div>
    </div>
  )
} 
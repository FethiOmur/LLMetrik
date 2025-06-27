import Link from "next/link"
import Image from "next/image"
import { cn } from "@/lib/utils"

export interface TestimonialAuthor {
  name: string
  handle: string
  avatar: string
}

interface TestimonialCardProps {
  author: TestimonialAuthor
  text: string
  href?: string
  className?: string
}

export function TestimonialCard({ 
  author, 
  text, 
  href, 
  className 
}: TestimonialCardProps) {
  const Card = href ? Link : "div"
  
  return (
    <Card 
      href={href || "#"} 
      className={cn(
        "flex flex-col gap-4 rounded-xl p-6",
        "bg-gradient-to-br from-zinc-900 via-zinc-800 to-zinc-900 backdrop-blur-md border border-white/10",
        "w-96 shrink-0 mx-2 sm:mx-4",
        "transition duration-300 ease-in-out",
        href && "hover:bg-gradient-to-br hover:from-zinc-800 hover:via-zinc-700 hover:to-zinc-800 hover:border-white/20",
        className
      )}
    >
      <div className="space-y-4">
        <p className="text-sm sm:text-base text-zinc-300">"{text}"</p>
        
        <div className="flex items-center gap-3">
          <div className="relative h-10 w-10 overflow-hidden rounded-full">
            <Image
              src={author.avatar}
              alt={author.name}
              fill
              className="object-cover"
            />
          </div>
          
          <div>
            <p className="text-sm font-medium text-white">{author.name}</p>
            <p className="text-sm text-zinc-400">{author.handle}</p>
          </div>
        </div>
      </div>
    </Card>
  )
} 
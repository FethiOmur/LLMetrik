import { cn } from "@/lib/utils"
import { XCard } from "@/components/ui/x-gradient-card"

interface TestimonialsSectionProps {
  title: string
  description: string
  testimonials: Array<{
    authorName: string
    authorHandle: string
    authorImage: string
    content: string[]
    isVerified?: boolean
    timestamp: string
    link?: string
  }>
  className?: string
}

export function TestimonialsSection({ 
  title,
  description,
  testimonials,
  className 
}: TestimonialsSectionProps) {
  return (
    <section className={cn(
      "bg-transparent text-foreground",
      "py-8 sm:py-12 px-0",
      className
    )}>
      <div className="mx-auto flex max-w-container flex-col items-center gap-4 text-center sm:gap-8">
        {(title || description) && (
          <div className="flex flex-col items-center gap-4 px-4">
            {title && (
              <h3 className="max-w-[720px] text-2xl font-semibold leading-tight sm:text-3xl sm:leading-tight text-white">
                {title}
              </h3>
            )}
            {description && (
              <p className="text-md max-w-[600px] font-medium text-zinc-400 sm:text-lg">
                {description}
              </p>
            )}
          </div>
        )}

        <div className="relative flex w-full flex-col items-center justify-center overflow-hidden">
          <div className="group flex overflow-hidden p-2 [--gap:2rem] [gap:var(--gap)] flex-row [--duration:100s]">
            <div className="flex shrink-0 justify-around [gap:var(--gap)] animate-marquee flex-row group-hover:[animation-play-state:paused]">
              {[...Array(4)].map((_, setIndex) => (
                testimonials.map((testimonial, i) => (
                  <XCard 
                    key={`${setIndex}-${i}`}
                    {...testimonial}
                  />
                ))
              ))}
            </div>
          </div>

          <div className="pointer-events-none absolute inset-y-0 left-0 hidden w-1/3 bg-gradient-to-r from-black sm:block" />
          <div className="pointer-events-none absolute inset-y-0 right-0 hidden w-1/3 bg-gradient-to-l from-black sm:block" />
        </div>
      </div>
    </section>
  )
} 
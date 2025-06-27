import { TestimonialsSection } from "@/components/blocks/testimonials-with-marquee"

const testimonials = [
  {
    authorName: "Emma Thompson",
    authorHandle: "emmaai",
    authorImage: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&h=150&fit=crop&crop=face",
    content: ["GPT-4's reasoning capabilities have transformed how we approach data analysis. The speed and accuracy are unprecedented."],
    isVerified: true,
    timestamp: "2 saat önce",
    link: "#"
  },
  {
    authorName: "David Park",
    authorHandle: "davidtech",
    authorImage: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
    content: ["Claude 3's API integration is flawless. We've reduced our development time by 60% since implementing this model."],
    isVerified: true,
    timestamp: "1 gün önce",
    link: "#"
  },
  {
    authorName: "Sofia Rodriguez",
    authorHandle: "sofiaml",
    authorImage: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&h=150&fit=crop&crop=face",
    content: ["Llama 3 has revolutionized our local AI deployment. Finally, an open source model that actually understands context!"],
    isVerified: false,
    timestamp: "3 gün önce"
  },
  {
    authorName: "James Wilson",
    authorHandle: "jwilsonai",
    authorImage: "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150&h=150&fit=crop&crop=face",
    content: ["Mistral's performance-to-cost ratio is unmatched. We're getting enterprise-level results at a fraction of the price."],
    isVerified: true,
    timestamp: "1 hafta önce"
  },
  {
    authorName: "Lin Wei",
    authorHandle: "linweidev",
    authorImage: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face",
    content: ["Gemini's multimodal capabilities have opened entirely new use cases we hadn't even considered for our platform."],
    isVerified: true,
    timestamp: "2 hafta önce"
  }
]

export function TestimonialsSectionDemo() {
  return (
    <TestimonialsSection
      title=""
      description=""
      testimonials={testimonials}
    />
  )
} 
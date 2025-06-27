"use client"

import { useState, useRef, useEffect } from "react"
import { motion, useAnimation, useInView, AnimatePresence } from "framer-motion"
import { Newspaper, TrendingUp, Lightbulb, Award, ExternalLink } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"

const newsItems = [
  {
    name: "GPT-5 Announcement",
    date: "May 10, 2023",
    icon: <Newspaper className="w-6 h-6" />,
    summary:
      "OpenAI has officially announced GPT-5, promising unprecedented reasoning capabilities and multimodal understanding.",
    features: [
      "10x larger parameter count than GPT-4",
      "Advanced reasoning capabilities",
      "Improved multimodal understanding",
      "Enhanced factual accuracy",
      "Reduced hallucinations",
      "Expanded context window of 100k tokens",
    ],
    highlight: "BREAKING NEWS!",
  },
  {
    name: "Claude 3 Sonnet Released",
    date: "April 28, 2023",
    icon: <TrendingUp className="w-6 h-6" />,
    summary:
      "Anthropic has released Claude 3 Sonnet, a more efficient and cost-effective version of their flagship AI assistant.",
    features: [
      "2x faster than Claude 3 Opus",
      "30% more cost-effective",
      "Improved coding capabilities",
      "Better instruction following",
      "Enhanced multilingual support",
      "New API features for developers",
    ],
    popular: true,
  },
  {
    name: "Llama 3 Open Source",
    date: "April 15, 2023",
    icon: <Lightbulb className="w-6 h-6" />,
    summary: "Meta has released Llama 3 as fully open source, allowing unrestricted commercial use and modification.",
    features: [
      "Fully open source license",
      "70B parameter model",
      "Commercial use allowed",
      "Competitive with closed models",
      "Community-driven improvements",
    ],
    notIncluded: ["No usage restrictions"],
  },
  {
    name: "LLM Benchmark Results",
    date: "April 5, 2023",
    icon: <Award className="w-6 h-6" />,
    summary:
      "The latest MMLU and HELM benchmark results show significant improvements across all major language models.",
    features: [
      "GPT-4 leads in reasoning tasks",
      "Claude 3 tops in factuality",
      "Llama 3 shows impressive gains",
      "Mistral Large excels in coding",
      "Gemini Ultra improves in math",
      "Overall 15% improvement across models",
    ],
  },
]

export default function LicenseOptionsSection() {
  const [hoveredCard, setHoveredCard] = useState<number | null>(null)
  const controls = useAnimation()
  const ref = useRef(null)
  const inView = useInView(ref, { once: true })

  useEffect(() => {
    if (inView) {
      controls.start("visible")
    }
  }, [controls, inView])

  return (
    <section ref={ref} id="license-options" className="py-20 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-black via-zinc-900/20 to-black"></div>

      <div className="container mx-auto px-4 relative">
        <motion.div
          initial="hidden"
          animate={controls}
          variants={{
            hidden: { opacity: 0, y: 20 },
            visible: { opacity: 1, y: 0, transition: { duration: 0.6 } },
          }}
          className="text-center mb-16"
        >
          <h2 className="text-5xl md:text-6xl font-bold mb-6">Latest LLM News</h2>
          <p className="text-xl text-zinc-400 max-w-2xl mx-auto">
            Stay updated with the most recent developments in the world of Large Language Models
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {newsItems.map((item, index) => (
            <motion.div
              key={item.name}
              variants={{
                hidden: { opacity: 0, y: 20 },
                visible: { opacity: 1, y: 0, transition: { duration: 0.5, delay: index * 0.1 } },
              }}
              initial="hidden"
              animate={controls}
              onHoverStart={() => setHoveredCard(index)}
              onHoverEnd={() => setHoveredCard(null)}
            >
              <Card
                className={`relative h-full ${
                  hoveredCard === index ? "scale-105" : "scale-100"
                } transition-all duration-300`}
              >
                <div className="absolute inset-0 rounded-lg p-[1px] bg-gradient-to-br from-white/20 to-white/0">
                  <div className="absolute inset-0 rounded-lg bg-black"></div>
                </div>

                {item.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-white text-black px-4 py-1 rounded-full text-sm font-semibold animate-pulse">
                      Trending
                    </span>
                  </div>
                )}

                {item.highlight && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-red-500 text-white px-4 py-1 rounded-full text-sm font-semibold animate-pulse">
                      {item.highlight}
                    </span>
                  </div>
                )}

                <CardContent className="relative p-6 rounded-lg h-full flex flex-col">
                  <div className="text-center mb-6">
                    <div className="inline-flex p-3 rounded-full bg-zinc-900 border border-white/10 mb-4">
                      {item.icon}
                    </div>
                    <h3 className="text-xl font-bold mb-2">{item.name}</h3>
                    <div className="text-sm font-medium text-zinc-400">{item.date}</div>
                  </div>

                  <div className="flex-grow">
                    <p className="text-sm text-zinc-300 mb-4">{item.summary}</p>

                    <AnimatePresence>
                      {hoveredCard === index && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{
                            height: "auto",
                            opacity: 1,
                            transition: {
                              height: {
                                duration: 0.3,
                                ease: "easeOut",
                              },
                              opacity: {
                                duration: 0.2,
                                delay: 0.1,
                              },
                            },
                          }}
                          exit={{
                            height: 0,
                            opacity: 0,
                            transition: {
                              height: {
                                duration: 0.2,
                              },
                              opacity: {
                                duration: 0.1,
                              },
                            },
                          }}
                          className="overflow-hidden"
                        >
                          <ul className="space-y-3 mb-6">
                            {item.features.map((feature, i) => (
                              <motion.li
                                key={i}
                                className="flex items-start"
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ duration: 0.3, delay: 0.2 + i * 0.05 }}
                              >
                                <div className="h-1.5 w-1.5 rounded-full bg-white mt-1.5 mr-2 shrink-0"></div>
                                <span className="text-sm text-zinc-300">{feature}</span>
                              </motion.li>
                            ))}
                            {item.notIncluded?.map((feature, i) => (
                              <motion.li
                                key={i}
                                className="flex items-start text-zinc-500"
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ duration: 0.3, delay: 0.2 + (item.features.length + i) * 0.05 }}
                              >
                                <div className="h-1.5 w-1.5 rounded-full bg-zinc-500 mt-1.5 mr-2 shrink-0"></div>
                                <span className="text-sm">{feature}</span>
                              </motion.li>
                            ))}
                          </ul>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>

                  <Button asChild className={`w-full bg-white text-black hover:bg-zinc-200 transition-colors mt-4`}>
                    <a href="#" target="_blank" rel="noopener noreferrer">
                      Read Full Story <ExternalLink className="ml-2 h-4 w-4" />
                    </a>
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}

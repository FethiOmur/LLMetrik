"use client"

import { useState, useRef } from "react"
import { motion, useScroll, useTransform } from "framer-motion"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Star, Zap, Clock, DollarSign, BarChart4 } from "lucide-react"
import { LazyChart, LazyChartBar } from "@/components/ui/lazy-chart"

// Example data - In a real project, this could be loaded from an API or another data source
const llmModels = [
  {
    id: 1,
    name: "GPT-4",
    provider: "OpenAI",
    type: "text",
    contextWindow: "128,000 tokens",
    price: "$0.01/1K tokens",
    speed: "High",
    features: ["Multimodal", "Tool use", "Function calling"],
    rating: 4.8,
    strengths: ["Reasoning", "Knowledge", "Instruction following"],
    weaknesses: ["Expensive", "Occasional hallucinations"],
    description:
      "GPT-4 is OpenAI's most advanced system, producing safer and more useful responses. It's available in the ChatGPT Plus subscription and API.",
  },
  {
    id: 2,
    name: "Claude 3 Opus",
    provider: "Anthropic",
    type: "text",
    contextWindow: "200,000 tokens",
    price: "$0.015/1K tokens",
    speed: "Medium",
    features: ["Multimodal", "Tool use", "Very long context"],
    rating: 4.7,
    strengths: ["Reasoning", "Context length", "Ethics"],
    weaknesses: ["Slower than some alternatives", "Limited tool use"],
    description:
      "Claude 3 Opus is Anthropic's most powerful model, designed for complex tasks requiring deep analysis and careful reasoning.",
  },
  {
    id: 3,
    name: "Llama 3 70B",
    provider: "Meta",
    type: "text",
    contextWindow: "8,000 tokens",
    price: "Free (self-hosted)",
    speed: "Depends on hardware",
    features: ["Open weights", "Customizable", "Commercial use"],
    rating: 4.5,
    strengths: ["Accessibility", "Customizability", "No API costs"],
    weaknesses: ["Requires significant hardware", "Shorter context window"],
    description:
      "Meta's Llama 3 70B is a powerful open-source model that can be run locally on sufficient hardware or through various APIs.",
  },
  {
    id: 4,
    name: "Mistral Large",
    provider: "Mistral AI",
    type: "text",
    contextWindow: "32,000 tokens",
    price: "$0.008/1K tokens",
    speed: "High",
    features: ["Function calling", "Good reasoning", "Multilingual"],
    rating: 4.6,
    strengths: ["Speed", "Cost-effective", "Good performance/price ratio"],
    weaknesses: ["Smaller context window than top models"],
    description:
      "Mistral Large is Mistral AI's most capable model, offering excellent performance at a more affordable price point than some competitors.",
  },
]

export default function ModelsComparisonSection() {
  const [selectedTab, setSelectedTab] = useState("all")
  const sectionRef = useRef<HTMLDivElement>(null)

  // Scroll-based opacity for fading out when scrolling down
  const { scrollYProgress } = useScroll({
    target: sectionRef,
    offset: ["start start", "end start"],
  })

  // Transform scrollYProgress to opacity (1 at the start, 0 as it scrolls out of view)
  const opacity = useTransform(scrollYProgress, [0, 0.8], [1, 0])

  // Filter models based on selection
  const filteredModels = selectedTab === "all" 
    ? llmModels 
    : llmModels.filter(model => model.provider.toLowerCase() === selectedTab)

  return (
    <motion.section
      ref={sectionRef}
      style={{ opacity }}
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="py-24"
      id="models"
    >
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">LLM Model Comparison</h2>
          <p className="text-xl text-zinc-400 max-w-3xl mx-auto">
            Comprehensive evaluation of AI models and service providers
          </p>
          <p className="text-xl text-zinc-400 max-w-3xl mx-auto mt-2">
            Gain insights into the AI ecosystem to select the optimal model and provider for your specific needs.
          </p>
        </div>

        <Tabs defaultValue="all" className="w-full mb-12">
          <div className="flex justify-center mb-6">
            <TabsList className="bg-zinc-800/50 p-1 rounded-full">
              <TabsTrigger value="all" onClick={() => setSelectedTab("all")} className="rounded-full px-6">
                All
              </TabsTrigger>
              <TabsTrigger value="openai" onClick={() => setSelectedTab("openai")} className="rounded-full px-6">
                OpenAI
              </TabsTrigger>
              <TabsTrigger value="anthropic" onClick={() => setSelectedTab("anthropic")} className="rounded-full px-6">
                Anthropic
              </TabsTrigger>
              <TabsTrigger value="meta" onClick={() => setSelectedTab("meta")} className="rounded-full px-6">
                Meta
              </TabsTrigger>
              <TabsTrigger value="mistral" onClick={() => setSelectedTab("mistral")} className="rounded-full px-6">
                Mistral
              </TabsTrigger>
            </TabsList>
          </div>

          <TabsContent value={selectedTab} className="mt-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {filteredModels.map((model) => (
                <Card
                  key={model.id}
                  className="bg-zinc-900/50 backdrop-blur-md border border-white/10 overflow-hidden group hover:border-white/20 transition-all"
                >
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle className="text-2xl">{model.name}</CardTitle>
                        <CardDescription className="text-zinc-400 mt-1">
                          {model.provider}
                        </CardDescription>
                      </div>
                      <div className="flex items-center space-x-1 bg-zinc-800 px-2 py-1 rounded-full text-xs">
                        <Star className="w-3 h-3 fill-yellow-500 text-yellow-500" />
                        <span>{model.rating}</span>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="text-sm space-y-2">
                      <div className="flex justify-between text-zinc-400">
                        <span className="flex items-center">
                          <DollarSign className="w-4 h-4 mr-1 opacity-70" /> Price
                        </span>
                        <span className="text-white">{model.price}</span>
                      </div>
                      <div className="flex justify-between text-zinc-400">
                        <span className="flex items-center">
                          <BarChart4 className="w-4 h-4 mr-1 opacity-70" /> Context Window
                        </span>
                        <span className="text-white">{model.contextWindow}</span>
                      </div>
                      <div className="flex justify-between text-zinc-400">
                        <span className="flex items-center">
                          <Clock className="w-4 h-4 mr-1 opacity-70" /> Speed
                        </span>
                        <span className="text-white">{model.speed}</span>
                      </div>
                    </div>

                    <div className="pt-3">
                      <h4 className="text-sm font-medium mb-2">Features</h4>
                      <div className="flex flex-wrap gap-1">
                        {model.features.map((feature, index) => (
                          <Badge key={index} variant="outline" className="bg-zinc-800/50 text-xs">
                            {feature}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Button
                      className="w-full bg-white/10 hover:bg-white/20 text-white border-0"
                      variant="outline"
                    >
                      <Zap className="w-4 h-4 mr-2" />
                      More Details
                    </Button>
                  </CardFooter>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="charts" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <LazyChart>
                <LazyChartBar />
              </LazyChart>
              <Card className="p-6 bg-gradient-to-br from-zinc-900/50 to-zinc-800/50 border-zinc-700">
                <h3 className="text-lg font-semibold mb-4 text-white">Performance Comparison</h3>
                <div className="space-y-3">
                  {llmModels.slice(0, 3).map((model, index) => (
                    <div key={model.id} className="flex items-center justify-between p-3 bg-zinc-800/50 rounded-lg">
                      <span className="text-white">{model.name}</span>
                      <div className="flex items-center space-x-2">
                        <div className="h-2 w-24 bg-zinc-700 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-gradient-to-r from-blue-500 to-purple-500" 
                            style={{ width: `${85 - index * 5}%` }}
                          />
                        </div>
                        <span className="text-sm text-zinc-400">{85 - index * 5}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </motion.section>
  )
} 
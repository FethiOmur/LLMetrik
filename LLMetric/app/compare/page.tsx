"use client"

import { useState, useEffect, lazy, Suspense } from "react"
import Link from "next/link"
import { ArrowLeft, BarChart3, Zap, DollarSign, Clock, TrendingUp, Trophy, Shield, Cpu } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { ModelsService } from "@/lib/services"
import { ModelItem } from "@/lib/types"

// Lazy load edilecek bileşenler
const ModelSelector = lazy(() => import("@/components/compare/ModelSelector"))
const CompareMatrix = lazy(() => import("@/components/compare/CompareMatrix"))
const AdvantageCard = lazy(() => import("@/components/compare/AdvantageCard"))
const StickyCTA = lazy(() => import("@/components/compare/StickyCTA"))

// Loading skeleton
const ComparePageSkeleton = () => (
  <div className="min-h-screen bg-[#0c0c1d] text-white">
    <div className="container mx-auto px-4 py-8">
      <div className="h-8 bg-zinc-700/30 rounded w-1/4 mb-8 animate-pulse"></div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {[1, 2].map(i => (
          <div key={i} className="h-64 bg-gradient-to-br from-zinc-800/50 to-zinc-700/50 rounded-lg animate-pulse"></div>
        ))}
      </div>
      <div className="h-96 bg-gradient-to-br from-zinc-800/30 to-zinc-700/30 rounded-lg animate-pulse"></div>
    </div>
  </div>
)

// Renkler ana sayfa ile uyumlu: koyu zemin, mavi, mor, beyaz, gri
const COLORS = {
  background: "bg-[#0c0c1d]",
  card: "bg-gradient-to-br from-[#18182a] to-[#232347]",
  border: "border-[#2a2a40]",
  accent: "text-[#4e63ff]",
  accentBg: "bg-[#4e63ff]/10",
  white: "text-white",
  gray: "text-gray-400",
  blue: "text-blue-400",
  purple: "text-purple-400"
}

// Güncel Artificial Analysis verilerine göre benchmark verileri
const realBenchmarkData = {
  "o4-mini": {
    intelligence: 70,
    mmlu: 88.2,
    truthfulness: 94.5,
    reasoning: 91.2,
    coding: 87.8,
    math: 82.4,
    overall: 86.9,
    speed: 128.4,
    latency: 35.75,
    contextWindow: "200k"
  },
  "gemini-2-5-pro": {
    intelligence: 69,
    mmlu: 87.1,
    truthfulness: 93.8,
    reasoning: 90.4,
    coding: 86.2,
    math: 84.7,
    overall: 86.3,
    speed: 150.9,
    latency: 37.37,
    contextWindow: "1m"
  },
  "claude-3-5-sonnet": {
    intelligence: 67,
    mmlu: 88.7,
    truthfulness: 95.2,
    reasoning: 92.1,
    coding: 89.3,
    math: 76.8,
    overall: 88.4,
    speed: 85.2,
    latency: 28.94,
    contextWindow: "200k"
  },
  "gpt-4-turbo": {
    intelligence: 65,
    mmlu: 86.4,
    truthfulness: 91.7,
    reasoning: 88.9,
    coding: 84.1,
    math: 78.2,
    overall: 85.9,
    speed: 95.7,
    latency: 22.15,
    contextWindow: "128k"
  },
  "llama-3-1-405b": {
    intelligence: 64,
    mmlu: 87.3,
    truthfulness: 89.4,
    reasoning: 86.7,
    coding: 88.6,
    math: 80.1,
    overall: 86.4,
    speed: 42.3,
    latency: 45.28,
    contextWindow: "128k"
  },
  "gemini-1-5-pro": {
    intelligence: 63,
    mmlu: 85.9,
    truthfulness: 90.8,
    reasoning: 87.2,
    coding: 84.7,
    math: 82.6,
    overall: 86.2,
    speed: 118.3,
    latency: 19.44,
    contextWindow: "2m"
  },
  "mistral-large-2": {
    intelligence: 62,
    mmlu: 84.0,
    truthfulness: 88.9,
    reasoning: 85.3,
    coding: 91.2,
    math: 77.4,
    overall: 85.4,
    speed: 156.8,
    latency: 16.21,
    contextWindow: "128k"
  },
  "grok-3-mini": {
    intelligence: 61,
    mmlu: 81.7,
    truthfulness: 86.3,
    reasoning: 83.8,
    coding: 79.5,
    math: 75.9,
    overall: 81.4,
    speed: 62.3,
    latency: 0.32,
    contextWindow: "1m"
  }
}

// Güncel fiyatlandırma verileri (USD per 1M tokens)
const realPricingData = {
  "o4-mini": "$1.93",
  "gemini-2-5-pro": "$3.44",
  "claude-3-5-sonnet": "$3.00",
  "gpt-4-turbo": "$10.00",
  "llama-3-1-405b": "Free (Open Source)",
  "gemini-1-5-pro": "$3.50",
  "mistral-large-2": "$3.00",
  "grok-3-mini": "$0.35"
}

// Model provider bilgileri
const modelProviders = {
  "o4-mini": { name: "OpenAI", logo: "🤖", tier: "Premium", company: "OpenAI" },
  "gemini-2-5-pro": { name: "Gemini 2.5 Pro", logo: "🔮", tier: "Premium", company: "Google" },
  "claude-3-5-sonnet": { name: "Claude 3.5 Sonnet", logo: "🎭", tier: "Premium", company: "Anthropic" },
  "gpt-4-turbo": { name: "GPT-4 Turbo", logo: "⚡", tier: "Standard", company: "OpenAI" },
  "llama-3-1-405b": { name: "Llama 3.1 405B", logo: "🦙", tier: "Open Source", company: "Meta" },
  "gemini-1-5-pro": { name: "Gemini 1.5 Pro", logo: "💎", tier: "Standard", company: "Google" },
  "mistral-large-2": { name: "Mistral Large 2", logo: "🌪️", tier: "Standard", company: "Mistral AI" },
  "grok-3-mini": { name: "Grok 3 Mini", logo: "🚀", tier: "Beta", company: "xAI" }
}

export default function ComparePage() {
  const [availableModels, setAvailableModels] = useState<ModelItem[]>([])
  const [selectedModels, setSelectedModels] = useState<ModelItem[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchModels() {
      try {
        const models: ModelItem[] = await ModelsService.getAllModels()
        setAvailableModels(models)
        // Varsayılan olarak GPT-4 Turbo ve Claude 3.5 Sonnet karşılaştırmasını göster
        const defaultModel1 = models.find((m: ModelItem) => m.id.toLowerCase().includes('gpt-4-turbo'))
        const defaultModel2 = models.find((m: ModelItem) => m.id.toLowerCase().includes('claude-3-5-sonnet'))
        if (defaultModel1 && defaultModel2) {
          setSelectedModels([defaultModel1, defaultModel2])
        } else if (models.length >= 2) {
          setSelectedModels([models[0], models[1]])
        }
      } catch (error) {
        setSelectedModels([])
      } finally {
        setLoading(false)
      }
    }
    fetchModels()
  }, [])

  const handleModelChange = (idx: number, modelId: string) => {
    const model = availableModels.find(m => m.id === modelId)
    if (!model) return
    const updated = [...selectedModels]
    updated[idx] = model
    setSelectedModels(updated)
  }

  const getBenchmarkScore = (modelId: string, metric: string): number | string => {
    const normalizedId = modelId.toLowerCase().replace(/\s+/g, '-')
    const modelData = realBenchmarkData[normalizedId as keyof typeof realBenchmarkData]
    if (!modelData) return 0
    const value = modelData[metric as keyof typeof modelData]
    return value || 0
  }

  const calculateDifference = (score1: number | string, score2: number | string) => {
    const num1 = typeof score1 === 'string' ? 0 : score1
    const num2 = typeof score2 === 'string' ? 0 : score2
    if (num1 === 0 || num2 === 0) return 0
    return Math.round(((num1 - num2) / num2) * 100)
  }

  const metrics = [
    { key: "intelligence", label: "Zeka Endeksi", icon: <Trophy className="h-5 w-5 text-blue-400" /> },
    { key: "mmlu", label: "MMLU", icon: <BarChart3 className="h-5 w-5 text-purple-400" /> },
    { key: "truthfulness", label: "Doğruluk", icon: <Shield className="h-5 w-5 text-blue-400" /> },
    { key: "reasoning", label: "Muhakeme", icon: <Cpu className="h-5 w-5 text-purple-400" /> },
    { key: "coding", label: "Kodlama", icon: <Zap className="h-5 w-5 text-blue-400" /> },
    { key: "math", label: "Matematik", icon: <TrendingUp className="h-5 w-5 text-purple-400" /> }
  ]

  const performanceMetrics = [
    { key: "speed", label: "Hız", unit: "tokens/s", icon: <Zap className="h-5 w-5 text-blue-400" /> },
    { key: "latency", label: "Gecikme", unit: "sn", icon: <Clock className="h-5 w-5 text-purple-400" /> },
    { key: "contextWindow", label: "Context Window", unit: "", icon: <BarChart3 className="h-5 w-5 text-blue-400" /> }
  ]

  const model1 = selectedModels[0]
  const model2 = selectedModels[1]

  if (loading) {
    return (
      <ComparePageSkeleton />
    )
  }

  if (!model1 || !model2) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-[#0c0c1d] text-white">
        <div className="text-4xl mb-4">⚠️</div>
        <div className="text-xl mb-2">Model karşılaştırması için en az iki model seçilmelidir.</div>
        <Link href="/">
          <Button className="bg-blue-600 hover:bg-blue-700">Ana Sayfaya Dön</Button>
        </Link>
      </div>
    )
  }

  return (
    <div className="min-h-screen w-full bg-[#0c0c1d] text-white pb-24">{/* pb-24 sticky CTA için alan */}
      {/* Header */}
      <div className="w-full border-b border-[#2a2a40] bg-[#0c0c1d]/80 sticky top-0 z-30">
        <div className="container mx-auto flex items-center gap-4 py-4 px-4">
          <Link href="/" className="inline-flex items-center text-gray-400 hover:text-white transition-colors group">
            <ArrowLeft className="mr-2 h-4 w-4 group-hover:-translate-x-1 transition-transform" />
            Ana Sayfa
          </Link>
        </div>
      </div>

      {/* Model Seçim Kartları */}
      <div className="container mx-auto py-8 px-4">
        <div className="flex flex-col md:flex-row items-center justify-center gap-8 mb-8">
          <Suspense fallback={<div className="h-64 bg-gradient-to-br from-zinc-800/50 to-zinc-700/50 rounded-lg animate-pulse"></div>}>
            <ModelSelector
              models={availableModels}
              selectedModel={model1}
              providerMap={modelProviders}
              onChange={(id: string) => handleModelChange(0, id)}
            />
          </Suspense>
          <Suspense fallback={<div className="h-64 bg-gradient-to-br from-zinc-800/50 to-zinc-700/50 rounded-lg animate-pulse"></div>}>
            <ModelSelector
              models={availableModels}
              selectedModel={model2}
              providerMap={modelProviders}
              onChange={(id: string) => handleModelChange(1, id)}
            />
          </Suspense>
        </div>

        {/* Başlık ve Özet */}
        <div className="text-center mb-10">
          <h1 className="text-3xl md:text-4xl font-bold mb-2 text-white">{model1.title} <span className="text-blue-400">vs</span> {model2.title}</h1>
          <p className="text-gray-400 max-w-2xl mx-auto">Performans, fiyat ve teknik özellikler açısından kapsamlı karşılaştırma</p>
        </div>

        {/* Özellik Matrisi */}
        <div className="mb-10">
          <Suspense fallback={<div className="h-96 bg-gradient-to-br from-zinc-800/30 to-zinc-700/30 rounded-lg animate-pulse"></div>}>
            <CompareMatrix
              metrics={metrics}
              model1={model1}
              model2={model2}
              getScore={getBenchmarkScore}
              calculateDiff={calculateDifference}
            />
          </Suspense>
        </div>

        {/* Teknik Detay & Fiyat */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
          <Card className={`rounded-xl p-6 flex flex-col items-center border ${COLORS.card} ${COLORS.border}`}>
            <DollarSign className="h-6 w-6 text-blue-400 mb-2" />
            <div className="font-semibold text-lg mb-1 text-white">Fiyat (1M token)</div>
            <div className="flex items-center gap-4">
              <span className="text-xl font-bold text-blue-400">{realPricingData[model1.id.toLowerCase().replace(/\s+/g, '-') as keyof typeof realPricingData]}</span>
              <span className="text-gray-400">/</span>
              <span className="text-xl font-bold text-purple-400">{realPricingData[model2.id.toLowerCase().replace(/\s+/g, '-') as keyof typeof realPricingData]}</span>
            </div>
          </Card>
          {performanceMetrics.map(metric => {
            const value1 = getBenchmarkScore(model1.id, metric.key)
            const value2 = getBenchmarkScore(model2.id, metric.key)
            return (
              <Card key={metric.key} className={`rounded-xl p-6 flex flex-col items-center border ${COLORS.card} ${COLORS.border}`}>
                <div className="mb-2">{metric.icon}</div>
                <div className="font-semibold text-lg mb-1 text-white">{metric.label}</div>
                <div className="flex items-center gap-4">
                  <span className="text-xl font-bold text-blue-400">{typeof value1 === 'string' ? value1 : value1.toLocaleString()} {metric.unit}</span>
                  <span className="text-gray-400">/</span>
                  <span className="text-xl font-bold text-purple-400">{typeof value2 === 'string' ? value2 : value2.toLocaleString()} {metric.unit}</span>
                </div>
              </Card>
            )
          })}
        </div>

        {/* Avantaj Kartları */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
          <Suspense fallback={<div className="h-64 bg-gradient-to-br from-zinc-800/50 to-zinc-700/50 rounded-lg animate-pulse"></div>}>
            <AdvantageCard
              model={model1}
              otherModel={model2}
              metrics={metrics}
              getScore={getBenchmarkScore}
              calculateDiff={calculateDifference}
              realPricingData={realPricingData}
            />
          </Suspense>
          <Suspense fallback={<div className="h-64 bg-gradient-to-br from-zinc-800/50 to-zinc-700/50 rounded-lg animate-pulse"></div>}>
            <AdvantageCard
              model={model2}
              otherModel={model1}
              metrics={metrics}
              getScore={getBenchmarkScore}
              calculateDiff={calculateDifference}
              realPricingData={realPricingData}
            />
          </Suspense>
        </div>
      </div>

      {/* Sticky CTA */}
      <Suspense fallback={<div className="h-16 bg-gradient-to-r from-zinc-800/50 to-zinc-700/50 animate-pulse fixed bottom-0 w-full"></div>}>
        <StickyCTA
          price1={realPricingData[model1.id.toLowerCase().replace(/\s+/g, '-') as keyof typeof realPricingData]}
          price2={realPricingData[model2.id.toLowerCase().replace(/\s+/g, '-') as keyof typeof realPricingData]}
          model1Name={model1.title}
          model2Name={model2.title}
        />
      </Suspense>
    </div>
  )
} 
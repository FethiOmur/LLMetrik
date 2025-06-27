import { Card } from "@/components/ui/card"
import { ModelItem } from "@/lib/types"
import { ReactNode } from "react"

interface Metric {
  key: string
  label: string
}

interface AdvantageCardProps {
  model: ModelItem
  otherModel: ModelItem
  metrics: Metric[]
  getScore: (modelId: string, metricKey: string) => number | string
  calculateDiff: (score1: number | string, score2: number | string) => number
  realPricingData: Record<string, string>
}

export default function AdvantageCard({ model, otherModel, metrics, getScore, calculateDiff, realPricingData }: AdvantageCardProps) {
  const advantages: ReactNode[] = []
  metrics.forEach(metric => {
    const score1 = typeof getScore(model.id, metric.key) === "number" ? getScore(model.id, metric.key) as number : 0
    const score2 = typeof getScore(otherModel.id, metric.key) === "number" ? getScore(otherModel.id, metric.key) as number : 0
    const diff = calculateDiff(score1, score2)
    if (diff > 5) {
      advantages.push(<li key={metric.key}><span className="text-blue-400 font-semibold">+{diff}%</span> daha iyi {metric.label.toLowerCase()}</li>)
    }
  })

  return (
    <Card className="rounded-xl p-6 border bg-gradient-to-br from-[#18182a] to-[#232347] border-[#2a2a40] text-gray-300">
      <div className="font-bold text-lg mb-2 text-white">{model.title} Avantajları</div>
      <ul className="list-disc pl-5 space-y-2">
        {advantages.length > 0 ? advantages : <li>Dikkate değer belirgin avantaj bulunamadı.</li>}
        <li><span className="text-blue-400 font-semibold">Fiyat:</span> {realPricingData[model.id.toLowerCase().replace(/\\s+/g, '-') ]}</li>
      </ul>
    </Card>
  )
} 
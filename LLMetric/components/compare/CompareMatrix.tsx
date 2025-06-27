import { Card } from "@/components/ui/card"
import { ModelItem } from "@/lib/types"
import { ReactNode } from "react"

interface Metric {
  key: string
  label: string
  icon: ReactNode
  unit?: string
}

interface CompareMatrixProps {
  metrics: Metric[]
  model1: ModelItem
  model2: ModelItem
  getScore: (modelId: string, metricKey: string) => number | string
  calculateDiff: (score1: number | string, score2: number | string) => number
}

export default function CompareMatrix({ metrics, model1, model2, getScore, calculateDiff }: CompareMatrixProps) {
  return (
    <Card className="overflow-x-auto rounded-xl border bg-gradient-to-br from-[#18182a] to-[#232347] border-[#2a2a40]">
      <table className="min-w-full text-left text-sm text-white">
        <thead>
          <tr className="bg-[#1f1f33] text-gray-300">
            <th className="px-4 py-3">Özellik</th>
            <th className="px-4 py-3 text-center">{model1.title}</th>
            <th className="px-4 py-3 text-center">{model2.title}</th>
            <th className="px-4 py-3 text-center">Fark</th>
          </tr>
        </thead>
        <tbody>
          {metrics.map(metric => {
            const score1 = getScore(model1.id, metric.key)
            const score2 = getScore(model2.id, metric.key)
            const diff = calculateDiff(score1, score2)
            return (
              <tr key={metric.key} className="border-t border-[#2a2a40] hover:bg-[#20203a]">
                <td className="flex items-center gap-2 px-4 py-3">
                  {metric.icon}
                  <span>{metric.label}</span>
                </td>
                <td className="px-4 py-3 text-center font-semibold text-blue-400">
                  {typeof score1 === "string" ? score1 : score1.toLocaleString()} {metric.unit}
                </td>
                <td className="px-4 py-3 text-center font-semibold text-purple-400">
                  {typeof score2 === "string" ? score2 : score2.toLocaleString()} {metric.unit}
                </td>
                <td className="px-4 py-3 text-center">
                  <span className={diff > 0 ? "text-blue-400" : diff < 0 ? "text-purple-400" : "text-gray-400"}>
                    {diff > 0 ? "+" : ""}{diff}%
                  </span>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </Card>
  )
} 
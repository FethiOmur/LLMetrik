import { Card } from "@/components/ui/card"
import { ModelItem } from "@/lib/types"

interface ProviderInfo {
  logo: string
  company: string
}

interface ModelSelectorProps {
  models: ModelItem[]
  selectedModel: ModelItem
  providerMap: Record<string, ProviderInfo>
  onChange: (modelId: string) => void
}

export default function ModelSelector({ models, selectedModel, providerMap, onChange }: ModelSelectorProps) {
  const providerInfo = providerMap[selectedModel.id.toLowerCase().replace(/\s+/g, "-")]

  return (
    <Card className="w-full max-w-xs p-6 rounded-2xl shadow-lg border bg-gradient-to-br from-[#18182a] to-[#232347] border-[#2a2a40] flex flex-col items-center">
      <div className="text-5xl mb-2">{providerInfo?.logo ?? "🤖"}</div>
      <div className="font-bold text-xl mb-1 text-white">{selectedModel.title}</div>
      <div className="text-gray-400 text-sm mb-2">{providerInfo?.company ?? "Model Provider"}</div>
      <select
        className="w-full mt-2 bg-[#18182a] border border-[#2a2a40] rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        value={selectedModel.id}
        onChange={e => onChange(e.target.value)}
      >
        {models.map(m => (
          <option key={m.id} value={m.id}>{m.title}</option>
        ))}
      </select>
    </Card>
  )
} 
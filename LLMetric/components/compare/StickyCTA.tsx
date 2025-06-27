import { DollarSign } from "lucide-react"
import { Button } from "@/components/ui/button"

interface StickyCTAProps {
  price1: string
  price2: string
  model1Name: string
  model2Name: string
}

export default function StickyCTA({ price1, price2, model1Name, model2Name }: StickyCTAProps) {
  return (
    <div className="fixed bottom-0 left-0 right-0 bg-[#18182a]/80 backdrop-blur-md border-t border-[#2a2a40] py-3 px-4 flex flex-col md:flex-row items-center justify-between z-40">
      <div className="flex items-center gap-4 mb-2 md:mb-0 text-gray-200 text-sm">
        <DollarSign className="h-4 w-4 text-blue-400" />
        <span>{model1Name}: <strong className="text-white">{price1}</strong></span>
        <span className="hidden md:inline">|</span>
        <span>{model2Name}: <strong className="text-white">{price2}</strong></span>
      </div>
      <Button className="bg-blue-600 hover:bg-blue-700" size="sm">Model Seç</Button>
    </div>
  )
} 
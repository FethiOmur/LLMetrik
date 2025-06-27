export interface ModelItem {
  id: string;
  title: string;
  description: string;
  provider: string;
  image?: string;
  link: string;
}

export const popularModels: ModelItem[] = [
  {
    id: "gpt-4-turbo",
    title: "GPT-4 Turbo",
    description: "OpenAI'nin en yeni modeli ile yaratıcı ve doğru içerikler oluşturun. Geniş bellek penceresi ve zengin multimodal özellikler sunar.",
    provider: "OpenAI",
    image: "/models/gpt4.jpg",
    link: "/models/gpt-4-turbo"
  },
  {
    id: "claude-3-7-sonnet",
    title: "Claude 3.7 Sonnet",
    description: "Anthropic'in gelişmiş diyalog yeteneklerine sahip yapay zekası. Mükemmel doğallık, doğruluk ve etik özellikler.",
    provider: "Anthropic",
    image: "/models/claude.jpg",
    link: "/models/claude-3-7-sonnet"
  },
  {
    id: "llama-3-70b",
    title: "Llama 3 70B",
    description: "Meta'nın açık kaynak kodlu güçlü dil modeli. Tüm geliştiricilerin erişebileceği yüksek kaliteli yapay zeka deneyimi.",
    provider: "Meta",
    image: "/models/llama3.jpg",
    link: "/models/llama-3-70b"
  },
  {
    id: "gemini-1-5-pro",
    title: "Gemini 1.5 Pro",
    description: "Google'ın multimodal modeli ile metin, görüntü, kod ve ses arasında kusursuz geçiş yapın. Yüksek bağlam kapasitesi sunar.",
    provider: "Google",
    image: "/models/gemini.jpg",
    link: "/models/gemini-1-5-pro"
  },
  {
    id: "mistral-large",
    title: "Mistral Large",
    description: "Mistral AI'nin performans odaklı modeli. Etkileyici çıkarım hızı ve kodu anlama yetenekleriyle öne çıkar.",
    provider: "Mistral AI",
    image: "/models/mistral.jpg",
    link: "/models/mistral-large"
  },
  {
    id: "grok-3",
    title: "Grok 3",
    description: "xAI'ın güncel olaylar hakkında bilgi sahibi ve mizah anlayışı olan liderlik modeli. İnternet erişimi ile gerçek zamanlı bilgiler sunar.",
    provider: "xAI",
    image: "/models/grok.jpg",
    link: "/models/grok-3"
  }
] 
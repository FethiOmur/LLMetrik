import Link from 'next/link'
import Image from 'next/image'
import { Metadata, ResolvingMetadata } from 'next'
import { notFound } from 'next/navigation'
import { ArrowLeft, Calendar, Share2, Bookmark, MessageSquare } from 'lucide-react'

import { NewsService, ModelsService } from '@/lib/services'
import { formatDate } from '@/lib/utils'
import { GradientCard } from '@/components/ui/gradient-card'
import { StarBorder } from '@/components/ui/star-border'
import { NewsSummaryCard } from '@/components/NewsSummaryCard'

// Dinamik metadata için (Next.js 15 requires Promise)
type Props = {
  params: Promise<{ slug: string }>
}

export async function generateMetadata(
  { params }: Props,
  parent: ResolvingMetadata
): Promise<Metadata> {
  // Params promise'i resolve et
  const resolvedParams = await params
  // Haberi veritabanından fetch edelim
  const news = await NewsService.getNewsBySlug(resolvedParams.slug)

  // Haber bulunamadıysa 404
  if (!news) {
    return {
      title: 'News Not Found',
    }
  }

  return {
    title: `${news.title} | LLMetric`,
    description: news.summary,
    openGraph: {
      images: [news.image],
    },
  }
}

// Sayfanın ana bileşeni
export default async function NewsDetailPage({ params }: Props) {
  // Params promise'i resolve et
  const resolvedParams = await params
  // Haber slug'ı kullanarak haberi getir
  const newsItem = await NewsService.getNewsBySlug(resolvedParams.slug)

  // Haber bulunamadıysa 404
  if (!newsItem) {
    notFound()
  }

  // İlgili modelleri getir
  const relatedModels = await ModelsService.getRelatedModels(newsItem, 3)

  return (
    <div className="bg-black text-white min-h-screen">
      {/* Hero section */}
      <div className="relative h-[50vh] md:h-[60vh] overflow-hidden">
        {/* Background gradient */}
        <div className="absolute inset-0 bg-gradient-to-b from-transparent to-black z-10"></div>
        <div className="absolute inset-0 bg-gradient-to-r from-purple-900/30 to-blue-900/30 z-0"></div>
        
        {/* Model image (if available) */}
        {newsItem.image && (
          <div className="absolute inset-0 opacity-50">
            <Image 
              src={newsItem.image} 
              alt={newsItem.title} 
              fill 
              className="object-cover object-center"
              priority
            />
          </div>
        )}
        
        {/* Title and category info */}
        <div className="absolute bottom-0 left-0 right-0 p-8 z-20">
          <div className="container mx-auto max-w-4xl">
            <Link 
              href="/#news" 
              className="inline-flex items-center mb-6 text-zinc-300 hover:text-white transition-colors"
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              All News
            </Link>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-4">
              {newsItem.title}
            </h1>
            <div className="flex items-center text-zinc-300 gap-6">
              <span className="flex items-center">
                <Calendar className="mr-2 h-4 w-4" />
                {formatDate(newsItem.publishDate)}
              </span>
            </div>
          </div>
        </div>
      </div>
      
      {/* Haber Özeti Kartı */}
      <div className="container mx-auto max-w-4xl px-4">
        <NewsSummaryCard summary={newsItem.summary} />
      </div>
      
      {/* Content section */}
      <div className="container mx-auto max-w-4xl px-4 py-12">
        <div className="prose prose-invert prose-lg max-w-none">
          
          <h2>Technical Details</h2>
          <p className="text-justify">
            This advancement in LLM technology is seen as a significant step in the field of artificial intelligence. 
            Particularly, the model's {newsItem.title.includes('GPT') ? 'high parameter count' : 
            newsItem.title.includes('Claude') ? 'efficiency/performance balance' : 
            newsItem.title.includes('Llama') ? 'open source structure' : 
            newsItem.title.includes('Benchmark') ? 'various test results' : 
            newsItem.title.includes('Mistral') ? 'new investment support' : 'innovative approach'} 
            stands out among its notable features.
          </p>
          
          <h2>Industry Impact</h2>
          <p className="text-justify">
            The effects of this development in the AI ecosystem are already starting to be seen.
            Particularly, the developer community has begun testing the capabilities of the new model
            in different applications. In the coming months, this model is expected to find wider use cases.
          </p>
          
          <h2>Conclusion</h2>
          <p className="text-justify">
            This advancement in the LLM field once again proves the continuously evolving nature of artificial intelligence.
            As new models and approaches develop, the capabilities and applications of AI systems will continue to expand.
          </p>
          
          <div className="mt-12 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button className="p-2 rounded-full bg-zinc-800 hover:bg-zinc-700 transition-colors">
                <Share2 className="h-5 w-5" />
              </button>
              <button className="p-2 rounded-full bg-zinc-800 hover:bg-zinc-700 transition-colors">
                <Bookmark className="h-5 w-5" />
              </button>
              <button className="p-2 rounded-full bg-zinc-800 hover:bg-zinc-700 transition-colors">
                <MessageSquare className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
      
      {/* Related models */}
      <div className="container mx-auto max-w-7xl px-4 py-16">
        <h2 className="text-3xl font-bold mb-10 text-center">Explore More</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {relatedModels.map((model) => (
            <div key={model.id} className="h-96">
              <GradientCard
                title={model.title}
                description={model.description}
                link={model.link}
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  )
} 
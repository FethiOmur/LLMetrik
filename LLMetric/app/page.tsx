"use client"
import { lazy, Suspense } from "react"
import Header from "./components/Header"
import HeroSection from "./components/HeroSection"
import Footer from "./components/Footer"
import InteractiveBackground from "./components/InteractiveBackground"

// Lazy load edilecek büyük componentler
const ModelsComparisonSection = lazy(() => import("./components/ModelsComparisonSection"))
const NewsSection = lazy(() => import("./components/NewsSection"))
const SubscribeSection = lazy(() => import("./components/SubscribeSection"))

// Loading component
const SectionSkeleton = () => (
  <div className="w-full h-96 bg-gradient-to-r from-zinc-900/20 to-zinc-800/20 rounded-lg animate-pulse mb-8">
    <div className="p-8 space-y-4">
      <div className="h-8 bg-zinc-700/30 rounded w-1/3 mx-auto"></div>
      <div className="space-y-3">
        <div className="h-4 bg-zinc-700/20 rounded w-3/4 mx-auto"></div>
        <div className="h-4 bg-zinc-700/20 rounded w-1/2 mx-auto"></div>
      </div>
    </div>
  </div>
)

export default function Home() {
  return (
    <div className="min-h-screen text-white relative">
      <InteractiveBackground />
      <div className="relative z-10">
        <Header />
        <main className="container mx-auto px-4">
          <HeroSection />
          
          <Suspense fallback={<SectionSkeleton />}>
            <ModelsComparisonSection />
          </Suspense>
          
          <Suspense fallback={<SectionSkeleton />}>
            <NewsSection />
          </Suspense>
          
          <Suspense fallback={<SectionSkeleton />}>
            <SubscribeSection />
          </Suspense>
        </main>
        <Footer />
      </div>
    </div>
  )
}

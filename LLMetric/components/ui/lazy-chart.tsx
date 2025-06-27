"use client"

import { lazy, Suspense } from "react"

// Chart loading skeleton
const ChartSkeleton = () => (
  <div className="w-full h-64 bg-gradient-to-r from-zinc-800/30 to-zinc-700/30 rounded-lg animate-pulse flex items-center justify-center">
    <div className="text-zinc-400 text-sm">Loading chart...</div>
  </div>
)

// Pre-configured lazy chart components
export const LazyChartBar = lazy(() => 
  import("../chart-bar").then(m => ({ default: m.ChartBar }))
)

export const LazyChartPie = lazy(() => 
  import("../chart-pie").then(m => ({ default: m.ChartPie }))
)

// Lazy chart wrapper with Suspense
export function LazyChart({ children }: { children: React.ReactNode }) {
  return (
    <Suspense fallback={<ChartSkeleton />}>
      {children}
    </Suspense>
  )
}

export { ChartSkeleton } 
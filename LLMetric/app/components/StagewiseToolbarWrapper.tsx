"use client"

import React from "react"

// Stagewise Toolbar sadece geliştirme modunda yüklenir
export default function StagewiseToolbarWrapper() {
  const [isMounted, setIsMounted] = React.useState(false)

  React.useEffect(() => {
    setIsMounted(true)
  }, [])

  if (!isMounted) return null

  // Dinamik olarak import ediyoruz böylece sadece istemci tarafında çalışacak
  const StagewiseToolbar = require('@stagewise/toolbar-next').StagewiseToolbar
  const stagewiseConfig = { plugins: [] }

  return <StagewiseToolbar config={stagewiseConfig} />
} 
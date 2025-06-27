"use client"

import type React from "react"
import { useEffect, useRef, useState } from "react"

const InteractiveBackground: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [mouseHasMoved, setMouseHasMoved] = useState(false)
  const [isClient, setIsClient] = useState(false)

  // Ensure client-side only rendering
  useEffect(() => {
    setIsClient(true)
  }, [])

  useEffect(() => {
    if (!isClient) return // Don't run on server

    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext("2d")
    if (!ctx) return

    let animationFrameId: number
    // Başlangıçta mouse'u ekranın ortasına konumlandır
    let mouseX = window.innerWidth / 2
    let mouseY = window.innerHeight / 2

    const particles: Particle[] = []
    // Responsive particle count - mobile'da daha az, desktop'ta normal
    const particleCount = window.innerWidth < 768 ? 150 : 
                         window.innerWidth < 1200 ? 200 : 250

    class Particle {
      x: number = 0
      y: number = 0
      size: number = 0
      speedX: number = 0
      speedY: number = 0
      color: string = ""
      originalX: number = 0
      originalY: number = 0
      isVisible: boolean = true

      constructor() {
        if (!canvas) return
        
        // Parçacıkları görünür ekranın dışına da yerleştir
        // Ekranın 2 katı genişlikte ve yükseklikte bir alanda parçacıkları konumlandır
        const extendedWidth = canvas.width * 2
        const extendedHeight = canvas.height * 2
        
        this.x = Math.random() * extendedWidth - (extendedWidth - canvas.width) / 2
        this.y = Math.random() * extendedHeight - (extendedHeight - canvas.height) / 2
        
        this.originalX = this.x
        this.originalY = this.y
        this.size = Math.random() * 5 + 1
        
        // Hızı %40 azalttık
        this.speedX = (Math.random() * 3 - 1.5) * 0.6
        this.speedY = (Math.random() * 3 - 1.5) * 0.6
        
        this.color = `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 255, 0.7)`
        
        // Görünür ekranın içinde olup olmadığını kontrol et
        this.isVisible = (
          this.x >= 0 && 
          this.x <= canvas.width && 
          this.y >= 0 && 
          this.y <= canvas.height
        )
      }

      update() {
        if (!canvas) return
        
        // Performans: Date.now() çağrısını azalt
        const now = performance.now()
        
        if (mouseHasMoved) {
          // Fare hareket ettiğinde parçacıkları hareket ettir
          const mouseInfluenceX = (mouseX - canvas.width / 2) * 0.008
          const mouseInfluenceY = (mouseY - canvas.height / 2) * 0.008
          
          this.x += this.speedX + mouseInfluenceX
          this.y += this.speedY + mouseInfluenceY

          if (this.x < -canvas.width/2 || this.x > canvas.width*1.5) this.speedX *= -1
          if (this.y < -canvas.height/2 || this.y > canvas.height*1.5) this.speedY *= -1
        } else {
          // Fare hareket etmediğinde bile hafif bir hareket (optimized math)
          this.x += Math.sin(now * 0.001 + this.originalX * 0.01) * 0.15
          this.y += Math.cos(now * 0.002 + this.originalY * 0.01) * 0.15
        }
        
        // Parçacığın görünürlüğünü güncelle (expand visibility bounds for smoother transitions)
        this.isVisible = (
          this.x >= -50 && 
          this.x <= canvas.width + 50 && 
          this.y >= -50 && 
          this.y <= canvas.height + 50
        )
      }

      draw() {
        if (!ctx || !this.isVisible) return // Sadece görünür parçacıkları çiz
        ctx.fillStyle = this.color
        ctx.beginPath()
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2)
        ctx.fill()
      }
    }

    const init = () => {
      for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle())
      }
    }

    let lastTime = 0
    const targetFPS = 60
    const frameTime = 1000 / targetFPS

    const animate = (currentTime: number) => {
      if (!canvas || !ctx) return
      
      // FPS throttling - daha smooth animasyon
      if (currentTime - lastTime < frameTime) {
        animationFrameId = requestAnimationFrame(animate)
        return
      }
      lastTime = currentTime
      
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      
      // Sadece görünür parçacıkları güncelle (performans optimizasyonu)
      for (const particle of particles) {
        if (particle.isVisible || Math.abs(particle.x - canvas.width/2) < canvas.width) {
          particle.update()
          particle.draw()
        }
      }
      
      animationFrameId = requestAnimationFrame(animate)
    }

    const handleResize = () => {
      if (!canvas) return
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }

    const handleMouseMove = (event: MouseEvent) => {
      mouseX = event.clientX
      mouseY = event.clientY
      if (!mouseHasMoved) {
        setMouseHasMoved(true)
      }
    }

    handleResize()
    init()
    animate(0)

    window.addEventListener("resize", handleResize)
    window.addEventListener("mousemove", handleMouseMove)

    return () => {
      window.removeEventListener("resize", handleResize)
      window.removeEventListener("mousemove", handleMouseMove)
      cancelAnimationFrame(animationFrameId)
    }
  }, [mouseHasMoved, isClient])

  // Don't render canvas on server
  if (!isClient) {
    return <div className="fixed inset-0 w-full h-full -z-10" />
  }

  return <canvas ref={canvasRef} className="fixed inset-0 w-full h-full -z-10" />
}

export default InteractiveBackground

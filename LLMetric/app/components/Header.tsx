"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Menu, MenuItem, ProductItem, HoveredLink } from "@/components/ui/menu-components"

export default function Header() {
  const [isScrolled, setIsScrolled] = useState(false)
  const [active, setActive] = useState<string | null>(null)

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 0)
    }
    window.addEventListener("scroll", handleScroll)
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  return (
    <header className={`fixed w-full z-10 transition-all duration-300 ${isScrolled ? "bg-black" : "bg-transparent"}`}>
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link href="/" className="text-3xl font-bold tracking-tighter z-20">
          LLMetric
        </Link>

        <div className="flex-1 flex justify-center">
          <Menu setActive={setActive}>
            <MenuItem setActive={setActive} active={active} item="Models">
              <div className="grid grid-cols-1 gap-4 p-4 w-48">
                <HoveredLink href="#models">GPT Models</HoveredLink>
                <HoveredLink href="#models">Claude Models</HoveredLink>
                <HoveredLink href="#models">Llama Models</HoveredLink>
                <HoveredLink href="#models">Mistral Models</HoveredLink>
              </div>
            </MenuItem>
            <MenuItem setActive={setActive} active={active} item="Features">
              <div className="grid grid-cols-2 gap-10 p-4">
                <ProductItem
                  title="Model Comparison"
                  href="#"
                  src="/placeholder.svg?height=70&width=140"
                  description="Compare different LLMs side by side."
                />
                <ProductItem
                  title="Benchmark Tests"
                  href="#"
                  src="/placeholder.svg?height=70&width=140"
                  description="See how models perform on standard benchmarks."
                />
                <ProductItem
                  title="Cost Analysis"
                  href="#"
                  src="/placeholder.svg?height=70&width=140"
                  description="Calculate and compare costs across providers."
                />
                <ProductItem
                  title="API Integration"
                  href="#"
                  src="/placeholder.svg?height=70&width=140"
                  description="Easily integrate with your existing applications."
                />
              </div>
            </MenuItem>
            <MenuItem setActive={setActive} active={active} item="News">
              <div className="grid grid-cols-1 gap-4 p-4 w-48">
                <HoveredLink href="#news">Latest Updates</HoveredLink>
                <HoveredLink href="#news">Research Papers</HoveredLink>
                <HoveredLink href="#news">Model Releases</HoveredLink>
                <HoveredLink href="#news">Industry Trends</HoveredLink>
              </div>
            </MenuItem>
            <MenuItem setActive={setActive} active={active} item="Subscribe">
              <div className="p-4 w-64">
                <h3 className="text-lg font-medium mb-2 text-white">Join our newsletter</h3>
                <p className="text-sm text-neutral-300 mb-3">
                  Get the latest LLM news and updates delivered to your inbox.
                </p>
                <form className="space-y-2">
                  <input
                    type="email"
                    placeholder="Enter your email"
                    className="w-full px-3 py-2 text-sm rounded-md bg-black/50 border border-white/20 text-white"
                  />
                  <button
                    type="submit"
                    className="w-full bg-white text-black hover:bg-white/90 px-3 py-2 text-sm font-medium rounded-md transition-colors"
                  >
                    Subscribe
                  </button>
                </form>
              </div>
            </MenuItem>
          </Menu>
        </div>

        <Button asChild variant="outline" className="hidden md:block z-20">
          <a href="https://huggingface.co/models" target="_blank" rel="noopener noreferrer">
            Hugging Face
          </a>
        </Button>
      </div>
    </header>
  )
}

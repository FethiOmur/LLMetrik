"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { motion } from "framer-motion"
import Link from "next/link"
import Image from "next/image"

const transition = {
  type: "spring",
  mass: 0.5,
  damping: 11.5,
  stiffness: 100,
  restDelta: 0.001,
  restSpeed: 0.001,
}

export const MenuItem = ({
  setActive,
  active,
  item,
  children,
}: {
  setActive: (item: string | null) => void
  active: string | null
  item: string
  children?: React.ReactNode
}) => {
  return (
    <div onMouseEnter={() => setActive(item)} className="relative">
      <motion.p
        transition={{ duration: 0.3 }}
        className="cursor-pointer text-white hover:opacity-[0.9] dark:text-white"
      >
        {item}
      </motion.p>
      {active !== null && (
        <motion.div
          initial={{ opacity: 0, scale: 0.85, y: 10 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          transition={transition}
        >
          {active === item && (
            <div className="absolute top-[calc(100%+1.7rem)] left-1/2 transform -translate-x-1/2 z-50">
              <motion.div
                transition={transition}
                layoutId="active" // layoutId ensures smooth animation
                className="bg-black backdrop-blur-sm rounded-2xl overflow-hidden border border-white/[0.2] shadow-xl"
              >
                <div className="w-max h-full p-4">{children}</div>
              </motion.div>
            </div>
          )}
        </motion.div>
      )}
    </div>
  )
}

export const Menu = ({
  setActive,
  children,
}: {
  setActive: (item: string | null) => void
  children: React.ReactNode
}) => {
  const [hovering, setHovering] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleMouseLeave = () => {
      setActive(null)
      setHovering(false)
    }

    const menuEl = menuRef.current
    if (menuEl) {
      menuEl.addEventListener("mouseleave", handleMouseLeave)
      return () => {
        menuEl.removeEventListener("mouseleave", handleMouseLeave)
      }
    }
  }, [setActive])

  return (
    <nav
      ref={menuRef}
      onMouseEnter={() => setHovering(true)}
      className="relative rounded-full border border-white/[0.2] bg-black/50 backdrop-blur-md z-50"
    >
      <div className="px-8 py-4 flex gap-6 items-center justify-center">{children}</div>
    </nav>
  )
}

export const HoveredLink = ({ children, ...rest }: any) => {
  return (
    <Link {...rest} className="text-white hover:text-purple-300 transition duration-200">
      {children}
    </Link>
  )
}

export const ProductItem = ({
  title,
  description,
  href,
  src,
}: {
  title: string
  description: string
  href: string
  src: string
}) => {
  return (
    <Link href={href} className="flex flex-col gap-2 group">
      <div className="relative overflow-hidden rounded-xl">
        <div className="h-36 w-full overflow-hidden rounded-xl border border-white/[0.2]">
          <Image
            src={src || "/placeholder.svg"}
            alt={title}
            width={200}
            height={100}
            className="h-full w-full object-cover group-hover:scale-105 transition duration-300"
          />
        </div>
      </div>
      <div className="flex flex-col gap-1">
        <p className="text-white font-medium">{title}</p>
        <p className="text-sm text-zinc-400">{description}</p>
      </div>
    </Link>
  )
}

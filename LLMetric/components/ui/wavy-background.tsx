"use client"

import type React from "react"

import { useEffect, useRef, useState } from "react"
import { cn } from "@/lib/utils"

export function WavyBackground({
  children,
  className,
  containerClassName,
  colors = ["#2563eb", "#4f46e5", "#8b5cf6", "#a855f7"],
  waveWidth = 50,
  backgroundFill = "black",
  blur = 10,
  speed = "fast",
  waveOpacity = 0.5,
  ...props
}: {
  children?: React.ReactNode
  className?: string
  containerClassName?: string
  colors?: string[]
  waveWidth?: number
  backgroundFill?: string
  blur?: number
  speed?: "slow" | "fast"
  waveOpacity?: number
  [key: string]: any
}) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [containerSize, setContainerSize] = useState<{
    width: number
    height: number
  }>({
    width: 0,
    height: 0,
  })

  useEffect(() => {
    if (containerRef.current) {
      const { width, height } = containerRef.current.getBoundingClientRect()
      setContainerSize({
        width,
        height,
      })
    }
  }, [])

  const speedValue = speed === "fast" ? 1 : 3

  return (
    <div
      ref={containerRef}
      className={cn("relative flex flex-col items-center justify-center overflow-hidden", containerClassName)}
    >
      <svg
        className="absolute inset-0 z-0"
        width={containerSize.width}
        height={containerSize.height}
        viewBox={`0 0 ${containerSize.width} ${containerSize.height}`}
        preserveAspectRatio="none"
        {...props}
      >
        <defs>
          <filter id="blur">
            <feGaussianBlur in="SourceGraphic" stdDeviation={blur} />
          </filter>
        </defs>
        <rect x="0" y="0" width={containerSize.width} height={containerSize.height} fill={backgroundFill} />
        {colors.map((color, i) => (
          <g key={i} filter="url(#blur)">
            <path
              d={`M0 ${containerSize.height * 0.5} C ${waveWidth} ${
                containerSize.height * 0.5 + 20 * Math.sin(i)
              }, ${2 * waveWidth} ${
                containerSize.height * 0.5 - 20 * Math.sin(i)
              }, ${3 * waveWidth} ${containerSize.height * 0.5} S ${
                4 * waveWidth
              } ${containerSize.height * 0.5 + 20 * Math.sin(i)}, ${
                5 * waveWidth
              } ${containerSize.height * 0.5} S ${6 * waveWidth} ${
                containerSize.height * 0.5 - 20 * Math.sin(i)
              }, ${7 * waveWidth} ${containerSize.height * 0.5} S ${
                8 * waveWidth
              } ${containerSize.height * 0.5 + 20 * Math.sin(i)}, ${
                9 * waveWidth
              } ${containerSize.height * 0.5} S ${10 * waveWidth} ${
                containerSize.height * 0.5 - 20 * Math.sin(i)
              }, ${11 * waveWidth} ${containerSize.height * 0.5} S ${
                12 * waveWidth
              } ${containerSize.height * 0.5 + 20 * Math.sin(i)}, ${
                13 * waveWidth
              } ${containerSize.height * 0.5} S ${14 * waveWidth} ${
                containerSize.height * 0.5 - 20 * Math.sin(i)
              }, ${15 * waveWidth} ${containerSize.height * 0.5} S ${
                16 * waveWidth
              } ${containerSize.height * 0.5 + 20 * Math.sin(i)}, ${
                17 * waveWidth
              } ${containerSize.height * 0.5} S ${18 * waveWidth} ${
                containerSize.height * 0.5 - 20 * Math.sin(i)
              }, ${19 * waveWidth} ${containerSize.height * 0.5} S ${
                20 * waveWidth
              } ${containerSize.height * 0.5 + 20 * Math.sin(i)}, ${21 * waveWidth} ${containerSize.height * 0.5}`}
              fill="none"
              stroke={color}
              strokeWidth="2"
              strokeOpacity={waveOpacity}
            >
              <animate
                attributeName="d"
                dur={`${speedValue * (i + 1)}s`}
                repeatCount="indefinite"
                values={`M0 ${containerSize.height * 0.5} C ${waveWidth} ${
                  containerSize.height * 0.5 + 20 * Math.sin(i)
                }, ${2 * waveWidth} ${
                  containerSize.height * 0.5 - 20 * Math.sin(i)
                }, ${3 * waveWidth} ${containerSize.height * 0.5} S ${
                  4 * waveWidth
                } ${containerSize.height * 0.5 + 20 * Math.sin(i)}, ${
                  5 * waveWidth
                } ${containerSize.height * 0.5} S ${6 * waveWidth} ${
                  containerSize.height * 0.5 - 20 * Math.sin(i)
                }, ${7 * waveWidth} ${containerSize.height * 0.5} S ${
                  8 * waveWidth
                } ${containerSize.height * 0.5 + 20 * Math.sin(i)}, ${
                  9 * waveWidth
                } ${containerSize.height * 0.5} S ${10 * waveWidth} ${
                  containerSize.height * 0.5 - 20 * Math.sin(i)
                }, ${11 * waveWidth} ${containerSize.height * 0.5} S ${
                  12 * waveWidth
                } ${containerSize.height * 0.5 + 20 * Math.sin(i)}, ${
                  13 * waveWidth
                } ${containerSize.height * 0.5} S ${14 * waveWidth} ${
                  containerSize.height * 0.5 - 20 * Math.sin(i)
                }, ${15 * waveWidth} ${containerSize.height * 0.5} S ${
                  16 * waveWidth
                } ${containerSize.height * 0.5 + 20 * Math.sin(i)}, ${
                  17 * waveWidth
                } ${containerSize.height * 0.5} S ${18 * waveWidth} ${
                  containerSize.height * 0.5 - 20 * Math.sin(i)
                }, ${19 * waveWidth} ${containerSize.height * 0.5} S ${
                  20 * waveWidth
                } ${containerSize.height * 0.5 + 20 * Math.sin(i)}, ${21 * waveWidth} ${containerSize.height * 0.5};
                
                M0 ${containerSize.height * 0.5} C ${waveWidth} ${
                  containerSize.height * 0.5 - 20 * Math.sin(i)
                }, ${2 * waveWidth} ${
                  containerSize.height * 0.5 + 20 * Math.sin(i)
                }, ${3 * waveWidth} ${containerSize.height * 0.5} S ${
                  4 * waveWidth
                } ${containerSize.height * 0.5 - 20 * Math.sin(i)}, ${
                  5 * waveWidth
                } ${containerSize.height * 0.5} S ${6 * waveWidth} ${
                  containerSize.height * 0.5 + 20 * Math.sin(i)
                }, ${7 * waveWidth} ${containerSize.height * 0.5} S ${
                  8 * waveWidth
                } ${containerSize.height * 0.5 - 20 * Math.sin(i)}, ${
                  9 * waveWidth
                } ${containerSize.height * 0.5} S ${10 * waveWidth} ${
                  containerSize.height * 0.5 + 20 * Math.sin(i)
                }, ${11 * waveWidth} ${containerSize.height * 0.5} S ${
                  12 * waveWidth
                } ${containerSize.height * 0.5 - 20 * Math.sin(i)}, ${
                  13 * waveWidth
                } ${containerSize.height * 0.5} S ${14 * waveWidth} ${
                  containerSize.height * 0.5 + 20 * Math.sin(i)
                }, ${15 * waveWidth} ${containerSize.height * 0.5} S ${
                  16 * waveWidth
                } ${containerSize.height * 0.5 - 20 * Math.sin(i)}, ${
                  17 * waveWidth
                } ${containerSize.height * 0.5} S ${18 * waveWidth} ${
                  containerSize.height * 0.5 + 20 * Math.sin(i)
                }, ${19 * waveWidth} ${containerSize.height * 0.5} S ${
                  20 * waveWidth
                } ${containerSize.height * 0.5 - 20 * Math.sin(i)}, ${21 * waveWidth} ${containerSize.height * 0.5}`}
              />
            </path>
          </g>
        ))}
      </svg>
      <div className={cn("relative z-10", className)}>{children}</div>
    </div>
  )
}

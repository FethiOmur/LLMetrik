"use client";

import React, { useRef, useState } from "react";
import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

interface NewsSummaryCardProps {
  summary: string;
  title?: string;
}

export function NewsSummaryCard({ summary, title }: NewsSummaryCardProps) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [isHovered, setIsHovered] = useState(false);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [rotation, setRotation] = useState({ x: 0, y: 0 });

  // Fare hareketi için 3D efekti
  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (cardRef.current) {
      const rect = cardRef.current.getBoundingClientRect();

      // Kartın merkezine göre fare pozisyonunu hesapla
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;

      setMousePosition({ x, y });

      // Hafif bir 3D rotasyon etkisi
      const rotateX = -(y / rect.height) * 5; // Maksimum 5 derece rotasyon
      const rotateY = (x / rect.width) * 5; // Maksimum 5 derece rotasyon

      setRotation({ x: rotateX, y: rotateY });
    }
  };

  // Fare karttan ayrıldığında rotasyonu sıfırla
  const handleMouseLeave = () => {
    setIsHovered(false);
    setRotation({ x: 0, y: 0 });
  };

  return (
    <div className="relative my-8 md:my-10 xl:my-12 overflow-hidden rounded-[32px] w-full">
      {/* Kart konteyner */}
      <motion.div
        ref={cardRef}
        className="relative rounded-[32px] overflow-hidden"
        style={{
          transformStyle: "preserve-3d",
          backgroundColor: "#0e131f",
          boxShadow: "0 -10px 100px 10px rgba(78, 99, 255, 0.25), 0 0 10px 0 rgba(0, 0, 0, 0.5)",
        }}
        initial={{ y: 0 }}
        animate={{
          y: isHovered ? -5 : 0,
          rotateX: rotation.x,
          rotateY: rotation.y,
          perspective: 1000,
        }}
        transition={{
          type: "spring",
          stiffness: 300,
          damping: 20
        }}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={handleMouseLeave}
        onMouseMove={handleMouseMove}
      >
        {/* Cam yansıma efekti */}
        <motion.div
          className="absolute inset-0 z-35 pointer-events-none"
          style={{
            background: "linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0) 40%, rgba(255,255,255,0) 80%, rgba(255,255,255,0.05) 100%)",
            backdropFilter: "blur(2px)",
          }}
          animate={{
            opacity: isHovered ? 0.7 : 0.5,
            rotateX: -rotation.x * 0.2,
            rotateY: -rotation.y * 0.2,
            z: 1,
          }}
          transition={{
            duration: 0.4,
            ease: "easeOut"
          }}
        />

        {/* Koyu arka plan */}
        <motion.div
          className="absolute inset-0 z-0"
          style={{
            background: "linear-gradient(180deg, #000000 0%, #000000 70%)",
          }}
          animate={{
            z: -1
          }}
        />

        {/* Gürültü efekti */}
        <motion.div
          className="absolute inset-0 opacity-30 mix-blend-overlay z-10"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='5' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
          }}
          animate={{
            z: -0.5
          }}
        />

        {/* Mor/mavi parıltı efekti */}
        <motion.div
          className="absolute bottom-0 left-0 right-0 h-2/3 z-20"
          style={{
            background: `
              radial-gradient(ellipse at bottom right, rgba(172, 92, 255, 0.7) -10%, rgba(79, 70, 229, 0) 70%),
              radial-gradient(ellipse at bottom left, rgba(56, 189, 248, 0.7) -10%, rgba(79, 70, 229, 0) 70%)
            `,
            filter: "blur(40px)",
          }}
          animate={{
            opacity: isHovered ? 0.9 : 0.8,
            y: isHovered ? rotation.x * 0.5 : 0,
            z: 0
          }}
          transition={{
            duration: 0.4,
            ease: "easeOut"
          }}
        />

        {/* Merkezi mor parıltı */}
        <motion.div
          className="absolute bottom-0 left-0 right-0 h-2/3 z-21"
          style={{
            background: `
              radial-gradient(circle at bottom center, rgba(161, 58, 229, 0.7) -20%, rgba(79, 70, 229, 0) 60%)
            `,
            filter: "blur(45px)",
          }}
          animate={{
            opacity: isHovered ? 0.85 : 0.75,
            y: isHovered ? `calc(10% + ${rotation.x * 0.3}px)` : "10%",
            z: 0
          }}
          transition={{
            duration: 0.4,
            ease: "easeOut"
          }}
        />

        {/* Alt kenar parıltısı */}
        <motion.div
          className="absolute bottom-0 left-0 right-0 h-[2px] z-25"
          style={{
            background: "linear-gradient(90deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.7) 50%, rgba(255, 255, 255, 0.05) 100%)",
          }}
          animate={{
            boxShadow: isHovered
              ? "0 0 20px 4px rgba(172, 92, 255, 0.9), 0 0 30px 6px rgba(138, 58, 185, 0.7), 0 0 40px 8px rgba(56, 189, 248, 0.5)"
              : "0 0 15px 3px rgba(172, 92, 255, 0.8), 0 0 25px 5px rgba(138, 58, 185, 0.6), 0 0 35px 7px rgba(56, 189, 248, 0.4)",
            opacity: isHovered ? 1 : 0.9,
            z: 0.5
          }}
          transition={{
            duration: 0.4,
            ease: "easeOut"
          }}
        />

        {/* Kart içeriği */}
        <motion.div
          className="relative flex flex-col h-full p-8 z-40"
          animate={{
            z: 2
          }}
        >
          {/* İkon dairesi */}
          <motion.div
            className="w-12 h-12 rounded-full flex items-center justify-center mb-6"
            style={{
              background: "linear-gradient(225deg, #171c2c 0%, #121624 100%)",
              position: "relative",
              overflow: "hidden"
            }}
            initial={{ filter: "blur(3px)", opacity: 0.7 }}
            animate={{
              filter: "blur(0px)",
              opacity: 1,
              boxShadow: isHovered
                ? "0 8px 16px -2px rgba(0, 0, 0, 0.3), 0 4px 8px -1px rgba(0, 0, 0, 0.2), inset 2px 2px 5px rgba(255, 255, 255, 0.15), inset -2px -2px 5px rgba(0, 0, 0, 0.7)"
                : "0 6px 12px -2px rgba(0, 0, 0, 0.25), 0 3px 6px -1px rgba(0, 0, 0, 0.15), inset 1px 1px 3px rgba(255, 255, 255, 0.12), inset -2px -2px 4px rgba(0, 0, 0, 0.5)",
              z: isHovered ? 10 : 5,
              y: isHovered ? -2 : 0,
              rotateX: isHovered ? -rotation.x * 0.5 : 0,
              rotateY: isHovered ? -rotation.y * 0.5 : 0
            }}
            transition={{
              duration: 0.4,
              ease: "easeOut"
            }}
          >
            {/* İkon vurgusu */}
            <div
              className="absolute top-0 left-0 w-2/3 h-2/3 opacity-40"
              style={{
                background: "radial-gradient(circle at top left, rgba(255, 255, 255, 0.5), transparent 80%)",
                pointerEvents: "none",
                filter: "blur(10px)"
              }}
            />

            {/* Yıldız ikonu */}
            <div className="flex items-center justify-center w-full h-full relative z-10">
              <svg width="20" height="20" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M8 0L9.4 5.4L14.8 5.4L10.6 8.8L12 14.2L8 10.8L4 14.2L5.4 8.8L1.2 5.4L6.6 5.4L8 0Z"
                  fill="white"
                />
              </svg>
            </div>
          </motion.div>

          {/* İçerik */}
          <motion.div
            className="mb-auto"
            animate={{
              z: isHovered ? 5 : 2,
              rotateX: isHovered ? -rotation.x * 0.3 : 0,
              rotateY: isHovered ? -rotation.y * 0.3 : 0
            }}
            transition={{
              duration: 0.4,
              ease: "easeOut"
            }}
          >
            <motion.h3
              className="text-2xl font-medium text-white mb-3 font-sans tracking-tight"
              style={{
                letterSpacing: "-0.01em",
                lineHeight: 1.2,
              }}
              initial={{ filter: "blur(3px)", opacity: 0.7 }}
              animate={{
                textShadow: isHovered ? "0 2px 4px rgba(0,0,0,0.2)" : "none",
                filter: "blur(0px)",
                opacity: 1,
                transition: { duration: 1.2, delay: 0.2 }
              }}
            >
              {title || "Haber Özeti"}
            </motion.h3>

            <motion.p
              className="text-sm mb-6 text-white font-sans"
              style={{
                lineHeight: 1.6,
                fontWeight: 350,
              }}
              initial={{ filter: "blur(3px)", opacity: 0.7 }}
              animate={{
                textShadow: isHovered ? "0 1px 2px rgba(0,0,0,0.1)" : "none",
                filter: "blur(0px)",
                opacity: 1,
                transition: { duration: 1.2, delay: 0.4 }
              }}
            >
              {summary}
            </motion.p>
          </motion.div>
        </motion.div>
      </motion.div>
    </div>
  );
} 
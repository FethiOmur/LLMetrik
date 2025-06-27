"use client"

import { useEffect, useState, useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { GradientCard } from "@/components/ui/gradient-card";
import { TestimonialsSectionDemo } from "./TestimonialsSectionDemo";
import { NewsService } from "@/lib/services";
import { NewsItem } from "@/lib/types";
import { slugify } from "@/lib/utils";

export default function NewsSection() {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);
  const sectionRef = useRef<HTMLDivElement>(null);

  // Scroll-based opacity for fading in when scrolling down
  const { scrollYProgress: scrollInProgress } = useScroll({
    target: sectionRef,
    offset: ["start end", "center center"],
  });

  // Transform scrollYProgress to opacity (0 before it's visible, 1 as it scrolls into view)
  const opacityIn = useTransform(scrollInProgress, [0, 0.5], [0, 1]);
  
  // Scroll-based opacity for fading out when scrolling down
  const { scrollYProgress: scrollOutProgress } = useScroll({
    target: sectionRef,
    offset: ["start start", "end start"],
  });

  // Transform scrollYProgress to opacity (1 at the start, 0.3 as it scrolls out of view)
  const opacityOut = useTransform(scrollOutProgress, [0, 1], [1, 0.3]);

  // Combine both effects
  const opacity = {
    opacity: opacityIn,
    // Apply second opacity effect as the section leaves the viewport
    opacity2: opacityOut,
  };

  useEffect(() => {
    async function fetchNews() {
      try {
        // Servis üzerinden en son haberleri getir
        const latestNews = await NewsService.getLatestNews(4);
        setNews(latestNews);
      } catch (error) {
        console.error("Error fetching news:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchNews();
  }, []);

  return (
    <motion.section 
      ref={sectionRef}
      style={{ opacity: opacity.opacity2 }}
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      id="news" 
      className="py-24 relative overflow-hidden bg-gradient-to-b from-black to-zinc-900"
    >
      <div className="absolute inset-0 bg-grid-pattern opacity-10"></div>

      <div className="container mx-auto px-4 relative">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">Latest LLM News</h2>
          <p className="text-xl text-zinc-400 max-w-3xl mx-auto">
            Stay updated with the most recent developments in the world of Large Language Models
          </p>
        </div>

        <TestimonialsSectionDemo />

        {loading ? (
          <div className="flex justify-center items-center h-96">
            <div className="w-12 h-12 border-4 border-t-transparent border-zinc-500 rounded-full animate-spin"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mt-16">
            {news.map((item, index) => (
              <div key={item.id || index} className="h-96">
                <GradientCard 
                  title={item.title} 
                  description={item.summary}
                  link={`/news/${item.slug || slugify(item.title)}`}
                />
              </div>
            ))}
          </div>
        )}
      </div>
    </motion.section>
  );
} 
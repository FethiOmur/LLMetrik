"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"

// Example data - In a real project, this could come from an API or JSON file
const benchmarkData = {
  mmlu: [
    { model: "GPT-4", score: 86.4, category: "Reasoning" },
    { model: "Claude 3 Opus", score: 85.2, category: "Reasoning" },
    { model: "Llama 3 70B", score: 78.9, category: "Reasoning" },
    { model: "Mistral Large", score: 81.2, category: "Reasoning" },
    { model: "Gemini 1.5 Pro", score: 83.7, category: "Reasoning" },
  ],
  truthfulqa: [
    { model: "GPT-4", score: 68.3, category: "Truthfulness" },
    { model: "Claude 3 Opus", score: 71.5, category: "Truthfulness" },
    { model: "Llama 3 70B", score: 63.2, category: "Truthfulness" },
    { model: "Mistral Large", score: 65.8, category: "Truthfulness" },
    { model: "Gemini 1.5 Pro", score: 67.1, category: "Truthfulness" },
  ],
  gsm8k: [
    { model: "GPT-4", score: 96.2, category: "Math" },
    { model: "Claude 3 Opus", score: 92.7, category: "Math" },
    { model: "Llama 3 70B", score: 88.4, category: "Math" },
    { model: "Mistral Large", score: 87.9, category: "Math" },
    { model: "Gemini 1.5 Pro", score: 91.3, category: "Math" },
  ],
  hellaswag: [
    { model: "GPT-4", score: 89.5, category: "Commonsense" },
    { model: "Claude 3 Opus", score: 88.2, category: "Commonsense" },
    { model: "Llama 3 70B", score: 85.6, category: "Commonsense" },
    { model: "Mistral Large", score: 84.3, category: "Commonsense" },
    { model: "Gemini 1.5 Pro", score: 87.8, category: "Commonsense" },
  ],
};

const benchmarkInfo = {
  mmlu: {
    title: "MMLU",
    description: "Massive Multitask Language Understanding, measures model performance across 57 subjects",
  },
  truthfulqa: {
    title: "TruthfulQA",
    description: "Tests the model's ability to generate truthful answers to questions",
  },
  gsm8k: {
    title: "GSM8K",
    description: "Grade School Math 8K, tests mathematical problem-solving abilities",
  },
  hellaswag: {
    title: "HellaSwag",
    description: "Tests commonsense natural language inference capabilities",
  },
};

export default function BenchmarksSection() {
  const [selectedBenchmark, setSelectedBenchmark] = useState("mmlu");
  const [sortOrder, setSortOrder] = useState("descending");

  // Get the selected benchmark data and sort
  const currentData = [...benchmarkData[selectedBenchmark as keyof typeof benchmarkData]].sort((a, b) => {
    return sortOrder === "descending" ? b.score - a.score : a.score - b.score;
  });

  // Find maximum score (for % display)
  const maxScore = Math.max(...currentData.map(item => item.score));

  return (
    <motion.section
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="py-24"
      id="benchmarks"
    >
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">Benchmark Results</h2>
          <p className="text-xl text-zinc-400 max-w-3xl mx-auto">
            Compare the performance of different LLM models in standard benchmark tests.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-8">
          <div className="bg-zinc-900/50 backdrop-blur-md border border-white/10 rounded-xl p-6">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
              <div>
                <h3 className="text-2xl font-bold mb-1">{benchmarkInfo[selectedBenchmark as keyof typeof benchmarkInfo].title}</h3>
                <p className="text-zinc-400">
                  {benchmarkInfo[selectedBenchmark as keyof typeof benchmarkInfo].description}
                </p>
              </div>
              <div className="flex flex-col sm:flex-row gap-4">
                <Tabs defaultValue={selectedBenchmark} onValueChange={setSelectedBenchmark} className="w-full sm:w-auto">
                  <TabsList className="bg-zinc-800/50 p-1 rounded-full w-full sm:w-auto">
                    <TabsTrigger value="mmlu" className="rounded-full text-xs">
                      MMLU
                    </TabsTrigger>
                    <TabsTrigger value="truthfulqa" className="rounded-full text-xs">
                      TruthfulQA
                    </TabsTrigger>
                    <TabsTrigger value="gsm8k" className="rounded-full text-xs">
                      GSM8K
                    </TabsTrigger>
                    <TabsTrigger value="hellaswag" className="rounded-full text-xs">
                      HellaSwag
                    </TabsTrigger>
                  </TabsList>
                </Tabs>
                <Select defaultValue={sortOrder} onValueChange={setSortOrder}>
                  <SelectTrigger className="bg-zinc-800/50 border-white/10 w-full sm:w-[150px]">
                    <SelectValue placeholder="Sort" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="descending">Highest</SelectItem>
                    <SelectItem value="ascending">Lowest</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="overflow-x-auto">
              <Table>
                <TableCaption>
                  Note: This data is based on open-source benchmark results.
                </TableCaption>
                <TableHeader>
                  <TableRow className="hover:bg-zinc-800/50">
                    <TableHead className="w-[100px]">Rank</TableHead>
                    <TableHead>Model</TableHead>
                    <TableHead>Category</TableHead>
                    <TableHead className="text-right">Score (%)</TableHead>
                    <TableHead className="text-right">Performance</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {currentData.map((item, index) => (
                    <TableRow key={item.model} className="hover:bg-zinc-800/50 border-white/5">
                      <TableCell className="font-medium">#{index + 1}</TableCell>
                      <TableCell className="font-medium">{item.model}</TableCell>
                      <TableCell>
                        <Badge variant="outline" className="bg-zinc-800/50">
                          {item.category}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-right">{item.score.toFixed(1)}%</TableCell>
                      <TableCell className="text-right">
                        <div className="flex items-center gap-2 justify-end">
                          <Progress
                            value={(item.score / maxScore) * 100}
                            className={`h-2 bg-zinc-700 ${index === 0 ? "bg-gradient-to-r from-indigo-500 to-purple-500" : "bg-zinc-500"}`}
                          />
                          <span className="text-xs w-10">{Math.round((item.score / maxScore) * 100)}%</span>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </div>
        </div>
      </div>
    </motion.section>
  )
} 
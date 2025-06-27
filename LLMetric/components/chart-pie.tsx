"use client"

import * as React from "react"
import { Label, Pie, PieChart } from "recharts"

import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { type ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"

const chartData = [
  { activity: "walking", minutes: 342, fill: "hsl(210, 12%, 28%)" }, // dark metallic gray
  { activity: "jogging", minutes: 187, fill: "hsl(210, 15%, 68%)" }, // light metallic gray
]

const chartConfig = {
  minutes: {
    label: "Minutes",
  },
  walking: {
    label: "Walking",
    color: "hsl(210, 12%, 28%)", // dark metallic gray
  },
  jogging: {
    label: "Jogging",
    color: "hsl(210, 15%, 68%)", // light metallic gray
  },
} satisfies ChartConfig

export function ChartPie() {
  const totalMinutes = React.useMemo(() => {
    return chartData.reduce((acc, curr) => acc + curr.minutes, 0)
  }, [])

  return (
    <Card className="flex flex-col h-full bg-black border-gray-800">
      <CardHeader className="items-center pb-0">
        <CardTitle className="text-white">Weekly Exercise Distribution</CardTitle>
      </CardHeader>
      <CardContent className="flex-1 pb-0">
        <ChartContainer config={chartConfig} className="mx-auto aspect-square max-h-[250px]">
          <PieChart>
            <ChartTooltip cursor={false} content={<ChartTooltipContent hideLabel />} />
            <Pie data={chartData} dataKey="minutes" nameKey="activity" innerRadius={60} strokeWidth={5}>
              <Label
                content={({ viewBox }) => {
                  if (viewBox && "cx" in viewBox && "cy" in viewBox) {
                    return (
                      <text x={viewBox.cx} y={viewBox.cy} textAnchor="middle" dominantBaseline="middle">
                        <tspan x={viewBox.cx} y={viewBox.cy} className="fill-white text-3xl font-bold">
                          {totalMinutes.toLocaleString()}
                        </tspan>
                        <tspan x={viewBox.cx} y={(viewBox.cy || 0) + 24} className="fill-gray-300">
                          Minutes
                        </tspan>
                      </text>
                    )
                  }
                }}
              />
            </Pie>
          </PieChart>
        </ChartContainer>
      </CardContent>
      <CardFooter className="text-sm justify-center mt-auto">
        <div className="text-center font-medium text-white">Walking: 65% | Jogging: 35% of total exercise time</div>
      </CardFooter>
    </Card>
  )
}

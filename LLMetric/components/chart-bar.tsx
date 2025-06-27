"use client"

import { Bar, BarChart, CartesianGrid, XAxis } from "recharts"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { type ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"

const chartData = [
  { day: "Monday", walking: 45, jogging: 20 },
  { day: "Tuesday", walking: 38, jogging: 25 },
  { day: "Wednesday", walking: 52, jogging: 30 },
  { day: "Thursday", walking: 30, jogging: 15 },
  { day: "Friday", walking: 42, jogging: 22 },
  { day: "Saturday", walking: 65, jogging: 40 },
  { day: "Sunday", walking: 70, jogging: 35 },
]

const chartConfig = {
  walking: {
    label: "Walking",
    color: "hsl(210, 12%, 28%)",
  },
  jogging: {
    label: "Jogging", 
    color: "hsl(210, 15%, 68%)",
  },
} satisfies ChartConfig

export function ChartBar() {
  return (
    <Card className="flex flex-col h-full bg-black border-gray-800">
      <CardHeader className="items-center pb-0">
        <CardTitle className="text-white">Weekly Exercise Activity</CardTitle>
      </CardHeader>
      <CardContent className="flex-1">
        <ChartContainer config={chartConfig}>
          <BarChart accessibilityLayer data={chartData}>
            <CartesianGrid vertical={false} stroke="rgba(255,255,255,0.1)" />
            <XAxis
              dataKey="day"
              tickLine={false}
              tickMargin={10}
              axisLine={false}
              tickFormatter={(value: string) => value.slice(0, 3)}
              stroke="rgba(255,255,255,0.7)"
            />
            <ChartTooltip content={<ChartTooltipContent hideLabel />} />
            <Bar dataKey="walking" stackId="a" fill="var(--color-walking)" radius={[0, 0, 4, 4]} />
            <Bar dataKey="jogging" stackId="a" fill="var(--color-jogging)" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ChartContainer>
      </CardContent>
      <CardFooter className="text-sm justify-center mt-auto">
        <div className="text-center font-medium text-white">Weekend activity is 48% higher than weekdays</div>
      </CardFooter>
    </Card>
  )
}

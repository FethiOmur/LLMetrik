export function SharedLegend() {
  return (
    <div className="w-full max-w-4xl bg-black p-4 rounded-lg border border-gray-800 shadow-sm">
      <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
        <div className="text-lg font-medium text-white">Exercise Legend:</div>
        <div className="flex items-center gap-6">
          <span className="inline-flex items-center">
            <span className="w-5 h-5 rounded-full bg-[hsl(210,12%,28%)] mr-2"></span>
            <span className="text-white text-base">Walking: 342 total minutes</span>
          </span>
          <span className="inline-flex items-center">
            <span className="w-5 h-5 rounded-full bg-[hsl(210,15%,68%)] mr-2"></span>
            <span className="text-white text-base">Jogging: 187 total minutes</span>
          </span>
        </div>
      </div>
    </div>
  )
}

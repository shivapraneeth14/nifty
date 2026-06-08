export default function StockChips({ stocks }: { stocks: string[] }) {
  if (!stocks?.length) return null
  return (
    <div className="flex flex-wrap gap-1.5 mt-2">
      {stocks.map((s) => (
        <span key={s} className="inline-flex items-center text-[10px] font-mono font-medium px-1.5 py-0.5 rounded bg-indigo-500/5 text-indigo-500 border border-indigo-500/10">
          {s}
        </span>
      ))}
    </div>
  )
}

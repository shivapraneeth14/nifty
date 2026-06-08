export default function HistoricalBar({ text }: { text: string }) {
  if (!text) return null
  return (
    <div className="flex items-center gap-1.5 mt-2 text-xs text-indigo-500 bg-indigo-500/5 border border-indigo-500/10 rounded-lg px-3 py-1.5">
      <span>📊</span>
      <span>{text}</span>
    </div>
  )
}

interface Props {
  label: string
  score?: number | null
}

const colors: Record<string, string> = {
  bullish: 'bg-green-100 text-green-800',
  bearish: 'bg-red-100 text-red-800',
  neutral: 'bg-gray-100 text-gray-600',
}

export default function SentimentBadge({ label, score }: Props) {
  const colorClass = colors[label] || colors.neutral
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium ${colorClass}`}>
      <span>{label === 'bullish' ? '🟢' : label === 'bearish' ? '🔴' : '⚪'}</span>
      {label}
      {score != null && <span className="opacity-60">({(score * 100).toFixed(0)}%)</span>}
    </span>
  )
}

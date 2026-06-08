import { motion } from 'framer-motion'

export default function SentimentBadge({ label, score = null, size = 'sm', animated = false }: {
  label: string
  score?: number | null
  size?: 'sm' | 'md' | 'lg'
  animated?: boolean
}) {
  const colors: Record<string, { bg: string; text: string; border: string }> = {
    bullish: { bg: 'bg-green-500/10', text: 'text-green-600 dark:text-green-400', border: 'border-green-500/20' },
    bearish: { bg: 'bg-red-500/10', text: 'text-red-600 dark:text-red-400', border: 'border-red-500/20' },
    neutral: { bg: 'bg-amber-500/10', text: 'text-amber-600 dark:text-amber-400', border: 'border-amber-500/20' },
  }
  const c = colors[label] || colors.neutral
  const sizeClass = size === 'sm' ? 'text-xs px-2 py-0.5' : size === 'lg' ? 'text-sm px-3 py-1' : 'text-xs px-2.5 py-1'

  const tag = (
    <span className={`inline-flex items-center gap-1.5 font-medium rounded-full border ${c.bg} ${c.text} ${c.border} ${sizeClass}`}>
      <span>{label === 'bullish' ? '🟢' : label === 'bearish' ? '🔴' : '⚪'}</span>
      <span className="capitalize">{label}</span>
      {score != null && <span className="opacity-60 font-mono text-[10px]">{(score * 100).toFixed(0)}%</span>}
    </span>
  )

  if (animated) return <motion.span initial={{ scale: 0.8 }} animate={{ scale: 1 }}>{tag}</motion.span>
  return tag
}

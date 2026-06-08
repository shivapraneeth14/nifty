export const SENTIMENT_COLORS = {
  bullish: { bg: 'bg-green-500/10', text: 'text-green-500', border: 'border-green-500/20', dot: '🟢' },
  bearish: { bg: 'bg-red-500/10', text: 'text-red-500', border: 'border-red-500/20', dot: '🔴' },
  neutral: { bg: 'bg-amber-500/10', text: 'text-amber-500', border: 'border-amber-500/20', dot: '⚪' },
} as const

export const EVENT_TYPE_COLORS: Record<string, string> = {
  RBI: 'bg-violet-500/10 text-violet-600 dark:text-violet-400',
  FED: 'bg-blue-500/10 text-blue-600 dark:text-blue-400',
  CPI: 'bg-orange-500/10 text-orange-600 dark:text-orange-400',
  BUDGET: 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400',
  GDP: 'bg-cyan-500/10 text-cyan-600 dark:text-cyan-400',
  EARNINGS: 'bg-pink-500/10 text-pink-600 dark:text-pink-400',
  GLOBAL: 'bg-gray-500/10 text-gray-600 dark:text-gray-400',
}

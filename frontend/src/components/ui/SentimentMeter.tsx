import { motion } from 'framer-motion'

interface Props {
  nifty: number
  banknifty: number
  overall: string
}

export default function SentimentMeter({ nifty, banknifty, overall }: Props) {
  const meterWidth = (val: number) => ((val + 1) / 2) * 100

  const color = (val: number) => {
    if (val > 0.3) return 'bg-green-500'
    if (val < -0.3) return 'bg-red-500'
    return 'bg-amber-500'
  }

  const label = (val: number) => {
    if (val > 0.1) return 'Bullish 📈'
    if (val < -0.1) return 'Bearish 📉'
    return 'Neutral ⚪'
  }

  return (
    <div className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-4 space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100">Live Sentiment</h3>
        <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
          overall === 'bullish' ? 'bg-green-500/10 text-green-600 dark:text-green-400' :
          overall === 'bearish' ? 'bg-red-500/10 text-red-600 dark:text-red-400' :
          'bg-amber-500/10 text-amber-600 dark:text-amber-400'
        }`}>{overall.toUpperCase()}</span>
      </div>

      {[
        { label: 'Nifty 50', val: nifty },
        { label: 'Bank Nifty', val: banknifty },
      ].map((item) => (
        <div key={item.label} className="space-y-1">
          <div className="flex justify-between text-xs">
            <span className="text-gray-500 dark:text-gray-400">{item.label}</span>
            <span className="font-medium text-gray-900 dark:text-gray-100">{label(item.val)}</span>
          </div>
          <div className="h-2 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: '50%' }}
              animate={{ width: `${meterWidth(item.val)}%` }}
              transition={{ duration: 0.8, ease: 'easeOut' }}
              className={`h-full rounded-full ${color(item.val)}`}
            />
          </div>
          <div className="flex justify-between text-[10px] text-gray-400">
            <span>Bearish</span>
            <span>Neutral</span>
            <span>Bullish</span>
          </div>
        </div>
      ))}
    </div>
  )
}

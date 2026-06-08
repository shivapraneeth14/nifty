import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import type { SentimentMeter as MeterData } from '../../types/brief'
import { fetchMeter } from '../../services/meter'

interface Props {
  activeIndex?: string
  overall?: string
}

export default function SentimentMeter({ activeIndex = 'nifty', overall }: Props) {
  const [data, setData] = useState<MeterData | null>(null)

  useEffect(() => { fetchMeter().then(setData).catch(() => {}) }, [])

  const nifty = data?.nifty ?? 0
  const banknifty = data?.banknifty ?? 0
  const overallSent = overall || data?.overall || 'neutral'

  const meterWidth = (val: number) => ((val + 1) / 2) * 100
  const color = (val: number) => val > 0.3 ? 'bg-green-500' : val < -0.3 ? 'bg-red-500' : 'bg-amber-500'
  const label = (val: number) => val > 0.1 ? 'Bullish 📈' : val < -0.1 ? 'Bearish 📉' : 'Neutral ⚪'

  return (
    <div className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-4 space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100">Live Sentiment</h3>
        <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
          overallSent === 'bullish' ? 'bg-green-500/10 text-green-600 dark:text-green-400' :
          overallSent === 'bearish' ? 'bg-red-500/10 text-red-600 dark:text-red-400' :
          'bg-amber-500/10 text-amber-600 dark:text-amber-400'
        }`}>{overallSent.toUpperCase()}</span>
      </div>

      {[
        { label: 'Nifty 50', val: nifty, key: 'nifty' },
        { label: 'Bank Nifty', val: banknifty, key: 'banknifty' },
      ].map((item) => {
        const isActive = item.key === activeIndex
        return (
          <div key={item.key} className="space-y-1">
            <div className="flex justify-between text-xs">
              <span className={`${isActive ? 'text-indigo-500 font-semibold' : 'text-gray-500 dark:text-gray-400'}`}>
                {item.label} {isActive ? '◀' : ''}
              </span>
              <span className="font-medium text-gray-900 dark:text-gray-100">{label(item.val)}</span>
            </div>
            <div className="h-2 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden relative">
              {isActive && <div className="absolute inset-0 ring-1 ring-indigo-500/30 rounded-full" />}
              <motion.div
                initial={{ width: '50%' }}
                animate={{ width: `${meterWidth(item.val)}%` }}
                transition={{ duration: 0.8, ease: 'easeOut' }}
                className={`h-full rounded-full ${color(item.val)}`}
              />
            </div>
            {data?.article_count != null && (
              <div className="text-[10px] text-gray-400 text-right">Based on {data.article_count} recent articles</div>
            )}
          </div>
        )
      })}
    </div>
  )
}

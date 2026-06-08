import { motion } from 'framer-motion'
import ProgressRing from '../components/ui/ProgressRing'
import SentimentBadge from '../components/ui/SentimentBadge'
import { EmptyState } from '../components/ui/ErrorState'
import { formatPoints } from '../utils/formatters'

const dummyDays = [
  { date: '2026-06-08', predicted: 'bullish', actual: 148 },
  { date: '2026-06-07', predicted: 'bearish', actual: -45 },
  { date: '2026-06-06', predicted: 'neutral', actual: 12 },
  { date: '2026-06-05', predicted: 'bullish', actual: 218 },
  { date: '2026-06-04', predicted: 'bullish', actual: -78 },
  { date: '2026-06-03', predicted: 'neutral', actual: 55 },
  { date: '2026-06-02', predicted: 'bearish', actual: -120 },
  { date: '2026-06-01', predicted: 'bullish', actual: 92 },
]
const correctCount = dummyDays.filter(d => d.predicted === 'neutral' ? Math.abs(d.actual) < 50 : d.predicted === 'bullish' ? d.actual > 0 : d.actual < 0).length
const accuracy = Math.round((correctCount / dummyDays.length) * 100)

export default function AccuracyScreen() {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6 pb-24">
      <h1 className="text-lg font-bold text-gray-900 dark:text-gray-100">Your Accuracy</h1>
      <div className="flex flex-col items-center py-6"><ProgressRing value={accuracy} size={100} strokeWidth={8} label="30-day accuracy" /></div>
      <div className="grid grid-cols-3 gap-3">
        {[
          { label: 'Briefs sent', value: '142' },
          { label: 'Correct', value: `${correctCount}/${dummyDays.length}` },
          { label: 'User ratings', value: '4.1k' },
        ].map(s => (
          <div key={s.label} className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-3 text-center">
            <div className="text-lg font-bold font-mono text-gray-900 dark:text-gray-100">{s.value}</div>
            <div className="text-[10px] text-gray-400 dark:text-gray-500 mt-0.5">{s.label}</div>
          </div>
        ))}
      </div>
      <div className="space-y-2">
        <h2 className="text-sm font-semibold text-gray-900 dark:text-gray-100">Recent days</h2>
        {dummyDays.map((d, i) => {
          const correct = d.predicted === 'neutral' ? Math.abs(d.actual) < 50 : d.predicted === 'bullish' ? d.actual > 0 : d.actual < 0
          return (
            <motion.div key={d.date} initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.05 }}
              className="flex items-center justify-between rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-3"
            >
              <div className="flex items-center gap-3">
                <span className={correct ? '' : 'opacity-40'}>{correct ? '✅' : '❌'}</span>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-medium text-gray-400 dark:text-gray-500 font-mono">{d.date}</span>
                    <SentimentBadge label={d.predicted} />
                  </div>
                  <span className={`text-xs font-mono font-semibold ${d.actual > 0 ? 'text-green-500' : d.actual < 0 ? 'text-red-500' : 'text-amber-500'}`}>Nifty {formatPoints(d.actual)}</span>
                </div>
              </div>
            </motion.div>
          )
        })}
      </div>
    </motion.div>
  )
}

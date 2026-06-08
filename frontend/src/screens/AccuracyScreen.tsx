import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import ProgressRing from '../components/ui/ProgressRing'
import SentimentBadge from '../components/ui/SentimentBadge'
import { EmptyState } from '../components/ui/ErrorState'
import { CardSkeleton } from '../components/ui/Skeleton'
import { get } from '../services/api'
import { formatPoints } from '../utils/formatters'

interface AccuracyData {
  last_10: number
  last_30: number
  total: number
  count: number
  recent_days: { date: string; predicted: string; actual_move: number | null; correct: boolean | null }[]
}

export default function AccuracyScreen() {
  const [index, setIndex] = useState('nifty')
  const [data, setData] = useState<AccuracyData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    get<AccuracyData>(`/accuracy?index=${index}`)
      .then(setData)
      .catch(() => setData(null))
      .finally(() => setLoading(false))
  }, [index])

  const idxLabel = index === 'nifty' ? 'Nifty 50' : 'Bank Nifty'

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6 pb-24">
      <h1 className="text-lg font-bold text-gray-900 dark:text-gray-100">Accuracy Tracker</h1>

      <div className="flex gap-1.5 bg-gray-50 dark:bg-[#131620] rounded-xl p-1 border border-gray-200 dark:border-gray-800">
        {['nifty', 'banknifty'].map((idx) => (
          <button key={idx} onClick={() => setIndex(idx)}
            className={`flex-1 py-1.5 text-sm font-medium rounded-lg transition-colors ${index === idx ? 'bg-white dark:bg-[#1A1D28] text-indigo-500 shadow-sm border border-gray-200 dark:border-gray-800' : 'text-gray-400 dark:text-gray-500'}`}
          >{idx === 'nifty' ? 'Nifty 50' : 'Bank Nifty'}</button>
        ))}
      </div>

      {loading ? (
        <div className="space-y-3">{[1,2,3].map(i => <CardSkeleton key={i} />)}</div>
      ) : !data || data.count === 0 ? (
        <EmptyState icon="📊" message="No accuracy data yet" submessage="Data appears after the first post-market debrief" />
      ) : (
        <>
          <div className="flex flex-col items-center py-4">
            <ProgressRing value={data.total} size={100} strokeWidth={8} label={`${idxLabel} accuracy`} />
          </div>

          <div className="grid grid-cols-3 gap-3">
            {[
              { label: 'Last 10', value: `${data.last_10}%` },
              { label: 'Last 30', value: `${data.last_30}%` },
              { label: 'Total days', value: String(data.count) },
            ].map(s => (
              <div key={s.label} className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-3 text-center">
                <div className="text-lg font-bold font-mono text-gray-900 dark:text-gray-100">{s.value}</div>
                <div className="text-[10px] text-gray-400 dark:text-gray-500 mt-0.5">{s.label}</div>
              </div>
            ))}
          </div>

          <div className="space-y-2">
            <h2 className="text-sm font-semibold text-gray-900 dark:text-gray-100">Recent days</h2>
            {data.recent_days.map((d, i) => (
              <motion.div key={d.date} initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.05 }}
                className="flex items-center justify-between rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-3"
              >
                <div className="flex items-center gap-3">
                  <span className={d.correct ? '' : 'opacity-40'}>{d.correct === true ? '✅' : d.correct === false ? '❌' : '⏳'}</span>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-medium text-gray-400 dark:text-gray-500 font-mono">{d.date}</span>
                      {d.predicted && <SentimentBadge label={d.predicted} />}
                    </div>
                    <span className={`text-xs font-mono font-semibold ${(d.actual_move ?? 0) > 0 ? 'text-green-500' : (d.actual_move ?? 0) < 0 ? 'text-red-500' : 'text-amber-500'}`}>
                      {idxLabel} {formatPoints(d.actual_move)}
                    </span>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </>
      )}
    </motion.div>
  )
}

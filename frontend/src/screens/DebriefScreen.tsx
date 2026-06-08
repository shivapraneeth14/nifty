import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { fetchDebrief } from '../services/debrief'
import type { Debrief } from '../types/brief'
import SentimentBadge from '../components/ui/SentimentBadge'
import ErrorState from '../components/ui/ErrorState'
import { formatPoints } from '../utils/formatters'

export default function DebriefScreen() {
  const [debrief, setDebrief] = useState<Debrief | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDebrief()
      .then(setDebrief)
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="py-20 text-center text-gray-400">Loading...</div>
  if (!debrief) return <ErrorState message="No debrief available yet" />

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4 pb-24">
      <h1 className="text-lg font-bold text-gray-900 dark:text-gray-100">Market Close Debrief</h1>

      <div className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-4 space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-400">{debrief.date}</span>
          <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
            debrief.correct === true ? 'bg-green-500/10 text-green-600' :
            debrief.correct === false ? 'bg-red-500/10 text-red-600' :
            'bg-gray-500/10 text-gray-500'
          }`}>
            {debrief.correct === true ? '✅ Correct' : debrief.correct === false ? '❌ Missed' : 'Pending'}
          </span>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div className="rounded-lg bg-gray-50 dark:bg-[#131620] p-3 text-center">
            <div className="text-[10px] text-gray-400 mb-1">Predicted</div>
            <SentimentBadge label={debrief.predicted} />
          </div>
          <div className="rounded-lg bg-gray-50 dark:bg-[#131620] p-3 text-center">
            <div className="text-[10px] text-gray-400 mb-1">Actual</div>
            <span className={`text-lg font-bold font-mono ${(debrief.actual_move ?? 0) > 0 ? 'text-green-500' : (debrief.actual_move ?? 0) < 0 ? 'text-red-500' : 'text-gray-400'}`}>
              {formatPoints(debrief.actual_move)}
            </span>
          </div>
        </div>

        <p className="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">{debrief.debrief_text}</p>
      </div>
    </motion.div>
  )
}

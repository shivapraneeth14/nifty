import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { fetchDebrief } from '../services/debrief'
import type { Debrief as DebriefType } from '../types/brief'
import SentimentBadge from '../components/ui/SentimentBadge'
import ErrorState from '../components/ui/ErrorState'
import { formatPoints } from '../utils/formatters'

export default function DebriefScreen() {
  const [debrief, setDebrief] = useState<DebriefType | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDebrief().then(setDebrief).catch(() => {}).finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="py-20 text-center text-gray-400">Loading...</div>
  if (!debrief) return <ErrorState message="No debrief available yet" />

  const pairs = [
    { label: 'Nifty 50', predicted: debrief.predicted_nifty || 'neutral', actual: debrief.nifty_move, correct: debrief.nifty_correct },
    { label: 'Bank Nifty', predicted: debrief.predicted_banknifty || 'neutral', actual: debrief.banknifty_move, correct: debrief.banknifty_correct },
  ]

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4 pb-24">
      <h1 className="text-lg font-bold text-gray-900 dark:text-gray-100">Market Close Debrief</h1>
      <div className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-4 space-y-4">
        <div className="flex items-center justify-between"><span className="text-xs text-gray-400">{debrief.date}</span></div>
        {pairs.map((p) => (
          <div key={p.label} className="space-y-2">
            <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400">{p.label}</h3>
            <div className="grid grid-cols-2 gap-3">
              <div className="rounded-lg bg-gray-50 dark:bg-[#131620] p-3 text-center">
                <div className="text-[10px] text-gray-400 mb-1">Predicted</div>
                <SentimentBadge label={p.predicted} />
              </div>
              <div className="rounded-lg bg-gray-50 dark:bg-[#131620] p-3 text-center">
                <div className="text-[10px] text-gray-400 mb-1">Actual</div>
                <span className={`text-lg font-bold font-mono ${(p.actual ?? 0) > 0 ? 'text-green-500' : (p.actual ?? 0) < 0 ? 'text-red-500' : 'text-gray-400'}`}>{formatPoints(p.actual)}</span>
              </div>
            </div>
            <div className="text-right">
              <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${p.correct === true ? 'bg-green-500/10 text-green-600' : p.correct === false ? 'bg-red-500/10 text-red-600' : 'bg-gray-500/10 text-gray-500'}`}>
                {p.correct === true ? '✅ Correct' : p.correct === false ? '❌ Missed' : '⏳ Pending'}
              </span>
            </div>
          </div>
        ))}
        <p className="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">{debrief.debrief_text}</p>
      </div>
    </motion.div>
  )
}

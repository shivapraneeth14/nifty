import { useState } from 'react'
import { motion } from 'framer-motion'
import { useHistory } from '../hooks/useHistory'
import { formatPoints } from '../utils/formatters'
import { CardSkeleton } from '../components/ui/Skeleton'
import { EmptyState } from '../components/ui/ErrorState'

const EVENT_TYPES = ['', 'RBI', 'FED', 'CPI', 'BUDGET', 'GDP', 'EARNINGS', 'GLOBAL']
const TYPE_COLORS: Record<string, string> = {
  RBI: 'bg-violet-500/10 text-violet-600 dark:text-violet-400',
  FED: 'bg-blue-500/10 text-blue-600 dark:text-blue-400',
  CPI: 'bg-orange-500/10 text-orange-600 dark:text-orange-400',
  BUDGET: 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400',
  GDP: 'bg-cyan-500/10 text-cyan-600 dark:text-cyan-400',
  EARNINGS: 'bg-pink-500/10 text-pink-600 dark:text-pink-400',
  GLOBAL: 'bg-gray-500/10 text-gray-600 dark:text-gray-400',
}

export default function HistoryScreen() {
  const [filter, setFilter] = useState('')
  const { events, loading } = useHistory(filter || undefined)
  const niftyMoves = events.map(e => e.nifty_move).filter((m): m is number => m != null)
  const avg = niftyMoves.length ? niftyMoves.reduce((a, b) => a + b, 0) / niftyMoves.length : 0
  const up = niftyMoves.filter(m => m > 0).length
  const down = niftyMoves.filter(m => m < 0).length

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4 pb-24">
      <h1 className="text-lg font-bold text-gray-900 dark:text-gray-100">Historical Impact</h1>
      <div className="flex gap-1.5 overflow-x-auto pb-1">
        {EVENT_TYPES.map(t => (
          <button key={t} onClick={() => setFilter(t)}
            className={`shrink-0 px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${filter === t ? 'bg-indigo-500 text-white border-indigo-500' : 'bg-gray-50 dark:bg-[#131620] text-gray-500 dark:text-gray-400 border-gray-200 dark:border-gray-800 hover:bg-gray-100 dark:hover:bg-gray-800'}`}
          >{t || 'All'}</button>
        ))}
      </div>
      {events.length > 0 && niftyMoves.length > 0 && (
        <div className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-3 text-xs space-y-1">
          <div className="flex items-center gap-2 text-gray-500 dark:text-gray-400">
            <span className="font-medium text-gray-900 dark:text-gray-100">Summary:</span>
            <span className="text-green-500">{up} up</span>
            <span className="text-red-500">{down} down</span>
          </div>
          <div className="text-gray-500 dark:text-gray-400">Avg Nifty: <span className={`font-mono font-semibold ${avg > 0 ? 'text-green-500' : 'text-red-500'}`}>{formatPoints(avg)} pts</span></div>
        </div>
      )}
      {loading ? <div className="space-y-3">{[1,2,3].map(i => <CardSkeleton key={i} />)}</div>
      : events.length === 0 ? <EmptyState icon="📚" message="No events found" submessage="Try a different filter" />
      : <div className="space-y-2">
          {events.map((e, i) => (
            <motion.div key={e.id} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.03 }}
              className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-3"
            >
              <div className="flex items-center justify-between mb-1">
                <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${TYPE_COLORS[e.event_type] || 'bg-gray-500/10 text-gray-500'}`}>{e.event_type}</span>
                <span className="text-[10px] text-gray-400 dark:text-gray-500 font-mono">{e.date}</span>
              </div>
              <p className="text-sm font-medium text-gray-900 dark:text-gray-100">{e.headline}</p>
              <div className="flex gap-4 mt-1.5 text-xs">
                {e.nifty_move != null && <span className={`font-mono font-semibold ${e.nifty_move > 0 ? 'text-green-500' : 'text-red-500'}`}>Nifty {formatPoints(e.nifty_move)}</span>}
                {e.banknifty_move != null && <span className={`font-mono font-semibold ${e.banknifty_move > 0 ? 'text-green-500' : 'text-red-500'}`}>BankNifty {formatPoints(e.banknifty_move)}</span>}
              </div>
            </motion.div>
          ))}
        </div>
      }
    </motion.div>
  )
}

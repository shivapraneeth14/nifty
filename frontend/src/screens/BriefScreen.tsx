import { useState } from 'react'
import { motion } from 'framer-motion'
import { Clock, Sun, Moon } from 'lucide-react'
import { useBrief } from '../hooks/useBrief'
import { useTheme } from '../config/theme'
import SentimentBadge from '../components/ui/SentimentBadge'
import { BriefSkeleton } from '../components/ui/Skeleton'
import ErrorState from '../components/ui/ErrorState'
import { EmptyState } from '../components/ui/ErrorState'
import BriefCard from '../components/brief/BriefCard'
import KeyLevelsPanel from '../components/brief/KeyLevelsPanel'
import Toggle from '../components/ui/Toggle'
import SentimentMeter from '../components/ui/SentimentMeter'
import GlobalMarketPulse from '../components/ui/GlobalMarketPulse'
import OptionChainCard from '../components/ui/OptionChainCard'
import FiiPanel from '../components/ui/FiiPanel'
import { getRelativeTime } from '../utils/formatters'

const INDEX_OPTIONS = [
  { label: 'Nifty 50', value: 'nifty' },
  { label: 'Bank Nifty', value: 'banknifty' },
]

export default function BriefScreen() {
  const { brief, loading, error, refetch } = useBrief()
  const { theme, toggle: toggleTheme } = useTheme()
  const [index, setIndex] = useState('nifty')

  if (loading) return <BriefSkeleton />
  if (error) return <ErrorState message={error} onRetry={refetch} />
  if (!brief || !brief.items?.length) return <EmptyState icon="📭" message="No brief yet for today" submessage="Check back around 8:45 AM" />

  const isNifty = index === 'nifty'
  const histSummary = isNifty ? brief.historical_summary_nifty : brief.historical_summary_banknifty
  const keyLevels = isNifty ? (brief.key_levels_nifty || brief.key_levels) : (brief.key_levels_banknifty || brief.key_levels)
  const indexLabel = isNifty ? 'Nifty' : 'BankNifty'
  const indexEmoji = isNifty ? '📈' : '🏦'

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4 pb-24">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-bold text-gray-900 dark:text-gray-100">Pre-market Brief</h1>
          <p className="text-xs text-gray-400 dark:text-gray-500 flex items-center gap-1 mt-0.5">
            <Clock size={10} />{getRelativeTime(brief.created_at)}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <SentimentBadge label={brief.overall_sentiment} size="lg" animated />
          <button onClick={toggleTheme} className="p-1.5 rounded-lg text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
            {theme === 'dark' ? <Sun size={16} /> : <Moon size={16} />}
          </button>
        </div>
      </header>

      <Toggle options={INDEX_OPTIONS} selected={index} onChange={setIndex} />

      <div className="bg-gray-50 dark:bg-[#131620] border border-gray-200 dark:border-gray-800 rounded-xl p-3 text-xs text-gray-500 dark:text-gray-400 leading-relaxed">
        {brief.summary_text}
      </div>

      {histSummary && (
        <div className="text-xs text-indigo-500 bg-indigo-500/5 border border-indigo-500/10 rounded-xl px-3 py-2">
          {indexEmoji} {indexLabel} historical context: {histSummary}
        </div>
      )}

      <GlobalMarketPulse />
      <SentimentMeter nifty={0.2} banknifty={0.1} overall={brief.overall_sentiment} />

      {keyLevels && <KeyLevelsPanel levels={keyLevels} index={indexLabel} />}

      <FiiPanel />
      <OptionChainCard />

      <div className="space-y-3">
        {brief.items.map((item) => (
          <BriefCard key={item.id} item={item} briefId={brief.id} index={index} />
        ))}
      </div>
    </motion.div>
  )
}

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Clock, Sun, Moon, TrendingUp, TrendingDown, Minus } from 'lucide-react'
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

function MarketCallBanner({ sentiment, accuracy, tradeAction, indexLabel, indexShort }: {
  sentiment: string
  accuracy?: { recent: number; last_10: string }
  tradeAction?: string
  indexLabel: string
  indexShort: string
}) {
  const isBullish = sentiment === 'bullish'
  const isBearish = sentiment === 'bearish'
  const bgColor = isBullish ? 'bg-green-500' : isBearish ? 'bg-red-500' : 'bg-amber-500'
  const Icon = isBullish ? TrendingUp : isBearish ? TrendingDown : Minus
  const emoji = isBullish ? '📈' : isBearish ? '📉' : '⚪'
  const action = isBullish ? `BUY ${indexShort.toUpperCase()} CALLS / SELL PUTS` : isBearish ? `BUY ${indexShort.toUpperCase()} PUTS / SELL CALLS` : 'RANGE TRADE / WAIT'
  const accText = accuracy ? `${accuracy.recent}% (${accuracy.last_10} last 10)` : 'No data yet'

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ type: 'spring', stiffness: 300 }}
      className={`rounded-xl border ${bgColor}/20 bg-gradient-to-br ${bgColor}/5 overflow-hidden`}
    >
      <div className="p-4 space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className={`w-10 h-10 rounded-xl ${bgColor} flex items-center justify-center shadow-lg`}>
              <Icon size={20} className="text-white" />
            </div>
            <div>
              <div className="text-lg font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2">
                {emoji} {indexLabel}: {sentiment.toUpperCase()}
              </div>
              <div className="text-xs text-gray-400 dark:text-gray-500">
                Suggested: <span className="font-medium text-gray-700 dark:text-gray-300">{action}</span>
              </div>
            </div>
          </div>
          <div className="text-right">
            <div className={`text-2xl font-bold font-mono ${isBullish ? 'text-green-500' : isBearish ? 'text-red-500' : 'text-amber-500'}`}>{emoji}</div>
            <div className="text-[10px] text-gray-400 mt-0.5">Accuracy: {accText}</div>
          </div>
        </div>
        {tradeAction && (
          <div className="rounded-lg bg-gray-900/5 dark:bg-white/5 px-3 py-2">
            <p className="text-xs text-gray-600 dark:text-gray-400 leading-relaxed">{tradeAction}</p>
          </div>
        )}
      </div>
    </motion.div>
  )
}

export default function BriefScreen() {
  const { brief, loading, error, refetch } = useBrief()
  const { theme, toggle: toggleTheme } = useTheme()
  const [index, setIndex] = useState('nifty')

  if (loading) return <BriefSkeleton />
  if (error) return <ErrorState message={error} onRetry={refetch} />
  if (!brief || !brief.items?.length && !brief.items_nifty?.length) return <EmptyState icon="📭" message="No brief yet for today" submessage="Check back around 8:45 AM" />

  const isNifty = index === 'nifty'
  const indexLabel = isNifty ? 'Nifty 50' : 'Bank Nifty'
  const indexShort = isNifty ? 'Nifty' : 'BankNifty'
  const indexEmoji = isNifty ? '📈' : '🏦'

  // DYNAMIC: Every field switches per index
  const currentSentiment = isNifty ? (brief.sentiment_nifty || brief.overall_sentiment) : (brief.sentiment_banknifty || brief.overall_sentiment)
  const currentItems = isNifty ? (brief.items_nifty || brief.items) : (brief.items_banknifty || brief.items)
  const currentSummary = isNifty ? (brief.summary_nifty || brief.summary_text) : (brief.summary_banknifty || brief.summary_text)
  const currentTradeAction = isNifty ? brief.trade_action_nifty : brief.trade_action_banknifty
  const currentHistSummary = isNifty ? brief.historical_summary_nifty : brief.historical_summary_banknifty
  const currentKeyLevels = isNifty ? (brief.key_levels_nifty || brief.key_levels) : (brief.key_levels_banknifty || brief.key_levels)

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4 pb-24">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-bold text-gray-900 dark:text-gray-100">Pre-market Brief</h1>
          <p className="text-xs text-gray-400 dark:text-gray-500 flex items-center gap-1 mt-0.5">
            <Clock size={10} />{getRelativeTime(brief.created_at)} · <span className="font-medium text-indigo-500">{indexShort}</span>
          </p>
        </div>
        <div className="flex items-center gap-2">
          <SentimentBadge label={currentSentiment} size="lg" animated />
          <button onClick={toggleTheme} className="p-1.5 rounded-lg text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
            {theme === 'dark' ? <Sun size={16} /> : <Moon size={16} />}
          </button>
        </div>
      </header>

      <MarketCallBanner
        sentiment={currentSentiment}
        accuracy={brief.accuracy}
        tradeAction={currentTradeAction}
        indexLabel={indexLabel}
        indexShort={indexShort}
      />

      <Toggle options={INDEX_OPTIONS} selected={index} onChange={setIndex} />

      <div className="bg-gray-50 dark:bg-[#131620] border border-gray-200 dark:border-gray-800 rounded-xl p-3 text-xs text-gray-500 dark:text-gray-400 leading-relaxed">
        {currentSummary}
      </div>

      {currentHistSummary && (
        <div className="text-xs text-indigo-500 bg-indigo-500/5 border border-indigo-500/10 rounded-xl px-3 py-2">
          {indexEmoji} {indexShort} historical context: {currentHistSummary}
        </div>
      )}

      <GlobalMarketPulse />
      <SentimentMeter activeIndex={index} overall={currentSentiment} />

      {currentKeyLevels && <KeyLevelsPanel levels={currentKeyLevels} index={indexShort} />}

      <FiiPanel />
      <OptionChainCard />

      <div className="space-y-3">
        {currentItems.map((item) => (
          <BriefCard key={item.id} item={item} briefId={brief.id} index={index} />
        ))}
      </div>
    </motion.div>
  )
}

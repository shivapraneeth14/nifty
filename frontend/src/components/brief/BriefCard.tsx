import { motion } from 'framer-motion'
import SentimentBadge from '../ui/SentimentBadge'
import FeedbackButtons from '../ui/FeedbackButtons'
import WhySection from './WhySection'
import SectorChips from './SectorChips'
import StockChips from './StockChips'
import HistoricalBar from './HistoricalBar'
import type { BriefItem } from '../../types/brief'

interface Props {
  item: BriefItem
  briefId: string
  index?: string
}

export default function BriefCard({ item, briefId, index = 'nifty' }: Props) {
  const isNifty = index === 'nifty'
  const histContext = isNifty
    ? (item.historical_context_nifty || item.historical_context)
    : (item.historical_context_banknifty || '')

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ type: 'spring', stiffness: 300, damping: 25 }}
      className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-4 space-y-2 hover:border-indigo-500/30 hover:shadow-lg hover:shadow-indigo-500/5 transition-all duration-200"
    >
      <div className="flex items-start justify-between gap-3">
        <h3 className="font-semibold text-sm leading-snug text-gray-900 dark:text-gray-100">{item.headline}</h3>
        <SentimentBadge label={item.sentiment_label} score={item.sentiment_score} />
      </div>

      <p className="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">{item.impact_text}</p>

      <WhySection reasons={item.why || []} />
      <SectorChips sectors={(item.sectors || {}) as Record<string, string>} />
      <StockChips stocks={(item.stocks || []) as string[]} />

      {histContext && (
        <HistoricalBar text={histContext} />
      )}

      <div className="flex items-center justify-between pt-1 text-[10px] text-gray-400 dark:text-gray-500">
        <span className="font-medium">{item.source}</span>
        <FeedbackButtons briefId={briefId} articleId={item.article_id || undefined} />
      </div>
    </motion.div>
  )
}

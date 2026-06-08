import { useEffect, useState } from 'react'
import { fetchTodayBrief } from '../api/brief'
import type { Brief } from '../types/brief'
import BriefCard from '../components/BriefCard'
import SentimentBadge from '../components/SentimentBadge'

type Index = 'nifty' | 'banknifty'

export default function BriefPage() {
  const [brief, setBrief] = useState<Brief | null>(null)
  const [loading, setLoading] = useState(true)
  const [index, setIndex] = useState<Index>('nifty')

  useEffect(() => {
    fetchTodayBrief()
      .then(setBrief)
      .catch(() => setBrief(null))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20 text-gray-400">
        Loading...
      </div>
    )
  }

  if (!brief || !brief.items?.length) {
    return (
      <div className="py-20 text-center text-gray-400">
        <p className="text-lg">📭</p>
        <p className="mt-2">No brief yet for today</p>
        <p className="text-sm">Check back around 8:45 AM</p>
      </div>
    )
  }

  const histSummary = index === 'nifty' ? brief.historical_summary_nifty : brief.historical_summary_banknifty

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-lg font-bold">Pre-market Brief</h1>
        <SentimentBadge label={brief.overall_sentiment} />
      </div>

      <div className="flex gap-1 bg-gray-100 rounded-lg p-1">
        <button
          onClick={() => setIndex('nifty')}
          className={`flex-1 text-center py-1.5 text-sm font-medium rounded-md transition ${
            index === 'nifty' ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-500'
          }`}
        >
          Nifty 50
        </button>
        <button
          onClick={() => setIndex('banknifty')}
          className={`flex-1 text-center py-1.5 text-sm font-medium rounded-md transition ${
            index === 'banknifty' ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-500'
          }`}
        >
          Bank Nifty
        </button>
      </div>

      <p className="text-sm text-gray-600 bg-gray-50 rounded-lg p-3">
        {brief.summary_text}
      </p>

      {histSummary && (
        <p className="text-xs text-blue-700 bg-blue-50 px-3 py-2 rounded-lg">
          📊 {index === 'nifty' ? 'Nifty' : 'BankNifty'} historical context: {histSummary}
        </p>
      )}

      <div className="space-y-3">
        {brief.items.map((item) => (
          <BriefCard key={item.id} item={item} briefId={brief.id} index={index} />
        ))}
      </div>
    </div>
  )
}

import { useEffect, useState } from 'react'
import { fetchTodayBrief } from '../api/brief'
import type { Brief } from '../types/brief'
import BriefCard from '../components/BriefCard'
import SentimentBadge from '../components/SentimentBadge'

export default function BriefPage() {
  const [brief, setBrief] = useState<Brief | null>(null)
  const [loading, setLoading] = useState(true)

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

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-lg font-bold">Pre-market Brief</h1>
        <SentimentBadge label={brief.overall_sentiment} />
      </div>

      <p className="text-sm text-gray-600 bg-gray-50 rounded-lg p-3">
        {brief.summary_text}
      </p>

      <div className="space-y-3">
        {brief.items.map((item) => (
          <BriefCard key={item.id} item={item} briefId={brief.id} />
        ))}
      </div>
    </div>
  )
}

import { useEffect, useState } from 'react'
import { fetchHistory } from '../api/history'
import type { HistoricalEvent } from '../types/history'

const EVENT_TYPES = ['', 'RBI', 'FED', 'CPI', 'BUDGET', 'GDP', 'EARNINGS', 'GLOBAL']

export default function HistoryPage() {
  const [events, setEvents] = useState<HistoricalEvent[]>([])
  const [filter, setFilter] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    fetchHistory(filter || undefined)
      .then((res) => setEvents(res.events))
      .catch(() => setEvents([]))
      .finally(() => setLoading(false))
  }, [filter])

  return (
    <div className="space-y-4">
      <h1 className="text-lg font-bold">Historical Impact</h1>

      <div className="flex gap-1 flex-wrap">
        {EVENT_TYPES.map((t) => (
          <button
            key={t}
            onClick={() => setFilter(t)}
            className={`px-3 py-1 rounded text-xs font-medium border ${
              filter === t
                ? 'bg-blue-600 text-white border-blue-600'
                : 'bg-white text-gray-600 border-gray-300 hover:bg-gray-50'
            }`}
          >
            {t || 'All'}
          </button>
        ))}
      </div>

      {loading ? (
        <p className="text-gray-400 text-center py-8">Loading...</p>
      ) : events.length === 0 ? (
        <p className="text-gray-400 text-center py-8">No events found</p>
      ) : (
        <div className="space-y-2">
          {events.map((e) => (
            <div key={e.id} className="border border-gray-200 rounded-lg p-3 text-sm">
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-0.5 rounded">
                  {e.event_type}
                </span>
                <span className="text-xs text-gray-400">{e.date}</span>
              </div>
              <p className="mt-1 font-medium">{e.headline}</p>
              <div className="flex gap-4 mt-1 text-xs">
                {e.nifty_move != null && (
                  <span className={e.nifty_move > 0 ? 'text-green-600' : 'text-red-600'}>
                    Nifty: {e.nifty_move > 0 ? '+' : ''}{e.nifty_move} pts
                  </span>
                )}
                {e.banknifty_move != null && (
                  <span className={e.banknifty_move > 0 ? 'text-green-600' : 'text-red-600'}>
                    BankNifty: {e.banknifty_move > 0 ? '+' : ''}{e.banknifty_move} pts
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

import { useState, useEffect } from 'react'
import type { HistoricalEvent } from '../types/history'
import { fetchHistory } from '../services/history'

export function useHistory(event_type?: string) {
  const [events, setEvents] = useState<HistoricalEvent[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    fetchHistory(event_type)
      .then((res) => setEvents(res.events))
      .catch(() => setEvents([]))
      .finally(() => setLoading(false))
  }, [event_type])

  return { events, loading }
}

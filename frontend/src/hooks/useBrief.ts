import { useState, useEffect } from 'react'
import type { Brief } from '../types/brief'
import { fetchTodayBrief } from '../services/brief'

export function useBrief() {
  const [brief, setBrief] = useState<Brief | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = () => {
    setLoading(true)
    setError(null)
    fetchTodayBrief()
      .then(setBrief)
      .catch((e) => setError(e.message || 'Failed to load brief'))
      .finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  return { brief, loading, error, refetch: load }
}

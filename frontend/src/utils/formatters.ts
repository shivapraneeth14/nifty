export function formatDate(dateStr: string): string {
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-IN', { month: 'short', day: 'numeric', year: 'numeric' })
}

export function formatTime(dateStr: string): string {
  const d = new Date(dateStr)
  return d.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })
}

export function formatPoints(pts: number | null): string {
  if (pts == null) return '—'
  return `${pts > 0 ? '+' : ''}${pts.toFixed(0)}`
}

export function formatCr(cr: number | null): string {
  if (cr == null) return '—'
  return `${cr > 0 ? '+' : ''}₹${Math.abs(cr).toLocaleString('en-IN')}cr`
}

export function getRelativeTime(dateStr: string): string {
  const now = Date.now()
  const diff = now - new Date(dateStr).getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 1) return 'just now'
  if (mins < 60) return `${mins}m ago`
  const hours = Math.floor(mins / 60)
  if (hours < 24) return `${hours}h ago`
  return formatDate(dateStr)
}

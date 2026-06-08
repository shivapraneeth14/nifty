import { TrendingUp, TrendingDown, BarChart3, DollarSign } from 'lucide-react'
import type { KeyLevels } from '../../types/brief'
import { formatPoints, formatCr } from '../../utils/formatters'

export default function KeyLevelsPanel({ levels }: { levels: KeyLevels | null }) {
  if (!levels) return null
  const items = [
    { icon: TrendingUp, label: 'Resistance', value: levels.resistance != null ? formatPoints(levels.resistance) : '—', color: levels.resistance ? 'text-red-500' : '' },
    { icon: TrendingDown, label: 'Support', value: levels.support != null ? formatPoints(levels.support) : '—', color: levels.support ? 'text-green-500' : '' },
    { icon: BarChart3, label: 'PCR', value: levels.pcr != null ? levels.pcr.toFixed(2) : '—', color: levels.pcr != null && levels.pcr > 1 ? 'text-green-500' : levels.pcr != null && levels.pcr < 0.7 ? 'text-red-500' : '' },
    { icon: DollarSign, label: 'FII', value: formatCr(levels.fii_cr), color: levels.fii_cr != null && levels.fii_cr > 0 ? 'text-green-500' : levels.fii_cr != null && levels.fii_cr < 0 ? 'text-red-500' : '' },
  ]
  return (
    <div className="grid grid-cols-4 gap-2">
      {items.map((item) => (
        <div key={item.label} className="flex flex-col items-center gap-0.5 p-2 rounded-lg bg-gray-50 dark:bg-[#131620] border border-gray-200 dark:border-gray-800">
          <item.icon size={14} className={item.color || 'text-gray-400 dark:text-gray-500'} />
          <span className="text-[10px] text-gray-400 dark:text-gray-500 font-medium">{item.label}</span>
          <span className={`text-xs font-mono font-semibold ${item.color || 'text-gray-900 dark:text-gray-100'}`}>{item.value}</span>
        </div>
      ))}
    </div>
  )
}

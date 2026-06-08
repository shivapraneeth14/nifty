import { TrendingUp, TrendingDown } from 'lucide-react'
import type { KeyLevels } from '../../types/brief'
import { formatPoints } from '../../utils/formatters'

interface Props {
  levels: KeyLevels | null
  index?: string
}

export default function KeyLevelsPanel({ levels, index = 'Nifty' }: Props) {
  if (!levels) return null
  const items = [
    { icon: TrendingUp, label: 'Resistance', value: levels.resistance != null ? formatPoints(levels.resistance) : '—', color: levels.resistance ? 'text-red-500' : '' },
    { icon: TrendingDown, label: 'Support', value: levels.support != null ? formatPoints(levels.support) : '—', color: levels.support ? 'text-green-500' : '' },
  ]
  return (
    <div className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-4 space-y-2">
      <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100">{index} Key Levels</h3>
      <div className="grid grid-cols-2 gap-2">
        {items.map((item) => (
          <div key={item.label} className="flex flex-col items-center gap-0.5 p-3 rounded-lg bg-gray-50 dark:bg-[#131620] border border-gray-200 dark:border-gray-800">
            <item.icon size={16} className={item.color || 'text-gray-400 dark:text-gray-500'} />
            <span className="text-[10px] text-gray-400 dark:text-gray-500 font-medium">{item.label}</span>
            <span className={`text-sm font-mono font-bold ${item.color || 'text-gray-900 dark:text-gray-100'}`}>{item.value}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

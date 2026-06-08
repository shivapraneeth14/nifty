import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown, DollarSign, BarChart3 } from 'lucide-react'
import type { GlobalMarketPulse } from '../../types/brief'
import { fetchGlobalMarketPulse } from '../../services/global_market'

export default function GlobalMarketPulse() {
  const [data, setData] = useState<GlobalMarketPulse | null>(null)

  useEffect(() => { fetchGlobalMarketPulse().then(setData).catch(() => {}) }, [])

  if (!data) return null

  const items = [
    { label: 'SGX Nifty', price: data.sgx_nifty.price, chg: data.sgx_nifty.change_pct, icon: TrendingUp },
    { label: 'Dow Futures', price: data.dow_futures.price, chg: data.dow_futures.change_pct, icon: TrendingDown },
    { label: 'Crude Oil', price: data.crude_oil.price, chg: data.crude_oil.change_pct, icon: DollarSign },
    { label: 'USD/INR', price: data.usd_inr.price, chg: data.usd_inr.change_pct, icon: BarChart3 },
  ]

  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-4 space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100">Global Market Pulse</h3>
        <span className="text-[10px] text-gray-400">Pre-market</span>
      </div>
      <div className="grid grid-cols-2 gap-2">
        {items.map((item) => (
          <div key={item.label} className="rounded-lg bg-gray-50 dark:bg-[#131620] p-2">
            <div className="flex items-center gap-1 text-[10px] text-gray-400 dark:text-gray-500 mb-0.5">
              <item.icon size={10} />
              <span>{item.label}</span>
            </div>
            <div className="text-sm font-semibold font-mono text-gray-900 dark:text-gray-100">
              {item.price ?? '—'}
            </div>
            {item.chg != null && (
              <div className={`text-[10px] font-mono font-medium ${item.chg > 0 ? 'text-green-500' : item.chg < 0 ? 'text-red-500' : 'text-gray-400'}`}>
                {item.chg > 0 ? '+' : ''}{item.chg.toFixed(1)}%
              </div>
            )}
          </div>
        ))}
      </div>
      {data.summary && (
        <p className="text-[10px] text-gray-400 dark:text-gray-500 leading-relaxed">{data.summary}</p>
      )}
    </motion.div>
  )
}

import { motion } from 'framer-motion'
import { useTheme } from '../config/theme'
import { Sun, Moon, Globe, Bell, Shield, ChevronRight } from 'lucide-react'

export default function SettingsScreen() {
  const { theme, toggle } = useTheme()
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6 pb-24">
      <h1 className="text-lg font-bold text-gray-900 dark:text-gray-100">Settings</h1>
      <section className="space-y-1">
        <div className="flex items-center justify-between rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-4">
          <div className="flex items-center gap-3"><Globe size={18} className="text-gray-400" /></div>
          <div><p className="text-sm font-medium text-gray-900 dark:text-gray-100">Brief Language</p><p className="text-xs text-gray-400 dark:text-gray-500">English</p></div>
          <ChevronRight size={16} className="text-gray-400" />
        </div>
        <div className="flex items-center justify-between rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-4">
          <div className="flex items-center gap-3"><Bell size={18} className="text-gray-400" /></div>
          <div><p className="text-sm font-medium text-gray-900 dark:text-gray-100">Pre-market alert</p><p className="text-xs text-gray-400 dark:text-gray-500">8:45 AM daily</p></div>
          <label className="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" className="sr-only peer" defaultChecked />
            <div className="w-9 h-5 bg-gray-200 dark:bg-gray-700 rounded-full peer peer-checked:bg-indigo-500 after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:after:translate-x-full" />
          </label>
        </div>
        <div className="flex items-center justify-between rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-4">
          <div className="flex items-center gap-3">{theme === 'dark' ? <Sun size={18} className="text-gray-400" /> : <Moon size={18} className="text-gray-400" />}</div>
          <div><p className="text-sm font-medium text-gray-900 dark:text-gray-100">Appearance</p><p className="text-xs text-gray-400 dark:text-gray-500 capitalize">{theme} mode</p></div>
          <button onClick={toggle} className="px-3 py-1 text-xs font-medium rounded-lg bg-gray-50 dark:bg-[#131620] border border-gray-200 dark:border-gray-800 text-gray-900 dark:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">Toggle</button>
        </div>
      </section>
      <section className="rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-[#1A1D28] p-4">
        <div className="flex items-center gap-2 text-xs text-gray-400 dark:text-gray-500"><Shield size={14} /><span>Nifty Brief v1.0 · Built with FinBERT</span></div>
      </section>
    </motion.div>
  )
}

import { Link, useLocation } from 'react-router-dom'
import { LayoutDashboard, Newspaper, History, ChartSpline, Settings } from 'lucide-react'

const tabs = [
  { label: 'Brief', path: '/', icon: LayoutDashboard },
  { label: 'Feed', path: '/feed', icon: Newspaper },
  { label: 'History', path: '/history', icon: History },
  { label: 'Accuracy', path: '/accuracy', icon: ChartSpline },
  { label: 'Settings', path: '/settings', icon: Settings },
]

export default function TabBar() {
  const location = useLocation()

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 border-t border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-[#0B0D14]/80 backdrop-blur-xl">
      <div className="max-w-lg mx-auto flex">
        {tabs.map((t) => {
          const active = location.pathname === t.path
          const Icon = t.icon
          return (
            <Link
              key={t.path}
              to={t.path}
              className={`flex-1 flex flex-col items-center gap-0.5 py-2 text-[10px] font-medium transition-colors ${
                active ? 'text-indigo-500' : 'text-gray-400 dark:text-gray-500'
              }`}
            >
              <Icon size={18} strokeWidth={active ? 2.5 : 1.5} />
              {t.label}
            </Link>
          )
        })}
      </div>
    </nav>
  )
}

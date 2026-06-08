import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom'
import BriefPage from './pages/BriefPage'
import FeedPage from './pages/FeedPage'
import HistoryPage from './pages/HistoryPage'
import ArticleDetailPage from './pages/ArticleDetailPage'
import SettingsPage from './pages/SettingsPage'

const tabs = [
  { label: 'Brief', path: '/' },
  { label: 'Feed', path: '/feed' },
  { label: 'History', path: '/history' },
  { label: 'Settings', path: '/settings' },
]

function Nav() {
  const location = useLocation()
  return (
    <nav className="flex border-b border-gray-200 bg-white sticky top-0 z-10">
      {tabs.map((t) => {
        const active = location.pathname === t.path
        return (
          <Link
            key={t.path}
            to={t.path}
            className={`flex-1 text-center py-3 text-sm font-medium ${
              active
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {t.label}
          </Link>
        )
      })}
    </nav>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="max-w-lg mx-auto bg-white min-h-screen shadow-sm">
        <Nav />
        <div className="p-4">
          <Routes>
            <Route path="/" element={<BriefPage />} />
            <Route path="/feed" element={<FeedPage />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/article/:id" element={<ArticleDetailPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  )
}

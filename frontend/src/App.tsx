import { BrowserRouter, Routes, Route } from 'react-router-dom'
import BriefScreen from './screens/BriefScreen'
import FeedScreen from './screens/FeedScreen'
import HistoryScreen from './screens/HistoryScreen'
import AccuracyScreen from './screens/AccuracyScreen'
import DebriefScreen from './screens/DebriefScreen'
import SettingsScreen from './screens/SettingsScreen'
import TabBar from './components/ui/TabBar'

export default function App() {
  return (
    <BrowserRouter>
      <div className="max-w-lg mx-auto min-h-screen bg-white dark:bg-[#0B0D14] transition-colors duration-300">
        <div className="p-4">
          <Routes>
            <Route path="/" element={<BriefScreen />} />
            <Route path="/feed" element={<FeedScreen />} />
            <Route path="/history" element={<HistoryScreen />} />
            <Route path="/accuracy" element={<AccuracyScreen />} />
            <Route path="/debrief" element={<DebriefScreen />} />
            <Route path="/settings" element={<SettingsScreen />} />
          </Routes>
        </div>
        <TabBar />
      </div>
    </BrowserRouter>
  )
}

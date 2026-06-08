export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-lg font-bold">Settings</h1>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Brief Language</label>
        <select className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm">
          <option>English</option>
          <option disabled>Hindi (coming soon)</option>
          <option disabled>Telugu (coming soon)</option>
          <option disabled>Tamil (coming soon)</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Pre-market alert time</label>
        <select className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm">
          <option>8:45 AM</option>
          <option>8:30 AM</option>
          <option>8:00 AM</option>
        </select>
      </div>

      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-gray-700">Breaking news alerts</span>
        <label className="relative inline-flex items-center cursor-pointer">
          <input type="checkbox" className="sr-only peer" defaultChecked />
          <div className="w-9 h-5 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-blue-600"></div>
        </label>
      </div>

      <div className="pt-4 border-t border-gray-200">
        <p className="text-xs text-gray-400">
          Nifty Brief v1.0.0
        </p>
      </div>
    </div>
  )
}

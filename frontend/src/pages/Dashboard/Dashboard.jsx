import { useEffect, useState } from 'react'
import { FaBullseye, FaChartLine, FaLeaf, FaSeedling, FaTriangleExclamation } from 'react-icons/fa6'
import DashboardCard from '../../components/DashboardCard/DashboardCard'
import HistoryTable from '../../components/HistoryTable/HistoryTable'
import Loader from '../../components/Loader/Loader'
import { dashboardService } from '../../services/dashboardService'
import { formatPercent } from '../../utils/helpers'

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    dashboardService.getStats().then(setStats).finally(() => setLoading(false))
  }, [])

  if (loading) return <Loader />

  const cards = [
    ['Total Predictions', stats.totalPredictions, FaChartLine, 'from-slate-900 to-slate-600', 'All-time scans'],
    ['Healthy Plants', stats.healthyPlants, FaLeaf, 'from-canopy to-leaf', 'No disease detected'],
    ['Diseased Plants', stats.diseasedPlants, FaTriangleExclamation, 'from-amber-500 to-red-500', 'Needs attention'],
    ['Accuracy', formatPercent(stats.accuracy), FaBullseye, 'from-blue-500 to-cyan-500', 'Model confidence'],
  ]

  return (
    <section className="container-page py-10">
      <div className="mb-8 flex flex-col justify-between gap-4 lg:flex-row lg:items-end">
        <div>
          <p className="text-sm font-semibold uppercase tracking-normal text-canopy">Command center</p>
          <h1 className="mt-2 text-4xl font-bold">Dashboard</h1>
          <p className="section-subtitle">Monitor scans, accuracy, disease pressure, and recent prediction activity.</p>
        </div>
        <div className="card min-w-64">
          <p className="text-sm text-slate-500">Most common disease</p>
          <p className="mt-2 flex items-center gap-2 text-xl font-bold"><FaSeedling className="text-canopy" /> {stats.mostCommonDisease}</p>
        </div>
      </div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {cards.map(([title, value, Icon, tone, caption]) => (
          <DashboardCard key={title} title={title} value={value} icon={Icon} tone={tone} caption={caption} />
        ))}
      </div>
      <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_360px]">
        <section className="card">
          <h2 className="text-xl font-bold">Prediction Trends</h2>
          <div className="mt-6 flex h-64 items-end gap-3">
            {(stats.trends || []).map((value, index) => (
              <div key={index} className="flex flex-1 flex-col items-center gap-2">
                <div className="w-full rounded-t-lg bg-gradient-to-t from-canopy to-leaf" style={{ height: `${Math.max(12, value)}%` }} />
                <span className="text-xs text-slate-500">D{index + 1}</span>
              </div>
            ))}
          </div>
        </section>
        <section className="card">
          <h2 className="text-xl font-bold">User Statistics</h2>
          <div className="mt-5 grid gap-3">
            {Object.entries(stats.userStatistics || {}).map(([key, value]) => (
              <div key={key} className="flex items-center justify-between rounded-lg bg-slate-50 p-4 dark:bg-white/5">
                <span className="capitalize text-slate-600 dark:text-slate-300">{key.replace(/([A-Z])/g, ' $1')}</span>
                <strong>{typeof value === 'number' && key.toLowerCase().includes('confidence') ? formatPercent(value) : value}</strong>
              </div>
            ))}
          </div>
        </section>
      </div>
      <div className="mt-6">
        <h2 className="mb-4 text-xl font-bold">Recent Predictions</h2>
        <HistoryTable records={stats.recentPredictions || []} />
      </div>
    </section>
  )
}

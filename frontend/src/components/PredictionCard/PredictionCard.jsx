import { FaChartSimple, FaLeaf, FaSeedling, FaTriangleExclamation } from 'react-icons/fa6'
import { formatPercent } from '../../utils/helpers'

export default function PredictionCard({ prediction }) {
  if (!prediction) return null
  const isHealthy = prediction.diseaseName?.toLowerCase().includes('healthy')
  return (
    <article className="glass rounded-lg p-5">
      <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex items-start gap-4">
          <div className={`grid h-14 w-14 place-items-center rounded-lg ${isHealthy ? 'bg-leaf/15 text-canopy' : 'bg-amber-100 text-amber-700'}`}>
            {isHealthy ? <FaLeaf /> : <FaTriangleExclamation />}
          </div>
          <div>
            <p className="text-sm font-semibold uppercase tracking-normal text-canopy">Prediction result</p>
            <h2 className="mt-1 text-2xl font-bold">{prediction.diseaseName}</h2>
            <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">Detected on {prediction.plantName}</p>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
          <Metric icon={FaSeedling} label="Plant" value={prediction.plantName} />
          <Metric icon={FaChartSimple} label="Confidence" value={formatPercent(prediction.confidenceScore)} />
          <Metric icon={FaTriangleExclamation} label="Severity" value={prediction.severityLevel} />
        </div>
      </div>
    </article>
  )
}

function Metric({ icon: Icon, label, value }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white/70 p-4 dark:border-white/10 dark:bg-white/5">
      <div className="mb-2 flex items-center gap-2 text-xs font-semibold uppercase tracking-normal text-slate-500">
        <Icon /> {label}
      </div>
      <p className="text-sm font-bold text-slate-950 dark:text-white">{value}</p>
    </div>
  )
}

import { FaCircleInfo, FaSeedling, FaShieldHeart, FaTriangleExclamation } from 'react-icons/fa6'

const sections = [
  ['Symptoms', 'symptoms', FaTriangleExclamation],
  ['Causes', 'causes', FaCircleInfo],
  ['Prevention', 'prevention', FaShieldHeart],
]

export default function DiseaseInfoCard({ prediction }) {
  if (!prediction) return null
  return (
    <section className="card">
      <div className="flex items-center gap-3">
        <span className="grid h-11 w-11 place-items-center rounded-lg bg-canopy/10 text-canopy">
          <FaSeedling />
        </span>
        <div>
          <h2 className="text-xl font-bold">Disease Intelligence</h2>
          <p className="text-sm text-slate-500 dark:text-slate-300">{prediction.diseaseDescription}</p>
        </div>
      </div>
      <div className="mt-6 grid gap-4 md:grid-cols-3">
        {sections.map(([title, key, Icon]) => (
          <div key={key} className="rounded-lg border border-slate-200 p-4 dark:border-white/10">
            <div className="mb-3 flex items-center gap-2 font-semibold">
              <Icon className="text-canopy" /> {title}
            </div>
            <ul className="space-y-2 text-sm text-slate-600 dark:text-slate-300">
              {(prediction[key]?.length ? prediction[key] : ['No model notes returned.']).map((item) => (
                <li key={item} className="flex gap-2">
                  <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-leaf" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </section>
  )
}

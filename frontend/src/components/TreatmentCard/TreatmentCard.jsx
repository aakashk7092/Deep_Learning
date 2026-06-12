import { FaBottleDroplet, FaFlask, FaKitMedical } from 'react-icons/fa6'

export default function TreatmentCard({ prediction }) {
  if (!prediction) return null
  const groups = [
    ['Treatment', prediction.treatment, FaKitMedical],
    ['Recommended Fertilizers', prediction.recommendedFertilizers, FaBottleDroplet],
    ['Recommended Fungicides', prediction.recommendedFungicides, FaFlask],
  ]
  return (
    <section className="grid gap-4 lg:grid-cols-3">
      {groups.map(([title, items, Icon]) => (
        <article key={title} className="card">
          <div className="mb-4 flex items-center gap-3">
            <span className="grid h-10 w-10 place-items-center rounded-lg bg-leaf/15 text-canopy">
              <Icon />
            </span>
            <h3 className="font-bold">{title}</h3>
          </div>
          <ul className="space-y-3 text-sm text-slate-600 dark:text-slate-300">
            {(items?.length ? items : ['No recommendations returned.']).map((item) => (
              <li key={item} className="rounded-lg bg-slate-50 p-3 dark:bg-white/5">{item}</li>
            ))}
          </ul>
        </article>
      ))}
    </section>
  )
}

import { FaEnvelope, FaFlask, FaGithub, FaLeaf, FaNetworkWired } from 'react-icons/fa6'

export default function About() {
  return (
    <section className="container-page py-10">
      <div className="grid gap-8 lg:grid-cols-[1fr_0.8fr] lg:items-center">
        <div>
          <p className="text-sm font-semibold uppercase tracking-normal text-canopy">About the project</p>
          <h1 className="mt-3 text-5xl font-extrabold tracking-normal">AI plant care for earlier disease response.</h1>
          <p className="mt-5 text-lg leading-8 text-slate-600 dark:text-slate-300">
            PlantGuard AI is a frontend for a plant disease detection backend that combines secure user workflows, image-based inference, and actionable agronomy guidance.
          </p>
        </div>
        <div className="glass rounded-lg p-6">
          <img src="/logo.png" alt="PlantGuard AI logo" className="mx-auto h-28 w-28 rounded-lg object-contain" />
          <div className="mt-6 grid gap-3">
            {['React 19 + Vite', 'JWT protected routes', 'Axios API services', 'Responsive Tailwind UI'].map((item) => (
              <div key={item} className="rounded-lg bg-white/70 p-3 text-sm font-semibold dark:bg-white/10">{item}</div>
            ))}
          </div>
        </div>
      </div>

      <div className="mt-16 grid gap-4 md:grid-cols-3">
        {[
          ['Model Details', 'Designed for CNN or transformer-based image classifiers returning disease metadata and confidence.', FaNetworkWired],
          ['Research Workflow', 'History, dashboard, and treatment cards support comparison and repeat analysis.', FaFlask],
          ['Farmer Friendly', 'Clear severity, prevention, and treatment steps support field-ready action.', FaLeaf],
        ].map(([title, text, Icon]) => (
          <article key={title} className="card">
            <div className="grid h-12 w-12 place-items-center rounded-lg bg-canopy/10 text-canopy"><Icon /></div>
            <h2 className="mt-5 text-xl font-bold">{title}</h2>
            <p className="mt-3 text-sm leading-6 text-slate-600 dark:text-slate-300">{text}</p>
          </article>
        ))}
      </div>

      <div className="mt-16">
        <h2 className="section-title">Team</h2>
        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {['AI Engineer', 'Frontend Engineer', 'Agronomy Advisor'].map((role) => (
            <article key={role} className="card">
              <div className="h-20 w-20 rounded-full bg-gradient-to-br from-canopy to-leaf" />
              <h3 className="mt-4 font-bold">{role}</h3>
              <p className="mt-2 text-sm text-slate-500">Plant disease detection system contributor</p>
            </article>
          ))}
        </div>
      </div>

      <div className="mt-16 card">
        <h2 className="text-2xl font-bold">Contact</h2>
        <div className="mt-5 flex flex-col gap-3 sm:flex-row">
          <a className="btn-secondary" href="mailto:hello@plantguard.ai"><FaEnvelope /> hello@plantguard.ai</a>
          <a className="btn-secondary" href="https://github.com" target="_blank" rel="noreferrer"><FaGithub /> GitHub</a>
        </div>
      </div>
    </section>
  )
}

import { Link } from 'react-router-dom'
import { FaGithub, FaLeaf, FaShieldHalved } from 'react-icons/fa6'

export default function Footer() {
  return (
    <footer className="border-t border-slate-200 bg-white/70 py-10 dark:border-white/10 dark:bg-white/[0.03]">
      <div className="container-page grid gap-8 md:grid-cols-[1.5fr_1fr_1fr]">
        <div>
          <Link to="/" className="inline-flex items-center gap-3 font-bold">
            <span className="grid h-10 w-10 place-items-center rounded-lg bg-canopy text-white">
              <FaLeaf />
            </span>
            PlantGuard AI
          </Link>
          <p className="mt-4 max-w-md text-sm leading-6 text-slate-600 dark:text-slate-300">
            AI-powered plant disease detection for faster field decisions, healthier crops, and clearer treatment plans.
          </p>
        </div>
        <div>
          <h3 className="text-sm font-semibold">Product</h3>
          <div className="mt-4 grid gap-3 text-sm text-slate-600 dark:text-slate-300">
            <Link to="/prediction">Disease detection</Link>
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/history">Prediction history</Link>
          </div>
        </div>
        <div>
          <h3 className="text-sm font-semibold">Trust</h3>
          <div className="mt-4 grid gap-3 text-sm text-slate-600 dark:text-slate-300">
            <span className="inline-flex items-center gap-2"><FaShieldHalved /> Secure JWT auth</span>
            <span className="inline-flex items-center gap-2"><FaGithub /> Research-ready UI</span>
          </div>
        </div>
      </div>
    </footer>
  )
}

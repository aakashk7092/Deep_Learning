import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { FaArrowRight, FaChartLine, FaLeaf, FaMicroscope, FaShieldHeart, FaStar } from 'react-icons/fa6'

const features = [
  ['Instant diagnosis', 'Upload a leaf image and receive disease, severity, and confidence insights.', FaMicroscope],
  ['Treatment guidance', 'Get prevention steps, fertilizers, and fungicides tied to the detected condition.', FaShieldHeart],
  ['Decision dashboard', 'Track trends, healthy scans, diseased plants, and common outbreak patterns.', FaChartLine],
]

const faqs = [
  ['Which crops are supported?', 'The interface is model-agnostic and displays any plant and disease returned by your backend model.'],
  ['Is my data secure?', 'JWT authentication is used for protected routes and API requests.'],
  ['Can this work in the field?', 'The responsive UI is optimized for mobile uploads and quick scan review.'],
]

export default function Home() {
  return (
    <>
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(48,199,123,0.22),transparent_35%),linear-gradient(135deg,rgba(15,143,98,0.08),transparent_40%)]" />
        <div className="container-page relative grid min-h-[calc(100vh-4rem)] items-center gap-10 py-16 lg:grid-cols-[1fr_0.9fr]">
          <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }}>
            <span className="inline-flex items-center gap-2 rounded-full border border-canopy/20 bg-canopy/10 px-4 py-2 text-sm font-semibold text-canopy">
              <FaLeaf /> AI-powered crop health intelligence
            </span>
            <h1 className="mt-6 max-w-4xl text-5xl font-extrabold tracking-normal text-slate-950 dark:text-white sm:text-6xl lg:text-7xl">
              Detect plant diseases before they spread.
            </h1>
            <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-600 dark:text-slate-300">
              PlantGuard AI turns leaf images into clear diagnosis, severity, treatment, and prevention plans for farmers, researchers, and agritech teams.
            </p>
            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <Link to="/prediction" className="btn-primary">
                Start detection <FaArrowRight />
              </Link>
              <Link to="/about" className="btn-secondary">Explore model</Link>
            </div>
          </motion.div>
          <motion.div initial={{ opacity: 0, scale: 0.96 }} animate={{ opacity: 1, scale: 1 }} className="relative">
            <div className="glass rounded-lg p-4">
              <img src="/hero-image.png" alt="Healthy crop field with plant disease detection interface" className="aspect-[4/3] w-full rounded-lg object-cover" />
              <div className="mt-4 grid grid-cols-3 gap-3">
                {['96.4% accuracy', '8 MB uploads', '24/7 scans'].map((item) => (
                  <div key={item} className="rounded-lg bg-white/80 p-3 text-center text-sm font-semibold dark:bg-white/10">{item}</div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      <section className="container-page py-20">
        <h2 className="section-title">Built for fast crop decisions</h2>
        <p className="section-subtitle">A polished workflow from image capture to action plan.</p>
        <div className="mt-10 grid gap-4 md:grid-cols-3">
          {features.map(([title, text, Icon]) => (
            <article key={title} className="card">
              <div className="grid h-12 w-12 place-items-center rounded-lg bg-canopy/10 text-canopy"><Icon /></div>
              <h3 className="mt-5 text-xl font-bold">{title}</h3>
              <p className="mt-3 text-sm leading-6 text-slate-600 dark:text-slate-300">{text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="bg-white/70 py-20 dark:bg-white/[0.03]">
        <div className="container-page">
          <h2 className="section-title">How it works</h2>
          <div className="mt-10 grid gap-4 md:grid-cols-3">
            {['Upload a clear leaf photo', 'AI model analyzes visual symptoms', 'Review diagnosis and treatment plan'].map((step, index) => (
              <div key={step} className="card">
                <div className="mb-5 grid h-10 w-10 place-items-center rounded-full bg-slate-950 font-bold text-white dark:bg-leaf dark:text-slate-950">{index + 1}</div>
                <h3 className="font-bold">{step}</h3>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="container-page py-20">
        <div className="grid gap-4 md:grid-cols-4">
          {['248 predictions', '156 diseased found', '92 healthy plants', '18 treatments saved'].map((stat) => (
            <div key={stat} className="glass rounded-lg p-6 text-center text-2xl font-bold">{stat}</div>
          ))}
        </div>
      </section>

      <section className="container-page py-20">
        <div className="grid gap-6 lg:grid-cols-2">
          <article className="card">
            <div className="flex gap-1 text-amber-400">{[1, 2, 3, 4, 5].map((item) => <FaStar key={item} />)}</div>
            <p className="mt-5 text-lg leading-8 text-slate-700 dark:text-slate-200">The upload-to-treatment flow helps our team triage plant samples much faster than spreadsheet logging.</p>
            <p className="mt-5 text-sm font-semibold">Aarav Mehta, Agritech Research Lead</p>
          </article>
          <article className="card">
            <div className="flex gap-1 text-amber-400">{[1, 2, 3, 4, 5].map((item) => <FaStar key={item} />)}</div>
            <p className="mt-5 text-lg leading-8 text-slate-700 dark:text-slate-200">The dashboard makes disease trends visible before they become expensive field problems.</p>
            <p className="mt-5 text-sm font-semibold">Neha Rao, Crop Advisor</p>
          </article>
        </div>
      </section>

      <section className="container-page pb-20">
        <h2 className="section-title">FAQ</h2>
        <div className="mt-8 grid gap-4">
          {faqs.map(([question, answer]) => (
            <details key={question} className="card">
              <summary className="cursor-pointer font-semibold">{question}</summary>
              <p className="mt-3 text-sm leading-6 text-slate-600 dark:text-slate-300">{answer}</p>
            </details>
          ))}
        </div>
      </section>
    </>
  )
}

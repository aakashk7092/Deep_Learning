import { useEffect, useState } from 'react'
import { Link, NavLink } from 'react-router-dom'
import { FaBars, FaLeaf, FaMoon, FaSun, FaUser, FaXmark } from 'react-icons/fa6'
import { AnimatePresence, motion } from 'framer-motion'
import useAuth from '../../hooks/useAuth'
import { navigationLinks, THEME_KEY } from '../../utils/constants'
import { classNames } from '../../utils/helpers'

export default function Navbar() {
  const [open, setOpen] = useState(false)
  const [dark, setDark] = useState(() => localStorage.getItem(THEME_KEY) === 'dark')
  const { isAuthenticated, user, logout } = useAuth()

  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark)
    localStorage.setItem(THEME_KEY, dark ? 'dark' : 'light')
  }, [dark])

  const visibleLinks = navigationLinks.filter((link) => isAuthenticated || !['/dashboard', '/history'].includes(link.path))

  return (
    <header className="sticky top-0 z-40 border-b border-slate-200/80 bg-white/80 backdrop-blur-xl dark:border-white/10 dark:bg-[#0c1110]/80">
      <nav className="container-page flex h-16 items-center justify-between gap-4">
        <Link to="/" className="flex items-center gap-3 font-bold">
          <span className="grid h-10 w-10 place-items-center rounded-lg bg-gradient-to-br from-canopy to-leaf text-white shadow-glow">
            <FaLeaf />
          </span>
          <span>PlantGuard AI</span>
        </Link>
        <div className="hidden items-center gap-1 lg:flex">
          {visibleLinks.map((link) => (
            <NavLink
              key={link.path}
              to={link.path}
              className={({ isActive }) =>
                classNames(
                  'rounded-full px-4 py-2 text-sm font-medium transition',
                  isActive ? 'bg-canopy/10 text-canopy' : 'text-slate-600 hover:text-canopy dark:text-slate-300',
                )
              }
            >
              {link.label}
            </NavLink>
          ))}
        </div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            aria-label="Toggle theme"
            onClick={() => setDark((value) => !value)}
            className="grid h-10 w-10 place-items-center rounded-full border border-slate-200 bg-white text-slate-700 dark:border-white/10 dark:bg-white/10 dark:text-white"
          >
            {dark ? <FaSun /> : <FaMoon />}
          </button>
          {isAuthenticated ? (
            <div className="hidden items-center gap-2 sm:flex">
              <Link to="/profile" className="btn-secondary py-2">
                <FaUser /> {user?.name?.split(' ')[0] || 'Profile'}
              </Link>
              <button type="button" onClick={logout} className="btn-primary py-2">Logout</button>
            </div>
          ) : (
            <div className="hidden items-center gap-2 sm:flex">
              <Link to="/login" className="btn-secondary py-2">Login</Link>
              <Link to="/register" className="btn-primary py-2">Start free</Link>
            </div>
          )}
          <button
            type="button"
            aria-label="Open menu"
            onClick={() => setOpen(true)}
            className="grid h-10 w-10 place-items-center rounded-full border border-slate-200 lg:hidden dark:border-white/10"
          >
            <FaBars />
          </button>
        </div>
      </nav>
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-slate-950/40 lg:hidden"
            onClick={() => setOpen(false)}
          >
            <motion.div
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              className="ml-auto h-full w-80 max-w-[86vw] bg-white p-5 shadow-soft dark:bg-[#101615]"
              onClick={(event) => event.stopPropagation()}
            >
              <div className="flex items-center justify-between">
                <span className="font-bold">Menu</span>
                <button type="button" aria-label="Close menu" onClick={() => setOpen(false)} className="grid h-10 w-10 place-items-center rounded-full border border-slate-200 dark:border-white/10">
                  <FaXmark />
                </button>
              </div>
              <div className="mt-8 grid gap-2">
                {visibleLinks.map((link) => (
                  <NavLink key={link.path} to={link.path} onClick={() => setOpen(false)} className="rounded-lg px-4 py-3 font-medium hover:bg-canopy/10">
                    {link.label}
                  </NavLink>
                ))}
                {isAuthenticated ? (
                  <>
                    <Link to="/profile" onClick={() => setOpen(false)} className="rounded-lg px-4 py-3 font-medium hover:bg-canopy/10">Profile</Link>
                    <button type="button" onClick={() => { logout(); setOpen(false) }} className="btn-primary mt-4">Logout</button>
                  </>
                ) : (
                  <div className="mt-4 grid gap-3">
                    <Link to="/login" onClick={() => setOpen(false)} className="btn-secondary">Login</Link>
                    <Link to="/register" onClick={() => setOpen(false)} className="btn-primary">Create account</Link>
                  </div>
                )}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  )
}

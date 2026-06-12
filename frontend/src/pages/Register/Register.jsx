import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { FaEye, FaEyeSlash, FaLeaf } from 'react-icons/fa6'
import useAuth from '../../hooks/useAuth'
import { validateAuthForm } from '../../utils/validators'

export default function Register() {
  const [form, setForm] = useState({ name: '', email: '', password: '' })
  const [show, setShow] = useState(false)
  const [errors, setErrors] = useState({})
  const { register, loading } = useAuth()
  const navigate = useNavigate()

  const submit = async (event) => {
    event.preventDefault()
    const nextErrors = validateAuthForm(form, 'register')
    setErrors(nextErrors)
    if (Object.keys(nextErrors).length) return
    try {
      await register(form)
      navigate('/dashboard')
    } catch (error) {
      toast.error(error.message)
    }
  }

  return (
    <section className="container-page grid min-h-[calc(100vh-4rem)] place-items-center py-12">
      <form onSubmit={submit} className="glass w-full max-w-md rounded-lg p-6">
        <div className="mb-8 text-center">
          <div className="mx-auto grid h-12 w-12 place-items-center rounded-lg bg-canopy text-white"><FaLeaf /></div>
          <h1 className="mt-4 text-3xl font-bold">Create your account</h1>
          <p className="mt-2 text-sm text-slate-500 dark:text-slate-300">Start tracking plant health with AI assistance.</p>
        </div>
        <Field label="Full name" error={errors.name}>
          <input className="input-field" value={form.name} onChange={(event) => setForm({ ...form, name: event.target.value })} autoComplete="name" />
        </Field>
        <Field label="Email" error={errors.email}>
          <input className="input-field" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} type="email" autoComplete="email" />
        </Field>
        <Field label="Password" error={errors.password}>
          <div className="relative">
            <input className="input-field pr-12" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} type={show ? 'text' : 'password'} autoComplete="new-password" />
            <button type="button" aria-label="Toggle password visibility" onClick={() => setShow((value) => !value)} className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500">
              {show ? <FaEyeSlash /> : <FaEye />}
            </button>
          </div>
        </Field>
        <button disabled={loading} className="btn-primary mt-3 w-full disabled:opacity-60">{loading ? 'Creating account...' : 'Register'}</button>
        <p className="mt-5 text-center text-sm text-slate-500">Already registered? <Link to="/login" className="font-semibold text-canopy">Login</Link></p>
      </form>
    </section>
  )
}

function Field({ label, error, children }) {
  return (
    <label className="mb-4 block">
      <span className="mb-2 block text-sm font-semibold">{label}</span>
      {children}
      {error && <span className="mt-1 block text-sm text-red-600">{error}</span>}
    </label>
  )
}

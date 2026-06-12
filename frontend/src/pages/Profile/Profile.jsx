import { useState } from 'react'
import toast from 'react-hot-toast'
import { FaCamera, FaLock, FaUserPen } from 'react-icons/fa6'
import useAuth from '../../hooks/useAuth'
import { initials } from '../../utils/helpers'

export default function Profile() {
  const { user, updateProfile, loading } = useAuth()
  const [form, setForm] = useState({
    name: user?.name || '',
    email: user?.email || '',
    phone: user?.phone || '',
    role: user?.role || 'Crop Specialist',
  })
  const [password, setPassword] = useState({ currentPassword: '', newPassword: '' })

  const saveProfile = async (event) => {
    event.preventDefault()
    try {
      await updateProfile(form)
    } catch (error) {
      toast.error(error.message)
    }
  }

  const changePassword = (event) => {
    event.preventDefault()
    if (password.newPassword.length < 8) return toast.error('New password must be at least 8 characters.')
    toast.success('Password change request is ready for backend integration.')
    setPassword({ currentPassword: '', newPassword: '' })
  }

  return (
    <section className="container-page py-10">
      <div className="mb-8">
        <p className="text-sm font-semibold uppercase tracking-normal text-canopy">Account</p>
        <h1 className="mt-2 text-4xl font-bold">Profile</h1>
      </div>
      <div className="grid gap-6 lg:grid-cols-[340px_1fr]">
        <aside className="card text-center">
          <div className="relative mx-auto grid h-28 w-28 place-items-center rounded-full bg-gradient-to-br from-canopy to-leaf text-3xl font-bold text-white">
            {initials(form.name || form.email)}
            <button aria-label="Upload avatar" className="absolute bottom-0 right-0 grid h-10 w-10 place-items-center rounded-full border-4 border-white bg-slate-950 text-sm text-white dark:border-[#101615]">
              <FaCamera />
            </button>
          </div>
          <h2 className="mt-5 text-2xl font-bold">{form.name || 'Plant Expert'}</h2>
          <p className="mt-1 text-sm text-slate-500">{form.role}</p>
          <div className="mt-6 grid grid-cols-3 gap-3 text-center">
            {['248 scans', '96% avg', '18 saved'].map((item) => <div key={item} className="rounded-lg bg-slate-50 p-3 text-sm font-semibold dark:bg-white/5">{item}</div>)}
          </div>
        </aside>
        <div className="grid gap-6">
          <form onSubmit={saveProfile} className="card">
            <h2 className="mb-5 flex items-center gap-2 text-xl font-bold"><FaUserPen className="text-canopy" /> Edit Profile</h2>
            <div className="grid gap-4 md:grid-cols-2">
              {[
                ['Name', 'name'],
                ['Email', 'email'],
                ['Phone', 'phone'],
                ['Role', 'role'],
              ].map(([label, key]) => (
                <label key={key}>
                  <span className="mb-2 block text-sm font-semibold">{label}</span>
                  <input className="input-field" value={form[key]} onChange={(event) => setForm({ ...form, [key]: event.target.value })} />
                </label>
              ))}
            </div>
            <button disabled={loading} className="btn-primary mt-5 disabled:opacity-60">Save changes</button>
          </form>
          <form onSubmit={changePassword} className="card">
            <h2 className="mb-5 flex items-center gap-2 text-xl font-bold"><FaLock className="text-canopy" /> Change Password</h2>
            <div className="grid gap-4 md:grid-cols-2">
              <input className="input-field" type="password" placeholder="Current password" value={password.currentPassword} onChange={(event) => setPassword({ ...password, currentPassword: event.target.value })} />
              <input className="input-field" type="password" placeholder="New password" value={password.newPassword} onChange={(event) => setPassword({ ...password, newPassword: event.target.value })} />
            </div>
            <button className="btn-secondary mt-5">Update password</button>
          </form>
        </div>
      </div>
    </section>
  )
}

import { useCallback, useEffect, useMemo, useState } from 'react'
import toast from 'react-hot-toast'
import { authService } from '../services/authService'
import { TOKEN_KEY, USER_KEY } from '../utils/constants'
import { AuthContext } from './authContextValue'

const getStoredUser = () => {
  try {
    return JSON.parse(localStorage.getItem(USER_KEY)) || null
  } catch {
    return null
  }
}

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY))
  const [user, setUser] = useState(getStoredUser)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (token) localStorage.setItem(TOKEN_KEY, token)
    else localStorage.removeItem(TOKEN_KEY)
  }, [token])

  useEffect(() => {
    if (user) localStorage.setItem(USER_KEY, JSON.stringify(user))
    else localStorage.removeItem(USER_KEY)
  }, [user])

  const persistSession = (payload) => {
    const nextToken = payload.token || payload.accessToken || payload.access_token || payload.jwt || payload.data?.access_token
    const rawUser = payload.user || payload.data?.user || {
      full_name: payload.name || 'Plant Expert',
      email: payload.email || 'farmer@example.com',
    }
    const nextUser = {
      ...rawUser,
      name: rawUser.name || rawUser.full_name,
    }
    if (!nextToken) throw new Error('Authentication token was not returned.')
    setToken(nextToken)
    setUser(nextUser)
    return nextUser
  }

  const login = useCallback(async (credentials) => {
    setLoading(true)
    try {
      const data = await authService.login(credentials)
      const nextUser = persistSession(data)
      toast.success(`Welcome back, ${nextUser.name?.split(' ')[0] || 'there'}.`)
      return nextUser
    } finally {
      setLoading(false)
    }
  }, [])

  const register = useCallback(async (payload) => {
    setLoading(true)
    try {
      const data = await authService.register(payload)
      const nextUser = persistSession(data)
      toast.success('Account created successfully.')
      return nextUser
    } finally {
      setLoading(false)
    }
  }, [])

  const updateProfile = useCallback(async (payload) => {
    setLoading(true)
    try {
      const data = await authService.updateProfile(payload)
      let nextUser
      setUser((currentUser) => {
        const rawUser = data.user || data.data || { ...currentUser, ...payload }
        nextUser = { ...rawUser, name: rawUser.name || rawUser.full_name }
        return nextUser
      })
      toast.success('Profile updated.')
      return nextUser
    } finally {
      setLoading(false)
    }
  }, [])

  const logout = () => {
    setToken(null)
    setUser(null)
    toast.success('Signed out.')
  }

  const value = useMemo(
    () => ({
      token,
      user,
      loading,
      isAuthenticated: Boolean(token),
      login,
      register,
      logout,
      updateProfile,
      setUser,
    }),
    [token, user, loading, login, register, updateProfile],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

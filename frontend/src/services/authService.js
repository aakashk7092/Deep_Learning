import api from './api'

const toProfilePayload = (payload) => {
  const rest = { ...payload }
  const { name } = rest
  delete rest.name
  delete rest.email
  delete rest.phone
  delete rest.role
  return {
    ...rest,
    ...(name !== undefined ? { full_name: name } : {}),
  }
}

export const authService = {
  async register(payload) {
    const { data } = await api.post('/api/auth/register', toProfilePayload(payload))
    return data
  },

  async login(payload) {
    const { data } = await api.post('/api/auth/login', payload)
    return data
  },

  async getProfile() {
    const { data } = await api.get('/api/auth/me')
    return data
  },

  async updateProfile(payload) {
    const { data } = await api.put('/api/auth/profile', toProfilePayload(payload))
    return data
  },
}

import axios from 'axios'
import { API_BASE_URL, TOKEN_KEY } from '../utils/constants'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY)
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const detail = error.response?.data?.detail
    const validationMessage = Array.isArray(detail)
      ? detail.map((item) => item.msg).filter(Boolean).join(' ')
      : detail?.message
    const message =
      validationMessage ||
      error.response?.data?.message ||
      error.response?.data?.error ||
      error.message ||
      'Something went wrong.'
    return Promise.reject(new Error(message))
  },
)

export default api

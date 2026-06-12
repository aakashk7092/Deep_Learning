import api from './api'
import { mockHistory } from '../utils/constants'
import { normalizePrediction } from '../utils/helpers'

export const predictionService = {
  async predict(file, onUploadProgress) {
    const formData = new FormData()
    formData.append('file', file)
    const { data } = await api.post('/api/predictions/predict', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress,
    })
    return normalizePrediction(data)
  },

  async getHistory() {
    try {
      const { data } = await api.get('/api/predictions/history')
      const records = Array.isArray(data) ? data : data.predictions || data.data?.items || data.data || []
      return records.map(normalizePrediction)
    } catch {
      return mockHistory.map(normalizePrediction)
    }
  },

  async deletePrediction(id) {
    const { data } = await api.delete(`/api/predictions/${id}`)
    return data
  },
}

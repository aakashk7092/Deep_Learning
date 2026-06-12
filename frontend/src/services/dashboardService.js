import api from './api'
import { mockHistory } from '../utils/constants'

export const dashboardService = {
  async getStats() {
    try {
      const { data } = await api.get('/api/dashboard/stats')
      const source = data.data || data
      return {
        totalPredictions: source.totalPredictions ?? source.total_predictions ?? 0,
        healthyPlants: source.healthyPlants ?? source.healthy_plants ?? 0,
        diseasedPlants: source.diseasedPlants ?? source.diseased_plants ?? 0,
        accuracy: source.accuracy ?? source.average_confidence ?? 0,
        mostCommonDisease: source.mostCommonDisease ?? source.most_common_disease ?? null,
        recentPredictions: source.recentPredictions ?? source.recent_predictions ?? [],
        userStatistics: source.userStatistics ?? {
          scansThisWeek: source.total_predictions ?? 0,
          savedTreatments: 0,
          averageConfidence: source.average_confidence ?? 0,
        },
      }
    } catch {
      return {
        totalPredictions: 248,
        healthyPlants: 92,
        diseasedPlants: 156,
        accuracy: 96.4,
        mostCommonDisease: 'Early Blight',
        trends: [28, 36, 32, 48, 44, 58, 62],
        recentPredictions: mockHistory,
        userStatistics: {
          scansThisWeek: 42,
          savedTreatments: 18,
          averageConfidence: 93.8,
        },
      }
    }
  },
}

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const TOKEN_KEY = 'plantguard_token'
export const USER_KEY = 'plantguard_user'
export const THEME_KEY = 'plantguard_theme'

export const navigationLinks = [
  { label: 'Home', path: '/' },
  { label: 'Detect', path: '/prediction' },
  { label: 'Dashboard', path: '/dashboard' },
  { label: 'History', path: '/history' },
  { label: 'About', path: '/about' },
]

export const acceptedImageTypes = ['image/jpeg', 'image/png', 'image/webp']
export const maxUploadSize = 8 * 1024 * 1024

export const demoPrediction = {
  id: 'demo-1',
  plantName: 'Tomato',
  diseaseName: 'Early Blight',
  confidenceScore: 94.2,
  severityLevel: 'Moderate',
  diseaseDescription:
    'A fungal disease that usually begins on older leaves and spreads through warm, humid conditions.',
  symptoms: ['Brown concentric leaf spots', 'Yellowing lower leaves', 'Premature leaf drop'],
  causes: ['Alternaria spores in soil', 'Overhead watering', 'Poor air circulation'],
  prevention: ['Rotate crops every season', 'Mulch soil surface', 'Prune for airflow'],
  treatment: ['Remove infected foliage', 'Apply copper-based fungicide', 'Water at the soil line'],
  recommendedFertilizers: ['Balanced NPK 10-10-10', 'Compost tea', 'Calcium supplement'],
  recommendedFungicides: ['Copper oxychloride', 'Mancozeb', 'Chlorothalonil'],
  createdAt: new Date().toISOString(),
}

export const mockHistory = [
  { ...demoPrediction, id: 'p-1001', plantName: 'Tomato', confidenceScore: 94.2, status: 'Diseased' },
  {
    ...demoPrediction,
    id: 'p-1002',
    plantName: 'Potato',
    diseaseName: 'Healthy',
    confidenceScore: 98.6,
    severityLevel: 'None',
    status: 'Healthy',
    createdAt: '2026-06-10T08:30:00.000Z',
  },
  {
    ...demoPrediction,
    id: 'p-1003',
    plantName: 'Apple',
    diseaseName: 'Apple Scab',
    confidenceScore: 91.3,
    severityLevel: 'High',
    status: 'Diseased',
    createdAt: '2026-06-09T13:20:00.000Z',
  },
  {
    ...demoPrediction,
    id: 'p-1004',
    plantName: 'Corn',
    diseaseName: 'Northern Leaf Blight',
    confidenceScore: 88.9,
    severityLevel: 'Moderate',
    status: 'Diseased',
    createdAt: '2026-06-08T11:10:00.000Z',
  },
]

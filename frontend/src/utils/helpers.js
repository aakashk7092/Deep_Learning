export const classNames = (...classes) => classes.filter(Boolean).join(' ')

export const formatDate = (value) =>
  new Intl.DateTimeFormat('en', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  }).format(new Date(value))

export const formatPercent = (value) => `${Number(value || 0).toFixed(1)}%`

export const normalizePrediction = (payload = {}) => {
  const source = payload.data || payload.prediction || payload
  return {
    id: source.id || source._id || crypto.randomUUID(),
    plantName: source.plantName || source.plant_name || source.plant || 'Unknown plant',
    diseaseName: source.diseaseName || source.disease_name || source.disease || 'Unknown disease',
    confidenceScore: Number(source.confidenceScore || source.confidence || source.score || 0),
    severityLevel: source.severityLevel || source.severity || 'Unknown',
    diseaseDescription:
      source.diseaseDescription || source.description || 'No description was returned by the model.',
    symptoms: toList(source.symptoms),
    causes: toList(source.causes),
    prevention: toList(source.prevention),
    treatment: toList(source.treatment),
    recommendedFertilizers: toList(source.recommendedFertilizers || source.fertilizers),
    recommendedFungicides: toList(source.recommendedFungicides || source.fungicides),
    imageUrl: source.imageUrl || source.image_url || '',
    createdAt: source.createdAt || source.created_at || new Date().toISOString(),
    status: source.status || (String(source.diseaseName || source.disease).toLowerCase().includes('healthy') ? 'Healthy' : 'Diseased'),
  }
}

export const toList = (value) => {
  if (Array.isArray(value)) return value.filter(Boolean)
  if (typeof value === 'string') return value.split(/[,\n]/).map((item) => item.trim()).filter(Boolean)
  return []
}

export const initials = (name = 'User') =>
  name
    .split(' ')
    .map((part) => part[0])
    .join('')
    .slice(0, 2)
    .toUpperCase()

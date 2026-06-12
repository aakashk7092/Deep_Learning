import { useContext } from 'react'
import { PredictionContext } from '../context/predictionContextValue'

export default function usePrediction() {
  const context = useContext(PredictionContext)
  if (!context) throw new Error('usePrediction must be used within PredictionProvider')
  return context
}

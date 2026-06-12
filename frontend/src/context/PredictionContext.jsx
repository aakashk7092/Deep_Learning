import { useCallback, useMemo, useState } from 'react'
import toast from 'react-hot-toast'
import { predictionService } from '../services/predictionService'
import { PredictionContext } from './predictionContextValue'

export function PredictionProvider({ children }) {
  const [currentPrediction, setCurrentPrediction] = useState(null)
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [progress, setProgress] = useState(0)

  const predict = useCallback(async (file) => {
    setLoading(true)
    setProgress(0)
    try {
      const result = await predictionService.predict(file, (event) => {
        if (event.total) setProgress(Math.round((event.loaded * 100) / event.total))
      })
      setCurrentPrediction(result)
      setHistory((items) => [result, ...items.filter((item) => item.id !== result.id)])
      toast.success('Prediction completed.')
      return result
    } finally {
      setLoading(false)
      setProgress(0)
    }
  }, [])

  const loadHistory = useCallback(async () => {
    setLoading(true)
    try {
      const records = await predictionService.getHistory()
      setHistory(records)
      return records
    } finally {
      setLoading(false)
    }
  }, [])

  const deletePrediction = useCallback(async (id) => {
    await predictionService.deletePrediction(id)
    setHistory((items) => items.filter((item) => item.id !== id))
    toast.success('Prediction deleted.')
  }, [])

  const value = useMemo(
    () => ({
      currentPrediction,
      setCurrentPrediction,
      history,
      loading,
      progress,
      predict,
      loadHistory,
      deletePrediction,
    }),
    [currentPrediction, history, loading, progress, predict, loadHistory, deletePrediction],
  )

  return <PredictionContext.Provider value={value}>{children}</PredictionContext.Provider>
}

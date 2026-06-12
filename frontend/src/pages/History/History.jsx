import { useEffect } from 'react'
import toast from 'react-hot-toast'
import HistoryTable from '../../components/HistoryTable/HistoryTable'
import PredictionCard from '../../components/PredictionCard/PredictionCard'
import DiseaseInfoCard from '../../components/DiseaseInfoCard/DiseaseInfoCard'
import TreatmentCard from '../../components/TreatmentCard/TreatmentCard'
import Loader from '../../components/Loader/Loader'
import usePrediction from '../../hooks/usePrediction'

export default function History() {
  const { history, loadHistory, deletePrediction, setCurrentPrediction, currentPrediction, loading } = usePrediction()

  useEffect(() => {
    loadHistory().catch((error) => toast.error(error.message))
  }, [loadHistory])

  const remove = async (id) => {
    try {
      await deletePrediction(id)
    } catch (error) {
      toast.error(error.message)
    }
  }

  return (
    <section className="container-page py-10">
      <div className="mb-8">
        <p className="text-sm font-semibold uppercase tracking-normal text-canopy">Records</p>
        <h1 className="mt-2 text-4xl font-bold">Prediction History</h1>
        <p className="section-subtitle">Search, filter, sort, inspect, and delete previous plant disease predictions.</p>
      </div>
      {loading ? <Loader /> : <HistoryTable records={history} onDelete={remove} onView={setCurrentPrediction} />}
      {currentPrediction && (
        <div className="mt-6 grid gap-6">
          <PredictionCard prediction={currentPrediction} />
          <DiseaseInfoCard prediction={currentPrediction} />
          <TreatmentCard prediction={currentPrediction} />
        </div>
      )}
    </section>
  )
}

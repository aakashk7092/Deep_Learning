import toast from 'react-hot-toast'
import UploadBox from '../../components/UploadBox/UploadBox'
import PredictionCard from '../../components/PredictionCard/PredictionCard'
import DiseaseInfoCard from '../../components/DiseaseInfoCard/DiseaseInfoCard'
import TreatmentCard from '../../components/TreatmentCard/TreatmentCard'
import Loader from '../../components/Loader/Loader'
import usePrediction from '../../hooks/usePrediction'

export default function Prediction() {
  const { currentPrediction, predict, loading, progress } = usePrediction()

  const submit = async (file) => {
    try {
      await predict(file)
    } catch (error) {
      toast.error(error.message)
    }
  }

  return (
    <section className="container-page py-10">
      <div className="mb-8">
        <p className="text-sm font-semibold uppercase tracking-normal text-canopy">AI diagnosis</p>
        <h1 className="mt-2 text-4xl font-bold">Plant Disease Prediction</h1>
        <p className="section-subtitle">Upload a clear image of the affected leaf and review a complete diagnosis with next-step recommendations.</p>
      </div>
      <div className="grid gap-6">
        <UploadBox onSubmit={submit} loading={loading} progress={progress} />
        {loading && <Loader label="Analyzing leaf structure and disease markers..." />}
        {currentPrediction && (
          <>
            <PredictionCard prediction={currentPrediction} />
            <DiseaseInfoCard prediction={currentPrediction} />
            <TreatmentCard prediction={currentPrediction} />
          </>
        )}
      </div>
    </section>
  )
}

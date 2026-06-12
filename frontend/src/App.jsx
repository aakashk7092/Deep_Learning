import { Toaster } from 'react-hot-toast'
import { AuthProvider } from './context/AuthContext'
import { PredictionProvider } from './context/PredictionContext'
import AppRoutes from './routes/AppRoutes'

function App() {
  return (
    <AuthProvider>
      <PredictionProvider>
        <div className="app-shell">
          <AppRoutes />
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 3500,
              style: {
                borderRadius: '14px',
                background: '#101828',
                color: '#fff',
              },
            }}
          />
        </div>
      </PredictionProvider>
    </AuthProvider>
  )
}

export default App

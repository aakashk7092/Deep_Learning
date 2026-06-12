import { useRef, useState } from 'react'
import toast from 'react-hot-toast'
import { FaCloudArrowUp, FaImage, FaTrash } from 'react-icons/fa6'
import { validateImageFile } from '../../utils/validators'
import { classNames } from '../../utils/helpers'

export default function UploadBox({ onSubmit, loading, progress }) {
  const inputRef = useRef(null)
  const [dragging, setDragging] = useState(false)
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState('')

  const selectFile = (nextFile) => {
    const error = validateImageFile(nextFile)
    if (error) {
      toast.error(error)
      return
    }
    setFile(nextFile)
    setPreview(URL.createObjectURL(nextFile))
  }

  const submit = () => {
    const error = validateImageFile(file)
    if (error) return toast.error(error)
    onSubmit(file)
  }

  const clear = () => {
    setFile(null)
    setPreview('')
    if (inputRef.current) inputRef.current.value = ''
  }

  return (
    <section className="card">
      <div
        role="button"
        tabIndex={0}
        onClick={() => inputRef.current?.click()}
        onKeyDown={(event) => event.key === 'Enter' && inputRef.current?.click()}
        onDragOver={(event) => { event.preventDefault(); setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={(event) => {
          event.preventDefault()
          setDragging(false)
          selectFile(event.dataTransfer.files?.[0])
        }}
        className={classNames(
          'grid min-h-72 cursor-pointer place-items-center rounded-lg border-2 border-dashed p-6 text-center transition',
          dragging ? 'border-canopy bg-canopy/10' : 'border-slate-200 bg-slate-50 dark:border-white/10 dark:bg-white/5',
        )}
      >
        <input ref={inputRef} type="file" accept="image/png,image/jpeg,image/webp" className="hidden" onChange={(event) => selectFile(event.target.files?.[0])} />
        {preview ? (
          <div className="w-full">
            <img src={preview} alt="Selected plant preview" className="mx-auto max-h-72 rounded-lg object-contain" />
            <p className="mt-4 text-sm font-medium">{file?.name}</p>
          </div>
        ) : (
          <div>
            <div className="mx-auto grid h-16 w-16 place-items-center rounded-lg bg-canopy/10 text-2xl text-canopy">
              <FaCloudArrowUp />
            </div>
            <h2 className="mt-5 text-xl font-bold">Drop a leaf image here</h2>
            <p className="mt-2 text-sm text-slate-500 dark:text-slate-300">JPG, PNG, or WebP up to 8 MB.</p>
          </div>
        )}
      </div>
      {progress > 0 && (
        <div className="mt-5 h-2 overflow-hidden rounded-full bg-slate-100 dark:bg-white/10">
          <div className="h-full rounded-full bg-canopy transition-all" style={{ width: `${progress}%` }} />
        </div>
      )}
      <div className="mt-5 flex flex-col gap-3 sm:flex-row">
        <button type="button" onClick={submit} disabled={loading} className="btn-primary disabled:cursor-not-allowed disabled:opacity-60">
          <FaImage /> {loading ? 'Analyzing image...' : 'Run diagnosis'}
        </button>
        {file && (
          <button type="button" onClick={clear} className="btn-secondary">
            <FaTrash /> Remove image
          </button>
        )}
      </div>
    </section>
  )
}

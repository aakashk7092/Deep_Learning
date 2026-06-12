import { useMemo, useState } from 'react'
import { FaArrowDownWideShort, FaEye, FaTrash } from 'react-icons/fa6'
import { formatDate, formatPercent } from '../../utils/helpers'

export default function HistoryTable({ records = [], onDelete, onView }) {
  const [query, setQuery] = useState('')
  const [filter, setFilter] = useState('All')
  const [sort, setSort] = useState('newest')
  const [page, setPage] = useState(1)
  const pageSize = 6

  const filtered = useMemo(() => {
    return records
      .filter((item) => filter === 'All' || item.status === filter || item.severityLevel === filter)
      .filter((item) => `${item.plantName} ${item.diseaseName}`.toLowerCase().includes(query.toLowerCase()))
      .sort((a, b) => {
        if (sort === 'confidence') return b.confidenceScore - a.confidenceScore
        if (sort === 'disease') return a.diseaseName.localeCompare(b.diseaseName)
        return new Date(b.createdAt) - new Date(a.createdAt)
      })
  }, [records, query, filter, sort])

  const pages = Math.max(1, Math.ceil(filtered.length / pageSize))
  const visible = filtered.slice((page - 1) * pageSize, page * pageSize)

  return (
    <section className="card">
      <div className="grid gap-3 lg:grid-cols-[1fr_160px_180px]">
        <input className="input-field" value={query} onChange={(event) => { setQuery(event.target.value); setPage(1) }} placeholder="Search plant or disease" />
        <select className="input-field" value={filter} onChange={(event) => { setFilter(event.target.value); setPage(1) }}>
          {['All', 'Healthy', 'Diseased', 'High', 'Moderate', 'Low'].map((item) => <option key={item}>{item}</option>)}
        </select>
        <select className="input-field" value={sort} onChange={(event) => setSort(event.target.value)}>
          <option value="newest">Newest first</option>
          <option value="confidence">Confidence</option>
          <option value="disease">Disease name</option>
        </select>
      </div>
      <div className="mt-5 overflow-x-auto">
        <table className="w-full min-w-[760px] text-left text-sm">
          <thead className="text-xs uppercase tracking-normal text-slate-500">
            <tr className="border-b border-slate-200 dark:border-white/10">
              <th className="py-3">Plant</th>
              <th>Disease</th>
              <th>Confidence</th>
              <th>Severity</th>
              <th>Date</th>
              <th className="text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            {visible.map((item) => (
              <tr key={item.id} className="border-b border-slate-100 dark:border-white/5">
                <td className="py-4 font-semibold">{item.plantName}</td>
                <td>{item.diseaseName}</td>
                <td>{formatPercent(item.confidenceScore)}</td>
                <td><span className="rounded-full bg-canopy/10 px-3 py-1 text-xs font-semibold text-canopy">{item.severityLevel}</span></td>
                <td>{formatDate(item.createdAt)}</td>
                <td>
                  <div className="flex justify-end gap-2">
                    <button type="button" aria-label="View details" onClick={() => onView?.(item)} className="grid h-9 w-9 place-items-center rounded-full border border-slate-200 dark:border-white/10"><FaEye /></button>
                    <button type="button" aria-label="Delete prediction" onClick={() => onDelete?.(item.id)} className="grid h-9 w-9 place-items-center rounded-full border border-red-200 text-red-600 dark:border-red-500/30"><FaTrash /></button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {!visible.length && <p className="py-10 text-center text-sm text-slate-500">No predictions match your filters.</p>}
      </div>
      <div className="mt-5 flex flex-col items-center justify-between gap-3 sm:flex-row">
        <p className="text-sm text-slate-500">Showing {visible.length} of {filtered.length} records</p>
        <div className="flex items-center gap-2">
          <button type="button" disabled={page === 1} onClick={() => setPage((value) => value - 1)} className="btn-secondary py-2 disabled:opacity-50">Previous</button>
          <span className="inline-flex items-center gap-2 text-sm font-semibold"><FaArrowDownWideShort /> {page} / {pages}</span>
          <button type="button" disabled={page === pages} onClick={() => setPage((value) => value + 1)} className="btn-secondary py-2 disabled:opacity-50">Next</button>
        </div>
      </div>
    </section>
  )
}

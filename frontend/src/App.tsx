import { useEffect, useState } from "react"
import { getCrops, getDiseases, getHealth } from "./api"
import { History } from "./History"
import { BookIcon, ClockIcon, LeafMark } from "./icons"
import { Library } from "./Library"
import { Result } from "./Result"
import { Scanner } from "./Scanner"
import { clearHistory, loadHistory } from "./storage"
import type { CropSummary, Disease, HistoryItem, ScanResult, View } from "./types"

export default function App() {
  const [view, setView] = useState<View>("scan")
  const [diseases, setDiseases] = useState<Disease[]>([])
  const [crops, setCrops] = useState<CropSummary[]>([])
  const [history, setHistory] = useState<HistoryItem[]>(() => loadHistory())
  const [modelReady, setModelReady] = useState(false)
  const [modelError, setModelError] = useState<string | null>(null)
  const [result, setResult] = useState<ScanResult | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [selectedId, setSelectedId] = useState<string | null>(null)

  useEffect(() => {
    void getDiseases().then(setDiseases).catch(() => undefined)
    void getCrops().then(setCrops).catch(() => undefined)
  }, [])

  useEffect(() => {
    let cancelled = false
    async function poll() {
      try {
        const health = await getHealth()
        if (cancelled) return
        setModelReady(health.model_ready)
        setModelError(health.model_error)
        if (!health.model_ready) window.setTimeout(() => void poll(), 1500)
      } catch {
        if (!cancelled) window.setTimeout(() => void poll(), 2000)
      }
    }
    void poll()
    return () => {
      cancelled = true
    }
  }, [])

  return (
    <div className="app">
      <header className="topbar">
        <button type="button" className="brand" onClick={() => { setView("scan"); setResult(null) }}>
          <LeafMark className="logo" />
          <span>
            Planta
            <small>leaf disease clinic</small>
          </span>
        </button>
        <div className={`status ${modelReady ? "ok" : modelError ? "bad" : "wait"}`}>
          {modelReady ? "Model ready" : modelError ? "Model failed" : "Loading model"}
        </div>
      </header>

      <main>
        {view === "scan" && result && preview ? (
          <Result
            result={result}
            preview={preview}
            diseases={diseases}
            onRescan={() => {
              setResult(null)
              setPreview(null)
            }}
            onOpenDisease={(id) => {
              setSelectedId(id)
              setView("library")
            }}
          />
        ) : view === "scan" ? (
          <Scanner
            modelReady={modelReady}
            onResult={(next, image, items) => {
              setResult(next)
              setPreview(image)
              setHistory(items)
            }}
          />
        ) : view === "library" ? (
          <Library
            diseases={diseases}
            crops={crops}
            selectedId={selectedId}
            onSelect={setSelectedId}
          />
        ) : (
          <History
            items={history}
            onOpen={(item) => {
              setSelectedId(item.label)
              setView("library")
            }}
            onClear={() => {
              clearHistory()
              setHistory([])
            }}
          />
        )}
      </main>

      <nav className="dock" aria-label="Primary">
        <button type="button" className={view === "scan" ? "active" : ""} onClick={() => { setView("scan"); setResult(null) }}>
          <LeafMark className="dock-icon" />
          Scan
        </button>
        <button
          type="button"
          className={view === "library" ? "active" : ""}
          onClick={() => { setView("library"); setSelectedId(null) }}
        >
          <BookIcon className="dock-icon" />
          Guide
        </button>
        <button type="button" className={view === "history" ? "active" : ""} onClick={() => setView("history")}>
          <ClockIcon className="dock-icon" />
          History
        </button>
      </nav>
    </div>
  )
}

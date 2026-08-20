import { useEffect, useState } from "react"
import { getCrops, getDiseases, getHealth, reloadModel } from "./api"
import { hydrateScan, scanFromHistory } from "./diagnosis"
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
  const [modelLoading, setModelLoading] = useState(true)
  const [modelError, setModelError] = useState<string | null>(null)
  const [result, setResult] = useState<ScanResult | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [retrying, setRetrying] = useState(false)

  useEffect(() => {
    void getDiseases().then(setDiseases).catch(() => undefined)
    void getCrops().then(setCrops).catch(() => undefined)
  }, [])

  useEffect(() => {
    if (diseases.length === 0) return
    setResult((current) => (current ? hydrateScan(current, diseases) : current))
  }, [diseases])

  useEffect(() => {
    return window.plantaDesktop?.onMenuCommand((command) => {
      if (command.type === "scan") {
        setView("scan")
        setResult(null)
        setPreview(null)
      }
    })
  }, [])

  useEffect(() => {
    let cancelled = false
    let delay = 1500
    async function poll() {
      try {
        const health = await getHealth()
        if (cancelled) return
        setModelReady(health.model_ready)
        setModelError(health.model_error)
        setModelLoading(Boolean(health.model_loading) && !health.model_ready)
        if (!health.model_ready) {
          delay = health.model_error ? Math.min(delay * 1.6, 10_000) : 1500
          window.setTimeout(() => void poll(), delay)
        }
      } catch {
        if (!cancelled) window.setTimeout(() => void poll(), 2000)
      }
    }
    void poll()
    return () => {
      cancelled = true
    }
  }, [])

  async function retryModel() {
    setRetrying(true)
    try {
      const health = await reloadModel()
      setModelReady(health.model_ready)
      setModelError(health.model_error)
      setModelLoading(true)
    } catch (err) {
      setModelError(err instanceof Error ? err.message : "Could not reload the model")
    } finally {
      setRetrying(false)
    }
  }

  const statusLabel = modelReady
    ? "Model ready"
    : modelError
      ? modelLoading || retrying
        ? "Retrying model"
        : "Model failed"
      : "Loading model"

  return (
    <div className="app">
      <header className="topbar">
        <button type="button" className="brand" onClick={() => { setView("scan"); setResult(null); setPreview(null) }}>
          <LeafMark className="logo" />
          <span>
            Planta
            <small>leaf disease clinic</small>
          </span>
        </button>
        <div className="status-cluster">
          <div
            className={`status ${modelReady ? "ok" : modelError ? "bad" : "wait"}`}
            title={modelError ?? undefined}
          >
            {statusLabel}
          </div>
          {modelError && !modelReady && (
            <button type="button" className="text-btn" onClick={() => void retryModel()} disabled={retrying}>
              {retrying ? "Retrying…" : "Retry"}
            </button>
          )}
        </div>
      </header>

      <main>
        {view === "scan" && result ? (
          <Result
            result={result}
            preview={preview}
            diseases={diseases}
            onChange={setResult}
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
              setResult(scanFromHistory(item, diseases))
              setPreview(item.dataUrl || null)
              setView("scan")
            }}
            onClear={() => {
              if (!window.confirm("Clear all saved leaf scans from this device?")) return
              clearHistory()
              setHistory([])
            }}
          />
        )}
      </main>

      <nav className="dock" aria-label="Primary">
        <button
          type="button"
          className={view === "scan" ? "active" : ""}
          aria-current={view === "scan" ? "page" : undefined}
          onClick={() => { setView("scan"); setResult(null); setPreview(null) }}
        >
          <LeafMark className="dock-icon" />
          Scan
        </button>
        <button
          type="button"
          className={view === "library" ? "active" : ""}
          aria-current={view === "library" ? "page" : undefined}
          onClick={() => { setView("library"); setSelectedId(null) }}
        >
          <BookIcon className="dock-icon" />
          Guide
        </button>
        <button
          type="button"
          className={view === "history" ? "active" : ""}
          aria-current={view === "history" ? "page" : undefined}
          onClick={() => setView("history")}
        >
          <ClockIcon className="dock-icon" />
          History
        </button>
      </nav>
    </div>
  )
}

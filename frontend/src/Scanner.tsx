import { useEffect, useRef, useState } from "react"
import { scanLeaf } from "./api"
import { CameraIcon, UploadIcon } from "./icons"
import { captureFrame, fileToJpeg, uid } from "./image"
import { pushHistory } from "./storage"
import type { HistoryItem, ScanResult } from "./types"

type Props = {
  modelReady: boolean
  onResult: (result: ScanResult, preview: string, history: HistoryItem[]) => void
}

const TIPS = [
  "Fill the frame with one leaf — the damaged area should be obvious.",
  "Use daylight. Avoid harsh flash and heavy shadows.",
  "A plain background (soil, paper, your hand) beats a busy garden shot.",
  "This model knows 14 crops. Houseplants and trees outside that list will be a guess.",
]

async function waitForVideo(video: HTMLVideoElement, stream: MediaStream) {
  video.srcObject = stream
  video.muted = true
  video.playsInline = true
  await video.play()
  if (video.videoWidth && video.videoHeight) return
  await new Promise<void>((resolve, reject) => {
    const timeout = window.setTimeout(() => {
      cleanup()
      reject(new Error("Camera did not produce a frame"))
    }, 4000)
    const onReady = () => {
      if (!video.videoWidth) return
      cleanup()
      resolve()
    }
    const cleanup = () => {
      window.clearTimeout(timeout)
      video.removeEventListener("loadeddata", onReady)
      video.removeEventListener("playing", onReady)
    }
    video.addEventListener("loadeddata", onReady)
    video.addEventListener("playing", onReady)
  })
}

export function Scanner({ modelReady, onResult }: Props) {
  const inputRef = useRef<HTMLInputElement>(null)
  const videoRef = useRef<HTMLVideoElement>(null)
  const streamRef = useRef<MediaStream | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [blob, setBlob] = useState<Blob | null>(null)
  const [cameraOpen, setCameraOpen] = useState(false)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [drag, setDrag] = useState(false)

  useEffect(() => {
    return () => stopCamera()
  }, [])

  useEffect(() => {
    if (!cameraOpen) return
    const video = videoRef.current
    const stream = streamRef.current
    if (!video || !stream) return
    let cancelled = false
    void waitForVideo(video, stream).catch((err: unknown) => {
      if (cancelled) return
      stopCamera()
      setError(err instanceof Error ? err.message : "Camera did not produce a frame")
    })
    return () => {
      cancelled = true
    }
  }, [cameraOpen])

  useEffect(() => {
    if (!cameraOpen) return
    function onKey(event: KeyboardEvent) {
      if (event.key === "Escape") {
        event.preventDefault()
        stopCamera()
      }
      if (event.key === " " || event.key === "Enter") {
        event.preventDefault()
        void snap()
      }
    }
    window.addEventListener("keydown", onKey)
    return () => window.removeEventListener("keydown", onKey)
  }, [cameraOpen])

  function stopCamera() {
    streamRef.current?.getTracks().forEach((track) => track.stop())
    streamRef.current = null
    if (videoRef.current) videoRef.current.srcObject = null
    setCameraOpen(false)
  }

  async function onFile(file: File) {
    setError(null)
    try {
      const converted = await fileToJpeg(file)
      setBlob(converted.blob)
      setPreview(converted.dataUrl)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not read that photo")
    }
  }

  async function openCamera() {
    setError(null)
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: { ideal: "environment" }, width: { ideal: 1280 } },
        audio: false,
      })
      streamRef.current = stream
      setCameraOpen(true)
    } catch (err) {
      stopCamera()
      if (err instanceof DOMException && err.name === "NotAllowedError") {
        setError("Camera permission was denied. You can still upload a photo.")
        return
      }
      setError(err instanceof Error ? err.message : "Camera permission was denied. You can still upload a photo.")
    }
  }

  async function snap() {
    const video = videoRef.current
    if (!video || !video.videoWidth) {
      setError("Camera is not ready yet")
      return
    }
    try {
      const frame = await captureFrame(video)
      stopCamera()
      await onFile(new File([frame], "capture.jpg", { type: "image/jpeg" }))
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not capture")
    }
  }

  async function identify() {
    if (!blob || !preview) return
    setBusy(true)
    setError(null)
    try {
      const result = await scanLeaf(blob)
      const item: HistoryItem = {
        id: uid(),
        createdAt: new Date().toISOString(),
        dataUrl: preview,
        label: result.top.id,
        name: result.top.name,
        crop: result.top.crop,
        confidence: result.top.confidence,
        healthy: result.healthy,
        severity: result.top.disease?.severity ?? "none",
        confidenceBand: result.confidence_band,
        note: result.note,
        alternatives: result.alternatives.map((alt) => ({
          id: alt.id,
          crop: alt.crop,
          name: alt.name,
          confidence: alt.confidence,
        })),
      }
      const history = pushHistory(item)
      onResult(result, preview, history)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Scan failed")
    } finally {
      setBusy(false)
    }
  }

  return (
    <section className="panel scanner">
      <div className="scanner-copy">
        <p className="eyebrow">Leaf clinic</p>
        <h1>Photograph a leaf. Find out what ails it.</h1>
        <p className="lede">
          Planta reads a close-up of a leaf and matches it against 38 crop diseases — from tomato
          late blight to apple scab — then gives you symptoms, causes, and what to do next.
        </p>
      </div>

      <div
        className={`dropzone ${drag ? "is-drag" : ""} ${preview ? "has-preview" : ""}`}
        onDragOver={(event) => {
          event.preventDefault()
          setDrag(true)
        }}
        onDragLeave={() => setDrag(false)}
        onDrop={(event) => {
          event.preventDefault()
          setDrag(false)
          const file = event.dataTransfer.files[0]
          if (file) void onFile(file)
        }}
      >
        {preview ? (
          <img src={preview} alt="Leaf to identify" className="preview-image" />
        ) : (
          <div className="dropzone-empty">
            <div className="viewfinder" aria-hidden="true" />
            <p>Drop a leaf photo here, or use the camera</p>
          </div>
        )}
      </div>

      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        hidden
        onChange={(event) => {
          const file = event.target.files?.[0]
          if (file) void onFile(file)
          event.target.value = ""
        }}
      />

      <div className="actions">
        <button type="button" className="btn primary" onClick={() => void openCamera()}>
          <CameraIcon className="btn-icon" />
          Open camera
        </button>
        <button type="button" className="btn ghost" onClick={() => inputRef.current?.click()}>
          <UploadIcon className="btn-icon" />
          Upload photo
        </button>
        {preview && (
          <button
            type="button"
            className="btn accent"
            disabled={!modelReady || busy}
            onClick={() => void identify()}
          >
            {busy ? "Reading the leaf…" : modelReady ? "Identify disease" : "Loading model…"}
          </button>
        )}
      </div>

      {preview && (
        <button type="button" className="text-btn" onClick={() => { setPreview(null); setBlob(null) }}>
          Choose a different photo
        </button>
      )}

      {error && <p className="banner error" role="alert">{error}</p>}
      {!modelReady && (
        <p className="banner">
          The recognition model is still loading on the server. You can frame a photo while you wait.
        </p>
      )}

      <ul className="tips">
        {TIPS.map((tip) => (
          <li key={tip}>{tip}</li>
        ))}
      </ul>

      {cameraOpen && (
        <div className="camera-modal" role="dialog" aria-modal="true" aria-label="Camera">
          <video ref={videoRef} autoPlay playsInline muted className="camera-video" />
          <div className="camera-bar">
            <button type="button" className="btn ghost" onClick={stopCamera}>
              Cancel
            </button>
            <button type="button" className="shutter" onClick={() => void snap()} aria-label="Capture" />
            <p className="camera-hint">Esc cancel · Space capture</p>
          </div>
        </div>
      )}
    </section>
  )
}

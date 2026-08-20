import type { CropSummary, Disease, HealthStatus, ScanResult } from "./types"

async function readError(response: Response): Promise<string> {
  try {
    const body = (await response.json()) as { detail?: unknown }
    if (typeof body.detail === "string") return body.detail
    if (Array.isArray(body.detail)) {
      return body.detail.map((item) => JSON.stringify(item)).join("; ")
    }
  } catch {
    /* ignore */
  }
  return response.statusText || "Request failed"
}

export async function getHealth(): Promise<HealthStatus> {
  const response = await fetch("/api/health")
  if (!response.ok) throw new Error(await readError(response))
  return response.json() as Promise<HealthStatus>
}

export async function reloadModel(): Promise<HealthStatus> {
  const response = await fetch("/api/model/reload", { method: "POST" })
  if (!response.ok) throw new Error(await readError(response))
  return response.json() as Promise<HealthStatus>
}

export async function getDiseases(): Promise<Disease[]> {
  const response = await fetch("/api/diseases")
  if (!response.ok) throw new Error(await readError(response))
  return response.json() as Promise<Disease[]>
}

export async function getCrops(): Promise<CropSummary[]> {
  const response = await fetch("/api/crops")
  if (!response.ok) throw new Error(await readError(response))
  return response.json() as Promise<CropSummary[]>
}

export async function scanLeaf(file: Blob, filename = "leaf.jpg"): Promise<ScanResult> {
  const body = new FormData()
  body.append("file", file, filename)
  const response = await fetch("/api/scan", { method: "POST", body })
  if (!response.ok) throw new Error(await readError(response))
  return response.json() as Promise<ScanResult>
}

import type { ConfidenceBand, Disease, HistoryItem, Prediction, ScanResult } from "./types"

export function confidenceBand(score: number): ConfidenceBand {
  if (score >= 0.75) return "high"
  if (score >= 0.45) return "medium"
  if (score >= 0.25) return "low"
  return "uncertain"
}

export function diagnosisNote(band: ConfidenceBand, healthy: boolean): string {
  if (band === "uncertain") {
    return "The model is not sure this matches a leaf it was trained on. Try a closer, well-lit photo of a single leaf against a plain background."
  }
  if (healthy) {
    return "No disease stood out — this looks like a healthy leaf of a supported crop. Keep scouting."
  }
  if (band === "low") {
    return "Take this as a shortlist, not a verdict. Compare symptoms below and consider a second photo."
  }
  if (band === "medium") {
    return "A likely match. Read the symptoms against your plant before treating."
  }
  return "Strong match to a known crop disease. Confirm the symptoms on the plant before you spray."
}

export function hydrateScan(result: ScanResult, diseases: Disease[]): ScanResult {
  if (diseases.length === 0) return result
  const lookup = (id: string) => diseases.find((row) => row.id === id) ?? null
  return {
    ...result,
    top: { ...result.top, disease: lookup(result.top.id) ?? result.top.disease },
    alternatives: result.alternatives.map((alt) => ({
      ...alt,
      disease: lookup(alt.id) ?? alt.disease,
    })),
  }
}

export function isHealthy(prediction: Prediction): boolean {
  return prediction.disease?.pathogen_type === "healthy"
}

export function scanFromHistory(item: HistoryItem, diseases: Disease[]): ScanResult {
  const lookup = (id: string) => diseases.find((row) => row.id === id) ?? null
  const disease = lookup(item.label)
  const band = item.confidenceBand ?? confidenceBand(item.confidence)
  const alternatives: Prediction[] = (item.alternatives ?? []).map((alt) => ({
    id: alt.id,
    crop: alt.crop,
    name: alt.name,
    confidence: alt.confidence,
    disease: lookup(alt.id),
  }))
  return {
    ready: true,
    healthy: item.healthy,
    confidence_band: band,
    note: item.note || diagnosisNote(band, item.healthy),
    top: {
      id: item.label,
      crop: item.crop,
      name: item.name,
      confidence: item.confidence,
      disease,
    },
    alternatives,
  }
}

export function promotePrediction(current: ScanResult, next: Prediction): ScanResult {
  const healthy = isHealthy(next)
  const band = confidenceBand(next.confidence)
  const previous = current.top
  return {
    ...current,
    healthy,
    confidence_band: band,
    note: diagnosisNote(band, healthy),
    top: next,
    alternatives: [previous, ...current.alternatives.filter((row) => row.id !== next.id)],
  }
}

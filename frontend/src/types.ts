export type TreatmentKind = "organic" | "cultural" | "chemical"
export type PathogenType =
  | "fungal"
  | "bacterial"
  | "viral"
  | "oomycete"
  | "pest"
  | "healthy"
export type Severity = "none" | "low" | "medium" | "high" | "critical"
export type ConfidenceBand = "high" | "medium" | "low" | "uncertain"

export type Treatment = {
  kind: TreatmentKind
  title: string
  details: string
}

export type Disease = {
  id: string
  crop: string
  name: string
  scientific_name: string | null
  pathogen_type: PathogenType
  severity: Severity
  contagious: boolean
  summary: string
  symptoms: string[]
  causes: string[]
  treatments: Treatment[]
  prevention: string[]
  similar: string[]
}

export type Prediction = {
  id: string
  crop: string
  name: string
  confidence: number
  disease: Disease | null
}

export type ScanResult = {
  ready: boolean
  healthy: boolean
  confidence_band: ConfidenceBand
  note: string
  top: Prediction
  alternatives: Prediction[]
}

export type HealthStatus = {
  status: string
  model: string
  model_ready: boolean
  model_error: string | null
  classes: number
  version: string
}

export type CropSummary = {
  name: string
  disease_count: number
  ailments: string[]
}

export type HistoryItem = {
  id: string
  createdAt: string
  dataUrl: string
  label: string
  name: string
  crop: string
  confidence: number
  healthy: boolean
  severity: Severity
}

export type View = "scan" | "library" | "history"

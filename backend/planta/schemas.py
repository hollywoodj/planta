from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Severity = Literal["none", "low", "medium", "high", "critical"]
PathogenType = Literal["fungal", "bacterial", "viral", "oomycete", "pest", "healthy"]
TreatmentKind = Literal["organic", "cultural", "chemical"]
ConfidenceBand = Literal["high", "medium", "low", "uncertain"]


class Treatment(BaseModel):
    kind: TreatmentKind
    title: str
    details: str


class Disease(BaseModel):
    id: str
    crop: str
    name: str
    scientific_name: str | None = None
    pathogen_type: PathogenType
    severity: Severity
    contagious: bool
    summary: str
    symptoms: list[str]
    causes: list[str]
    treatments: list[Treatment]
    prevention: list[str]
    similar: list[str] = Field(default_factory=list)


class Prediction(BaseModel):
    id: str
    crop: str
    name: str
    confidence: float
    disease: Disease | None = None


class ScanResult(BaseModel):
    ready: bool = True
    healthy: bool
    confidence_band: ConfidenceBand
    note: str
    top: Prediction
    alternatives: list[Prediction] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str
    model: str
    model_ready: bool
    model_error: str | None = None
    model_loading: bool = False
    classes: int
    version: str


class CropSummary(BaseModel):
    name: str
    disease_count: int
    ailments: list[str]

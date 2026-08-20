from __future__ import annotations

from planta.schemas import ConfidenceBand


def confidence_band(score: float) -> ConfidenceBand:
    if score >= 0.75:
        return "high"
    if score >= 0.45:
        return "medium"
    if score >= 0.25:
        return "low"
    return "uncertain"


def diagnosis_note(band: ConfidenceBand, healthy: bool) -> str:
    if band == "uncertain":
        return (
            "The model is not sure this matches a leaf it was trained on. "
            "Try a closer, well-lit photo of a single leaf against a plain background."
        )
    if healthy:
        return "No disease stood out — this looks like a healthy leaf of a supported crop. Keep scouting."
    if band == "low":
        return "Take this as a shortlist, not a verdict. Compare symptoms below and consider a second photo."
    if band == "medium":
        return "A likely match. Read the symptoms against your plant before treating."
    return "Strong match to a known crop disease. Confirm the symptoms on the plant before you spray."

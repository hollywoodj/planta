from __future__ import annotations

import io
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from PIL import Image, UnidentifiedImageError

from planta import __version__
from planta.classifier import PlantClassifier, StubClassifier
from planta.knowledge import MODEL_LABELS, all_diseases, crops, get_disease
from planta.schemas import (
    ConfidenceBand,
    Disease,
    HealthResponse,
    ScanResult,
)

LOGGER = logging.getLogger("planta")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

MAX_BYTES = 12 * 1024 * 1024
MIN_EDGE = 64

def _build_classifier() -> PlantClassifier:
    if os.environ.get("PLANTA_STUB_MODEL") == "1":
        return StubClassifier()
    return PlantClassifier()


classifier: PlantClassifier = _build_classifier()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    classifier.load_in_background()
    yield


app = FastAPI(
    title="Planta",
    description="Scan a leaf photo and identify crop diseases from the PlantVillage set.",
    version=__version__,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("PLANTA_CORS", "*").split(","),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _confidence_band(score: float) -> ConfidenceBand:
    if score >= 0.75:
        return "high"
    if score >= 0.45:
        return "medium"
    if score >= 0.25:
        return "low"
    return "uncertain"


def _note(band: ConfidenceBand, healthy: bool) -> str:
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


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        model=classifier.model_id,
        model_ready=classifier.ready,
        model_error=classifier.error,
        classes=len(MODEL_LABELS),
        version=__version__,
    )


@app.get("/api/diseases", response_model=list[Disease])
def list_diseases() -> list[Disease]:
    return all_diseases()


@app.get("/api/diseases/{disease_id}", response_model=Disease)
def disease_detail(disease_id: str) -> Disease:
    found = get_disease(disease_id)
    if found is None:
        raise HTTPException(status_code=404, detail="Unknown disease id")
    return found


@app.get("/api/crops")
def list_crops():
    return crops()


@app.post("/api/scan", response_model=ScanResult)
async def scan(file: UploadFile = File(...)) -> ScanResult:
    if not classifier.ready:
        raise HTTPException(
            status_code=503,
            detail=classifier.error or "The recognition model is still loading. Try again in a moment.",
        )

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty upload")
    if len(data) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="Image is larger than 12 MB")

    try:
        image = Image.open(io.BytesIO(data))
        image.load()
    except UnidentifiedImageError as exc:
        raise HTTPException(status_code=400, detail="That file is not a readable image") from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Could not open image") from exc

    width, height = image.size
    if min(width, height) < MIN_EDGE:
        raise HTTPException(status_code=400, detail="Image is too small — use a closer photo")

    try:
        predictions = classifier.predict(image, top_k=4)
    except Exception as exc:
        LOGGER.exception("Inference failed")
        raise HTTPException(status_code=500, detail=f"Recognition failed: {exc}") from exc

    if not predictions:
        raise HTTPException(status_code=500, detail="Model returned no predictions")

    top = predictions[0]
    disease = top.disease
    healthy = bool(disease and disease.pathogen_type == "healthy")
    band = _confidence_band(top.confidence)
    return ScanResult(
        healthy=healthy,
        confidence_band=band,
        note=_note(band, healthy),
        top=top,
        alternatives=predictions[1:],
    )


FRONTEND_DIST = Path(
    os.environ.get("PLANTA_STATIC_DIR")
    or (Path(__file__).resolve().parents[2] / "frontend" / "dist")
)
if FRONTEND_DIST.is_dir():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")

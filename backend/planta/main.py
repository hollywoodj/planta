from __future__ import annotations

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from planta import __version__
from planta.classifier import PlantClassifier, StubClassifier
from planta.images import ImageRejected, MAX_PIXELS, open_image, prepare_image
from planta.knowledge import MODEL_LABELS, all_diseases, crops, get_disease
from planta.notes import confidence_band, diagnosis_note
from planta.schemas import (
    Disease,
    HealthResponse,
    ScanResult,
)

LOGGER = logging.getLogger("planta")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

MAX_BYTES = 12 * 1024 * 1024


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


def _health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        model=classifier.model_id,
        model_ready=classifier.ready,
        model_error=classifier.error,
        model_loading=classifier.loading,
        classes=len(MODEL_LABELS),
        version=__version__,
    )


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return _health()


@app.post("/api/model/reload", response_model=HealthResponse)
def reload_model() -> HealthResponse:
    classifier.request_load()
    return _health()


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
    if len(data) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="Image is larger than 12 MB")

    try:
        image = prepare_image(open_image(data, max_pixels=MAX_PIXELS), max_pixels=MAX_PIXELS)
    except ImageRejected as exc:
        status = 400
        raise HTTPException(status_code=status, detail=str(exc)) from exc

    try:
        predictions = await asyncio.to_thread(classifier.predict, image, 4)
    except Exception as exc:
        LOGGER.exception("Inference failed")
        raise HTTPException(status_code=500, detail=f"Recognition failed: {exc}") from exc

    if not predictions:
        raise HTTPException(status_code=500, detail="Model returned no predictions")

    top = predictions[0]
    disease = top.disease
    healthy = bool(disease and disease.pathogen_type == "healthy")
    band = confidence_band(top.confidence)
    return ScanResult(
        healthy=healthy,
        confidence_band=band,
        note=diagnosis_note(band, healthy),
        top=top,
        alternatives=predictions[1:],
    )


FRONTEND_DIST = Path(
    os.environ.get("PLANTA_STATIC_DIR")
    or (Path(__file__).resolve().parents[2] / "frontend" / "dist")
)
if FRONTEND_DIST.is_dir():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")

from __future__ import annotations

import logging
import os
import threading
from pathlib import Path

from PIL import Image

from planta.knowledge import display_name, get_disease
from planta.schemas import Prediction

LOGGER = logging.getLogger("planta.classifier")

DEFAULT_MODEL = os.environ.get(
    "PLANTA_MODEL",
    "kimcomehome/plantvillage-vit-leaf-disease",
)

CACHE_DIR = Path(os.environ.get("HF_HOME", Path(__file__).resolve().parents[2] / ".hf_cache"))


class PlantClassifier:
    """Thin wrapper around a Hugging Face image-classification pipeline."""

    def __init__(self, model_id: str = DEFAULT_MODEL) -> None:
        self.model_id = model_id
        self.ready = False
        self.error: str | None = None
        self._pipeline = None
        self._lock = threading.Lock()

    def load(self) -> None:
        with self._lock:
            if self.ready:
                return
            try:
                CACHE_DIR.mkdir(parents=True, exist_ok=True)
                os.environ.setdefault("HF_HOME", str(CACHE_DIR))
                os.environ.setdefault("TRANSFORMERS_CACHE", str(CACHE_DIR))
                os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

                import torch
                from transformers import pipeline

                device = 0 if torch.cuda.is_available() else -1
                LOGGER.info("Loading %s on device=%s", self.model_id, device)
                self._pipeline = pipeline(
                    "image-classification",
                    model=self.model_id,
                    device=device,
                )
                self.ready = True
                self.error = None
                LOGGER.info("Model ready")
            except Exception as exc:  # pragma: no cover - exercised in integration
                self.ready = False
                self.error = str(exc)
                LOGGER.exception("Failed to load plant disease model")
                raise

    def load_in_background(self) -> None:
        thread = threading.Thread(target=self._safe_load, name="planta-model", daemon=True)
        thread.start()

    def _safe_load(self) -> None:
        try:
            self.load()
        except Exception:
            return

    def predict(self, image: Image.Image, top_k: int = 5) -> list[Prediction]:
        if not self.ready or self._pipeline is None:
            raise RuntimeError(self.error or "Model is still loading")

        rgb = image.convert("RGB")
        scores = self._pipeline(rgb, top_k=top_k)
        predictions: list[Prediction] = []
        for row in scores:
            label = str(row["label"])
            crop, name = display_name(label)
            predictions.append(
                Prediction(
                    id=label,
                    crop=crop,
                    name=name,
                    confidence=float(row["score"]),
                    disease=get_disease(label),
                )
            )
        return predictions


class StubClassifier(PlantClassifier):
    """Deterministic classifier used in tests — no model download."""

    def __init__(self, label: str = "Tomato___Early_blight", confidence: float = 0.91) -> None:
        super().__init__(model_id="stub")
        self._label = label
        self._confidence = confidence
        self.ready = True

    def load(self) -> None:
        self.ready = True

    def load_in_background(self) -> None:
        return

    def predict(self, image: Image.Image, top_k: int = 5) -> list[Prediction]:
        del image, top_k
        crop, name = display_name(self._label)
        return [
            Prediction(
                id=self._label,
                crop=crop,
                name=name,
                confidence=self._confidence,
                disease=get_disease(self._label),
            ),
            Prediction(
                id="Tomato___healthy",
                crop="Tomato",
                name="Healthy tomato",
                confidence=max(0.0, 1.0 - self._confidence),
                disease=get_disease("Tomato___healthy"),
            ),
        ]

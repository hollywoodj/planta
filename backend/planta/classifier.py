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
MAX_LOAD_ATTEMPTS = 5


def select_torch_device(*, cuda: bool, mps: bool) -> int | str:
    """Prefer NVIDIA CUDA, then Apple MPS, then CPU (`-1` for the HF pipeline)."""
    if cuda:
        return 0
    if mps:
        return "mps"
    return -1


class PlantClassifier:
    """Thin wrapper around a Hugging Face image-classification pipeline."""

    def __init__(self, model_id: str = DEFAULT_MODEL) -> None:
        self.model_id = model_id
        self.ready = False
        self.error: str | None = None
        self._pipeline = None
        self._lock = threading.Lock()
        self._loading = False
        self._pending = False
        self._attempts = 0

    @property
    def loading(self) -> bool:
        return self._loading or self._pending

    def load(self) -> None:
        with self._lock:
            if self.ready:
                self._pending = False
                return
            if self._loading:
                return
            self._loading = True
            self._pending = False
            self.error = None

        try:
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            os.environ.setdefault("HF_HOME", str(CACHE_DIR))
            os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

            import torch
            from transformers import pipeline

            cuda = torch.cuda.is_available()
            mps = bool(getattr(torch.backends, "mps", None) and torch.backends.mps.is_available())
            device = select_torch_device(cuda=cuda, mps=mps)
            LOGGER.info("Loading %s on device=%s", self.model_id, device)
            try:
                self._pipeline = pipeline(
                    "image-classification",
                    model=self.model_id,
                    device=device,
                )
            except Exception:
                if device == -1:
                    raise
                LOGGER.exception("Accelerator %s failed; falling back to CPU", device)
                self._pipeline = pipeline(
                    "image-classification",
                    model=self.model_id,
                    device=-1,
                )
            self.ready = True
            self.error = None
            self._attempts = 0
            self._pending = False
            LOGGER.info("Model ready")
        except Exception as exc:  # pragma: no cover - exercised in integration
            self.ready = False
            self.error = str(exc)
            LOGGER.exception("Failed to load plant disease model")
            raise
        finally:
            self._loading = False

    def load_in_background(self) -> None:
        self._pending = True
        thread = threading.Thread(target=self._safe_load, name="planta-model", daemon=True)
        thread.start()

    def request_load(self) -> None:
        """Kick another load attempt after a failure (or while still loading)."""
        if self.ready:
            return
        self._attempts = 0
        self.load_in_background()

    def _safe_load(self) -> None:
        try:
            self.load()
        except Exception:
            self._attempts += 1
            if self._attempts >= MAX_LOAD_ATTEMPTS:
                self._pending = False
                LOGGER.error("Gave up loading the model after %s attempts", self._attempts)
                return
            delay = min(2**self._attempts, 30)
            self._pending = True
            LOGGER.info("Retrying model load in %ss (attempt %s)", delay, self._attempts + 1)
            timer = threading.Timer(delay, self._safe_load)
            timer.daemon = True
            timer.start()

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
        self.error = None
        self._loading = False
        self._pending = False

    def load_in_background(self) -> None:
        return

    def request_load(self) -> None:
        self.ready = True
        self.error = None
        self._pending = False

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

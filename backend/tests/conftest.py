from __future__ import annotations

import io
import os

import pytest
from fastapi.testclient import TestClient
from PIL import Image

os.environ["PLANTA_STUB_MODEL"] = "1"

from planta.main import app  # noqa: E402


def make_png(size: int = 224, color: tuple[int, int, int] = (34, 120, 56)) -> bytes:
    image = Image.new("RGB", (size, size), color)
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client

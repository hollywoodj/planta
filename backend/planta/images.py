from __future__ import annotations

import io

from PIL import Image, ImageOps, UnidentifiedImageError

MIN_EDGE = 64
MAX_PIXELS = 40_000_000


class ImageRejected(ValueError):
    """Raised when an uploaded image cannot be used for a scan."""


def prepare_image(
    image: Image.Image,
    *,
    min_edge: int = MIN_EDGE,
    max_pixels: int = MAX_PIXELS,
) -> Image.Image:
    """Apply EXIF orientation, flatten to RGB, and reject unusable sizes."""
    try:
        oriented = ImageOps.exif_transpose(image) or image
    except Exception as exc:  # pragma: no cover - defensive
        raise ImageRejected("Could not read image orientation") from exc

    width, height = oriented.size
    if min(width, height) < min_edge:
        raise ImageRejected("Image is too small — use a closer photo")
    if width * height > max_pixels:
        raise ImageRejected("Image is too large — try a smaller photo")

    if oriented.mode in {"RGBA", "LA"}:
        background = Image.new("RGB", oriented.size, (255, 255, 255))
        alpha = oriented.getchannel("A")
        background.paste(oriented.convert("RGB"), mask=alpha)
        return background
    if oriented.mode != "RGB":
        return oriented.convert("RGB")
    return oriented


def open_image(data: bytes, *, max_pixels: int = MAX_PIXELS) -> Image.Image:
    if not data:
        raise ImageRejected("Empty upload")
    try:
        image = Image.open(io.BytesIO(data))
        width, height = image.size
        if width * height > max_pixels:
            raise ImageRejected("Image is too large — try a smaller photo")
        image.load()
        return image
    except ImageRejected:
        raise
    except UnidentifiedImageError as exc:
        raise ImageRejected("That file is not a readable image") from exc
    except Image.DecompressionBombError as exc:
        raise ImageRejected("Image is too large — try a smaller photo") from exc
    except Exception as exc:
        raise ImageRejected("Could not open image") from exc

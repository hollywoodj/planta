from io import BytesIO

from PIL import Image

from planta.classifier import select_torch_device
from planta.images import ImageRejected, open_image, prepare_image
from planta.notes import confidence_band, diagnosis_note


def test_select_torch_device_prefers_cuda_then_mps():
    assert select_torch_device(cuda=True, mps=True) == 0
    assert select_torch_device(cuda=False, mps=True) == "mps"
    assert select_torch_device(cuda=False, mps=False) == -1


def test_prepare_image_applies_exif_orientation():
    image = Image.new("RGB", (200, 80), (34, 140, 56))
    exif = image.getexif()
    exif[0x0112] = 6  # rotate 90 CW
    buffer = BytesIO()
    image.save(buffer, format="JPEG", exif=exif)

    prepared = prepare_image(open_image(buffer.getvalue()))
    assert prepared.size == (80, 200)
    assert prepared.mode == "RGB"


def test_prepare_image_flattens_rgba():
    image = Image.new("RGBA", (80, 80), (10, 200, 40, 128))
    prepared = prepare_image(image)
    assert prepared.mode == "RGB"
    assert prepared.size == (80, 80)


def test_prepare_image_rejects_tiny_and_huge():
    tiny = Image.new("RGB", (20, 20), (0, 0, 0))
    try:
        prepare_image(tiny)
        assert False, "expected tiny image to be rejected"
    except ImageRejected as exc:
        assert "too small" in str(exc)

    huge = Image.new("RGB", (80, 80), (0, 0, 0))
    try:
        prepare_image(huge, max_pixels=1000)
        assert False, "expected huge image to be rejected"
    except ImageRejected as exc:
        assert "too large" in str(exc)


def test_open_image_rejects_empty_and_non_image():
    try:
        open_image(b"")
        assert False, "expected empty upload to be rejected"
    except ImageRejected as exc:
        assert "Empty" in str(exc)

    try:
        open_image(b"not-an-image")
        assert False, "expected garbage to be rejected"
    except ImageRejected as exc:
        assert "not a readable image" in str(exc)


def test_open_image_rejects_too_many_pixels():
    image = Image.new("RGB", (80, 80), (0, 80, 0))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    try:
        open_image(buffer.getvalue(), max_pixels=100)
        assert False, "expected pixel cap to reject the image"
    except ImageRejected as exc:
        assert "too large" in str(exc)


def test_confidence_notes():
    assert confidence_band(0.9) == "high"
    assert confidence_band(0.5) == "medium"
    assert confidence_band(0.3) == "low"
    assert confidence_band(0.1) == "uncertain"
    assert "Strong match" in diagnosis_note("high", False)
    assert "healthy leaf" in diagnosis_note("high", True)
    assert "not sure" in diagnosis_note("uncertain", False)

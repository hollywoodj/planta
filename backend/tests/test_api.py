from tests.conftest import make_png


def test_health_reports_stub_model(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model_ready"] is True
    assert body["model_loading"] is False
    assert body["classes"] == 38
    assert body["model"] == "stub"


def test_reload_model_endpoint(client):
    response = client.post("/api/model/reload")
    assert response.status_code == 200
    assert response.json()["model_ready"] is True


def test_diseases_endpoint_lists_all(client):
    response = client.get("/api/diseases")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 38
    assert body[0]["id"] == "Apple___Apple_scab"


def test_disease_detail_and_404(client):
    ok = client.get("/api/diseases/Tomato___Late_blight")
    assert ok.status_code == 200
    assert ok.json()["severity"] == "critical"
    missing = client.get("/api/diseases/nope")
    assert missing.status_code == 404


def test_crops_endpoint(client):
    response = client.get("/api/crops")
    names = {row["name"] for row in response.json()}
    assert "Tomato" in names
    assert "Apple" in names
    assert "Bell pepper" in names


def test_scan_returns_stub_diagnosis(client):
    response = client.post(
        "/api/scan",
        files={"file": ("leaf.png", make_png(), "image/png")},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["top"]["id"] == "Tomato___Early_blight"
    assert body["healthy"] is False
    assert body["confidence_band"] == "high"
    assert body["top"]["disease"]["name"] == "Early blight"
    assert body["alternatives"]


def test_scan_rejects_empty(client):
    response = client.post("/api/scan", files={"file": ("leaf.png", b"", "image/png")})
    assert response.status_code == 400


def test_scan_rejects_tiny_image(client):
    response = client.post(
        "/api/scan",
        files={"file": ("leaf.png", make_png(size=32), "image/png")},
    )
    assert response.status_code == 400


def test_scan_rejects_non_image(client):
    response = client.post(
        "/api/scan",
        files={"file": ("notes.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 400


def test_scan_accepts_jpeg_with_exif_orientation(client):
    from io import BytesIO

    from PIL import Image

    image = Image.new("RGB", (160, 80), (34, 120, 56))
    exif = image.getexif()
    exif[0x0112] = 6
    buffer = BytesIO()
    image.save(buffer, format="JPEG", exif=exif)
    response = client.post(
        "/api/scan",
        files={"file": ("leaf.jpg", buffer.getvalue(), "image/jpeg")},
    )
    assert response.status_code == 200
    assert response.json()["top"]["id"] == "Tomato___Early_blight"


def test_scan_rejects_pixel_bomb(client, monkeypatch):
    monkeypatch.setattr("planta.main.MAX_PIXELS", 1000)
    response = client.post(
        "/api/scan",
        files={"file": ("leaf.png", make_png(size=224), "image/png")},
    )
    assert response.status_code == 400
    assert "too large" in response.json()["detail"]

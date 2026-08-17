# Planta

Photograph a leaf. Planta identifies the crop disease and tells you what to do about it.

It is a small web app: a camera-first React client and a FastAPI service that runs a Vision Transformer trained on the [PlantVillage](https://arxiv.org/abs/1511.08060) dataset (38 classes across 14 crops). Every diagnosis is paired with symptoms, likely causes, and organic / cultural / conventional next steps.

## What it can recognize

Apple, blueberry, cherry, corn, grape, orange, peach, bell pepper, potato, raspberry, soybean, squash, strawberry, and tomato — including healthy leaves plus ailments such as late blight, early blight, apple scab, citrus greening, powdery mildew, TYLCV, and two-spotted spider mites.

The model will still *emit* a class for anything you photograph. Low confidence is called out in the UI; treat out-of-scope plants (houseplants, oaks, lawns) as unknown.

## Quick start

You need Python 3.12+ and Node 22+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

cd frontend && npm install && cd ..

# terminal 1 — API (downloads the ~330MB model on first run)
source .venv/bin/activate
PYTHONPATH=backend HF_HOME="$PWD/.hf_cache" uvicorn planta.main:app --reload --host 0.0.0.0 --port 8000

# terminal 2 — UI
cd frontend && npm run dev
```

Open [http://127.0.0.1:5173](http://127.0.0.1:5173). The Vite dev server proxies `/api` to port 8000.

Or run both with `./scripts/dev.sh` after install.

### Production-style (API serves the UI)

```bash
cd frontend && npm run build && cd ..
PYTHONPATH=backend HF_HOME="$PWD/.hf_cache" uvicorn planta.main:app --host 0.0.0.0 --port 8000
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Tests

```bash
source .venv/bin/activate
PYTHONPATH=backend PLANTA_STUB_MODEL=1 pytest backend/tests -q
cd frontend && npm run build
```

API tests use a stub classifier so they do not download the neural net. CI installs `backend/requirements-test.txt` (no PyTorch) for the same reason.


## How a scan works

1. The browser captures or uploads a photo and resizes it to a JPEG.
2. `POST /api/scan` runs `kimcomehome/plantvillage-vit-leaf-disease`.
3. The top classes are joined to a built-in knowledge base (`backend/planta/knowledge.py`) with treatments and look-alikes.
4. Scans are stored only in your browser (`localStorage`). Images are not written to disk on the server.

## API

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/health` | Model ready flag |
| `GET` | `/api/diseases` | Full field guide |
| `GET` | `/api/crops` | Crops and ailment counts |
| `POST` | `/api/scan` | Multipart file upload named `file` |

Environment:

- `PLANTA_MODEL` — Hugging Face model id (default above)
- `PLANTA_STUB_MODEL=1` — skip the neural net (tests / UI work)
- `HF_HOME` — model cache directory
- `PLANTA_CORS` — comma-separated origins (default `*`)

## Disclaimer

Planta is a screening aid, not an agronomist. Confirm symptoms on the plant, and follow local pesticide labels and regulations.

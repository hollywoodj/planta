# Planta

Photograph a leaf. Planta identifies the crop disease and tells you what to do about it.

It is a Mac (and Windows) desktop app: an Electron shell around a camera-first React UI and a FastAPI service that runs a Vision Transformer trained on the [PlantVillage](https://arxiv.org/abs/1511.08060) dataset (38 classes across 14 crops). Every diagnosis is paired with symptoms, likely causes, and organic / cultural / conventional next steps.

## Desktop app

```bash
./scripts/install.sh
npm run electron:dev
```

That opens the native window against the Vite dev server. The first identification downloads the ~330MB model into the app data folder.

### Packaged Mac / Windows installers

```bash
npm run electron:build:mac    # DMG in release/
npm run electron:build:win    # NSIS installer in release/
```

Packaging bundles a relocatable CPython (via python-build-standalone), PyTorch, and the UI. The first launch still downloads model weights.

### Auto-release

Pushing to `main` (or running the **Release** workflow) auto-bumps the patch version, builds Mac and Windows installers, and publishes a GitHub Release — the same pattern as OmniClone / OmniPlan / Notebook. Use `[skip release]` in a commit message to skip. Manual runs can pass `version` (for example `v1.2.0`).

Unsigned local/CI builds: on macOS, right-click the app → Open the first time.

## Web (optional)

You need Python 3.12+ and Node 22+.

```bash
./scripts/install.sh

# terminal 1 — API
source .venv/bin/activate
PYTHONPATH=backend HF_HOME="$PWD/.hf_cache" python3 -m planta

# terminal 2 — UI
cd frontend && npm run dev
```

Open [http://127.0.0.1:5173](http://127.0.0.1:5173). The Vite dev server proxies `/api` to port 8000.

Or run both with `./scripts/dev.sh`.

## What it can recognize

Apple, blueberry, cherry, corn, grape, orange, peach, bell pepper, potato, raspberry, soybean, squash, strawberry, and tomato — including healthy leaves plus ailments such as late blight, early blight, apple scab, citrus greening, powdery mildew, TYLCV, and two-spotted spider mites.

The model will still *emit* a class for anything you photograph. Low confidence is called out in the UI; treat out-of-scope plants (houseplants, oaks, lawns) as unknown.

## Tests

```bash
source .venv/bin/activate
PLANTA_STUB_MODEL=1 pytest -q
cd frontend && npm run build
node --check electron/main.cjs
```

API tests use a stub classifier so they do not download the neural net. CI installs `backend/requirements-test.txt` (no PyTorch) for the same reason.

## How a scan works

1. The app captures or uploads a photo and resizes it to a JPEG.
2. `POST /api/scan` runs `kimcomehome/plantvillage-vit-leaf-disease`.
3. The top classes are joined to a built-in knowledge base (`backend/planta/knowledge.py`) with treatments and look-alikes.
4. Scans stay in the renderer (`localStorage`). Images are not written to disk on the server.

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
- `PLANTA_STATIC_DIR` — folder of built UI files for the packaged app
- `PLANTA_HOST` / `PORT` — bind address (desktop uses `127.0.0.1:8742`)
- `PLANTA_CORS` — comma-separated origins (default `*`)

## Disclaimer

Planta is a screening aid, not an agronomist. Confirm symptoms on the plant, and follow local pesticide labels and regulations.

from __future__ import annotations

import os

from planta.main import app

if __name__ == "__main__":
    import uvicorn

    host = os.environ.get("PLANTA_HOST", "127.0.0.1")
    port = int(os.environ.get("PORT") or os.environ.get("PLANTA_PORT") or "8000")
    uvicorn.run(app, host=host, port=port)

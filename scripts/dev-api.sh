#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="${PYTHONPATH:-$ROOT/backend}"
export HF_HOME="${HF_HOME:-$ROOT/.hf_cache}"
if [[ -x "$ROOT/.venv/bin/python" ]]; then
  exec "$ROOT/.venv/bin/python" -m planta
fi
if [[ -x "$ROOT/.venv/Scripts/python.exe" ]]; then
  exec "$ROOT/.venv/Scripts/python.exe" -m planta
fi
exec python3 -m planta

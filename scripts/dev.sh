#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -d .venv ]]; then
  echo "Run ./scripts/install.sh first" >&2
  exit 1
fi

# shellcheck disable=SC1091
source .venv/bin/activate
export PYTHONPATH="$ROOT/backend"
export HF_HOME="${HF_HOME:-$ROOT/.hf_cache}"

uvicorn planta.main:app --reload --host 0.0.0.0 --port 8000 &
API_PID=$!
trap 'kill "$API_PID" 2>/dev/null || true' EXIT

cd "$ROOT/frontend"
npm run dev -- --host 0.0.0.0 --port 5173

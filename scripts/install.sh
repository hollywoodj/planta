#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -U pip
if [[ "$(uname -s)" == "Linux" ]]; then
  pip install -r backend/requirements-linux-cpu.txt
else
  pip install -r backend/requirements.txt
  pip install "torch==2.8.0"
fi
(cd frontend && npm install)
npm install

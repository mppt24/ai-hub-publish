#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BASE"
if [[ ! -f .env ]]; then
  echo "Criar .env a partir dos defaults"
  cat > .env <<'ENV'
ENABLE_OPENAI=false
OPENAI_API_KEY=
ALLOWED_ORIGINS=*
HUB_PORT=8181
OLLAMA_PORT=11434
ENV
fi
echo "✅ Projeto preparado em $BASE (não arrancou nada)."
echo "➡ Revê .env (HUB_PORT, OLLAMA_PORT)."

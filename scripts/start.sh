#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BASE"
set -a; [[ -f .env ]] && . ./.env; set +a

echo "🔧 Subir LLM (Ollama)…"
docker compose --profile llm up -d --build

echo "🔧 Subir core (Hub + Redis)…"
docker compose --profile core up -d --build

CID=$(docker ps -qf name=ollama || true)
if [[ -n "${CID:-}" ]]; then
  echo "⬇️  Pull modelo local (llama3.1:8b)…"
  docker exec -it "$CID" ollama pull llama3.1:8b || true
fi

echo "🧪 Testes:"
bash scripts/test_request.sh || true

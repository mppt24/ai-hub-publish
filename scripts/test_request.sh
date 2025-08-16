#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BASE"
set -a; [[ -f .env ]] && . ./.env; set +a

echo "GET /"
curl -s "http://localhost:${HUB_PORT:-8181}/" || true
echo -e "\nPOST /chat"
curl -s "http://localhost:${HUB_PORT:-8181}/chat" \
  -H 'content-type: application/json' \
  -d '{"message":"Plano global de acessibilidade para telemóvel/TV/PC."}' || true
echo

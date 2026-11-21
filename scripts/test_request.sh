#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BASE"
docker compose exec -T agent-hub python - <<'PY'
import json
from urllib.request import urlopen

with urlopen("http://127.0.0.1:8080/", timeout=5) as response:
    status = json.load(response)

if status.get("ok") is not True:
    raise SystemExit("O AI Hub respondeu, mas não confirmou o estado de saúde.")

print(json.dumps(status, ensure_ascii=False))
PY

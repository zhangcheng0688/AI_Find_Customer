#!/usr/bin/env bash
# Idempotent Cloud Agent / local bootstrap for AI Hunter.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

export BUN_INSTALL="${BUN_INSTALL:-$HOME/.bun}"
export PATH="$BUN_INSTALL/bin:$PATH"

# `import venv` can succeed even when ensurepip is missing; check ensurepip itself.
if ! python3 -c "import ensurepip" 2>/dev/null; then
  sudo apt-get update -qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3.12-venv python3-pip
fi

if ! command -v bun >/dev/null 2>&1; then
  curl -fsSL https://bun.sh/install | bash
  export PATH="$BUN_INSTALL/bin:$PATH"
fi

cd "$ROOT/backend"
# Recreate a broken/incomplete venv if pip is unavailable.
if [[ ! -x .venv/bin/pip ]]; then
  rm -rf .venv
  python3 -m venv .venv
fi
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
if [[ ! -f .env ]]; then
  cp .env.example .env
fi

cd "$ROOT/frontend"
bun install

echo "Dev environment ready."
echo "  Backend:  cd backend && source .venv/bin/activate && uvicorn api.app:app --host 0.0.0.0 --port 8000"
echo "  Frontend: cd frontend && bun run dev -- --host 0.0.0.0 --port 3000"

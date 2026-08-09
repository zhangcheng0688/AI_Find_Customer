#!/usr/bin/env bash
# Idempotent Cloud Agent / local bootstrap for AI Hunter.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

export BUN_INSTALL="${BUN_INSTALL:-$HOME/.bun}"
export PATH="$BUN_INSTALL/bin:$PATH"

# Fresh Cloud Agent images often lack a working ensurepip even when
# `import ensurepip` appears to succeed. Always install python3-venv.
sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3.12-venv python3-pip

if ! command -v bun >/dev/null 2>&1; then
  curl -fsSL https://bun.sh/install | bash
  export PATH="$BUN_INSTALL/bin:$PATH"
fi

cd "$ROOT/backend"
rm -rf .venv
python3 -m venv .venv
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

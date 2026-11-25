#!/usr/bin/env bash
# Fix the 3 missing Python tools on InstaBox momomuse ONLY.
# Root cause: pipx was not installed (Debian python is externally managed,
# plain pip install --user fails). Use --break-system-packages.
# Usage on momomuse: nohup bash /data/home/fix-python-tools.sh > /data/home/fix-python-tools.log 2>&1 &
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"

echo "== pipx + waymore =="
python3 -m pip install --user --break-system-packages -q pipx waymore
python3 -m pipx ensurepath || true
export PATH="$HOME/.local/bin:$PATH"

echo "== arjun via pipx =="
python3 -m pipx install arjun || pipx install arjun || echo "arjun install failed, continuing"

echo "== paramspider from local clone =="
cd ~/workspace/tools-web-recon/paramspider
python3 -m pip install --user --break-system-packages -q . || echo "paramspider pip install failed, continuing"

echo "DONE. Run verify-web-recon.sh next."

#!/usr/bin/env bash
# Install Beacon web-recon tools on InstaBox momomuse ONLY. Never on Hatch VM.
# Go tools go to ~/go/bin (already on PATH on momomuse). Go 1.27 present.
# Usage on momomuse: bash ~/workspace/bounty-hunter/scripts/install-web-recon.sh
# Verify: bash ~/workspace/bounty-hunter/scripts/verify-web-recon.sh
set -euo pipefail
export PATH="$HOME/go/bin:$PATH"
export GOPATH="${GOPATH:-$HOME/go}"
export CGO_ENABLED=1

echo "== Go tools =="
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install github.com/ffuf/ffuf/v2@latest
go install -v github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest
go install github.com/sensepost/gowitness@latest
go install github.com/tomnomnom/assetfinder@latest
go install github.com/tomnomnom/waybackurls@latest
go install github.com/tomnomnom/gf@latest
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/owasp-amass/amass/v5/cmd/amass@main || echo "amass install failed, continuing"

echo "== Dalfox =="
if command -v brew >/dev/null 2>&1; then
  brew install dalfox || echo "dalfox brew failed, continuing"
else
  go install github.com/hahwul/dalfox/v2@latest || echo "dalfox go install failed, continuing"
fi

echo "== Python tools =="
python3 -m pip install --user --break-system-packages -q pipx 2>/dev/null || true
python3 -m pipx install arjun 2>/dev/null || pipx install arjun || echo "arjun install failed, continuing"
python3 -m pip install --user --break-system-packages -q waymore 2>/dev/null || echo "waymore install failed, continuing"

echo "== ParamSpider + LinkFinder (git clones, reference only) =="
mkdir -p ~/workspace/tools-web-recon
cd ~/workspace/tools-web-recon
[ -d paramspider ] || git clone https://github.com/devanshbatham/paramspider
[ -d LinkFinder ] || git clone https://github.com/GerbenJavado/LinkFinder.git

echo "DONE. Run verify-web-recon.sh next."

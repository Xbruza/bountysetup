#!/usr/bin/env bash
# Verify Beacon web-recon tools on hunt compute box <YOUR_COMPUTE_BOX>.
# Usage: bash ~/workspace/bounty-hunter/scripts/verify-web-recon.sh
export PATH="$HOME/go/bin:$HOME/.local/bin:$PATH"
fail=0
for t in subfinder assetfinder amass dnsx httpx naabu katana waybackurls gau waymore arjun gf nuclei ffuf dalfox gowitness interactsh-client; do
  if command -v "$t" >/dev/null 2>&1; then
    echo "OK $t $(command -v "$t")"
  else
    echo "MISSING $t"
    fail=1
  fi
done
if [ -d ~/workspace/tools-web-recon/paramspider ]; then
  echo "OK paramspider clone ~/workspace/tools-web-recon/paramspider"
elif command -v paramspider >/dev/null 2>&1; then
  echo "OK paramspider $(command -v paramspider)"
else
  echo "MISSING paramspider"
  fail=1
fi
echo "--- versions (best effort) ---"
subfinder -version 2>&1 | head -1 || true
nuclei -version 2>&1 | head -1 || true
ffuf -V 2>&1 | head -1 || true
katana -version 2>&1 | head -1 || true
exit $fail

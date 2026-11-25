#!/usr/bin/env bash
# Poll InstaBox install-web-recon.log until DONE appears or 15 min elapse.
HELPER=/home/hatch/workspace/custom-connectors/custom.instabox/bin/instabox.py
for i in $(seq 1 20); do
  sleep 45
  OUT=$(python3 "$HELPER" exec momomuse -- 'tail -n 5 /data/home/install-web-recon.log; ls ~/go/bin/ 2>/dev/null | tr "\n" " "' 2>/dev/null)
  echo "--- poll $i ---"
  echo "$OUT" | tail -n 12
  if echo "$OUT" | grep -q "DONE\. Run verify"; then
    echo "INSTALL_DONE"
    exit 0
  fi
  if echo "$OUT" | grep -q "INSTALL_EXIT"; then
    echo "INSTALL_EXIT_MARKER"
    exit 0
  fi
done
echo "POLL_TIMEOUT_15MIN"
exit 1

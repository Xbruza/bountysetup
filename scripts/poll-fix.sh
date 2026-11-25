#!/usr/bin/env bash
# Poll InstaBox fix-python-tools.log until DONE appears or 10 min elapse.
HELPER=/home/hatch/workspace/custom-connectors/custom.instabox/bin/instabox.py
for i in $(seq 1 13); do
  sleep 45
  OUT=$(python3 "$HELPER" exec momomuse -- 'tail -n 5 /data/home/fix-python-tools.log; ls ~/.local/bin/ 2>/dev/null | tr "\n" " "' 2>/dev/null)
  echo "--- poll $i ---"
  echo "$OUT" | tail -n 12
  if echo "$OUT" | grep -q "DONE\. Run verify"; then
    echo "FIX_DONE"
    exit 0
  fi
done
echo "POLL_TIMEOUT_10MIN"
exit 1

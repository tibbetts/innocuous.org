#!/usr/bin/env bash
# Drive site-check.py from a persistent Monitor.
#
# Emits on stdout ONLY on a state change: once when checks start failing, once
# when they recover. A naive `|| echo` would re-print the same failure every
# cycle for the whole outage, which trains you to ignore it.
#
#   Monitor: tools/monitoring/watch.sh   (persistent: true)

cd "$(dirname "$0")/../.." || exit 1
INTERVAL="${INTERVAL:-900}"
prev=ok

while true; do
  if out=$(./tools/monitoring/site-check.py 2>&1); then
    if [ "$prev" = fail ]; then
      echo "=== site-check RECOVERED $(date '+%Y-%m-%d %H:%M') ==="
      echo "    all invariants passing again"
    fi
    prev=ok
  else
    if [ "$prev" = ok ]; then
      echo "$out"
    fi
    prev=fail
  fi
  sleep "$INTERVAL"
done

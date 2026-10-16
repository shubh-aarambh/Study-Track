#!/usr/bin/env bash
set -euo pipefail

URL="${URL:-http://studytrack.local/api/health}"
REQUESTS="${REQUESTS:-1000}"
CONCURRENCY="${CONCURRENCY:-10}"

echo "=================================================="
echo " StudyTrack Load Test"
echo " Target URL   : $URL"
echo " Total Reqs   : $REQUESTS"
echo " Concurrency  : $CONCURRENCY"
echo "=================================================="

START_TIME=$(date +%s)

# Run batches of concurrent curl requests to simulate real load for HPA & Prometheus
COMPLETED=0
BATCH_SIZE="$CONCURRENCY"

while [ "$COMPLETED" -lt "$REQUESTS" ]; do
  REMAINING=$((REQUESTS - COMPLETED))
  BATCH=$((REMAINING < BATCH_SIZE ? REMAINING : BATCH_SIZE))
  
  PIDS=()
  for ((i = 0; i < BATCH; i++)); do
    curl -s -o /dev/null -w "%{http_code}\n" "$URL" &
    PIDS+=($!)
  done

  # Wait for batch to finish
  for pid in "${PIDS[@]}"; do
    wait "$pid" 2>/dev/null || true
  done

  COMPLETED=$((COMPLETED + BATCH))
  if [ $((COMPLETED % 100)) -eq 0 ] || [ "$COMPLETED" -eq "$REQUESTS" ]; then
    echo "Progress: $COMPLETED / $REQUESTS requests sent..."
  fi
done

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
[ "$DURATION" -eq 0 ] && DURATION=1
RPS=$((REQUESTS / DURATION))

echo "=================================================="
echo " Load test completed in ${DURATION}s (~${RPS} req/sec)"
echo " Check Prometheus/Grafana and HPA for autoscaling!"
echo "=================================================="


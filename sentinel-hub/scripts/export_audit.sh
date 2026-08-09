#!/usr/bin/env bash
# export_audit.sh
# Exports the KeeperHub audit trail for all recent runs.
# The audit trail is the primary proof surface for judging:
# it logs: trigger, simulation result, tx submitted, gas used, outcome, timestamp.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)"
EVIDENCE="$ROOT/evidence"
mkdir -p "$EVIDENCE"

echo "[audit] Fetching recent run history..."

# Get the last 10 runs across all workflows
RUNS=$(kh run status --json 2>/dev/null || echo '{"data":[]}')
RUN_IDS=$(echo "$RUNS" | jq -r '.data[].id // empty' 2>/dev/null | head -10)

if [ -z "$RUN_IDS" ]; then
  echo "No runs found. Have you executed any workflows?"
  exit 0
fi

for RUN_ID in $RUN_IDS; do
  echo "[audit] Exporting run $RUN_ID..."
  kh run logs "$RUN_ID" --json > "$EVIDENCE/audit_${RUN_ID}.json" 2>/dev/null \
    && echo "  Saved: $EVIDENCE/audit_${RUN_ID}.json" \
    || echo "  Failed to export $RUN_ID"
done

echo
echo "[audit] Audit trail files:"
ls -lh "$EVIDENCE"/audit_*.json 2>/dev/null || echo "  (none exported)"
echo
echo "[audit] These files are your proof surface. Include them in your submission."

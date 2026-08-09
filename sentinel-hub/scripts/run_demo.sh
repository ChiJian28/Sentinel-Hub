#!/usr/bin/env bash
# run_demo.sh
# Executes a full demo cycle: runs the Sentry Agent once, exports audit trail,
# and prints a submission-ready summary of all evidence.
#
# This is the script to run during judging to generate verifiable proof.

set -euo pipefail

GREEN='\033[0;32m'
PURPLE='\033[0;35m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

log()     { echo -e "${PURPLE}[demo]${NC} $*"; }
ok()      { echo -e "${GREEN}[✓]${NC} $*"; }
header()  { echo -e "\n${BOLD}${CYAN}$*${NC}"; }

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)"
cd "$ROOT"

[ -f .env ] && source .env

header "🛡️  Sentinel-Hub Demo — Full Agent Execution Cycle"
echo
log "Target wallet: ${TARGET_WALLET:-NOT SET}"
log "Chain:         ${CHAIN_ID:-11155111} (Sepolia)"
log "Timestamp:     $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo

# Verify wallet is funded
log "Checking agentic wallet balance..."
npx -p @keeperhub/wallet keeperhub-wallet balance || {
  echo
  echo "Wallet not funded. Run: npx -p @keeperhub/wallet keeperhub-wallet fund"
  exit 1
}
echo

# Run the Sentry Agent for exactly one cycle
header "Running Sentry Agent (single cycle)..."
python3 sentinel_agent.py --once

# Find the latest evidence file
LATEST=$(ls -t evidence/cycle_*.json 2>/dev/null | head -1)
if [ -z "$LATEST" ]; then
  echo "No evidence file found. Did the cycle complete?"
  exit 1
fi

header "Evidence Summary"
ok "Evidence file: $LATEST"
cat "$LATEST" | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(f'  Cycle:       {d[\"cycle\"]}')
print(f'  Timestamp:   {d[\"timestamp\"]}')
print(f'  Wallet:      {d[\"wallet\"]}')
print(f'  Chain:       {d[\"chain_id\"]}')
print(f'  Keepers called: {len(d[\"keepers_called\"])}')
for k in d.get(\"keepers_called\", []):
    print(f'    - {k}')
print(f'  Transactions:   {len(d[\"transaction_hashes\"])}')
for tx in d.get(\"transaction_hashes\", []):
    print(f'    - {tx}')
    print(f'      Sepolia: https://sepolia.etherscan.io/tx/{tx}')
"

# Export audit trail for each run
header "Exporting Audit Trails via KeeperHub CLI"
log "Run: kh run logs --json for each completed run"
kh run status --json 2>/dev/null | head -20 || true

header "Registry Verification Links"
ok "x402scan: https://x402scan.com"
ok "mppscan:  https://mppscan.com"
ok "KeeperHub Marketplace:"
echo "  https://app.keeperhub.com/api/mcp/workflows/defi-portfolio-snapshot/call"
echo "  https://app.keeperhub.com/api/mcp/workflows/aave-v3-health-guardian/call"
echo "  https://app.keeperhub.com/api/mcp/workflows/chainlink-price-sentinel/call"

echo
log "Demo complete. Save $LATEST as submission evidence."

#!/usr/bin/env bash
# deploy_keepers.sh
# Deploys all Keeper workflows to KeeperHub and publishes them to the Marketplace.
# Run this ONCE before the demo. After run, verify on x402scan.com and mppscan.com.
#
# Prerequisites:
#   kh auth login
#   KEEPERHUB_API_KEY exported in environment

set -euo pipefail

PURPLE='\033[0;35m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()  { echo -e "${PURPLE}[deploy]${NC} $*"; }
ok()   { echo -e "${GREEN}[✓]${NC} $*"; }
warn() { echo -e "${YELLOW}[!]${NC} $*"; }
err()  { echo -e "${RED}[✗]${NC} $*"; exit 1; }

CONFIG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../keepers" && pwd)"

log "Starting Sentinel-Hub Keeper deployment"
log "Config dir: $CONFIG_DIR"

# Verify kh CLI is available and authenticated
if ! command -v kh &>/dev/null; then
  err "KeeperHub CLI 'kh' not found. Install: npm install -g @keeperhub/cli"
fi

kh auth status --json | grep -q '"authenticated":true' || err "Not authenticated. Run: kh auth login"
ok "KeeperHub CLI authenticated"

# Create project for organisation
log "Creating project..."
PROJECT_ID=$(kh project create "Sentinel-Hub" --description "Autonomous agentic execution economy" --json | jq -r '.data.id' 2>/dev/null || echo "")
if [ -n "$PROJECT_ID" ]; then
  ok "Project created: $PROJECT_ID"
else
  warn "Project may already exist — continuing"
fi

# Create tags
log "Creating tags..."
kh tag create "sentinel-hub" --json &>/dev/null || warn "Tag may already exist"
kh tag create "agentic-economy" --json &>/dev/null || warn "Tag may already exist"
ok "Tags ready"

# ---------------------------------------------------------------------------
# Deploy and publish each Keeper workflow
# ---------------------------------------------------------------------------

deploy_keeper() {
  local json_file="$1"
  local slug="$2"
  local price="$3"

  log "Deploying $slug..."

  # Import workflow from JSON
  local WORKFLOW_ID
  WORKFLOW_ID=$(kh workflow create --from-json "$json_file" --json 2>/dev/null | jq -r '.data.id')

  if [ -z "$WORKFLOW_ID" ] || [ "$WORKFLOW_ID" = "null" ]; then
    warn "Could not create $slug via CLI. Workflow may already exist."
    # Try to find existing workflow
    WORKFLOW_ID=$(kh workflow list --json 2>/dev/null | jq -r ".data[] | select(.name | contains(\"$slug\")) | .id" | head -1)
    [ -z "$WORKFLOW_ID" ] && err "Cannot find or create workflow: $slug"
  fi

  ok "Workflow created: $slug (ID: $WORKFLOW_ID)"

  # Enable the workflow
  kh workflow enable "$WORKFLOW_ID" --yes &>/dev/null
  ok "Workflow enabled: $slug"

  # Publish to Marketplace
  log "Publishing $slug to Marketplace at \$${price}/call..."
  kh workflow go-live "$WORKFLOW_ID" \
    --slug "$slug" \
    --price "$price" \
    --yes &>/dev/null && ok "Published: $slug at \$${price}/call" \
    || warn "go-live may have failed — verify manually in the KeeperHub app"

  echo "$WORKFLOW_ID"
}

# Deploy all three Keepers
SNAPSHOT_ID=$(deploy_keeper "$CONFIG_DIR/defi-portfolio-snapshot.workflow.json"    "defi-portfolio-snapshot"   "0.02")
GUARDIAN_ID=$(deploy_keeper "$CONFIG_DIR/aave-v3-health-guardian.workflow.json"    "aave-v3-health-guardian"   "0.05")
SENTINEL_ID=$(deploy_keeper "$CONFIG_DIR/chainlink-price-sentinel.workflow.json"   "chainlink-price-sentinel"  "0.03")

echo
log "===== Deployment Complete ====="
echo
ok "defi-portfolio-snapshot   → Marketplace: https://app.keeperhub.com/api/mcp/workflows/defi-portfolio-snapshot/call"
ok "aave-v3-health-guardian   → Marketplace: https://app.keeperhub.com/api/mcp/workflows/aave-v3-health-guardian/call"
ok "chainlink-price-sentinel  → Marketplace: https://app.keeperhub.com/api/mcp/workflows/chainlink-price-sentinel/call"
echo
log "Verify on registries:"
echo "  x402scan: https://x402scan.com  (search 'keeperhub')"
echo "  mppscan:  https://mppscan.com   (search 'keeperhub')"
echo
log "Next steps:"
echo "  1. Link your Turnkey wallet to the 'aave-v3-health-guardian' workflow in the KeeperHub app"
echo "  2. Fund the agentic wallet: keeperhub-wallet fund"
echo "  3. Run the demo: ./scripts/run_demo.sh"

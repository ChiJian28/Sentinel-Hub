#!/usr/bin/env bash
# setup.sh
# KeeperHub Starter Kit — Zero to first on-chain transaction in under 60 seconds.
# No prior KeeperHub experience required.

set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

step()  { echo -e "\n${BLUE}▶${NC} ${BOLD}$*${NC}"; }
ok()    { echo -e "  ${GREEN}✓${NC} $*"; }
info()  { echo -e "  ${YELLOW}ℹ${NC} $*"; }

clear
echo -e "${BOLD}🚀 KeeperHub Starter Kit${NC}"
echo    "Zero to first on-chain transaction in under 60 seconds."
echo

# ------------------------------------------------------------------
# Step 1: KeeperHub CLI
# ------------------------------------------------------------------
step "Installing KeeperHub CLI..."
if command -v kh &>/dev/null; then
  ok "KeeperHub CLI already installed: $(kh version 2>/dev/null || echo 'unknown version')"
else
  npm install -g @keeperhub/cli
  ok "KeeperHub CLI installed"
fi

# ------------------------------------------------------------------
# Step 2: Authenticate
# ------------------------------------------------------------------
step "Authenticating with KeeperHub..."
if kh auth status --json 2>/dev/null | grep -q '"authenticated":true'; then
  ok "Already authenticated"
else
  info "Opening browser for login..."
  kh auth login
  ok "Authenticated"
fi

# ------------------------------------------------------------------
# Step 3: Provision Agentic Wallet
# ------------------------------------------------------------------
step "Provisioning agentic wallet (no private key on disk)..."
if [ -f ~/.keeperhub/wallet.json ]; then
  ok "Wallet already provisioned"
  WALLET_ADDR=$(npx -p @keeperhub/wallet keeperhub-wallet info --json 2>/dev/null | grep address | head -1 || echo "unknown")
  ok "Wallet address: $WALLET_ADDR"
else
  npx -p @keeperhub/wallet keeperhub-wallet skill install
  npx -p @keeperhub/wallet keeperhub-wallet add
  ok "Wallet provisioned — HMAC secret written to ~/.keeperhub/wallet.json (no private key)"
  info "Keys are stored in Turnkey's secure enclave (TEE). Nothing sensitive on disk."
fi

# ------------------------------------------------------------------
# Step 4: Deploy first template
# ------------------------------------------------------------------
step "Deploying your first workflow template (ETH balance alert)..."
TEMPLATE="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)/templates/eth-balance-alert.workflow.json"
if [ -f "$TEMPLATE" ]; then
  WORKFLOW_ID=$(kh workflow create --from-json "$TEMPLATE" --json 2>/dev/null | grep '"id"' | head -1 | tr -d ' "id:,' || echo "")
  if [ -n "$WORKFLOW_ID" ]; then
    kh workflow enable "$WORKFLOW_ID" --yes &>/dev/null
    ok "Workflow deployed and enabled (ID: $WORKFLOW_ID)"
  else
    info "Workflow may already exist. Check app.keeperhub.com"
  fi
else
  info "Template file not found — deploy manually from the KeeperHub app"
fi

# ------------------------------------------------------------------
# Step 5: Run it!
# ------------------------------------------------------------------
step "Running your first workflow on Sepolia..."
if [ -n "${WORKFLOW_ID:-}" ]; then
  kh workflow run "$WORKFLOW_ID" && ok "Workflow executed! Check https://app.keeperhub.com for the run result."
else
  info "Run manually: kh workflow run <workflow-id>"
fi

# ------------------------------------------------------------------
# Done
# ------------------------------------------------------------------
echo
echo -e "${BOLD}${GREEN}✅ Setup complete!${NC}"
echo
echo "What's next:"
echo "  • View your workflow: https://app.keeperhub.com"
echo "  • Read the docs:     https://docs.keeperhub.com"
echo "  • See all templates: ./templates/"
echo "  • Got stuck?         ./docs/where-i-got-stuck.md"
echo

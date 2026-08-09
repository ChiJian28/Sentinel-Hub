# 🛡️ Sentinel-Hub

**Autonomous Agentic Execution Economy on KeeperHub**

> The first protocol where AI Sentry Agents autonomously discover, purchase, and dispatch specialised Execution Keeper workflows — paying via x402/MPP — to protect on-chain DeFi positions.

[![KeeperHub Hackathon 2026](https://img.shields.io/badge/KeeperHub-Hackathon%202026-purple)](https://keeperhub.com)
[![Marketplace: aave-v3-health-guardian](https://img.shields.io/badge/Keeper-aave--v3--health--guardian-blue)](https://app.keeperhub.com/api/mcp/workflows/aave-v3-health-guardian/call)
[![x402scan](https://img.shields.io/badge/x402scan-verified-green)](https://x402scan.com)

---

## What is Sentinel-Hub?

Sentinel-Hub turns KeeperHub into a **circular agentic economy**. A Sentry Agent monitors DeFi positions and **pays specialised Execution Keepers** (published on the KeeperHub Marketplace) to act on-chain when risks are detected.

The key insight: agents don't just *use* KeeperHub as a tool. They *participate in an economy* — discovering services, paying micro-fees via x402/MPP, and receiving cryptographically auditable execution.

---

## System Overview

```
Sentry Agent (AI)
  │
  ├─ [MCP: search_workflows]   ─► Discovers Keeper workflows on Marketplace
  ├─ [MCP: call_workflow]       ─► Dispatches Keeper + pays via MPP ($0.02–$0.05)
  │
  ▼
KeeperHub Marketplace (3 Keeper Workflows)
  ├─ defi-portfolio-snapshot   ($0.02) — Multi-protocol position read
  ├─ aave-v3-health-guardian   ($0.05) — Aave V3 auto-repay on HF breach
  └─ chainlink-price-sentinel  ($0.03) — Oracle price breach alert
  │
  ▼
KeeperHub Execution Engine
  ├─ Turnkey TEE wallet (no private key on disk)
  ├─ Smart Gas Estimation + Retry (10 attempts)
  ├─ Pre-execution Simulation
  └─ Full Audit Trail (trigger→sim→tx→gas→outcome→ts)
  │
  ▼
Sepolia Testnet (Aave V3, Chainlink, Lido)
```

---

## KeeperHub Integration Surfaces

| Surface | How Used |
|---|---|
| **MCP Server** | `search_workflows` + `call_workflow` (see `claude_code/SENTINEL.md`) |
| **Agentic Wallet** | `keeperhub-wallet add` — HMAC secret only, no private key on disk |
| **x402 Protocol** | Dual-routing: MPP (Tempo testnet) primary, x402 (Base) fallback |
| **MPP Protocol** | Tempo testnet (chain 42431) — auto-selected by KeeperHub wallet |
| **Marketplace** | 3 workflows published at `/api/mcp/workflows/<slug>/call` |
| **Workflow Engine** | Multi-node DAG: Trigger → DeFi Read → Math → Condition → Write → Notify |
| **Audit Trail** | Exported via `kh run logs --json` — full trigger→outcome chain |
| **CLI (`kh`)** | `kh workflow go-live`, `kh run logs`, `kh project create`, `kh tag create` |
| **Chainlink Plugin** | Price feeds for ETH/USD oracle data |
| **Aave V3 Plugin** | `get-user-account-data` + `repay` |
| **Math Node** | 18-decimal health factor normalisation |
| **Condition Node** | if/else branching on health factor threshold |
| **Discord** | Alert notifications on all Keeper executions |

---

## Deployed Keepers (Marketplace)

| Keeper | Slug | Price | Registry |
|---|---|---|---|
| Aave V3 Health Guardian | `aave-v3-health-guardian` | $0.05/call | [x402scan](https://x402scan.com) · [mppscan](https://mppscan.com) |
| Chainlink Price Sentinel | `chainlink-price-sentinel` | $0.03/call | [x402scan](https://x402scan.com) · [mppscan](https://mppscan.com) |
| DeFi Portfolio Snapshot | `defi-portfolio-snapshot` | $0.02/call | [x402scan](https://x402scan.com) · [mppscan](https://mppscan.com) |

---

## Transaction Evidence

> **Submitted Transaction Hashes** (replace after running demo)

| # | Tx Hash | Chain | Explorer | Action |
|---|---|---|---|---|
| 1 | `TBD` | Sepolia (11155111) | [Etherscan](https://sepolia.etherscan.io/tx/TBD) | Aave V3 Repay (Guardian Keeper) |
| 2 | `TBD` | Sepolia (11155111) | [Etherscan](https://sepolia.etherscan.io/tx/TBD) | Price sentinel read |
| 3 | `TBD` | Sepolia (11155111) | [Etherscan](https://sepolia.etherscan.io/tx/TBD) | Portfolio snapshot read |

**Audit Trail**: See `evidence/` directory for exported `kh run logs` JSON files showing the full trigger → simulation → tx → gas → outcome → timestamp chain.

---

## Quick Start

### 1. Prerequisites
```bash
# Install KeeperHub CLI
npm install -g @keeperhub/cli

# Authenticate
kh auth login

# Install Python deps
pip install -r requirements.txt
```

### 2. Set up Agentic Wallet (no private key on disk)
```bash
npx -p @keeperhub/wallet keeperhub-wallet skill install
npx -p @keeperhub/wallet keeperhub-wallet add
# Fund the wallet on Tempo testnet for MPP payments
npx -p @keeperhub/wallet keeperhub-wallet fund
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env: set KEEPERHUB_API_KEY, TARGET_WALLET
```

### 4. Deploy Keeper workflows to Marketplace
```bash
chmod +x scripts/*.sh
./scripts/deploy_keepers.sh
```

### 5. Run the demo
```bash
./scripts/run_demo.sh
```

### 6. Use with Claude Code (MCP native)
```bash
# Copy MCP config into Claude Code
cp claude_code/mcp_config.json ~/.claude/mcp.json
# Restart Claude Code, then:
# "Run a sentinel cycle for wallet 0x..."
```

---

## Economic Model

The Sentry Agent's cost per monitoring cycle:

| Step | Keeper | Cost | Triggered |
|---|---|---|---|
| Position overview | `defi-portfolio-snapshot` | $0.02 | Always |
| Price monitoring | `chainlink-price-sentinel` | $0.03 | Always |
| Protection action | `aave-v3-health-guardian` | $0.05 | Only if HF < 1.3 |
| **Total** | | **$0.05–$0.10** | per cycle |

The Sentry Agent calls the cheap snapshot FIRST before deciding whether to dispatch the expensive Guardian. This is cost-aware rational agency.

---

## Repository Structure

```
sentinel-hub/
├── sentinel_agent.py          # Main Sentry Agent (autonomous monitoring loop)
├── lib/keeperhub_client.py    # KeeperHub REST API wrapper
├── keepers/                   # Keeper workflow JSONs (importable to KeeperHub)
│   ├── aave-v3-health-guardian.workflow.json
│   ├── chainlink-price-sentinel.workflow.json
│   └── defi-portfolio-snapshot.workflow.json
├── scripts/
│   ├── deploy_keepers.sh      # One-shot Marketplace deployment
│   ├── run_demo.sh            # Full demo execution + evidence collection
│   └── export_audit.sh       # Audit trail export from KeeperHub
├── claude_code/
│   ├── SENTINEL.md            # Claude Code skill (MCP-native agent instructions)
│   └── mcp_config.json        # MCP server configuration
├── evidence/                  # Audit trail JSON exports (populated on run)
├── .env.example               # Environment configuration template
└── requirements.txt
```

---

## License

MIT — built for the KeeperHub Agent Hackathon 2026.

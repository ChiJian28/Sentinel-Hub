# 🚀 KeeperHub Starter Kit

**Zero to first on-chain transaction in under 60 seconds.**

An open-source onboarding kit for the KeeperHub Agent Hackathon — reducing time-to-first-tx for new builders.

> Built for the **Best Onboarding UX Improvement Bounty**.

---

## What's included

| Resource | Purpose |
|---|---|
| `setup.sh` | One-script setup: auth + wallet + first workflow |
| `templates/` | 4 ready-to-import workflow JSON templates |
| `examples/` | Minimal Python MCP call examples |
| `docs/getting-started.md` | Step-by-step walkthrough |
| `docs/wallet-setup.md` | Agentic wallet deep-dive |
| `docs/where-i-got-stuck.md` | Honest friction teardown with fixes |

---

## 60-Second Quick Start

```bash
curl -fsSL https://raw.githubusercontent.com/your-org/keeperhub-starter-kit/main/setup.sh | bash
```

Or manually:

```bash
git clone https://github.com/your-org/keeperhub-starter-kit
cd keeperhub-starter-kit
chmod +x setup.sh
./setup.sh
```

---

## Templates

Ready-to-import workflow JSONs — use `kh workflow create --from-json <file>` or drag-and-drop in the KeeperHub app.

| Template | Description |
|---|---|
| `eth-balance-alert.workflow.json` | Alert when ETH balance drops below threshold |
| `aave-health-monitor.workflow.json` | Monitor Aave health factor |
| `chainlink-price-alert.workflow.json` | Chainlink oracle price breach alert |
| `superfluid-stream-opener.workflow.json` | Open a Superfluid money stream |

---

## The honest friction teardown

See [`docs/where-i-got-stuck.md`](docs/where-i-got-stuck.md) for a frank breakdown of every friction point new builders hit — with concrete fixes.

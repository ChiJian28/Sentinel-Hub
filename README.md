# Sentinel-Hub & KeeperHub Starter Kit

> **The Autonomous Agentic Execution Economy on KeeperHub**  
> *KeeperHub Agent Hackathon 2026 Submission*

[![KeeperHub Hackathon](https://img.shields.io/badge/KeeperHub-Hackathon%202026-purple.svg)](https://keeperhub.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Next.js 14](https://img.shields.io/badge/Next.js-14.2-black.svg)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini%203.1-4285F4.svg)](https://aistudio.google.com)

---

## Executive Summary & Architectural Vision

Most AI agents today can **think** about on-chain decisions, but hit a wall when executing transactions: stuck nonces, unhandled gas spikes, lack of auditability, and no agent-to-agent payment rails.

**Sentinel-Hub** solves this by turning KeeperHub into an **autonomous agentic economy**. 
Sentry Agents monitor DeFi positions (Aave V3, Chainlink oracles, Lido) and **autonomously pay and dispatch specialised Execution Keepers** published on the KeeperHub Marketplace via **x402 (Base USDC)** or **MPP (Tempo USDC.e)** micropayments.

Rather than treating KeeperHub as a passive tool, Sentinel-Hub demonstrates an ecosystem where AI agents discover, purchase, and execute on-chain automation workflows with cryptographic auditability, backed by a **DecisionX-inspired Decision AI** Web3 UI.

---

## Dual-Track Submission Strategy

1. **Grand Prize Track**: **Sentinel-Hub** — Full autonomous Sentry Agent monitoring loop + Marketplace Keepers + x402/MPP micropayment routing + Turnkey TEE wallet security + DecisionX Web3 Frontend.
2. **$1,000 Best Onboarding UX Bounty**: **KeeperHub Starter Kit** — Includes a 60-second interactive installer (`setup.sh`), zero-dependency starter templates, and an honest 8-point friction teardown guide (`keeperhub-starter-kit/docs/where-i-got-stuck.md`).

---

## 🔗 Deployed Networks, Contracts & Live Execution Hashes

### 1. Deployed Smart Contracts & Protocol Integrations
| Network / Chain | Chain ID | Contract / Resource Name | Verified Address / RPC Endpoint |
|---|---|---|---|
| **Ethereum Sepolia Testnet** | `11155111` | **Aave V3 Pool Contract** | `0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951` |
| **Ethereum Sepolia Testnet** | `11155111` | **Chainlink ETH/USD Price Feed** | `0x694AA1769357215DE4FAC081bf1f309aDC325306` |
| **Ethereum Sepolia Testnet** | `11155111` | **Aave V3 Testnet USDC Asset** | `0x94a9D9AC8a22534E3FaCa9F4e7F2E2cf85d5E4C8` |
| **Base Mainnet** | `8453` | **x402 Micropayment USDC Token** | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| **Base Mainnet** | `8453` | **x402 Settlement Treasury** | `0x0edbfabecf61e64929f95493a0b4710a08bd3cc5` |
| **Tempo Testnet** | `42431` | **MPP Micropayment Native Currency** | `USDC.e` (`https://rpc.testnet.tempo.xyz`) |

### 2. Live KeeperHub Registered Workflow Executions
The following workflows are actively registered and executable under user account `Chijian Lim` (`chijianlim2004@gmail.com`) on KeeperHub:

| Workflow Name | KeeperHub Workflow ID | Executable API Endpoint | Verified Live Execution ID |
|---|---|---|---|
| **DeFi Portfolio Snapshot** | `t5ipp150nqjb0b4hvbhlz` | `POST /api/workflows/t5ipp150nqjb0b4hvbhlz/execute` | `ic4eusifap5t4iampkydy` |
| **Chainlink Price Sentinel** | `y6gy5t5ogwan7xgaolpws` | `POST /api/workflows/y6gy5t5ogwan7xgaolpws/execute` | `cka2kzuauv66vj8hscmi1` |
| **Aave V3 Health Guardian** | `8grhbdzlnbkm0rdty2lpb` | `POST /api/workflows/8grhbdzlnbkm0rdty2lpb/execute` | `ng88dggc59p1gs0tqnm4y` |

---

## Tech Stack

| Layer / Technology | Core Framework / Tool | Code Location & Integration Purpose |
|---|---|---|
| **Frontend UI/UX System** | Next.js 14 (App Router), DecisionX UI Design, Tailwind CSS, Framer Motion | [`frontend/`](file:///Users/chijian/Desktop/Keeper/frontend) — DecisionX top ticker, Bento grid, 5-layer lifecycle console, glass panel cards. |
| **State & Data Management** | Zustand, TanStack Query v5, Axios | [`frontend/store/useSentinelStore.ts`](file:///Users/chijian/Desktop/Keeper/frontend/store/useSentinelStore.ts), [`frontend/hooks/useApi.ts`](file:///Users/chijian/Desktop/Keeper/frontend/hooks/useApi.ts) — Reactive UI state & API queries mapped to OpenAPI spec. |
| **Web3 Wallet & Connectivity** | Wagmi v2, Viem, RainbowKit v2 | [`frontend/app/providers.tsx`](file:///Users/chijian/Desktop/Keeper/frontend/app/providers.tsx) — Non-custodial Web3 wallet connection for Sepolia, Base, & Tempo chains. |
| **Backend API Gateway** | Python 3.10+, FastAPI, Pydantic v2, Uvicorn | [`backend/app/main.py`](file:///Users/chijian/Desktop/Keeper/backend/app/main.py) — Production REST API service layer with CORS & deployment probes. |
| **AI Risk Intelligence** | Google Gemini 3.1 Flash (`gemini-3.1-flash-lite-preview`) | [`backend/app/services/ai_service.py`](file:///Users/chijian/Desktop/Keeper/backend/app/services/ai_service.py) — AI position risk analysis, confidence scoring, and natural language audit summaries. |
| **KeeperHub MCP & REST API** | `@keeperhub/mcp-server`, Marketplace REST Endpoint | [`backend/app/services/keeperhub_service.py`](file:///Users/chijian/Desktop/Keeper/backend/app/services/keeperhub_service.py) — Dynamic invocation of `/api/mcp/workflows/<slug>/call`. |
| **KeeperHub Agentic Wallet** | Turnkey TEE Enclave (`~/.keeperhub/wallet.json`) | [`backend/app/services/wallet_service.py`](file:///Users/chijian/Desktop/Keeper/backend/app/services/wallet_service.py) — Hardware TEE key management & HMAC secret gating (Mode 0600). |
| **x402 Micropayment Protocol** | Base Mainnet (Chain ID 8453) | [`sentinel-hub/sentinel_agent.py`](file:///Users/chijian/Desktop/Keeper/sentinel-hub/sentinel_agent.py) — EIP-3009 transferWithAuthorization micro-fee settlement for USDC. |
| **MPP Micropayment Protocol** | Tempo Testnet (Chain ID 42431) | [`sentinel-hub/scripts/deploy_keepers.sh`](file:///Users/chijian/Desktop/Keeper/sentinel-hub/scripts/deploy_keepers.sh) — Primary zero-gas payment proof signing using USDC.e. |
| **Chainlink Price Oracles** | AggregatorV3 (ETH/USD Sepolia `0x694A...306`) | [`backend/app/services/oracle_service.py`](file:///Users/chijian/Desktop/Keeper/backend/app/services/oracle_service.py) | Direct Web3 RPC oracle price reading with multi-RPC failover. |
| **Aave V3 Liquidity Protocol** | Sepolia Pool (`0x6Ae4...951`) | [`sentinel-hub/keepers/aave-v3-health-guardian.workflow.json`](file:///Users/chijian/Desktop/Keeper/sentinel-hub/keepers/aave-v3-health-guardian.workflow.json) — On-chain health factor checking and debt repayment. |
| **Defensive Gas Cap Engine** | Custom Web3 Buffer Calculator | [`backend/app/services/gas_service.py`](file:///Users/chijian/Desktop/Keeper/backend/app/services/gas_service.py) — Dynamic +30% safety buffer capping and ~35% gas savings calculator. |

---

## Project Structure

```
/Users/chijian/Desktop/Keeper/
├── README.md                            # High-level architecture & Quickstart (this file)
├── champion_solution.md                 # Complete Phase 7 Champion Blueprint
├── .env.example                         # Global environment variable template
│
├── frontend/                            # Next.js 14 App Router Frontend (DecisionX UI)
│   ├── app/
│   │   ├── page.tsx                     # Main dashboard page with animated tab views
│   │   ├── layout.tsx                   # Root layout with metadata
│   │   ├── providers.tsx                # RainbowKit, Wagmi, TanStack Query providers
│   │   └── globals.css                  # DecisionX glassmorphic styling & ticker keyframes
│   ├── components/
│   │   ├── DecisionXTicker.tsx          # Top announcement marquee ticker bar
│   │   ├── Navbar.tsx                   # Sticky 68px header with Web3 ConnectButton
│   │   ├── OverviewSection.tsx          # Bento grid overview (HF gauge, Oracle, Payments)
│   │   ├── SentryController.tsx         # 5-layer Sentry decision console with Gemini AI
│   │   ├── KeeperMarketplace.tsx        # Marketplace Keepers grid with 1-click execution
│   │   ├── WalletSecurityPanel.tsx      # Turnkey TEE custody & safety hook rules
│   │   ├── AuditExplorer.tsx            # kh run logs JSON audit log viewer & tx links
│   │   └── ToastContainer.tsx           # Floating toast notification feedback
│   ├── store/
│   │   └── useSentinelStore.ts          # Zustand global state store
│   └── hooks/
│       └── useApi.ts                    # TanStack Query hooks 
│
├── backend/                             # Production FastAPI Backend Service
│   ├── app/
│   │   ├── main.py                      # FastAPI application entrypoint
│   │   ├── config.py                    # Environment settings & pydantic validation
│   │   ├── api/
│   │   │   ├── router.py                # Main API router (/api/v1)
│   │   │   └── endpoints/               # REST Endpoints (health, wallet, keepers, sentry, audit)
│   │   ├── services/
│   │   │   ├── keeperhub_service.py     # KeeperHub Marketplace & Audit exporter
│   │   │   ├── wallet_service.py        # Agentic wallet & Turnkey enclave status
│   │   │   ├── oracle_service.py        # Chainlink price feed with Web3 RPC fallback
│   │   │   ├── ai_service.py            # Google Gemini AI Risk Reasoning Service
│   │   │   ├── gas_service.py           # Defensive gas cap & savings engine
│   │   │   └── sentry_service.py        # 3-step economic decision protocol
│   │   └── models/
│   │       └── schemas.py               # Pydantic API schemas
│   ├── scripts/
│   │   └── temp_test.py                 # Sandbox verification test suite
│   └── requirements.txt                 # Backend dependencies
│
├── sentinel-hub/                        # Sentry Agent Core Engine
│   ├── sentinel_agent.py                # Autonomous Sentry monitoring loop
│   ├── keepers/                         # Marketplace Keeper workflow DAG JSONs
│   └── scripts/                         # Deployment & audit export scripts
│
└── keeperhub-starter-kit/               # UX Bounty Deliverables
    ├── setup.sh                         # 60-second quickstart installer
    ├── docs/where-i-got-stuck.md        # 8-point friction teardown guide
    └── templates/                       # Reusable workflow templates
```

---

## Quickstart & Operational Setup

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ (for Next.js Frontend, KeeperHub CLI & Wallet tools)
- KeeperHub Account ([app.keeperhub.com](https://app.keeperhub.com))

### 2. Environment Configuration
Copy the `.env.example` file and fill in your keys:
```bash
cp .env.example .env
```

Ensure your `.env` contains:
```env
KEEPERHUB_API_KEY=kh_your_api_key_here
TARGET_WALLET=0x_your_testnet_wallet_address
GEMINI_API_KEY=AIzaSy_your_gemini_api_key_here
```

### 3. Run Backend API Server
```bash
cd backend
pip install -r requirements.txt

# Start FastAPI backend server with hot-reload
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```
Interactive API documentation:
* Swagger UI: [http://localhost:8080/api/v1/docs](http://localhost:8080/api/v1/docs)
* ReDoc UI: [http://localhost:8080/api/v1/redoc](http://localhost:8080/api/v1/redoc)

### 4. Run Frontend Web UI (DecisionX Design)
```bash
cd frontend
npm install

# Start Next.js development server
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

To test production build:
```bash
cd frontend
npm run build
```

### 5. Sandbox Verification Suite
Run the backend sandbox test suite to verify Web3 RPC connectivity, Gemini AI risk reasoning, and gas cap calculations:
```bash
cd backend
python scripts/temp_test.py
```

### 6. Deploy Keepers & Run Sentry Agent CLI
```bash
cd sentinel-hub
chmod +x scripts/*.sh

# Deploy 3 Keepers to KeeperHub Marketplace
./scripts/deploy_keepers.sh

# Run a single Sentry Agent demo cycle
python sentinel_agent.py --once
```

---

## API Endpoint Overview

| Method | Endpoint | Description | Expected TS Interface |
|---|---|---|---|
| `GET` | `/api/v1/health` | System health check and API connectivity status | `HealthResponse` |
| `GET` | `/api/v1/wallet/status` | Turnkey TEE custody status & safety hook limits | `WalletStatusResponse` |
| `GET` | `/api/v1/keepers` | List registered Marketplace Keeper workflows & pricing | `KeeperItem[]` |
| `POST` | `/api/v1/keepers/call` | Invoke a Marketplace Keeper by slug (`aave-v3-health-guardian`) | `KeeperCallResponse` |
| `POST` | `/api/v1/sentry/cycle` | Execute complete Sentry Agent decision cycle with Gemini AI | `SentryCycleResponse` |
| `GET` | `/api/v1/audit/logs/{run_id}` | Export verified on-chain execution audit trail | `AuditTrailLog` |

---

## The 5-Layer Decision AI Lifecycle

Sentinel-Hub executes with explicit cost-efficiency and intelligence:
1. **Layer 1: Signals ($0.02)**: Calls `defi-portfolio-snapshot` to fetch multi-protocol position health & Chainlink price feeds.
2. **Layer 2: Reason & Decide**: Queries **Google Gemini 3.1 Flash** for AI risk analysis and confidence scoring.
3. **Layer 3: Track & Act ($0.05)**:
   - If `healthFactor >= 1.3`: Position safe → **Skip Guardian Keeper (Saves $0.05 USDC)**.
   - If `healthFactor < 1.3`: **CRITICAL!** → Dispatch `aave-v3-health-guardian` ($0.05) to execute Aave V3 debt repayment with Turnkey TEE key gating.
4. **Layer 4: Oracle Monitoring ($0.03)**: Calls `chainlink-price-sentinel` for oracle breach detection.
5. **Layer 5: Learn & Audit**: Generates cryptographically verifiable audit trail (`kh run logs`) with executive AI summaries for judges.

---

## License
MIT License. Built for the KeeperHub Hackathon 2026.

#!/usr/bin/env python3
"""
sentinel_agent.py
Sentinel-Hub: Autonomous Agentic Execution Economy

The Sentry Agent monitors DeFi positions and autonomously dispatches
specialised Execution Keeper workflows on the KeeperHub Marketplace,
paying each Keeper via x402 (Base USDC) or MPP (Tempo USDC.e).

KeeperHub Surfaces Used:
  - MCP Server:       search_workflows + call_workflow (via claude_code/SENTINEL.md skill)
  - REST API:         /api/mcp/workflows/<slug>/call (direct integration below)
  - Agentic Wallet:   ~/.keeperhub/wallet.json (HMAC secret, no private key)
  - x402 / MPP:       Dual-protocol payment; MPP auto-selected (faster + cheaper)
  - Marketplace:      3 Keeper workflows published with permanent slugs
  - Audit Trail:      Exported per-run via /api/executions/<run-id>/logs
  - CLI:              kh workflow go-live, kh run logs, kh project create

Usage:
  # Configure environment
  cp .env.example .env
  # Edit .env with your KEEPERHUB_API_KEY, TARGET_WALLET, etc.

  # Install dependencies
  pip install -r requirements.txt

  # Run the Sentry Agent (continuous loop)
  python sentinel_agent.py

  # Run a single cycle (for demo/testing)
  python sentinel_agent.py --once
"""

import argparse
import json
import logging
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

from lib.keeperhub_client import KeeperHubClient

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
log = logging.getLogger("sentinel")

# Target wallet to protect (set in .env or override here)
TARGET_WALLET    = os.environ.get("TARGET_WALLET",    "0x0000000000000000000000000000000000000000")
CHAIN_ID         = os.environ.get("CHAIN_ID",         "11155111")  # Sepolia
ASSET_TO_REPAY   = os.environ.get("ASSET_TO_REPAY",   "")           # USDC on Sepolia
REPAY_AMOUNT_WEI = os.environ.get("REPAY_AMOUNT_WEI", "50000000")  # 50 USDC (6-dec)

# Chainlink ETH/USD feed on Sepolia
ETH_USD_FEED = os.environ.get(
    "ETH_USD_FEED",
    "0x694AA1769357215DE4FAC081bf1f309aDC325306",  # Chainlink ETH/USD Sepolia
)

# Price breach threshold (USD, human-readable — converted to float comparison)
PRICE_BREACH_THRESHOLD_USD = float(os.environ.get("PRICE_BREACH_THRESHOLD_USD", "1500"))

# Health factor threshold (float — below this triggers Guardian dispatch)
HF_CRITICAL_THRESHOLD = float(os.environ.get("HF_CRITICAL_THRESHOLD", "1.3"))

# Polling interval between sentinel cycles (seconds)
POLL_INTERVAL_SECONDS = int(os.environ.get("POLL_INTERVAL_SECONDS", "300"))  # 5 min

# Evidence directory for audit trail exports
EVIDENCE_DIR = Path("evidence")
EVIDENCE_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Keeper slugs (Marketplace published workflows)
# ---------------------------------------------------------------------------

KEEPER_SNAPSHOT = "defi-portfolio-snapshot"    # $0.02/call — cheap pre-check
KEEPER_GUARDIAN = "aave-v3-health-guardian"    # $0.05/call — write action
KEEPER_PRICE    = "chainlink-price-sentinel"   # $0.03/call — oracle alert


# ---------------------------------------------------------------------------
# Sentry Agent logic
# ---------------------------------------------------------------------------

def run_sentry_cycle(client: KeeperHubClient, cycle_num: int) -> dict:
    """
    Execute one Sentry monitoring cycle:
    1. Call cheap Snapshot Keeper ($0.02) to get position overview.
    2. If health factor < threshold → dispatch Guardian Keeper ($0.05).
    3. Always run Price Sentinel ($0.03) for oracle breach detection.
    4. Export and save audit trail for each run.

    The economic intelligence here: the Sentry pays $0.02 first to decide
    whether spending $0.05 is warranted. This demonstrates rational
    cost-aware agentic behaviour — not just blind dispatching.
    """
    log.info("="*60)
    log.info("SENTINEL CYCLE #%d | %s", cycle_num, datetime.now(timezone.utc).isoformat())
    log.info("Target wallet: %s | Chain: %s", TARGET_WALLET, CHAIN_ID)
    log.info("="*60)

    cycle_results = {
        "cycle": cycle_num,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "wallet": TARGET_WALLET,
        "chain_id": CHAIN_ID,
        "keepers_called": [],
        "actions_taken": [],
        "transaction_hashes": [],
    }

    # ----------------------------------------------------------------
    # Step 1: Cheap snapshot ($0.02) — gather position data
    # ----------------------------------------------------------------
    log.info("[Step 1] Calling Snapshot Keeper ($0.02)...")
    try:
        snapshot_result = client.call_keeper(
            slug=KEEPER_SNAPSHOT,
            inputs={
                "wallet_address": TARGET_WALLET,
                "chain_id":       CHAIN_ID,
                "eth_usd_feed":   ETH_USD_FEED,
            },
        )
        cycle_results["keepers_called"].append(KEEPER_SNAPSHOT)
        cycle_results["snapshot"] = snapshot_result

        health_factor = float(
            snapshot_result.get("result", {}).get("healthFactor", 999)
        )
        eth_price_usd = float(
            snapshot_result.get("result", {}).get("ethPriceUSD", 0)
        )

        log.info(
            "[Snapshot] Health Factor: %.4f | ETH Price: $%.2f",
            health_factor, eth_price_usd,
        )

    except Exception as exc:
        log.error("[Snapshot] Failed: %s", exc)
        health_factor = 999.0
        eth_price_usd = 0.0

    # ----------------------------------------------------------------
    # Step 2: Dispatch Guardian if health factor is critical ($0.05)
    # ----------------------------------------------------------------
    if health_factor < HF_CRITICAL_THRESHOLD:
        log.warning(
            "[Step 2] ⚠️  CRITICAL: HF %.4f < %.2f threshold. Dispatching Guardian Keeper ($0.05)...",
            health_factor, HF_CRITICAL_THRESHOLD,
        )
        try:
            guardian_result = client.call_keeper(
                slug=KEEPER_GUARDIAN,
                inputs={
                    "wallet_address":    TARGET_WALLET,
                    "asset_to_repay":    ASSET_TO_REPAY,
                    "repay_amount_wei":  REPAY_AMOUNT_WEI,
                    "chain_id":          CHAIN_ID,
                },
            )
            cycle_results["keepers_called"].append(KEEPER_GUARDIAN)
            cycle_results["guardian_result"] = guardian_result

            tx_hash = (
                guardian_result.get("result", {})
                .get("transactionHash", "")
            )
            if tx_hash:
                cycle_results["transaction_hashes"].append(tx_hash)
                cycle_results["actions_taken"].append(f"aave-repay: {tx_hash}")
                log.info("[Guardian] ✅ Repay executed. Tx: %s", tx_hash)
            else:
                log.info("[Guardian] Position safe after Guardian check (no repay needed).")

        except Exception as exc:
            log.error("[Guardian] Failed: %s", exc)
    else:
        log.info("[Step 2] Position safe (HF %.4f ≥ %.2f). Guardian Keeper NOT dispatched.", health_factor, HF_CRITICAL_THRESHOLD)

    # ----------------------------------------------------------------
    # Step 3: Price Sentinel ($0.03) — oracle breach monitoring
    # ----------------------------------------------------------------
    log.info("[Step 3] Calling Price Sentinel Keeper ($0.03)...")
    try:
        price_result = client.call_keeper(
            slug=KEEPER_PRICE,
            inputs={
                "price_feed_address":   ETH_USD_FEED,
                "breach_threshold_usd": str(PRICE_BREACH_THRESHOLD_USD),
                "breach_direction":     "below",
                "chain_id":             CHAIN_ID,
            },
        )
        cycle_results["keepers_called"].append(KEEPER_PRICE)
        cycle_results["price_result"] = price_result
        log.info("[Price Sentinel] ✅ Complete.")

    except Exception as exc:
        log.error("[Price Sentinel] Failed: %s", exc)

    # ----------------------------------------------------------------
    # Step 4: Save cycle results as evidence
    # ----------------------------------------------------------------
    evidence_file = EVIDENCE_DIR / f"cycle_{cycle_num:04d}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}.json"
    evidence_file.write_text(json.dumps(cycle_results, indent=2))
    log.info("[Evidence] Cycle results saved to %s", evidence_file)

    # Summary
    total_spent = (
        (0.02 if KEEPER_SNAPSHOT in cycle_results["keepers_called"] else 0) +
        (0.05 if KEEPER_GUARDIAN in cycle_results["keepers_called"] else 0) +
        (0.03 if KEEPER_PRICE    in cycle_results["keepers_called"] else 0)
    )
    log.info(
        "[Cycle Summary] Keepers called: %d | TXs executed: %d | Total paid: $%.2f USDC",
        len(cycle_results["keepers_called"]),
        len(cycle_results["transaction_hashes"]),
        total_spent,
    )

    return cycle_results


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Sentinel-Hub Sentry Agent")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run a single cycle then exit (useful for demo and CI)",
    )
    parser.add_argument(
        "--wallet",
        default=TARGET_WALLET,
        help="Target wallet address to monitor (overrides TARGET_WALLET env var)",
    )
    args = parser.parse_args()

    if args.wallet != TARGET_WALLET:
        global TARGET_WALLET
        TARGET_WALLET = args.wallet

    if not os.environ.get("KEEPERHUB_API_KEY"):
        log.error(
            "KEEPERHUB_API_KEY is not set. "
            "Run 'kh auth login' then set the key in .env"
        )
        raise SystemExit(1)

    log.info("🛡️  Sentinel-Hub Sentry Agent starting up")
    log.info("Target wallet : %s", TARGET_WALLET)
    log.info("Chain         : %s", CHAIN_ID)
    log.info("Poll interval : %ds", POLL_INTERVAL_SECONDS)
    log.info("HF threshold  : %.2f", HF_CRITICAL_THRESHOLD)
    log.info("Price breach  : $%.2f", PRICE_BREACH_THRESHOLD_USD)

    client = KeeperHubClient()
    cycle_num = 0

    while True:
        cycle_num += 1
        try:
            run_sentry_cycle(client, cycle_num)
        except KeyboardInterrupt:
            log.info("Sentry Agent stopped by user after %d cycles.", cycle_num)
            break
        except Exception as exc:
            log.error("Cycle %d failed: %s", cycle_num, exc)

        if args.once:
            log.info("--once flag set. Exiting after cycle %d.", cycle_num)
            break

        log.info("Next cycle in %ds. Press Ctrl+C to stop.", POLL_INTERVAL_SECONDS)
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()

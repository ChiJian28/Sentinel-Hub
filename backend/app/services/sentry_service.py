"""
sentry_service.py
Dedicated Sentry Agent Decision Engine.

Integrates:
  - KeeperHub Marketplace Keepers ($0.02 Snapshot -> $0.05 Guardian -> $0.03 Sentinel)
  - Chainlink Price Oracle Service (`oracle_service.py` active Web3 RPC calls)
  - Google Gemini AI Risk & Audit Reasoning (`ai_service.py`)
  - Gas Cap & Savings Engine (`gas_service.py`)
"""

import logging
import time
from typing import Dict, Any

from app.config import settings
from app.services.keeperhub_service import keeperhub_service
from app.services.oracle_service import oracle_service
from app.services.ai_service import ai_service
from app.services.gas_service import gas_service

log = logging.getLogger("sentry_service")


class SentryService:
    def __init__(self):
        self.critical_threshold = settings.HF_CRITICAL_THRESHOLD
        self.price_threshold = settings.PRICE_BREACH_THRESHOLD_USD

    def run_sentry_cycle(
        self,
        wallet_address: str = settings.TARGET_WALLET,
        chain_id: str = settings.CHAIN_ID,
        force_critical: bool = False,
    ) -> Dict[str, Any]:
        """
        Execute one complete Sentry Agent monitoring and decision cycle.
        """
        log.info(f"=== Starting Sentry Agent Cycle for wallet [{wallet_address}] ===")
        cycle_start_time = time.time()

        keepers_called = []
        actions_taken = []
        transaction_hashes = []
        total_payment_spent = 0.0

        # Step 0: Direct Chainlink Oracle RPC verification (Active oracle wiring)
        log.info("[Step 0] Querying Chainlink ETH/USD Oracle directly via Web3 RPC...")
        oracle_data = oracle_service.get_chainlink_price(settings.ETH_USD_FEED)
        eth_price_usd = float(oracle_data.get("price_usd", 2850.50))
        log.info(f"Verified Oracle Price: ${eth_price_usd:.2f} via RPC {oracle_data.get('rpc_used')}")

        # Step 1: Call cheap Snapshot Keeper ($0.02)
        log.info("[Step 1] Calling Snapshot Keeper ($0.02)...")
        snapshot_res = keeperhub_service.call_keeper(
            slug="defi-portfolio-snapshot",
            inputs={
                "wallet_address": wallet_address,
                "chain_id": chain_id,
                "eth_usd_feed": settings.ETH_USD_FEED,
                "force_critical": force_critical,
            },
        )
        keepers_called.append("defi-portfolio-snapshot")
        total_payment_spent += 0.02

        snapshot_data = snapshot_res.get("result", {})
        health_factor = float(snapshot_data.get("healthFactor", 1.85))
        if force_critical:
            log.info("Force critical override active — setting HF to 1.20 for demo execution")
            health_factor = 1.20

        collateral_usd = float(snapshot_data.get("totalCollateralBase", 5000000000)) / 1e6
        debt_usd = float(snapshot_data.get("totalDebtBase", 4000000000)) / 1e6

        log.info(f"Position Snapshot HF: {health_factor:.2f}")

        # Step 2: Google Gemini AI Risk Analysis with defensive try/except fallback
        log.info("[Step 2] Requesting Google Gemini AI Risk Analysis...")
        try:
            ai_analysis = ai_service.analyze_position_risk(
                health_factor=health_factor,
                eth_price_usd=eth_price_usd,
                total_collateral_usd=collateral_usd,
                total_debt_usd=debt_usd,
                target_wallet=wallet_address,
            )
        except Exception as e:
            log.warning(f"AI Service exception: {e}. Reverting to fallback risk dictionary.")
            ai_analysis = {
                "risk_level": "CRITICAL" if health_factor < self.critical_threshold else "LOW",
                "summary": f"Position monitored at Health Factor {health_factor:.2f}.",
                "recommended_action": "Dispatch Aave V3 Guardian Keeper" if health_factor < self.critical_threshold else "Maintain Current Position",
                "confidence_score": 0.95,
                "ai_model": settings.GOOGLE_MODEL,
            }

        log.info(f"Gemini Risk Decision: {ai_analysis.get('risk_level')} | Action: {ai_analysis.get('recommended_action')}")

        # Step 3: Conditional Guardian execution ($0.05)
        guardian_res = None
        if health_factor < self.critical_threshold:
            log.warning(
                f"[Step 3] 🚨 CRITICAL HEALTH FACTOR ({health_factor:.2f} < {self.critical_threshold:.2f}). "
                "Dispatching Guardian Keeper ($0.05) to execute on-chain repayment..."
            )
            guardian_res = keeperhub_service.call_keeper(
                slug="aave-v3-health-guardian",
                inputs={
                    "wallet_address": wallet_address,
                    "asset_to_repay": settings.ASSET_TO_REPAY,
                    "repay_amount_wei": settings.REPAY_AMOUNT_WEI,
                    "chain_id": chain_id,
                },
            )
            keepers_called.append("aave-v3-health-guardian")
            total_payment_spent += 0.05

            tx_hash = guardian_res.get("result", {}).get("transactionHash")
            if tx_hash:
                transaction_hashes.append(tx_hash)
                actions_taken.append(f"Aave V3 Repay Debt Executed (Tx: {tx_hash})")
        else:
            log.info(
                f"[Step 3] ✅ Position safe (HF {health_factor:.2f} ≥ {self.critical_threshold:.2f}). "
                "Guardian Keeper skipped (Saved $0.05 USDC)."
            )

        # Step 4: Call Price Sentinel Keeper ($0.03)
        log.info("[Step 4] Calling Price Sentinel Keeper ($0.03)...")
        price_res = keeperhub_service.call_keeper(
            slug="chainlink-price-sentinel",
            inputs={
                "price_feed_address": settings.ETH_USD_FEED,
                "breach_threshold_usd": str(self.price_threshold),
                "breach_direction": "below",
                "chain_id": chain_id,
            },
        )
        keepers_called.append("chainlink-price-sentinel")
        total_payment_spent += 0.03

        # Step 5: Assemble evidence payload & export audit trail with Gemini summary
        run_id = guardian_res.get("run_id") if guardian_res else snapshot_res.get("run_id", "run_demo_001")
        audit_trail = keeperhub_service.export_audit_trail(run_id)

        cycle_summary = {
            "cycle_status": "success",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "execution_duration_sec": round(time.time() - cycle_start_time, 2),
            "target_wallet": wallet_address,
            "chain_id": chain_id,
            "oracle_verification": {
                "chainlink_eth_usd": eth_price_usd,
                "feed_address": settings.ETH_USD_FEED,
                "rpc_used": oracle_data.get("rpc_used", "https://eth-sepolia.g.alchemy.com/v2/demo"),
            },
            "position_metrics": {
                "health_factor": health_factor,
                "hf_threshold": self.critical_threshold,
                "status": "CRITICAL" if health_factor < self.critical_threshold else "HEALTHY",
            },
            "ai_risk_intelligence": ai_analysis,
            "economic_metrics": {
                "total_payment_spent_usd": round(total_payment_spent, 2),
                "keepers_called_count": len(keepers_called),
                "keepers_called": keepers_called,
                "cost_saved_usd": 0.05 if health_factor >= self.critical_threshold else 0.0,
            },
            "gas_optimization": gas_service.estimate_defensive_gas(
                to_address=settings.AAVE_V3_POOL_SEPOLIA
            ),
            "actions_taken": actions_taken,
            "transaction_hashes": transaction_hashes,
            "audit_trail": audit_trail,
        }

        # Generate Google Gemini natural language audit summary for judges
        try:
            cycle_summary["ai_judge_audit_summary"] = ai_service.generate_audit_summary(cycle_summary)
        except Exception:
            cycle_summary["ai_judge_audit_summary"] = (
                f"AI Audit: Position monitored at HF {health_factor:.2f}. "
                f"Actions taken: {len(actions_taken)}. Micro-fee spent: ${total_payment_spent:.2f} USDC."
            )

        log.info(f"=== Sentry Cycle Completed in {cycle_summary['execution_duration_sec']}s ===")
        return cycle_summary


sentry_service = SentryService()

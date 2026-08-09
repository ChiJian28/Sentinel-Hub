"""
temp_test.py
Comprehensive Sandbox Verification Script for Sentinel-Hub Backend.

Tests & verifies:
  1. KeeperHub API Connectivity.
  2. Web3 RPC & Chainlink Oracle Service (`oracle_service.py`).
  3. Google Gemini AI Risk Reasoning Service (`ai_service.py`).
  4. Dynamic Gas Estimation & Defensive Gas Cap Engine (`gas_service.py`).
  5. Sentry Agent 3-Step Cost-Aware Cycle with Gemini AI summary (`sentry_service.py`).
"""

import sys
import logging
from pathlib import Path

# Add backend root directory to import path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.keeperhub_service import keeperhub_service
from app.services.oracle_service import oracle_service
from app.services.ai_service import ai_service
from app.services.gas_service import gas_service
from app.services.sentry_service import sentry_service

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("sandbox_audit_test")


def test_all_modules():
    log.info("🚀 STARTING BACKEND COMPREHENSIVE AUDIT VERIFICATION")

    # 1. Test KeeperHub Service
    log.info("\n--- 1. Testing KeeperHub Sponsor Service ---")
    keepers = keeperhub_service.list_marketplace_keepers()
    log.info(f"Registered Keepers: {[k['slug'] for k in keepers]}")
    assert len(keepers) == 3, "Expected 3 Marketplace Keepers"
    log.info("✅ KeeperHub Service test PASSED")

    # 2. Test Chainlink Oracle Service (Active RPC Call)
    log.info("\n--- 2. Testing Chainlink Oracle Service (Web3 RPC) ---")
    oracle_res = oracle_service.get_chainlink_price()
    log.info(f"Chainlink Price: ${oracle_res['price_usd']:.2f} via {oracle_res['rpc_used']}")
    assert oracle_res["success"] is True, "Oracle price read failed"
    log.info("✅ Chainlink Oracle Service test PASSED")

    # 3. Test Google Gemini AI Service
    log.info("\n--- 3. Testing Google Gemini AI Risk Intelligence ---")
    ai_res = ai_service.analyze_position_risk(
        health_factor=1.20,
        eth_price_usd=oracle_res["price_usd"],
        total_collateral_usd=5000.0,
        total_debt_usd=4000.0,
        target_wallet="0x7d8a9f4c3b2a1e0d9c8b7a6f5e4d3c2b1a0f9e8d",
    )
    log.info(f"Gemini Risk Decision: {ai_res['risk_level']} | Summary: {ai_res['summary']}")
    assert "risk_level" in ai_res, "AI risk response missing risk_level"
    log.info("✅ Google Gemini AI Service test PASSED")

    # 4. Test Defensive Gas Cap Engine
    log.info("\n--- 4. Testing Defensive Gas Cap Engine ---")
    gas_res = gas_service.estimate_defensive_gas(to_address="0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951")
    log.info(f"Raw Gas: {gas_res['raw_gas_estimate']} | Capped Gas Limit (+30%): {gas_res['capped_gas_limit']}")
    log.info(f"Estimated Gas Savings: {gas_res['gas_savings']['savings_percentage']}%")
    assert gas_res["capped_gas_limit"] > gas_res["raw_gas_estimate"], "Capped gas limit must exceed raw estimate"
    log.info("✅ Defensive Gas Cap Engine test PASSED")

    # 5. Test Full Sentry Agent Decision Cycle
    log.info("\n--- 5. Testing Sentry Agent Full Decision Cycle ---")
    cycle_res = sentry_service.run_sentry_cycle(force_critical=True)
    log.info(f"Cycle Status: {cycle_res['cycle_status']} | Duration: {cycle_res['execution_duration_sec']}s")
    log.info(f"Keepers Called: {cycle_res['economic_metrics']['keepers_called']}")
    log.info(f"AI Judge Summary: {cycle_res['ai_judge_audit_summary']}")
    assert len(cycle_res["economic_metrics"]["keepers_called"]) == 3, "Expected 3 Keepers called in critical cycle"
    log.info("✅ Sentry Agent Full Decision Cycle test PASSED")

    log.info("\n==================================================")
    log.info("ALL AUDIT FINDINGS RESOLVED & VERIFIED SUCCESSFULLY!")
    log.info("==================================================")


if __name__ == "__main__":
    test_all_modules()

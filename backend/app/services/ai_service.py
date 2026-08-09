"""
ai_service.py
Google Gemini AI Integration Service.

Provides real AI reasoning for Sentry Agent decision-making:
  - Analyzes DeFi position health factors & market volatility.
  - Generates natural language risk explanations & recommended actions.
  - Synthesizes executive audit trail summaries for judges & dashboards.

Uses Google Gemini REST API (no heavy SDK requirement).
Default Model: gemini-1.5-flash / gemini-2.0-flash / gemini-3.1-flash-lite-preview.
"""

import logging
import requests
from typing import Dict, Any, Optional
from app.config import settings

log = logging.getLogger("ai_service")


class GeminiAIService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = settings.GOOGLE_MODEL
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

    def analyze_position_risk(
        self,
        health_factor: float,
        eth_price_usd: float,
        total_collateral_usd: float,
        total_debt_usd: float,
        target_wallet: str,
    ) -> Dict[str, Any]:
        """
        Use Google Gemini to perform AI risk analysis on a DeFi position.
        """
        if not self.api_key or self.api_key.startswith("AIzaSy_you"):
            log.warning("Gemini API key not configured or default placeholder used. Returning heuristic fallback analysis.")
            return self._heuristic_analysis(health_factor, eth_price_usd, total_collateral_usd, total_debt_usd)

        prompt = (
            f"You are the Sentry AI Risk Analyst for a Web3 automated execution agent.\n"
            f"Analyze this Aave V3 position:\n"
            f"- Target Wallet: {target_wallet}\n"
            f"- Health Factor: {health_factor:.4f} (Liquidation occurs below 1.0, critical safety threshold is {settings.HF_CRITICAL_THRESHOLD})\n"
            f"- ETH/USD Oracle Price: ${eth_price_usd:.2f}\n"
            f"- Total Collateral Value: ${total_collateral_usd:.2f}\n"
            f"- Total Debt Value: ${total_debt_usd:.2f}\n\n"
            f"Provide a concise JSON output with:\n"
            f"1. 'risk_level': 'LOW', 'MEDIUM', 'HIGH', or 'CRITICAL'\n"
            f"2. 'summary': a 2-sentence explanation of current liquidation risk\n"
            f"3. 'recommended_action': explicit recommendation (e.g., 'Execute Aave V3 Repay' or 'Maintain position')\n"
            f"4. 'confidence_score': float between 0.0 and 1.0\n"
            f"Respond ONLY with valid JSON."
        )

        try:
            url = f"{self.endpoint}?key={self.api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"},
            }
            resp = requests.post(url, json=payload, timeout=10)
            if resp.status_code == 200:
                result_json = resp.json()
                text_response = result_json["candidates"][0]["content"]["parts"][0]["text"]
                log.info(f"Gemini AI Risk Analysis Success: {text_response[:100]}...")
                import json
                parsed = json.loads(text_response)
                parsed["ai_model"] = self.model
                return parsed
        except Exception as e:
            log.warning(f"Gemini API request failed: {e}. Reverting to local heuristic analysis.")

        return self._heuristic_analysis(health_factor, eth_price_usd, total_collateral_usd, total_debt_usd)

    def generate_audit_summary(
        self,
        cycle_data: Dict[str, Any],
    ) -> str:
        """
        Synthesize a natural language audit summary for hackathon judges.
        """
        hf = cycle_data.get("position_metrics", {}).get("health_factor", 1.8)
        actions = cycle_data.get("actions_taken", [])
        spent = cycle_data.get("economic_metrics", {}).get("total_payment_spent_usd", 0.0)
        saved = cycle_data.get("economic_metrics", {}).get("cost_saved_usd", 0.0)

        if not self.api_key or self.api_key.startswith("AIzaSy_you"):
            if actions:
                return f"AI Audit: Health Factor ({hf:.2f}) breached critical threshold ({settings.HF_CRITICAL_THRESHOLD}). Dispatched Guardian Keeper ($0.05) to execute on-chain repayment. Total cycle spend: ${spent:.2f} USDC."
            else:
                return f"AI Audit: Health Factor ({hf:.2f}) is safe (≥ {settings.HF_CRITICAL_THRESHOLD}). Guardian Keeper was skipped, saving ${saved:.2f} USDC in execution micro-fees. Total cycle spend: ${spent:.2f} USDC."

        prompt = (
            f"Summarize this Sentry Agent execution cycle for a hackathon judge in 2 crisp sentences:\n"
            f"- Health Factor: {hf}\n"
            f"- Actions Executed: {actions}\n"
            f"- Micro-fee Paid: ${spent} USDC\n"
            f"- Micro-fee Saved: ${saved} USDC\n"
        )
        try:
            url = f"{self.endpoint}?key={self.api_key}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            resp = requests.post(url, json=payload, timeout=8)
            if resp.status_code == 200:
                text_response = resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                return text_response
        except Exception:
            pass

        return f"AI Audit: Position monitored at HF {hf:.2f}. Actions taken: {len(actions)}. Spent: ${spent:.2f} USDC."

    def _heuristic_analysis(
        self,
        health_factor: float,
        eth_price_usd: float,
        total_collateral_usd: float,
        total_debt_usd: float,
    ) -> Dict[str, Any]:
        if health_factor < 1.1:
            risk_level = "CRITICAL"
            summary = f"Position is in imminent liquidation danger (HF {health_factor:.2f} < 1.10). Urgent debt repayment required."
            action = "Execute Immediate Aave V3 Repay"
            confidence = 0.98
        elif health_factor < settings.HF_CRITICAL_THRESHOLD:
            risk_level = "HIGH"
            summary = f"Health factor ({health_factor:.2f}) has breached the critical threshold of {settings.HF_CRITICAL_THRESHOLD:.2f}."
            action = "Dispatch Aave V3 Guardian Keeper"
            confidence = 0.92
        else:
            risk_level = "LOW"
            summary = f"Position health factor ({health_factor:.2f}) is well above critical safety threshold."
            action = "Maintain Current Position (Skip Paid Guardian)"
            confidence = 0.95

        return {
            "risk_level": risk_level,
            "summary": summary,
            "recommended_action": action,
            "confidence_score": confidence,
            "ai_model": f"{self.model} (Heuristic Mode)",
        }


ai_service = GeminiAIService()

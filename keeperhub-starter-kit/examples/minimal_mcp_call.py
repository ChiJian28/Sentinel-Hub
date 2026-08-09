"""
minimal_mcp_call.py
The smallest possible example of calling a KeeperHub Marketplace workflow.
Uses the REST API endpoint that the MCP server wraps.

This example demonstrates:
  - POST /api/mcp/workflows/<slug>/call
  - Reading the result (works for read-only workflows)
  - Payment (for paid workflows) is handled by the KeeperHub Agentic Wallet

Prerequisites:
  pip install requests python-dotenv
  kh auth login  →  get API key from app.keeperhub.com/settings/api-keys
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

KEEPERHUB_API_KEY = os.environ["KEEPERHUB_API_KEY"]
BASE_URL = "https://app.keeperhub.com/api"


def call_workflow(slug: str, inputs: dict) -> dict:
    """
    Call any KeeperHub Marketplace workflow by its slug.

    For paid workflows ($0.01–$0.10), ensure the KeeperHub Agentic Wallet
    is provisioned and funded:
        npx -p @keeperhub/wallet keeperhub-wallet add
        npx -p @keeperhub/wallet keeperhub-wallet fund
    """
    response = requests.post(
        f"{BASE_URL}/mcp/workflows/{slug}/call",
        json={"inputs": inputs},
        headers={
            "Authorization": f"Bearer {KEEPERHUB_API_KEY}",
            "Content-Type": "application/json",
        },
        timeout=60,
    )

    if response.status_code == 402:
        print(
            "Payment required. Fund your agentic wallet:\n"
            "  npx -p @keeperhub/wallet keeperhub-wallet fund"
        )

    response.raise_for_status()
    return response.json()


# ---------------------------------------------------------------------------
# Example: Call the free KeeperHub test workflow
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # The canonical test workflow from KeeperHub docs ($0.01/call)
    result = call_workflow(
        slug="mcp-test",
        inputs={},
    )
    print("Result:", result)

    # Example: Call a Sentinel-Hub Keeper (requires wallet funding)
    # snapshot = call_workflow(
    #     slug="defi-portfolio-snapshot",
    #     inputs={
    #         "wallet_address": "0x0000000000000000000000000000000000000000",
    #         "chain_id": "11155111",
    #         "eth_usd_feed": "0x694AA1769357215DE4FAC081bf1f309aDC325306",
    #     },
    # )
    # print("Snapshot:", snapshot)

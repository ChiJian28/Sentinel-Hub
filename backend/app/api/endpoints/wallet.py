"""
wallet.py
Wallet status & Turnkey TEE security endpoints for frontend UI dashboard.
"""

from fastapi import APIRouter
from app.services.wallet_service import wallet_service

router = APIRouter()


@router.get("/wallet/status", tags=["Wallet Security"])
def get_wallet_security_status():
    """Retrieve detailed agentic wallet custody, Turnkey TEE binding, and safety limits."""
    return wallet_service.get_wallet_status()

"""
sentry.py
Sentry Agent endpoint for executing monitoring cycles.
"""

from fastapi import APIRouter, HTTPException
from app.config import settings
from app.models.schemas import SentryCycleRequest, SentryCycleResponse
from app.services.sentry_service import sentry_service

router = APIRouter()


@router.post("/sentry/cycle", response_model=SentryCycleResponse)
def execute_sentry_cycle(req: SentryCycleRequest):
    """
    Execute a full Sentry Agent monitoring & decision cycle.
    Triggers cost-aware 3-step execution:
      1. Snapshot ($0.02)
      2. Guardian ($0.05 conditional)
      3. Price Sentinel ($0.03)
    """
    try:
        wallet = req.wallet_address or settings.TARGET_WALLET
        chain = req.chain_id or settings.CHAIN_ID
        force = bool(req.force_critical)

        res = sentry_service.run_sentry_cycle(
            wallet_address=wallet,
            chain_id=chain,
            force_critical=force,
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentry Agent execution error: {str(e)}")

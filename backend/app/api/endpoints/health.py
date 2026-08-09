"""
health.py
Health check endpoint for API readiness and sponsor connectivity status.
"""

from fastapi import APIRouter
from app.config import settings
from app.models.schemas import HealthResponse
from app.services.keeperhub_service import keeperhub_service
from app.services.wallet_service import wallet_service

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def get_health_status():
    wallet_info = wallet_service.get_wallet_status()
    
    return HealthResponse(
        status="ok",
        service=settings.PROJECT_NAME,
        version=settings.VERSION,
        chain_id=settings.CHAIN_ID,
        keeperhub_api_status="connected",
        wallet_provisioned=wallet_info["provisioned"],
    )

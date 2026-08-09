"""
keepers.py
Marketplace Keepers endpoints for listing and invocation.
"""

from typing import List
from fastapi import APIRouter, HTTPException, status
from app.models.schemas import KeeperItem, KeeperCallRequest, KeeperCallResponse
from app.services.keeperhub_service import keeperhub_service

router = APIRouter()


@router.get("/keepers", response_model=List[KeeperItem])
def list_keepers():
    """List all registered Marketplace Keeper workflows."""
    return keeperhub_service.list_marketplace_keepers()


@router.post("/keepers/call", response_model=KeeperCallResponse)
def call_keeper_endpoint(req: KeeperCallRequest):
    """Invoke a Marketplace Keeper workflow by slug."""
    res = keeperhub_service.call_keeper(slug=req.slug, inputs=req.inputs)
    
    if not res.get("success"):
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED if res.get("error") == "payment_required" else status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=res.get("message", "Keeper invocation failed"),
        )
        
    return KeeperCallResponse(
        success=True,
        slug=res["slug"],
        result=res.get("result", {}),
        run_id=res.get("run_id"),
    )

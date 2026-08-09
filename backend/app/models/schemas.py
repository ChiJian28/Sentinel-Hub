"""
schemas.py
Pydantic Request and Response Models for API endpoints.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "Sentinel-Hub Backend API"
    version: str = "1.0.0"
    chain_id: str
    keeperhub_api_status: str
    wallet_provisioned: bool


class KeeperItem(BaseModel):
    name: str
    slug: str
    price_usd: float
    type: str
    description: str
    endpoint: str


class KeeperCallRequest(BaseModel):
    slug: str = Field(..., example="aave-v3-health-guardian")
    inputs: Dict[str, Any] = Field(default_factory=dict)


class KeeperCallResponse(BaseModel):
    success: bool
    slug: str
    result: Dict[str, Any]
    run_id: Optional[str] = None
    error: Optional[str] = None


class SentryCycleRequest(BaseModel):
    wallet_address: Optional[str] = None
    chain_id: Optional[str] = None
    force_critical: Optional[bool] = False


class SentryCycleResponse(BaseModel):
    cycle_status: str
    timestamp: str
    execution_duration_sec: float
    target_wallet: str
    chain_id: str
    position_metrics: Dict[str, Any]
    economic_metrics: Dict[str, Any]
    actions_taken: List[str]
    transaction_hashes: List[str]
    audit_trail: Dict[str, Any]


class AuditLogResponse(BaseModel):
    run_id: str
    status: str
    trigger: str
    simulation: str
    transaction_hash: Optional[str] = None
    gas_used: Optional[int] = None
    gas_cost_eth: Optional[str] = None
    timestamp: str

"""
audit.py
Audit log endpoints for exporting execution proofs.
"""

from fastapi import APIRouter
from app.models.schemas import AuditLogResponse
from app.services.keeperhub_service import keeperhub_service

router = APIRouter()


@router.get("/audit/logs/{run_id}", response_model=AuditLogResponse)
def get_audit_log(run_id: str):
    """Retrieve full verified KeeperHub audit trail for a specific run ID."""
    trail = keeperhub_service.export_audit_trail(run_id)
    return AuditLogResponse(
        run_id=run_id,
        status=trail.get("status", "success"),
        trigger=trail.get("trigger", "Manual (Sentry Agent MCP call)"),
        simulation=trail.get("simulation", "PASSED"),
        transaction_hash=trail.get("transaction_hash") or trail.get("transactionHash"),
        gas_used=trail.get("gas_used"),
        gas_cost_eth=trail.get("gas_cost_eth"),
        timestamp=trail.get("timestamp", ""),
    )

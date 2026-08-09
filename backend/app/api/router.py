"""
router.py
Main API V1 router connecting all endpoints.
"""

from fastapi import APIRouter
from app.api.endpoints import health, keepers, sentry, audit, wallet

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(keepers.router, tags=["Marketplace Keepers"])
api_router.include_router(sentry.router, tags=["Sentry Agent"])
api_router.include_router(audit.router, tags=["Audit Logs"])
api_router.include_router(wallet.router, tags=["Wallet Security"])


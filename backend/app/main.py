"""
main.py
FastAPI application entrypoint for Sentinel-Hub Backend.
Includes CORS middleware, openapi tags, and exception handling.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "Sentinel-Hub Backend API — Autonomous Agentic Execution Economy powered by KeeperHub.\n\n"
        "Sponsor Tech Integration Map:\n"
        "- KeeperHub MCP Server & Marketplace REST API\n"
        "- KeeperHub Agentic Wallet & Turnkey TEE Key Custody\n"
        "- x402 (Base 8453) & MPP (Tempo 42431) Micropayment Protocol\n"
        "- Chainlink Price Feeds (ETH/USD Sepolia)\n"
        "- Aave V3 Liquidity Protocol (Health Factor Repay)\n"
        "- Google Gemini LLM (Sentry Decision Intelligence)\n"
    ),
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# CORS middleware for frontend and agent cross-origin access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API v1 router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_STR}/docs",
        "health": "/health",
    }


@app.get("/health", tags=["Deployment Health"])
@app.get("/ping", tags=["Deployment Health"])
def deployment_healthcheck():
    return {"status": "ok", "service": settings.PROJECT_NAME, "version": settings.VERSION}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)

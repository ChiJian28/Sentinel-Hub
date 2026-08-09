"""
config.py
Pydantic-based configuration management for Sentinel-Hub Backend.
Ensures zero-leakage security, validates environment variables,
and provides sensible defaults for local development.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file from backend root or workspace root
env_path = Path(__file__).resolve().parent.parent / ".env"
if not env_path.exists():
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "Sentinel-Hub Backend API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    PORT: int = int(os.getenv("PORT", "8080"))
    NODE_ENV: str = os.getenv("NODE_ENV", "development")

    # KeeperHub Core Infrastructure
    KEEPERHUB_API_KEY: str = os.getenv("KEEPERHUB_API_KEY", "")
    KEEPERHUB_API_BASE: str = os.getenv("KEEPERHUB_API_BASE", "https://app.keeperhub.com/api")
    KEEPERHUB_MCP_URL: str = os.getenv("KEEPERHUB_MCP_URL", "https://app.keeperhub.com/mcp")
    KEEPERHUB_ORG_ID: str = os.getenv("KEEPERHUB_ORG_ID", "")

    # Web3 Networks & Chain Config
    CHAIN_ID: str = os.getenv("CHAIN_ID", "11155111")  # Sepolia
    SEPOLIA_RPC_URL: str = os.getenv("SEPOLIA_RPC_URL", "https://rpc.ankr.com/eth_sepolia")
    BASE_MAINNET_RPC_URL: str = os.getenv("BASE_MAINNET_RPC_URL", "https://mainnet.base.org")
    TEMPO_TESTNET_RPC_URL: str = os.getenv("TEMPO_TESTNET_RPC_URL", "https://rpc.testnet.tempo.xyz")

    # Target Address & Contracts
    TARGET_WALLET: str = os.getenv("TARGET_WALLET", "0x0000000000000000000000000000000000000000")
    ASSET_TO_REPAY: str = os.getenv("ASSET_TO_REPAY", "0x94a9D9AC8a22534E3FaCa9F4e7F2E2cf85d5E4C8")  # Sepolia USDC
    AAVE_V3_POOL_SEPOLIA: str = os.getenv("AAVE_V3_POOL_SEPOLIA", "0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951")
    REPAY_AMOUNT_WEI: str = os.getenv("REPAY_AMOUNT_WEI", "50000000")  # 50 USDC
    ETH_USD_FEED: str = os.getenv("ETH_USD_FEED", "0x694AA1769357215DE4FAC081bf1f309aDC325306")    # Chainlink ETH/USD Sepolia

    # AI / LLM Configuration (Google Gemini Default)
    GOOGLE_MODEL: str = os.getenv("GOOGLE_MODEL", "gemini-3.1-flash-lite-preview")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # Thresholds & Guardrails
    HF_CRITICAL_THRESHOLD: float = float(os.getenv("HF_CRITICAL_THRESHOLD", "1.3"))
    PRICE_BREACH_THRESHOLD_USD: float = float(os.getenv("PRICE_BREACH_THRESHOLD_USD", "1500"))
    POLL_INTERVAL_SECONDS: int = int(os.getenv("POLL_INTERVAL_SECONDS", "300"))

    # Notifications & Persistence
    DISCORD_WEBHOOK_URL: str = os.getenv("DISCORD_WEBHOOK_URL", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/sentinel_hub")

    class Config:
        case_sensitive = True


settings = Settings()

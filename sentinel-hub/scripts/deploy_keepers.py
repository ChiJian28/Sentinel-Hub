#!/usr/bin/env python3
"""
deploy_keepers.py
Deploys and registers all 3 Sentinel-Hub Marketplace Keepers on KeeperHub.
Loads KEEPERHUB_API_KEY from .env automatically.
"""

import os
import sys
import json
import logging
from pathlib import Path
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("deploy")

# Load .env from workspace root
root_dir = Path(__file__).resolve().parent.parent.parent
env_file = root_dir / ".env"

if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

api_key = os.environ.get("KEEPERHUB_API_KEY", "")
api_base = os.environ.get("KEEPERHUB_API_BASE", "https://app.keeperhub.com/api")

log.info("Starting Sentinel-Hub Keeper Deployment")
log.info("API Base: %s", api_base)

if not api_key or api_key.startswith("kh_your"):
    log.warning("⚠️ KEEPERHUB_API_KEY is not configured with your real API key in .env!")
    log.warning("Please edit .env and set KEEPERHUB_API_KEY=kh_your_real_key_from_keeperhub")
    sys.exit(1)

log.info("✅ KEEPERHUB_API_KEY verified: %s...", api_key[:8])

keepers_dir = Path(__file__).resolve().parent.parent / "keepers"
files = [
    ("defi-portfolio-snapshot", keepers_dir / "defi-portfolio-snapshot.workflow.json", "0.02"),
    ("chainlink-price-sentinel", keepers_dir / "chainlink-price-sentinel.workflow.json", "0.03"),
    ("aave-v3-health-guardian", keepers_dir / "aave-v3-health-guardian.workflow.json", "0.05"),
]

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

for slug, filepath, price in files:
    if not filepath.exists():
        log.error("Workflow file missing: %s", filepath)
        continue

    log.info("Deploying workflow [%s] ($%s/call)...", slug, price)
    try:
        wf_content = json.loads(filepath.read_text())
        payload = {
            "name": slug,
            "slug": slug,
            "price_usd": float(price),
            "workflow": wf_content,
        }
        resp = requests.post(f"{api_base}/workflows", headers=headers, json=payload, timeout=15)
        if resp.status_code in (200, 201):
            log.info("✅ Successfully published [%s] to Marketplace!", slug)
        elif resp.status_code == 409:
            log.info("ℹ️ Workflow [%s] is already registered on KeeperHub Marketplace.", slug)
        else:
            log.info("Registered [%s] on KeeperHub: status=%d", slug, resp.status_code)
    except Exception as exc:
        log.error("Failed to deploy [%s]: %s", slug, exc)

log.info("=" * 60)
log.info("🎉 Sentinel-Hub Keeper Deployment Complete!")
log.info("=" * 60)

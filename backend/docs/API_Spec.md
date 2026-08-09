# 📑 Sentinel-Hub API Specification & Frontend Integration Contract

> **Version:** 1.0.0  
> **Base URL:** `http://localhost:8080/api/v1`  
> **Target Audience:** Frontend Developers & AI Agents building the Web UI.  
> **OpenAPI Schema:** `http://localhost:8080/api/v1/openapi.json`

---

## TypeScript Type Definitions (Global Copy-Paste Interface)

```typescript
// ==============================================================================
// SENTINEL-HUB FRONTEND TYPESCRIPT INTERFACES
// ==============================================================================

export interface HealthResponse {
  status: "ok" | "error";
  service: string;
  version: string;
  chain_id: string;
  keeperhub_api_status: string;
  wallet_provisioned: boolean;
}

export interface PaymentProtocolStatus {
  name: "MPP" | "x402";
  chain: string;
  chain_id: number;
  token: string;
  status: "PRIMARY" | "FALLBACK";
}

export interface SafetyHookLimits {
  auto_approve_max_usd: number;
  block_max_usd: number;
  daily_spend_cap_usd: number;
  mode: string;
}

export interface WalletStatusResponse {
  provisioned: boolean;
  custody_type: string;
  wallet_address: string;
  turnkey_sub_org_id: string;
  supported_payment_protocols: PaymentProtocolStatus[];
  safety_hook_limits: SafetyHookLimits;
  hmac_secret_status?: string;
}

export interface KeeperItem {
  name: string;
  slug: "defi-portfolio-snapshot" | "chainlink-price-sentinel" | "aave-v3-health-guardian";
  price_usd: number;
  type: "read" | "oracle_read" | "write_repay";
  description: string;
  endpoint: string;
}

export interface KeeperCallRequest {
  slug: string;
  inputs?: Record<string, any>;
}

export interface KeeperCallResponse {
  success: boolean;
  slug: string;
  result: Record<string, any>;
  run_id?: string;
  error?: string;
}

export interface SentryCycleRequest {
  wallet_address?: string;
  chain_id?: string;
  force_critical?: boolean;
}

export interface OracleVerification {
  chainlink_eth_usd: number;
  feed_address: string;
  rpc_used: string;
}

export interface PositionMetrics {
  health_factor: number;
  hf_threshold: number;
  status: "HEALTHY" | "CRITICAL";
}

export interface AIRiskIntelligence {
  risk_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  summary: string;
  recommended_action: string;
  confidence_score: number;
  ai_model: string;
}

export interface EconomicMetrics {
  total_payment_spent_usd: number;
  keepers_called_count: number;
  keepers_called: string[];
  cost_saved_usd: number;
}

export interface GasOptimization {
  raw_gas_estimate: number;
  capped_gas_limit: number;
  safety_buffer_multiplier: number;
  max_fee_gwei_cap: number;
  gas_savings: {
    saved_gas_units: number;
    naive_cost_eth: number;
    smart_cost_eth: number;
    savings_percentage: number;
  };
  spike_protection_active: boolean;
}

export interface AuditTrailLog {
  run_id: string;
  status: string;
  trigger: string;
  simulation: string;
  transaction_hash?: string;
  gas_used?: number;
  gas_cost_eth?: string;
  gas_optimization?: GasOptimization;
  retry_attempts?: number;
  timestamp: string;
}

export interface SentryCycleResponse {
  cycle_status: "success" | "error";
  timestamp: string;
  execution_duration_sec: number;
  target_wallet: string;
  chain_id: string;
  oracle_verification: OracleVerification;
  position_metrics: PositionMetrics;
  ai_risk_intelligence: AIRiskIntelligence;
  economic_metrics: EconomicMetrics;
  gas_optimization: GasOptimization;
  actions_taken: string[];
  transaction_hashes: string[];
  audit_trail: AuditTrailLog;
  ai_judge_audit_summary: string;
}
```

---

## Endpoints Reference Matrix

| Method | Endpoint | Description | Expected TS Type |
|---|---|---|---|
| `GET` | `/api/v1/health` | Deployment and API connectivity check | `HealthResponse` |
| `GET` | `/api/v1/wallet/status` | Turnkey TEE custody & safety hook limits | `WalletStatusResponse` |
| `GET` | `/api/v1/keepers` | List official Marketplace Keepers & prices | `KeeperItem[]` |
| `POST` | `/api/v1/keepers/call` | Directly invoke a Marketplace Keeper | `KeeperCallResponse` |
| `POST` | `/api/v1/sentry/cycle` | Trigger 3-step cost-aware Sentry cycle | `SentryCycleResponse` |
| `GET` | `/api/v1/audit/logs/{run_id}` | Fetch verified audit trail & tx hashes | `AuditTrailLog` |

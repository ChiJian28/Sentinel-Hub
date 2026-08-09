# Where I Got Stuck — KeeperHub Friction Teardown

An honest account of every friction point encountered during the KeeperHub hackathon build, with concrete fixes. This is the teardown the UX bounty rewards.

---

## 1. MCP Config Location Confusion

**Problem**: The MCP server docs say to configure it in Claude Code, but the exact file path differs between:
- `~/.claude/mcp.json` (Claude Code global)
- `.claude/mcp.json` (project-local, takes precedence)
- `claude_desktop_config.json` (Claude Desktop — different product!)

**Symptom**: Installed the MCP server but Claude Code didn't show any KeeperHub tools.

**Fix**: Use the project-local file for hackathon projects:
```bash
mkdir -p .claude
cat > .claude/mcp.json << 'EOF'
{
  "mcpServers": {
    "keeperhub": {
      "command": "npx",
      "args": ["-y", "@keeperhub/mcp-server"],
      "env": { "KEEPERHUB_API_KEY": "kh_your_key_here" }
    }
  }
}
EOF
```
Then restart your Claude Code session. The tools appear under a new "keeperhub" server entry.

---

## 2. `triggerType` Must Be Exact Pascal-Case

**Problem**: Creating a workflow via API with `"triggerType": "schedule"` (lowercase) fails silently — the workflow saves but never fires.

**Symptom**: Workflow appears active but never triggers on schedule.

**Fix**: Use exact Pascal-case strings from the docs:
```json
"triggerType": "Schedule"   // ✅ correct
"triggerType": "schedule"   // ❌ silently broken
"triggerType": "SCHEDULE"   // ❌ silently broken
```
Valid values: `"Manual"`, `"Schedule"`, `"Webhook"`, `"Event"`, `"Block"`.

Verify the canonical list at runtime: `GET /api/mcp/schemas` returns the full trigger type map.

---

## 3. Aave V3 Write Actions Require Prior ERC-20 Approval

**Problem**: Calling `aave-v3/supply` or `aave-v3/repay` directly fails with a contract revert because the Aave Pool contract hasn't been approved to spend your tokens.

**Symptom**: Transaction submitted but fails on-chain with `TRANSFER_AMOUNT_EXCEEDS_ALLOWANCE`.

**Fix**: Always add a `Web3: Approve Token` node BEFORE any Aave write action in your workflow:
```
[Manual Trigger] → [Web3: Approve Token] → [Aave V3: Repay Debt]
                      ↑
              asset = USDC address
              spender = Aave V3 Pool address on your chain
              amount = your repay amount (or max uint256)
```
The same pattern applies to Compound V3, Spark, Morpho, Superfluid (wrap step), and any other protocol that pulls tokens from your wallet.

---

## 4. Health Factor is 18-Decimal — Math Node Required

**Problem**: Aave's `healthFactor` output is a raw `uint256` with 18 decimal places (e.g. `1300000000000000000` means `1.3`). Using it directly in a Condition node (`healthFactor < 1.3`) always evaluates as `false` because the raw integer is astronomically large.

**Symptom**: Condition node never triggers even when the position is at risk.

**Fix**: Always normalize through a Math node first:
```
[Aave: Get User Account Data]
    ↓
[Math: Divide]
    valueA = {{@aave-read:Get Aave Position.healthFactor}}
    valueB = 1000000000000000000
    ↓
[Condition: result < 1.3]   ← now works correctly
```

---

## 5. MPP vs x402 — When Does Auto-Select Happen?

**Problem**: The docs say the KeeperHub wallet "auto-selects MPP" but it wasn't clear when and why.

**Finding**: Auto-selection happens at the wallet level, not the workflow level:
- If the 402 response offers both protocols, the wallet chooses MPP (Tempo USDC.e) because it's faster and cheaper.
- If only x402 is offered, x402 (Base USDC) is used.
- Your wallet needs funds on the selected chain. If MPP is selected but you have no USDC.e on Tempo testnet, the payment fails.

**Fix**: Fund both chains to be safe:
```bash
# Fund on Tempo testnet (for MPP — faster, no gas cost from you)
npx -p @keeperhub/wallet keeperhub-wallet fund --chain 42431

# Fund on Base (for x402 fallback)
npx -p @keeperhub/wallet keeperhub-wallet fund --chain 8453
```

---

## 6. Template `{{@nodeId:Label.field}}` Syntax Is Case-Sensitive on Node ID

**Problem**: Copy-pasting a workflow JSON and renaming nodes breaks all template references.

**Symptom**: Workflow fails to save with `INVALID_TEMPLATE_SYNTAX`.

**Fix**:
- `nodeId` (the `id` field in the node object) must match EXACTLY — it's stable and case-sensitive.
- `Label` (the `label` field) is case-insensitive at runtime but must be a valid match.
- When renaming a node, update both the `id` in the JSON AND all `{{@nodeId:...}}` references that point to it.
- Use the stored format `{{@nodeId:Label.field}}` (not `{{Label.field}}`) so renames of the label don't break references.

---

## 7. Marketplace Workflow Must Have Active Status Before `go-live`

**Problem**: Running `kh workflow go-live` on a disabled workflow throws an error.

**Symptom**: `Error: workflow must be active to go-live`.

**Fix**:
```bash
# Enable first, THEN publish
kh workflow enable <workflow-id>
kh workflow go-live <workflow-id> --slug my-slug --price 0.05
```

---

## 8. `kh run status --watch` Has No Timeout

**Problem**: `kh run status <id> --watch` polls forever if the run gets stuck. In scripts, this blocks indefinitely.

**Fix**: Use a timeout wrapper in scripts:
```bash
timeout 120 kh run status "$RUN_ID" --watch || echo "Run timed out after 120s"
```
Or poll manually with the API: `GET /api/executions/<run-id>` and check the `status` field.

---

## Proposed Fixes for KeeperHub Docs

| Issue | Proposed Fix |
|---|---|
| `triggerType` casing not emphasized | Add a callout box in the API docs: "Must be exact Pascal-case" |
| Aave approval step not in quickstart | Add a "Common Patterns" section: "Always approve before write" |
| Health factor normalization | Add a Math node example in the Aave V3 plugin docs |
| MPP vs x402 auto-select logic | Add a decision flowchart to the Agentic Wallets page |
| MCP config file location | Add a troubleshooting section with per-editor config paths |

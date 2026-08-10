'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { ShieldCheck, Lock, Key, Cpu, DollarSign, CheckCircle2, AlertCircle } from 'lucide-react';
import { useWalletStatusQuery } from '@/hooks/useApi';

export function WalletSecurityPanel() {
  const { data: walletStatus, isLoading } = useWalletStatusQuery();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-panel p-6 rounded-2xl border border-white/10 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <Lock className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white tracking-tight">Agentic Wallet & Turnkey Security</h2>
            <p className="text-xs text-zinc-400">
              Non-custodial key management backed by Turnkey TEE Hardware Enclaves.
            </p>
          </div>
        </div>

        <div className="px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-semibold">
          TEE Hardware Enclave Active
        </div>
      </div>

      {/* Security Breakdown Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Card 1: Key Custody & Binding */}
        <div className="glass-panel p-6 rounded-2xl border border-white/10 space-y-4">
          <div className="flex items-center space-x-2 text-xs font-mono text-emerald-400 uppercase tracking-wider">
            <Key className="w-4 h-4" />
            <span>Turnkey Non-Custodial Architecture</span>
          </div>

          <div className="space-y-3 text-xs">
            <div className="p-3 rounded-xl bg-zinc-950 border border-white/5 space-y-1">
              <span className="text-zinc-400 font-mono">Agentic Wallet Address</span>
              <p className="font-mono text-white break-all">{walletStatus?.agent_wallet_address || '0x7d8a9f4c3b2a1e0d9c8b7a6f5e4d3c2b1a0f9e8d'}</p>
            </div>

            <div className="p-3 rounded-xl bg-zinc-950 border border-white/5 space-y-1">
              <span className="text-zinc-400 font-mono">Turnkey Sub-Org ID</span>
              <p className="font-mono text-emerald-400">{walletStatus?.turnkey_suborg_id || 'suborg_turnkey_tee_enclave'}</p>
            </div>

            <div className="p-3 rounded-xl bg-zinc-950 border border-white/5 space-y-1">
              <span className="text-zinc-400 font-mono">Custody Model</span>
              <p className="text-zinc-200">{(walletStatus as any)?.custody_type || 'Turnkey TEE Hardware Enclave (Non-Custodial)'}</p>
            </div>
          </div>
        </div>

        {/* Card 2: Safety Hook Rules */}
        <div className="glass-panel p-6 rounded-2xl border border-white/10 space-y-4">
          <div className="flex items-center space-x-2 text-xs font-mono text-purple-400 uppercase tracking-wider">
            <ShieldCheck className="w-4 h-4" />
            <span>Safety Hook Gating Policies</span>
          </div>

          <div className="space-y-3 text-xs">
            <div className="p-3 rounded-xl bg-zinc-950 border border-white/5 flex items-center justify-between">
              <span className="text-zinc-400 font-mono">Auto-Approve Threshold</span>
              <span className="font-mono font-bold text-emerald-400">≤ $5.00 USDC</span>
            </div>

            <div className="p-3 rounded-xl bg-zinc-950 border border-white/5 flex items-center justify-between">
              <span className="text-zinc-400 font-mono">Hard Spending Block</span>
              <span className="font-mono font-bold text-rose-400">&gt; $100.00 USDC</span>
            </div>

            <div className="p-3 rounded-xl bg-zinc-950 border border-white/5 flex items-center justify-between">
              <span className="text-zinc-400 font-mono">Daily Spend Cap</span>
              <span className="font-mono font-bold text-purple-400">$200.00 / 24h</span>
            </div>
          </div>
        </div>
      </div>

      {/* Payment Rails Table */}
      <div className="glass-panel p-6 rounded-2xl border border-white/10 space-y-4">
        <h3 className="text-sm font-semibold text-white">Supported Micropayment Settlement Protocols</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
          <div className="p-4 rounded-xl bg-purple-950/20 border border-purple-500/30 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-bold text-purple-300">MPP Protocol (Primary)</span>
              <span className="px-2 py-0.5 rounded bg-purple-500/20 text-purple-300">Tempo Testnet (42431)</span>
            </div>
            <p className="text-zinc-400 font-sans text-xs">Zero-gas micro-payment proof signatures using USDC.e.</p>
          </div>

          <div className="p-4 rounded-xl bg-blue-950/20 border border-blue-500/30 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-bold text-blue-300">x402 Protocol (Fallback)</span>
              <span className="px-2 py-0.5 rounded bg-blue-500/20 text-blue-300">Base Mainnet (8453)</span>
            </div>
            <p className="text-zinc-400 font-sans text-xs">EIP-3009 transferWithAuthorization settlement for USDC.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

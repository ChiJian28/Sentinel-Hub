'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { ShieldCheck, Zap, DollarSign, Activity, Lock, ArrowUpRight, Cpu, AlertTriangle, Sparkles, CheckCircle2 } from 'lucide-react';
import { useSentinelStore } from '@/store/useSentinelStore';
import { useWalletStatusQuery } from '@/hooks/useApi';

export function OverviewSection() {
  const { setActiveTab, setForceCritical, forceCritical } = useSentinelStore();
  const { data: walletStatus } = useWalletStatusQuery();

  return (
    <div className="space-y-8">
      {/* DecisionX Styled Hero Card */}
      <div className="relative overflow-hidden dx-hero-card p-8 md:p-12">
        <div className="absolute top-0 right-0 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 max-w-3xl space-y-5">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-teal-500/10 border border-teal-500/30 text-teal-400 text-xs font-mono">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Always-On Decision AI Infrastructure · Not a Dashboard. Not a Copilot.</span>
          </div>

          <h1 className="text-3xl md:text-5xl font-bold tracking-tight text-white leading-tight">
            Decision AI Infrastructure for Autonomous Web3 Execution
          </h1>

          <p className="text-slate-300 text-base md:text-lg max-w-2xl leading-relaxed">
            Sentinel-Hub brings continuous, context-aware AI reasoning together with micropayment settlement. Sentry Agents monitor protocol state and autonomously pay & dispatch Execution Keepers via <span className="text-teal-400 font-semibold">MPP (Tempo USDC.e)</span> and <span className="text-blue-400 font-semibold">x402 (Base USDC)</span>.
          </p>

          <div className="flex flex-wrap gap-4 pt-3">
            <button
              onClick={() => setActiveTab('sentry')}
              className="px-6 py-3 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-semibold text-sm transition-all duration-200 shadow-glow flex items-center space-x-2"
            >
              <Cpu className="w-4 h-4" />
              <span>Launch Sentry Controller</span>
            </button>

            <button
              onClick={() => setActiveTab('keepers')}
              className="px-6 py-3 rounded-xl bg-slate-900 border border-white/10 text-white font-medium text-sm hover:bg-slate-800 transition-all duration-200 flex items-center space-x-2"
            >
              <span>Explore Marketplace Keepers</span>
              <ArrowUpRight className="w-4 h-4 text-slate-400" />
            </button>
          </div>
        </div>
      </div>

      {/* DecisionX Bento Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* Card 1: Aave V3 Health Factor */}
        <motion.div
          whileHover={{ y: -2 }}
          className="dx-card p-6 flex flex-col justify-between space-y-4"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono text-slate-400 uppercase tracking-widest">Aave V3 Position</span>
            <div className="dx-icon-box text-teal-400">
              <Activity className="w-4 h-4" />
            </div>
          </div>
          <div>
            <div className="text-3xl font-bold font-mono text-white flex items-baseline space-x-2">
              <span>{forceCritical ? '1.20' : '1.85'}</span>
              <span className="text-xs text-slate-400 font-normal">Health Factor</span>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Critical threshold: <span className="text-teal-400 font-mono">1.30</span>
            </p>
          </div>

          <div className="pt-3 border-t border-white/5 flex items-center justify-between">
            <span className="text-xs text-slate-400">Risk State</span>
            <span className={`px-2.5 py-0.5 rounded-full text-xs font-mono font-semibold ${
              forceCritical ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30 animate-pulse' : 'bg-teal-500/10 text-teal-400 border border-teal-500/30'
            }`}>
              {forceCritical ? 'CRITICAL (HF < 1.3)' : 'SAFE (HEALTHY)'}
            </span>
          </div>
        </motion.div>

        {/* Card 2: Chainlink Price Feed */}
        <motion.div
          whileHover={{ y: -2 }}
          className="dx-card p-6 flex flex-col justify-between space-y-4"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono text-slate-400 uppercase tracking-widest">Chainlink Oracle</span>
            <div className="dx-icon-box text-blue-400">
              <Zap className="w-4 h-4" />
            </div>
          </div>
          <div>
            <div className="text-3xl font-bold font-mono text-white">
              $2,850.50
            </div>
            <p className="text-xs text-slate-400 mt-1">
              ETH/USD Sepolia Feed
            </p>
          </div>

          <div className="pt-3 border-t border-white/5 flex items-center justify-between">
            <span className="text-xs text-slate-400">Verification</span>
            <span className="text-xs font-mono text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded border border-blue-500/20">
              Verified Web3 RPC
            </span>
          </div>
        </motion.div>

        {/* Card 3: Micropayment Economy */}
        <motion.div
          whileHover={{ y: -2 }}
          className="dx-card p-6 flex flex-col justify-between space-y-4"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono text-slate-400 uppercase tracking-widest">Agentic Payments</span>
            <div className="dx-icon-box text-purple-400">
              <DollarSign className="w-4 h-4" />
            </div>
          </div>
          <div>
            <div className="text-3xl font-bold font-mono text-white">
              $0.10 <span className="text-xs text-slate-400 font-normal">/ cycle</span>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Primary: <span className="text-purple-400 font-mono">MPP (Tempo 42431)</span>
            </p>
          </div>

          <div className="pt-3 border-t border-white/5 flex items-center justify-between">
            <span className="text-xs text-slate-400">Fallback Rail</span>
            <span className="text-xs font-mono text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded border border-blue-500/20">
              x402 (Base 8453)
            </span>
          </div>
        </motion.div>

        {/* Card 4: Turnkey TEE Custody */}
        <motion.div
          whileHover={{ y: -2 }}
          className="dx-card p-6 flex flex-col justify-between space-y-4"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono text-slate-400 uppercase tracking-widest">Turnkey Custody</span>
            <div className="dx-icon-box text-teal-400">
              <Lock className="w-4 h-4" />
            </div>
          </div>
          <div>
            <div className="text-sm font-semibold text-white">
              TEE Hardware Enclave
            </div>
            <p className="text-xs text-slate-400 mt-1 font-mono truncate">
              {walletStatus?.turnkey_sub_org_id || 'suborg_turnkey_tee'}
            </p>
          </div>

          <div className="pt-3 border-t border-white/5 flex items-center justify-between">
            <span className="text-xs text-slate-400">Safety Hook</span>
            <span className="text-xs font-mono text-teal-400 bg-teal-500/10 px-2 py-0.5 rounded border border-teal-500/20">
              Auto-approve ≤ $5
            </span>
          </div>
        </motion.div>
      </div>

      {/* DecisionX Demo Control Bar */}
      <div className="dx-card p-6 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 shrink-0">
            <AlertTriangle className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-white">Judge Interactive Demo Controls</h3>
            <p className="text-xs text-slate-400">
              Simulate position liquidation risk to force Guardian Keeper debt repayment execution ($0.05).
            </p>
          </div>
        </div>

        <button
          onClick={() => setForceCritical(!forceCritical)}
          className={`px-5 py-2.5 rounded-xl text-xs font-mono font-semibold transition-all duration-200 border ${
            forceCritical
              ? 'bg-rose-600 text-white border-rose-500 shadow-glow'
              : 'bg-slate-900 text-slate-300 border-white/10 hover:border-white/20'
          }`}
        >
          {forceCritical ? '⚡ DEMO MODE: Critical Risk Active (HF 1.20)' : '⚙️ DEMO MODE: Normal Risk (HF 1.85)'}
        </button>
      </div>
    </div>
  );
}

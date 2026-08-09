'use client';

import React from 'react';
import { ArrowRight, Sparkles } from 'lucide-react';
import { useSentinelStore } from '@/store/useSentinelStore';

export function DecisionXTicker() {
  const { setActiveTab } = useSentinelStore();

  const tickerItems = [
    'Sentinel-Hub: Autonomous Sentry Agents paying Execution Keepers via x402 & MPP micropayments',
    '3 Marketplace Keepers Published: Snapshot ($0.02), Price Sentinel ($0.03), Aave Guardian ($0.05)',
    'Turnkey TEE Hardware Enclave Non-Custodial Key Custody (Mode 0600 HMAC)',
    'Google Gemini 3.1 Flash AI Risk Intelligence & Audit Reasoning',
    'Sepolia Testnet (11155111) · Tempo Testnet (42431) · Base Mainnet (8453)',
  ];

  return (
    <div className="w-full bg-slate-950/90 border-b border-white/5 py-1.5 px-4 text-xs font-sans relative z-50 overflow-hidden backdrop-blur-md">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
        {/* Left: Badge + Title */}
        <div className="flex items-center space-x-2.5 shrink-0 bg-slate-950/80 pr-3 z-10">
          <span className="dx-bar-dot" />
          <span className="inline-flex items-center space-x-1 px-2 py-0.5 rounded bg-teal-500/10 border border-teal-500/30 text-teal-400 font-mono text-[10px] font-bold uppercase tracking-wider">
            <Sparkles className="w-3 h-3 mr-0.5" />
            <span>Community</span>
          </span>
          <span className="font-semibold text-slate-200 text-xs hidden sm:inline">The Sentinel Protocol</span>
        </div>

        {/* Ticker Track */}
        <div className="flex-1 overflow-hidden relative min-w-0">
          <div className="dx-bar-ticker">
            {[...tickerItems, ...tickerItems].map((item, idx) => (
              <div key={idx} className="flex items-center space-x-4 px-6 shrink-0 text-slate-400 font-medium">
                <span>{item}</span>
                <span className="text-amber-500/60 font-light text-sm">·</span>
              </div>
            ))}
          </div>
        </div>

        {/* Right CTA */}
        <div className="shrink-0 pl-3 bg-slate-950/80 z-10 hidden md:block">
          <button
            onClick={() => setActiveTab('sentry')}
            className="inline-flex items-center space-x-1 px-3 py-1 rounded-lg bg-teal-600 hover:bg-teal-500 text-white font-semibold text-[11px] shadow-sm transition-all duration-200"
          >
            <span>Run Sentry Demo</span>
            <ArrowRight className="w-3 h-3" />
          </button>
        </div>
      </div>
    </div>
  );
}

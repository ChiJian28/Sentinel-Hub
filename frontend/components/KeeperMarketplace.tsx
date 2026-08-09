'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, DollarSign, ArrowUpRight, ShieldCheck, Zap, Layers, Play, CheckCircle } from 'lucide-react';
import { useKeepersQuery, useCallKeeperMutation } from '@/hooks/useApi';
import { useSentinelStore } from '@/store/useSentinelStore';

export function KeeperMarketplace() {
  const { data: keepers, isLoading } = useKeepersQuery();
  const callMutation = useCallKeeperMutation();
  const { targetWallet, addToast } = useSentinelStore();

  const handleCallKeeper = (slug: string) => {
    callMutation.mutate(
      {
        slug,
        inputs: {
          wallet_address: targetWallet,
          chain_id: '11155111',
          eth_usd_feed: '0x694AA1769357215DE4FAC081bf1f309aDC325306',
          breach_threshold_usd: '1500',
        },
      },
      {
        onSuccess: (data) => {
          addToast({
            type: 'success',
            title: `Keeper Execution Success [${slug}]`,
            message: `Run ID: ${data.run_id || 'run_001'}`,
          });
        },
        onError: (err) => {
          addToast({
            type: 'error',
            title: 'Invocation Failed',
            message: err.message,
          });
        },
      }
    );
  };

  return (
    <div className="space-y-6">
      {/* DecisionX Header */}
      <div className="dx-card p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400 text-xs font-mono mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            <span>KeeperHub Paid Workflow Registry</span>
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Marketplace Keeper Workflows</h2>
          <p className="text-xs text-slate-400 max-w-xl">
            Specialized execution Keepers monetized per-call via x402 & MPP micropayment headers.
          </p>
        </div>

        <div className="flex items-center space-x-3 text-xs font-mono">
          <div className="px-3 py-1.5 rounded-lg bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center space-x-1.5">
            <span className="w-2 h-2 rounded-full bg-blue-400" />
            <span>x402 (Base 8453)</span>
          </div>

          <div className="px-3 py-1.5 rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-400 flex items-center space-x-1.5">
            <span className="w-2 h-2 rounded-full bg-purple-400" />
            <span>MPP (Tempo 42431)</span>
          </div>
        </div>
      </div>

      {/* Keeper Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[1, 2, 3].map((i) => (
            <div key={i} className="dx-card h-64 animate-pulse" />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {keepers?.map((keeper) => {
            const isGuardian = keeper.slug === 'aave-v3-health-guardian';
            const isSnapshot = keeper.slug === 'defi-portfolio-snapshot';

            return (
              <motion.div
                key={keeper.slug}
                whileHover={{ y: -3 }}
                className={`dx-card p-6 flex flex-col justify-between space-y-6 ${
                  isGuardian
                    ? 'border-purple-500/30 shadow-glow-purple'
                    : isSnapshot
                    ? 'border-teal-500/30 shadow-glow'
                    : 'border-blue-500/30 shadow-glow-blue'
                }`}
              >
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono text-slate-400 uppercase tracking-wider">{keeper.type}</span>
                    <div className="px-3 py-1 rounded-full bg-teal-500/10 border border-teal-500/30 text-teal-400 font-mono font-bold text-xs flex items-center space-x-1">
                      <DollarSign className="w-3.5 h-3.5" />
                      <span>{keeper.price_usd.toFixed(2)} / call</span>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-bold text-white tracking-tight">{keeper.name}</h3>
                    <p className="text-xs font-mono text-teal-400/90 mt-0.5">{keeper.slug}</p>
                    <p className="text-xs text-slate-400 mt-2 leading-relaxed">{keeper.description}</p>
                  </div>
                </div>

                <div className="space-y-3 pt-4 border-t border-white/5">
                  <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
                    <span>Payment Settlement</span>
                    <span className="text-white font-semibold">x402 / MPP Auto</span>
                  </div>

                  <button
                    onClick={() => handleCallKeeper(keeper.slug)}
                    disabled={callMutation.isPending}
                    className="w-full py-2.5 rounded-xl bg-slate-900 border border-white/10 hover:border-teal-500/40 text-white font-medium text-xs transition-all flex items-center justify-center space-x-2"
                  >
                    <Play className="w-3.5 h-3.5 text-teal-400 fill-current" />
                    <span>Direct Call Keeper (${keeper.price_usd.toFixed(2)})</span>
                  </button>
                </div>
              </motion.div>
            );
          })}
        </div>
      )}
    </div>
  );
}

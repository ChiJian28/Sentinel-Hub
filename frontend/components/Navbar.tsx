'use client';

import React from 'react';
import { ConnectButton } from '@rainbow-me/rainbowkit';
import { Activity, Cpu, Database, Wallet, Sparkles } from 'lucide-react';
import { useSentinelStore } from '@/store/useSentinelStore';
import { useHealthQuery } from '@/hooks/useApi';

export function Navbar() {
  const { activeTab, setActiveTab } = useSentinelStore();
  const { data: health } = useHealthQuery();

  const tabs = [
    { id: 'overview', label: 'Platform Overview', icon: Activity },
    { id: 'sentry', label: 'Sentry Agent', icon: Cpu },
    { id: 'keepers', label: 'Marketplace Keepers', icon: Sparkles },
    { id: 'wallet', label: 'Wallet & Security', icon: Wallet },
    { id: 'audit', label: 'Audit Trail', icon: Database },
  ] as const;

  return (
    <header className="sticky top-0 z-40 w-full bg-slate-950/85 backdrop-blur-xl border-b border-white/10 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-17 flex items-center justify-between gap-4">
        {/* Brand Logo (icon.svg) & Tag */}
        <div className="flex items-center space-x-3 cursor-pointer shrink-0" onClick={() => setActiveTab('overview')}>
          <div className="relative w-10 h-10 rounded-xl overflow-hidden shadow-glow border border-teal-500/30 flex items-center justify-center bg-slate-950">
            <img src="/icon.svg" alt="Sentinel-Hub Logo" className="w-full h-full object-cover scale-110" />
          </div>
          <div className="flex items-center space-x-2">
            <span className="font-bold text-lg tracking-tight text-white font-sans">Sentinel-Hub</span>
            <span className="px-2 py-0.5 text-[9px] font-mono font-bold uppercase tracking-wider bg-teal-500/10 text-teal-400 border border-teal-500/30 rounded">
              DECISION AI
            </span>
          </div>
        </div>

        {/* DecisionX Navigation Items */}
        <nav className="hidden md:flex items-center space-x-1 bg-slate-900/80 p-1 rounded-xl border border-white/5">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all duration-200 ${
                  isActive
                    ? 'bg-teal-600 text-white shadow-sm font-semibold'
                    : 'text-slate-400 hover:text-white hover:bg-white/5'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Web3 Connect & Status Badge */}
        <div className="flex items-center space-x-3 shrink-0">
          <div className="hidden lg:flex items-center space-x-2 px-3 py-1 rounded-lg bg-slate-900 border border-white/10 text-xs font-mono">
            <span className={`w-2 h-2 rounded-full ${health?.status === 'ok' ? 'bg-teal-400 animate-pulse' : 'bg-amber-400'}`} />
            <span className="text-slate-300">Sepolia (11155111)</span>
          </div>
          <ConnectButton chainStatus="icon" showBalance={false} accountStatus="avatar" />
        </div>
      </div>

      {/* Mobile Nav Bar */}
      <div className="md:hidden flex items-center justify-around border-t border-white/5 py-2 bg-slate-950/90 backdrop-blur-md">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex flex-col items-center p-1.5 rounded-lg ${
                isActive ? 'text-teal-400' : 'text-slate-400'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span className="text-[10px] mt-0.5 font-medium">{tab.label}</span>
            </button>
          );
        })}
      </div>
    </header>
  );
}

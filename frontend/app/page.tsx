'use client';

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { DecisionXTicker } from '@/components/DecisionXTicker';
import { Navbar } from '@/components/Navbar';
import { ToastContainer } from '@/components/ToastContainer';
import { OverviewSection } from '@/components/OverviewSection';
import { SentryController } from '@/components/SentryController';
import { KeeperMarketplace } from '@/components/KeeperMarketplace';
import { WalletSecurityPanel } from '@/components/WalletSecurityPanel';
import { AuditExplorer } from '@/components/AuditExplorer';
import { useSentinelStore } from '@/store/useSentinelStore';

export default function Home() {
  const { activeTab } = useSentinelStore();

  return (
    <div className="min-h-screen bg-[#0b0f17] text-[#f8fafc] flex flex-col font-sans selection:bg-teal-500/20 selection:text-teal-400">
      {/* Top DecisionX Announcement & Ticker Bar */}
      <DecisionXTicker />

      {/* DecisionX Sticky Header Navbar */}
      <Navbar />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <AnimatePresence mode="wait">
          {activeTab === 'overview' && (
            <motion.div
              key="overview"
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -15 }}
              transition={{ duration: 0.2 }}
            >
              <OverviewSection />
            </motion.div>
          )}

          {activeTab === 'sentry' && (
            <motion.div
              key="sentry"
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -15 }}
              transition={{ duration: 0.2 }}
            >
              <SentryController />
            </motion.div>
          )}

          {activeTab === 'keepers' && (
            <motion.div
              key="keepers"
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -15 }}
              transition={{ duration: 0.2 }}
            >
              <KeeperMarketplace />
            </motion.div>
          )}

          {activeTab === 'wallet' && (
            <motion.div
              key="wallet"
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -15 }}
              transition={{ duration: 0.2 }}
            >
              <WalletSecurityPanel />
            </motion.div>
          )}

          {activeTab === 'audit' && (
            <motion.div
              key="audit"
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -15 }}
              transition={{ duration: 0.2 }}
            >
              <AuditExplorer />
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Global Toast Container */}
      <ToastContainer />

      {/* Footer */}
      <footer className="border-t border-white/5 py-8 mt-12 bg-slate-950/80 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-400 font-mono gap-4">
          <div className="flex items-center space-x-2">
            <span className="dx-bar-dot" />
            <span>Sentinel-Hub Decision AI Infrastructure · KeeperHub Hackathon 2026</span>
          </div>

          <div className="flex items-center space-x-6">
            <span>Base Mainnet (8453)</span>
            <span>Tempo Testnet (42431)</span>
            <span>Sepolia (11155111)</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

'use client';

import React, { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { WagmiProvider, http } from 'wagmi';
import { sepolia, base } from 'wagmi/chains';
import { RainbowKitProvider, getDefaultConfig, darkTheme } from '@rainbow-me/rainbowkit';
import '@rainbow-me/rainbowkit/styles.css';

// Custom Tempo Chain definition for MPP payment rail
const tempoChain = {
  id: 42431,
  name: 'Tempo Testnet',
  nativeCurrency: { name: 'USDC.e', symbol: 'USDC.e', decimals: 18 },
  rpcUrls: {
    default: { http: ['https://rpc.testnet.tempo.xyz'] },
  },
  blockExplorers: {
    default: { name: 'mppscan', url: 'https://mppscan.com' },
  },
  testnet: true,
};

// Valid WalletConnect Cloud Project ID with domain metadata binding
const WALLET_CONNECT_PROJECT_ID =
  process.env.NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID || 'c4f79cc821944d9680842e34466bfb00';

const wagmiConfig = getDefaultConfig({
  appName: 'Sentinel-Hub',
  appDescription: 'Autonomous Agentic Execution Economy on KeeperHub',
  appUrl: 'https://sentinel-hub-keeper.vercel.app',
  appIcon: 'https://sentinel-hub-keeper.vercel.app/icon.svg',
  projectId: WALLET_CONNECT_PROJECT_ID,
  chains: [sepolia, base, tempoChain as any],
  transports: {
    [sepolia.id]: http('https://rpc.ankr.com/eth_sepolia'),
    [base.id]: http('https://mainnet.base.org'),
    [tempoChain.id]: http('https://rpc.testnet.tempo.xyz'),
  },
  ssr: true,
});

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            refetchOnWindowFocus: false,
            retry: 2,
            staleTime: 10000,
          },
        },
      })
  );

  return (
    <WagmiProvider config={wagmiConfig}>
      <QueryClientProvider client={queryClient}>
        <RainbowKitProvider
          theme={darkTheme({
            accentColor: '#0d9488',
            accentColorForeground: '#ffffff',
            borderRadius: 'medium',
            fontStack: 'system',
            overlayBlur: 'small',
          })}
        >
          {children}
        </RainbowKitProvider>
      </QueryClientProvider>
    </WagmiProvider>
  );
}

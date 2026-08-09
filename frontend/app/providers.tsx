'use client';

import React, { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { WagmiProvider, createConfig, http } from 'wagmi';
import { sepolia, base } from 'wagmi/chains';
import { injected } from 'wagmi/connectors';
import { RainbowKitProvider, darkTheme } from '@rainbow-me/rainbowkit';
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

const wagmiConfig = createConfig({
  chains: [sepolia, base, tempoChain as any],
  connectors: [injected()],
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
            accentColor: '#10b981',
            accentColorForeground: '#09090b',
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

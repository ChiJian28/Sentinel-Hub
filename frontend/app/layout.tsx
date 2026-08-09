import type { Metadata } from 'next';
import './globals.css';
import { Providers } from './providers';

export const metadata: Metadata = {
  title: 'Sentinel-Hub — Autonomous Agentic Execution Economy',
  description:
    'The first protocol where AI Sentry Agents discover, pay via x402/MPP, and dispatch Execution Keepers on the KeeperHub Marketplace.',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#09090b] text-[#fafafa] antialiased selection:bg-emerald-500/20 selection:text-emerald-400">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}

import type { Metadata } from 'next';
import './globals.css';
import { Providers } from './providers';

export const metadata: Metadata = {
  title: 'Sentinel-Hub — Autonomous Agentic Execution Economy',
  description:
    'The first protocol where AI Sentry Agents discover, pay via x402/MPP, and dispatch Execution Keepers on the KeeperHub Marketplace.',
  icons: {
    icon: '/icon.svg',
    shortcut: '/icon.svg',
    apple: '/icon.svg',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="icon" href="/icon.svg" type="image/svg+xml" />
      </head>
      <body className="bg-[#0b0f17] text-[#f8fafc] antialiased selection:bg-teal-500/20 selection:text-teal-400">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}

import type { Metadata } from 'next';
import './globals.css';
import { Providers } from './providers';

export const metadata: Metadata = {
  metadataBase: new URL('https://sentinel-hub-keeper.vercel.app'),
  title: 'Sentinel-Hub — Autonomous Agentic Execution Economy',
  description:
    'The first protocol where AI Sentry Agents discover, pay via x402/MPP, and dispatch Execution Keepers on the KeeperHub Marketplace.',
  applicationName: 'Sentinel-Hub',
  authors: [{ name: 'Chijian Lim', url: 'https://github.com/ChiJian28/Sentinel-Hub' }],
  icons: {
    icon: '/icon.svg',
    shortcut: '/icon.svg',
    apple: '/icon.svg',
  },
  openGraph: {
    title: 'Sentinel-Hub — Autonomous Agentic Execution Economy',
    description:
      'AI Sentry Agents discover, pay via x402/MPP, and dispatch Execution Keepers on KeeperHub Marketplace.',
    url: 'https://sentinel-hub-keeper.vercel.app',
    siteName: 'Sentinel-Hub',
    images: [
      {
        url: '/icon.svg',
        width: 800,
        height: 800,
        alt: 'Sentinel-Hub Logo',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Sentinel-Hub — Autonomous Agentic Execution Economy',
    description:
      'AI Sentry Agents discover, pay via x402/MPP, and dispatch Execution Keepers on KeeperHub Marketplace.',
    images: ['/icon.svg'],
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

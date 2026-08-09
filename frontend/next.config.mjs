/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  transpilePackages: ['@rainbow-me/rainbowkit', 'wagmi', 'viem'],
  webpack: (config, { webpack }) => {
    config.resolve.fallback = {
      ...config.resolve.fallback,
      fs: false,
      net: false,
      tls: false,
      encoding: false,
    };

    config.resolve.alias = {
      ...config.resolve.alias,
      '@x402/svm/exact/client': false,
      '@x402/svm': false,
    };

    config.plugins.push(
      new webpack.IgnorePlugin({
        resourceRegExp: /^@x402\/svm/,
      })
    );

    config.externals.push('pino-pretty', 'lokijs', 'encoding');
    return config;
  },
};

export default nextConfig;

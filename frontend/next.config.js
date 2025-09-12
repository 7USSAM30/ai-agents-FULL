/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable standalone output for unified deployment
  output: 'standalone',
  
  // Environment variables for production
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || '/api',
  },
  
  // Optimize for production
  compress: true,
  poweredByHeader: false,
  
  // Enable experimental features for better performance
  experimental: {
    serverComponentsExternalPackages: ['python-shell'],
  },
  
  // Webpack configuration for Python integration
  webpack: (config, { isServer }) => {
    if (isServer) {
      // Allow importing Python modules
      config.externals.push('python-shell');
    }
    return config;
  },
};

module.exports = nextConfig;

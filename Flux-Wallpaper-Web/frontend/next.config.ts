import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  output: "standalone",
  allowedDevOrigins: ['http://localhost:3000', 'http://127.0.0.1:3000', 'http://10.121.223.22:3000', 'http://10.121.223.22:3000', '10.121.223.22'],
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://127.0.0.1:8000/api/:path*',
      },
    ]
  },
};

export default nextConfig;

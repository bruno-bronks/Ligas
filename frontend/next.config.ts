import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: {
    allowedDevOrigins: ["2.25.140.67", "2.25.140.67:3010", "localhost:3010"]
  }
};

export default nextConfig;

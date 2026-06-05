import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  allowedDevOrigins: ["2.25.140.67", "2.25.140.67:3010", "localhost:3010"],
  async rewrites() {
    const backendUrl = process.env.BACKEND_URL || "http://localhost:8000";
    return [
      {
        source: "/api/v1/:path*",
        destination: `${backendUrl}/api/v1/:path*`,
      },
    ];
  },
};

export default nextConfig;

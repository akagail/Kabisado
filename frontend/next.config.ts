import type { NextConfig } from "next";

const backend = process.env.BACKEND_INTERNAL_URL ?? "http://localhost:8000";

const nextConfig: NextConfig = {
  output: "standalone",
  // The Django API uses trailing slashes. Next's default 308 normalization
  // would strip them before the rewrite, loop with APPEND_SLASH, and break
  // every API call through the proxy.
  skipTrailingSlashRedirect: true,
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        // Next strips the trailing slash from `:path*`; Django expects it.
        destination: `${backend}/api/:path*/`,
      },
    ];
  },
};

export default nextConfig;

import { describe, expect, it } from "vitest";

import nextConfig from "../../next.config";

describe("API proxy config", () => {
  it("preserves trailing slashes so Django routes do not redirect-loop", () => {
    expect(nextConfig.skipTrailingSlashRedirect).toBe(true);
  });
});

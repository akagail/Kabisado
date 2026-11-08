import { beforeEach, describe, expect, it, vi } from "vitest";

import { ApiError, apiRequest, loginRedirectUrl, resetCsrfToken } from "@/lib/api/client";

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

describe("apiRequest", () => {
  const fetchMock = vi.fn();

  beforeEach(() => {
    fetchMock.mockReset();
    resetCsrfToken();
    vi.stubGlobal("fetch", fetchMock);
  });

  it("sends credentials and reads JSON", async () => {
    fetchMock.mockResolvedValueOnce(json({ user: { id: "1", email: "a@b.com" } }));

    const result = await apiRequest<{ user: { email: string } }>("/me/");

    expect(result.user.email).toBe("a@b.com");
    expect(fetchMock).toHaveBeenCalledWith(
      "/api/v1/me/",
      expect.objectContaining({ credentials: "include", method: "GET" }),
    );
  });

  it("refetches the CSRF token and retries once on csrf_error", async () => {
    fetchMock
      .mockResolvedValueOnce(json({ csrfToken: "first" }))
      .mockResolvedValueOnce(
        json({ error: { code: "csrf_error", message: "Expired." } }, 403),
      )
      .mockResolvedValueOnce(json({ csrfToken: "second" }))
      .mockResolvedValueOnce(json({ ok: true }));

    const result = await apiRequest<{ ok: boolean }>("/me/", {
      method: "PATCH",
      body: { display_name: "Ada" },
    });

    expect(result.ok).toBe(true);
    expect(fetchMock).toHaveBeenCalledTimes(4);
    const retry = fetchMock.mock.calls[3];
    const headers = retry[1].headers as Headers;
    expect(headers.get("X-CSRFToken")).toBe("second");
  });

  it("throws an ApiError with field messages", async () => {
    fetchMock
      .mockResolvedValueOnce(json({ csrfToken: "test-token" }))
      .mockResolvedValueOnce(
        json(
          {
            error: {
              code: "validation_error",
              message: "Validation failed.",
              fields: { password: ["Use at least 12 characters."] },
            },
          },
          400,
        ),
      );

    await expect(apiRequest("/auth/register/", { method: "POST", body: {} })).rejects.toEqual(
      expect.objectContaining({
        status: 400,
        code: "validation_error",
        fields: { password: ["Use at least 12 characters."] },
      }),
    );
  });

  it("maps a non-JSON failure to a generic ApiError", async () => {
    fetchMock.mockResolvedValueOnce(new Response("bad gateway", { status: 502 }));

    await expect(apiRequest("/me/")).rejects.toBeInstanceOf(ApiError);
  });

  it("builds a login redirect that returns to the current page", () => {
    expect(loginRedirectUrl("/profile/export", "?tab=ready")).toBe(
      "/login?next=%2Fprofile%2Fexport%3Ftab%3Dready",
    );
  });
});

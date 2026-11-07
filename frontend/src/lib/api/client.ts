const API_BASE = "/api/v1";
const SAFE_METHODS = new Set(["GET", "HEAD", "OPTIONS", "TRACE"]);

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly code: string,
    message: string,
    public readonly fields?: Record<string, string[]>,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

let csrfToken: string | null = null;

async function fetchCsrfToken(force = false): Promise<string> {
  if (csrfToken && !force) {
    return csrfToken;
  }
  const response = await fetch(`${API_BASE}/auth/csrf/`, {
    credentials: "include",
    cache: "no-store",
  });
  if (!response.ok) {
    throw new ApiError(response.status, "error", "Could not start a secure session.");
  }
  const data = (await response.json()) as { csrfToken?: string };
  if (!data.csrfToken) {
    throw new ApiError(500, "error", "Could not start a secure session.");
  }
  csrfToken = data.csrfToken;
  return csrfToken;
}

async function toApiError(response: Response): Promise<ApiError> {
  try {
    const body = (await response.json()) as {
      error?: { code?: string; message?: string; fields?: Record<string, string[]> };
    };
    return new ApiError(
      response.status,
      body.error?.code ?? "error",
      body.error?.message ?? "Something went wrong. Please try again.",
      body.error?.fields,
    );
  } catch {
    return new ApiError(
      response.status,
      "error",
      "Something went wrong. Please try again.",
    );
  }
}

export interface RequestOptions {
  method?: string;
  body?: unknown;
  headers?: HeadersInit;
}

export async function apiRequest<T>(
  path: string,
  options: RequestOptions = {},
): Promise<T> {
  const method = (options.method ?? "GET").toUpperCase();
  const unsafe = !SAFE_METHODS.has(method);
  let lastError: ApiError | null = null;

  for (let attempt = 0; attempt < 2; attempt += 1) {
    const headers = new Headers(options.headers);
    if (unsafe) {
      headers.set("X-CSRFToken", await fetchCsrfToken(attempt > 0));
    }
    if (options.body !== undefined) {
      headers.set("Content-Type", "application/json");
    }

    const response = await fetch(`${API_BASE}${path}`, {
      method,
      headers,
      credentials: "include",
      cache: "no-store",
      body: options.body === undefined ? undefined : JSON.stringify(options.body),
    });

    if (response.ok) {
      if (response.status === 204) {
        return undefined as T;
      }
      return (await response.json()) as T;
    }

    const error = await toApiError(response);
    if (unsafe && attempt === 0 && error.code === "csrf_error") {
      lastError = error;
      continue;
    }
    throw error;
  }

  throw lastError ?? new ApiError(403, "csrf_error", "Session expired. Please try again.");
}

export function resetCsrfToken(): void {
  csrfToken = null;
}

"use client";

import { useState } from "react";

import { requestExport } from "@/lib/api/auth";
import { ApiError } from "@/lib/api/client";
import type { ExportRequest } from "@/lib/api/types";

const STATUS_TEXT: Record<ExportRequest["status"], string> = {
  pending: "Export requested. We will notify you when it is ready.",
  ready: "Your export is ready to download.",
  expired: "The download link expired. Request a new export.",
};

export function ExportView() {
  const [exportRequest, setExportRequest] = useState<ExportRequest | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function request() {
    setError(null);
    setLoading(true);
    try {
      setExportRequest(await requestExport());
    } catch (caught) {
      if (caught instanceof ApiError) {
        setError(caught.message);
      } else {
        setError("Something went wrong. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-4">
      <button
        type="button"
        onClick={request}
        disabled={loading || exportRequest?.status === "pending"}
        className="rounded-lg bg-foreground px-4 py-2.5 text-sm font-semibold text-background disabled:opacity-60"
      >
        {loading ? "Requesting…" : "Request export"}
      </button>
      {exportRequest ? (
        <p role="status" aria-live="polite" className="text-sm text-muted-foreground">
          {STATUS_TEXT[exportRequest.status]}
        </p>
      ) : null}
      {exportRequest?.download_url ? (
        <a
          href={exportRequest.download_url}
          className="inline-block rounded-lg border px-4 py-2 text-sm font-semibold"
        >
          Download export
        </a>
      ) : null}
      {error ? (
        <p role="alert" aria-live="polite" className="text-sm text-red-700">
          {error}
        </p>
      ) : null}
    </div>
  );
}

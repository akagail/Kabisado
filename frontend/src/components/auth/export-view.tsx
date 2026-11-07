"use client";

import { useEffect, useState } from "react";

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
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        setExportRequest(await requestExport());
        if (cancelled) return;
      } catch (caught) {
        if (!cancelled) {
          if (caught instanceof ApiError && caught.code === "conflict") {
            setError("Export already requested. Check back later.");
          } else if (caught instanceof ApiError) {
            setError(caught.message);
          } else {
            setError("Something went wrong. Please try again.");
          }
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  async function request() {
    if (loading || submitting || exportRequest?.status === "pending") return;
    setError(null);
    setSubmitting(true);
    try {
      setExportRequest(await requestExport());
    } catch (caught) {
      if (caught instanceof ApiError) {
        setError(caught.message);
      } else {
        setError("Something went wrong. Please try again.");
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="space-y-4">
      {loading ? (
        <p role="status" aria-live="polite" className="text-sm text-muted-foreground">
          Checking export status…
        </p>
      ) : null}
      {error ? (
        <p role="alert" aria-live="polite" className="text-sm text-red-700">
          {error}
        </p>
      ) : null}
      {!exportRequest ? null : (
        <>
          <p role="status" aria-live="polite" className="text-sm text-muted-foreground">
            {STATUS_TEXT[exportRequest.status]}
          </p>
          <button
            type="button"
            onClick={request}
            disabled={submitting || exportRequest?.status === "pending"}
            className="rounded-lg bg-foreground px-4 py-2.5 text-sm font-semibold text-background disabled:opacity-60"
          >
            {submitting ? "Requesting…" : "Request export"}
          </button>
          {exportRequest.download_url ? (
            <a
              href={exportRequest.download_url}
              className="inline-block rounded-lg border px-4 py-2 text-sm font-semibold"
            >
              Download export
            </a>
          ) : null}
        </>
      )}
    </div>
  );
}

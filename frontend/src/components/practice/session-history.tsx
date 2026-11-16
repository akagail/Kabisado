"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { getHistory } from "@/lib/api/practice";
import type { PracticeHistoryEntry, PracticeStatus } from "@/lib/api/types";

const STATUS_LABELS: Record<PracticeStatus, string> = {
  in_progress: "In progress",
  submitted: "Submitted",
  expired: "Expired",
  abandoned: "Abandoned",
};

export function SessionHistory() {
  const [sessions, setSessions] = useState<PracticeHistoryEntry[] | null>(null);
  const [status, setStatus] = useState<"loading" | "ready" | "error">("loading");

  useEffect(() => {
    let cancelled = false;
    getHistory()
      .then((data) => {
        if (cancelled) return;
        setSessions(data);
        setStatus("ready");
      })
      .catch(() => {
        if (cancelled) return;
        setStatus("error");
      });
    return () => {
      cancelled = true;
    };
  }, []);

  if (status === "loading") {
    return (
      <p role="status" className="text-sm text-muted-foreground">
        Loading your practice history…
      </p>
    );
  }

  if (status === "error" || !sessions) {
    return (
      <p role="alert" className="text-sm text-red-700">
        Something went wrong loading your practice history.
      </p>
    );
  }

  if (sessions.length === 0) {
    return (
      <p className="text-sm text-muted-foreground">
        You have no practice sessions yet.{" "}
        <Link href="/exams" className="underline underline-offset-4">
          Browse the catalogue
        </Link>{" "}
        to start one.
      </p>
    );
  }

  return (
    <ul className="space-y-3">
      {sessions.map((session) => {
        const href =
          session.status === "submitted"
            ? `/practice/${session.id}/results`
            : `/practice/${session.id}`;
        const score =
          session.score_correct !== null && session.score_total !== null
            ? `${session.score_correct} of ${session.score_total}`
            : "—";

        return (
          <li key={session.id}>
            <Link
              href={href}
              className="flex flex-wrap items-baseline justify-between gap-2 rounded-lg border px-4 py-3 text-sm hover:bg-muted"
            >
              <span className="font-medium">
                {session.mode === "timed" ? "Timed" : "Untimed"} practice
              </span>
              <span>{STATUS_LABELS[session.status]}</span>
              <span>Score: {score}</span>
              <span className="text-muted-foreground">
                {new Date(session.started_at).toLocaleString()}
              </span>
            </Link>
          </li>
        );
      })}
    </ul>
  );
}

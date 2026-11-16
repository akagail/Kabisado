"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useRef, useState } from "react";

import { ApiError } from "@/lib/api/client";
import { getSession, saveAnswer, submitSession } from "@/lib/api/practice";
import type { PracticeSession } from "@/lib/api/types";

import { Countdown } from "./countdown";

type LoadStatus = "loading" | "ready" | "error" | "not-found";

export function PracticeSessionView({ sessionId }: { sessionId: string }) {
  const router = useRouter();
  const [session, setSession] = useState<PracticeSession | null>(null);
  const [status, setStatus] = useState<LoadStatus>("loading");
  const [index, setIndex] = useState(0);
  const [selected, setSelected] = useState<Record<number, string>>({});
  const [savingPosition, setSavingPosition] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [confirming, setConfirming] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const submitted = useRef(false);

  useEffect(() => {
    let cancelled = false;
    getSession(sessionId)
      .then((data) => {
        if (cancelled) return;
        if (data.status === "submitted") {
          router.replace(`/practice/${sessionId}/results`);
          return;
        }
        const saved: Record<number, string> = {};
        for (const item of data.items) {
          if (item.saved_answer) saved[item.position] = item.saved_answer.selected_option_id;
        }
        setSelected(saved);
        setSession(data);
        setStatus("ready");
      })
      .catch((caught) => {
        if (cancelled) return;
        setStatus(caught instanceof ApiError && caught.status === 404 ? "not-found" : "error");
      });
    return () => {
      cancelled = true;
    };
  }, [router, sessionId]);

  const submit = useCallback(async () => {
    if (submitted.current) return;
    submitted.current = true;
    setSubmitting(true);
    setError(null);
    try {
      await submitSession(sessionId);
      router.replace(`/practice/${sessionId}/results`);
    } catch (caught) {
      submitted.current = false;
      setSubmitting(false);
      setConfirming(false);
      setError(
        caught instanceof ApiError
          ? caught.message
          : "Something went wrong. Please try again.",
      );
    }
  }, [router, sessionId]);

  async function choose(position: number, optionId: string) {
    const previous = selected[position];
    setSelected((current) => ({ ...current, [position]: optionId }));
    setError(null);
    setSavingPosition(position);
    try {
      await saveAnswer(sessionId, position, optionId);
    } catch (caught) {
      setSelected((current) => {
        const next = { ...current };
        if (previous) next[position] = previous;
        else delete next[position];
        return next;
      });
      setError(
        caught instanceof ApiError
          ? caught.message
          : "Your answer could not be saved. Please try again.",
      );
    } finally {
      setSavingPosition(null);
    }
  }

  if (status === "loading") {
    return (
      <p role="status" className="text-sm text-muted-foreground">
        Loading session…
      </p>
    );
  }

  if (status === "not-found") {
    return (
      <p role="alert" className="text-sm text-red-700">
        This practice session was not found.{" "}
        <Link href="/practice" className="underline underline-offset-4">
          Back to your practice history
        </Link>
      </p>
    );
  }

  if (status === "error" || !session) {
    return (
      <p role="alert" className="text-sm text-red-700">
        Something went wrong loading this session.{" "}
        <Link href="/practice" className="underline underline-offset-4">
          Back to your practice history
        </Link>
      </p>
    );
  }

  const item = session.items[index];
  const isLast = index === session.items.length - 1;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <p className="text-sm text-muted-foreground">
          Question {index + 1} of {session.items.length}
        </p>
        {session.mode === "timed" && session.expires_at ? (
          <Countdown expiresAt={session.expires_at} onExpire={submit} />
        ) : null}
      </div>

      <fieldset className="space-y-3">
        <legend className="text-lg font-medium">{item.question.stem}</legend>
        {item.question.options.map((option) => (
          <label
            key={option.id}
            className="flex cursor-pointer items-start gap-3 rounded-lg border px-4 py-3 text-sm"
          >
            <input
              type="radio"
              name={`question-${item.position}`}
              value={option.id}
              checked={selected[item.position] === option.id}
              onChange={() => choose(item.position, option.id)}
              className="mt-0.5"
            />
            <span>{option.text}</span>
          </label>
        ))}
      </fieldset>

      {savingPosition === item.position ? (
        <p role="status" className="text-xs text-muted-foreground">
          Saving…
        </p>
      ) : null}

      {error ? (
        <p role="alert" className="text-sm text-red-700">
          {error}
        </p>
      ) : null}

      <div className="flex flex-wrap items-center gap-3">
        <button
          type="button"
          onClick={() => setIndex((current) => Math.max(0, current - 1))}
          disabled={index === 0}
          className="rounded-lg border px-4 py-2 text-sm font-medium disabled:opacity-60"
        >
          Previous
        </button>
        <button
          type="button"
          onClick={() => setIndex((current) => Math.min(session.items.length - 1, current + 1))}
          disabled={isLast}
          className="rounded-lg border px-4 py-2 text-sm font-medium disabled:opacity-60"
        >
          Next
        </button>
      </div>

      {confirming ? (
        <div className="space-y-3 rounded-lg border p-4">
          <p className="text-sm">
            Submit this session? Unanswered items count as incorrect.
          </p>
          <div className="flex flex-wrap gap-3">
            <button
              type="button"
              onClick={submit}
              disabled={submitting}
              className="rounded-lg bg-foreground px-4 py-2 text-sm font-semibold text-background disabled:opacity-60"
            >
              {submitting ? "Submitting…" : "Confirm submit"}
            </button>
            <button
              type="button"
              onClick={() => setConfirming(false)}
              disabled={submitting}
              className="rounded-lg border px-4 py-2 text-sm font-medium disabled:opacity-60"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <button
          type="button"
          onClick={() => setConfirming(true)}
          className="rounded-lg bg-foreground px-4 py-2 text-sm font-semibold text-background"
        >
          Submit session
        </button>
      )}
    </div>
  );
}

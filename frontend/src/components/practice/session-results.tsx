"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { ApiError } from "@/lib/api/client";
import { getResults } from "@/lib/api/practice";
import type { PracticeResults } from "@/lib/api/types";

export function SessionResults({ sessionId }: { sessionId: string }) {
  const [results, setResults] = useState<PracticeResults | null>(null);
  const [status, setStatus] = useState<"loading" | "ready" | "error" | "not-submitted">(
    "loading",
  );

  useEffect(() => {
    let cancelled = false;
    getResults(sessionId)
      .then((data) => {
        if (cancelled) return;
        setResults(data);
        setStatus("ready");
      })
      .catch((caught) => {
        if (cancelled) return;
        setStatus(
          caught instanceof ApiError && caught.status === 403 ? "not-submitted" : "error",
        );
      });
    return () => {
      cancelled = true;
    };
  }, [sessionId]);

  if (status === "loading") {
    return (
      <p role="status" className="text-sm text-muted-foreground">
        Loading results…
      </p>
    );
  }

  if (status === "not-submitted") {
    return (
      <p role="alert" className="text-sm text-red-700">
        Results are available after you submit.{" "}
        <Link href={`/practice/${sessionId}`} className="underline underline-offset-4">
          Back to the session
        </Link>
      </p>
    );
  }

  if (status === "error" || !results) {
    return (
      <p role="alert" className="text-sm text-red-700">
        Something went wrong loading these results.{" "}
        <Link href="/practice" className="underline underline-offset-4">
          Back to your practice history
        </Link>
      </p>
    );
  }

  return (
    <div className="space-y-8">
      <p className="text-lg font-semibold">
        Score: {results.score_correct} of {results.score_total}
      </p>

      <ol className="space-y-6">
        {results.items.map((item) => {
          const outcome = !item.selected_option_id
            ? "Not answered"
            : item.is_correct
              ? "Correct"
              : "Incorrect";

          return (
            <li key={item.position} className="space-y-3 rounded-lg border p-4">
              <div className="flex flex-wrap items-baseline justify-between gap-2">
                <p className="text-sm text-muted-foreground">
                  Question {item.position + 1}
                </p>
                <p className="text-sm font-semibold">{outcome}</p>
              </div>

              <p className="font-medium">{item.question.stem}</p>

              <ul className="space-y-1 text-sm">
                {item.question.options.map((option) => {
                  const correct = Boolean(option.is_correct);
                  const chosen = option.id === item.selected_option_id;
                  return (
                    <li key={option.id}>
                      {option.text}
                      {correct ? " — correct answer" : ""}
                      {chosen ? " — your answer" : ""}
                    </li>
                  );
                })}
              </ul>

              <p className="text-sm">
                <span className="font-medium">Explanation: </span>
                {item.explanation}
              </p>
              <p className="text-xs text-muted-foreground">
                Source: {item.provenance}
              </p>
            </li>
          );
        })}
      </ol>

      <p>
        <Link href="/practice" className="text-sm underline underline-offset-4">
          Back to your practice history
        </Link>
      </p>
    </div>
  );
}

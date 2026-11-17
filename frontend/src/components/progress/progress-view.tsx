"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { SessionHistory } from "@/components/practice/session-history";
import { getSubjectProgress, getTopicProgress } from "@/lib/api/analytics";
import type { SubjectAccuracy, TopicAccuracy } from "@/lib/api/types";

function attemptsLabel(attempts: number): string {
  return attempts === 1 ? "1 attempt" : `${attempts} attempts`;
}

export function ProgressView() {
  const [subjects, setSubjects] = useState<SubjectAccuracy[] | null>(null);
  const [topics, setTopics] = useState<TopicAccuracy[] | null>(null);
  const [status, setStatus] = useState<"loading" | "ready" | "error">("loading");

  useEffect(() => {
    let cancelled = false;
    Promise.all([getSubjectProgress(), getTopicProgress()])
      .then(([subjectData, topicData]) => {
        if (cancelled) return;
        setSubjects(subjectData.subjects);
        setTopics(topicData.topics);
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
        Loading your progress…
      </p>
    );
  }

  if (status === "error" || !subjects || !topics) {
    return (
      <p role="alert" className="text-sm text-red-700">
        Something went wrong loading your progress. Please try again.
      </p>
    );
  }

  const weakTopics = topics.filter((row) => row.weak_topic);

  return (
    <div className="space-y-10">
      <section aria-labelledby="subjects-heading" className="space-y-4">
        <h2 id="subjects-heading" className="text-xl font-semibold tracking-tight">
          Accuracy by subject
        </h2>
        {subjects.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Start practising with a topic.{" "}
            <Link href="/exams" className="underline underline-offset-4">
              Browse the catalogue
            </Link>
            .
          </p>
        ) : (
          <ul className="grid gap-3 sm:grid-cols-2">
            {subjects.map((row) => (
              <li key={row.subject.id} className="rounded-lg border p-4">
                <p className="font-medium">{row.subject.name}</p>
                <p className="mt-2 text-2xl font-semibold">{row.accuracy}%</p>
                <p className="text-sm text-muted-foreground">
                  {attemptsLabel(row.attempts)}
                </p>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section aria-labelledby="weak-topics-heading" className="space-y-4">
        <h2 id="weak-topics-heading" className="text-xl font-semibold tracking-tight">
          Weak topics
        </h2>
        {weakTopics.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            No weak topics yet. Keep practising and they will appear here.
          </p>
        ) : (
          <ul className="space-y-3">
            {weakTopics.map((row) => (
              <li
                key={row.topic.id}
                className="flex flex-wrap items-center justify-between gap-3 rounded-lg border px-4 py-3"
              >
                <div className="space-y-1">
                  <p className="font-medium">{row.topic.name}</p>
                  <p className="text-sm text-muted-foreground">
                    {row.accuracy}% over {attemptsLabel(row.attempts)}
                  </p>
                  {row.weak_reason ? (
                    <p className="text-xs text-muted-foreground">{row.weak_reason}</p>
                  ) : null}
                </div>
                <Link
                  href={`/topics/${row.topic.id}`}
                  className="rounded-lg border px-4 py-2 text-sm font-semibold"
                >
                  Practise
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section aria-labelledby="recent-sessions-heading" className="space-y-4">
        <h2 id="recent-sessions-heading" className="text-xl font-semibold tracking-tight">
          Recent sessions
        </h2>
        <SessionHistory />
      </section>
    </div>
  );
}

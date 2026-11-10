"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { getSubjects, getTopics } from "@/lib/api/catalogue";
import type { Subject, Topic } from "@/lib/api/types";

interface SubjectWithTopics {
  subject: Subject;
  topics: Topic[];
}

export function SubjectList({ versionId }: { versionId: string }) {
  const [subjects, setSubjects] = useState<SubjectWithTopics[]>([]);
  const [status, setStatus] = useState<"loading" | "ready" | "error">("loading");

  useEffect(() => {
    let cancelled = false;
    getSubjects(versionId)
      .then(async (rows) => {
        const withTopics = await Promise.all(
          rows.map(async (subject) => ({
            subject,
            topics: await getTopics(subject.id),
          })),
        );
        if (cancelled) return;
        setSubjects(withTopics);
        setStatus("ready");
      })
      .catch(() => {
        if (cancelled) return;
        setStatus("error");
      });
    return () => {
      cancelled = true;
    };
  }, [versionId]);

  if (status === "loading") {
    return <p role="status" className="text-sm text-muted-foreground">Loading subjects…</p>;
  }

  if (status === "error") {
    return (
      <p role="alert" className="text-sm text-red-700">
        Something went wrong. Please try again.
      </p>
    );
  }

  if (subjects.length === 0) {
    return (
      <p className="text-sm text-muted-foreground">
        This examination version has no subjects yet.{" "}
        <Link href="/exams" className="underline underline-offset-4">
          Back to the catalogue
        </Link>
      </p>
    );
  }

  return (
    <div className="space-y-8">
      {subjects.map(({ subject, topics }) => (
        <section key={subject.id} aria-labelledby={`subject-${subject.id}`} className="space-y-3">
          <h2 id={`subject-${subject.id}`} className="text-lg font-semibold">
            {subject.name}
          </h2>
          {topics.length === 0 ? (
            <p className="text-sm text-muted-foreground">No topics published for this subject.</p>
          ) : (
            <ul className="divide-y rounded-2xl border">
              {topics.map((topic) => (
                <li key={topic.id}>
                  <Link
                    href={`/topics/${topic.id}`}
                    className="flex min-h-11 items-center justify-between gap-3 px-4 py-3 hover:bg-muted/40 focus-visible:ring-2 focus-visible:ring-foreground/40"
                  >
                    <span className="text-sm">{topic.name}</span>
                    <span className="text-xs text-muted-foreground">
                      {topic.attempts > 0
                        ? `${topic.accuracy?.toFixed(1) ?? "—"}% · ${topic.attempts} attempts`
                        : "Not started"}
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </section>
      ))}
    </div>
  );
}

"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { getTopic } from "@/lib/api/catalogue";
import type { Topic } from "@/lib/api/types";

export function TopicDetail({ topicId }: { topicId: string }) {
  const [topic, setTopic] = useState<Topic | null>(null);
  const [status, setStatus] = useState<"loading" | "ready" | "error">("loading");

  useEffect(() => {
    let cancelled = false;
    getTopic(topicId)
      .then((data) => {
        if (cancelled) return;
        setTopic(data);
        setStatus("ready");
      })
      .catch(() => {
        if (cancelled) return;
        setStatus("error");
      });
    return () => {
      cancelled = true;
    };
  }, [topicId]);

  if (status === "loading") {
    return <p role="status" className="text-sm text-muted-foreground">Loading topic…</p>;
  }

  if (status === "error" || !topic) {
    return (
      <p role="alert" className="text-sm text-red-700">
        Topic not found.{" "}
        <Link href="/exams" className="underline underline-offset-4">
          Back to the catalogue
        </Link>
      </p>
    );
  }

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-semibold tracking-tight">{topic.name}</h1>
        {topic.weak_topic ? (
          <p className="inline-flex rounded-full border px-3 py-1 text-xs font-semibold">
            Weak topic
          </p>
        ) : null}
        <p className="text-sm text-muted-foreground">
          {topic.attempts > 0
            ? `${topic.accuracy?.toFixed(1) ?? "—"}% accuracy across ${topic.attempts} attempts`
            : "You have not practised this topic yet."}
        </p>
      </div>

      <button
        type="button"
        disabled
        className="w-full rounded-lg bg-foreground px-4 py-3 text-sm font-semibold text-background disabled:opacity-60 sm:w-auto"
      >
        Start practice
      </button>
      <p className="text-xs text-muted-foreground">
        Practice sessions are not enabled yet.
      </p>

      <p>
        <Link href="/exams" className="text-sm underline underline-offset-4">
          Back to the catalogue
        </Link>
      </p>
    </div>
  );
}

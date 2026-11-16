"use client";

import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";

import { TextField } from "@/components/ui/text-field";
import { ApiError } from "@/lib/api/client";
import { startSession } from "@/lib/api/practice";
import type { PracticeMode } from "@/lib/api/types";

export function StartPractice({ topicId }: { topicId: string }) {
  const router = useRouter();
  const [mode, setMode] = useState<PracticeMode>("untimed");
  const [size, setSize] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [starting, setStarting] = useState(false);

  async function start(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setStarting(true);
    try {
      const session = await startSession({ topic: topicId, mode, size });
      router.push(`/practice/${session.id}`);
    } catch (caught) {
      setError(
        caught instanceof ApiError
          ? caught.message
          : "Something went wrong. Please try again.",
      );
      setStarting(false);
    }
  }

  return (
    <form onSubmit={start} className="space-y-4">
      <fieldset className="space-y-2">
        <legend className="text-sm font-medium">Practice mode</legend>
        <label className="flex items-center gap-2 text-sm">
          <input
            type="radio"
            name="mode"
            value="untimed"
            checked={mode === "untimed"}
            onChange={() => setMode("untimed")}
          />
          Untimed
        </label>
        <label className="flex items-center gap-2 text-sm">
          <input
            type="radio"
            name="mode"
            value="timed"
            checked={mode === "timed"}
            onChange={() => setMode("timed")}
          />
          Timed
        </label>
      </fieldset>

      <TextField
        label="Number of questions"
        type="number"
        min={1}
        max={50}
        value={size}
        onChange={(event) => setSize(Number(event.target.value))}
        hint="Between 1 and 50. Fewer questions are used if the topic has fewer."
      />

      {error ? (
        <p role="alert" className="text-sm text-red-700">
          {error}
        </p>
      ) : null}

      <button
        type="submit"
        disabled={starting}
        className="w-full rounded-lg bg-foreground px-4 py-3 text-sm font-semibold text-background disabled:opacity-60 sm:w-auto"
      >
        {starting ? "Starting…" : "Start practice"}
      </button>
    </form>
  );
}

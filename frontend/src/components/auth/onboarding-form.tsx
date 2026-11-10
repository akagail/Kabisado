"use client";

import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";

import { updateMe } from "@/lib/api/auth";
import { ApiError } from "@/lib/api/client";

// shortcut: hard-coded exam slugs match the seeded catalogue; fetch /exams/ if a third exam ships.
const OPTIONS = [
  {
    value: "cse-professional",
    label: "Professional",
    hint: "For first- and second-level professional positions.",
  },
  {
    value: "cse-subprofessional",
    label: "Subprofessional",
    hint: "For first-level clerical and support positions.",
  },
];

export function OnboardingForm() {
  const router = useRouter();
  const [targetExam, setTargetExam] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!targetExam) {
      setError("Choose the examination you are preparing for.");
      return;
    }
    setError(null);
    setLoading(true);
    try {
      await updateMe({ target_exam: targetExam });
      router.push("/");
    } catch (caught) {
      setError(
        caught instanceof ApiError
          ? caught.message
          : "Something went wrong. Please try again.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={onSubmit} className="space-y-4">
      <fieldset className="space-y-3">
        <legend className="text-sm font-medium">Which examination are you preparing for?</legend>
        {OPTIONS.map((option) => (
          <label
            key={option.value}
            className="flex cursor-pointer gap-3 rounded-xl border p-4 has-[:focus-visible]:ring-2 has-[:focus-visible]:ring-foreground/40"
          >
            <input
              type="radio"
              name="target_exam"
              value={option.value}
              checked={targetExam === option.value}
              onChange={() => setTargetExam(option.value)}
              disabled={loading}
              className="mt-1"
            />
            <span>
              <span className="block text-sm font-semibold">{option.label}</span>
              <span className="block text-sm text-muted-foreground">{option.hint}</span>
            </span>
          </label>
        ))}
      </fieldset>
      {error ? (
        <p role="alert" aria-live="polite" className="text-sm text-red-700">
          {error}
        </p>
      ) : null}
      <button
        type="submit"
        disabled={loading}
        className="w-full rounded-lg bg-foreground px-4 py-2.5 text-sm font-semibold text-background disabled:opacity-60"
      >
        {loading ? "Saving…" : "Continue"}
      </button>
    </form>
  );
}

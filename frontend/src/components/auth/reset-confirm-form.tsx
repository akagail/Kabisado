"use client";

import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";

import { TextField } from "@/components/ui/text-field";
import { confirmPasswordReset } from "@/lib/api/auth";
import { ApiError } from "@/lib/api/client";

export function ResetConfirmForm({ token }: { token: string }) {
  const router = useRouter();
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [fields, setFields] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setFields({});

    if (password.length < 12) {
      setFields({ password: "Use at least 12 characters." });
      return;
    }
    if (password !== confirm) {
      setFields({ confirm: "Passwords do not match." });
      return;
    }

    setLoading(true);
    try {
      await confirmPasswordReset(token, password);
      router.push("/profile");
    } catch (caught) {
      if (caught instanceof ApiError) {
        setError(caught.message);
        setFields(
          Object.fromEntries(
            Object.entries(caught.fields ?? {}).map(([key, value]) => [key, value[0]]),
          ),
        );
      } else {
        setError("Something went wrong. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={onSubmit} noValidate className="space-y-4">
      <TextField
        label="New password"
        type="password"
        name="password"
        autoComplete="new-password"
        required
        value={password}
        onChange={(event) => setPassword(event.target.value)}
        error={fields.password}
        hint="At least 12 characters."
        disabled={loading}
      />
      <TextField
        label="Confirm new password"
        type="password"
        name="confirm"
        autoComplete="new-password"
        required
        value={confirm}
        onChange={(event) => setConfirm(event.target.value)}
        error={fields.confirm}
        disabled={loading}
      />
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
        {loading ? "Saving…" : "Set new password"}
      </button>
    </form>
  );
}

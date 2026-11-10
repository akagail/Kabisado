"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState, type FormEvent } from "react";

import { TextField } from "@/components/ui/text-field";
import { deleteMe, getMe, logout, updateMe } from "@/lib/api/auth";
import { ApiError } from "@/lib/api/client";
import type { SessionPayload } from "@/lib/api/types";

export function ProfileView() {
  const router = useRouter();
  const [session, setSession] = useState<SessionPayload | null>(null);
  const [status, setStatus] = useState<"loading" | "ready" | "error">("loading");
  const [displayName, setDisplayName] = useState("");
  const [targetExam, setTargetExam] = useState("");
  const [timezone, setTimezone] = useState("Asia/Manila");
  const [mode, setMode] = useState<"untimed" | "timed">("untimed");
  const [size, setSize] = useState(20);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [stale, setStale] = useState(false);
  const [fields, setFields] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);

  const [showDelete, setShowDelete] = useState(false);
  const [deletePassword, setDeletePassword] = useState("");
  const [deleteError, setDeleteError] = useState<string | null>(null);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    let cancelled = false;
    getMe()
      .then((data) => {
        if (cancelled) return;
        setSession(data);
        setDisplayName(data.profile.display_name);
        setTargetExam(data.profile.target_exam?.slug ?? "");
        setTimezone(data.profile.timezone);
        setMode(data.profile.preference.mode ?? "untimed");
        setSize(data.profile.preference.size ?? 20);
        setStatus("ready");
      })
      .catch((caught) => {
        if (cancelled) return;
        if (caught instanceof ApiError && caught.status === 401) {
          router.push("/login?next=/profile");
          return;
        }
        setStatus("error");
      });
    return () => {
      cancelled = true;
    };
  }, [router]);

  async function save(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage(null);
    setError(null);
    setStale(false);
    setFields({});
    setSaving(true);
    try {
      const result = await updateMe({
        display_name: displayName,
        ...(targetExam ? { target_exam: targetExam } : {}),
        timezone,
        preference: { mode, size },
        updated_at: session?.profile.updated_at,
      });
      setSession((current) => (current ? { ...current, profile: result.profile } : current));
      setMessage("Profile saved.");
    } catch (caught) {
      if (caught instanceof ApiError && caught.status === 409) {
        // Another tab saved first; offer a refresh instead of overwriting it.
        setStale(true);
      } else if (caught instanceof ApiError) {
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
      setSaving(false);
    }
  }

  async function signOut() {
    try {
      await logout();
    } finally {
      router.push("/login");
    }
  }

  async function removeAccount() {
    setDeleteError(null);
    setDeleting(true);
    try {
      await deleteMe(deletePassword);
      router.push("/?deleted=1");
    } catch (caught) {
      setDeleteError(
        caught instanceof ApiError
          ? caught.message
          : "Something went wrong. Please try again.",
      );
    } finally {
      setDeleting(false);
    }
  }

  if (status === "loading") {
    return <p role="status">Loading your profile…</p>;
  }

  if (status === "error") {
    return (
      <p role="alert" className="text-sm text-red-700">
        Could not load your profile. Refresh the page to try again.
      </p>
    );
  }

  return (
    <div className="space-y-8">
      <section className="rounded-2xl border p-6">
        <h2 className="text-lg font-semibold">Profile</h2>
        <p className="mt-1 text-sm text-muted-foreground">{session?.user.email}</p>
        <form onSubmit={save} className="mt-4 space-y-4">
          <TextField
            label="Display name"
            name="display_name"
            maxLength={80}
            value={displayName}
            onChange={(event) => setDisplayName(event.target.value)}
            error={fields.display_name}
            disabled={saving}
          />
          <fieldset className="space-y-2">
            <legend className="text-sm font-medium">Target examination</legend>
            <label className="flex items-center gap-2 text-sm">
              <input
                type="radio"
                name="target_exam"
                checked={targetExam === "cse-professional"}
                onChange={() => setTargetExam("cse-professional")}
                disabled={saving}
              />
              Professional
            </label>
            <label className="flex items-center gap-2 text-sm">
              <input
                type="radio"
                name="target_exam"
                checked={targetExam === "cse-subprofessional"}
                onChange={() => setTargetExam("cse-subprofessional")}
                disabled={saving}
              />
              Subprofessional
            </label>
          </fieldset>
          <TextField
            label="Timezone"
            name="timezone"
            value={timezone}
            onChange={(event) => setTimezone(event.target.value)}
            error={fields.timezone}
            disabled={saving}
          />
          <fieldset className="space-y-2">
            <legend className="text-sm font-medium">Practice preference</legend>
            <label className="flex items-center gap-2 text-sm">
              <input
                type="radio"
                name="mode"
                checked={mode === "untimed"}
                onChange={() => setMode("untimed")}
                disabled={saving}
              />
              Untimed
            </label>
            <label className="flex items-center gap-2 text-sm">
              <input
                type="radio"
                name="mode"
                checked={mode === "timed"}
                onChange={() => setMode("timed")}
                disabled={saving}
              />
              Timed
            </label>
          </fieldset>
          <TextField
            label="Questions per practice session"
            name="size"
            type="number"
            min={1}
            max={100}
            value={size}
            onChange={(event) => setSize(Number(event.target.value))}
            error={fields.preference}
            disabled={saving}
          />
          {message ? (
            <p role="status" aria-live="polite" className="text-sm text-muted-foreground">
              {message}
            </p>
          ) : null}
          {stale ? (
            <p role="alert" aria-live="polite" className="text-sm text-red-700">
              This profile was changed in another tab.{" "}
              <button
                type="button"
                onClick={() => window.location.reload()}
                className="underline underline-offset-4"
              >
                Refresh
              </button>{" "}
              to see the latest version.
            </p>
          ) : null}
          {error ? (
            <p role="alert" aria-live="polite" className="text-sm text-red-700">
              {error}
            </p>
          ) : null}
          <button
            type="submit"
            disabled={saving}
            className="rounded-lg bg-foreground px-4 py-2.5 text-sm font-semibold text-background disabled:opacity-60"
          >
            {saving ? "Saving…" : "Save profile"}
          </button>
        </form>
      </section>

      <section className="rounded-2xl border p-6">
        <h2 className="text-lg font-semibold">Your data</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Request a copy of your profile and learning history.
        </p>
        <Link
          href="/profile/export"
          className="mt-3 inline-block rounded-lg border px-4 py-2 text-sm font-semibold"
        >
          Manage export
        </Link>
      </section>

      <section className="rounded-2xl border p-6">
        <h2 className="text-lg font-semibold">Session</h2>
        <div className="mt-3 flex flex-wrap gap-3">
          <button
            type="button"
            onClick={signOut}
            className="rounded-lg border px-4 py-2 text-sm font-semibold"
          >
            Sign out
          </button>
          <button
            type="button"
            onClick={() => setShowDelete(true)}
            className="rounded-lg border border-red-300 px-4 py-2 text-sm font-semibold text-red-700"
          >
            Delete account
          </button>
        </div>
      </section>

      {showDelete ? (
        <section
          role="dialog"
          aria-modal="true"
          aria-labelledby="delete-heading"
          className="rounded-2xl border border-red-300 p-6"
        >
          <h2 id="delete-heading" className="text-lg font-semibold">
            Delete account
          </h2>
          <p className="mt-1 text-sm text-muted-foreground">
            This permanently deletes your account and all of your practice data.
          </p>
          <div className="mt-4 space-y-3">
            <TextField
              label="Confirm your password"
              type="password"
              name="delete-password"
              autoComplete="current-password"
              value={deletePassword}
              onChange={(event) => setDeletePassword(event.target.value)}
              disabled={deleting}
            />
            {deleteError ? (
              <p role="alert" aria-live="polite" className="text-sm text-red-700">
                {deleteError}
              </p>
            ) : null}
            <div className="flex gap-3">
              <button
                type="button"
                onClick={removeAccount}
                disabled={deleting || deletePassword.length === 0}
                className="rounded-lg bg-red-700 px-4 py-2 text-sm font-semibold text-white disabled:opacity-60"
              >
                {deleting ? "Deleting…" : "Delete permanently"}
              </button>
              <button
                type="button"
                onClick={() => {
                  setShowDelete(false);
                  setDeletePassword("");
                  setDeleteError(null);
                }}
                disabled={deleting}
                className="rounded-lg border px-4 py-2 text-sm font-semibold"
              >
                Cancel
              </button>
            </div>
          </div>
        </section>
      ) : null}
    </div>
  );
}

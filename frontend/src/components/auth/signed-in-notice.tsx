"use client";

import { useSyncExternalStore } from "react";

function subscribe() {
  return () => {};
}

function isAlreadySignedIn() {
  return window.location.hash === "#already-signed-in";
}

function serverSnapshot() {
  return false;
}

/**
 * Shows the "already signed in" notice when the register screen redirects here
 * (spec §10). The hash is client-only, so the server snapshot is always false.
 */
export function SignedInNotice() {
  const show = useSyncExternalStore(subscribe, isAlreadySignedIn, serverSnapshot);

  if (!show) return null;

  return (
    <p role="status" aria-live="polite" className="rounded-2xl border px-4 py-3 text-sm">
      You are already signed in.
    </p>
  );
}

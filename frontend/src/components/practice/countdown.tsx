"use client";

import { useEffect, useRef, useState } from "react";

export function Countdown({
  expiresAt,
  onExpire,
}: {
  expiresAt: string;
  onExpire: () => void;
}) {
  const target = new Date(expiresAt).getTime();
  const [remaining, setRemaining] = useState(() => Math.max(0, target - Date.now()));
  const fired = useRef(false);

  useEffect(() => {
    function tick() {
      const next = Math.max(0, target - Date.now());
      setRemaining(next);
      if (next === 0 && !fired.current) {
        fired.current = true;
        onExpire();
      }
    }
    tick();
    const timer = window.setInterval(tick, 1000);
    return () => window.clearInterval(timer);
  }, [target, onExpire]);

  const totalSeconds = Math.ceil(remaining / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;

  return (
    <p role="timer" aria-label="Time remaining" className="text-sm font-semibold">
      {minutes}:{String(seconds).padStart(2, "0")} remaining
    </p>
  );
}

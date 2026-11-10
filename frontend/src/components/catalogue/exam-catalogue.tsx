"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { getExamFamilies } from "@/lib/api/catalogue";
import type { ExamFamily } from "@/lib/api/types";

export function ExamCatalogue() {
  const [families, setFamilies] = useState<ExamFamily[]>([]);
  const [status, setStatus] = useState<"loading" | "ready" | "error">("loading");

  useEffect(() => {
    let cancelled = false;
    getExamFamilies()
      .then((data) => {
        if (cancelled) return;
        setFamilies(data.exam_families);
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
    return <p role="status" className="text-sm text-muted-foreground">Loading the catalogue…</p>;
  }

  if (status === "error") {
    return (
      <p role="alert" className="text-sm text-red-700">
        Something went wrong. Please try again.
      </p>
    );
  }

  if (families.length === 0) {
    return <p className="text-sm text-muted-foreground">No examinations are published yet.</p>;
  }

  return (
    <div className="space-y-8">
      {families.map((family) => (
        <section key={family.id} aria-labelledby={`family-${family.id}`} className="space-y-3">
          <h2 id={`family-${family.id}`} className="text-sm font-semibold">
            {family.name}
          </h2>
          <ul className="space-y-3">
            {family.exams.map((exam) => (
              <li key={exam.id}>
                {exam.current_version ? (
                  <Link
                    href={`/subjects/${exam.current_version.id}`}
                    className="block rounded-2xl border p-4 hover:border-foreground/40 focus-visible:ring-2 focus-visible:ring-foreground/40"
                  >
                    <span className="block text-base font-semibold">{exam.name}</span>
                    <span className="mt-1 block text-sm text-muted-foreground">
                      {exam.current_version.label}
                      {exam.current_version.passing_rate
                        ? ` · passing ${exam.current_version.passing_rate.toFixed(2)}`
                        : ""}
                    </span>
                  </Link>
                ) : (
                  <div className="rounded-2xl border p-4">
                    <span className="block text-base font-semibold">{exam.name}</span>
                    <span className="mt-1 block text-sm text-muted-foreground">
                      No published version yet.
                    </span>
                  </div>
                )}
              </li>
            ))}
          </ul>
        </section>
      ))}
    </div>
  );
}

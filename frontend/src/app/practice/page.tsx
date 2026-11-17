import { SessionHistory } from "@/components/practice/session-history";

export default function PracticeHistoryPage() {
  return (
    <main className="mx-auto w-full max-w-2xl px-6 py-16">
      <h1 className="text-3xl font-semibold tracking-tight">Practice history</h1>
      <p className="mt-2 text-sm text-muted-foreground">
        <a href="/progress" className="underline underline-offset-4">
          See your progress by subject and weak topics
        </a>
      </p>
      <div className="mt-8">
        <SessionHistory />
      </div>
    </main>
  );
}

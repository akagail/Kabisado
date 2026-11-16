import { SessionHistory } from "@/components/practice/session-history";

export default function PracticeHistoryPage() {
  return (
    <main className="mx-auto w-full max-w-2xl px-6 py-16">
      <h1 className="text-3xl font-semibold tracking-tight">Practice history</h1>
      <div className="mt-8">
        <SessionHistory />
      </div>
    </main>
  );
}

import { ProgressView } from "@/components/progress/progress-view";

export default function ProgressPage() {
  return (
    <main className="mx-auto w-full max-w-2xl px-6 py-16">
      <h1 className="text-3xl font-semibold tracking-tight">Your progress</h1>
      <div className="mt-8">
        <ProgressView />
      </div>
    </main>
  );
}

import { SessionResults } from "@/components/practice/session-results";

export default async function PracticeResultsPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  return (
    <main className="mx-auto w-full max-w-2xl px-6 py-16">
      <h1 className="mb-8 text-3xl font-semibold tracking-tight">Results</h1>
      <SessionResults sessionId={id} />
    </main>
  );
}

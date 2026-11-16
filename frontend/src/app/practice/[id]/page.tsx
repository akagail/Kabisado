import { PracticeSessionView } from "@/components/practice/practice-session";

export default async function PracticeSessionPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  return (
    <main className="mx-auto w-full max-w-2xl px-6 py-16">
      <h1 className="mb-8 text-3xl font-semibold tracking-tight">Practice session</h1>
      <PracticeSessionView sessionId={id} />
    </main>
  );
}

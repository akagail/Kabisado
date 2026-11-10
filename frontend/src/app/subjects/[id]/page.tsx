import { SubjectList } from "@/components/catalogue/subject-list";

export default async function SubjectsPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;

  return (
    <main className="mx-auto w-full max-w-2xl px-6 py-16">
      <h1 className="text-3xl font-semibold tracking-tight">Subjects</h1>
      <p className="mt-2 text-sm text-muted-foreground">
        Coverage areas in the official bulletin order.
      </p>
      <div className="mt-8">
        <SubjectList versionId={id} />
      </div>
    </main>
  );
}

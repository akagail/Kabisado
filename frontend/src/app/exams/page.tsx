import { ExamCatalogue } from "@/components/catalogue/exam-catalogue";

export default function ExamsPage() {
  return (
    <main className="mx-auto w-full max-w-2xl px-6 py-16">
      <h1 className="text-3xl font-semibold tracking-tight">Catalogue</h1>
      <p className="mt-2 text-sm text-muted-foreground">
        Official coverage areas for the examination you are preparing for.
      </p>
      <div className="mt-8">
        <ExamCatalogue />
      </div>
    </main>
  );
}

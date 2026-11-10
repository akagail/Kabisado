import { SignedInNotice } from "@/components/auth/signed-in-notice";

export default function Home() {
  return (
    <main className="mx-auto flex min-h-dvh w-full max-w-3xl flex-col justify-center gap-8 px-6 py-16">
      <div className="space-y-3">
        <p className="text-xs font-semibold tracking-[0.2em] text-muted-foreground uppercase">
          Kabisado
        </p>
        <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">
          Study with intent.
        </h1>
        <p className="max-w-xl text-lg leading-relaxed text-muted-foreground">
          An AI-assisted examination preparation platform, starting with the
          Philippine Civil Service Examination.
        </p>
      </div>

      <SignedInNotice />

      <section
        aria-labelledby="status-heading"
        className="rounded-2xl border p-6"
      >
        <h2 id="status-heading" className="text-sm font-semibold">
          Engineering foundation
        </h2>
        <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
          The foundation is in place. Examination features are not enabled yet.
        </p>
      </section>

      <nav aria-label="Account" className="flex flex-wrap gap-3">
        <a href="/exams" className="rounded-lg border px-4 py-2.5 text-sm font-semibold">
          Browse the catalogue
        </a>
        <a
          href="/register"
          className="rounded-lg bg-foreground px-4 py-2.5 text-sm font-semibold text-background"
        >
          Create account
        </a>
        <a href="/login" className="rounded-lg border px-4 py-2.5 text-sm font-semibold">
          Sign in
        </a>
      </nav>

      <p className="text-xs text-muted-foreground">
        Kabisado is not affiliated with the Civil Service Commission.
      </p>
    </main>
  );
}

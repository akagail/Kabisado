import Link from "next/link";

import { ExportView } from "@/components/auth/export-view";

export default function ExportPage() {
  return (
    <main className="mx-auto w-full max-w-md px-6 py-16">
      <h1 className="text-3xl font-semibold tracking-tight">Data export</h1>
      <p className="mt-2 text-sm text-muted-foreground">
        Exports are fulfilled manually at alpha and are available for seven days.
      </p>
      <div className="mt-8">
        <ExportView />
      </div>
      <p className="mt-6 text-sm text-muted-foreground">
        <Link href="/profile" className="underline underline-offset-4">
          Back to profile
        </Link>
      </p>
    </main>
  );
}

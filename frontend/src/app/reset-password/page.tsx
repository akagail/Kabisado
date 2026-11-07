import Link from "next/link";

import { ResetRequestForm } from "@/components/auth/reset-request-form";

export default function ResetPasswordPage() {
  return (
    <main className="mx-auto w-full max-w-md px-6 py-16">
      <h1 className="text-3xl font-semibold tracking-tight">Reset password</h1>
      <p className="mt-2 text-sm text-muted-foreground">
        Enter your email and we will send a reset link if the address exists.
      </p>
      <div className="mt-8">
        <ResetRequestForm />
      </div>
      <p className="mt-6 text-sm text-muted-foreground">
        <Link href="/login" className="underline underline-offset-4">
          Back to sign in
        </Link>
      </p>
    </main>
  );
}

import Link from "next/link";

import { LoginForm } from "@/components/auth/login-form";

export default function LoginPage() {
  return (
    <main className="mx-auto w-full max-w-md px-6 py-16">
      <h1 className="text-3xl font-semibold tracking-tight">Sign in</h1>
      <p className="mt-2 text-sm text-muted-foreground">
        Continue your examination preparation.
      </p>
      <div className="mt-8">
        <LoginForm />
      </div>
      <p className="mt-6 text-sm text-muted-foreground">
        New here?{" "}
        <Link href="/register" className="underline underline-offset-4">
          Create an account
        </Link>
      </p>
    </main>
  );
}

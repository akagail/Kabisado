import { ResetConfirmForm } from "@/components/auth/reset-confirm-form";

export default async function ResetPasswordConfirmPage({
  params,
}: {
  params: Promise<{ token: string }>;
}) {
  const { token } = await params;

  return (
    <main className="mx-auto w-full max-w-md px-6 py-16">
      <h1 className="text-3xl font-semibold tracking-tight">Set a new password</h1>
      <p className="mt-2 text-sm text-muted-foreground">
        Reset links are single use and expire after three days.
      </p>
      <div className="mt-8">
        <ResetConfirmForm token={token} />
      </div>
    </main>
  );
}

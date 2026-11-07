import { OnboardingForm } from "@/components/auth/onboarding-form";

export default function OnboardingPage() {
  return (
    <main className="mx-auto w-full max-w-md px-6 py-16">
      <h1 className="text-3xl font-semibold tracking-tight">Choose your exam</h1>
      <p className="mt-2 text-sm text-muted-foreground">
        This scopes the catalogue and practice sets to your target examination.
      </p>
      <div className="mt-8">
        <OnboardingForm />
      </div>
    </main>
  );
}

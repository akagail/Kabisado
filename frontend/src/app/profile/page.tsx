import { ProfileView } from "@/components/auth/profile-view";

export default function ProfilePage() {
  return (
    <main className="mx-auto w-full max-w-2xl px-6 py-16">
      <h1 className="text-3xl font-semibold tracking-tight">Your account</h1>
      <div className="mt-8">
        <ProfileView />
      </div>
    </main>
  );
}

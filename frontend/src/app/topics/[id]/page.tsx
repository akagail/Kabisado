import { TopicDetail } from "@/components/catalogue/topic-detail";

export default async function TopicPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;

  return (
    <main className="mx-auto w-full max-w-2xl px-6 py-16">
      <TopicDetail topicId={id} />
    </main>
  );
}

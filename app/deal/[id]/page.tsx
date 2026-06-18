import { DealDetailClient } from "@/components/DealDetailClient";

type DealDetailPageProps = {
  params: Promise<{
    id: string;
  }>;
};

export default async function DealDetailPage({ params }: DealDetailPageProps) {
  const { id } = await params;
  return <DealDetailClient dealId={id} />;
}

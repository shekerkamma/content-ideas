"use client";

import { useQuery } from "convex/react";
import { api } from "@/convex/_generated/api";
import { PackageDownload } from "@/components/PackageDownload";
import { PipelineProgress } from "@/components/PipelineProgress";

type DealDetailClientProps = {
  dealId: string;
};

type StageOutputRecord = {
  stage: string;
  status: "pending" | "running" | "completed" | "failed";
  output: Record<string, unknown>;
};

export function DealDetailClient({ dealId }: DealDetailClientProps) {
  const result = useQuery(api.pipeline.getDealPipeline, { dealId: dealId as never });
  const stageOutputs = (result?.stageOutputs ?? []) as StageOutputRecord[];

  function getStage(stage: string) {
    return stageOutputs.find((output) => output.stage === stage);
  }

  const researchStage = getStage("research");
  const briefStage = getStage("brief");
  const deckStage = getStage("deck");
  const objectionsStage = getStage("objections");
  const packageStage = getStage("package");

  const steps = [
    {
      label: "Research",
      status: researchStage?.status ?? "pending",
      preview: (researchStage?.output.companyDescription as string | undefined) ?? undefined
    },
    {
      label: "Brief",
      status: briefStage?.status ?? "pending",
      preview: ((briefStage?.output.markdown as string | undefined) ?? undefined)?.slice(0, 80)
    },
    {
      label: "Deck",
      status: deckStage?.status ?? "pending",
      preview: Array.isArray(deckStage?.output.slides)
        ? `${(deckStage?.output.slides as Array<unknown>).length} slides`
        : undefined
    },
    {
      label: "Objections",
      status: objectionsStage?.status ?? "pending",
      preview: Array.isArray(objectionsStage?.output.scripts)
        ? `${(objectionsStage?.output.scripts as Array<unknown>).length} scripts`
        : undefined
    },
    {
      label: "Package",
      status: packageStage?.status ?? "pending",
      preview: Array.isArray(packageStage?.output.notes) ? (packageStage?.output.notes as string[])[0] : undefined
    }
  ];

  const packageRecord = packageStage?.output;
  const packageUrls = result?.deal
    ? {
        briefUrl: `/api/deals/${dealId}/download?artifact=brief`,
        deckUrl: `/api/deals/${dealId}/download?artifact=deck`,
        objectionsUrl: `/api/deals/${dealId}/download?artifact=objections`,
        zipUrl: `/api/deals/${dealId}/download?artifact=zip`
      }
    : null;

  return (
    <main className="min-h-screen bg-paper">
      <section className="mx-auto max-w-6xl px-6 py-8 sm:px-8 lg:px-10">
        <div className="mb-6">
          <p className="text-sm font-medium text-stone-500">DealForge</p>
          <h1 className="text-2xl font-semibold text-ink">{result?.deal?.prospectName ?? "Deal details"}</h1>
          <p className="mt-1 text-sm text-stone-600">
            {result?.deal?.prospectIndustry ?? "Unknown industry"} · {result?.deal?.useCase ?? "No use case set"}
          </p>
        </div>

        <div className="grid gap-6 lg:grid-cols-[1.4fr_0.9fr]">
          <PipelineProgress steps={steps} />
          <div className="space-y-6">
            <div className="rounded-lg border border-stone-200 bg-white p-5">
              <h2 className="text-base font-semibold text-ink">Current package</h2>
              <p className="mt-1 text-sm text-stone-600">
                {(packageRecord?.notes as string[] | undefined)?.[0] ??
                  "The package manifest will appear once the pipeline reaches the final stage."}
              </p>
            </div>

            <PackageDownload
              briefUrl={packageUrls?.briefUrl}
              deckUrl={packageUrls?.deckUrl}
              objectionsUrl={packageUrls?.objectionsUrl}
              zipUrl={packageUrls?.zipUrl}
            />
          </div>
        </div>
      </section>
    </main>
  );
}

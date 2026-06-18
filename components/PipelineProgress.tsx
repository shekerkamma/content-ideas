"use client";

import { CheckCircle2, Circle, Loader2, XCircle } from "lucide-react";

type PipelineStep = {
  label: string;
  status: "pending" | "running" | "completed" | "failed";
  preview?: string;
};

type PipelineProgressProps = {
  steps: PipelineStep[];
};

export function PipelineProgress({ steps }: PipelineProgressProps) {
  return (
    <div className="rounded-lg border border-stone-200 bg-white p-5">
      <div className="mb-4 flex items-center justify-between gap-3">
        <div>
          <h2 className="text-base font-semibold text-ink">Pipeline progress</h2>
          <p className="mt-1 text-sm text-stone-600">Research, brief, deck, objections, and package.</p>
        </div>
        <div className="text-sm font-medium text-stone-500">{steps.filter((step) => step.status === "completed").length}/5 complete</div>
      </div>

      <div className="space-y-3">
        {steps.map((step) => {
          const icon =
            step.status === "completed" ? (
              <CheckCircle2 className="h-5 w-5 text-emerald-600" />
            ) : step.status === "running" ? (
              <Loader2 className="h-5 w-5 animate-spin text-amber-600" />
            ) : step.status === "failed" ? (
              <XCircle className="h-5 w-5 text-red-600" />
            ) : (
              <Circle className="h-5 w-5 text-stone-300" />
            );

          return (
            <div key={step.label} className="flex items-start gap-3 rounded-md border border-stone-100 px-3 py-2">
              <div className="mt-0.5">{icon}</div>
              <div className="min-w-0">
                <div className="text-sm font-medium text-ink">{step.label}</div>
                <div className="text-sm text-stone-600">{step.preview ?? step.status}</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

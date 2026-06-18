import type { DeckPlan } from "./pptx";
import type { ObjectionPlan } from "./objections";
import type { ProspectResearch } from "./search";
import type { StrategyBriefResult } from "./ai";

export type PackageManifest = {
  outputName: string;
  briefUrl: string;
  deckUrl: string;
  objectionsUrl: string;
  zipUrl: string;
  status: "scaffold" | "ready";
  notes: string[];
};

export type PackageInput = {
  dealId: string;
  prospectName: string;
  research: ProspectResearch;
  brief: StrategyBriefResult;
  deck: DeckPlan;
  objections: ObjectionPlan;
};

export function buildPackageManifest(input: PackageInput): PackageManifest {
  const slug = input.prospectName.toLowerCase().replace(/[^a-z0-9]+/g, "-");
  const base = `/api/deals/${input.dealId}/download`;

  return {
    outputName: `${slug}-deal-package.zip`,
    briefUrl: `${base}?artifact=brief`,
    deckUrl: `${base}?artifact=deck`,
    objectionsUrl: `${base}?artifact=objections`,
    zipUrl: `${base}?artifact=zip`,
    status: "scaffold",
    notes: [
      "Package bundle scaffold created from the stage outputs.",
      "Wire the download route and file storage in the next pass."
    ]
  };
}

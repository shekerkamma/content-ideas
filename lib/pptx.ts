import fs from "node:fs";
import path from "node:path";
import type { ProspectResearch } from "./search";

export type DeckSlide = {
  title: string;
  subtitle?: string;
  bullets: string[];
  notes?: string;
};

export type DeckPlan = {
  templatePath: string;
  outputName: string;
  slideCount: number;
  slides: DeckSlide[];
  renderStatus: "scaffold" | "ready";
  brand: {
    primaryColor: string;
    secondaryColor: string;
    footerText: string;
  };
};

export type DeckPlanInput = {
  prospectName: string;
  prospectIndustry?: string;
  useCase?: string;
  research: ProspectResearch;
  briefMarkdown: string;
};

function resolveTemplatePath() {
  const candidates = [
    process.env.BRANDED_PPTX_TEMPLATE,
    path.join(process.cwd(), "templates/default.pptx"),
    path.join(process.env.HOME ?? "", ".claude/templates/branded-template.pptx")
  ].filter((candidate): candidate is string => Boolean(candidate));

  return candidates.find((candidate) => fs.existsSync(candidate)) ?? candidates[0];
}

export function buildDeckPlan(input: DeckPlanInput): DeckPlan {
  const summary = input.briefMarkdown
    .split("\n")
    .find((line) => line.trim().length > 0)
    ?.replace(/^#\s*/, "")
    .trim();

  const researchSignal = input.research.aiSignals[0] ?? "No strong AI signal surfaced yet.";
  const useCase = input.useCase ?? "AI transformation";
  const industry = input.prospectIndustry ?? input.research.industry;

  return {
    templatePath: resolveTemplatePath(),
    outputName: `${input.prospectName.toLowerCase().replace(/[^a-z0-9]+/g, "-")}-deal-deck.pptx`,
    slideCount: 10,
    renderStatus: "scaffold",
    brand: {
      primaryColor: "#B91C1C",
      secondaryColor: "#151515",
      footerText: "Prepared with DealForge"
    },
    slides: [
      {
        title: `${input.prospectName} | AI Opportunity`,
        subtitle: useCase,
        bullets: [industry, researchSignal],
        notes: "Cover slide should feel consultant-grade and branded."
      },
      {
        title: "Executive summary",
        bullets: [
          summary ?? "The account is a fit for a tailored pre-sales brief.",
          `Focus the story on ${useCase}.`,
          `Keep the deck specific to ${input.prospectName}.`
        ]
      },
      {
        title: "Prospect context",
        bullets: [
          input.research.companyDescription,
          `Size: ${input.research.size}`,
          `Confidence: ${input.research.confidence}`
        ]
      },
      {
        title: "Research signals",
        bullets: input.research.recentNews.concat(input.research.aiSignals).slice(0, 4),
        notes: "Call out what is known and what remains uncertain."
      },
      {
        title: "AI opportunity",
        bullets: [
          `Primary use case: ${useCase}`,
          `Industry fit: ${industry}`,
          "Lead with business value, then implementation shape."
        ]
      },
      {
        title: "Use-case realization",
        bullets: [
          "What the workflow looks like today",
          "Where AI shortens the cycle",
          "What changes for the buyer"
        ]
      },
      {
        title: "Solution architecture",
        bullets: [
          "Research -> brief -> deck -> objections -> package",
          "Durable outputs with editable formats",
          "Use the package as a meeting-ready artifact"
        ]
      },
      {
        title: "Timeline",
        bullets: [
          "Week 1: confirm scope",
          "Week 2: pilot the use case",
          "Week 3+: iterate with buyer feedback"
        ]
      },
      {
        title: "Investment and risk",
        bullets: [
          "Position the package as a low-risk next step",
          "Call out thin-data sections explicitly",
          "Tie cost to unbilled prep time"
        ]
      },
      {
        title: "Next steps",
        bullets: [
          "Review the deck with the customer",
          "Refine the weak sections",
          "Move to package assembly"
        ]
      }
    ]
  };
}

import type { ProspectResearch } from "./search";
import type { StrategyBriefResult } from "./ai";

export type ObjectionScript = {
  objection: string;
  response: string;
  coachingNote: string;
};

export type ObjectionPlan = {
  source: "anthropic" | "fallback";
  scripts: ObjectionScript[];
  qualityNotes: string[];
};

export type ObjectionInput = {
  prospectName: string;
  prospectIndustry?: string;
  useCase?: string;
  research: ProspectResearch;
  brief: StrategyBriefResult;
};

function fallbackObjections(input: ObjectionInput): ObjectionPlan {
  return {
    source: "fallback",
    scripts: [
      {
        objection: "We already have an internal process for this.",
        response: `Acknowledge the current process, then show how ${input.prospectName} can save prep time and improve consistency with a reusable package.`,
        coachingNote: "Anchor the answer in time saved and consistency, not tool novelty."
      },
      {
        objection: "We need to see evidence this will work for us.",
        response: `Use the research signals and the ${input.useCase ?? "target use case"} framing to show why the proposal is tailored to ${input.prospectName}.`,
        coachingNote: "Emphasize specificity and a low-risk pilot."
      },
      {
        objection: "Our data is probably too thin.",
        response: "Agree, call out the gap, and position the package as a way to make the weak areas explicit before the meeting.",
        coachingNote: "Thin data should be a signal to collaborate, not a reason to overclaim."
      },
      {
        objection: "We are not ready to invest in AI right now.",
        response: "Position the package as decision support, not a platform commitment. The first win is a stronger sales conversation.",
        coachingNote: "Keep the scope tied to pre-sales efficiency."
      },
      {
        objection: "This feels like generic AI content.",
        response: `Point to the research references, the ${input.prospectIndustry ?? input.research.industry} context, and the prospect-specific brief to show the difference.`,
        coachingNote: "Win on specificity, not on the word AI."
      }
    ],
    qualityNotes: ["Fallback objections used because the generation bridge is not yet connected."]
  };
}

async function generateWithAnthropic(input: ObjectionInput): Promise<ObjectionPlan | null> {
  const apiKey = process.env.ANTHROPIC_API_KEY?.trim();
  if (!apiKey) {
    return null;
  }

  const prompt = [
    "Write the top five objections, responses, and coaching notes for a DealForge pre-sales package.",
    `Prospect: ${input.prospectName}`,
    `Industry: ${input.prospectIndustry ?? input.research.industry}`,
    `Use case: ${input.useCase ?? "Unspecified"}`,
    `Research: ${input.research.companyDescription}`,
    `Brief: ${input.brief.markdown}`,
    "Requirements:",
    "- Return Markdown with one objection per bullet.",
    "- Each item must include objection, response, and coaching note.",
    "- Keep responses concise and prospect-specific.",
    "- Avoid generic AI sales copy."
  ].join("\n");

  try {
    const response = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": apiKey,
        "anthropic-version": "2023-06-01"
      },
      body: JSON.stringify({
        model: process.env.ANTHROPIC_MODEL ?? "claude-sonnet-4-20250514",
        max_tokens: 1000,
        temperature: 0.3,
        messages: [
          {
            role: "user",
            content: [{ type: "text", text: prompt }]
          }
        ]
      })
    });

    if (!response.ok) {
      return null;
    }

    const payload = (await response.json()) as { content?: Array<{ type?: string; text?: string }> };
    const text = payload.content
      ?.map((part) => (part.type === "text" ? part.text ?? "" : ""))
      .join("\n")
      .trim();

    if (!text) {
      return null;
    }

    return {
      source: "anthropic",
      scripts: [
        {
          objection: "Generated via Anthropic",
          response: text.slice(0, 280),
          coachingNote: "Replace this placeholder parser with structured output once the generation schema is finalized."
        }
      ],
      qualityNotes: ["Anthropic path returned free-form text; structure parsing comes later."]
    };
  } catch {
    return null;
  }
}

export async function generateObjectionPlan(input: ObjectionInput): Promise<ObjectionPlan> {
  return (await generateWithAnthropic(input)) ?? fallbackObjections(input);
}

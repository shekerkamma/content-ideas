import type { ProspectResearch } from "./search";

export type StrategyBriefResult = {
  markdown: string;
  source: "anthropic" | "fallback";
  qualityNotes: string[];
};

export type StrategyBriefInput = {
  prospectName: string;
  prospectIndustry?: string;
  useCase?: string;
  research: ProspectResearch;
};

function fallbackBrief(input: StrategyBriefInput): StrategyBriefResult {
  const markdown = `# AI Opportunity Brief\n\n## Prospect\n${input.prospectName}\n\n## Working thesis\n- Industry: ${input.prospectIndustry ?? input.research.industry}\n- Use case: ${input.useCase ?? "Unspecified"}\n- Research confidence: ${input.research.confidence}\n\n## Context\n${input.research.companyDescription}\n\n## Signals\n${input.research.aiSignals.map((signal) => `- ${signal}`).join("\n")}\n\n## Next step\nRefine this brief with live Claude output and any internal customer knowledge.`;

  return {
    markdown,
    source: "fallback",
    qualityNotes: ["Fallback brief used because Anthropic API credentials were not available."]
  };
}

function extractText(payload: { content?: Array<{ type?: string; text?: string }> }) {
  return payload.content
    ?.map((part) => (part.type === "text" ? part.text ?? "" : ""))
    .join("\n")
    .trim();
}

export async function generateStrategyBrief(input: StrategyBriefInput): Promise<StrategyBriefResult> {
  const apiKey = process.env.ANTHROPIC_API_KEY?.trim();
  if (!apiKey) {
    return fallbackBrief(input);
  }

  const prompt = [
    "Write a concise one-page AI opportunity brief in Markdown.",
    `Prospect: ${input.prospectName}`,
    `Industry: ${input.prospectIndustry ?? input.research.industry}`,
    `Use case: ${input.useCase ?? "Unspecified"}`,
    `Prospect description: ${input.research.companyDescription}`,
    `Recent news: ${input.research.recentNews.join(" | ")}`,
    `AI signals: ${input.research.aiSignals.join(" | ")}`,
    `Key people: ${input.research.keyPeople.join(" | ")}`,
    "Requirements:",
    "- Mention the prospect by name at least twice.",
    "- Ground the brief in the supplied research details.",
    "- Include a working thesis, value hypothesis, risks, and next steps.",
    "- Avoid generic AI strategy language."
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
        max_tokens: 1200,
        temperature: 0.4,
        messages: [
          {
            role: "user",
            content: [
              {
                type: "text",
                text: prompt
              }
            ]
          }
        ]
      })
    });

    if (!response.ok) {
      return fallbackBrief(input);
    }

    const payload = (await response.json()) as { content?: Array<{ type?: string; text?: string }> };
    const text = extractText(payload);
    if (!text) {
      return fallbackBrief(input);
    }

    const mentionCount = [input.prospectName, input.prospectIndustry ?? input.research.industry, input.useCase]
      .filter(Boolean)
      .reduce((count, term) => (term && text.includes(term) ? count + 1 : count), 0);

    const markdown = text.includes(input.prospectName) ? text : `# AI Opportunity Brief\n\n${text}`;

    return {
      markdown,
      source: "anthropic",
      qualityNotes: [
        mentionCount > 0 ? "Brief is grounded in the supplied account context." : "Brief should be checked for prospect specificity."
      ]
    };
  } catch {
    return fallbackBrief(input);
  }
}

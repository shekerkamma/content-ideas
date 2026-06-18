export type ProspectResearch = {
  companyName: string;
  companyDescription: string;
  industry: string;
  size: string;
  recentNews: string[];
  aiSignals: string[];
  keyPeople: string[];
  citations: Array<{
    title: string;
    url: string;
  }>;
  thinData: boolean;
  confidence: "low" | "medium" | "high";
  source: "exa" | "fallback";
};

type ExaResult = {
  title?: string;
  url?: string;
  summary?: string;
  text?: string;
  publishedDate?: string;
  author?: string;
  highlights?: string[];
  entities?: Array<{
    properties?: {
      description?: string;
      workforce?: { total?: number };
      financials?: {
        revenueAnnual?: number;
        fundingTotal?: number;
      };
    };
  }>;
};

type ExaResponse = {
  results?: ExaResult[];
};

function dedupe(values: string[]) {
  return [...new Set(values.filter(Boolean))];
}

function normalizeCompanySize(result: ExaResult) {
  const workforce = result.entities?.[0]?.properties?.workforce?.total;
  if (!workforce) {
    return "Unknown";
  }

  if (workforce < 50) return "1-49 employees";
  if (workforce < 200) return "50-199 employees";
  if (workforce < 1000) return "200-999 employees";
  return "1000+ employees";
}

function fallbackResearch(prospectName: string, prospectIndustry?: string, useCase?: string): ProspectResearch {
  const thinData = !prospectIndustry && !useCase;

  return {
    companyName: prospectName,
    companyDescription: `${prospectName} is the target account for a DealForge research pass. Public data is thin, so the pipeline should prompt manual validation.`,
    industry: prospectIndustry ?? "Unspecified",
    size: "Unknown",
    recentNews: ["No live news fetch yet - use this as a placeholder until Exa is connected."],
    aiSignals: useCase ? [`User-specified use case: ${useCase}`] : ["No strong AI signals captured yet."],
    keyPeople: ["No people identified yet."],
    citations: [],
    thinData,
    confidence: thinData ? "low" : "medium",
    source: "fallback"
  };
}

async function searchExa(query: string): Promise<ExaResponse | null> {
  const apiKey = process.env.EXA_API_KEY?.trim();
  if (!apiKey) {
    return null;
  }

  const response = await fetch("https://api.exa.ai/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": apiKey
    },
    body: JSON.stringify({
      query,
      numResults: 5,
      contents: {
        text: true,
        highlights: true,
        summary: true
      },
      type: "auto",
      category: "company"
    })
  });

  if (!response.ok) {
    return null;
  }

  return (await response.json()) as ExaResponse;
}

function deriveResearchFromResults(
  prospectName: string,
  prospectIndustry: string | undefined,
  useCase: string | undefined,
  results: ExaResult[]
): ProspectResearch {
  const first = results[0];
  const citations = dedupe(
    results
      .map((result) => (result.title && result.url ? { title: result.title, url: result.url } : null))
      .filter((entry): entry is { title: string; url: string } => entry !== null)
      .map((entry) => `${entry.title}::${entry.url}`)
  ).map((entry) => {
    const [title, url] = entry.split("::");
    return { title, url };
  });

  const recentNews = dedupe(
    results.map((result) => result.summary ?? result.highlights?.[0] ?? result.text ?? "").filter(Boolean)
  ).slice(0, 3);

  const aiSignals = dedupe(
    [
      useCase ? `Use case focus: ${useCase}` : null,
      prospectIndustry ? `Industry hint: ${prospectIndustry}` : null,
      first?.entities?.[0]?.properties?.financials?.fundingTotal
        ? "Funding signal suggests capacity for transformation"
        : null,
      first?.entities?.[0]?.properties?.financials?.revenueAnnual
        ? "Revenue profile indicates an enterprise-scale account"
        : null
    ].filter((signal): signal is string => signal !== null)
  );

  const keyPeople = dedupe(results.map((result) => result.author ?? "").filter(Boolean)).slice(0, 5);

  const description =
    first?.entities?.[0]?.properties?.description ??
    first?.summary ??
    first?.text ??
    `Public search results suggest ${prospectName} is active enough to warrant a tailored pre-sales brief.`;

  const thinData = !description || recentNews.length === 0;

  return {
    companyName: prospectName,
    companyDescription: description,
    industry: prospectIndustry ?? "Unspecified",
    size: normalizeCompanySize(first ?? {}),
    recentNews: recentNews.length > 0 ? recentNews : ["No recent news extracted from public results."],
    aiSignals: aiSignals.length > 0 ? aiSignals : ["No obvious AI signal surfaced in the initial search pass."],
    keyPeople: keyPeople.length > 0 ? keyPeople : ["No people identified yet."],
    citations,
    thinData,
    confidence: thinData ? "low" : "medium",
    source: "exa"
  };
}

export async function researchProspect(
  prospectName: string,
  prospectIndustry?: string,
  useCase?: string
): Promise<ProspectResearch> {
  const fallback = fallbackResearch(prospectName, prospectIndustry, useCase);
  const query = [
    prospectName,
    prospectIndustry ? `${prospectIndustry} company profile` : "company profile",
    useCase ? `${useCase} AI use case` : "technology initiatives",
    "recent news leadership funding website"
  ]
    .filter(Boolean)
    .join(" ");

  try {
    const response = await searchExa(query);
    const results = response?.results ?? [];
    if (results.length === 0) {
      return fallback;
    }

    return deriveResearchFromResults(prospectName, prospectIndustry, useCase, results);
  } catch {
    return fallback;
  }
}

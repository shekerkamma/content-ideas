import { useEffect } from "react";
import { CHAPTERS, type ChapterId } from "./chapters";
import {
  companies,
  competitors,
  execaction,
  execcompare,
  hostileQuestions,
  patterns,
  posture,
  pyramid,
  type Company,
} from "./data";

type JsonSchema = Record<string, unknown>;

interface WebMCPTool {
  name: string;
  title: string;
  description: string;
  inputSchema: JsonSchema;
  annotations: {
    readOnlyHint: boolean;
    untrustedContentHint: boolean;
  };
  execute: (
    input: Record<string, unknown>,
    context: { signal?: AbortSignal },
  ) => Promise<unknown> | unknown;
}

interface ModelContext {
  registerTool: (tool: WebMCPTool, options: { signal: AbortSignal }) => Promise<unknown> | unknown;
}

type WebMCPDocument = Document & { modelContext?: ModelContext };
type WebMCPNavigator = Navigator & { modelContext?: ModelContext };

interface WebMCPToolsProps {
  onNavigateSection: (section: ChapterId) => void;
  onShowCompany: (companyId: string) => void;
  onShowQuestion: (questionIndex: number) => void;
}

function getModelContext(): ModelContext | null {
  if (typeof document !== "undefined") {
    const context = (document as WebMCPDocument).modelContext;
    if (context?.registerTool) return context;
  }

  if (typeof navigator !== "undefined") {
    const context = (navigator as WebMCPNavigator).modelContext;
    if (context?.registerTool) return context;
  }

  return null;
}

function assertNotAborted(signal?: AbortSignal) {
  if (signal?.aborted) {
    throw new DOMException("The WebMCP tool call was cancelled.", "AbortError");
  }
}

function requireString(input: Record<string, unknown>, key: string): string {
  const value = input[key];
  if (typeof value !== "string" || !value.trim()) {
    throw new Error(`\`${key}\` must be a non-empty string.`);
  }
  return value.trim();
}

function getCompany(value: string) {
  const normalized = value.toLocaleLowerCase();
  const company = companies.find(
    (candidate) =>
      candidate.id.toLocaleLowerCase() === normalized ||
      candidate.name.toLocaleLowerCase() === normalized,
  );

  if (!company) {
    throw new Error(
      `Unknown company \`${value}\`. Choose one of: ${companies.map((candidate) => candidate.name).join(", ")}.`,
    );
  }

  return company;
}

function getCompanySnapshot(company: Company) {
  const ranking = competitors.find((candidate) => candidate.id === company.id);
  return {
    company: company.name,
    tier: company.tier,
    posture: company.posture,
    facts: {
      founded: company.founded,
      headquarters: company.hq,
      status: company.status,
      value: company.value,
    },
    sells: company.sells,
    strategic_read: company.read,
    open_gaps: company.gaps,
    evidence: company.evidence,
    ranking: ranking
      ? {
          score: ranking.score,
          execution: ranking.execution,
          access: ranking.access,
          leverage: ranking.leverage,
          blocker: ranking.blocker,
          blocker_reason: ranking.blocker_why,
          evidence: ranking.ev,
        }
      : null,
  };
}

const PATTERN_BY_COMPANY: Record<string, number> = {
  stradvision: 0,
  aptiv: 1,
  zf: 2,
  sterling: 2,
  drivebuddy: 3,
  starkenn: 3,
  bitsensing: 3,
  gahan: 4,
  netrasemi: 4,
};

const POSTURE_BY_COMPANY: Record<string, number> = {
  stradvision: 0,
  zf: 1,
  aptiv: 1,
  starkenn: 2,
  sterling: 2,
  gahan: 3,
  netrasemi: 3,
  bitsensing: 3,
  drivebuddy: 3,
};

function findExecutiveComparison(company: Company) {
  const aliases: Record<string, string> = {
    aptiv: "Aptiv",
    sterling: "Sterling",
  };
  const needle = aliases[company.id] ?? company.name;
  return execcompare.rows.find((row) => row[0].toLocaleLowerCase().includes(needle.toLocaleLowerCase()));
}

function createCompetitiveResponse(company: Company) {
  const pattern = patterns.rows[PATTERN_BY_COMPANY[company.id]];
  const mode = posture.modes[POSTURE_BY_COMPANY[company.id]];
  const comparison = findExecutiveComparison(company);
  const ranking = competitors.find((candidate) => candidate.id === company.id);

  return {
    company: company.name,
    relationship: pattern?.[0] ?? "UNCLASSIFIED",
    current_action: comparison?.[5] ?? pattern?.[4] ?? company.read,
    recommended_move: pattern?.[4] ?? company.read,
    strategic_posture: mode
      ? {
          verb: mode[0],
          applies_to: mode[1],
          rationale: mode[3],
          proof_boundary: mode[4],
        }
      : null,
    score: ranking?.score ?? null,
    blocker_reason: ranking?.blocker_why ?? null,
    open_gaps: company.gaps,
    evidence: [company.evidence, ranking?.ev, pattern?.[6]].filter(Boolean),
  };
}

function createExecutiveBrief(topN: number) {
  const ranking = [...competitors]
    .sort((left, right) => right.score - left.score)
    .slice(0, topN)
    .map((competitor, index) => ({
      rank: index + 1,
      company: competitor.name,
      score: competitor.score,
      blocker_reason: competitor.blocker_why,
      evidence: competitor.ev,
    }));

  return {
    governing_thought: pyramid.governing_thought,
    supports: pyramid.supports,
    top_threats: ranking,
    strategic_choice: posture.choice,
    posture: posture.modes.map(([verb, who, , why, boundary]) => ({ verb, who, why, boundary })),
    ninety_day_decisions: execaction.rows.map(([number, decision, action, proofGate, owner]) => ({
      number,
      decision,
      action,
      proof_gate: proofGate,
      owner,
    })),
    do_not_fund: execaction.donotfund,
  };
}

interface EvidenceHit {
  evidence_id: string;
  source: "company_profile" | "ranking" | "strategic_pattern";
  company?: string;
  subject: string;
  summary: string;
}

function evidenceIds(value: string): string[] {
  return value.match(/EV-[A-Z]+-\d+/g) ?? [];
}

function createEvidenceIndex(): EvidenceHit[] {
  const hits: EvidenceHit[] = [];

  for (const company of companies) {
    for (const evidenceId of evidenceIds(company.evidence)) {
      hits.push({
        evidence_id: evidenceId,
        source: "company_profile",
        company: company.name,
        subject: company.sells,
        summary: company.read,
      });
    }
  }

  for (const competitor of competitors) {
    for (const evidenceId of evidenceIds(competitor.ev)) {
      hits.push({
        evidence_id: evidenceId,
        source: "ranking",
        company: competitor.name,
        subject: `Score ${competitor.score.toFixed(1)} · blocker ${competitor.blocker}`,
        summary: competitor.blocker_why,
      });
    }
  }

  for (const [relationship, definition, companiesInPattern, , move, , evidence] of patterns.rows) {
    for (const evidenceId of evidenceIds(evidence)) {
      hits.push({
        evidence_id: evidenceId,
        source: "strategic_pattern",
        company: companiesInPattern,
        subject: `${relationship} · ${definition}`,
        summary: move,
      });
    }
  }

  const seen = new Set<string>();
  return hits.filter((hit) => {
    const key = `${hit.evidence_id}|${hit.source}|${hit.company ?? ""}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function executiveBriefMarkdown(brief: ReturnType<typeof createExecutiveBrief>): string {
  const threats = brief.top_threats
    .map((threat) => `${threat.rank}. **${threat.company}** — ${threat.score.toFixed(1)}; ${threat.blocker_reason}`)
    .join("\n");
  const decisions = brief.ninety_day_decisions
    .map((decision) => `- **${decision.decision}** (${decision.owner}): ${decision.action}\n  - Proof gate: ${decision.proof_gate}`)
    .join("\n");

  return `# DeepGrid India ADAS Competitive Brief\n\n## Governing thought\n\n${brief.governing_thought}\n\n## Top threats\n\n${threats}\n\n## Strategic choice\n\n${brief.strategic_choice}\n\n## 90-day decisions\n\n${decisions}\n\n## Do not fund\n\n${brief.do_not_fund}`;
}

function competitorResponseMarkdown(response: ReturnType<typeof createCompetitiveResponse>): string {
  return `# ${response.company} — Competitive Response\n\n- **Relationship:** ${response.relationship}\n- **Current action:** ${response.current_action}\n- **Recommended move:** ${response.recommended_move}\n- **Posture:** ${response.strategic_posture?.verb ?? "Unclassified"}\n- **Proof boundary:** ${response.strategic_posture?.proof_boundary ?? "No boundary recorded"}\n- **Score:** ${response.score ?? "n/a"}\n\n## Open gaps\n\n${response.open_gaps.map((gap) => `- ${gap}`).join("\n")}\n\n## Evidence\n\n${response.evidence.map((item) => `- ${item}`).join("\n")}`;
}

function rankingMarkdown(): string {
  const rows = [...competitors]
    .sort((left, right) => right.score - left.score)
    .map((competitor, index) => `| ${index + 1} | ${competitor.name} | ${competitor.score.toFixed(1)} | ${competitor.blocker_why} |`)
    .join("\n");
  return `# DeepGrid Competitor Ranking\n\n| Rank | Company | Score | Blocker reason |\n|---:|---|---:|---|\n${rows}`;
}

export function WebMCPTools({
  onNavigateSection,
  onShowCompany,
  onShowQuestion,
}: WebMCPToolsProps) {
  useEffect(() => {
    const modelContext = getModelContext();
    if (!modelContext) return;

    const controller = new AbortController();
    const companyNames = companies.map((company) => company.name);
    const sectionIds = CHAPTERS.map((chapter) => chapter.id);

    const tools: WebMCPTool[] = [
      {
        name: "navigate_dossier_section",
        title: "Navigate the DeepGrid dossier",
        description: "Show one chapter of the DeepGrid India ADAS competitor dossier in the page.",
        inputSchema: {
          type: "object",
          properties: {
            section: {
              type: "string",
              enum: sectionIds,
              description: "Dossier chapter to show.",
            },
          },
          required: ["section"],
          additionalProperties: false,
        },
        annotations: { readOnlyHint: true, untrustedContentHint: false },
        execute(input, { signal }) {
          assertNotAborted(signal);
          const section = requireString(input, "section") as ChapterId;
          if (!sectionIds.includes(section)) {
            throw new Error(`Unknown section \`${section}\`. Choose one of: ${sectionIds.join(", ")}.`);
          }
          onNavigateSection(section);
          return {
            ok: true,
            section,
            label: CHAPTERS.find((chapter) => chapter.id === section)?.label,
          };
        },
      },
      {
        name: "show_competitor",
        title: "Show a competitor profile",
        description: "Open a company profile and return its evidence-backed facts, strategic read, and open gaps.",
        inputSchema: {
          type: "object",
          properties: {
            company: {
              type: "string",
              enum: companyNames,
              description: "Competitor name to show.",
            },
          },
          required: ["company"],
          additionalProperties: false,
        },
        annotations: { readOnlyHint: true, untrustedContentHint: false },
        execute(input, { signal }) {
          assertNotAborted(signal);
          const company = getCompany(requireString(input, "company"));
          onShowCompany(company.id);
          onNavigateSection("contest");
          return {
            ok: true,
            company: company.name,
            tier: company.tier,
            posture: company.posture,
            facts: {
              founded: company.founded,
              headquarters: company.hq,
              status: company.status,
              value: company.value,
            },
            sells: company.sells,
            ai: company.ai.map(([capability, detail]) => ({ capability, detail })),
            details: company.detail.map(([topic, detail]) => ({ topic, detail })),
            open_gaps: company.gaps,
            strategic_read: company.read,
            evidence: company.evidence,
          };
        },
      },
      {
        name: "show_hostile_question",
        title: "Show a hostile diligence question",
        description: "Open one appendix diligence question and return the dossier's answer.",
        inputSchema: {
          type: "object",
          properties: {
            question_number: {
              type: "integer",
              minimum: 1,
              maximum: hostileQuestions.length,
              description: `Question number from 1 to ${hostileQuestions.length}.`,
            },
          },
          required: ["question_number"],
          additionalProperties: false,
        },
        annotations: { readOnlyHint: true, untrustedContentHint: false },
        execute(input, { signal }) {
          assertNotAborted(signal);
          const questionNumber = input.question_number;
          if (
            typeof questionNumber !== "number" ||
            !Number.isInteger(questionNumber) ||
            questionNumber < 1 ||
            questionNumber > hostileQuestions.length
          ) {
            throw new Error(`\`question_number\` must be an integer from 1 to ${hostileQuestions.length}.`);
          }
          const questionIndex = questionNumber - 1;
          const [question, answer] = hostileQuestions[questionIndex];
          onShowQuestion(questionIndex);
          onNavigateSection("appendix");
          return { ok: true, question_number: questionNumber, question, answer };
        },
      },
      {
        name: "get_competitor_ranking",
        title: "Get the competitor ranking",
        description: "Show the ranking chapter and return competitors ordered by execution, access, and leverage score.",
        inputSchema: {
          type: "object",
          properties: {
            limit: {
              type: "integer",
              minimum: 1,
              maximum: competitors.length,
              description: `Maximum rows to return. Defaults to all ${competitors.length}.`,
            },
          },
          additionalProperties: false,
        },
        annotations: { readOnlyHint: true, untrustedContentHint: false },
        execute(input, { signal }) {
          assertNotAborted(signal);
          const limit = input.limit ?? competitors.length;
          if (
            typeof limit !== "number" ||
            !Number.isInteger(limit) ||
            limit < 1 ||
            limit > competitors.length
          ) {
            throw new Error(`\`limit\` must be an integer from 1 to ${competitors.length}.`);
          }
          onNavigateSection("ranking");
          return {
            ok: true,
            ranking: [...competitors]
              .sort((left, right) => right.score - left.score)
              .slice(0, limit)
              .map((competitor, index) => ({
                rank: index + 1,
                company: competitor.name,
                score: competitor.score,
                blocker: competitor.blocker,
                blocker_reason: competitor.blocker_why,
                execution: competitor.execution,
                access: competitor.access,
                leverage: competitor.leverage,
                evidence: competitor.ev,
              })),
          };
        },
      },
      {
        name: "compare_competitors",
        title: "Compare two competitors",
        description: "Compare two dossier companies across profile facts, strategic posture, ranking score, gaps, and evidence.",
        inputSchema: {
          type: "object",
          properties: {
            companies: {
              type: "array",
              minItems: 2,
              maxItems: 2,
              items: { type: "string", enum: companyNames },
              description: "Exactly two distinct competitor names to compare.",
            },
          },
          required: ["companies"],
          additionalProperties: false,
        },
        annotations: { readOnlyHint: true, untrustedContentHint: false },
        execute(input, { signal }) {
          assertNotAborted(signal);
          const values = input.companies;
          if (!Array.isArray(values) || values.length !== 2 || values.some((value) => typeof value !== "string")) {
            throw new Error("`companies` must contain exactly two competitor names.");
          }
          const selected = values.map((value) => getCompany(value));
          if (selected[0].id === selected[1].id) {
            throw new Error("Choose two distinct competitors.");
          }
          onShowCompany(selected[0].id);
          onNavigateSection("contest");
          const snapshots = selected.map(getCompanySnapshot);
          const scored = snapshots.filter((snapshot) => snapshot.ranking);
          const higherScore = scored.length === 2
            ? [...scored].sort((left, right) => (right.ranking?.score ?? 0) - (left.ranking?.score ?? 0))[0].company
            : null;
          return {
            ok: true,
            comparison: snapshots,
            summary: {
              higher_ranked_threat: higherScore,
              same_tier: snapshots[0].tier === snapshots[1].tier,
              same_evidence_posture: snapshots[0].posture === snapshots[1].posture,
            },
          };
        },
      },
      {
        name: "find_evidence",
        title: "Find dossier evidence",
        description: "Find bounded evidence references by evidence ID, company, relationship, or keyword.",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              minLength: 2,
              maxLength: 100,
              description: "Evidence ID, company name, relationship, or keyword to find.",
            },
            limit: {
              type: "integer",
              minimum: 1,
              maximum: 10,
              description: "Maximum matches to return. Defaults to 5.",
            },
          },
          required: ["query"],
          additionalProperties: false,
        },
        annotations: { readOnlyHint: true, untrustedContentHint: false },
        execute(input, { signal }) {
          assertNotAborted(signal);
          const query = requireString(input, "query");
          if (query.length < 2 || query.length > 100) {
            throw new Error("`query` must contain 2 to 100 characters.");
          }
          const limit = input.limit ?? 5;
          if (typeof limit !== "number" || !Number.isInteger(limit) || limit < 1 || limit > 10) {
            throw new Error("`limit` must be an integer from 1 to 10.");
          }
          const normalized = query.toLocaleLowerCase();
          const matches = createEvidenceIndex()
            .filter((hit) =>
              [hit.evidence_id, hit.source, hit.company, hit.subject, hit.summary]
                .filter(Boolean)
                .join(" ")
                .toLocaleLowerCase()
                .includes(normalized),
            )
            .slice(0, limit);
          onNavigateSection("field");
          return {
            ok: true,
            match_count: matches.length,
            matches,
            guidance: matches.length === 0
              ? "No indexed match. Retry with an evidence ID prefix such as EV-SV, a company name, or a relationship such as gatekeeper."
              : undefined,
          };
        },
      },
      {
        name: "build_executive_brief",
        title: "Build an executive competitive brief",
        description: "Return the dossier verdict, top threats, strategic posture, 90-day decisions, proof gates, and do-not-fund boundary.",
        inputSchema: {
          type: "object",
          properties: {
            top_n: {
              type: "integer",
              minimum: 1,
              maximum: 5,
              description: "Number of ranked threats to include. Defaults to 3.",
            },
          },
          additionalProperties: false,
        },
        annotations: { readOnlyHint: true, untrustedContentHint: false },
        execute(input, { signal }) {
          assertNotAborted(signal);
          const topN = input.top_n ?? 3;
          if (typeof topN !== "number" || !Number.isInteger(topN) || topN < 1 || topN > 5) {
            throw new Error("`top_n` must be an integer from 1 to 5.");
          }
          onNavigateSection("verdict");
          return { ok: true, brief: createExecutiveBrief(topN) };
        },
      },
      {
        name: "recommend_competitive_response",
        title: "Recommend a competitive response",
        description: "Return the dossier's sourced relationship, posture, move, proof boundary, gaps, and evidence for one company.",
        inputSchema: {
          type: "object",
          properties: {
            company: {
              type: "string",
              enum: companyNames,
              description: "Competitor name for which to prepare a response.",
            },
          },
          required: ["company"],
          additionalProperties: false,
        },
        annotations: { readOnlyHint: true, untrustedContentHint: false },
        execute(input, { signal }) {
          assertNotAborted(signal);
          const company = getCompany(requireString(input, "company"));
          onShowCompany(company.id);
          onNavigateSection("contest");
          return { ok: true, response: createCompetitiveResponse(company) };
        },
      },
      {
        name: "export_analysis",
        title: "Export a shareable analysis",
        description: "Prepare an executive, competitor-response, or ranking analysis as Markdown or structured JSON.",
        inputSchema: {
          type: "object",
          properties: {
            format: {
              type: "string",
              enum: ["markdown", "json"],
              description: "Output format for the prepared analysis.",
            },
            scope: {
              type: "string",
              enum: ["executive", "competitor", "ranking"],
              description: "Analysis scope. Defaults to executive.",
            },
            company: {
              type: "string",
              enum: companyNames,
              description: "Required when scope is competitor.",
            },
          },
          required: ["format"],
          additionalProperties: false,
        },
        annotations: { readOnlyHint: true, untrustedContentHint: false },
        execute(input, { signal }) {
          assertNotAborted(signal);
          const format = requireString(input, "format");
          const scope = input.scope ?? "executive";
          if (!(["markdown", "json"] as unknown[]).includes(format)) {
            throw new Error("`format` must be `markdown` or `json`.");
          }
          if (typeof scope !== "string" || !["executive", "competitor", "ranking"].includes(scope)) {
            throw new Error("`scope` must be `executive`, `competitor`, or `ranking`.");
          }

          let content: unknown;
          if (scope === "competitor") {
            const companyValue = requireString(input, "company");
            const company = getCompany(companyValue);
            const response = createCompetitiveResponse(company);
            onShowCompany(company.id);
            onNavigateSection("contest");
            content = format === "markdown" ? competitorResponseMarkdown(response) : response;
          } else if (scope === "ranking") {
            const ranking = [...competitors]
              .sort((left, right) => right.score - left.score)
              .map((competitor, index) => ({ rank: index + 1, ...competitor }));
            onNavigateSection("ranking");
            content = format === "markdown" ? rankingMarkdown() : ranking;
          } else {
            const brief = createExecutiveBrief(3);
            onNavigateSection("verdict");
            content = format === "markdown" ? executiveBriefMarkdown(brief) : brief;
          }

          return { ok: true, format, scope, content };
        },
      },
    ];

    const register = async () => {
      await Promise.all(
        tools.map((tool) =>
          modelContext.registerTool(tool, { signal: controller.signal }),
        ),
      );
    };

    void register().catch((error) => {
      if (!controller.signal.aborted) {
        console.error("Unable to register WebMCP tools", error);
      }
    });

    return () => controller.abort();
  }, [onNavigateSection, onShowCompany, onShowQuestion]);

  return null;
}

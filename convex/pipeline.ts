import { internal } from "./_generated/api";
import { internalMutation, query } from "./_generated/server";
import { v } from "convex/values";

const STAGES = ["research", "brief", "deck", "objections", "package"] as const;

type Stage = (typeof STAGES)[number];

function stageQualityScore(stage: Stage, thinData: boolean) {
  if (stage === "research") {
    return thinData ? 2 : 4;
  }

  if (stage === "package") {
    return thinData ? 3 : 5;
  }

  return thinData ? 3 : 4;
}

function buildStageOutput(stage: Stage, deal: {
  prospectName: string;
  prospectIndustry?: string;
  useCase?: string;
}, previousOutputs: Partial<Record<Stage, unknown>>) {
  const thinData = !deal.prospectIndustry && !deal.useCase;

  switch (stage) {
    case "research":
      return {
        stage,
        prospectName: deal.prospectName,
        prospectIndustry: deal.prospectIndustry ?? "unclassified",
        useCase: deal.useCase ?? "unspecified",
        thinData,
        signals: [
          "Public account signal review pending real research integration",
          "Industry and use-case hints captured from intake"
        ],
        confidence: thinData ? "low" : "medium"
      };
    case "brief":
      return {
        stage,
        markdown: `# AI Opportunity Brief\n\n${deal.prospectName} is a promising fit for the DealForge pipeline.\n\n## Working thesis\n- Industry: ${deal.prospectIndustry ?? "unknown"}\n- Use case: ${deal.useCase ?? "unspecified"}\n- Research status: ${thinData ? "thin public data" : "enough context to personalize"}\n\n## Next step\nRefine this with live research and Claude generation.`,
        references: {
          research: previousOutputs.research ?? null
        }
      };
    case "deck":
      return {
        stage,
        slides: [
          { title: "Cover", bullets: [deal.prospectName, deal.useCase ?? "AI opportunity"] },
          { title: "Prospect context", bullets: ["Research summary placeholder", "Current pain points"] },
          { title: "Opportunity", bullets: ["AI use-case framing", "Expected ROI"] },
          { title: "Execution", bullets: ["Implementation approach", "Timeline"] },
          { title: "Next steps", bullets: ["Review the package", "Approve follow-up"] }
        ]
      };
    case "objections":
      return {
        stage,
        objections: [
          {
            objection: "We already have a process for this.",
            response: "Show how the package reduces manual prep time and increases consistency."
          },
          {
            objection: "We are not ready to invest in AI.",
            response: "Position the output as a low-risk validation artifact, not a full platform commitment."
          },
          {
            objection: "The public data is thin.",
            response: "Call out the gap explicitly and suggest what the user should add before sending."
          }
        ]
      };
    case "package":
      return {
        stage,
        ready: true,
        artifacts: ["brief", "deck", "objections"],
        notes: ["Package assembly scaffold complete", "File generation and zip export come in a later task"]
      };
  }

  const exhaustiveCheck: never = stage;
  throw new Error(`Unhandled stage: ${exhaustiveCheck}`);
}

export const startDealPipeline = internalMutation({
  args: {
    dealId: v.id("deals")
  },
  handler: async (ctx, args) => {
    const deal = await ctx.db.get(args.dealId);
    if (!deal) {
      return null;
    }

    await ctx.db.patch(args.dealId, {
      status: "running",
      pipelineProgress: 0
    });

    await ctx.scheduler.runAfter(0, internal.stages.research.requestResearchStage, {
      dealId: args.dealId
    });

    return null;
  }
});

export const advanceDealPipeline = internalMutation({
  args: {
    dealId: v.id("deals"),
    stageIndex: v.number()
  },
  handler: async (ctx, args) => {
    const deal = await ctx.db.get(args.dealId);
    if (!deal) {
      return null;
    }

    const stage = STAGES[args.stageIndex];
    if (!stage) {
      await ctx.db.patch(args.dealId, {
        status: "completed",
        pipelineProgress: STAGES.length,
        completedAt: Date.now()
      });
      return null;
    }

    const previousOutputs = await ctx.db
      .query("stageOutputs")
      .withIndex("by_deal", (q) => q.eq("dealId", args.dealId))
      .collect();

    const previousByStage = previousOutputs.reduce((acc, output) => {
      acc[output.stage as Stage] = output.output;
      return acc;
    }, {} as Partial<Record<Stage, unknown>>);

    const now = Date.now();
    const payload = buildStageOutput(stage, deal, previousByStage);
    const thinData = !deal.prospectIndustry && !deal.useCase;
    const qualityScore = stageQualityScore(stage, thinData);
    const existingOutput = previousOutputs.find((output) => output.stage === stage);

    if (existingOutput) {
      await ctx.db.delete(existingOutput._id);
    }

    const outputId = await ctx.db.insert("stageOutputs", {
      dealId: args.dealId,
      stage,
      status: "running",
      output: payload,
      qualityScore,
      startedAt: now
    });

    await ctx.db.patch(outputId, {
      status: "completed",
      output: payload,
      qualityScore,
      completedAt: now
    });

    if (stage === "package") {
      await ctx.db.patch(args.dealId, {
        pipelineProgress: args.stageIndex + 1,
        status: "completed",
        completedAt: now
      });
    } else {
      await ctx.db.patch(args.dealId, {
        pipelineProgress: args.stageIndex + 1,
        status: "running"
      });
    }

    if (stage !== "package") {
      await ctx.scheduler.runAfter(0, internal.pipeline.advanceDealPipeline, {
        dealId: args.dealId,
        stageIndex: args.stageIndex + 1
      });
    }

    return null;
  }
});

export const retryDealStage = internalMutation({
  args: {
    dealId: v.id("deals"),
    stageIndex: v.number()
  },
  handler: async (ctx, args) => {
    const deal = await ctx.db.get(args.dealId);
    if (!deal) {
      return null;
    }

    await ctx.db.patch(args.dealId, {
      status: "running",
      pipelineProgress: Math.max(0, Math.min(args.stageIndex, STAGES.length - 1))
    });

    await ctx.scheduler.runAfter(0, internal.pipeline.advanceDealPipeline, {
      dealId: args.dealId,
      stageIndex: args.stageIndex
    });

    return null;
  }
});

export const getDealPipeline = query({
  args: {
    dealId: v.id("deals")
  },
  handler: async (ctx, args) => {
    const deal = await ctx.db.get(args.dealId);
    if (!deal) {
      return null;
    }

    const stageOutputs = await ctx.db
      .query("stageOutputs")
      .withIndex("by_deal", (q) => q.eq("dealId", args.dealId))
      .collect();

    return {
      deal,
      stageOutputs,
      nextStage:
        deal.status === "completed" ? null : STAGES[Math.min(deal.pipelineProgress, STAGES.length - 1)]
    };
  }
});

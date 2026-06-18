import { internal } from "../_generated/api";
import { internalAction, internalMutation } from "../_generated/server";
import { v } from "convex/values";
import { generateStrategyBrief } from "../../lib/ai";

export const runBriefStage = internalAction({
  args: {
    dealId: v.id("deals"),
    prospectName: v.string(),
    prospectIndustry: v.optional(v.string()),
    useCase: v.optional(v.string()),
    research: v.object({
      companyName: v.string(),
      companyDescription: v.string(),
      industry: v.string(),
      size: v.string(),
      recentNews: v.array(v.string()),
      aiSignals: v.array(v.string()),
      keyPeople: v.array(v.string()),
      citations: v.array(
        v.object({
          title: v.string(),
          url: v.string()
        })
      ),
      thinData: v.boolean(),
      confidence: v.union(v.literal("low"), v.literal("medium"), v.literal("high")),
      source: v.union(v.literal("exa"), v.literal("fallback"))
    })
  },
  handler: async (ctx, args) => {
    const brief = await generateStrategyBrief({
      prospectName: args.prospectName,
      prospectIndustry: args.prospectIndustry,
      useCase: args.useCase,
      research: args.research
    });

    await ctx.runMutation(internal.stages.brief.saveBriefStage, {
      dealId: args.dealId,
      prospectName: args.prospectName,
      prospectIndustry: args.prospectIndustry,
      useCase: args.useCase,
      research: args.research,
      brief
    });

    return null;
  }
});

export const saveBriefStage = internalMutation({
  args: {
    dealId: v.id("deals"),
    prospectName: v.string(),
    prospectIndustry: v.optional(v.string()),
    useCase: v.optional(v.string()),
    research: v.object({
      companyName: v.string(),
      companyDescription: v.string(),
      industry: v.string(),
      size: v.string(),
      recentNews: v.array(v.string()),
      aiSignals: v.array(v.string()),
      keyPeople: v.array(v.string()),
      citations: v.array(
        v.object({
          title: v.string(),
          url: v.string()
        })
      ),
      thinData: v.boolean(),
      confidence: v.union(v.literal("low"), v.literal("medium"), v.literal("high")),
      source: v.union(v.literal("exa"), v.literal("fallback"))
    }),
    brief: v.object({
      markdown: v.string(),
      source: v.union(v.literal("anthropic"), v.literal("fallback")),
      qualityNotes: v.array(v.string())
    })
  },
  handler: async (ctx, args) => {
    const existingOutputs = await ctx.db
      .query("stageOutputs")
      .withIndex("by_deal", (q) => q.eq("dealId", args.dealId))
      .collect();
    const existingBrief = existingOutputs.find((output) => output.stage === "brief");
    const now = Date.now();
    const qualityScore =
      args.brief.markdown.includes(args.prospectName) &&
      (args.prospectIndustry ? args.brief.markdown.includes(args.prospectIndustry) : true)
        ? args.research.thinData
          ? 3
          : 4
        : 2;

    if (existingBrief) {
      await ctx.db.delete(existingBrief._id);
    }

    await ctx.db.insert("stageOutputs", {
      dealId: args.dealId,
      stage: "brief",
      status: "completed",
      output: {
        ...args.brief,
        prospectName: args.prospectName,
        prospectIndustry: args.prospectIndustry,
        useCase: args.useCase,
        research: args.research
      },
      qualityScore,
      startedAt: now,
      completedAt: now
    });

    await ctx.db.patch(args.dealId, {
      status: "running",
      pipelineProgress: 2
    });

    await ctx.scheduler.runAfter(0, internal.stages.deck.runDeckStage, {
      dealId: args.dealId,
      prospectName: args.prospectName,
      prospectIndustry: args.prospectIndustry,
      useCase: args.useCase,
      research: args.research,
      brief: args.brief
    });

    return null;
  }
});

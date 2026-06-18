import { internal } from "../_generated/api";
import { internalAction, internalMutation } from "../_generated/server";
import { v } from "convex/values";
import { researchProspect } from "../../lib/search";

export const requestResearchStage = internalMutation({
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

    await ctx.scheduler.runAfter(0, internal.stages.research.runResearchStage, {
      dealId: args.dealId,
      prospectName: deal.prospectName,
      prospectIndustry: deal.prospectIndustry,
      useCase: deal.useCase
    });

    return null;
  }
});

export const runResearchStage = internalAction({
  args: {
    dealId: v.id("deals"),
    prospectName: v.string(),
    prospectIndustry: v.optional(v.string()),
    useCase: v.optional(v.string())
  },
  handler: async (ctx, args) => {
    const research = await researchProspect(args.prospectName, args.prospectIndustry, args.useCase);

    await ctx.runMutation(internal.stages.research.saveResearchStage, {
      dealId: args.dealId,
      prospectName: args.prospectName,
      prospectIndustry: args.prospectIndustry,
      useCase: args.useCase,
      research
    });

    return null;
  }
});

export const saveResearchStage = internalMutation({
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
    const existingOutputs = await ctx.db
      .query("stageOutputs")
      .withIndex("by_deal", (q) => q.eq("dealId", args.dealId))
      .collect();
    const existingResearch = existingOutputs.find((output) => output.stage === "research");
    const now = Date.now();
    const qualityScore = args.research.thinData ? 2 : 4;

    if (existingResearch) {
      await ctx.db.delete(existingResearch._id);
    }

    await ctx.db.insert("stageOutputs", {
      dealId: args.dealId,
      stage: "research",
      status: "completed",
      output: args.research,
      qualityScore,
      startedAt: now,
      completedAt: now
    });

    await ctx.db.patch(args.dealId, {
      status: "running",
      pipelineProgress: 1
    });

    await ctx.scheduler.runAfter(0, internal.stages.brief.runBriefStage, {
      dealId: args.dealId,
      prospectName: args.prospectName,
      prospectIndustry: args.prospectIndustry,
      useCase: args.useCase,
      research: args.research
    });

    return null;
  }
});

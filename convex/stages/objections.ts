import { internal } from "../_generated/api";
import { internalAction, internalMutation } from "../_generated/server";
import { v } from "convex/values";
import { generateObjectionPlan } from "../../lib/objections";

const researchShape = v.object({
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
});

const briefShape = v.object({
  markdown: v.string(),
  source: v.union(v.literal("anthropic"), v.literal("fallback")),
  qualityNotes: v.array(v.string())
});

export const runObjectionsStage = internalAction({
  args: {
    dealId: v.id("deals"),
    prospectName: v.string(),
    prospectIndustry: v.optional(v.string()),
    useCase: v.optional(v.string()),
    research: researchShape,
    brief: briefShape
  },
  handler: async (ctx, args) => {
    const objections = await generateObjectionPlan({
      prospectName: args.prospectName,
      prospectIndustry: args.prospectIndustry,
      useCase: args.useCase,
      research: args.research,
      brief: args.brief
    });

    await ctx.runMutation(internal.stages.objections.saveObjectionsStage, {
      dealId: args.dealId,
      prospectName: args.prospectName,
      prospectIndustry: args.prospectIndustry,
      useCase: args.useCase,
      research: args.research,
      brief: args.brief,
      objections
    });

    return null;
  }
});

export const saveObjectionsStage = internalMutation({
  args: {
    dealId: v.id("deals"),
    prospectName: v.string(),
    prospectIndustry: v.optional(v.string()),
    useCase: v.optional(v.string()),
    research: researchShape,
    brief: briefShape,
    objections: v.object({
      source: v.union(v.literal("anthropic"), v.literal("fallback")),
      scripts: v.array(
        v.object({
          objection: v.string(),
          response: v.string(),
          coachingNote: v.string()
        })
      ),
      qualityNotes: v.array(v.string())
    })
  },
  handler: async (ctx, args) => {
    const existingOutputs = await ctx.db
      .query("stageOutputs")
      .withIndex("by_deal", (q) => q.eq("dealId", args.dealId))
      .collect();
    const existingObjections = existingOutputs.find((output) => output.stage === "objections");
    const now = Date.now();

    if (existingObjections) {
      await ctx.db.delete(existingObjections._id);
    }

    await ctx.db.insert("stageOutputs", {
      dealId: args.dealId,
      stage: "objections",
      status: "completed",
      output: {
        ...args.objections,
        prospectName: args.prospectName,
        prospectIndustry: args.prospectIndustry,
        useCase: args.useCase,
        research: args.research,
        brief: args.brief
      },
      qualityScore: args.objections.scripts.length >= 5 ? 4 : 3,
      startedAt: now,
      completedAt: now
    });

    await ctx.db.patch(args.dealId, {
      status: "running",
      pipelineProgress: 4
    });

    await ctx.scheduler.runAfter(0, internal.stages.package.runPackageStage, {
      dealId: args.dealId
    });

    return null;
  }
});

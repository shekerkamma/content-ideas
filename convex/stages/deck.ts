import { internal } from "../_generated/api";
import { internalAction, internalMutation } from "../_generated/server";
import { v } from "convex/values";
import { buildDeckPlan } from "../../lib/pptx";

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

export const runDeckStage = internalAction({
  args: {
    dealId: v.id("deals"),
    prospectName: v.string(),
    prospectIndustry: v.optional(v.string()),
    useCase: v.optional(v.string()),
    research: researchShape,
    brief: briefShape
  },
  handler: async (ctx, args) => {
    const deck = buildDeckPlan({
      prospectName: args.prospectName,
      prospectIndustry: args.prospectIndustry,
      useCase: args.useCase,
      research: args.research,
      briefMarkdown: args.brief.markdown
    });

    await ctx.runMutation(internal.stages.deck.saveDeckStage, {
      dealId: args.dealId,
      prospectName: args.prospectName,
      prospectIndustry: args.prospectIndustry,
      useCase: args.useCase,
      research: args.research,
      brief: args.brief,
      deck
    });

    return null;
  }
});

export const saveDeckStage = internalMutation({
  args: {
    dealId: v.id("deals"),
    prospectName: v.string(),
    prospectIndustry: v.optional(v.string()),
    useCase: v.optional(v.string()),
    research: researchShape,
    brief: briefShape,
    deck: v.object({
      templatePath: v.string(),
      outputName: v.string(),
      slideCount: v.number(),
      slides: v.array(
        v.object({
          title: v.string(),
          subtitle: v.optional(v.string()),
          bullets: v.array(v.string()),
          notes: v.optional(v.string())
        })
      ),
      renderStatus: v.union(v.literal("scaffold"), v.literal("ready")),
      brand: v.object({
        primaryColor: v.string(),
        secondaryColor: v.string(),
        footerText: v.string()
      })
    })
  },
  handler: async (ctx, args) => {
    const existingOutputs = await ctx.db
      .query("stageOutputs")
      .withIndex("by_deal", (q) => q.eq("dealId", args.dealId))
      .collect();
    const existingDeck = existingOutputs.find((output) => output.stage === "deck");
    const now = Date.now();

    if (existingDeck) {
      await ctx.db.delete(existingDeck._id);
    }

    await ctx.db.insert("stageOutputs", {
      dealId: args.dealId,
      stage: "deck",
      status: "completed",
      output: {
        ...args.deck,
        prospectName: args.prospectName,
        prospectIndustry: args.prospectIndustry,
        useCase: args.useCase,
        research: args.research,
        brief: args.brief
      },
      qualityScore: args.deck.slideCount >= 10 ? 4 : 3,
      startedAt: now,
      completedAt: now
    });

    await ctx.db.patch(args.dealId, {
      status: "running",
      pipelineProgress: 3
    });

    await ctx.scheduler.runAfter(0, internal.stages.objections.runObjectionsStage, {
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

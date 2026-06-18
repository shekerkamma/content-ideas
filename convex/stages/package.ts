import { internal } from "../_generated/api";
import { internalMutation } from "../_generated/server";
import { v } from "convex/values";
import { buildPackageManifest } from "../../lib/package";

export const runPackageStage = internalMutation({
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

    const research = stageOutputs.find((output) => output.stage === "research")?.output;
    const brief = stageOutputs.find((output) => output.stage === "brief")?.output;
    const deck = stageOutputs.find((output) => output.stage === "deck")?.output;
    const objections = stageOutputs.find((output) => output.stage === "objections")?.output;

    if (!research || !brief || !deck || !objections) {
      return null;
    }

    const manifest = buildPackageManifest({
      dealId: String(args.dealId),
      prospectName: deal.prospectName,
      research,
      brief,
      deck,
      objections
    });

    const existingPackages = await ctx.db
      .query("packages")
      .withIndex("by_deal", (q) => q.eq("dealId", args.dealId))
      .collect();
    const existingPackage = existingPackages[0];
    const now = Date.now();

    if (existingPackage) {
      await ctx.db.delete(existingPackage._id);
    }

    await ctx.db.insert("packages", {
      dealId: args.dealId,
      briefUrl: manifest.briefUrl,
      deckUrl: manifest.deckUrl,
      objectionsUrl: manifest.objectionsUrl,
      zipUrl: manifest.zipUrl,
      createdAt: now
    });

    const existingStageOutputs = stageOutputs.find((output) => output.stage === "package");
    if (existingStageOutputs) {
      await ctx.db.delete(existingStageOutputs._id);
    }

    await ctx.db.insert("stageOutputs", {
      dealId: args.dealId,
      stage: "package",
      status: "completed",
      output: manifest,
      qualityScore: 4,
      startedAt: now,
      completedAt: now
    });

    await ctx.db.patch(args.dealId, {
      status: "completed",
      pipelineProgress: 5,
      completedAt: now
    });

    return null;
  }
});

import { v } from "convex/values";
import { mutation, query } from "./_generated/server";
import { internal } from "./_generated/api";

export const createDeal = mutation({
  args: {
    userId: v.id("users"),
    prospectName: v.string(),
    prospectIndustry: v.optional(v.string()),
    useCase: v.optional(v.string())
  },
  handler: async (ctx, args) => {
    const now = Date.now();
    const dealId = await ctx.db.insert("deals", {
      userId: args.userId,
      prospectName: args.prospectName,
      prospectIndustry: args.prospectIndustry,
      useCase: args.useCase,
      status: "pending",
      pipelineProgress: 0,
      createdAt: now
    });

    await ctx.scheduler.runAfter(0, internal.pipeline.startDealPipeline, {
      dealId
    });

    return { dealId, status: "pending" as const };
  }
});

export const listDeals = query({
  args: {
    userId: v.id("users")
  },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("deals")
      .withIndex("by_user", (q) => q.eq("userId", args.userId))
      .order("desc")
      .collect();
  }
});

export const getDealById = query({
  args: {
    dealId: v.id("deals")
  },
  handler: async (ctx, args) => {
    return await ctx.db.get(args.dealId);
  }
});

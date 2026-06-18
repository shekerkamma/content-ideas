import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

const defaultBrandSettings = {
  primaryColor: "#B91C1C",
  secondaryColor: "#151515",
  footerText: "Prepared with DealForge"
};

export const upsertCurrentUser = mutation({
  args: {
    clerkId: v.string(),
    name: v.string(),
    email: v.optional(v.string())
  },
  handler: async (ctx, args) => {
    const now = Date.now();
    const existing = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.clerkId))
      .unique();

    if (existing) {
      await ctx.db.patch(existing._id, {
        name: args.name,
        email: args.email,
        updatedAt: now
      });
      return existing._id;
    }

    return await ctx.db.insert("users", {
      clerkId: args.clerkId,
      name: args.name,
      email: args.email,
      brandSettings: defaultBrandSettings,
      plan: "free",
      createdAt: now,
      updatedAt: now
    });
  }
});

export const getCurrentUserByClerkId = query({
  args: {
    clerkId: v.string()
  },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.clerkId))
      .unique();
  }
});

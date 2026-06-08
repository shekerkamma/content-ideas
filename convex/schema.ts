import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    clerkId: v.string(),
    email: v.optional(v.string()),
    name: v.string(),
    company: v.optional(v.string()),
    brandSettings: v.object({
      logoUrl: v.optional(v.string()),
      primaryColor: v.string(),
      secondaryColor: v.string(),
      footerText: v.string()
    }),
    plan: v.union(v.literal("free"), v.literal("pro"), v.literal("team")),
    createdAt: v.number(),
    updatedAt: v.number()
  }).index("by_clerk_id", ["clerkId"]),
  deals: defineTable({
    userId: v.id("users"),
    prospectName: v.string(),
    prospectIndustry: v.optional(v.string()),
    useCase: v.optional(v.string()),
    status: v.union(v.literal("pending"), v.literal("running"), v.literal("completed"), v.literal("failed")),
    pipelineProgress: v.number(),
    createdAt: v.number(),
    completedAt: v.optional(v.number())
  }).index("by_user", ["userId"]),
  stageOutputs: defineTable({
    dealId: v.id("deals"),
    stage: v.union(
      v.literal("research"),
      v.literal("brief"),
      v.literal("deck"),
      v.literal("objections"),
      v.literal("package")
    ),
    status: v.union(v.literal("pending"), v.literal("running"), v.literal("completed"), v.literal("failed")),
    output: v.any(),
    qualityScore: v.optional(v.number()),
    startedAt: v.number(),
    completedAt: v.optional(v.number()),
    error: v.optional(v.string())
  }).index("by_deal", ["dealId"]),
  packages: defineTable({
    dealId: v.id("deals"),
    briefUrl: v.string(),
    deckUrl: v.string(),
    objectionsUrl: v.string(),
    zipUrl: v.string(),
    createdAt: v.number()
  }).index("by_deal", ["dealId"])
});

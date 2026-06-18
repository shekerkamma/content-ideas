# Product Roadmap — DealForge

## Build Philosophy

1. **Ship working increments.** Every phase ends with something demoable.
2. **Magic moment first.** The core pipeline (name → package) must work before any polish.
3. **Concierge validates code.** The manual pipeline already works. Code replaces manual steps one at a time.
4. **No speculative features.** Only build what the 5 concierge users asked for.

---

## Phase 1 — Foundation (Week 1)

> **Goal:** Project scaffolding, auth, and a working dashboard shell. User can sign up, see an empty dashboard, and navigate the app.

**Status:** 5/5 tasks complete

**Agent session prompt:** "Set up the DealForge project: Next.js app with Convex backend, Clerk auth, and a basic dashboard layout. Follow the PRD's repo structure. The dashboard should have an empty state that invites the user to create their first deal."

- [x] **TASK-001** — Initialize Next.js project with App Router and TypeScript
  Files: `package.json`, `tsconfig.json`, `next.config.ts`
  Notes: Use `npx create-next-app@latest` with TypeScript, App Router, Tailwind.

- [x] **TASK-002** — Set up Convex backend
  Files: `convex/schema.ts`, `convex/auth.config.ts`, `convex/_generated/`
  Notes: `npx convex dev` to initialize. Define User, Deal, StageOutput, Package tables per PRD data model.

- [x] **TASK-003** — Integrate Clerk authentication
  Files: `app/layout.tsx`, `middleware.ts`, `convex/auth.config.ts`
  Notes: Clerk + Convex integration. Google and GitHub social providers. Middleware protects all routes except landing.

- [x] **TASK-004** — Build dashboard layout and empty state
  Files: `app/dashboard/page.tsx`, `components/DealCard.tsx`, `components/EmptyState.tsx`
  Notes: Card grid layout for deals. Empty state: centered CTA "Enter a prospect name to generate your first deal package." Use Tailwind for styling.

- [x] **TASK-005** — User record creation on first sign-in
  Files: `convex/users.ts`
  Notes: Convex mutation triggered on first auth. Creates user record with default brandSettings and free plan.

---

## Phase 2 — Core Pipeline (Weeks 2-3)

> **Goal:** The magic moment works end-to-end. User enters a prospect name, pipeline runs 5 stages, outputs are generated and downloadable. This is the MVP.

**Status:** 9/9 tasks complete

**Agent session prompt:** "Build the DealForge pipeline: 5 stages that take a prospect name and produce a deal-prep package. Each stage runs sequentially via Convex scheduled functions. Use Claude API for generation and Exa for research. The pipeline should show real-time progress. Output is a downloadable zip with briefing, deck, and objection scripts."

- [x] **TASK-006** — New Deal input form (modal)
  Files: `components/NewDealModal.tsx`, `convex/deals.ts`
  Notes: Prospect name (required), industry (dropdown), use case (text). On submit: create Deal record, trigger pipeline.

- [x] **TASK-007** — Pipeline orchestration
  Files: `convex/pipeline.ts`
  Notes: Convex scheduled function that runs stages sequentially. Updates Deal.pipelineProgress and StageOutput records. Handles failures per stage with retry.

- [x] **TASK-008** — Stage 1: Account Research
  Files: `convex/stages/research.ts`, `lib/search.ts`
  Notes: Query Exa API with prospect name. Extract: company description, industry, size, recent news, AI signals, key people. Store as structured StageOutput. Flag if data is thin.

- [x] **TASK-009** — Stage 2: Strategy Brief Generation
  Files: `convex/stages/brief.ts`, `lib/ai.ts`
  Notes: Claude API call with research context + industry knowledge. Generate 1-page AI opportunity brief in markdown. Quality check: must mention specific prospect details, not generic.

- [x] **TASK-010** — Stage 3: Deck Generation
  Files: `convex/stages/deck.ts`, `lib/pptx.ts`, `templates/default.pptx`
  Notes: Generate slide content via Claude, then render .pptx. 10-12 slides: cover, exec summary, prospect context, AI opportunity, use-case detail, solution architecture, timeline, pricing, competitive edge, next steps. Upload to Convex file storage.

- [x] **TASK-011** — Stage 4: Objection Script Generation
  Files: `convex/stages/objections.ts`
  Notes: Claude API call with research + brief context. Generate top 5 objections with: objection text, response script, coaching note. Output as structured markdown.

- [x] **TASK-012** — Stage 5: Package Assembly
  Files: `convex/stages/package.ts`
  Notes: Bundle brief (render md → PDF), deck (.pptx), objections (.md) into a zip file. Upload zip to Convex file storage. Create Package record with signed URLs.

- [x] **TASK-013** — Pipeline progress UI
  Files: `app/deal/[id]/page.tsx`, `components/PipelineProgress.tsx`
  Notes: 5-step progress bar, real-time updates via Convex subscription. Completed stages show green check + preview. Failed shows red + retry. Use Convex `useQuery` for reactive updates.

- [x] **TASK-014** — Download package
  Files: `app/deal/[id]/page.tsx`, `components/PackageDownload.tsx`
  Notes: Three individual download buttons (brief, deck, objections) + "Download All" zip button. Signed URLs from Convex file storage.

---

## Phase 3 — Polish & Payments (Week 4)

> **Goal:** Production-ready with payments, brand settings, and quality-of-life improvements. Ready for first paying customers.

**Agent session prompt:** "Add payments (Polar), brand settings, deal history, and polish to DealForge. Users should be able to subscribe to Pro, upload their logo and brand colors, see all past deals, and re-run deals with modified inputs. Fix any rough edges from Phase 2."

- [ ] **TASK-015** — Polar payment integration
  Files: `app/settings/billing/page.tsx`, `convex/subscriptions.ts`, `app/api/webhooks/polar/route.ts`
  Notes: Free tier (2 deals/month), Pro ($300/month, unlimited). Polar checkout redirect from pricing page. Webhook updates user plan in Convex. Usage counter resets monthly.

- [ ] **TASK-016** — Brand settings page
  Files: `app/settings/brand/page.tsx`, `convex/users.ts`
  Notes: Upload logo, set primary + secondary brand colors, footer text. Saved to user.brandSettings. Applied to all future deck generations.

- [ ] **TASK-017** — Deal history dashboard
  Files: `app/dashboard/page.tsx`, `components/DealCard.tsx`
  Notes: Card grid of all deals: prospect name, date, status badge (pending/running/completed/failed), download button, re-run button. Sort by most recent. Paginate at 20.

- [ ] **TASK-018** — Re-run deal with modified inputs
  Files: `app/deal/[id]/page.tsx`, `components/RerunModal.tsx`
  Notes: Pre-fill form with existing inputs. On submit: create new Deal (don't overwrite old). Link to previous deal for comparison.

- [ ] **TASK-019** — Quality flags on thin data
  Files: `components/QualityFlag.tsx`, `convex/stages/research.ts`
  Notes: Research stage assigns qualityScore 1-5 per section. Sections scoring < 3 get yellow warning badge in UI: "Limited public data — consider adding your own research."

- [ ] **TASK-020** — Error handling and retry
  Files: `convex/pipeline.ts`, `components/StageError.tsx`
  Notes: Per-stage retry button. Exponential backoff on Claude API rate limits. Graceful fallback: if deck gen fails twice, generate PDF instead and flag.

- [ ] **TASK-021** — Landing page
  Files: `app/page.tsx`
  Notes: Hero: headline + subhead + CTA. Before/after visual: manual prep vs. DealForge. Three feature blocks. Pricing table. Social proof section (placeholder for testimonials). Footer.

- [ ] **TASK-022** — Deploy to production
  Files: `.env.production`, `vercel.json`
  Notes: Deploy Next.js to Vercel. Convex production deployment. Set all API keys (Claude, Exa, Clerk, Polar) in Vercel env vars. DNS + custom domain.

---

## Agent Session Guide

### Session structure
- **One phase per session.** Don't try to build everything at once.
- **Start each session** by reading this roadmap and the PRD. Check which tasks are complete.
- **Mark tasks done** by changing `- [ ]` to `- [x]` in this file as you complete them.
- **Test after each task.** Don't batch 5 tasks then test — test incrementally.

### Key files to read first
- `docs/prd.md` — Technical blueprint (data model, API spec, UI requirements)
- `docs/product-vision.md` — Product strategy (personas, flows, success metrics)
- `vision.json` — Raw founder answers (tech stack choices, rationale)

### Environment setup
```bash
# Install dependencies
npm install

# Start Convex dev server (separate terminal)
npx convex dev

# Start Next.js dev server
npm run dev

# Set up environment variables
# CLERK_SECRET_KEY, NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
# CONVEX_DEPLOYMENT
# ANTHROPIC_API_KEY
# EXA_API_KEY
# POLAR_ACCESS_TOKEN
```

# Architecture — Freelance Designer Client Portal

**Stack:** Next.js 14 App Router · Supabase (Postgres + Auth + Storage) · Vercel · Stripe · Resend
**Target:** Solo freelance designer, 5–12 active clients, $29/mo SaaS

---

## DATABASE SCHEMA

```sql
-- Designers (linked to Supabase Auth user)
create table designers (
  id          uuid primary key references auth.users(id),
  email       text not null unique,
  name        text not null,
  slug        text not null unique,   -- designer.app/[slug] = their portal root
  stripe_account_id text,             -- Stripe Connect Express
  created_at  timestamptz default now()
);

-- Projects
create table projects (
  id          uuid primary key default gen_random_uuid(),
  designer_id uuid not null references designers(id) on delete cascade,
  client_name text not null,
  client_email text not null,
  title       text not null,
  status      text not null default 'brief_pending'
               check (status in ('brief_pending','active','awaiting_feedback',
                                  'revision','invoice_sent','paid','complete')),
  magic_token text not null unique default gen_random_uuid()::text,
  created_at  timestamptz default now()
);

-- Briefs (client fills this in)
create table briefs (
  id          uuid primary key default gen_random_uuid(),
  project_id  uuid not null references projects(id) on delete cascade,
  answers     jsonb not null,          -- {question: answer} pairs
  submitted_at timestamptz default now()
);

-- Deliverables (designer uploads)
create table deliverables (
  id          uuid primary key default gen_random_uuid(),
  project_id  uuid not null references projects(id) on delete cascade,
  file_path   text not null,           -- Supabase Storage path
  file_name   text not null,
  version     int not null default 1,
  uploaded_at timestamptz default now()
);

-- Feedback (client leaves on a deliverable)
create table feedback (
  id             uuid primary key default gen_random_uuid(),
  deliverable_id uuid not null references deliverables(id) on delete cascade,
  project_id     uuid not null references projects(id) on delete cascade,
  comment        text not null,
  created_at     timestamptz default now()
);

-- Invoices
create table invoices (
  id                 uuid primary key default gen_random_uuid(),
  project_id         uuid not null references projects(id) on delete cascade,
  designer_id        uuid not null references designers(id),
  amount_cents       int not null,
  currency           text not null default 'usd',
  stripe_payment_link text,
  status             text not null default 'draft'
                     check (status in ('draft','sent','paid','void')),
  paid_at            timestamptz,
  created_at         timestamptz default now()
);
```

### RLS Policies

```sql
-- Designers own their data
alter table projects enable row level security;
create policy "designer_owns_projects" on projects
  for all using (auth.uid() = designer_id);

-- Deliverables and feedback: designer can read all on their projects
create policy "designer_reads_deliverables" on deliverables
  for select using (
    project_id in (select id from projects where designer_id = auth.uid())
  );

-- Public (magic-link) access handled in API routes, not RLS
-- Client-facing routes verify magic_token in middleware, bypass RLS via service role key
```

---

## AUTH FLOW

**Designer auth:** Supabase email magic link (no password). On first login, create `designers` row.

**Client access (no account required):**
1. Designer creates project → system generates `magic_token` (UUID)
2. Designer clicks "Send to client" → Resend email with link: `app.com/p/[magic_token]`
3. Client opens link → middleware validates `magic_token` against `projects` table → sets session cookie with `project_id`
4. Client can view/interact with their project only, no auth required

```
middleware.ts
  └─ /p/[token]  → validate token → set cookie → allow
  └─ /dashboard  → require Supabase session → redirect to /login if missing
  └─ /api/*      → check cookie or session based on route type
```

---

## API SURFACE

```
POST /api/projects            create project, send invite email
GET  /api/projects            list designer's projects (auth required)
GET  /api/projects/[id]       project detail (auth or magic-token cookie)

POST /api/briefs/[projectId]  client submits brief (magic-token cookie)

POST /api/deliverables/[projectId]  designer uploads file (auth)
GET  /api/deliverables/[projectId]  list deliverables (auth or cookie)

POST /api/feedback/[deliverableId]  client leaves feedback (magic-token cookie)
GET  /api/feedback/[deliverableId]  list feedback (auth)

POST /api/invoices/[projectId]      designer creates invoice (auth)
POST /api/webhooks/stripe           Stripe payment webhook (signature verified)
```

---

## INTEGRATION PLAN

| Service | Use | Key detail |
|---------|-----|-----------|
| Supabase Auth | Designer login | Email magic link, no password |
| Supabase Storage | Deliverable files | Bucket: `deliverables`, private, signed URLs |
| Stripe Connect Express | Payments | Designer onboards their own Stripe account; platform fee 0% v1 |
| Resend | Transactional email | New project invite, brief submitted, file uploaded, invoice sent, payment received |

---

## FOLDER STRUCTURE

```
app/
  (designer)/
    dashboard/page.tsx          — active projects grid
    projects/[id]/page.tsx      — project detail + upload + invoice
    login/page.tsx              — magic link login
  (client)/
    p/[token]/page.tsx          — client view (brief + deliverable + feedback)
    p/[token]/brief/page.tsx    — brief intake form
  api/
    projects/route.ts
    briefs/[projectId]/route.ts
    deliverables/[projectId]/route.ts
    feedback/[deliverableId]/route.ts
    invoices/[projectId]/route.ts
    webhooks/stripe/route.ts
components/
  ProjectCard.tsx
  BriefForm.tsx
  DeliverableViewer.tsx
  FeedbackThread.tsx
  InvoicePanel.tsx
lib/
  supabase/
    client.ts                   — browser client
    server.ts                   — server component client
    middleware.ts               — magic token validation
  stripe.ts                     — Stripe client + webhook helper
  resend.ts                     — email sending wrapper
  types.ts                      — shared TypeScript types
middleware.ts                   — route guard (designer auth + client token)
```

---

## ENV VARS

```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=          # server-only, never expose to client

# Stripe
STRIPE_SECRET_KEY=
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=
STRIPE_WEBHOOK_SECRET=

# Resend
RESEND_API_KEY=
RESEND_FROM_EMAIL=noreply@yourdomain.com

# App
NEXT_PUBLIC_APP_URL=https://yourdomain.com
```

---

## CRITICAL DECISIONS

1. **No client accounts.** Magic token per project. Reduces onboarding friction to zero — client clicks a link, no signup. Revisit post-launch if designers request multi-project client logins.

2. **Stripe Connect Express (not Checkout).** Designer receives money directly into their own Stripe account. No money flows through the platform = no money transmitter complexity. Platform fee = 0% in v1.

3. **One deliverable version per upload.** Version number increments automatically. No branching. If designer uploads v3, client sees v1, v2, v3 in sequence. No delete — append only.

4. **Supabase Storage with signed URLs.** Deliverable files are private. Client gets a 1-hour signed URL via the API route (after magic token validation). No public bucket.

5. **Service role key only in API routes.** Never in client components. Client-side Supabase calls use the anon key + RLS. Magic-token routes use the service role key to bypass RLS safely.

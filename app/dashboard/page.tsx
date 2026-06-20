import { EmptyState } from "@/components/EmptyState";
import { EnsureUser } from "@/components/EnsureUser";
import { NewDealModal } from "@/components/NewDealModal";
import Link from "next/link";

export default function DashboardPage() {
  const authReady = Boolean(
    process.env.NEXT_PUBLIC_CONVEX_URL && process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
  );

  return (
    <main className="min-h-screen bg-paper">
      {authReady ? <EnsureUser /> : null}
      <header className="border-b border-stone-200 bg-ivory">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4 sm:px-8 lg:px-10">
          <div>
            <p className="text-sm font-medium text-stone-500">DealForge</p>
            <h1 className="text-2xl font-semibold text-ink">Deal packages</h1>
          </div>
          <div className="rounded-md border border-stone-200 bg-white px-3 py-2 text-sm font-medium text-stone-600">
            Auth scaffold ready
          </div>
        </div>
      </header>

      <section className="mx-auto max-w-6xl px-6 py-8 sm:px-8 lg:px-10">
        <div className="mb-6 flex flex-col justify-between gap-3 sm:flex-row sm:items-end">
          <div>
            <h2 className="text-lg font-semibold text-ink">Dashboard</h2>
            <p className="mt-1 text-sm text-stone-600">
              Track prospect research, strategy decks, objection scripts, and downloads.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <span className="hidden rounded-full border border-stone-200 bg-white px-3 py-1 text-xs uppercase tracking-[0.18em] text-stone-500 sm:inline">
              Exploratory
            </span>
            {authReady ? <NewDealModal /> : <NewDealModal userId="demo-user" />}
          </div>
        </div>
        <EmptyState />
        <div className="mt-6 rounded-lg border border-stone-200 bg-white p-4 text-sm text-stone-600">
          Phase 2 test accounts live in <span className="font-medium text-ink">docs/test-accounts.md</span>. Start with
          Acme Manufacturing, focus on predictive quality, and compare the output against the rest of the matrix.
        </div>
        <div className="mt-4 rounded-lg border border-stone-200 bg-white p-4 text-sm text-stone-600">
          <Link className="font-semibold text-ink underline-offset-4 hover:underline" href="/domain-workflows/kyc-screening">
            Open KYC workflow
          </Link>
        </div>
      </section>
    </main>
  );
}

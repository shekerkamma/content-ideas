import { EmptyState } from "@/components/EmptyState";
import { EnsureUser } from "@/components/EnsureUser";

export default function DashboardPage() {
  return (
    <main className="min-h-screen bg-paper">
      <EnsureUser />
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
          <button className="rounded-md bg-ink px-4 py-2 text-sm font-semibold text-white" type="button">
            New deal
          </button>
        </div>
        <EmptyState />
      </section>
    </main>
  );
}

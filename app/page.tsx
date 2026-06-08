import Link from "next/link";
import { ArrowRight } from "lucide-react";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-ink text-ivory">
      <section className="mx-auto flex min-h-screen w-full max-w-6xl flex-col justify-between px-6 py-8 sm:px-8 lg:px-10">
        <nav className="flex items-center justify-between">
          <div className="text-lg font-semibold">DealForge</div>
          <Link
            className="rounded-md border border-white/20 px-4 py-2 text-sm font-medium text-white transition hover:bg-white hover:text-ink"
            href="/dashboard"
          >
            Dashboard
          </Link>
        </nav>

        <div className="max-w-3xl py-24">
          <p className="mb-5 text-sm font-semibold uppercase tracking-[0.18em] text-red-200">
            AI consultant pre-sales
          </p>
          <h1 className="text-5xl font-semibold leading-[1.02] sm:text-6xl lg:text-7xl">
            Stop prepping. Start closing.
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-8 text-stone-200">
            DealForge turns a prospect name into a complete deal-prep package:
            account briefing, strategy deck, and objection scripts.
          </p>
          <Link
            className="mt-8 inline-flex items-center gap-2 rounded-md bg-accent px-5 py-3 text-sm font-semibold text-white transition hover:bg-red-800"
            href="/dashboard"
          >
            Create first deal
            <ArrowRight aria-hidden="true" size={18} />
          </Link>
        </div>

        <div className="grid gap-4 border-t border-white/10 pt-6 text-sm text-stone-300 sm:grid-cols-3">
          <div>4-8 hours of prep compressed into a focused workflow.</div>
          <div>Editable outputs: briefing, deck, objection scripts.</div>
          <div>Transparent quality flags when public data is thin.</div>
        </div>
      </section>
    </main>
  );
}

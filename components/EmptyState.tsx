import { PlusCircle } from "lucide-react";

export function EmptyState() {
  return (
    <div className="flex min-h-[420px] flex-col items-center justify-center rounded-lg border border-dashed border-stone-300 bg-ivory px-6 text-center">
      <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-md bg-red-50 text-accent">
        <PlusCircle aria-hidden="true" size={24} />
      </div>
      <h2 className="text-xl font-semibold text-ink">Enter a prospect name to generate your first deal package.</h2>
      <p className="mt-3 max-w-md text-sm leading-6 text-stone-600">
        Phase 1 has the dashboard shell ready. The Phase 2 pipeline will connect research,
        deck generation, objection scripts, and package download.
      </p>
      <button
        className="mt-6 rounded-md bg-accent px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-red-800"
        type="button"
      >
        New deal
      </button>
    </div>
  );
}

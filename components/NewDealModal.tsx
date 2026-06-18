"use client";

import { useMutation, useQuery } from "convex/react";
import { useUser } from "@clerk/nextjs";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { api } from "@/convex/_generated/api";

type NewDealModalProps = {
  userId?: string;
};

const authReady = Boolean(process.env.NEXT_PUBLIC_CONVEX_URL && process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY);

export function NewDealModal(props: NewDealModalProps) {
  if (!authReady) {
    return <DemoNewDealModal userId={props.userId} />;
  }

  return <AuthenticatedNewDealModal />;
}

function DemoNewDealModal({ userId }: NewDealModalProps) {
  const [open, setOpen] = useState(false);
  const [prospectName, setProspectName] = useState("Acme Manufacturing");
  const [prospectIndustry, setProspectIndustry] = useState("Manufacturing");
  const [useCase, setUseCase] = useState("Predictive quality");
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);

    try {
      if (typeof window !== "undefined") {
        const current = window.localStorage.getItem("dealforge.demoDeals");
        const existing = current ? (JSON.parse(current) as Array<Record<string, string>>) : [];
        existing.unshift({
          userId: userId ?? "demo-user",
          prospectName,
          prospectIndustry,
          useCase,
          createdAt: new Date().toISOString()
        });
        window.localStorage.setItem("dealforge.demoDeals", JSON.stringify(existing.slice(0, 10)));
      }
      setOpen(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create deal.");
    }
  }

  return (
    <div>
      <button
        className="rounded-md bg-ink px-4 py-2 text-sm font-semibold text-white"
        type="button"
        onClick={() => setOpen(true)}
      >
        New deal
      </button>

      {open ? (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
          <div className="w-full max-w-lg rounded-lg bg-white p-6 shadow-2xl">
            <div className="flex items-start justify-between gap-4">
              <div>
                <h2 className="text-lg font-semibold text-ink">Create deal</h2>
                <p className="mt-1 text-sm text-stone-600">
                  Seed the pipeline with a test account before Phase 2 generation work starts.
                </p>
                <p className="mt-2 text-xs uppercase tracking-[0.16em] text-stone-500">
                  Demo mode saves a local draft until live auth is available.
                </p>
              </div>
              <button className="text-sm font-medium text-stone-500" type="button" onClick={() => setOpen(false)}>
                Close
              </button>
            </div>

            <form className="mt-5 space-y-4" onSubmit={handleSubmit}>
              <label className="block">
                <span className="text-sm font-medium text-ink">Prospect name</span>
                <input
                  className="mt-1 w-full rounded-md border border-stone-300 px-3 py-2"
                  value={prospectName}
                  onChange={(event) => setProspectName(event.target.value)}
                />
              </label>
              <label className="block">
                <span className="text-sm font-medium text-ink">Industry</span>
                <input
                  className="mt-1 w-full rounded-md border border-stone-300 px-3 py-2"
                  value={prospectIndustry}
                  onChange={(event) => setProspectIndustry(event.target.value)}
                />
              </label>
              <label className="block">
                <span className="text-sm font-medium text-ink">Use case</span>
                <input
                  className="mt-1 w-full rounded-md border border-stone-300 px-3 py-2"
                  value={useCase}
                  onChange={(event) => setUseCase(event.target.value)}
                />
              </label>

              {error ? <p className="text-sm text-red-700">{error}</p> : null}

              <div className="flex justify-end gap-3">
                <button
                  className="rounded-md border border-stone-300 px-4 py-2 text-sm font-medium text-stone-700"
                  type="button"
                  onClick={() => setOpen(false)}
                >
                  Cancel
                </button>
                <button className="rounded-md bg-accent px-4 py-2 text-sm font-semibold text-white" type="submit">
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      ) : null}
    </div>
  );
}

function AuthenticatedNewDealModal() {
  const router = useRouter();
  const { user, isLoaded } = useUser();
  const currentUser = useQuery(
    api.users.getCurrentUserByClerkId,
    isLoaded && user?.id ? { clerkId: user.id } : "skip"
  );
  const createDeal = useMutation(api.deals.createDeal);
  const [open, setOpen] = useState(false);
  const [prospectName, setProspectName] = useState("Acme Manufacturing");
  const [prospectIndustry, setProspectIndustry] = useState("Manufacturing");
  const [useCase, setUseCase] = useState("Predictive quality");
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);

    try {
      if (!currentUser?._id) {
        throw new Error("No current user record found.");
      }

      const created = await createDeal({
        userId: currentUser._id,
        prospectName,
        prospectIndustry,
        useCase
      });

      setOpen(false);
      router.push(`/deal/${created.dealId}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create deal.");
    }
  }

  return (
    <div>
      <button
        className="rounded-md bg-ink px-4 py-2 text-sm font-semibold text-white"
        type="button"
        onClick={() => setOpen(true)}
      >
        New deal
      </button>

      {open ? (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
          <div className="w-full max-w-lg rounded-lg bg-white p-6 shadow-2xl">
            <div className="flex items-start justify-between gap-4">
              <div>
                <h2 className="text-lg font-semibold text-ink">Create deal</h2>
                <p className="mt-1 text-sm text-stone-600">
                  Seed the pipeline with a test account before Phase 2 generation work starts.
                </p>
                <p className="mt-2 text-xs uppercase tracking-[0.16em] text-stone-500">
                  Connected auth creates a real Convex deal record.
                </p>
              </div>
              <button className="text-sm font-medium text-stone-500" type="button" onClick={() => setOpen(false)}>
                Close
              </button>
            </div>

            <form className="mt-5 space-y-4" onSubmit={handleSubmit}>
              <label className="block">
                <span className="text-sm font-medium text-ink">Prospect name</span>
                <input
                  className="mt-1 w-full rounded-md border border-stone-300 px-3 py-2"
                  value={prospectName}
                  onChange={(event) => setProspectName(event.target.value)}
                />
              </label>
              <label className="block">
                <span className="text-sm font-medium text-ink">Industry</span>
                <input
                  className="mt-1 w-full rounded-md border border-stone-300 px-3 py-2"
                  value={prospectIndustry}
                  onChange={(event) => setProspectIndustry(event.target.value)}
                />
              </label>
              <label className="block">
                <span className="text-sm font-medium text-ink">Use case</span>
                <input
                  className="mt-1 w-full rounded-md border border-stone-300 px-3 py-2"
                  value={useCase}
                  onChange={(event) => setUseCase(event.target.value)}
                />
              </label>

              {error ? <p className="text-sm text-red-700">{error}</p> : null}

              <div className="flex justify-end gap-3">
                <button
                  className="rounded-md border border-stone-300 px-4 py-2 text-sm font-medium text-stone-700"
                  type="button"
                  onClick={() => setOpen(false)}
                >
                  Cancel
                </button>
                <button className="rounded-md bg-accent px-4 py-2 text-sm font-semibold text-white" type="submit">
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      ) : null}
    </div>
  );
}

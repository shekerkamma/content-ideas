"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import {
  AlertTriangle,
  ArrowLeft,
  CheckCircle2,
  FileWarning,
  Play,
  RotateCcw,
  ShieldAlert
} from "lucide-react";
import type { KycUiComponent } from "@/lib/domain-workflows/kyc-ui";

type BeneficialOwner = {
  name: string;
  ownership_percent: number;
  pep_declared: boolean;
  nationality: string;
};

type ApplicantRecord = {
  applicant_id: string;
  applicant_name: string;
  applicant_type: "private_company" | "individual" | "trust";
  jurisdiction: string;
  source_of_funds: string;
  beneficial_owners: BeneficialOwner[];
  documents_received: Array<{
    type: string;
    status: "received" | "expired";
  }>;
  screening_results: {
    sanctions: "no-hit" | "possible-hit" | "confirmed" | "not-run";
    pep: "no-hit" | "possible-hit" | "confirmed" | "not-run";
    adverse_media: "no-hit" | "possible-hit" | "confirmed" | "not-run";
  };
};

type WorkflowResponse = {
  workflow: string;
  ui: KycUiComponent[];
};

const SAMPLE_APPLICANT: ApplicantRecord = {
  applicant_id: "APP-001",
  applicant_name: "Northstar Family Holdings Ltd.",
  applicant_type: "private_company",
  jurisdiction: "United Kingdom",
  source_of_funds: "",
  beneficial_owners: [
    {
      name: "Jane Doe",
      ownership_percent: 55,
      pep_declared: true,
      nationality: "United Kingdom"
    },
    {
      name: "Nominee Services Ltd.",
      ownership_percent: 20,
      pep_declared: false,
      nationality: "Cayman Islands"
    }
  ],
  documents_received: [
    {
      type: "certificate_of_incorporation",
      status: "received"
    },
    {
      type: "beneficial_ownership_register",
      status: "received"
    }
  ],
  screening_results: {
    sanctions: "no-hit",
    pep: "confirmed",
    adverse_media: "possible-hit"
  }
};

const DOCUMENT_OPTIONS = [
  "certificate_of_incorporation",
  "beneficial_ownership_register",
  "source_of_funds"
];

const SCREENING_OPTIONS = ["not-run", "no-hit", "possible-hit", "confirmed"] as const;

function formatLabel(value: string) {
  return value.replaceAll("_", " ");
}

function hasDocument(record: ApplicantRecord, docType: string) {
  return record.documents_received.some((doc) => doc.type === docType);
}

function setDocument(record: ApplicantRecord, docType: string, enabled: boolean): ApplicantRecord {
  if (enabled) {
    if (hasDocument(record, docType)) {
      return record;
    }
    return {
      ...record,
      documents_received: [...record.documents_received, { type: docType, status: "received" }]
    };
  }

  return {
    ...record,
    documents_received: record.documents_received.filter((doc) => doc.type !== docType)
  };
}

function StatusPill({ tone, children }: { tone: "green" | "amber" | "red" | "blue"; children: React.ReactNode }) {
  const tones = {
    green: "border-emerald-200 bg-emerald-50 text-emerald-800",
    amber: "border-amber-200 bg-amber-50 text-amber-900",
    red: "border-red-200 bg-red-50 text-red-800",
    blue: "border-sky-200 bg-sky-50 text-sky-800"
  };
  return (
    <span className={`inline-flex items-center rounded-md border px-2.5 py-1 text-xs font-semibold ${tones[tone]}`}>
      {children}
    </span>
  );
}

function renderGeneratedComponent(component: KycUiComponent) {
  switch (component.component) {
    case "DispositionSummary": {
      const riskTone = component.props.riskRating === "high" ? "red" : component.props.riskRating === "medium" ? "amber" : "green";
      return (
        <section className="rounded-md border border-stone-200 bg-white p-5 shadow-panel" key={component.component}>
          <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <div className="flex items-center gap-2 text-sm font-semibold text-stone-500">
                <ShieldAlert aria-hidden="true" size={17} />
                Disposition
              </div>
              <h2 className="mt-2 text-2xl font-semibold text-ink">{component.props.applicantName}</h2>
              <p className="mt-1 text-sm text-stone-500">{component.props.applicantId}</p>
            </div>
            <div className="flex flex-wrap gap-2">
              <StatusPill tone={riskTone}>{component.props.riskRating} risk</StatusPill>
              <StatusPill tone="blue">{component.props.disposition}</StatusPill>
              {component.props.humanReviewRequired ? <StatusPill tone="amber">human review</StatusPill> : null}
            </div>
          </div>
          <div className="mt-5 grid gap-2">
            {component.props.escalationReasons.length ? (
              component.props.escalationReasons.map((reason) => (
                <div className="flex items-start gap-2 rounded-md border border-red-100 bg-red-50 px-3 py-2 text-sm text-red-900" key={reason}>
                  <AlertTriangle aria-hidden="true" className="mt-0.5 shrink-0" size={16} />
                  <span>{reason}</span>
                </div>
              ))
            ) : (
              <div className="flex items-center gap-2 rounded-md border border-emerald-100 bg-emerald-50 px-3 py-2 text-sm text-emerald-900">
                <CheckCircle2 aria-hidden="true" size={16} />
                <span>No escalation reason returned.</span>
              </div>
            )}
          </div>
        </section>
      );
    }
    case "MissingDocuments":
      return (
        <section className="rounded-md border border-stone-200 bg-white p-5 shadow-panel" key={component.component}>
          <div className="flex items-center gap-2 text-sm font-semibold text-stone-500">
            <FileWarning aria-hidden="true" size={17} />
            Documents
          </div>
          <div className="mt-4 flex flex-wrap gap-2">
            {component.props.documents.length ? (
              component.props.documents.map((doc) => (
                <StatusPill tone="amber" key={doc}>{formatLabel(doc)}</StatusPill>
              ))
            ) : (
              <StatusPill tone="green">complete</StatusPill>
            )}
            {component.props.expiredDocuments.map((doc) => (
              <StatusPill tone="red" key={doc}>expired {formatLabel(doc)}</StatusPill>
            ))}
          </div>
        </section>
      );
    case "RuleOutcomeTable":
      return (
        <section className="rounded-md border border-stone-200 bg-white p-5 shadow-panel" key={component.component}>
          <div className="text-sm font-semibold text-stone-500">Rule outcomes</div>
          <div className="mt-4 overflow-x-auto">
            <table className="w-full min-w-[720px] border-collapse text-left text-sm">
              <thead>
                <tr className="border-b border-stone-200 text-xs font-semibold uppercase text-stone-500">
                  <th className="py-2 pr-4">Rule</th>
                  <th className="py-2 pr-4">Outcome</th>
                  <th className="py-2 pr-4">Severity</th>
                  <th className="py-2">Evidence</th>
                </tr>
              </thead>
              <tbody>
                {component.props.outcomes.map((outcome) => (
                  <tr className="border-b border-stone-100 align-top last:border-0" key={outcome.rule_id}>
                    <td className="py-3 pr-4 font-semibold text-ink">{outcome.rule_id}</td>
                    <td className="py-3 pr-4">
                      <StatusPill tone={outcome.outcome === "fail" ? "red" : "green"}>{outcome.outcome}</StatusPill>
                    </td>
                    <td className="py-3 pr-4 text-stone-700">{outcome.severity}</td>
                    <td className="py-3 text-stone-700">{outcome.evidence}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      );
    case "ValidationStatus":
      return (
        <section className="rounded-md border border-stone-200 bg-white p-5 shadow-panel" key={component.component}>
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="text-sm font-semibold text-stone-500">Validation</div>
            <StatusPill tone={component.props.status === "pass" ? "green" : "red"}>
              {component.props.status} · {component.props.error_count} errors
            </StatusPill>
          </div>
          {component.props.errors.length ? (
            <ul className="mt-4 grid gap-2 text-sm text-red-800">
              {component.props.errors.map((error) => (
                <li className="rounded-md border border-red-100 bg-red-50 px-3 py-2" key={error}>{error}</li>
              ))}
            </ul>
          ) : null}
        </section>
      );
    case "ReviewerPacket":
      return (
        <section className="rounded-md border border-stone-200 bg-white p-5 shadow-panel" key={component.component}>
          <div className="text-sm font-semibold text-stone-500">Reviewer packet</div>
          <pre className="mt-4 max-h-[420px] overflow-auto rounded-md bg-ink p-4 text-xs leading-6 text-ivory">
            {component.props.markdown}
          </pre>
        </section>
      );
    default:
      return null;
  }
}

export default function KycScreeningPage() {
  const [record, setRecord] = useState<ApplicantRecord>(SAMPLE_APPLICANT);
  const [response, setResponse] = useState<WorkflowResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const documentSet = useMemo(() => new Set(record.documents_received.map((doc) => doc.type)), [record.documents_received]);

  async function runWorkflow() {
    setIsRunning(true);
    setError(null);
    try {
      const res = await fetch("/api/domain-workflows/kyc-screening", {
        method: "POST",
        headers: {
          "content-type": "application/json"
        },
        body: JSON.stringify({ applicant: record })
      });
      const payload = await res.json();
      if (!res.ok) {
        throw new Error(payload.error ?? "Workflow request failed");
      }
      setResponse(payload as WorkflowResponse);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Workflow request failed");
    } finally {
      setIsRunning(false);
    }
  }

  return (
    <main className="min-h-screen bg-paper text-ink">
      <header className="border-b border-stone-200 bg-ivory">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-6 py-4 sm:px-8 lg:px-10">
          <div className="min-w-0">
            <Link className="inline-flex items-center gap-2 text-sm font-medium text-stone-600 transition hover:text-ink" href="/dashboard">
              <ArrowLeft aria-hidden="true" size={16} />
              Dashboard
            </Link>
            <h1 className="mt-2 text-2xl font-semibold text-ink">KYC workflow</h1>
          </div>
          <button
            className="inline-flex min-h-10 items-center gap-2 rounded-md bg-accent px-4 py-2 text-sm font-semibold text-white transition hover:bg-red-800 disabled:cursor-not-allowed disabled:bg-stone-400"
            disabled={isRunning}
            onClick={runWorkflow}
            type="button"
          >
            <Play aria-hidden="true" size={17} />
            {isRunning ? "Running" : "Run workflow"}
          </button>
        </div>
      </header>

      <div className="mx-auto grid max-w-7xl gap-6 px-6 py-6 sm:px-8 lg:grid-cols-[420px_minmax(0,1fr)] lg:px-10">
        <aside className="rounded-md border border-stone-200 bg-white p-5 shadow-panel">
          <div className="flex items-center justify-between gap-3">
            <h2 className="text-base font-semibold">Applicant</h2>
            <button
              className="inline-flex min-h-9 items-center gap-2 rounded-md border border-stone-200 px-3 py-2 text-sm font-semibold text-stone-700 transition hover:bg-stone-50"
              onClick={() => {
                setRecord(SAMPLE_APPLICANT);
                setResponse(null);
                setError(null);
              }}
              type="button"
            >
              <RotateCcw aria-hidden="true" size={16} />
              Reset
            </button>
          </div>

          <div className="mt-5 grid gap-4">
            <label className="grid gap-1.5 text-sm font-medium text-stone-700">
              Name
              <input
                className="min-h-10 rounded-md border border-stone-200 px-3 py-2 text-sm outline-none transition focus:border-ink"
                onChange={(event) => setRecord({ ...record, applicant_name: event.target.value })}
                value={record.applicant_name}
              />
            </label>

            <div className="grid grid-cols-2 gap-3">
              <label className="grid gap-1.5 text-sm font-medium text-stone-700">
                Type
                <select
                  className="min-h-10 rounded-md border border-stone-200 px-3 py-2 text-sm outline-none transition focus:border-ink"
                  onChange={(event) => setRecord({ ...record, applicant_type: event.target.value as ApplicantRecord["applicant_type"] })}
                  value={record.applicant_type}
                >
                  <option value="private_company">Private company</option>
                  <option value="individual">Individual</option>
                  <option value="trust">Trust</option>
                </select>
              </label>
              <label className="grid gap-1.5 text-sm font-medium text-stone-700">
                Jurisdiction
                <input
                  className="min-h-10 rounded-md border border-stone-200 px-3 py-2 text-sm outline-none transition focus:border-ink"
                  onChange={(event) => setRecord({ ...record, jurisdiction: event.target.value })}
                  value={record.jurisdiction}
                />
              </label>
            </div>

            <label className="grid gap-1.5 text-sm font-medium text-stone-700">
              Source of funds
              <input
                className="min-h-10 rounded-md border border-stone-200 px-3 py-2 text-sm outline-none transition focus:border-ink"
                onChange={(event) => setRecord({ ...record, source_of_funds: event.target.value })}
                value={record.source_of_funds}
              />
            </label>

            <div>
              <div className="mb-2 text-sm font-semibold text-stone-700">Documents</div>
              <div className="grid gap-2">
                {DOCUMENT_OPTIONS.map((docType) => (
                  <label className="flex min-h-10 items-center gap-3 rounded-md border border-stone-200 px-3 py-2 text-sm" key={docType}>
                    <input
                      checked={documentSet.has(docType)}
                      className="h-4 w-4 accent-red-700"
                      onChange={(event) => setRecord(setDocument(record, docType, event.target.checked))}
                      type="checkbox"
                    />
                    <span>{formatLabel(docType)}</span>
                  </label>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 gap-3 sm:grid-cols-3 lg:grid-cols-1">
              {(["sanctions", "pep", "adverse_media"] as const).map((field) => (
                <label className="grid gap-1.5 text-sm font-medium text-stone-700" key={field}>
                  {formatLabel(field)}
                  <select
                    className="min-h-10 rounded-md border border-stone-200 px-3 py-2 text-sm outline-none transition focus:border-ink"
                    onChange={(event) =>
                      setRecord({
                        ...record,
                        screening_results: {
                          ...record.screening_results,
                          [field]: event.target.value
                        }
                      })
                    }
                    value={record.screening_results[field]}
                  >
                    {SCREENING_OPTIONS.map((option) => (
                      <option key={option} value={option}>{option}</option>
                    ))}
                  </select>
                </label>
              ))}
            </div>
          </div>
        </aside>

        <section className="grid content-start gap-5">
          {error ? (
            <div className="rounded-md border border-red-200 bg-red-50 p-4 text-sm font-medium text-red-900">
              {error}
            </div>
          ) : null}
          {response ? (
            response.ui.map(renderGeneratedComponent)
          ) : (
            <div className="rounded-md border border-stone-200 bg-white p-8 text-center shadow-panel">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-md bg-stone-100 text-stone-600">
                <ShieldAlert aria-hidden="true" size={24} />
              </div>
              <h2 className="mt-4 text-lg font-semibold">No disposition yet</h2>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}

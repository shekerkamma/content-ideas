type DealCardProps = {
  prospectName: string;
  status: "pending" | "running" | "completed" | "failed";
  createdAt: string;
};

const statusStyles = {
  pending: "bg-stone-100 text-stone-700",
  running: "bg-blue-50 text-blue-700",
  completed: "bg-emerald-50 text-emerald-700",
  failed: "bg-red-50 text-red-700"
};

export function DealCard({ prospectName, status, createdAt }: DealCardProps) {
  return (
    <article className="rounded-lg border border-stone-200 bg-white p-5 shadow-panel">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="font-semibold text-ink">{prospectName}</h3>
          <p className="mt-1 text-sm text-stone-500">{createdAt}</p>
        </div>
        <span className={`rounded-full px-2.5 py-1 text-xs font-medium ${statusStyles[status]}`}>
          {status}
        </span>
      </div>
    </article>
  );
}

"use client";

import { Download, FileText, Presentation, Package } from "lucide-react";

type PackageDownloadProps = {
  briefUrl?: string | null;
  deckUrl?: string | null;
  objectionsUrl?: string | null;
  zipUrl?: string | null;
};

function DownloadLink({
  href,
  label,
  icon
}: {
  href?: string | null;
  label: string;
  icon: React.ReactNode;
}) {
  return (
    <a
      className="inline-flex items-center gap-2 rounded-md border border-stone-200 bg-white px-3 py-2 text-sm font-medium text-ink transition hover:border-stone-300 hover:bg-stone-50"
      href={href ?? "#"}
      onClick={(event) => {
        if (!href) {
          event.preventDefault();
        }
      }}
    >
      {icon}
      {label}
    </a>
  );
}

export function PackageDownload({ briefUrl, deckUrl, objectionsUrl, zipUrl }: PackageDownloadProps) {
  return (
    <div className="rounded-lg border border-stone-200 bg-white p-5">
      <div className="mb-4">
        <h2 className="text-base font-semibold text-ink">Downloads</h2>
        <p className="mt-1 text-sm text-stone-600">Individual artifacts plus the combined package.</p>
      </div>

      <div className="flex flex-wrap gap-3">
        <DownloadLink href={briefUrl} label="Brief" icon={<FileText className="h-4 w-4" />} />
        <DownloadLink href={deckUrl} label="Deck" icon={<Presentation className="h-4 w-4" />} />
        <DownloadLink href={objectionsUrl} label="Objections" icon={<Package className="h-4 w-4" />} />
        <DownloadLink href={zipUrl} label="Download all" icon={<Download className="h-4 w-4" />} />
      </div>
    </div>
  );
}

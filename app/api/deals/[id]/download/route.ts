import { readFile } from "node:fs/promises";
import path from "node:path";
import { NextRequest } from "next/server";
import { createZip } from "@/lib/zip";

export const runtime = "nodejs";

function downloadHeaders(filename: string, contentType: string) {
  return {
    "Content-Type": contentType,
    "Content-Disposition": `attachment; filename="${filename}"`,
    "Cache-Control": "no-store"
  };
}

async function getDeckTemplateBytes() {
  const templatePath =
    process.env.BRANDED_PPTX_TEMPLATE ?? path.join(process.cwd(), "templates/default.pptx");
  return await readFile(templatePath);
}

export async function GET(request: NextRequest, context: { params: Promise<{ id: string }> }) {
  const { id } = await context.params;
  const artifact = request.nextUrl.searchParams.get("artifact") ?? "zip";
  const prospectSlug = `deal-${id}`;

  if (artifact === "brief") {
    const brief = `# DealForge Brief Placeholder\n\nDeal: ${id}\n\nThis local download route is wired for testing. Replace it with Convex file storage when real artifact generation is connected.`;
    return new Response(brief, {
      headers: downloadHeaders(`${prospectSlug}-brief.md`, "text/markdown; charset=utf-8")
    });
  }

  if (artifact === "objections") {
    const objections = [
      "# Objections Placeholder",
      "",
      `Deal: ${id}`,
      "",
      "- Objection: We need more evidence.",
      "  - Response: Use the research and brief outputs to show a tailored path.",
      "- Objection: We already have a process.",
      "  - Response: Keep the framing on speed and consistency."
    ].join("\n");

    return new Response(objections, {
      headers: downloadHeaders(`${prospectSlug}-objections.md`, "text/markdown; charset=utf-8")
    });
  }

  if (artifact === "deck") {
    const deckBytes = await getDeckTemplateBytes();
    return new Response(deckBytes, {
      headers: downloadHeaders(`${prospectSlug}-deck.pptx`, "application/vnd.openxmlformats-officedocument.presentationml.presentation")
    });
  }

  const brief = `# DealForge Brief Placeholder\n\nDeal: ${id}\n\nThis local download route is wired for testing.`;
  const objections = `# Objections Placeholder\n\nDeal: ${id}\n`;
  const deckBytes = await getDeckTemplateBytes();
  const zip = createZip([
    { name: `${prospectSlug}-brief.md`, data: Buffer.from(brief, "utf8") },
    { name: `${prospectSlug}-deck.pptx`, data: deckBytes },
    { name: `${prospectSlug}-objections.md`, data: Buffer.from(objections, "utf8") }
  ]);

  return new Response(zip, {
    headers: downloadHeaders(`${prospectSlug}-package.zip`, "application/zip")
  });
}

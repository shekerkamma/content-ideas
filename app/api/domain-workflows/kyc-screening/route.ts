import { execFile as execFileCallback } from "node:child_process";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { promisify } from "node:util";
import { buildKycUiSurface, type KycDisposition, type KycValidationResult } from "@/lib/domain-workflows/kyc-ui";

const execFile = promisify(execFileCallback);

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

function workflowPath(...segments: string[]) {
  return path.join(
    process.cwd(),
    "domain-workflows",
    "financial-services",
    "kyc-screening",
    ...segments
  );
}

function parseValidation(stdout: string): KycValidationResult {
  try {
    return JSON.parse(stdout) as KycValidationResult;
  } catch {
    return {
      status: "fail",
      error_count: 1,
      errors: ["Validator did not return parseable JSON."]
    };
  }
}

function errorMessage(error: unknown) {
  if (error instanceof Error) {
    return error.message;
  }
  return "Unknown workflow error";
}

export async function POST(request: Request) {
  const body = await request.json();
  const applicant = body.applicant ?? body;
  const runScript = workflowPath("scripts", "run_kyc_screening.py");
  const validateScript = workflowPath("scripts", "validate_kyc_disposition.py");
  const rules = workflowPath("references", "rules-grid.json");
  const workDir = await mkdtemp(path.join(tmpdir(), "kyc-screening-"));
  const inputPath = path.join(workDir, "input.json");
  const dispositionPath = path.join(workDir, "kyc-disposition.json");
  const reviewerPacketPath = path.join(workDir, "reviewer-packet.md");

  try {
    await writeFile(inputPath, JSON.stringify(applicant, null, 2), "utf8");
    await execFile("python3", [runScript, inputPath, "--rules", rules, "--out", workDir], {
      maxBuffer: 1024 * 1024
    });

    const disposition = JSON.parse(
      await readFile(dispositionPath, "utf8")
    ) as KycDisposition;
    const reviewerPacket = await readFile(reviewerPacketPath, "utf8");

    let validation: KycValidationResult;
    try {
      const { stdout } = await execFile(
        "python3",
        [validateScript, dispositionPath, "--input", inputPath, "--rules", rules],
        { maxBuffer: 1024 * 1024 }
      );
      validation = parseValidation(stdout);
    } catch (error) {
      const stdout = typeof (error as { stdout?: unknown }).stdout === "string"
        ? ((error as { stdout: string }).stdout)
        : "";
      validation = parseValidation(stdout);
    }

    return Response.json({
      workflow: "financial-services-kyc-screening",
      disposition,
      reviewerPacket,
      validation,
      ui: buildKycUiSurface(disposition, validation, reviewerPacket)
    });
  } catch (error) {
    return Response.json(
      {
        error: errorMessage(error)
      },
      { status: 500 }
    );
  } finally {
    await rm(workDir, { recursive: true, force: true });
  }
}

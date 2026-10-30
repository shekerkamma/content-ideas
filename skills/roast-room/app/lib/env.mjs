import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

// content-ideas port: the app ships inside the roast-room skill (skills/roast-room/app/), and
// everything a user creates lives under ROAST_HOME, never in the skill folder (a plugin cache
// can be replaced on upgrade). ROAST_HOME = $ROAST_HOME, else $CONTENT_HOME/roast-room, else
// ~/Documents/Content/roast-room. Custom seats, brains, portraits, and a roster override sit
// there and win over the bundled ones.
export const APP_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
export const SKILL_DIR = path.resolve(APP_ROOT, "..");
export const ROAST_HOME = path.resolve(
  process.env.ROAST_HOME ||
    path.join(process.env.CONTENT_HOME || path.join(os.homedir(), "Documents", "Content"), "roast-room"),
);
export const SESSIONS_DIR = path.join(ROAST_HOME, "sessions");
export const EXAMPLES_DIR = path.join(SKILL_DIR, "examples");
/** Where saved councils are read from: the user's own first, then the bundled examples. */
export const SESSION_ROOTS = [SESSIONS_DIR, EXAMPLES_DIR];
/** Folder for a session id, or null when no root holds it. */
export const sessionDir = (name) => SESSION_ROOTS.map((r) => path.join(r, name)).find((d) => fs.existsSync(d)) || null;
export const ROSTER = fs.existsSync(path.join(ROAST_HOME, "roster.json"))
  ? path.join(ROAST_HOME, "roster.json")
  : path.join(SKILL_DIR, "roster.json");
export const USER_PORTRAITS = path.join(ROAST_HOME, "portraits");

const firstExisting = (...ps) => ps.find((p) => fs.existsSync(p)) || ps[ps.length - 1];
/** A seat's instructions: a custom seat in ROAST_HOME wins over the bundled one. */
export const seatFile = (key) =>
  firstExisting(path.join(ROAST_HOME, "seats", `council-${key}.md`), path.join(SKILL_DIR, "seats", `council-${key}.md`));
/** A seat's brain folder, same precedence. */
export const brainDir = (slug) =>
  firstExisting(path.join(ROAST_HOME, "brains", slug), path.join(SKILL_DIR, "brains", slug));

let cache = null;
export function env(key) {
  if (process.env[key]) return process.env[key];
  if (!cache) {
    cache = {};
    for (const p of [path.join(ROAST_HOME, ".env"), path.join(APP_ROOT, ".env")]) {
      if (!fs.existsSync(p)) continue;
      for (const line of fs.readFileSync(p, "utf8").split(/\r?\n/)) {
        const m = line.match(/^([A-Z0-9_]+)=(.*)$/);
        if (m && !(m[1] in cache)) cache[m[1]] = m[2].trim();
      }
    }
  }
  return cache[key] || "";
}

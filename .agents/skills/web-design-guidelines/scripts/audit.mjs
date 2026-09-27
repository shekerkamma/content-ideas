#!/usr/bin/env node
import fs from 'fs';
import path from 'path';

const targetDir = process.argv[2] || '.';

function walk(dir, results = []) {
  if (!fs.existsSync(dir)) return results;
  const list = fs.readdirSync(dir);
  for (const item of list) {
    if (['node_modules', '.git', '.next', 'dist', 'build'].includes(item)) continue;
    const fullPath = path.join(dir, item);
    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      walk(fullPath, results);
    } else if (/\.(tsx|jsx|html|css|vue|svelte)$/.test(item)) {
      results.push(fullPath);
    }
  }
  return results;
}

const files = walk(targetDir);
let violationCount = 0;

for (const file of files) {
  const content = fs.readFileSync(file, 'utf8');
  const lines = content.split('\n');

  lines.forEach((line, idx) => {
    const lineNum = idx + 1;

    // Rule: Never transition: all
    if (/transition\s*:\s*all\b/i.test(line)) {
      console.log(`${file}:${lineNum}: [Animation] Never use 'transition: all' — explicitly enumerate animated properties.`);
      violationCount++;
    }

    // Rule: Outline none without focus replacement
    if (/\boutline-none\b/i.test(line) && !/focus-visible/i.test(line)) {
      console.log(`${file}:${lineNum}: [Focus States] 'outline-none' detected without adjacent ':focus-visible' ring replacement.`);
      violationCount++;
    }

    // Rule: Triple dots in JSX
    if (/>[^<]*\.\.\.[^<]*</.test(line)) {
      console.log(`${file}:${lineNum}: [Typography] Use proper ellipsis character '…' instead of triple dots '...'.`);
      violationCount++;
    }

    // Rule: Icon-only button missing aria-label
    if (/<button\b/i.test(line) && !/aria-label/i.test(line) && (/<svg\b/i.test(line) || /icon/i.test(line))) {
      console.log(`${file}:${lineNum}: [Accessibility] Potential icon button missing explicit 'aria-label'.`);
      violationCount++;
    }

    // Rule: Image missing width/height
    if (/<img\b/i.test(line) && (!/width=/i.test(line) || !/height=/i.test(line))) {
      console.log(`${file}:${lineNum}: [Images] '<img>' missing explicit width/height (causes CLS).`);
      violationCount++;
    }
  });
}

console.log(`\nAudit complete: ${violationCount} potential guideline violation(s) found across ${files.length} file(s).`);

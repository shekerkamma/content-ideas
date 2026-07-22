import { writeFile, mkdir } from 'node:fs/promises';
import {
  PresentationFile, P, C, K, SERIF,
  tx, sh, rect, roundRect, ellipse,
  footer, header, headerDark, addSlide,
  card, kpi, table, rail, chain, SRC,
} from './deck-kit.mjs';
import { GRID, cols, rows, cx, span, bandTop, bandH } from './deck-grid.mjs';

const RUN = process.env.DECK_RUN || new URL('.', import.meta.url).pathname;
const NAME = process.env.DECK_NAME || 'UC-08-Multi-Model-Coding-Pilot-Client-Ready';
const OUT = `${RUN}/${NAME}-draft.pptx`;
const RENDERS = `${RUN}/qa/renders`;
await mkdir(RENDERS, { recursive: true });

const bodyTop = bandTop('BODY');
const bodyH = bandH('BODY');
const full = cols(1)[0];

const noteSources = [
  'https://opencode.ai/docs/providers',
  'https://build.nvidia.com/models',
  'https://docs.api.nvidia.com/nim/docs/product',
  'https://zenmux.ai/provider/moonshotai',
  'https://www.kimi.com/code/docs/en/kimi-code/models.html',
].join('\n');

function label(text, x, y, w, { fill = K.softCyan, color = K.slate, border = K.cyan } = {}) {
  return [
    roundRect(x, y, w, 30, fill, border, 1),
    tx(text.toUpperCase(), x + 8, y + 8, w - 16, 14, { size: 9, bold: true, color, align: 'center' }),
  ];
}

function checkItem(text, x, y, w, { dark = false, color = K.green } = {}) {
  return [
    ellipse(x, y + 2, 22, 22, color, color, 1),
    tx('✓', x + 2, y + 4, 18, 16, { size: 12, bold: true, color: K.white, align: 'center' }),
    tx(text, x + 34, y, w - 34, 30, { size: 13, color: dark ? K.white : K.slate, bold: true }),
  ];
}

function miniCard(x, y, w, h, title, body, color = K.cyan, dark = false) {
  const fill = dark ? '#12243A' : K.white;
  const line = dark ? '#28405B' : K.line;
  return [
    roundRect(x, y, w, h, fill, line, 1),
    rect(x, y, 5, h, color),
    tx(title, x + 18, y + 14, w - 30, 24, { size: 14, bold: true, color: dark ? K.white : K.slate }),
    tx(body, x + 18, y + 44, w - 30, h - 56, { size: 11, color: dark ? '#A9BACD' : K.gray }),
  ];
}

// 01 — Cover / L01
{
  const [left, right] = cols(2, { gutter: 38 });
  const providerCols = cols(2, { left: right.x + 22, right: right.x + right.w - 22, gutter: 14 });
  addSlide([
    rect(0, 0, 1280, 720, K.midnight),
    tx('UC-08 · USE-CASE REALIZATION', left.x, 52, left.w, 22, { size: 11, bold: true, color: K.cyan }),
    tx('A low-cost multi-model\ncoding pilot is possible now', left.x, 104, left.w + 30, 132,
      { size: 45, face: SERIF, bold: true, color: K.white }),
    tx('One terminal workflow. Multiple provider options. A bounded pilot before production commitment.',
      left.x, 260, left.w - 10, 62, { size: 18, color: '#B8C7D9' }),
    ...label('Pilot proposition', left.x, 356, 170, { fill: '#12243A', color: K.cyan, border: K.cyan }),
    tx('Prototype access can be free or promotional; production economics and terms require validation.',
      left.x, 405, left.w, 66, { size: 15, color: K.white, bold: true }),
    rect(right.x, 82, right.w, 460, '#101F33', '#28405B', 1),
    rect(right.x, 82, right.w, 42, '#162A43'),
    ellipse(right.x + 18, 97, 10, 10, '#FF6B6B'),
    ellipse(right.x + 36, 97, 10, 10, '#F6C453'),
    ellipse(right.x + 54, 97, 10, 10, '#39C57A'),
    tx('opencode  /models', right.x + 84, 94, right.w - 104, 18, { size: 11, color: '#9FB4CA' }),
    tx('SELECT A MODEL BY TASK', right.x + 24, 150, right.w - 48, 22, { size: 10, bold: true, color: K.cyan }),
    ...miniCard(providerCols[0].x, 194, providerCols[0].w, 112, 'NVIDIA', 'Prototype catalog\nOpen-model endpoints', K.teal, true),
    ...miniCard(providerCols[1].x, 194, providerCols[1].w, 112, 'ZENMUX', 'Aggregated access\nPromotional options', K.cyan, true),
    ...miniCard(providerCols[0].x, 324, providerCols[0].w, 112, 'KIMI K3', 'Long-horizon work\nUp to 1M context*', K.paleBlue, true),
    ...miniCard(providerCols[1].x, 324, providerCols[1].w, 112, 'TASK ROUTING', 'Code · vision\nreasoning · speed', K.green, true),
    tx('*Availability depends on provider and plan.', right.x + 24, 474, right.w - 48, 24, { size: 10, color: '#8FA2B7', italic: true }),
    tx('CLIENT-READY REBUILD · 22 JUL 2026', left.x, 620, 620, 20, { size: 10, bold: true, color: '#8FA2B7' }),
    ...footer(1, true),
  ], {
    background: K.midnight,
    notes: `Frame this as a pilot proposition, not a permanent zero-cost promise. The source deck's $0 claim has been qualified because provider promotions and production terms can change.\n\nSources:\n${noteSources}`,
  });
}

// 02 — Executive summary / L02
{
  const leftW = span(1, 6);
  const rightLeft = cx(7);
  const rightW = span(7, 12);
  const tiles = [
    { x: rightLeft, y: bodyTop, w: (rightW - 20) / 2, h: 164, n: '1', t: 'TERMINAL WORKFLOW', b: 'OpenCode connects credentials and exposes provider/model selection.' },
    { x: rightLeft + (rightW - 20) / 2 + 20, y: bodyTop, w: (rightW - 20) / 2, h: 164, n: '2', t: 'PROVIDER OPTIONS', b: 'NVIDIA and ZenMux can be evaluated without redesigning the developer workflow.' },
    { x: rightLeft, y: bodyTop + 184, w: (rightW - 20) / 2, h: 164, n: '3', t: 'BOUNDED ACCESS', b: 'Free prototype access and promotions are conditional—not a production entitlement.' },
    { x: rightLeft + (rightW - 20) / 2 + 20, y: bodyTop + 184, w: (rightW - 20) / 2, h: 164, n: '4', t: 'MEASURED DECISION', b: 'Four weeks can establish quality, reliability, governance, and cost evidence.' },
  ];
  addSlide([
    ...header('01 · EXECUTIVE SUMMARY', 'The opportunity is access without premature platform lock-in', 'Approve a bounded pilot; do not assume promotional access becomes the production model.', 2),
    rect(full.x, bodyTop, leftW, 368, K.midnight),
    tx('RECOMMENDATION', full.x + 28, bodyTop + 28, leftW - 56, 18, { size: 10, bold: true, color: K.cyan }),
    tx('Run a four-week pilot with a small engineering cohort.', full.x + 28, bodyTop + 70, leftW - 56, 90, { size: 31, face: SERIF, bold: true, color: K.white }),
    tx('The pilot should validate task quality, provider availability, data controls, rate limits, and cost per successful task before any production commitment.',
      full.x + 28, bodyTop + 184, leftW - 56, 112, { size: 15, color: '#B8C7D9' }),
    ...label('Decision: pilot', full.x + 28, bodyTop + 316, 150, { fill: '#12243A', color: K.cyan, border: K.cyan }),
    ...tiles.flatMap((d) => [
      roundRect(d.x, d.y, d.w, d.h, K.surface, K.line, 1),
      tx(d.n, d.x + 16, d.y + 14, 36, 34, { size: 24, face: SERIF, bold: true, color: K.cyan }),
      tx(d.t, d.x + 58, d.y + 20, d.w - 72, 20, { size: 10, bold: true, color: K.slate }),
      tx(d.b, d.x + 18, d.y + 66, d.w - 36, 80, { size: 12, color: K.gray }),
    ]),
    SRC('Sources: OpenCode provider docs; NVIDIA NIM FAQ; ZenMux and Kimi official model pages (accessed 22 Jul 2026).'),
  ], { notes: `Lead with the decision. The architecture is credible enough to test; the economics and operating fit are not yet proven.\n\nSources:\n${noteSources}` });
}

// 03 — Current pain / L04
{
  const painNodes = [
    ['Fragmented access', 'Separate subscriptions, credentials, and model catalogs', K.cyan],
    ['Configuration load', 'Provider-specific setup and uneven model metadata', K.teal],
    ['Unclear economics', 'Preview access and promotions can change by provider', K.paleBlue],
    ['Governance gap', 'Task data and model behavior need explicit controls', K.amber],
  ];
  addSlide([
    ...header('02 · CURRENT STATE', 'Cost and configuration fragment the developer experience', 'The friction is not one expensive model—it is the operating complexity across providers.', 3),
    ...chain(full.x, bodyTop + 30, full.w, painNodes, { nodeW: 244, nodeH: 118 }),
    rect(full.x, bodyTop + 212, full.w, 1, K.line),
    tx('BUSINESS IMPACT', full.x, bodyTop + 242, 180, 20, { size: 10, bold: true, color: K.cyan }),
    ...cols(3, { left: full.x, right: full.x + full.w }).flatMap((c, i) => {
      const items = [
        ['ACCESS', 'Students and junior developers can be priced out of high-quality assistance.'],
        ['PRODUCTIVITY', 'Teams lose time maintaining provider-specific setup and deciding which model to use.'],
        ['CONTROL', 'Unmeasured usage creates risk around data, quality, availability, and production cost.'],
      ][i];
      return miniCard(c.x, bodyTop + 280, c.w, 130, items[0], items[1], [K.cyan, K.teal, K.amber][i]);
    }),
  ], { notes: 'The source deck correctly identifies cost and access friction. This rebuild reframes the issue as an operating-model problem so the pilot can test a repeatable workflow rather than chase a static list of free models.' });
}

// 04 — Target operating model / L07
{
  const left = { x: cx(1), w: span(1, 3) };
  const center = { x: cx(4), w: span(4, 7) };
  const right = { x: cx(8), w: span(8, 12) };
  const rightCols = cols(2, { left: right.x, right: right.x + right.w, gutter: 14 });
  addSlide([
    ...header('03 · TARGET STATE', 'One terminal workflow can govern model choice by task', 'A stable developer experience sits above changing providers and models.', 4),
    ...miniCard(left.x, bodyTop + 34, left.w, 154, 'ENGINEER', 'One terminal interface\nOne permission model\nOne task workflow', K.slate),
    sh('rightArrow', left.x + left.w + 2, bodyTop + 98, 16, 18, K.cyan, K.cyan, 1),
    roundRect(center.x, bodyTop, center.w, 222, K.midnight, K.midnight, 1),
    tx('OPENCODE', center.x + 22, bodyTop + 24, center.w - 44, 30, { size: 22, face: SERIF, bold: true, color: K.white, align: 'center' }),
    tx('Connect credentials · select models · apply task policy', center.x + 22, bodyTop + 68, center.w - 44, 42, { size: 13, color: '#B8C7D9', align: 'center' }),
    ...label('/connect', center.x + 38, bodyTop + 132, 120, { fill: '#12243A', color: K.cyan, border: K.cyan }),
    ...label('/models', center.x + center.w - 158, bodyTop + 132, 120, { fill: '#12243A', color: K.teal, border: K.teal }),
    sh('rightArrow', center.x + center.w + 2, bodyTop + 98, 16, 18, K.teal, K.teal, 1),
    ...miniCard(rightCols[0].x, bodyTop, rightCols[0].w, 104, 'NVIDIA', 'Hosted prototype endpoints\nand downloadable NIMs', K.teal),
    ...miniCard(rightCols[1].x, bodyTop, rightCols[1].w, 104, 'ZENMUX', 'Aggregated models and\ntime-bound promotions', K.cyan),
    ...miniCard(rightCols[0].x, bodyTop + 120, rightCols[0].w, 102, 'PRIMARY', 'Best-fit model for\ncomplex implementation', K.paleBlue),
    ...miniCard(rightCols[1].x, bodyTop + 120, rightCols[1].w, 102, 'SPECIALIST', 'Speed, vision, or\nreasoning by task', K.green),
    rect(full.x, bodyTop + 270, full.w, 138, K.cool, K.line, 1),
    tx('GOVERNANCE PLANE', full.x + 22, bodyTop + 290, 180, 20, { size: 10, bold: true, color: K.cyan }),
    ...['Approved models', 'Secrets handling', 'Task/data policy', 'Quality tests', 'Usage & cost'].flatMap((t, i) => {
      const cs = cols(5, { left: full.x + 22, right: full.x + full.w - 22, gutter: 12 });
      return label(t, cs[i].x, bodyTop + 334, cs[i].w, { fill: K.white, color: K.slate, border: K.line });
    }),
    SRC('Source: OpenCode provider documentation — opencode.ai/docs/providers.'),
  ], { notes: `The target state is provider flexibility behind a consistent terminal experience and governance plane. OpenCode documents NVIDIA and ZenMux provider connections via /connect and model selection via /models.\n\nSource:\nhttps://opencode.ai/docs/providers` });
}

// 05 — AI workflow / L04
{
  const nodes = [
    ['Install', 'Launch OpenCode and confirm the terminal workflow', K.slate, 'flowChartAlternateProcess'],
    ['Connect', 'Add NVIDIA and ZenMux credentials through /connect', K.cyan, 'flowChartProcess'],
    ['Select', 'Use /models to choose an approved model by task', K.teal, 'flowChartDecision'],
    ['Measure', 'Capture quality, latency, failures, usage, and cost', K.green, 'flowChartProcess'],
  ];
  const roleCols = cols(4);
  addSlide([
    ...header('04 · AI WORKFLOW', 'The workflow is a four-step connection and selection loop', 'The pilot tests the operating loop—not a permanent commitment to any one model.', 5),
    ...chain(full.x, bodyTop + 18, full.w, nodes, { nodeW: 244, nodeH: 122 }),
    tx('TASK ROUTING PRINCIPLE', full.x, bodyTop + 184, 260, 20, { size: 10, bold: true, color: K.cyan }),
    ...roleCols.flatMap((c, i) => {
      const d = [
        ['QUICK EDIT', 'Favor speed and low overhead'],
        ['IMPLEMENTATION', 'Favor coding quality and tool use'],
        ['UI / VISION', 'Require verified multimodal support'],
        ['REASONING', 'Favor reliability on complex decisions'],
      ][i];
      return miniCard(c.x, bodyTop + 224, c.w, 130, d[0], d[1], [K.paleBlue, K.cyan, K.teal, K.green][i]);
    }),
    SRC('Source: OpenCode provider documentation — connection and model selection steps.'),
  ], { notes: `The documented OpenCode pattern is to connect a provider, then select from available models. Model names should be discovered at pilot time rather than hard-coded into the operating process.\n\nSource:\nhttps://opencode.ai/docs/providers` });
}

// 06 — Evidence / L10-like matrix
{
  const matrixCols = [
    { t: 'Verified proposition', w: 330 },
    { t: 'Current evidence', w: 560 },
    { t: 'Condition', w: 294 },
  ];
  const matrixRows = [
    ['Native provider workflow', 'OpenCode documents NVIDIA and ZenMux under /connect and model selection under /models.', 'Reconfirm in installed version'],
    ['Broad prototype catalog', 'NVIDIA catalog displayed 139 models on 22 Jul 2026; entries vary by free endpoint and download status.', 'Catalog changes over time'],
    ['Developer prototype access', 'NVIDIA Developer Program provides hosted NIM access for prototyping, research, development, and testing.', 'Production license required'],
    ['Kimi K3 capability', 'Official Kimi docs describe 2.8T parameters and up to 1M context.', 'Context depends on plan'],
    ['Promotional free route', 'ZenMux listed Kimi K3 Free at $0/M tokens for a limited time.', 'Promotion may expire'],
  ];
  addSlide([
    ...header('05 · PROOF OBJECTS', 'Official sources support the core proposition—with conditions', 'The credible claim is “pilot-ready access,” not “permanently free production.”', 6),
    ...table(full.x, bodyTop, full.w, matrixCols, matrixRows, { rowH: 64, headH: 36, highlight: 2 }),
    rect(full.x, bodyTop + 370, full.w, 46, K.softCyan, K.cyan, 1),
    tx('DECISION RULE', full.x + 18, bodyTop + 384, 120, 16, { size: 9, bold: true, color: K.cyan }),
    tx('Verify access, terms, and the available model list on day 1; freeze the tested configuration for the pilot.', full.x + 150, bodyTop + 379, full.w - 168, 24, { size: 13, bold: true, color: K.slate }),
    SRC('Sources: OpenCode · NVIDIA NIM FAQ/catalog · ZenMux K3 listing · Kimi Code model docs; accessed 22 Jul 2026.'),
  ], { notes: `Use this slide to distinguish facts from conditions. The NVIDIA developer route is for prototype/development use. ZenMux explicitly labels its Kimi K3 free listing as limited-time. Kimi's 1M context depends on membership tier.\n\nSources:\n${noteSources}` });
}

// 07 — Roadmap / L11
{
  const workCols = cols(4);
  const milestones = [
    ['WEEK 1', 'Baseline', 'Setup · tasks · controls', K.cyan, true],
    ['WEEK 2', 'Daily use', 'Coding cohort runs', K.teal, true],
    ['WEEK 3', 'Optimize', 'Routing · prompts · policy', K.paleBlue, false],
    ['WEEK 4', 'Decide', 'Evidence · economics · gate', K.green, false],
  ];
  addSlide([
    ...header('06 · IMPLEMENTATION ROADMAP', 'Four weeks is enough to test value and operating fit', 'Keep the cohort small, the tasks representative, and the exit criteria explicit.', 7),
    ...rail(full.x, bodyTop + 8, full.w, milestones),
    tx('WORKSTREAM OWNERSHIP', full.x, bodyTop + 172, 220, 20, { size: 10, bold: true, color: K.cyan }),
    ...workCols.flatMap((c, i) => {
      const d = [
        ['PLATFORM', 'Install, credentials, approved endpoints, version freeze'],
        ['ENGINEERING', 'Representative tasks, human review, defect capture'],
        ['SECURITY', 'Secrets, data classification, retention, access policy'],
        ['FINOPS', 'Usage, limits, cost per successful task, production scenario'],
      ][i];
      return miniCard(c.x, bodyTop + 210, c.w, 142, d[0], d[1], [K.cyan, K.teal, K.amber, K.green][i]);
    }),
    rect(full.x, bodyTop + 376, full.w, 40, K.midnight),
    tx('GATE', full.x + 18, bodyTop + 389, 70, 16, { size: 9, bold: true, color: K.cyan }),
    tx('Scale only if quality, reliability, governance, and production economics all meet the agreed threshold.', full.x + 92, bodyTop + 385, full.w - 110, 22, { size: 13, bold: true, color: K.white }),
  ], { notes: 'Week 1 establishes a frozen baseline. Weeks 2–3 test real work and refine routing. Week 4 compares evidence to the exit criteria. Do not expand the cohort before the gate.' });
}

// 08 — Metrics / L06
{
  const ks = cols(4);
  const metricData = [
    ['≤ 60 min', 'SETUP TIME', 'Target per participant', K.cyan],
    ['≥ 80%', 'TASK SUCCESS', 'Human-approved completion', K.green],
    ['≥ 95%', 'WORKFLOW RELIABILITY', 'Sessions without provider failure', K.teal],
    ['MEASURE', 'COST / SUCCESS', 'No assumed savings baseline', K.paleBlue],
  ];
  const scoreRows = [
    ['Quality', 'Acceptance rate · defects · rework', 'Human review rubric'],
    ['Speed', 'Cycle time versus cohort baseline', 'Comparable task set'],
    ['Reliability', 'Rate limits · failed calls · fallback use', 'Session telemetry'],
    ['Governance', 'Policy exceptions · sensitive-data events', 'Zero critical exceptions'],
    ['Economics', 'Usage and production-priced scenario', 'Cost per successful task'],
  ];
  addSlide([
    ...header('07 · METRICS & PILOT SCOPE', 'Pilot success is task quality, reliability, and controlled cost', 'Replace headline ROI claims with a scorecard the cohort can actually measure.', 8),
    ...ks.flatMap((c, i) => kpi(c.x, bodyTop, c.w, ...metricData[i])),
    ...table(full.x, bodyTop + 182, full.w, [
      { t: 'Dimension', w: 220 }, { t: 'Measure', w: 584 }, { t: 'Decision evidence', w: 380 },
    ], scoreRows, { rowH: 42, headH: 34 }),
    SRC('Targets are proposed pilot thresholds; they are not measured outcomes.'),
  ], { notes: 'The original deck asserted $0 monthly cost and a $100+ comparison without a measured baseline. This slide converts those claims into testable pilot metrics. Adjust thresholds with the sponsor before kickoff.' });
}

// 09 — Risks / L10
{
  const riskRows = [
    ['Promotion or access expires', 'High', 'Verify day 1; maintain a paid or alternate-provider fallback.'],
    ['Prototype terms do not cover production', 'High', 'Keep the pilot non-production; model enterprise licensing separately.'],
    ['Rate limits or model drift disrupt work', 'Medium', 'Freeze versions where possible; log failures; test fallback routing.'],
    ['Secrets or sensitive code leave policy boundary', 'High', 'Use approved repos/tasks; redact secrets; enforce data classification.'],
    ['Output quality creates hidden rework', 'Medium', 'Require human review, task rubrics, and defect/rework measurement.'],
  ];
  addSlide([
    ...header('08 · RISKS & MITIGATIONS', 'The main risks are commercial, operational, and governance-related', 'Each risk has a control, an owner, and a stop condition.', 9),
    ...table(full.x, bodyTop, full.w, [
      { t: 'Risk', w: 334 }, { t: 'Priority', w: 150 }, { t: 'Mitigation / stop condition', w: 700 },
    ], riskRows, {
      rowH: 58, headH: 36,
      colColor: (ri, ci) => ci === 1 ? (ri === 2 || ri === 4 ? K.amber : K.red) : (ci === 0 ? K.slate : K.gray),
    }),
    rect(full.x, bodyTop + 352, full.w, 64, K.cool, K.line, 1),
    tx('NO-GO CONDITION', full.x + 18, bodyTop + 374, 150, 18, { size: 10, bold: true, color: K.red }),
    tx('Stop if the pilot cannot meet data-policy requirements or if provider terms do not permit the intended test.', full.x + 170, bodyTop + 369, full.w - 188, 26, { size: 13, bold: true, color: K.slate }),
    SRC('Commercial terms: NVIDIA NIM FAQ and ZenMux K3 listing; accessed 22 Jul 2026.'),
  ], { notes: `This replaces the original slide 9, which repeated the setup checklist rather than presenting risks. The highest risks are terms, data handling, and hidden rework—not installation.\n\nSources:\nhttps://docs.api.nvidia.com/nim/docs/product\nhttps://zenmux.ai/provider/moonshotai` });
}

// 10 — Ask / L14
{
  const right = { x: cx(6), w: span(6, 12) };
  const left = { x: cx(1), w: span(1, 5) };
  addSlide([
    rect(0, 0, 1280, 720, K.white),
    rect(0, 0, 520, 720, K.midnight),
    tx('09 · PILOT DECISION', left.x, 42, left.w, 18, { size: 10, bold: true, color: K.cyan }),
    tx('Approve a bounded pilot with explicit exit criteria', left.x, 92, left.w, 132, { size: 38, face: SERIF, bold: true, color: K.white }),
    tx('Four weeks · small cohort · non-production scope', left.x, 254, left.w, 54, { size: 17, color: '#B8C7D9' }),
    ...label('Decision requested', left.x, 344, 174, { fill: '#12243A', color: K.cyan, border: K.cyan }),
    tx('Authorize setup, representative engineering tasks,\nsecurity review, and measured provider evaluation.', left.x, 400, left.w - 22, 100, { size: 14, bold: true, color: K.white }),
    tx('SUCCESS CONDITIONS', right.x, 54, right.w, 20, { size: 10, bold: true, color: K.cyan }),
    ...checkItem('Quality threshold met on representative tasks', right.x, 104, right.w),
    ...checkItem('Provider reliability and fallback behavior proven', right.x, 158, right.w),
    ...checkItem('Data and secrets controls approved', right.x, 212, right.w),
    ...checkItem('Production-priced scenario is acceptable', right.x, 266, right.w),
    rect(right.x, 326, right.w, 1, K.line),
    tx('FIRST 72 HOURS', right.x, 356, right.w, 20, { size: 10, bold: true, color: K.teal }),
    ...miniCard(right.x, 396, (right.w - 20) / 2, 128, '1 · VERIFY', 'Confirm terms, catalog, model IDs, access limits, and data policy.', K.cyan),
    ...miniCard(right.x + (right.w - 20) / 2 + 20, 396, (right.w - 20) / 2, 128, '2 · BASELINE', 'Select the cohort, freeze versions, and record benchmark tasks.', K.teal),
    tx('OUTCOME', right.x, 556, 84, 16, { size: 9, bold: true, color: K.cyan }),
    tx('A measured decision to scale, revise, or stop—without platform lock-in.', right.x + 88, 550, right.w - 88, 30, { size: 15, face: SERIF, bold: true, color: K.slate }),
    ...footer(10),
  ], { notes: 'The ask is not permission to deploy to production. It is permission to run a controlled four-week experiment with defined ownership, measurements, and stop conditions.' });
}

await (await PresentationFile.exportPptx(P)).save(OUT);

for (let i = 0; i < P.slides.count; i += 1) {
  const blob = await P.export({ format: 'png', slide: P.slides.getItem(i), scale: 1 });
  const path = `${RENDERS}/slide-${String(i + 1).padStart(2, '0')}.png`;
  await writeFile(path, Buffer.from(await blob.arrayBuffer()));
}

console.log(JSON.stringify({ output: OUT, slides: P.slides.count, renders: RENDERS }, null, 2));

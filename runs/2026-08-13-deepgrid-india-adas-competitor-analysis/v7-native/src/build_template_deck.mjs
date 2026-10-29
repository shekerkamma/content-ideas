// build_template_deck.mjs — the ADAPTED prompt-template deck.
//
// Deliverable 1 of 2. Replicates the supplied guide's page architecture exactly
// (`accenture-style-claude-guide-draft.pptx`): every slide IS a prompt template,
// carrying WHEN TO USE · WORKFLOW · KEY PROMPT · OUTPUT INCLUDES.
//
// Tokens and geometry are measured from that file, not approximated:
//   accent #00C9A7 · chip #E0F7F1 · prompt box #0A1628 · amber label #FFB800
//   ink #1B2B3C · muted #5B6B7C · Calibri throughout · 1280x720 stage
//
// The seven patterns are adapted to this deck's content — each exists because
// profiling all 73 dossier slides actually found that structure.
//
//   DECK_RUN=<dir> DECK_NAME=<slug> [DECK_RENDER=1] node src/build_template_deck.mjs
import { readFile, writeFile, mkdir } from 'node:fs/promises';

const AT = process.env.ARTIFACT_TOOL_DIST || 'file:///home/sheke/.local/artifact-tool-linux/dist';
const { Presentation, PresentationFile, layers: composeLayers } = await import(`${AT}/artifact_tool.mjs`);
const { textStyle, stroke } = await import(`${AT}/presentation-jsx/index.mjs`);
const { jsx, jsxs } = await import(`${AT}/presentation-jsx/jsx-runtime.mjs`);

const RUN = process.env.DECK_RUN || '.';
const G = {                                   // measured from the guide
  green: '#00C9A7',                           // fills + rules only (non-text: exempt)
  greenTx: '#00755F',                         // the text-safe green: 5.66:1 on white
  chip: '#E0F7F1', navy: '#0A1628', navy2: '#12243A',
  ink: '#1B2B3C', muted: '#5B6B7C', amber: '#FFB800',
  deep: '#00695C',                            // 5.90:1 on the chip (guide's was 3.12:1)
  white: '#FFFFFF',
};
const F = 'Calibri';
const pt = (v) => v / 0.75;                   // guide sizes are in points

const P = Presentation.create();
const C = P.compose;
const Text = ({ children = '', ...p }) => C.text(String(children), p);
const Shape = (p) => C.shape(p);
const Layers = ({ children = [], ...p }) => composeLayers(p, Array.isArray(children) ? children : [children]);

const st = (o) => textStyle(`font: ${o.bold ? 'bold ' : ''}${o.size}px ${o.face || F}; `
  + `color: ${o.color}; align: ${o.align || 'left'}; anchor: ${o.anchor || 'top'}; inset: 0px; autofit: shrink`);
const tx = (t, x, y, w, h, o) => jsx(Text, {
  width: C.fixed(Math.max(4, w)), height: C.fixed(Math.max(6, h)),
  position: { left: x, top: y }, style: st(o), children: o.caps ? String(t).toUpperCase() : t });
const box = (x, y, w, h, fill, lc = 'none', lw = 0) => jsx(Shape, {
  geometry: 'rect', width: C.fixed(Math.max(1, w)), height: C.fixed(Math.max(1, h)), fill,
  line: lc === 'none' ? stroke('0px none') : stroke(`${lw}px solid ${lc}`), position: { left: x, top: y } });

const TOTAL = 9;
function chrome(page) {
  return [
    box(0, 0, 1280, 720, G.white),
    box(0, 0, 1280, 13, G.green),                 // top rule
    box(0, 0, 6, 720, G.navy),                    // left edge
    tx('DeepGrid India ADAS Dossier  |  Adapted Prompt Templates', 58, 680, 864, 20,
       { size: pt(10), color: G.muted }),
    tx(`${page} / ${TOTAL}`, 1155, 678, 67, 20,
       { size: pt(10), bold: true, color: G.ink, align: 'right' }),
  ];
}

// one prompt-template page, laid out on the guide's grid
function templateSlide({ domain, name, when, workflow, prompt, outputs, page }) {
  const el = [...chrome(page)];
  el.push(box(62, 24, 442, 27, G.chip));
  el.push(tx(domain, 62, 29, 442, 20, { size: pt(11), bold: true, color: G.deep, align: 'center', caps: true }));
  el.push(tx(name, 62, 56, 1162, 50, { size: pt(32), bold: true, color: G.ink }));
  el.push(box(62, 130, 211, 4, G.green));

  el.push(tx('When to use', 62, 142, 576, 20, { size: pt(11), bold: true, color: G.greenTx, caps: true }));
  el.push(box(62, 165, 499, 4, G.chip));
  when.forEach((b, i) => el.push(tx(`•  ${b}`, 62, 173 + i * 22, 499, 20, { size: pt(11.5), color: G.ink })));

  el.push(tx('Workflow', 62, 288, 576, 20, { size: pt(11), bold: true, color: G.greenTx, caps: true }));
  el.push(box(62, 309, 499, 4, G.chip));
  workflow.forEach((w, i) => {
    const y = 317 + i * 62;
    el.push(box(62, y, 27, 27, G.green));
    el.push(tx(String(i + 1), 62, y + 4, 27, 20, { size: pt(11), bold: true, color: G.navy, align: 'center' }));
    el.push(tx(w, 96, y + 1, 463, 52, { size: pt(11.5), color: G.ink }));
    if (i < workflow.length - 1) el.push(box(96, y + 50, 463, 1, G.chip));
  });

  el.push(box(586, 142, 653, 254, G.navy));
  el.push(tx('Key prompt  →  Tell Claude:', 605, 152, 614, 22, { size: pt(11), bold: true, color: G.amber, caps: true }));
  el.push(tx(`"${prompt}"`, 605, 182, 614, 200, { size: pt(12.5), color: G.white }));

  el.push(tx('Output includes', 586, 408, 576, 20, { size: pt(11), bold: true, color: G.greenTx, caps: true }));
  el.push(box(586, 429, 653, 4, G.green));
  outputs.forEach((o, i) => {
    const col = i < Math.ceil(outputs.length / 2) ? 0 : 1;
    const row = col === 0 ? i : i - Math.ceil(outputs.length / 2);
    const x = col === 0 ? 586 : 922;
    const y = 444 + row * 36;
    el.push(box(x, y, 6, 6, G.green));
    el.push(tx(o, x + 14, y - 6, 317, 32, { size: pt(11), color: G.ink }));
  });

  const s = P.slides.add(); s.setViewportSize(1280, 720);
  s.compose(jsxs(Layers, { width: C.fixed(1280), height: C.fixed(720), children: el }));
  s.speakerNotes.text = `${domain} — ${name}\n\nKEY PROMPT:\n${prompt}\n\nOUTPUT INCLUDES:\n- ${outputs.join('\n- ')}`;
}

// ── cover ────────────────────────────────────────────────────────────────
{
  const el = [
    box(0, 0, 1280, 720, G.navy), box(0, 0, 1280, 13, G.green),
    tx('PROMPT TEMPLATES FOR COMPETITOR DOSSIERS', 62, 188, 900, 22,
       { size: pt(11), bold: true, color: G.green, caps: true }),
    tx('The Adapted\nIndia ADAS\nPrompt Template Set', 62, 224, 900, 190,
       { size: pt(44), bold: true, color: G.white }),
    tx('7 evidence patterns  ·  4 domains  ·  1 typed content envelope each',
       62, 432, 900, 26, { size: pt(14), color: '#A3B5C8' }),
    box(62, 476, 88, 4, G.green),
    ...[['7', 'Patterns'], ['4', 'Domains'], ['73', 'Slides profiled'], ['565', 'Ledger claims']]
      .flatMap(([n, l], i) => [
        tx(n, 62 + i * 190, 512, 170, 52, { size: pt(30), bold: true, color: G.green }),
        tx(l, 62 + i * 190, 562, 170, 18, { size: pt(10), bold: true, color: '#A3B5C8', caps: true })]),
    tx('Derived from the supplied Accenture-style guide  ·  adapted to this deck’s content',
       58, 680, 900, 20, { size: pt(10), color: '#A3B5C8' }),
    tx('1 / 9', 1155, 678, 67, 20, { size: pt(10), bold: true, color: '#A3B5C8', align: 'right' }),
  ];
  const s = P.slides.add(); s.setViewportSize(1280, 720);
  s.compose(jsxs(Layers, { width: C.fixed(1280), height: C.fixed(720), children: el }));
  s.speakerNotes.text = 'Cover. Format replicated from the supplied guide; patterns adapted to this deck’s content.';
}

// ── contents ─────────────────────────────────────────────────────────────
{
  const el = [...chrome(2)];
  el.push(tx('What’s Inside', 62, 40, 1162, 56, { size: pt(32), bold: true, color: G.ink }));
  el.push(tx('7 patterns  ·  4 domains  ·  each with a copy-paste prompt and a typed content envelope',
             62, 100, 1000, 22, { size: pt(12), color: G.muted }));
  el.push(box(62, 132, 211, 4, G.green));
  const doms = [
    ['01  Evidence Posture', ['P1  Evidence Ladder — 21 slides', 'P7  Confidence Register — 1 slide']],
    ['02  Competitive Structure', ['P2  Threat × Arena Matrix — 11 slides']],
    ['03  Bounded Action', ['P3  Staged Move — 18 slides', 'P4  Bounded Argument — 18 slides']],
    ['04  Execution & Economics', ['P5  Dated Plan — 2 slides', 'P6  Cost Bridge — 2 slides']],
  ];
  doms.forEach((d, i) => {
    const x = 62 + (i % 2) * 600, y = 176 + Math.floor(i / 2) * 200;
    el.push(box(x, y, 560, 27, G.chip));
    el.push(tx(d[0], x + 12, y + 5, 540, 20, { size: pt(11), bold: true, color: G.deep, caps: true }));
    d[1].forEach((m, j) => {
      el.push(box(x, y + 46 + j * 40, 6, 6, G.green));
      el.push(tx(m, x + 16, y + 38 + j * 40, 520, 30, { size: pt(12.5), color: G.ink }));
    });
  });
  el.push(box(62, 596, 1162, 1, G.chip));
  el.push(tx('Each pattern exists because profiling all 73 dossier slides found that structure in the content. '
            + 'A pattern earns its exhibit only when the evidence can actually draw it.',
             62, 612, 1000, 40, { size: pt(11), color: G.muted }));
  const s = P.slides.add(); s.setViewportSize(1280, 720);
  s.compose(jsxs(Layers, { width: C.fixed(1280), height: C.fixed(720), children: el }));
  s.speakerNotes.text = 'Contents: 7 patterns across 4 domains.';
}

// ── the seven pattern templates ──────────────────────────────────────────
const PATTERNS = [
 { domain: 'Domain 1: Evidence Posture', name: 'P1 · Evidence Ladder', page: 3,
   when: ['A competitor or claim carries mixed-quality evidence',
          'Leadership is treating a company statement as verified fact',
          'The rating rests on what is known versus what is asserted'],
   workflow: ['Split every statement into verified fact, attributed claim, qualified interpretation, insufficient evidence',
              'Assign each a confidence and name the artifact that would raise it',
              'Convert the weakest load-bearing rung into the decision'],
   prompt: 'Build an evidence ladder for [subject] as of [date] using only [evidence IDs]. Produce four rungs ordered strongest to weakest. For each give the label, the statement in one sentence, its status, a confidence between 0 and 1, and the named artifact that would raise it. Do not merge rungs of different status. End with the response decision, the owner, and the artifact that moves the rating.',
   outputs: ['Observable Position (1 paragraph)', 'Rungs[] with status + confidence', 'Named artifact that raises each rung',
             'Evidence gap holding the rating', 'Response decision · owner · trigger', 'EXHIBIT: rung width = confidence'] },

 { domain: 'Domain 1: Evidence Posture', name: 'P7 · Confidence Register', page: 4,
   when: ['Many claims of uneven quality must be prioritised for diligence',
          'The team needs to know what to purge from client-facing material',
          'Before a board review or an external pitch'],
   workflow: ['List the load-bearing claims behind the plan',
              'Score each by importance and evidence strength on the same 1–3 scale',
              'Purge high-importance, low-evidence claims and name the test'],
   prompt: 'Register the load-bearing claims behind [plan]. Score each on importance 1–3 and evidence strength 1–3, using the same scale throughout. Identify which are load-bearing — high importance, low evidence. Convert those into a purge list and a test plan with owners. End with the rule for what may appear in client-facing material.',
   outputs: ['Claims[] scored importance × evidence', 'Confidence band per claim', 'Load-bearing claims flagged',
             'Purge list for external material', 'Publication rule', 'EXHIBIT: scored dot register'] },

 { domain: 'Domain 2: Competitive Structure', name: 'P2 · Threat × Arena Matrix', page: 5,
   when: ['A competitor’s power differs by who is buying',
          'Effort is allocated by brand rather than by arena',
          'One threat rating is hiding where exposure actually sits'],
   workflow: ['Fix the arenas and the control point each one rewards',
              'Rate the competitor per arena with the single fact behind each cell',
              'Name the arena to defend, to concede, and the inversion signal'],
   prompt: 'Rate [competitor] across [arenas] on the control point each arena rewards. For every cell give a rating from HIGHEST / HIGH / MEDIUM-HIGH / MEDIUM / LOW-MEDIUM / LOW and the single fact behind it in under twelve words. Explain in one sentence why the rating changes between arenas — the mechanism, not a restatement. End with the arena to defend, the arena to concede, and the signal that would invert the ranking.',
   outputs: ['Matrix: arenas × dimensions', 'Rating + supporting fact per cell', 'Variance mechanism (1 sentence)',
             'Defend / concede verdict', 'Inversion signal', 'EXHIBIT: heatmap, colour = rating'] },

 { domain: 'Domain 3: Bounded Action', name: 'P3 · Staged Move', page: 6,
   when: ['A bounded action is proposed against a rival or partner',
          'The move must be testable and abandonable, not open-ended',
          'Sales or BD needs a sequence, not a feature comparison'],
   workflow: ['State the rival’s advantage as a mechanism',
              'Design the narrowest sequence that tests it, marking what is reversible',
              'Set the gate that escalates and the condition that abandons'],
   prompt: 'Design a bounded staged move for [company] against [competitor]. Give 3–4 stages in order. For each: a label of at most 30 characters, what happens in one sentence, whether it is reversible, and its commitment level. The final stage must be a decision gate with an explicit escalate condition. State their advantage as a mechanism first. End with the abandonment rule — do not propose a feature-for-feature response.',
   outputs: ['Their mechanism (1 sentence)', 'Stages[] with reversibility', 'Commitment level per stage',
             'Escalate condition', 'Abandonment rule', 'EXHIBIT: numbered chain with arrows'] },

 { domain: 'Domain 3: Bounded Action', name: 'P4 · Bounded Argument', page: 7,
   when: ['The page carries an argument rather than a dataset',
          'A position must survive a hostile question',
          'No structured evidence exists — the reasoning is the exhibit'],
   workflow: ['State the position answer-first',
              'Give the three stances a reader could take and what each rests on',
              'Close on the one that survives, and what would overturn it'],
   prompt: 'Argue [position] for [audience]. Give exactly three stances: the position taken, the strongest opposing stance, and the bounded middle. For each give the claim in one sentence and what it rests on. Mark which stance the evidence currently supports. Do not hedge the losing stances — state them at full strength. End with the decision, the owner, and the observable that would overturn the chosen stance.',
   outputs: ['Three stances: taken / opposing / bounded', 'What each rests on', 'Which the evidence supports',
             'Overturning observable', 'Decision · owner · trigger', 'EXHIBIT: three-stance bar'] },

 { domain: 'Domain 4: Execution & Economics', name: 'P5 · Dated Plan', page: 8,
   when: ['Claims must become artifacts inside a fixed window',
          'Funding should release on evidence rather than on calendar',
          'Several workstreams are running without gates'],
   workflow: ['Set the window and the artifact each phase must produce',
              'Sequence so each phase unlocks the next',
              'Attach a gate, an owner and a stop condition to every phase'],
   prompt: 'Build a [duration] plan for [company] that converts claims into reproducible artifacts. Give 3–5 phases. For each: the window as written on a chart, its span in weeks, the artifact it must produce, the owner, and the gate that releases the next phase. Sequence so each phase unlocks the following one. End with the condition under which the plan stops rather than continues.',
   outputs: ['Target outcome', 'Phases[] with span in weeks', 'Artifact per phase (never an activity)',
             'Gate and owner per phase', 'Stop condition', 'EXHIBIT: timeline rail, spans to scale'] },

 { domain: 'Domain 4: Execution & Economics', name: 'P6 · Cost Bridge', page: 9,
   when: ['A cost advantage is claimed but not modelled',
          'Capital is requested against a projected unit price',
          'A die-level number is compared to a system price'],
   workflow: ['State today’s delivered cost and what it includes',
              'Bridge to the target through every element that must be carried',
              'Gate the commitment on the model, not on the direction'],
   prompt: 'Build the cost bridge from [current] to [target] for [company]. Give each step as a label, a display amount, a numeric value for the bar height, and whether the magnitude is verified or directional. Carry every element that must be paid: NRE, yield, package, qualification, warranty, lifecycle. State explicitly whether a projected die price is comparable to a system price. End with the gate that must clear before capital is committed.',
   outputs: ['Steps[] with value and verified flag', 'Base → add → target sequence', 'Comparability rule',
             'Directional caveat where unverified', 'Capital gate', 'EXHIBIT: waterfall, height = magnitude'] },
];
PATTERNS.forEach(templateSlide);

const OUT = `${RUN}/${process.env.DECK_NAME || 'prompt-templates'}-draft.pptx`;
await (await PresentationFile.exportPptx(P)).save(OUT);
console.log(`DONE: ${P.slides.count} slides -> ${OUT}`);

if (process.env.DECK_RENDER) {
  const dir = `${RUN}/qa/renders-templates`;
  await mkdir(dir, { recursive: true });
  for (let i = 0; i < P.slides.count; i += 1) {
    const b = await P.export({ format: 'png', slide: P.slides.getItem(i), scale: 1 });
    await writeFile(`${dir}/slide-${String(i + 1).padStart(2, '0')}.png`, Buffer.from(await b.arrayBuffer()));
  }
  console.log(`  rendered ${P.slides.count} PNGs -> ${dir}`);
}

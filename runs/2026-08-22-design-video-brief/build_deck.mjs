// Client-Ready PPTX — /design video brief (frame-grounded)
//
// Content source: frame-evidence.md. The first cut was built from captions only and was
// correspondingly thin — a screencast's substance is on screen, and narration is the
// weakest of this repo's three evidence tiers. Re-pulled at 1080p (the default download
// offers only 640x360, at which none of the UI text is legible) and read off frames.
// Built with artifact-tool presentation JSX per vault-presales-pptx-pipeline's PowerPoint
// Rule. Storyline from story-pack.md / slide-plan.json. Every card height is 'auto'.
//
//   DECK_RUN=<dir> DECK_NAME=<slug> DECK_FOOTER='...' node build_deck.mjs

import {
  P, C, K, SERIF, PresentationFile,
  tx, rect, roundRect, ellipse, sh, addSlide, OUT,
} from '/home/sheke/.claude/skills/vault-presales-pptx-pipeline/assets/deck-kit.mjs';
// Chrome and components come from the spec-corrected scale — the kit sets the design
// system's POINT numbers as PIXEL values, so its type renders ~25% under floor.
import { header, headerDark, footer, card, kpi, table, chain, rail, SRC, T }
  from './kit-spec.mjs';
import { cols, cx, span, GRID } from '/home/sheke/.claude/skills/vault-presales-pptx-pipeline/assets/deck-grid.mjs';

const BODY = GRID.bands.BODY[0];          // 168
const SOURCE = 'Brendan Jowett · “Master NEW /design Claude Skill In 10 Minutes!” · youtube.com/watch?v=IHPcOvVU4PM';

// ── 1 · L01 Cover ────────────────────────────────────────────────────────────
addSlide([
  rect(0, 0, 1280, 720, K.midnight),
  rect(0, 0, 1280, 4, K.cyan),
  tx('VIDEO BRIEF · CLAUDE CODE /DESIGN', 48, 96, 900, 22, { size: T.kicker, bold: true, color: K.cyan }),
  rect(48, 140, 132, 3, K.cyan),
  tx('The narration says he forgot to save.\nThe screen says something better.',
     48, 182, 1150, 200, { size: T.cover - 6, face: SERIF, bold: true, color: K.white }),
  tx('Reading a twelve-minute screencast off its frames instead of its captions — and finding an agent that writes files, versions them, and reviews your work.',
     48, 400, 1100, 60, { size: T.sub, color: '#A9BACD' }),
  rect(48, 486, 1184, 1, '#23364C'),
  ...[['954', 'LINES OF .DC.HTML WRITTEN'], ['8', 'ARTBOARDS DIFFED'], ['3', 'EDITS FOUND']]
    .map(([n, l], i) => [
      tx(n, 48 + i * 300, 506, 280, 56, { size: T.kpiNum - 6, face: SERIF, bold: true, color: K.cyan }),
      tx(l, 48 + i * 300, 566, 280, 20, { size: T.kpiLab, bold: true, color: '#8FA2B7' }),
    ]).flat(),
  tx('Brendan Jowett · "Master NEW /design Claude Skill In 10 Minutes!" · youtube.com/watch?v=IHPcOvVU4PM',
     48, 664, 1100, 20, { size: T.foot, color: '#6E8199' }),
], { background: K.midnight, notes: 'Frames re-pulled at 1080p with --extractor-args youtube:player_client=default,mweb,web_embedded. The default download is 640x360 and none of the on-screen text is legible at that size.' });

// ── 2 · Executive summary ────────────────────────────────────────────────────
{
  const k = cols(3, { left: cx(6), right: 1232 });
  addSlide([
    ...header('Executive summary', 'The command is the small half. The file trail is the story.',
              'What /design actually did, read off the build log rather than the narration.', 2),
    roundRect(48, BODY, span(1, 5), 468, K.midnight),
    rect(48, BODY, 6, 468, K.cyan),
    tx('What one prompt produced', 76, BODY + 30, span(1, 5) - 56, 28, { size: T.cardH, bold: true, color: K.white }),
    tx('Five named .dc.html artboards, written as files and announced one by one. A canvas.json manifest. A reference recreation of the live site as the entry artboard. A capability check. Then a published artifact URL.\n\nNone of that is in the captions.',
       76, BODY + 74, span(1, 5) - 56, 250, { size: T.sub, color: '#A9BACD' }),
    rect(76, BODY + 372, 64, 2, K.amber),
    tx('The narration for all of it: "it was able to give me each of these design variations."',
       76, BODY + 392, span(1, 5) - 56, 60, { size: T.body, italic: true, color: '#8FA2B7' }),
    ...kpi(k[0].x, BODY, k[0].w, '954', 'lines written', 'across five artboards', K.cyan),
    ...kpi(k[1].x, BODY, k[1].w, '8', 'artboards diffed', 'to read one hand-edit back', K.teal),
    ...kpi(k[2].x, BODY, k[2].w, '2', 'defects called', 'one fixed, one deliberately not', K.amber),
    ...card(cx(6), BODY + 190, span(6, 12), 'auto', 'The claim this brief makes',
            'The interesting object is not the canvas. It is an agent that writes named files, publishes them as versioned artifacts, diffs those versions to recover your hand-edits, reviews what you changed, and declines to guess when your intent is ambiguous.',
            K.amber, K.surface),
  ], { notes: 'All figures read off frames at 04:36 and 12:02. See frame-evidence.md.' });
}

// ── 3 · The build log ────────────────────────────────────────────────────────
addSlide([
  ...header('What it built', 'Five directions, five files, each announced as it landed',
            'The agent narrates its own build in the transcript pane — none of it is spoken.', 3),
  ...table(48, BODY, 1184, [
    { t: 'File', w: 260 },
    { t: 'Lines', w: 110, a: 'right' },
    { t: 'Direction', w: 380 },
    { t: 'What the agent said next', w: 434 },
  ], [
    ['Editorial.dc.html', '+199', 'Light, print-inspired broadsheet', '"Direction 1 done. Now the terminal direction."'],
    ['Terminal.dc.html', '+196', 'Dark, laid out as a shell session', '"Two down. Next: the brutalist poster grid."'],
    ['Brutalist.dc.html', '+176', 'Poster grid, heavy type', '"Three down. Now the atmospheric dark direction."'],
    ['Aurora.dc.html', '+168', 'Atmospheric dark', '"Four down. Last one: the Swiss spec-sheet."'],
    ['SpecSheet.dc.html', '+215', 'Swiss spec-sheet', '"Now the entry artboard — a reference recreation."'],
    ['canvas.json', '+28', 'The manifest that lays them out', '"Checks out. Loading the capability roster."'],
  ], { rowH: 42, highlight: 5 }),
  ...card(48, BODY + 320, 1184, 'auto', 'And one honest aside, mid-build',
          '"Heredoc quoting is fighting the content; switching to the file writer." The agent hits a real tooling problem and changes approach on camera — the kind of moment a polished demo usually edits out.',
          K.teal, K.surface),
], { notes: 'Frame 04:36. Line counts are the +N figures beside each Created line. 199+196+176+168+215 = 954.' });

// ── 4 · The canvas is a document ─────────────────────────────────────────────
addSlide([
  ...header('The artefact', 'Eight artboards, a manifest, and a published URL',
            'The canvas is a real document with an address — not a panel bolted into the app.', 4),
  ...chain(48, BODY + 10, 1184, [
    ['Entry artboard', 'A recreation of the live site, to compare against', K.gray, 'flowChartAlternateProcess'],
    ['Five directions', 'In a row below, "deliberately spread far apart"', K.cyan],
    ['canvas.json', 'Positions, entry file, launch view', K.cyan],
    ['A published artifact', 'claude.ai/code/artifact/6d74e446…', K.teal, 'flowChartAlternateProcess'],
  ], { nodeH: 112 }),
  ...card(48, BODY + 150, span(1, 6), 'auto', 'What the skill description says on screen',
          '"Published as an Artifact… You DRAFT the design as .dc.html artboards laid out on one pan/zoom canvas; where saving is enabled… Save publishes a new version for everyone, otherwise they get a view-and-export preview."',
          K.cyan),
  ...card(cx(7), BODY + 150, span(7, 12), 'auto', 'What gets read aloud',
          'The first six words. The command menu is on screen for eleven seconds with the whole contract visible in it, and the walkthrough moves straight past.',
          K.amber, K.surface),
  ...card(48, BODY + 320, 1184, 'auto', 'Also on that menu, never mentioned',
          'design-sync · design-revoke · design-consent · artifact-design · frontend-design. Five sibling commands, one of which grants an agent ongoing access to your design projects.',
          K.amber, K.surface),
], { notes: 'Frame 03:19 — the slash menu with the full description panel legible beside it.' });

// ── 5 · The panel is a DOM inspector ─────────────────────────────────────────
addSlide([
  ...header('The panel', 'Not "similar to Figma" — a DOM inspector with a debug readout',
            'What the properties panel actually exposes, read off the frame.', 5),
  ...table(48, BODY, 1184, [
    { t: 'Section', w: 240 },
    { t: 'Controls visible on screen', w: 620 },
    { t: 'What that tells you', w: 324 },
  ], [
    ['Edit · Code · Tweaks', 'Three tabs; the walkthrough only ever opens Edit', 'Two modes go undemonstrated'],
    ['Sizing', 'Width / Height with Hug · Fixed · Fill, plus min and max', 'CSS box model, not canvas geometry'],
    ['Position', 'Inline · Absolute, plus offset', 'Flow layout, not coordinates'],
    ['Padding · Margin', 'None · All · X & Y · Individual', 'Real spacing model'],
    ['Debug', '{"tid":25,"tag":"span","parent":"h1","attrs":{"class":"mark"}}', 'The artboard is DOM'],
  ], { rowH: 44, highlight: 4 }),
  ...card(48, BODY + 288, 1184, 'auto', 'And the Save button is in that same frame',
          'Top right, beside the panel toggle, visible from 07:50 — four minutes before the demo breaks and he goes looking for it. Nothing was hidden; it simply was not part of the mental model yet.',
          K.amber, K.surface),
], { notes: 'Frame 07:50. The Debug line is the strongest single piece of evidence that .dc.html artboards render as real DOM.' });

// ── 6 · THE TURN ─────────────────────────────────────────────────────────────
addSlide([
  rect(0, 0, 1280, 720, K.midnight),
  rect(0, 0, 6, 720, K.amber),
  tx('THEN THE DEMO BROKE', 92, 226, 900, 24, { size: T.kicker, bold: true, color: K.amber }),
  tx('He hosted the site.\nHis edits weren’t on it.',
     92, 268, 1060, 200, { size: T.cover - 10, face: SERIF, bold: true, color: K.white }),
  tx('The narration explains it in nine words: "the one thing I forgot to do is save."',
     92, 480, 1000, 40, { size: T.sub, color: '#A9BACD' }),
  tx('The screen spends the next minute doing something far more useful.',
     92, 520, 1000, 40, { size: T.sub, italic: true, color: K.amber }),
  ...footer(6, true),
], { background: K.midnight, notes: 'Frame 11:44 / 12:02. Let the failure land before the recovery.' });

// ── 7 · What the agent actually did ──────────────────────────────────────────
addSlide([
  ...header('The recovery', 'It diffed eight artboards across two versions to find three edits',
            'Version 1787189090 to 1787190748 — and only 03a had changed.', 7),
  ...table(48, BODY, 1184, [
    { t: 'Your edit, recovered from the diff', w: 800 },
    { t: 'Applied', w: 384, a: 'center' },
  ], [
    ['"Jowett" → JOWETT', '✓'],
    ['Name block: magenta #FF00E3, 789×148, 50px radius', '✓'],
    ['"Building in public" badge: yellow #FFCF2F, 50px radius', '✓'],
  ], { rowH: 46 }),
  ...card(48, BODY + 200, span(1, 6), 'auto', 'It also fixed what the edit would have broken',
          'The name block was fixed at 789×148px against 168px type — it would break on a responsive page. Re-expressed in em: computes to exactly 789×148 at 168px and scales with the headline. "Verified at desktop and at 375px, no overflow either way."',
          K.teal),
  ...card(cx(7), BODY + 200, span(7, 12), 'auto', 'And it corrected its own diagnosis',
          '"I leaned on ‘you probably didn’t save’ when the more useful move was to just ask you to save and re-check, which is what got there."',
          K.gray, K.surface),
], { notes: 'Frame 12:02. Version identity is explicit and addressable: 1787190748-9864. Local site at localhost:4173.' });

// ── 8 · The refusal ──────────────────────────────────────────────────────────
addSlide([
  ...header('The judgement call', 'It found an accessibility defect and refused to fix it',
            'The most instructive thirty seconds in the video, and none of it is narrated.', 8),
  roundRect(48, BODY, 1184, 150, K.surface, K.line, 1),
  rect(48, BODY, 6, 150, K.amber),
  tx('"White on #FFCF2F is about 1.5:1 contrast — effectively unreadable, especially at 13px. Your edit only changed the background, so I left the text colour alone rather than assume."',
     78, BODY + 32, 1120, 100, { size: T.cardH + 2, italic: true, color: K.slate }),
  ...cols(3).map((c, i) => {
    const t = [['Found it', 'Measured the contrast of an edit the human made by hand'],
               ['Priced the fix', 'Black gives roughly 13:1 and keeps the poster look'],
               ['Left it alone', 'Changing the background is not consent to change the text']][i];
    return [
      rect(c.x, BODY + 190, c.w, 3, [K.cyan, K.teal, K.amber][i]),
      tx(t[0].toUpperCase(), c.x, BODY + 206, c.w, 22, { size: T.kicker, bold: true, color: [K.cyan, K.teal, K.amber][i] }),
      tx(t[1], c.x, BODY + 234, c.w, 90, { size: T.body, color: K.gray }),
    ];
  }).flat(),
  ...card(48, BODY + 340, 1184, 'auto', 'Why this is the part worth copying',
          'An agent that silently "improves" a hand-edit destroys the reason you made it by hand. This one measured the problem, quantified the remedy, named it as the one open item, and stopped. "Say the word and it’s a one-line change."',
          K.cyan, K.surface),
], { notes: 'Frame 12:02, lower half. This is the behaviour to hold vendors to, not the canvas.' });

// ── 9 · Captions vs frames ───────────────────────────────────────────────────
addSlide([
  ...header('Method', 'Captions carried roughly a sixth of this video',
            'Why a screencast has to be read off frames, with the numbers from this run.', 9),
  ...table(48, BODY, 1184, [
    { t: 'Evidence', w: 300 },
    { t: 'What it gave', w: 560 },
    { t: 'Verdict', w: 324 },
  ], [
    ['Auto-captions', '"This right here", "you’ll see this panel" — deixis without referents', 'Weakest tier'],
    ['Default download', '640×360 only; no on-screen text is legible', 'Unusable, and silent'],
    ['1080p frames', 'File names, line counts, version ids, hex values, the debug readout', 'The actual record'],
  ], { rowH: 52, highlight: 2 }),
  ...card(48, BODY + 230, span(1, 6), 'auto', 'The flag that recovers the format ladder',
          '--extractor-args "youtube:player_client=default,mweb,web_embedded". Without it yt-dlp offers format 18 and nothing errors — you simply get an unreadable deck and no warning.',
          K.amber),
  ...card(cx(7), BODY + 230, span(7, 12), 'auto', 'The ranking that should have applied',
          'Execution, then on-screen text, then narration. The first cut of this brief used only the third, and read as thin because it was.',
          K.cyan, K.surface),
], { notes: 'This slide is the method note. Twelve frames at 1600px carried more than 212 caption segments.' });

// ── 10 · Close ───────────────────────────────────────────────────────────────
addSlide([
  rect(0, 0, 1280, 720, K.midnight),
  ...headerDark('The takeaway', 'Judge the agent, not the canvas',
                'The drawing surface is the demo. The file trail and the refusal are the product.', 10),
  roundRect(48, BODY + 30, 1184, 190, '#12243A'),
  rect(48, BODY + 30, 6, 190, K.amber),
  tx('Save before you speak — and read what it says back, because it will have reviewed you.',
     84, BODY + 76, 1110, 120, { size: T.title - 6, face: SERIF, bold: true, color: K.white }),
  ...cols(3).map((c, i) => {
    const t = [['IT WRITES FILES', 'Named .dc.html artboards you can read, diff and keep'],
               ['IT VERSIONS THEM', 'Published artifacts with ids, diffed to recover your edits'],
               ['IT DECLINES', 'Flags what your edit broke, and waits for you to say go']][i];
    return [
      rect(c.x, BODY + 268, c.w, 3, [K.cyan, K.teal, K.amber][i]),
      tx(t[0], c.x, BODY + 286, c.w, 22, { size: T.kicker, bold: true, color: [K.cyan, K.teal, K.amber][i] }),
      tx(t[1], c.x, BODY + 314, c.w, 100, { size: T.body, color: '#A9BACD' }),
    ];
  }).flat(),
], { background: K.midnight, notes: 'The habit is Save. The insight is that the agent is doing more than drawing, and the captions hide all of it.' });

const file = await PresentationFile.exportPptx(P);
await file.save(OUT);

const { writeFile, mkdir } = await import('node:fs/promises');
const DIR = `${process.env.DECK_RUN || '.'}/qa/renders`;
await mkdir(DIR, { recursive: true });
const n = P.slides.count;
for (let i = 0; i < n; i += 1) {
  const blob = await P.export({ format: 'png', slide: P.slides.getItem(i), scale: 1 });
  await writeFile(`${DIR}/slide-${String(i + 1).padStart(2, '0')}.png`, Buffer.from(await blob.arrayBuffer()));
}
console.log('saved', OUT, '·', n, 'slides ·', n, 'renders');

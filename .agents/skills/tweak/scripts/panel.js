// tweak panel: sliders for the page's design tokens, section toggles, and a Bake button that writes the
// values back into the source CSS through tweak.py. Injected by tweak.py; never ship it in a build.
// With a tweak.json (served at /__tweak/config) it shows only the curated controls, labelled, with swatch
// presets and named sections; every raw token stays reachable under "All tokens".
(async () => {
  const me = document.currentScript;
  const TOKEN = me && me.dataset.token;
  const root = document.documentElement;
  let tokens = {}, config = {};
  try {
    tokens = await (await fetch('/__tweak/tokens')).json();
    config = await (await fetch('/__tweak/config')).json();
  } catch { return; }
  const curated = Array.isArray(config.controls) && config.controls.length > 0;

  const host = document.createElement('div');
  host.id = 'tweak-panel-host';
  host.style.cssText = 'position:fixed;top:12px;right:12px;z-index:2147483647';
  const sh = host.attachShadow({ mode: 'open' });
  sh.innerHTML = `<style>
    :host{all:initial}
    .p{font:13px/1.35 system-ui,sans-serif;color:#e8e6e1;background:#16181a;border:1px solid #3a3f44;border-radius:8px;
       width:320px;max-height:calc(100vh - 24px);display:flex;flex-direction:column;box-shadow:0 8px 32px #0008}
    .h{display:flex;align-items:center;gap:8px;padding:10px 12px;border-bottom:1px solid #2c3034}
    .h b{flex:1;font-size:13px}
    .b{overflow:auto;padding:8px 12px 12px}
    .row{display:grid;grid-template-columns:1fr 92px;gap:4px 8px;align-items:center;padding:6px 0;border-bottom:1px solid #24282b}
    .row label{grid-column:1/-1;font:12px ui-monospace,monospace;color:#b9c0c6;display:flex;justify-content:space-between}
    .row.named label{font:600 12px system-ui,sans-serif;color:#e8e6e1}
    .row label i{font-style:normal;color:#e6b35a;font-family:ui-monospace,monospace;font-weight:400}
    .sw{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:6px}
    .sw button{display:flex;align-items:center;gap:6px;min-height:32px;padding:4px 10px}
    .sw button span{width:14px;height:14px;border-radius:3px;border:1px solid #fff4}
    .sw button[aria-pressed=true]{border-color:#e6b35a;background:#2c2618}
    input[type=range]{width:100%;accent-color:#e6b35a}
    input[type=text],input[type=number]{width:100%;box-sizing:border-box;background:#0f1112;color:#e8e6e1;border:1px solid #3a3f44;
       border-radius:4px;padding:4px 6px;font:12px ui-monospace,monospace}
    input[type=color]{width:100%;height:28px;border:1px solid #3a3f44;border-radius:4px;background:none;padding:0}
    button{font:600 12px system-ui;border-radius:5px;border:1px solid #3a3f44;background:#22262a;color:#e8e6e1;padding:7px 10px;cursor:pointer;min-height:32px}
    button.bake{background:#e6b35a;color:#16181a;border-color:#e6b35a}
    h4{margin:12px 0 4px;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:#8d949a}
    details summary{cursor:pointer;margin-top:12px;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:#8d949a}
    .sec{display:flex;gap:8px;align-items:center;padding:3px 0;font-size:12px}
    .out{white-space:pre-wrap;font:11px ui-monospace,monospace;color:#9fd18b;margin-top:8px}
    .min .b{display:none}
  </style>
  <div class="p"><div class="h"><b>${config.title || 'tweak'}</b><button class="reset">Reset</button><button class="bake">Bake</button>
  <button class="fold" aria-label="Collapse panel">–</button></div><div class="b"></div></div>`;
  document.body.appendChild(host);
  const body = sh.querySelector('.b');
  const changed = {};

  const HEX = /^#([0-9a-f]{3}|[0-9a-f]{6})$/i;
  const LEN = /^(-?\d*\.?\d+)(px|rem|em|%|vw|vh|ch|pt|s|ms|deg)?$/i;
  const rgbToHex = (v) => { const m = v.match(/rgba?\((\d+)[ ,]+(\d+)[ ,]+(\d+)/); return m ? '#' + m.slice(1, 4).map((x) => (+x).toString(16).padStart(2, '0')).join('') : null; };
  const toHex = (v) => HEX.test(v) ? (v.length === 4 ? '#' + [...v.slice(1)].map((x) => x + x).join('') : v) : (rgbToHex(v) || '#000000');
  const kind = (v) => (HEX.test(v) || rgbToHex(v) ? 'colour' : LEN.test(v) ? 'size' : 'other');
  const setters = {};  // token -> [fn(value)] so a curated control and its raw row stay in sync
  const set = (name, val) => { root.style.setProperty(name, val); changed[name] = val; (setters[name] || []).forEach((f) => f(val)); };

  // one row for one token; opts: {label, min, max, step, swatches}
  function row(name, opts = {}) {
    const v = tokens[name].value.trim();
    const el = document.createElement('div');
    el.className = 'row' + (opts.label ? ' named' : '');
    el.dataset.token = name;
    el.innerHTML = `<label>${opts.label || name}<i>${v}</i></label>`;
    const badge = el.querySelector('i');
    const sync = [(val) => { badge.textContent = val; }];
    const k = kind(v);
    if (opts.swatches && opts.swatches.length) {
      const wrap = document.createElement('div'); wrap.className = 'sw';
      for (const s of opts.swatches) {
        const b = document.createElement('button'); b.type = 'button'; b.dataset.value = s.value;
        b.innerHTML = `<span style="background:${s.value}"></span>${s.label}`;
        b.setAttribute('aria-pressed', String(s.value.toLowerCase() === v.toLowerCase()));
        b.onclick = () => set(name, s.value);
        wrap.append(b);
      }
      sync.push((val) => wrap.querySelectorAll('button').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.value.toLowerCase() === String(val).toLowerCase()))));
      el.append(wrap);
    } else if (k === 'colour') {
      const c = document.createElement('input'); c.type = 'color'; c.value = toHex(v);
      const t = document.createElement('input'); t.type = 'text'; t.value = v;
      c.addEventListener('input', () => set(name, c.value));
      t.addEventListener('change', () => set(name, t.value));
      sync.push((val) => { t.value = val; if (HEX.test(val)) c.value = toHex(val); });
      el.append(c, t);
    } else if (k === 'size') {
      const [, num, unit = ''] = v.match(LEN);
      const x = parseFloat(num);
      const step = opts.step ?? (unit === 'px' || unit === '%' || unit === 'ms' || unit === 'deg' ? 1 : 0.05);
      const max = opts.max ?? Math.max(Math.abs(x) * 3, unit === 'px' ? 48 : unit === 'ms' ? 1000 : 4);
      const r = document.createElement('input'); r.type = 'range'; r.min = opts.min ?? Math.min(0, x); r.max = max; r.step = step; r.value = x;
      const t = document.createElement('input'); t.type = 'number'; t.step = step; t.value = x;
      const apply = (val) => set(name, `${+(+val).toFixed(3)}${unit}`);
      r.addEventListener('input', () => apply(r.value));
      t.addEventListener('change', () => apply(t.value));
      sync.push((val) => { const n = parseFloat(val); if (!isNaN(n)) { r.value = n; t.value = n; } });
      el.append(r, t);
    } else {
      const t = document.createElement('input'); t.type = 'text'; t.value = v; t.style.gridColumn = '1/-1';
      t.addEventListener('change', () => set(name, t.value));
      sync.push((val) => { t.value = val; });
      el.append(t);
    }
    (setters[name] = setters[name] || []).push(...sync);
    return el;
  }

  function rawTokens(into) {
    const groups = { colour: [], size: [], other: [] };
    for (const n of Object.keys(tokens).sort()) groups[kind(tokens[n].value.trim())].push(n);
    for (const [title, list] of Object.entries(groups)) {
      if (!list.length) continue;
      into.insertAdjacentHTML('beforeend', `<h4>${title} (${list.length})</h4>`);
      for (const n of list) into.append(row(n));
    }
  }

  if (curated) {
    body.insertAdjacentHTML('beforeend', `<h4>${config.group || 'Feel'}</h4>`);
    for (const c of config.controls) body.append(row(c.token, c));
    const all = document.createElement('details');
    all.innerHTML = `<summary>All tokens (${Object.keys(tokens).length})</summary>`;
    rawTokens(all);
    body.append(all);
  } else {
    rawTokens(body);
  }

  // section toggles: hide in preview; Bake records them in a marked, reversible CSS block (never deletes markup)
  const hidden = new Set();
  const sections = curated && config.sections
    ? Object.entries(config.sections).map(([sel, label]) => [sel, label, document.querySelector(sel)]).filter(([, , el]) => el)
    : [...document.querySelectorAll('main section[id], body > section[id], main > [id], header[id], footer[id]')]
        .filter((el, i, a) => a.indexOf(el) === i).slice(0, 40).map((el) => [`#${CSS.escape(el.id)}`, `#${el.id}`, el]);
  if (sections.length) {
    body.insertAdjacentHTML('beforeend', `<h4>${curated && config.sections ? 'Show' : `sections (${sections.length}, only those with an id)`}</h4>`);
    for (const [sel, label, el] of sections) {
      const lab = document.createElement('label'); lab.className = 'sec';
      lab.innerHTML = `<input type="checkbox" checked> <span></span>`;
      lab.querySelector('span').textContent = label;
      lab.querySelector('input').dataset.selector = sel;
      lab.querySelector('input').addEventListener('change', (e) => {
        el.style.display = e.target.checked ? '' : 'none';
        e.target.checked ? hidden.delete(sel) : hidden.add(sel);
      });
      body.append(lab);
    }
  }
  const out = document.createElement('div'); out.className = 'out'; body.append(out);

  sh.querySelector('.fold').onclick = () => sh.querySelector('.p').classList.toggle('min');
  sh.querySelector('.reset').onclick = () => { for (const n of Object.keys(changed)) { root.style.removeProperty(n); delete changed[n]; } location.reload(); };
  sh.querySelector('.bake').onclick = async () => {
    if (!Object.keys(changed).length && !hidden.size) { out.textContent = 'Nothing to bake yet.'; return; }
    out.textContent = 'Baking…';
    const res = await fetch('/__tweak/bake', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Tweak-Token': TOKEN },
      body: JSON.stringify({ values: changed, hidden: [...hidden] }) });
    const r = await res.json();
    if (!res.ok) { out.textContent = 'Bake failed: ' + (r.error || res.status); return; }
    out.textContent = [
      ...r.changed.map((c) => `${c.name}: ${c.from} → ${c.to}`),
      ...r.skipped.map((s) => `skipped ${s.name}: ${s.reason}`),
      ...(r.hidden.length ? [`hidden: ${r.hidden.join(', ')}`] : []),
      ...r.backups.map((b) => `backup: ${b.split('/').pop()}`),
    ].join('\n') || 'No changes.';
  };
})();

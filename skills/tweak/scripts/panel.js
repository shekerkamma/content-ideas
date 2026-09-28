// tweak panel: sliders for the page's design tokens, section toggles, and a Bake button that writes the
// values back into the source CSS through tweak.py. Injected by tweak.py; never ship it in a build.
(async () => {
  const me = document.currentScript;
  const TOKEN = me && me.dataset.token;
  const root = document.documentElement;
  let tokens = {};
  try { tokens = await (await fetch('/__tweak/tokens')).json(); } catch { return; }

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
    .row label i{font-style:normal;color:#e6b35a}
    input[type=range]{width:100%;accent-color:#e6b35a}
    input[type=text],input[type=number]{width:100%;box-sizing:border-box;background:#0f1112;color:#e8e6e1;border:1px solid #3a3f44;
       border-radius:4px;padding:4px 6px;font:12px ui-monospace,monospace}
    input[type=color]{width:100%;height:28px;border:1px solid #3a3f44;border-radius:4px;background:none;padding:0}
    button{font:600 12px system-ui;border-radius:5px;border:1px solid #3a3f44;background:#22262a;color:#e8e6e1;padding:7px 10px;cursor:pointer;min-height:32px}
    button.bake{background:#e6b35a;color:#16181a;border-color:#e6b35a}
    h4{margin:12px 0 4px;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:#8d949a}
    .sec{display:flex;gap:8px;align-items:center;padding:3px 0;font-size:12px}
    .out{white-space:pre-wrap;font:11px ui-monospace,monospace;color:#9fd18b;margin-top:8px}
    .min .b{display:none}
  </style>
  <div class="p"><div class="h"><b>tweak</b><button class="reset">Reset</button><button class="bake">Bake</button>
  <button class="fold" aria-label="Collapse panel">–</button></div><div class="b"></div></div>`;
  document.body.appendChild(host);
  const body = sh.querySelector('.b');
  const changed = {};

  const HEX = /^#([0-9a-f]{3}|[0-9a-f]{6})$/i;
  const LEN = /^(-?\d*\.?\d+)(px|rem|em|%|vw|vh|ch|pt|s|ms|deg)?$/i;
  const rgbToHex = (v) => { const m = v.match(/rgba?\((\d+)[ ,]+(\d+)[ ,]+(\d+)/); return m ? '#' + m.slice(1, 4).map((x) => (+x).toString(16).padStart(2, '0')).join('') : null; };
  const set = (name, val, badge) => { root.style.setProperty(name, val); changed[name] = val; badge.textContent = val; };

  const names = Object.keys(tokens).sort();
  const groups = { colour: [], size: [], other: [] };
  for (const n of names) {
    const v = tokens[n].value.trim();
    (HEX.test(v) || rgbToHex(v) ? groups.colour : LEN.test(v) ? groups.size : groups.other).push(n);
  }
  for (const [title, list] of Object.entries(groups)) {
    if (!list.length) continue;
    body.insertAdjacentHTML('beforeend', `<h4>${title} (${list.length})</h4>`);
    for (const n of list) {
      const v = tokens[n].value.trim();
      const row = document.createElement('div');
      row.className = 'row';
      row.innerHTML = `<label>${n}<i>${v}</i></label>`;
      const badge = row.querySelector('i');
      if (title === 'colour') {
        const c = document.createElement('input'); c.type = 'color'; c.value = HEX.test(v) && v.length === 7 ? v : (rgbToHex(v) || '#000000').slice(0, 7);
        if (/^#[0-9a-f]{3}$/i.test(v)) c.value = '#' + [...v.slice(1)].map((x) => x + x).join('');
        const t = document.createElement('input'); t.type = 'text'; t.value = v;
        c.addEventListener('input', () => { t.value = c.value; set(n, c.value, badge); });
        t.addEventListener('change', () => set(n, t.value, badge));
        row.append(c, t);
      } else if (title === 'size') {
        const [, num, unit = ''] = v.match(LEN);
        const x = parseFloat(num);
        const step = unit === 'px' || unit === '%' || unit === 'ms' || unit === 'deg' ? 1 : 0.05;
        const max = Math.max(Math.abs(x) * 3, unit === 'px' ? 48 : unit === 'ms' ? 1000 : 4);
        const r = document.createElement('input'); r.type = 'range'; r.min = Math.min(0, x); r.max = max; r.step = step; r.value = x;
        const t = document.createElement('input'); t.type = 'number'; t.step = step; t.value = x;
        const apply = (val) => { r.value = val; t.value = val; set(n, `${+(+val).toFixed(3)}${unit}`, badge); };
        r.addEventListener('input', () => apply(r.value));
        t.addEventListener('change', () => apply(t.value));
        row.append(r, t);
      } else {
        const t = document.createElement('input'); t.type = 'text'; t.value = v; t.style.gridColumn = '1/-1';
        t.addEventListener('change', () => set(n, t.value, badge));
        row.append(t);
      }
      body.append(row);
    }
  }

  // section toggles: hide in preview; Bake records them in a marked, reversible CSS block (never deletes markup)
  const selectorFor = (el) => el.id ? `#${CSS.escape(el.id)}` : null;
  const sections = [...document.querySelectorAll('main section[id], body > section[id], main > [id], header[id], footer[id]')]
    .filter((el, i, a) => a.indexOf(el) === i).slice(0, 40);
  const hidden = new Set();
  if (sections.length) {
    body.insertAdjacentHTML('beforeend', `<h4>sections (${sections.length}, only those with an id)</h4>`);
    for (const el of sections) {
      const sel = selectorFor(el);
      const lab = document.createElement('label'); lab.className = 'sec';
      lab.innerHTML = `<input type="checkbox" checked> <span>${sel}</span>`;
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

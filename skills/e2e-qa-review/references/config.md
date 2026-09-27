# Config

## qa/sweep.json

```json
{
  "base": "http://127.0.0.1:8768/my-site/",
  "routes": ["", "products", "about/team", "no-such-page"],
  "widths": [[1440, 900, "desktop"], [390, 844, "phone"]],
  "out": "qa/sweep-results.json",
  "shots": "qa/shots",
  "reveal": ".section-head, .reveal",
  "axe": "node_modules/axe-core/axe.min.js",
  "webgl": true
}
```

- `routes`: every page and sub-page, relative to `base`; include one missing path to test the 404 page.
- `reveal` (optional): the selector of scroll-revealed blocks; any still under 0.99 opacity after the
  scroll-through is a finding.
- `axe` (optional): a path to `axe.min.js`; default resolves `axe-core` from the project.
- `webgl`: launch Chromium with SwiftShader so three.js / WebGL pages render headless.

## qa/nav.json

```json
{
  "base": "http://127.0.0.1:8768/my-site/",
  "start": "contact",
  "menu": "nav.mega-nav",
  "trigger": ".mega-trigger",
  "topLinks": "nav.mega-nav > a",
  "phoneOpen": "[aria-label=\"Open navigation\"]",
  "sheet": ".mobile-sheet",
  "notFound": ".nf-page",
  "typed": ["about", "about/team", "contact"],
  "extraVariants": [["use-cases", "use-cases/motors"]],
  "externalAllow": "^https://(www\\.)?youtube\\.com/@"
}
```

- `typed`: routes whose `/Title`, `/UPPER`, `/x/` and `/x.html` forms must reach the page.
- `extraVariants`: `[typed, expected]` pairs such as a bare section path.
- `externalAllow`: external menu links must match this and open in a new tab.
- `noPhoneSheet`: set `true` for a site with no phone menu sheet; the phone pass is skipped and says nothing.
- The nav gate assumes the disclosure pattern: each dropdown button carries `aria-controls` naming its
  panel's `id`, and the panel is `hidden` when closed. Zero dropdowns found is a finding, not a pass.

## qa/lanes.json

```json
{
  "src": "app",
  "dist": "dist/pages",
  "base": "http://127.0.0.1:8768/my-site/",
  "lanes": ["guidelines", "impeccable", "scrollcraft"],
  "impeccableVersion": "4.1.0",
  "impeccableTargets": ["app"],
  "skillDirs": { "scroll-craft": "/path/to/scroll-craft" },
  "scrollOut": "qa/scroll",
  "scrollChrome": "/usr/bin/google-chrome",
  "out": "qa/lanes-results.json"
}
```

- `src`: the UI source tree (the guidelines audit and, by default, the impeccable detector read it).
- `dist`: the build output; the scroll-craft lane looks here for `data-sc-act` to decide applicability.
- `impeccableTargets` (optional): override the detector's targets. Avoid `dist/`: bundles drag in vendored
  libraries (paths under `vendor/`, `node_modules/`, `downloads/` and `*.min.*` are dropped regardless).
- `scrollChrome` (optional): the browser scroll-craft uses, passed as `SCROLLCRAFT_CHROME`; it must decode h264
  (verify by playing a clip, see [lanes.md](lanes.md)).
- `skillDirs` (optional): pin a peer skill's directory; see [lanes.md](lanes.md) for the search order.

Dependencies: `playwright` and `axe-core` resolve from the site, then `$E2E_QA_NODE_MODULES` (a
`node_modules` directory), then this skill's repo. The run prints which one served.
- `allowedFonts` (sweep, optional): the families DESIGN.md declares, e.g.
  `["Inter Variable", "Newsreader Variable", "JetBrains Mono Variable"]`. Any visible text whose computed
  first family is outside the list is a finding, named by family and element class. This is the runtime
  proof for a detector's font warning: it separates a dead CSS rule from one that actually paints.

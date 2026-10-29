# Component, effect and icon sources

Where to take a proven section, effect or icon set instead of having the model draw one, and the licence
condition that comes with each. Terms were read from each source's own licence or terms page on
2026-09-28; re-check the live page before a paid or client product ships, because every one of these
changes.

Research still comes first (SKILL.md): these supply parts, not the direction. A borrowed component is
restyled to the project's tokens before it lands, never pasted with its demo colours.

## Components and effects

| Source | What it is good for | Licence and conditions | How to use it |
|---|---|---|---|
| [21st.dev](https://21st.dev) | Community React sections (Tailwind + Radix, shadcn-style): heroes, pricing, testimonials | Each component stays its **author's** property; the site code (`serafimcloud/21st`) is MIT. Terms (20 Jul 2026) forbid **scraping or automated collection** and **using its content to train models**, and require a visible link back if you republish a component elsewhere | Use the component page's own *Copy prompt* or install command. **Do not point an agent at the site to crawl it**, the "go through the gallery" pattern is prohibited here |
| [React Bits](https://reactbits.dev) | Animated text, glass cards, cursor effects, backgrounds | **MIT + Commons Clause** (`DavidHDev/react-bits`, GitHub reports it as NOASSERTION): free in any app, site or product, including commercial; you may **not sell, sublicense or redistribute the components themselves**, alone, bundled or ported | Copy the component, then restyle to tokens. Fine in a client site; not in a template or UI kit you sell |
| [Canvas UI](https://canvasui.dev) | 35 WebGL/WebGPU effects (Blaze, Liquid, Glass, Shatter, Particle Reveal, VHS), React, Solid, Preact, Vue, Svelte, vanilla TS | **MIT + Commons Clause**, same author and terms as React Bits | `npx shadcn@latest add @canvas-ui/<effect>-react` (shadcn registry; the shadcn MCP is optional) |

**Canvas UI's catch, which its marketing does not lead with:** effects that draw *live HTML on the canvas*
depend on an experimental capability that ships **only in Chrome, behind a flag**. Every other visitor sees
the content as plain HTML. The overlay effects (Blaze, Liquid, Laser, Clouds, Bubble, Droplets, Glass,
Magnify, Grid, Ripple) still run everywhere as a GPU layer; WebGPU builds need Chrome, Edge, Safari 26 or
Firefox 141. So a hero that depends on Particle Reveal is a hero most visitors never see. Decide the
effect from what degrades acceptably, and check the page in a browser without the flag.

## Icons

| Source | Licence and conditions | Notes |
|---|---|---|
| [Iconify](https://iconify.design) | Framework MIT, but **each icon set carries its own licence**. Of 238 sets (API, 2026-09-28): 108 MIT, 52 **CC-BY-4.0** (credit required, including Font Awesome 6), 31 Apache-2.0, 13 OFL-1.1, 10 CC0, 7 **CC-BY-SA-4.0** (share-alike), 3 ISC, 2 **GPL-2.0-or-later** | Read the set's licence at `api.iconify.design/collections` before choosing. Lucide (ISC), Tabler (MIT), Phosphor `ph` (MIT) and Material Symbols (Apache-2.0) need no credit line |
| [Lordicon](https://lordicon.com) | Free tier: based on **CC BY-ND 4.0**, commercial use allowed, **author credit required**, new downloads only while the account exists, Embed-HTML use capped at 1M CDN requests. PRO: no credit. Neither tier allows redistributing the icons as standalone files, using them as the core of an icon product, or putting them in HTML templates or themes without meeting the Lordicon API terms | Animated (Lottie JSON). A free icon without a visible credit line is a licence breach; `e2e-qa-review`'s sweep flags it |
| [Flaticon](https://www.flaticon.com) | Free icons need attribution; whole-pack downloads usually need Premium | Check per pack |

**Rules that follow from the table**

- **One set, one style, per product.** Mixing sets is how an interface starts to look assembled
  (see [icons.md](icons.md)).
- **Supply icons; don't let the model draw them.** Model-drawn icons are the tell; a downloaded set also
  gives the model a style reference for any icon the set lacks.
- **Icons are SVG.** A raster icon blurs at 2x and cannot be recoloured by a token. `e2e-qa-review` flags
  small raster images used as icons.
- **Credit lines are part of the build, not an afterthought.** Put the attribution in the footer or
  credits page in the same change that adds the icon.

## When a registry beats a copy-paste

Canvas UI and 21st.dev both speak the shadcn registry protocol, so an agent can install by name
(`npx shadcn@latest add ...`) instead of pasting code. That keeps provenance in the command history and
the component in the repo, where the token restyle and the licence note can follow it.

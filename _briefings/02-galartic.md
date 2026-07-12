# Briefing: !GalArtic — unified cosmic explorer

**For:** any coding agent (Claude Code subagent, Gemini in Antigravity, Cursor, fresh Claude session). Self-contained. Read top to bottom before executing.
**Target:** `C:\Users\Liezl\Documents\Github\GemGames\_builds\galartic\`
**Owner:** Liezl Coetzee · sociable.systems
**Scope:** consolidate 5–10 cosmic/space-themed interactive applets into a single browser-shipable umbrella app with a unifying exploration metaphor.

---

## 1. Concept

**!GalArtic is a single-tab cosmic observatory.** The user arrives at a persistent "sky" — a full-viewport starfield / cosmos view — and the individual applets are presented as *instruments*: telescope, synthesiser, cartographer, forge, nebula-sandbox. Each instrument is an existing applet. The shell's job is to make moving between them feel like turning the dial on a single piece of observatory equipment rather than navigating a website.

**Unifying mechanic — the Coordinate.** The shell holds one piece of shared state: a cosmic coordinate (RA, Dec, Epoch — or a simpler (x, y, z, t) tuple, agent's call). Every applet, when activated, receives the current coordinate as a URL parameter or postMessage payload on load. Applets that don't use it ignore it; applets that do, use it as a seed. This creates the illusion of a continuous cosmos the user is navigating across tools.

**Visual direction:** deep navy (`#0a1428`) base, teal-cyan accent (`#26c6da`), violet/magenta highlights (`#b388ff`), warm amber for interactive affordances (`#ff9800`). Same prism palette as the sociable.systems GrieVoice section — reuse deliberately. Typography: serif display font for poetic chrome (Cormorant Garamond or similar via Google Fonts), mono for technical readouts.

---

## 2. Source pool

Primary source (all candidates are eligible unless the agent finds them broken):

```
C:\Users\Liezl\Documents\Github\GemGames\ArtApps\!GalArtic\
  ├── cosmic-infinity-engine\
  ├── interactive-galaxy-forge\
  ├── interactive-galaxy-generator\
  ├── nebula-forge-galactic-simulator\
  └── nebula-nexus-galaxy-sandbox\
```

Secondary source (check for cosmic overflow that fits the concept; include if thematically aligned):

```
C:\Users\Liezl\Documents\Github\Playa\extracted\art-mindfulness-gumroad-bundle\visual-art\
  ├── cosmic-infinity-engine\       (likely dupe of above — deduplicate)
  ├── cosmic-renaissance-composer\
  ├── interactive-galaxy-forge\     (likely dupe)
  ├── interactive-galaxy-generator\ (likely dupe)
  ├── jwst-deep-field-explorer\
  ├── nebula-forge-galactic-simulator\ (likely dupe)
  └── nebula-nexus-galaxy-sandbox\  (likely dupe)
```

Tertiary (check for cosmic applets tagged as mindfulness but actually cosmic):

```
C:\Users\Liezl\Documents\Github\Playa\extracted\art-mindfulness-gumroad-bundle\mindfulness-sound\
  ├── astral-cavern-cosmic-mindfulness\
  ├── celestial-altar-the-ritual\
  ├── cosmic-sanctuary\
  ├── the-astral-shrine\
  ├── the-eternal-vigil-cosmic-altar\
  └── infrared-journey\
```

Agent's curation call on tertiary: include if the applet's mechanic is visual-exploration of cosmos; skip if it's primarily meditation-audio / ritual-ceremony with cosmic skin (those belong in SentAInt's contemplative layer, not here).

**Target inclusion count:** 5–10 applets in the final build. If the deduplication / curation leaves you fewer than 5, that's fine — quality over quantity.

---

## 3. Shell design

A single `index.html` at the target root. Layout:

### Persistent layer (always visible)
- **Full-viewport starfield background** — procedural, vanilla Canvas, parallax on mouse movement. Agent may use a tiny CSS-only twinkle layer if preferred, but Canvas is better. No WebGL unless necessary.
- **Coordinate readout (top-right)** — displays the current (x, y, z, t) in a decorative ornate format, e.g. "RA 12h 34m 56s · Dec +23°45′ · Epoch 2026.294". Updated when user moves.
- **Instrument rack (bottom edge)** — horizontal strip of applet tiles. Each tile shows: source image thumbnail (32–48 px), applet display name, a hover preview of the applet's inspiration image enlarged.
- **Navigation (click-drag on starfield)** — dragging pans the coordinate; pan is slow and atmospheric, not a free-camera.

### Foreground layer (on instrument activation)
- Selecting an instrument expands it to a centred modal occupying ~70% of viewport, the starfield remains dimmed in the background.
- Instrument iframe is loaded on-demand with the current coordinate passed via URL hash (`#seed=<coord>&epoch=<t>`).
- A top-right "close" control returns to the persistent view. A bottom-right "lock view" control persists the current instrument as a side-panel (so power users can run two instruments simultaneously).

### About panel
- Accessible via a small sextant-icon in the top-left. Displays:
  - The umbrella's name and concept.
  - The full AI-generation disclosure (verbatim from shared rules §1).
  - A list of included instruments with their source-image thumbnails.
  - Credit line: "Curated, consolidated, and extended by Liezl Coetzee · sociable.systems".

---

## 4. Source-image usage — specific requirements

(Binding; derived from shared rules §2.)

- **Instrument rack tiles** — each instrument tile uses its `source.jpg/png` as a circular/oval "aperture" thumbnail. Tile pulses subtly when instrument is featured.
- **Instrument activation transition** — when a user clicks an instrument tile, the source image briefly expands to fill the viewport (300–500ms ease-out) before the applet iframe loads over it. The source image becomes the "lens" the user looks through.
- **Starfield seeding** — the hex colour-histogram of each source image contributes to the starfield palette when that instrument is the most recently used. Transitions smoothly when the user switches instruments.
- **About panel gallery** — full source images displayed with captions ("Inspiration: [filename or human-readable descriptor derived from filename]"). User can click any image to jump directly into its corresponding instrument.

---

## 5. Technical requirements

(Binding; derived from shared rules §4.)

- Single `index.html` for the shell, with inlined CSS. Shell JS may be inlined or in `assets/shell.js`; agent's call.
- Each applet preserved as its own `<applet-slug>/index.html` in `applets/`, unchanged from source.
- Applets loaded in iframes. The shell passes state via URL hash, not postMessage (simpler, survives page reload).
- CDN allowed for fonts (Google Fonts) and tiny utility libs (anime.js or GSAP if animation quality demands). No p5, no three.js, no WebGL unless the shell's starfield genuinely needs it — vanilla Canvas is the target.
- Mobile: on viewports under 768px wide, collapse the persistent starfield to a static image (use a pre-rendered fallback PNG in `assets/`), and present the instrument rack as a vertical scroll list. Applet activation takes over the full viewport on mobile.

---

## 6. Metadata (every HTML file)

(Binding; derived from shared rules §3.)

In the shell's `<head>`:
```html
<title>!GalArtic — a cosmic observatory</title>
<meta name="author" content="Liezl Coetzee">
<meta name="description" content="A cosmic observatory of interactive applets. Originally generated by Google Gemini from source images; curated, consolidated, and extended by Liezl Coetzee.">
<meta name="generator" content="Gemini (original applets); human consolidation by Liezl Coetzee">
```

In each applet's `<head>` (add if missing — do not otherwise modify the applet):
```html
<meta name="author" content="Liezl Coetzee">
<meta name="description" content="[applet name] — an instrument in the !GalArtic cosmic observatory. Originally generated by Google Gemini from source images; curated, consolidated, and extended by Liezl Coetzee.">
```

---

## 7. Output structure (binding; derived from shared rules §6)

```
_builds/galartic/
├── index.html
├── README.md
├── assets/
│   ├── starfield-fallback.png   # for mobile
│   └── shell.js                 # if externalised
└── applets/
    ├── cosmic-infinity-engine/
    │   ├── index.html
    │   └── source.{jpg,png}
    ├── interactive-galaxy-forge/
    │   ├── ...
    └── ...
```

The shell's applet-discovery logic reads `applets/` — adding a new cosmic applet later is a drag-and-drop, no shell code changes.

---

## 8. Acceptance criteria (self-verify before declaring done)

- [ ] Shell `index.html` opens in Chrome/Firefox/Safari with zero console errors.
- [ ] Starfield renders and responds to mouse movement (desktop) / touch (mobile).
- [ ] Coordinate readout updates visibly when the user drags the starfield.
- [ ] Every included applet appears in the instrument rack.
- [ ] Every applet loads when its tile is activated.
- [ ] Source image appears on every tile.
- [ ] Footer disclosure is visible on the shell and on every applet's wrapper (shell overlay).
- [ ] Meta tags present on shell and every applet HTML.
- [ ] Mobile viewport (375×812) renders a usable interface — instrument rack scrolls, applets take over viewport on tap.
- [ ] No network requests to analytics or trackers (verify via devtools network tab).
- [ ] `README.md` in the build root lists included applets, skipped applets (with reason), the unifying mechanic explanation, and known issues.
- [ ] Total build folder under 50 MB (if cosmic source images push it over, flag but don't fail — cosmic images tend to be large).

---

## 9. Explicit non-goals

- No pricing page, no checkout, no "buy now" CTA in the shell. Marketing is out of scope.
- No user accounts, no saves, no server-side state. The coordinate is ephemeral.
- No rewriting of the original Gemini applet internals beyond the minimum metadata additions in section 6.
- No new cosmic applets generated from scratch — the brief is consolidation, not creation.

---

## 10. What "done" looks like from the user's perspective

Liezl opens `_builds/galartic/index.html` in a browser. She sees a drifting starfield and a rack of 5–10 instrument tiles at the bottom. She clicks one — the source image flares briefly across the screen and the instrument applet loads, running against a coordinate that visibly updates when she pans the starfield. She can close the instrument, switch to another, read the About panel, and do all of this on her phone. The footer credits the AI generation honestly and attributes the consolidation to her. It feels like one piece of software, not five. Zipping the `_builds/galartic/` folder produces a Gumroad-ready archive.

If that experience works, the build is done.

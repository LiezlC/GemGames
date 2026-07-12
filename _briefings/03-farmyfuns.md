# Briefing: FarmyFuns — a cohesive tycoon-verse of farming sims

**For:** any coding agent (Claude Code subagent, Gemini in Antigravity, Cursor, fresh Claude session). Self-contained. Read top to bottom before executing.
**Target:** `C:\Users\Liezl\Documents\Github\GemGames\_builds\farmyfuns\`
**Owner:** Liezl Coetzee · sociable.systems
**Scope:** consolidate 12 farming-sim applets into a single umbrella "FarmyFuns World" where each applet is a distinct farm/region the player can visit, tied together by a shared resource economy and a persistent overworld map.

---

## 1. Concept

**FarmyFuns is a tycoon-verse.** Twelve farms sit as pins on a stylised world map. Each farm is one of the source applets — a cyber-bloom synthesis lab, a sunset ranch, a Sunday braai simulator, a twin-peaks tycoon, an AI-influencer vibe-stack, etc. The user is the *absentee owner* of all twelve. They travel between farms via the overworld map, run the individual farm applets, and a shared "Portfolio" panel tracks simple aggregate metrics across the twelve.

**Unifying mechanics — lightweight, not a full save game:**

1. **Overworld map** — a single-image or SVG map with twelve animated pins. Hovering shows the farm's source image and tagline; clicking enters the farm.
2. **Portfolio panel** — a right-side drawer showing: total farms owned (12), current farm, a fictional "Assets Under Cultivation" number generated from the hash of the farm's name (deterministic, no state), a whimsical leaderboard that shuffles by source-image colour hue.
3. **Seasonal tint** — shell reads the user's local clock and applies a subtle seasonal overlay to the overworld (warm-amber for dusk, cool-cyan for dawn, etc). Whimsical touch, does not affect applet behaviour.
4. **Travel transitions** — moving between farms plays a brief "road movie" transition (a strip of the source images ticker-taping by, ~400ms). Sells the tycoon-verse feel.

**Explicit non-goal:** this is NOT a real save-state economy. We are not building a tycoon game from scratch. The 12 applets each already contain their own mini-game logic. FarmyFuns is a *framing shell* that makes them feel like one product — a whimsical agricultural empire — without trying to unify their internal mechanics.

**Visual direction:** warm paper base (`#f8f6f1` paper tone), rust accent (`#a84b2f`), deep ink (`#1a2f38`) for body text, brass (`#c9a961`) for ornament. Hand-drawn feel — the overworld map should look sketched, not infographic. Typography: serif display for farm names (Playfair Display or similar), sans-serif for chrome (Inter, Work Sans).

---

## 2. Source pool (all 12 are the target — curate only if broken)

```
C:\Users\Liezl\Documents\Github\Playa\extracted\art-mindfulness-gumroad-bundle\farming-sim\
  ├── bitsoil-farm-the-digital-detox\
  ├── cyber-bloom-synthesis\
  ├── cyber-pastoral-farm-interface\
  ├── dreamscape-forager\
  ├── nile-riverfront-builder\
  ├── sunday-braai-simulator\
  ├── sunset-ranch-simulator\
  ├── synth-farm-2077-agri-tech-simulator\
  ├── twin-peaks-tycoon\
  ├── valley-estate-architect\
  ├── vibesonly-tycoon-the-ai-influencer\
  └── vibestack-viral-tycoon\
```

All 12 should ship unless one is provably broken (shell fails to open it, or the HTML has a syntax error that blocks rendering). Skip + document rather than attempt to fix.

**Naming note:** each farm needs a display name in the overworld. Default to a human-readable version of the slug (`sunday-braai-simulator` → "Sunday Braai"). If a better name suggests itself from the applet's own `<title>` tag, use that. Keep names concise — 1–3 words — so the map isn't cluttered.

---

## 3. Shell design

Single `index.html` at target root. Layout:

### Overworld (default view)
- **Full-viewport map** — an illustrated world map, hand-drawn style. Agent may generate this procedurally via Canvas (abstract shapes, coastlines, mountains) OR use a freely-licensed cartographic base (e.g., a Natural Earth low-res shapefile rendered to SVG). Vanilla Canvas or SVG preferred — no external map tiles (no CORS, no analytics).
- **Twelve pins** placed across the map in thematically suggestive positions:
  - *Sunday Braai* → southern Africa
  - *Nile Riverfront Builder* → north-east Africa
  - *Synth Farm 2077* → East Asia / speculative zone
  - *Cyber-Pastoral Farm* → central Europe
  - *Twin Peaks Tycoon* → Pacific Northwest
  - *Sunset Ranch* → American Southwest
  - *Valley Estate Architect* → southern France / Tuscany
  - *Dreamscape Forager* → anywhere evocative; agent's call
  - *Bitsoil Farm (Digital Detox)* → remote island
  - *Cyber Bloom Synthesis* → futuristic coastal lab
  - *Vibesonly Tycoon (AI Influencer)* → LA/media-coast
  - *Vibestack Viral Tycoon* → adjacent to Vibesonly, signalling they're a duo
- Pin positions matter narratively but the agent has discretion to make the overall map visually balanced.
- Hovering a pin: pops a small preview card showing the farm's source image thumbnail, its display name, and a one-line whimsical tagline (e.g., "Where the bits till themselves."). Agent generates taglines from the applet's `<title>` or filename — one per farm, 5–8 words each, gently comedic.
- Clicking a pin: travel transition (400ms source-image ticker), then farm applet loads.

### Farm view (applet loaded)
- Applet iframe fills ~80% of viewport.
- Top bar shows: farm display name, a "← Back to world" button, the source image as a small "postcard" in the corner.
- Shell's Portfolio panel collapses to a thin edge-tab on the right; click expands.
- Footer visible below the applet with disclosure.

### Portfolio panel (right-side drawer, expand/collapse)
- Your Farms: 12
- Currently Visiting: [farm name]
- Assets Under Cultivation: [whimsical number, e.g., "₦ 42,069,800 vibe-bushels"]
- Today's Mood: [cycles through the 12 farms' source-image dominant colours, one per hour; display is "Sunset Ranch is 🌅 golden today"]
- About FarmyFuns: brief text block + full AI-generation disclosure.

### Seasonal overlay
- Based on `new Date()` local time, apply a CSS filter or background-gradient overlay to the overworld only: dawn (5–8am) cool-pink, day (8am–5pm) none, dusk (5–8pm) warm amber, night (8pm–5am) deep navy with star speckle. Never applies to the applet view — farms run at their own hour.

---

## 4. Source-image usage — specific requirements

(Binding; derived from shared rules §2.)

- **Pin preview card** — each pin's hover card displays its source image, ~120×90 thumbnail, with a painterly frame.
- **Travel transition** — the ticker-tape transition between overworld and farm uses the target farm's source image as the primary large frame, with the 11 other farms' source images as smaller scrolling panels behind it. 400ms ease.
- **Farm postcard** — while a farm applet is running, its source image sits in the top-right corner as a ~80×60 "postcard" — clicking it opens a modal displaying the full image with a caption "Inspiration for [Farm Name]."
- **Portfolio mood colour** — the day's "mood" reads the dominant colour from the current farm's source image and tints the Portfolio drawer's accent. Subtle — 10–15% opacity max on the accent, not a full theme swap.

---

## 5. Technical requirements

(Binding; derived from shared rules §4.)

- Single `index.html` for shell, inlined CSS, inlined or `assets/shell.js` JS.
- Each farm applet preserved as its own `applets/<slug>/index.html`, unchanged from source.
- Farms loaded in iframes. No state passed to farms — each farm is self-contained.
- Google Fonts allowed (Playfair Display, Inter). No other external deps unless justified.
- Map rendering: Canvas or SVG, procedural or from a licence-compatible base. Absolutely no tile-server calls.
- Mobile: overworld becomes a vertical list of farm cards (pins map-position preserved as an "on-planet location" caption). Applet takes full viewport on tap.

---

## 6. Metadata (every HTML file)

(Binding; derived from shared rules §3.)

Shell `<head>`:
```html
<title>FarmyFuns — a tycoon-verse of twelve peculiar farms</title>
<meta name="author" content="Liezl Coetzee">
<meta name="description" content="Twelve interactive farming simulators united in one tycoon-verse. Originally generated by Google Gemini from source images; curated, consolidated, and extended by Liezl Coetzee.">
<meta name="generator" content="Gemini (original applets); human consolidation by Liezl Coetzee">
```

Each farm applet `<head>` (add if missing):
```html
<meta name="author" content="Liezl Coetzee">
<meta name="description" content="[Farm Name] — one of the twelve farms in the FarmyFuns tycoon-verse. Originally generated by Google Gemini from source images; curated, consolidated, and extended by Liezl Coetzee.">
```

---

## 7. Output structure (binding; derived from shared rules §6)

```
_builds/farmyfuns/
├── index.html
├── README.md
├── assets/
│   ├── map-base.svg          (or canvas generator inline)
│   └── shell.js
└── applets/
    ├── bitsoil-farm-the-digital-detox/
    │   ├── index.html
    │   └── source.{jpg,png}
    ├── cyber-bloom-synthesis/
    │   ├── ...
    └── (... 10 more ...)
```

---

## 8. Acceptance criteria (self-verify before declaring done)

- [ ] Shell opens in Chrome/Firefox/Safari without console errors.
- [ ] Overworld map renders with all 12 pins visible.
- [ ] Every pin shows its hover card with source image + tagline.
- [ ] Clicking any pin runs the travel transition and loads the farm applet.
- [ ] "Back to world" returns to the overworld cleanly.
- [ ] Portfolio drawer opens/closes, renders all 12 farms listed.
- [ ] Seasonal overlay renders correctly at different test times (agent verifies by temporarily mocking `Date`).
- [ ] Source image visible as the farm's postcard while its applet is active.
- [ ] Footer disclosure visible on shell and overlay.
- [ ] Meta tags on shell and every applet HTML.
- [ ] Mobile viewport (375×812): vertical farm-card list, applet takes over viewport cleanly on tap.
- [ ] `README.md` documents: included farms with map positions, any skipped farms with reason, shell mechanic, known issues.

---

## 9. Explicit non-goals

- No real tycoon economy. The "Assets Under Cultivation" number is decorative.
- No player progression, no XP, no unlocks. It's a whimsical visit-your-empire experience, not a game.
- No cross-farm inventory, no shared resources, no synthesis across farms (each farm is a self-contained applet — preserve that).
- No newly-generated farm applets. Consolidation only.

---

## 10. What "done" looks like from the user's perspective

Liezl opens `_builds/farmyfuns/index.html`. She sees a charming hand-drawn world map with twelve pins spread across it, tinted by the time of day. Hovering a pin pops a postcard of its source image and a one-line gag. Clicking travels her in, plays a brief source-image montage, and drops her into the farm applet. She can poke around the farm, come back out, visit another. The Portfolio drawer shows her "farming empire" with whimsical made-up numbers. Everything has a warm paper-and-ink feel, and the footer credits both the AI generation and her curatorial hand. On her phone, the map becomes a scrollable list of farm cards; farms run full-screen on tap. Zipping the folder produces a Gumroad-ready bundle.

If that experience works, the build is done.

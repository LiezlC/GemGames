# Briefing: SentAInt — a contemplative gallery of AI thought-experiments

**For:** any coding agent (Claude Code subagent, Gemini in Antigravity, Cursor, fresh Claude session). Self-contained. Read top to bottom before executing.
**Target:** `C:\Users\Liezl\Documents\Github\GemGames\_builds\sentaint\`
**Owner:** Liezl Coetzee · sociable.systems
**Scope:** curate 10–15 applets from a source pool of 45 speculative-AI-futures applets and consolidate them into a contemplative "cabinet of curiosities" umbrella — each applet presented as a specimen in a philosophical gallery exploring what it would mean for AI to think, feel, remember, refuse, or cease.

---

## 1. Concept — and why it matters

**SentAInt is a gallery, not a game.** The user moves through a darkened room — a virtual cabinet — in which each specimen is an interactive thought experiment about artificial mind. Some specimens are simulations (what does a singularity event look like?). Some are interfaces (talk to a synthetic dog that "translates" its bark). Some are traps (a Turing test you cannot pass). Some are gentle (a companion protocol that asks you to sit with it).

**The point of the gallery is provenance + contemplation, not entertainment.** Each specimen has a placard: who it is (the applet's internal title), what question it asks, and a curator's note (1–3 sentences, written in an unhurried voice) situating the specimen in a broader philosophical question. The placards are the shell's creative contribution — they're what turns 12 disconnected applets into one exhibition.

**This umbrella is thematically adjacent to the Sociable Systems intellectual line-up** (The Asimov Cycle, The Clarke Constraint, The Watchdog Paradox, the Calvin Convention). Some of the source applets directly touch those concepts — `the-asimov-interface`, `strange-loops-eternal-learning-algorithm`, `project-plato-s-cave-simulation-architect`. Where overlap exists, the curator's note should gesture toward the relevant Sociable Systems concept *without* turning the gallery into a marketing page for it. Resonance, not cross-selling.

**Unifying mechanic — the Specimen Drawer.**
Each applet is a specimen in a drawer. The gallery's chrome offers:

1. A **room view** (entry) — a darkened hall with display plinths, each plinth representing one specimen. Plinths glow at different tempos; hovering reveals the specimen's name and question.
2. A **specimen view** (on click) — the applet loads inside a framed display case. Above and below the case: placard (name + question + curator's note), source image (rendered as a small "inspiration" card), and navigation to adjacent specimens.
3. A **journal panel** (right-side drawer) — the user can capture a reflection on any specimen. Reflections stay in localStorage only (no backend). The journal is purely for the user's own engagement; nothing is sent anywhere.

**Visual direction:** near-black base (`#0a0a0e`), parchment warm-white for placards (`#f5f0e8`), brass ornaments (`#c9a961`), one restrained accent colour picked per specimen from that specimen's source image (glows, frame tint). Typography: a serif with personality for placards (Cormorant Garamond, Cormorant Infant, or EB Garamond), mono for specimen metadata.

---

## 2. Source pool — 45 candidates, curate to 10–15

Full source pool:

```
C:\Users\Liezl\Documents\Github\Playa\extracted\speculative-ai-futures\
  (45 subfolders, each containing index.html + source.{jpg,png,pdf})
```

Candidate titles (the agent should verify in the folder — this is just the list as it appeared at survey):

africa-2030-the-digital-revolution-simulator · africa-s-single-digital-market-2030-simulator · agi-convergence-simulator · ai-dog-translator-decoding-the-bark · ai-dream-decoder · ai-ethics-the-dilemma-engine · ai-futures-alignment-vs-convergence · ai-office-chronicles-the-game · ai-reconstruction-protocol · authentic-human-simulator · beyond-automation-ai-lab-simulator · brain-2-0-evolution-simulator · chronos-bridge-the-great-upload · cyber-homestead-os · cyber-shepherd-os · digital-entropy-cube · digital-sentience-the-synthesizer · eagleeye-synthetic-chorus-protocol · flamingone-the-turing-test · forever-alone-companion-protocol · mobius-data-self-referential-consciousness · neural-convergence-interface · neural-perception-visualizer · neural-synthesizer-ai · project-plato-s-cave-simulation-architect · singularity-reactor-control · soulquery-the-organic-database · strange-loops-eternal-learning-algorithm · symbiosis-human-ai-resonance · synapse-the-living-book · synth-mind-neural-interface · the-ai-voice-promise-vs-peril-interactive-policy-simulator · the-algoriture-influence-simulator · the-ascension-protocol · the-asimov-interface · the-convergence-interface · the-creator-s-dilemma-artificial-beings · the-neural-cartographer-ai-memory-simulation · the-singularity-event · the-tech-panic-playbook-interactive · vibe-coding-simulator-google-ai-studio · void-drifter-event-horizon · xeno-synthesis-lab

### Curation criteria (apply in this order)

1. **Thematic coherence first.** The gallery is about *AI interiority and its philosophical ripples* — mind, memory, dream, refusal, cessation, convergence, upload, consciousness. Skip applets that are primarily about regional policy, technological hype, or workplace productivity (e.g., `africa-2030-the-digital-revolution-simulator`, `vibe-coding-simulator-google-ai-studio`, `the-tech-panic-playbook-interactive` probably don't belong — but verify by opening them).
2. **Interaction quality second.** Open each candidate. If the applet has a genuine interactive loop (not just a scrolling infographic or a single-button toy), it's stronger.
3. **Variety third.** Aim for 10–15 specimens that collectively span: one simulation, one interface/dialogue, one evolutionary/temporal piece, one epistemic puzzle, one companion/relational piece, one visualisation, one Turing-test/trap, one synthesis/lab. Diversity of mode, not redundant variations on the same theme.
4. **Sociable Systems resonance fourth.** Where an applet directly resonates with an existing canon concept, prefer it. Examples: `the-asimov-interface` (Asimov cycle), `project-plato-s-cave-simulation-architect` (epistemic opacity), `strange-loops-eternal-learning-algorithm` (consciousness loop), `ai-ethics-the-dilemma-engine` (Calvin Convention), `mobius-data-self-referential-consciousness` (Clarke constraint).

### Suggested curated set (the agent may adjust; audit before deciding)

Strong candidates, in rough suggested ordering:

- `the-asimov-interface` — speak to pre-action constraints
- `project-plato-s-cave-simulation-architect` — epistemic opacity
- `flamingone-the-turing-test` — the ur-question
- `strange-loops-eternal-learning-algorithm` — self-reference
- `mobius-data-self-referential-consciousness` — self-reference variant
- `the-neural-cartographer-ai-memory-simulation` — memory
- `ai-dream-decoder` — dream / latent space
- `forever-alone-companion-protocol` — the relational specimen
- `ai-dog-translator-decoding-the-bark` — the irreducibility specimen
- `digital-sentience-the-synthesizer` — the synthesis specimen
- `ai-ethics-the-dilemma-engine` — the moral specimen
- `the-creator-s-dilemma-artificial-beings` — the Frankenstein specimen
- `xeno-synthesis-lab` — the alien-intelligence specimen
- `void-drifter-event-horizon` — the cessation / beyond specimen

That's 14. Final count 10–15. Adjust based on what opens cleanly.

---

## 3. Curator's notes (the creative contribution)

Each included specimen gets a **curator's note** in the placard. 1–3 sentences. Unhurried, declarative, not florid. Ideally asks rather than answers.

Tone reference: *Wunderkammer* cards in a good museum. Not academic. Not whimsical. Contemplative.

The agent writes these. Guidelines:

- Start with what the specimen *is as interactive mechanism*, not what it claims to be about. ("A dial that adjusts the imagined weights of a synthetic dream until the user can no longer tell which layer is theirs.")
- End with a question, not a conclusion.
- Avoid: "this explores", "this asks us to consider", "imagine if". Instead use specific sensory or cognitive language.
- Where the specimen resonates with a Sociable Systems canon concept, name the concept once, neutrally, without selling it. (Example: "The mechanic here is a near-neighbour of the Clarke Constraint — authority through opacity.")
- Do NOT invent facts about the specimens. Base the note on what you observe in the applet.

The curator's notes are what make SentAInt a *gallery* rather than a folder. Give them care.

---

## 4. Shell design

Single `index.html` at target root.

### Room view (entry)
- Full-viewport near-black canvas. Plinths scattered across the viewport — 10–15 of them, one per specimen. Each plinth: a subtle glow (colour derived from the specimen's source image), a floating label.
- Hovering a plinth: the specimen's source image fades in as a watermark behind the plinth, and the placard excerpt (specimen name + one-line question) appears.
- Clicking a plinth: camera "walks" up to it (~600ms ease-in), then transitions into specimen view.
- Ambient audio: OPTIONAL. If included, use one low-volume tone generator (Web Audio, oscillator-based, no sample files), with a clear mute control. No audio on first load — user must opt in. Skip this feature entirely if in doubt; silence is fine.

### Specimen view
- Horizontally split: placard (left, ~30%), display case containing the applet iframe (centre, ~55%), source-image card + navigation (right, ~15%).
- Placard shows: specimen name (display title), **the question** (one line, bold, larger), curator's note (1–3 sentences), a small Sociable Systems resonance badge if applicable ("Near-neighbour: The Asimov Cycle" etc.) with a hover-tooltip but no link.
- Display case: applet iframe with a brass-frame border. The iframe is the applet's own HTML, untouched.
- Source-image card: the applet's source image, captioned "Inspiration for [specimen name]". Click expands to full screen.
- Navigation: "← previous specimen" / "next specimen →" buttons using the curated ordering, plus a "return to gallery" button.

### Journal panel (right-side drawer)
- User can type a reflection on the current specimen (textarea). Save to localStorage keyed by specimen slug.
- Prior reflections for this specimen are visible when the panel opens.
- A "view all reflections" mode shows every specimen's reflection as a contemplative log.
- "Export reflections" downloads a `.md` of all reflections. No server, no sending, no analytics.
- Full text: "Reflections are stored only in your browser's local storage. Nothing is sent anywhere."

### About panel
- Accessible from a small pillar-icon top-left. Displays:
  - SentAInt name + concept paragraph.
  - Full AI-generation disclosure.
  - A grid of every specimen's source image with curator's note excerpt.
  - Credit line.

---

## 5. Source-image usage — specific requirements

(Binding; derived from shared rules §2.)

- **Plinth glow colour** — derived from the specimen's source image's dominant non-grey colour.
- **Plinth hover watermark** — specimen's source image fades in behind the plinth (10–20% opacity).
- **Specimen-view source card** — source image shown in full, clickable to expand.
- **Specimen-view frame accent** — specimen's source image's dominant colour used as the brass-frame's secondary tint.
- **About panel gallery** — every specimen's source image visible with curator's note excerpt.

If a source is a PDF (check — `the-asimov-interface/source.pdf` was observed in survey), extract the first page as an image at build time and use that as the source image. Preserve the PDF accessible from the source-card modal.

---

## 6. Metadata (every HTML file)

(Binding; derived from shared rules §3.)

Shell `<head>`:
```html
<title>SentAInt — a gallery of interactive AI thought-experiments</title>
<meta name="author" content="Liezl Coetzee">
<meta name="description" content="A contemplative gallery of interactive applets exploring AI mind, memory, and meaning. Originally generated by Google Gemini from source images; curated, consolidated, and extended by Liezl Coetzee.">
<meta name="generator" content="Gemini (original applets); human consolidation and curatorial writing by Liezl Coetzee">
```

Each specimen's `<head>` (add if missing):
```html
<meta name="author" content="Liezl Coetzee">
<meta name="description" content="[specimen name] — a specimen in the SentAInt gallery. Originally generated by Google Gemini from source images; curated, consolidated, and extended by Liezl Coetzee.">
```

---

## 7. Output structure (binding; derived from shared rules §6)

```
_builds/sentaint/
├── index.html
├── README.md                 (documents curation choices + curator's notes as a reading piece)
├── curators-notes.md         (the notes as a standalone essay — a bonus artifact for newsletter cross-posting)
├── assets/
│   ├── fonts/                (Google Fonts self-hosted if license allows, or CDN)
│   └── shell.js
└── applets/
    ├── the-asimov-interface/
    │   ├── index.html
    │   └── source.jpg        (or source.pdf-page-1.png + original source.pdf)
    ├── flamingone-the-turing-test/
    │   ├── ...
    └── (... 8–13 more ...)
```

---

## 8. Acceptance criteria (self-verify before declaring done)

- [ ] Shell opens in Chrome/Firefox/Safari with zero console errors.
- [ ] Room view renders 10–15 plinths with distinct glow colours.
- [ ] Hovering any plinth reveals source-image watermark and placard excerpt.
- [ ] Clicking any plinth transitions to specimen view cleanly.
- [ ] Specimen view shows: name, question, curator's note, applet iframe, source image.
- [ ] Curator's notes are all written and present — no empty placeholders.
- [ ] Previous/next navigation works; wrap-around or stop-at-ends both acceptable (document choice in README).
- [ ] Journal panel saves and retrieves reflections from localStorage.
- [ ] Export reflections downloads a usable `.md` file.
- [ ] About panel displays disclosure and full specimen grid.
- [ ] Footer disclosure visible on every view.
- [ ] Meta tags on shell and every applet HTML.
- [ ] Mobile viewport (375×812): plinths become a vertical list, specimen view stacks placard → applet → source card vertically.
- [ ] If ambient audio is included: muted by default, visible mute control.
- [ ] No network requests to analytics or trackers.
- [ ] `README.md` documents curation choices (included / skipped with reason), shell mechanic, known issues.
- [ ] `curators-notes.md` collects all placard notes as a standalone reading piece.

---

## 9. Explicit non-goals

- **No new applets generated from scratch.** Curation of existing applets only.
- **No server-side anything.** Reflections are local-storage-only.
- **No analytics, no telemetry.**
- **No pricing / commerce UI.**
- **No direct cross-marketing to Sociable Systems.** Resonance badges are allowed; "buy the training" buttons are not.
- **No AI-rewriting of the applet internals.** Preserve the Gemini output.
- **Do not include applets that didn't make the curation cut.** Skipped applets are documented in the README, not shipped.

---

## 10. What "done" looks like from the user's perspective

Liezl opens `_builds/sentaint/index.html`. The room is dark. Ten to fifteen plinths glow softly at different tempos. She hovers one and the specimen's source image ghosts in behind it; a placard excerpt asks a question. She clicks — the camera moves up to the plinth, which opens into a display case. On the left, a curator's note speaks quietly about what this specimen is as a mechanism, gesturing toward but not explaining a broader question. The applet runs in a brass frame. She reads, plays, pauses, writes a reflection in the journal drawer. She moves to the next specimen. On her phone, the same experience stacks cleanly. The footer credits the AI generation and her curatorial voice honestly. The build feels like a museum you could visit in fifteen minutes and keep thinking about for a week. Zipping the folder produces a Gumroad-ready archive.

If that experience works, the build is done.

---

## 11. A note on editorial weight

Of the four umbrellas, this is the one where Liezl's voice matters most. The curator's notes are not decoration — they are 30% of the product. Write them with care. If, as the executing agent, you're not confident in any single note, leave it as `[NOTE-TODO]` with a short description of what it needs, rather than shipping something forgettable. Liezl will write that one herself. Better a visible gap than a filler line.

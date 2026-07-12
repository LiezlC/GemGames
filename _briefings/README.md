# Umbrella-app consolidation briefings

Four briefings, one per umbrella product. Each is a **self-contained prompt** you can hand cold to any coding agent (a Claude Code subagent, Gemini in Antigravity, a fresh Cursor session, etc.) to execute the consolidation work.

## The four umbrellas

| # | Umbrella | Concept | Source pool | Applet count |
|---|----------|---------|-------------|---|
| 1 | **OmniCanvas** | Multi-applet visual-art composer with layer/blend mechanics | `ArtApps/OmniCanvas/applets/` + `ArtApps/To_Omni/` + bundle `visual-art/` | ~16 candidates |
| 2 | **!GalArtic** | Unified cosmic explorer — shared sky, multiple instruments | `ArtApps/!GalArtic/` + cosmic overflow | ~5–10 candidates |
| 3 | **FarmyFuns** | Meta-farm shell binding farming-sim toys into one tycoon world | bundle `farming-sim/` | 12 candidates |
| 4 | **SentAInt** | Contemplative gallery of interactive AI-philosophy thought experiments | `speculative-ai-futures/` | 45 candidates (curate to 10–15) |

## How to use a briefing

1. Open the briefing for whichever umbrella you want built.
2. Copy the entire file contents.
3. Paste as the opening message in a fresh agent session. **Do not** pre-load the session with other context — the briefing is designed to stand alone.
4. Agent executes. Output lands at the target path specified at the bottom of each briefing.
5. You review the result. If it needs iteration, you can either reply to the same session with specific feedback, or hand the output (plus diff from your feedback) to a different agent for a second pass.

## Shared rules

**[00-shared-packaging-rules.md](00-shared-packaging-rules.md)** is referenced by all four briefings. It covers AI-generation disclosure, attribution, source-image usage rules, file-format requirements, and acceptance criteria common across umbrellas. You don't need to hand it to the agent separately — each briefing embeds the required parts inline. The file exists so you can update rules in one place if the standard shifts.

## Order of operations (recommended)

1. **!GalArtic first** — smallest scope, tightest source pool, fastest to land. Use it as the proof-of-concept. If the result is good, the other three follow the same pattern with confidence.
2. **FarmyFuns second** — medium scope, naturally cohesive (all farming), good second validation.
3. **OmniCanvas third** — already has partial build artifacts in `ArtApps/OmniCanvas/`, so the agent is extending rather than starting from scratch. Slightly more care needed to respect existing work.
4. **SentAInt last** — biggest curation burden (45 → ~12), most conceptually delicate (philosophy of AI), and the one where your own editorial voice matters most. Do this one when you can review the curation choices yourself before the agent locks them.

## Where the output goes

Each briefing specifies its own target directory under `C:\Users\Liezl\Documents\Github\GemGames\_builds\<umbrella-slug>\`. The consolidated app is delivered as:

- `index.html` — the umbrella shell (single file, self-contained)
- `applets/<applet-slug>/` — one folder per included applet, each containing the applet HTML + original source image
- `assets/` — any shared images/CSS/JS the shell needs
- `README.md` — author-facing notes: what was consolidated, what was skipped, known issues

## A note on what these briefings DON'T cover

- **Marketing copy, pricing, landing pages** — deliberately out of scope. The briefings produce working consolidated apps. Packaging decisions happen after you see the built artifacts.
- **Hosting/deployment** — briefings produce single-HTML bundles that can be opened locally, zipped for Gumroad, or embedded via iframe on sociable.systems later. No deployment pipeline assumed.
- **Testing beyond smoke-test** — briefings require the agent to open the final build in a headless browser and confirm it renders + each applet loads, but not full behavioural QA. You'll catch the rest by playing with it.

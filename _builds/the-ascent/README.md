# The Ascent — a pilgrimage in fourteen stations

A contemplative umbrella app binding fourteen interactive shrine-applets into a single climb
from dusk to dawn. Open `index.html` — you arrive at the trailhead at the **bottom** of the
page and scroll **upward**. The procedural sky (canvas: gradient palette, parallax ridges,
stars, mist, embers) shifts from ember-dusk through midnight and violet pre-dawn to summit
gold as your scroll altitude rises. Each station is an applet; entering it opens a shrine
overlay (iframe + placard + curator's note). "Light the lantern" marks it complete
(localStorage). When all fourteen lanterns are lit, the summit gate opens and the Dawn Bell
(WebAudio) can be rung.

## Consolidated stations (base → summit)

| # | Station | Source |
|---|---------|--------|
| I | Neon Rain: Zen Walk | `extracted/simulation/Neon_Rain_Zen_Walk` |
| II | Zen Veranda Architect | `extracted/simulation/Zen_Veranda_Architect` |
| III | The Sanctuary Tree | `extracted/simulation/The_Sanctuary_Tree` |
| IV | Lumi: The Serenity Bot | `extracted/simulation/Lumi_The_Serenity_Bot` |
| V | The Mystic Doorway | `extracted/simulation/The_Mystic_Doorway` |
| VI | The Shadow Oracle | `extracted/simulation/The_Shadow_Oracle` |
| VII | The Vigil: Keeper of the Flame | `extracted/puzzle/The_Vigil_Keeper_of_the_Flame` |
| VIII | Celestial Altar: The Ritual | `extracted/simulation/Celestial_Altar_The_Ritual` |
| IX | The Astral Shrine | `extracted/simulation/The_Astral_Shrine` |
| X | The Rift Walker | `extracted/simulation/The_Rift_Walker` |
| XI | Neon Ascension: The Tower Climb | `extracted/arcade/Neon_Ascension_The_Tower_Climb` |
| XII | Rise & Remix: The Ascension | `extracted/simulation/Rise_Remix_The_Ascension` |
| XIII | The Ascent to Sunspire | `extracted/simulation/The_Ascent_to_Sunspire` |
| XIV | Ascension: Step Into The Light | `extracted/simulation/Ascension_Step_Into_The_Light` |

## Skipped (with reason)

- `ASCENSION_PROTOCOL_BEYOND_UBI` — policy-dashboard piece, breaks the contemplative register.
- `Cosmic_Sanctuary`, `The_Eternal_Vigil_Cosmic_Altar` — cosmic-altar applets reserved for the !GalArtic umbrella.
- `Rift_Walker_The_Orange_Void` — variant/duplicate of The Rift Walker (one Rift crossing is enough).
- `Project_Ascension` — near-duplicate register of the Ascension Protocol family; kept the pool lean.
- `Rise_Remix_The_Ascension_2`, `_2_3` — duplicates of Rise & Remix (kept the primary).

## Packaging

- Shell + every applet carries the AI-generation disclosure meta tags (author / description / generator).
- Footer disclosure always visible on the shell; About panel (☸, top-left) shows the full
  provenance statement and a gallery of all fourteen source images.
- Applet internals untouched except the inserted `<meta>` tags. Source images normalized to
  `applets/<slug>/source.{jpg,webp}`.
- No external trackers or analytics. Pilgrimage state is localStorage only
  (`the-ascent-lanterns-v1`); "Extinguish all lanterns" in the About panel resets it.

## Known issues / notes

- Applets are Gemini-generated and vary in quality; a few may have their own console noise —
  they run sandboxed in the shrine iframe and don't affect the shell.
- Build total ≈ 8 MB (well under the 50 MB cap).

Curated, consolidated, and extended by Liezl Coetzee · sociable.systems

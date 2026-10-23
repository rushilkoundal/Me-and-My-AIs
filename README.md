# Me and My AIs

Production workspace for the animated AI parody Shorts "Me and My AIs / Inside the AI Chat".
Agents start with [AGENTS.md](AGENTS.md).

| Path | What it is |
|---|---|
| `YOUTUBE_CHANNEL_WORKING_MEMORY.md` | Standing production brief |
| `RK-FOURTH-WALL-FORMAT-RULES.txt` | Optional direct-address treatment |
| `*_RULES.md` | Older comedy-technique references (style and Grok sections superseded) |
| `.codex/skills/stable-character-animation/` | The animation skill: rules, Ember benchmark, scripts |
| `output/character-bible-2026-10-03/` | Approved cast reference and character sheets |
| `output/stable-movement-*-2026-10-23/` | Worked examples: RK/Chad walk-stop-react test, smoothed, then Ember-style effects and sound |
| `tools/sfx/kenney/` | Kenney CC0 sound packs (Impact, Interface, UI, RPG) with `LICENSES.json` |
| `episodes/` | One folder per episode; the current one is `i-just-wanted-milk-and-eggs` |

Rebuild the Ember-style example: `python3 output/stable-movement-ember-pass-2026-10-23/build_ember_pass.py`.
The two earlier examples render from their `scene.json` with
`python3 .codex/skills/stable-character-animation/scripts/render_scene.py <scene.json> --output-dir <dir>`;
their build scripts also need the original 22 October drawing sheets, which aren't in this repo.

Sound effects in `tools/sfx/kenney/` are by Kenney (www.kenney.nl), CC0.

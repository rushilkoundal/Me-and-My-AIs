# Episode brief: "I Just Wanted Milk and Eggs"

Status: approved idea, voiceover being recorded in ElevenLabs. Build with the
`stable-character-animation` skill (`.codex/skills/stable-character-animation/SKILL.md`).
Read `YOUTUBE_CHANNEL_WORKING_MEMORY.md` first. Visual, motion and sound benchmark:
Ember (see the skill's `references/benchmark-evidence.md`).

## The idea

**Real AI behaviour:** you ask ChatGPT for something tiny and get absurd overkill.
A yes/no question comes back as twelve paragraphs; a quick list becomes a whole system.
Source signal: ideas report of 21 October 2026, idea 6, reframed for casual users.

- **Emotion the viewer recognises:** "I asked for one small thing."
- **Who it gets sent to:** anyone who uses ChatGPT for everyday tasks ("this is every time I ask it anything").
- **Format:** music-and-sound physical comedy with five short captioned lines. The joke
  must read muted: a tiny request against an enormous pile of output.
- **Target length:** about 14-15 s at 24 fps, 1080x1920.

## Dialogue (ElevenLabs: RK = Andre, Chad = Miles)

Files arrive as `audio/vo/01-rk.mp3` ... `05-chad.mp3` (one line per file). Trim
silences, keep delivery brisk, never infer a speaker from anything but this table.

| # | Speaker | Line | Delivery |
|---|---|---|---|
| 1 | RK | Chad, just make me a quick to-do list. | casual, no big deal |
| 2 | Chad | Absolutely! Let's build you a complete productivity system! | bright, eager |
| 3 | Chad | Priorities, sub-priorities, color codes, weekly reviews... | fast, building momentum |
| 4 | RK | I just wanted milk and eggs. | flat, tired, buried under paper |
| 5 | Chad | I added a Gantt chart. | sincere and proud, missing the point |

Captions: short, handwritten-style, lower third, two lines max, never over faces.

## Shots (timings are starting points; retime to the recorded lines)

| Shot | Time | Framing | Action | Sound |
|---|---|---|---|---|
| S1 | 0.0-3.0 | **Wide**, characters small (RK ~18% of frame height) | Calm room. RK stands left with a tiny notepad, asks (line 1). Chad on the right, attentive. | Light room tone; a soft pencil tap as RK lifts the notepad. |
| S2 | 3.0-4.6 | **Medium** on Chad | Chad's eager anticipation: eyes light up, arms up (line 2). | Bright "confirmation" tone on the pose change. |
| S3 | 4.6-9.0 | **Wide** (same as S1) | Chad writes in a frantic cycle; one sheet becomes a scroll that unrolls across the floor and out of frame right, then papers pile up around RK in stages (line 3). | Page flips in blocks, synced to each new sheet; a paper thud per pile stage. |
| S4 | 9.0-10.6 | **Style break**: full-colour flat insert | "THE PRODUCTIVITY SYSTEM": a giant board with colour-coded tabs, charts and a glowing Gantt chart. 2 impact frames on the reveal, radial speed lines. | Short epic fanfare sting, stops dead. |
| S5 | 10.6-12.2 | **Wide** | Hard cut back: RK buried to the neck in paper. ~0.6 s silence, then he raises a tiny sticky note (line 4). | Hard silence, then a small paper rustle on the note. |
| S6 | 12.2-14.5 | **Medium** on Chad | Chad beams with pride (line 5). Hold to the end. | Cheerful "success" chime as the button, then quiet. |

Ember checks for the cut: wide shots carry the setup, one style break lands the
payoff, sound comes in blocks with a hard silence after the reveal, -14 LUFS master.
Run `scripts/measure_video.py` on the render and fix anything outside Ember's range.

## Drawings to generate (image generation)

Attach `output/character-bible-2026-10-03/approved-cast-reference.png` (plus the RK
and Chad sheets) to every character prompt. Generate one background master per shot
and separate character drawings on a flat cream background so they can be cut out.
Keep the camera, floor line and character scale fixed within a shot.

**Style block (paste into every prompt):**
```
Minimal hand-drawn 2D cartoon, 9:16 vertical. Warm cream background (#F5F2E9). Scenery is
sparse, thin, pale grey line art with lots of empty space. Characters have confident dark
outlines and flat colours; only the characters and the key prop carry colour. No
gradients, no texture, no text unless asked. Match the attached approved character
references exactly: same faces, proportions, costumes and logo placement.
```

1. **Room background master (S1, S3, S5):** "Empty living room seen straight on, wide shot.
   Faint grey outlines of a window, a small sofa and a fridge far back, a thin floor line
   at about 80% of the frame height. Lots of empty cream space in the middle. No people."
2. **RK, standing with notepad (S1):** full body, small notepad and pen, relaxed, side-3/4
   view facing right. Plus mouth variants: closed, open (A), wide (E), round (O).
3. **RK, watching worried (S3):** same scale, slight lean back, eyebrows up.
4. **Paper pile stages (S3-S5):** four drawings of a messy pile of white paper sheets and
   rolled scroll at the same scale: ankle height, knee height, chest height, neck height.
   Plain white paper with faint grey lines; nothing written.
5. **RK buried to the neck (S5):** only his head and one hand above the pile, deadpan;
   a second drawing with the hand raising a small yellow sticky note.
6. **Sticky note close-up (S5, optional insert):** a small yellow sticky note in RK's hand,
   handwritten "milk, eggs".
7. **Chad attentive (S1):** full body, facing left, friendly.
8. **Chad eager "Absolutely!" (S2, medium):** waist-up, eyes sparkling, both hands raised.
9. **Chad writing cycle (S3):** four drawings of Chad scribbling frantically on paper, same
   scale and position, for a looping 2s cycle.
10. **Scroll strip (S3):** a long horizontal strip of unrolling white paper with faint grey
    lines, transparent background, wide enough to tile across the floor.
11. **Style-break board (S4):** "Bold full-colour flat illustration, vertical: a giant
    over-the-top productivity dashboard filling the frame: colour-coded tabs, pie charts,
    sticky columns and a huge glowing Gantt chart, dramatic radial light behind it.
    Thick outlines, saturated flat colours, no readable text except the title
    'PRODUCTIVITY SYSTEM'." (Chad may appear small at the bottom, proudly presenting.)
12. **Chad proud (S6, medium):** beaming, chest out, hands on hips.

## Sound plan (sources in `tools/sfx/kenney`, all CC0)

| Moment | Sound |
|---|---|
| Notepad lift | `rpg-audio/Audio/bookPlace1.ogg` (quiet) |
| Chad's eager pose | `interface-sounds/Audio/confirmation_001.ogg` |
| Each new sheet / scroll burst | `rpg-audio/Audio/bookFlip1-3.ogg` in quick blocks |
| Each pile stage | `rpg-audio/Audio/bookPlace2-3.ogg` |
| Reveal impact | `impact-sounds/Audio/impactSoft_heavy_001.ogg` |
| Sticky note | `rpg-audio/Audio/bookFlip2.ogg` (quiet) |
| Final button | `interface-sounds/Audio/confirmation_004.ogg` |
| Epic sting (S4) | Not in the installed packs: download Kenney "Music Jingles" (CC0) into `tools/sfx/kenney/` and record it in `LICENSES.json`, or use a YouTube Audio Library cue with its credit. |

Voices duck music by about 9 dB. Hard silence of about 0.6 s at the start of S5.

## Build steps

1. Generate the drawings above; save sources and prompts in `episodes/i-just-wanted-milk-and-eggs/art/`.
2. Cut characters out (flat cream background), register each on its planted foot, one scale per shot.
3. Write one manifest per shot (see the skill's `references/manifest-format.md`): cels,
   `cycles` for Chad's writing, eased `position_keys` for the scroll travel, `effects`
   for S4 (speed lines, impact frames, flash).
4. Add RIFE in-betweens only where `scripts/inbetween_cels.py` accepts the gap; review hands.
5. Sync mouths to the ElevenLabs lines; only the speaker's mouth moves.
6. Build the sound with `scripts/mix_audio.py`, render with `scripts/render_scene.py`,
   join shots with hard cuts, add captions.
7. Run `scripts/measure_video.py`; deliver the MP4 plus editable sources. Never publish
   without the creator's explicit approval.

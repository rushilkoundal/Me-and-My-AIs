# Whole-cel manifest

Run `python3 scripts/render_scene.py manifest.json --output-dir /absolute/output`.
`--check-only` creates the frame audit, contact sheet and phone preview without MP4.
All media paths are relative to the manifest. No dependencies are downloaded.

The actual working example is `assets/scene-template.json`. It is a silent two-pose
technical example with older approved project drawings, not a style-quality benchmark.

Required root fields: `duration`, `layers`. Optional root fields: `size`(default1080x1920),
`fps`(24), `background`(cream), `safe_area`([80,180,920,1600]), `audio`(a finished mix).
Duration must equal an integer number of output frames.

Each layer has:

- Unique `id`; `z` determines back-to-front order.
- One fixed `scale`, optional `opacity`0..1, and `position`[worldX,worldY].
- Either `file` for an unchanged layer or `cels` sorted by `start` time, beginning0.
- `anchor`[nativeX,nativeY], shared or supplied by each cel. Position places this anchor
  in world space. Source cels keep their real pose compression; don't normalize each size.
- Optional `position_keys`[[seconds,x,y],…] for explicitly authored whole-layer travel.
  The helper linearly interpolates root position only; it doesn't animate body shapes.
- `subjects` map each actor/critical prop id to native bounding box[x0,y0,x1,y1].
  Cel-specific subjects replace the shared ones. Each is checked against the safe area.
- `check_alpha_bounds:true` additionally checks actual visible alpha bounds. Use this on
  actor/interaction layers, not full-bleed backgrounds. Keep background artwork separate.
- `marks` map authored contact names to native[x,y] positions. Each cel can supply its
  own marks when a drawing changes. Author actual shoe/grip/support points visually.

World transform: `worldPoint = round(position - anchor*scale) + nativePoint*scale`.
This single transform controls the entire drawing, preserving internal registration.
Per-cel scale/rotation/warp settings are rejected instead of silently ignored.

Root `contacts` records can assert a point stays on a floor or meets another layer:

```json
{
  "name": "left shoe contact",
  "layer": "rk",
  "mark": "left_sole",
  "world": [380, 1550],
  "start": 0,
  "end": 0.4,
  "tolerance": 3
}
```

For a hand gripping a separate phone, replace `world` with `other_layer:"phone"`
and `other_mark:"grip"`. Add matching marks to the two layers. Contacts only check
the declared points, not whether the drawings contain convincing fingers or support.
Set intervals to actual planted/gripped periods; a moving foot shouldn't be pinned.

Inspect the contact sheet and encoded output at phone size. Passing geometry proves
no declared out-of-bounds/contact failures, not stable facial identity or comic timing.
Existing project-specific mouth tracking and audio tools can be reused; the helper
accepts their final audio mix but doesn't transcribe, generate voice or align phonemes.

## Motion, effects and sound (Ember tools)

**Eased travel.** A position key may carry a fourth item naming the ease of the segment
that ends at it: `[1.2, 640, 1570, "out3"]`. Eases: linear, in, out, inout, in3, out3,
inout3, back (overshoot), spring (overshoot and settle), hold (jump at the key).
Use `out`/`out3` to arrive and brake, `in` to launch, `back`/`spring` for a settle.
Travel moves the whole drawing; never use it to fake a walk without foot contacts.

**Cycles.** A layer may loop drawings over a window while it travels:
`"cycles": [{"start": 0.5, "end": 2.0, "hold": 2, "frames": [{"file": "run-01.png", "anchor": [x, y]}, ...]}]`.
`hold` is the exposure (2 = on 2s). Cycles override `cels` inside their window.

**Effects** (root `effects` list, drawn after geometry checks, in order):

| type | use | main fields |
|---|---|---|
| `speed_lines` | burst or rush around a focus | `mode` radial/directional, `center`, `inner`, `count`, `angle`, `color` |
| `impact` | black/white impact frames at the hit | `hold` frames per flip, `threshold`, `invert_first` |
| `shake` | decaying hit shake (re-picked on 2s) | `amplitude` px, `decay`, `seed` |
| `flash` | full-frame flash that fades | `color`, `opacity` |
| `echo` | ghost trail for laughter/panic | `trail` frames, `strength` |

Every effect has `start`/`end` in seconds. Ember pattern: 2-4 frames of speed lines on
the anticipation, 1-2 impact frames on the hit, 4-8 frames of shake after it.

**Sound** (root `sound` block, built by `scripts/mix_audio.py` into a mastered WAV):
`cues` (effects: `file`, `frame` or `at`, `gain_db`, optional `credit`), `music`
(stings: `file`, `start`, `end`, `gain_db`, fades), `voices` (dialogue, ducks music by
`duck_db`), `silence` (hard mutes: `start`, `end`), `target_lufs` (-14), `true_peak` (-1).
Time cues by frame so each sound lands on its visible change. Set the manifest's `audio`
to the mixed file before rendering, then check the MP4 with `scripts/measure_video.py`.

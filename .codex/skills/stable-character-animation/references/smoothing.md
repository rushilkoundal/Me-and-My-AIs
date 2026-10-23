# Smoother motion without losing stability

Stability (same face, proportions, planted feet) comes from coherent source drawings.
Smoothness (smaller changes between frames) can be added afterwards. Never trade the
first for the second. Evidence: local tests on 2026-10-23 with the RK/Chad walk,
brake and reaction cels (`output/stable-movement-test*`, `output/animatediff-controlnet-test-2026-10-23`).

## Decision ladder

Work down the list; stop at the first rung that makes the motion read cleanly.

1. **Timing first.** Re-time holds and exposures (2s on fast action, longer holds on
   reactions) before adding frames. Many "stepped" complaints are uneven spacing.
2. **Author breakdown drawings** for big pose changes: walk contacts/passing positions,
   raised knees, arm swings, hand gestures that change shape. These cannot be
   interpolated (see gate below). First check unused drawings on existing approved
   sheets: rank every pair by registered silhouette change and pick the sequence with
   the smallest jumps (the 2026-10-23 smooth test found passing/knee-up breakdowns this
   way). Calibrate sheet rows drawn at different sizes once per row, and register by
   the planted shoe heel when a measured contact point disagrees with the drawing.
   Otherwise generate complete same-scale whole bodies from the approved cast,
   registered to the same sole/pelvis landmark.
3. **Selective RIFE in-betweens** for small changes only: reaction settles, breathing
   holds, brake-to-stop, head turns, slow arm drift. Use `scripts/inbetween_cels.py`.
4. **AnimateDiff + ControlNet** failed identity in testing; research only (see below).

Never run interpolation over the whole composited video: scenery lines warp and
both characters ghost. Interpolate one actor at a time on flat paper, then composite.

## Selective RIFE (`scripts/inbetween_cels.py`)

Registers two whole-body cels on one authored landmark (planted sole or pelvis),
flattens them on paper, asks RIFE for in-betweens, re-mattes them to RGBA and saves
them at native cel size with the anchor recorded. Add them to the manifest as
ordinary cels with the reported `anchor`; layer scale/position stay unchanged.

```bash
python3 scripts/inbetween_cels.py A.png B.png --mark-a 148.5,392.7 --mark-b 144.6,393.8 \
  --times 0.33,0.67 --scale 2.07 --rife /path/rife-ncnn-vulkan --model /path/rife-v4.6 \
  --out-dir /abs/out --prefix react-04-05
```

- `--scale`: use the shot's layer scale so RIFE sees lines at final thickness.
- `--times`: uneven spacing gives eases (e.g. `0.2,0.5` slows into B).
- Register on the foot that stays planted; for a walk, on the pelvis.

**Pose-gap gate.** The script measures silhouette change after registration and
refuses pairs above 0.35 (`--max-change`). Calibration on RK cels with rife-v4.6:

| Pair | Change | Result |
|---|---|---|
| react 04→05 | 0.08 | clean |
| react 05→06 | 0.29 | usable; fingers go soft — inspect hands |
| brake 04→05 | 0.31 | clean |
| walk 02→04 | 0.66 | broken shoe, missing hand |
| walk 00→01 | 0.78 | see-through leg and hand (ghosting) |

Above 0.20 the report says to check hands and shoes closely. Passing the gate is
necessary, not sufficient: on the full RK reaction, 5 of 13 gated candidates were
rejected for see-through or doubled hands, two of them at only 0.19-0.22 change.
Hands that slide across the shirt or pants ghost most; hands moving in open space
held up. Reject per frame and let the previous authored drawing hold. A rejected pair needs a
breakdown drawing between A and B; then interpolate the two smaller gaps. `--force`
exists only for demonstrating the failure. Automatic ghost metrics (ink count,
off-palette colour, crossfade similarity) were tried and could not separate clean
from ghosted frames, so every candidate needs a look at the review sheet.

Other findings: `rife-anime` ghosted more than `rife-v4.6`; temporal TTA (`-z`) is on.
The RIFE binary is the portable ncnn release (Vulkan via MoltenVK on macOS); in a
sandboxed agent it may need GPU access granted. In the channel workspace it lives at
`tools/rife/` with provenance and licence.

## AnimateDiff + ControlNet (video-to-video)

Regenerates every frame with Stable Diffusion 1.5 (DreamShaper 8), the AnimateDiff
v1-5-3 motion adapter and a Canny ControlNet built from our own frames.
Channel-workspace runtime: `tools/animatediff/` (venv, pinned weights, provenance);
test script `output/animatediff-controlnet-test-2026-10-23/animate_test.py`.

**Verdict: not for production; do not reach for it to fix smoothness.** Results:

- 4 frames, strength 0.30, 3 steps: output stayed near the source because it barely
  changed it, so it added no smoothness.
- 12 frames (walk to stop), strength 0.30, Canny scale 1.10, 8 steps: every frame
  turned into blotchy watercolour texture; RK's face blurred, Chad's face and shirt
  broke apart, outlines vanished and the mug/table dissolved. 22 minutes for 1.5 s.
  (`conservative/contact-sheet.jpg`.) Part of this may come from the memory
  workarounds below (fp16 + sliced attention on MPS); that was not isolated, but even
  a clean run regenerates every pixel, which is what endangers locked character art.
- The higher-change preset (strength 0.55) was not run: the conservative setting
  already failed identity.

Revisit only with a dedicated CUDA GPU, a model fine-tuned (LoRA) on the approved
cast, and an explicit user decision to spend that time. Then test on a 12-frame clip
first and compare against the source at phone size before any longer render.

Running it on a 24 GB Apple-silicon Mac:

- All 30 frames in one call asks MPS for a ~25 GB attention buffer and aborts.
  Use `--window 12` (overlapping windows, blended) and `--slice-attention`.
- Attention slicing ran ~140-170 s per denoising step (12 frames, 360x640) either
  way, so a full 30-frame clip takes ~85 minutes per setting.
- Allow GPU access for the run; the first download is ~4.2 GB.

---
name: stable-character-animation
description: Plan, create and review stable minimal line-art animation for the user's RK, Chad, Claude and Grok cast. Use for scene staging, whole-drawing cel animation, restrained backgrounds, grounded props, dialogue mouth timing, and making motion smoother (breakdown drawings, selective RIFE in-betweens, AnimateDiff trials), including application of the supplied Ember benchmark. Does not train a video model or publish videos.
---

# Stable Character Animation

Aim for stable, readable acting. Held poses and short purposeful actions are welcome;
continuous movement and high drawing counts are not quality requirements.

## Context and authority

- In the channel workspace, read `YOUTUBE_CHANNEL_WORKING_MEMORY.md` before production.
  Current user instructions override older Grok-only, no-voiceover and duration rules.
- Use `assets/approved-cast-reference.png` as the identity authority. Read
  [characters](references/characters.md) for facial, costume and logo invariants.
- `assets/simplified-cast-candidate.png` is a generated presentation variant. Keep it
  separate from the approved identity reference; don't silently designate it a new master.
  User approval can promote it. Existing authorization to animate the approved cast remains valid.
- `assets/scene-style-anchor.png` illustrates the requested low-contrast room and
  selective colour with RK/Chad. It is a composition candidate, not a universal scene
  template or extracted animation layer. Prompts/provenance are in `references/`.
- **Ember (instagram.com/emberer00) is the creator's benchmark for scene style, motion,
  props and sound (set 23 October 2026).** [Visual system](references/visual-system.md) and
  [motion and audio](references/motion-and-audio.md) encode it; follow them by default and
  copy Ember's approach, never its characters, artwork, music or audio.
- Read [benchmark evidence](references/benchmark-evidence.md) when justifying a benchmark
  claim. The five-reel sample has mixed coverage; covers and spot screenshots are not
  full moving-image analysis. Never invent exact fps, drawing counts or the creator's tools.
- This workflow does not retrain a model or make one still contain missing action.
  Do not promise generative-video quality from instructions alone.

## Work within the request

For a single correction, preserve useful footage/assets and change the affected element.
For new work, define the action, interaction and readable ending before generating art.
If the user requested only a script or plan, stop at that deliverable. Don't infer
permission to publish, contact a creator or purchase services.

1. Define the starting pose, motivated action, result and reaction. For channel stories,
   ground the incident in recognisable AI use. Select cast by the idea.
2. Read [visual system](references/visual-system.md) and choose one camera, floor plane,
   actor scale, prop support and colour hierarchy per shot.
3. Plan the drawings that communicate the action. Read [motion and audio](references/motion-and-audio.md)
   for contacts, exposures and speech. Use complete redrawn bodies or interacting pairs.
   Don't rotate detached raster limbs as a substitute for authored natural action.
4. Create/edit raster art with the available image-generation tool, using the approved
   cast and a clean scene anchor. Save prompts/provenance. Keep one background master
   instead of regenerating scenery with each pose. Use exact supplied logo art if an emblem drifts.
5. Assemble at fixed scale. Stable holds are welcome. Add actual breakdown drawings
   where a transition is unreadable. Don't apply crossfades, optical flow or mesh warping by default.
   When the user wants smoother motion, read [smoothing](references/smoothing.md): retime,
   then author breakdowns for large pose gaps, then add RIFE in-betweens only to small
   gaps with `scripts/inbetween_cels.py`. Never interpolate the composited video.
6. For dialogue, inspect the supplied audio; map speaker turns, word times and pauses.
   Keep brisk natural delivery. Close the speaking mouth during silence; leave the
   listener's mouth still. Label rehearsal cues provisional until recordings arrive.
   Never infer both voices from a filename.
7. Build the sound pass with `scripts/mix_audio.py`: an effect on every visible contact,
   music only as a short sting, hard silence after the main impact, -14 LUFS master.
   Mix original or appropriately licensed sounds at visible contacts. Keep music below
   speech and preserve comic silence. A requested coughing action needs a suitable cough,
   not a noise-exhale relabelled as one.
8. Run `scripts/measure_video.py` on the render and fix anything outside Ember's range.
   Review at phone size and at motion contacts. Inspect the encoded video as well as
   source frames; deliver the final file and editable source path.

## Helpers

`scripts/render_scene.py` assembles existing RGBA cels and static layers from a JSON
manifest. It does not generate missing drawings, phonemes, artwork or fluid motion.
An existing verified project renderer can also be used; don't rebuild it solely for this helper.

```bash
python3 scripts/render_scene.py assets/scene-template.json --output-dir /absolute/output/path
```

The template is a two-pose technical example using earlier project drawings, not a
demonstration of the redesigned cast or a completed episode. Read [manifest format](references/manifest-format.md)
before adapting it. Pillow and FFmpeg must exist; the helper does not install dependencies.

The manifest also supports eased travel, looping cycles and frame effects (speed lines,
impact frames, shake, flash, echo); see [manifest format](references/manifest-format.md).

`scripts/mix_audio.py` builds the soundtrack from frame-timed cues in the manifest:
effects on their frames, music stings, ducked voices, hard silences, mastered to
-14 LUFS / -1 dBTP, with `credits.txt`. Sources and licences: [sound library](references/sound-library.md).

`scripts/measure_video.py` measures a render (movement share, holds, loudness, sound
hits, sync, silence) against the Ember benchmark. Run it on every delivery.

`scripts/inbetween_cels.py` makes RIFE in-between cels for one actor between two
authored cels, registered on a planted landmark, and rejects pose gaps too large to
interpolate. Output cels drop into the manifest with their reported anchors. It needs
numpy, scipy and a local `rife-ncnn-vulkan` with a model folder; candidates still need
visual review. Details and calibration: [smoothing](references/smoothing.md).

## Delivery checks

- Both full bodies and important hand/prop contacts remain visible inside the chosen
  mobile safe area. The background fills 9:16 without black bars.
- Face construction, costume, emblem side and actor-size relationship stay coherent.
  Pose compression is allowed; unexplained scale compensation and identity changes are not.
- Planted feet attach to the floor. Resting objects touch supports. Held objects meet
  hands. Prop ownership and occlusion remain clear through a handoff.
- Background/static props do not shimmer. Moving actors do not drag the scenery.
- Pose changes convey emotion without automatic bobbing, presenter gestures or unreadable jumps.
- Speech is intact, the correct mouth moves, pauses close it, and effects don't mask words.
  Word-time estimates aren't a claim of phoneme-perfect alignment.
- Numerical checks cover only declared geometry. Review silhouette, anatomy, emotion
  and contact visually; passing metadata checks does not establish finished art.
- Never play the creator's own public YouTube videos for checks. Use local exports,
  non-playing analytics/metadata/transcripts and comments.

If a video model or external service is needed, identify the dependency instead of
implying that adding a skill creates that capability.

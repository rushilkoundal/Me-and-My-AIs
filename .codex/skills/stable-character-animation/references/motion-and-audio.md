# Stable motion and audio

## Ember motion pattern (benchmark)

Measured on 12 reels: a median 61% of frames show visible change, so Ember mostly
moves on 1s. Small simple figures travel, walk, run and repeat short actions (a hammer
swung three times) continuously; holds of 0.5 s or more take a median 22% of runtime,
used for reactions and beats. Each impact has a clear anticipation. Hard cuts switch
between the wide shot and close inserts; the payoff often breaks style (see
visual-system). Effects are drawn over the action: speed lines, smear arcs, debris,
dust, flashes, shake.

How we reach that look without 24 new drawings per second:
- Move whole characters along **eased paths** (`position_keys` with an `ease`), loop
  short **cycles** (walk, run, hammer) while they travel, and add RIFE in-betweens on
  small pose changes.
- Put the real drawings where the acting is: key poses, contacts, reactions.
- Add `effects` for impact frames, shake, flashes, speed lines and smears (see
  `manifest-format.md`).
- Check the render with `scripts/measure_video.py` against the benchmark numbers.

## Pose economy and contacts

A drawing can hold for several24fps output frames. A steady pose is welcome; an
unmotivated jump between incompatible poses is not. Choose timing from the action.

For a reach/handoff consider intent/gaze, anticipation, reach breakdown, contact/grip,
transfer, release and settle. Combine stages when clear; add a drawing at a failed
transition rather than regenerating everything. Fast impacts can use a few strong
poses, contact sound and a clear cut.

For walk -> notice -> stop -> react: establish coherent left/right contacts; keep the
planted foot in world space while weight passes it; swing the free foot in an arc.
Let gaze notice the issue, brake with a landing/weight shift, carry the torso forward
briefly and settle into the emotional pose. No compulsory bobbing during the hold.

Register complete cels to a stable shoe/sole landmark and use one scale for the shot.
Per-cel size normalization hides crouching and causes scale breathing. Compare face,
head/body ratio and costume before rendering. For complex hand/phone transfers, a
complete pair cel can preserve contact. Separate props need explicit grip points,
ownership and z-order before/at/after transfer.

## Drawings

Generate complete clean poses or separated same-scale cel sheets. Keep camera, floor,
cast authority and prop geometry constant. Inspect each drawing for drift. One image
doesn't establish unseen views or the future action. Default to stable holds and clear
next drawings. Dissolves create double limbs; unvalidated flow can melt faces/props.
Use these only for a justified inspected transition, never as an automatic smooth switch.
Respect the user's preference against hinged puppet acting.

## Speech

Inspect the entire supplied recording. One filename may contain all characters/turns.
Trim measured empty handles/needless pauses without losing consonants. Prefer modest
pitch-preserving tempo changes plus shot retiming; verify the edited wording again.

Record speaker, text, source ranges, tempo and final timing. Derive word times from
edited clips; inspect ambiguous bounds against waveform/spectrogram. Use authored
illustrated shapes such as closedMBP,A,wide,E,O,U,FV. Only the speaker's mouth changes.
Measured pauses close it; the listener stays still. Preserve stubble/nose/jaw, cheeks
and front phone occlusion. Matte only mouth ink, not a face rectangle.

Label broad word-timed shapes honestly unless a tested phonetic aligner provides
more precise evidence. Historical project fact: installed Rhubarb macOS binaries
launched but crashed on recognition and produced no usable cues. Don't repeatedly
retry them without a changed setup. Use verified word timing/audio energy or a
separately tested alternative.

## Sound

Ember pattern (measured): mastered to -14 LUFS integrated; about 2.4 sound hits per
second; strong hits land within 2 frames of a visible change. Sound comes in blocks:
a burst of synced effects, then hard silence, then the next burst. Music is rarely a
continuous bed (median about 6% of runtime); it enters as a short parody sting
(epic, game or movie style) under the escalation and stops dead. Leave about 0.5-1 s
of silence right after the main impact. Ambience beds (water, wind) can carry a
scene. Ember's sound sources are unknown; use our own or licensed sounds of the same
kind and timing.

Build the mix with `scripts/mix_audio.py` from frame-timed cues in the manifest, so
every sound sits on its visible frame. Master to -14 LUFS integrated and -1 dBTP true
peak (Ember clips above 0 dBTP; we don't). Sources and licences: see `sound-library.md`.

Use current approved voices and user takes. Don't clone voices for convenience.
Match original/licensed SFX to cough, footfall, grip, paper or phone contact. Keep
source provenance for imported sounds. Never reuse the benchmark's music or audio.

Duck music under speech with short shoulders and preserve useful comic silence.
Master: -14 LUFS integrated, -1 dBTP true peak (matches Ember); verify the encoded audio.
These are production choices, not platform requirements. Intact words, no clipping
and comfortable speech clarity matter more than one target number. Listen when
playback is available; do not claim subjective listening from ASR alone.

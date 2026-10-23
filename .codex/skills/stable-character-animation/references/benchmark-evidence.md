# Ember benchmark — measured study, 23 October 2026

Source: https://www.instagram.com/emberer00/ (33K followers, 61 posts; 12 reels are
public without login). All 12 were downloaded with the creator's approval from the
public embed for private analysis and measured with `scripts/measure_video.py`
(study folder: `output/ember-benchmark-study-2026-10-23/` in the channel workspace:
`summary.json`, per-reel timelines and shot sheets). Never reuse the reels' footage,
characters, music or audio. Copy the approach only.

## Measured numbers (12 reels: min / median / max)

| Measure | Min | Median | Max |
|---|---|---|---|
| Duration (s) | 13.0 | 17.4 | 30.7 |
| Frame rate | 24 | 24 | 24 |
| Integrated loudness (LUFS) | -14.4 | **-14.1** | -14.0 |
| True peak (dBTP) | -4.3 | -0.5 | +3.5 (they clip; we don't) |
| Loudness range (LU) | 2.4 | 8.3 | 16.9 |
| Cuts per reel | 3 | 11.5 | 25 |
| Frames with visible change (%) | 47 | **61** | 88 |
| Runtime in holds of 0.5 s or more (%) | 0 | 22 | 41 |
| Sound hits per second | 1.5 | **2.4** | 4.9 |
| Strong sound hits within 2 frames of a visible change (%) | 92 | **100** | 100 |
| Continuous music bed (% of runtime, approximate) | 0 | 6 | 19 |
| Near-silence (% of runtime) | 0 | 17.5 | 33 |

Dialogue appears in 4 of 12 reels; the rest are non-verbal (screams, laughter,
knocking, effects). Every reel is labelled "Original audio".

## What the reels do (observed in timelines and shot sheets)

**Structure.** Open on a wide, quiet establishing shot; set up the situation with
small, readable actions; escalate; land the payoff with a style break; end on a
short silence, a held reaction or one tonal sting.

**Scale.** In wide shots the characters are tiny: roughly 10-20% of frame height,
inside sparse grey line scenery (trees, skyline, fences, floor grids) on a cream
field. Characters and the key prop carry the colour. Close-ups are used sparingly
and hit hard.

**Motion.** Mostly animated on 1s: small simple figures move continuously (walks,
runs, whole-figure travel, small cycles). Holds are used for reactions and beats
(median 22% of runtime). Effects are drawn over the action: speed lines, smear arcs,
tracer lines, flying debris, dust, lightning, screen flashes, shake with ghost trails
on laughter.

**The style break (the payoff device).** The top three reels by likes (333K, 216K,
142K) all switch style at the payoff: a painted hyper-detailed close-up punch on a
dark radial background, a lightning god-mode sequence, a video-game boss title card
with black-and-white impact frames flickering every 1-2 frames. Others cut to a
3D-rendered object, a full-colour flat close-up (a fuel pump counter), or a real
photo inside a phone frame. Cut-back rhythm builds suspense: wide, insert, wide,
insert, each insert slightly further along.

**Sound.** Built in blocks: a burst of tightly synced effects, then hard digital
silence, then the next burst. Effects land on visible changes (median 100% within
2 frames). Footsteps and knocks are short clicks with fast decay. Ambience beds
(rushing water) carry some scenes. Music is rarely a continuous bed; it enters as a
**parody sting** (epic, game or movie style) under the escalation and stops dead. A
dramatic silence of about 0.5-1 s often sits right after the impact. Mastered to
-14 LUFS integrated.

**Text.** Small handwritten-style captions near the bottom; occasional top title text
for dialogue reels. Never large blocks of text.

## Limits

- Like counts are confounded by post age (the 4K-like reel was 6 days old).
- The music detector underestimates music under speech; read timelines visually.
- Sound sources (libraries, tracks) are unknown and not identified; don't guess them.
- Drawing software is unknown. The on-1s smoothness fits small, simple figures;
  copy the look with travel, cycles and in-betweens rather than 24 new full drawings
  per second (see `smoothing.md`).

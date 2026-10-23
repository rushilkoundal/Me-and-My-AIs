# Camera Flow Rules — one-take camera language in a clip-by-clip pipeline

> Technique reference: [Animated AI Parody Production Brief](YOUTUBE_CHANNEL_WORKING_MEMORY.md), locked 12 October 2026, takes precedence over older style, duration and one-clip mandates below. Preserve useful framing, contact and continuity techniques within the approved shot-anchor/Grok workflow. Extract the exact last frame for a requested continuation.

> **Update 23 October 2026:** visual styling, motion, props and sound now follow the Ember benchmark and the `stable-character-animation` skill (see YOUTUBE_CHANNEL_WORKING_MEMORY.md). Grok Imagine is no longer used, `camera-flow/` and the September episode packs/analyses this file cites were archived. Use this file only for its comedy and acting principles.

Reference: fal's **H3 Max Director** announcement (@fal, 4 Sep 2026) and the prompt
@OdinLovis published for it (3 Sep 2026). Supplement to `AI_WORKPLACE_SITCOM_RULES.md`
and `YOUTUBE_CHANNEL_WORKING_MEMORY.md`. Nothing here overrides the hook rules or the
8–12 second structure — this only changes how we get from beat to beat.

> **Read `camera-flow/single-frame-prompting.md` first.** The default is now **one
> frame, one clip, locked camera, camera move added in post.** This document covers
> what to do when the script genuinely cannot fit in one frame. Multi-clip is the
> exception, not the standard path.

## 1. What the reference actually is, and what we can take from it

fal's post is about a model that generates **one continuous video stream** — 33 seconds
in a single pass, holding context across the whole scene instead of chaining discrete
clips. That is why the camera in their video glides from space to space without ever
resetting.

We cannot reproduce that. Grok Imagine gives us short clips from still frames.

**But the model is not the interesting part. The shot grammar is.** What reads as
"one flow" is not continuous generation — it is a camera that *never resets*. Every
time our camera hard-cuts to a new angle, the viewer re-orients: where am I, who is
this, what changed. That re-orientation is a swipe risk, and per our own diagnosis the
entry/attention problem is the whole ballgame. A camera that travels instead of
cutting removes those re-orientations.

That grammar is reproducible with stitched clips. Feature films have done it for
decades without a continuous camera. We copy the grammar, not the model, and we do
not copy fal's visual styling at all.

**Correction after reading Odin's prompt.** The reference camera is not a smooth
one-take glide — the prompt explicitly asks for "hard smash cuts, bam bam bam, shot and
reverse-shot," with a restless orbit *inside* each stretch. What holds it together
across all that cutting is a hard identity lock, a standing camera doctrine, and a rule
that every stretch **lands on the same readable anchor shot**. Cutting is fine if the
anchor holds. See `camera-flow/single-frame-prompting.md`.

## 2. The one structural change

**Today:** frames are independent islands. Each is drawn separately, animated
separately, hard-cut together. Six frames = six resets.

**From now:** frames are **stations along a single camera path.** The camera leaves
station 1 already moving, and arrives at station 2 still moving. The cut lives inside
the movement, where the eye cannot find it.

Write the camera path *before* drawing any frame. One line, top of the script:

> Camera path: start close on RK's phone → pull back and track right to Chad →
> push in on Chad's face for the punchline.

If that sentence cannot be written, the beats are not spatially connected and the
video is still six islands.

## 3. What the sticker style already gives us

Our style is **die-cut sticker collage**: characters and props cut out with a white
border and a soft drop shadow, laid over a warm textured colour field with paper grain,
plus torn-paper collage cards floating behind them.

This matters for camera work in three ways, and all three are in our favour:

1. **Depth already exists.** The drop shadows separate every element from the
   background. We do not need to draw floor lines, wall corners or room perspective to
   make a move read — and we should not, because architectural lines fight the collage
   look. The layering is the depth.
2. **The torn-paper cards are the best wipe objects we have.** A card sliding across the
   lens is native to the style and hides a cut completely. See §5, T2.
3. **A flat colour field survives a 2D move cleanly.** Push, pull, pan and tilt read
   perfectly on graphic art without parallax, which is why those four moves belong in
   post (§4).

The only thing to protect is the treatment itself: **white cut-out borders, drop
shadows, the textured field, and the palette must not drift.** That is what the lock
block in every prompt is for, and it is the thing Grok abandons first.

## 3b. Which camera moves come from where — the deciding rule

> **If the move only needs pixels already in the frame, post does it.
> If it needs pixels that do not exist yet, only Grok can do it.**

That is the whole division, and it is about what is physically possible rather than a
judgement call per shot.

| Move | Needs | Source |
|---|---|---|
| Push in / pull back | pixels already in frame | **post** — exact, free, re-timeable |
| Pan / tilt | pixels already in frame | **post** |
| Shot-size change (wide → close-up) | pixels already in frame | **post** — `punchline-cut.sh` |
| Head / body turn, small | modest new angle on a character | Grok, reliably |
| Camera orbit around the scene | new angles that do not exist | **not available in our style** |

**The sticker style cannot orbit.** Flat die-cut cut-outs have no other side and there is
no room to travel through. This was tested twice (see `dimensional-style-test/`) and the
only way to unlock it is a full dimensional restyle, which was tried and declined.

**The workaround, and it is the better option anyway:** a profile-to-front reveal is done
as a **cut between two frames**, not a camera move. That is standard 2D animation grammar,
and for comedy a hard cut onto a face lands harder than a slow arc toward it.

### Shot/reverse-shot from one clip — the default edit

**Rule: both speaking characters are always staged in one frame.** One generation, one
locked camera, both faces present. The speaker is then isolated by cutting to a close-up
in post:

```bash
./camera-flow/speaker-cut.sh clip.mp4 out.mp4 shots.txt
```

`shots.txt` is one line per shot — `start cx cy w push` — and each shot runs until the
next one starts. See `chatgpt-zero-sympathy-frames/shots.txt` for a worked example.

Why this and not a frame per character:

- Vertical wants **faces centred and large**; a two-shot held for ten seconds leaves each
  face at about a tenth of the frame height, which is the format's main failure mode.
- Roughly **85% watch on mute**, so expression has to carry the story.
- Comedy rewards **fast cutting on setup and punchline**, with reactions isolated.
- Separate frames per character cost extra generations, seams, and character drift
  between them — for a result the crop gives you free, with zero drift because it is
  literally the same pixels.

**Never ask Grok to move the camera to the speaker.** Its camera cannot be aimed or
retimed, and it drifted off-subject in testing. Lock it and cut in post.

### Pace: cut the dead air, and keep the END of a reaction

Grok leaves long gaps between lines — typically 3-5 seconds of silence in a 10-second
clip. Shorts audiences do not wait. Every clip goes through:

```bash
./camera-flow/tighten.sh clip.mp4 tight.mp4 0.20 0.9 end
```

Two rules learned the hard way:

1. **Cap gaps between lines at ~0.20s.** Anything longer reads as the video buffering.
2. **For the final reaction, keep the END of the hold, not the start** (`tail_mode=end`).
   A character's expression *evolves* across a take — the smile drops, the eyes fall, the
   shoulders go. Keeping the first 1.5 seconds gives you the moment **before** the
   reaction happens, which is the opposite of what the joke needs. In the layoff video
   the punchline landed at 7.8s but RK's face did not turn until 9.7s.

`tail_mode=end` creates a jump in time at the final line. **Put a shot change there in
`shots.txt`** — cutting from the speaker's close-up to the reaction close-up at that
exact moment makes it invisible. Without a shot change it reads as a jump cut.

### The punchline cut — the standard finish

One Grok clip becomes a two-shot edit. The setup plays wide with a gentle push; the
instant the punchline lands, cut to a static close-up and hold it to the end.

```bash
./camera-flow/punchline-cut.sh clip.mp4 out.mp4 <cut_time> 0.12 0.45 <cx> <cy>
```

Three rules:

1. **Cut on the beat after the punchline line ends**, not on it. The line plays wide; the
   reaction plays close.
2. **Motion stops at the cut.** The wide drifts, the close-up is dead still. Movement
   ending exactly as the joke lands is what gives the reaction weight — and it is the one
   speed change the video is allowed. Keep the wide push at 12%, not more; the cut does
   the work of reaching the face.
3. **Do not crop tighter than ~0.45** of frame width. Keep the story object in shot — the
   letter, the phone, whatever the joke is about. A face alone loses the reason for the
   face. It is also what makes the loop back to frame 0 read.

Verified on sticker art: linework, white cut-out borders and paper grain all survive the
upscale at 0.45, and even at 0.35. Flat high-contrast art upscales far better than
photographic detail. Audio passes through untouched, so the cut never disturbs Grok's
dialogue timing.

**Check the crop centre before running it.** `cx,cy` are the fractions of frame width and
height at the centre of the subject's head, and Grok's framing may drift from the seed
frame. Pull one frame and look first:

```bash
ffmpeg -i clip.mp4 -ss <cut_time> -frames:v 1 check.png
```

## 4. Camera vocabulary — six moves, each with a fixed meaning

Do not invent moves per video. Reuse these so the language becomes ours and the
phrasing stays consistent. **Moves 1, 2, 3 and 5 are produced in post with
`camera-flow/post-camera.sh`, not by Grok.** Only the arc (6) and any real parallax
must come from Grok; the whip (4) is made at the seam by `whip-join.sh`. **The arc is
high-risk on flat sticker cut-outs — see the warning in §7 before using it.**

| # | Move | Means | Use at |
|---|---|---|---|
| 1 | **Push in** (dolly in, slow) | this is dawning on them | realization, the beat before a punchline |
| 2 | **Pull back** (dolly out) | the situation is worse than you thought | consequence reveal, showing what was off-frame |
| 3 | **Lateral track** (dolly left/right) | moving from one party to the other | handing the scene between characters |
| 4 | **Whip pan** | something just happened over there | reaction to an interruption, hiding a cut |
| 5 | **Tilt down / up** | status change | down = demotion, exposure, defeat; up = escalation, authority arriving |
| 6 | **Slow arc** (orbit ~20°) | the reversal has landed | punchline / final reaction |

Speed rule: **one speed change per video, maximum.** Slow drift throughout, one fast
move at the reversal. Constantly-moving camera is nausea, not style.

## 5. The four transitions that hide a cut

This is the actual technique. Each one needs a matched **out-frame** (end of clip N)
and **in-frame** (start of clip N+1).

### T1 — Whip handoff
The camera whips in one direction; everything streaks; the new space is already there
when it settles.
- **Out-frame:** camera must already be accelerating in the whip direction at the end.
- **In-frame:** camera must still be decelerating in the *same* direction at the start.
- **Direction must match.** A left whip into a right whip is just a cut with blur on it.
- Best for: a character reacting to something off-frame, another agent arriving, an interruption.
- Post: `camera-flow/whip-join.sh`.

### T2 — Object wipe
A foreground element crosses the lens and fills frame; the next space is behind it.
- **Best option: a torn-paper collage card sliding across the lens.** It is already part
  of the style, it fills frame cleanly, and it needs no perspective to work.
- Also available: a closing laptop lid, a character's body passing camera, a phone
  raised into the lens, a hand.
- **Out-frame:** object entering frame edge, camera drifting toward it.
- **In-frame:** the same object clearing the opposite frame edge, camera still drifting.
- Best for: changing the scene — a different background colour field, a different set
  of collage cards, a different grouping of characters.
- This is the most reliable of the four, because a full-frame object hides everything.

### T3 — Push-through
Camera pushes into a screen/surface and emerges in the space beyond it.
- Push into: a laptop screen, a phone, a chat window, a torn-paper collage card.
- **Out-frame:** the surface centred and growing, camera pushing.
- **In-frame:** starts wide *inside* the new space, camera still pushing, then settles.
- Best for: our exact premise — going from RK's side of the frame into the AI's world,
  or into a chat. Most native to this channel; use it more than the others.

### T4 — Match-scale
Two frames share a shape at the same size and screen position; cut on the shape.
- Round blank head → round phone camera lens. Laptop rectangle → torn-paper collage
  card. Phone screen → laptop screen. Cursor → eye.
- **Out-frame and in-frame:** the shared shape at identical position and scale, and the
  camera moving the same direction across the cut.
- Best for: a joke that rhymes two ideas. Cheapest of the four — no motion blur needed.

## 6. Frame design changes: draw pairs, not singles

For every seam, the two adjacent frames are now **designed together**, and must share:

1. **Camera height.** Eye-level to eye-level. A jump in height destroys the flow.
2. **Direction of travel.** Both frames moving the same way through the seam.
3. **One carry-over element** visible in both — the same torn-paper card, the same desk
   edge, the same prop. This is the viewer's proof it is one scene.
4. **Same sticker treatment and palette.** White border thickness, drop-shadow direction
   and softness, background colour and grain. A shadow that flips direction across the
   seam reads as a cut even when the geometry matches.
5. **Screen-direction consistency.** If Chad is camera-right of RK, he stays
   camera-right for the whole video. Crossing the line is an instant reset.

Practically: name frames as pairs so this is visible in the folder —
`beat-02-out-whip-left.png` / `beat-03-in-whip-left.png`.

## 7. Grok Imagine prompt template — multi-clip case

For the single-clip case use the six-block template in
`camera-flow/single-frame-prompting.md`, which is the one to reach for by default.
Use the template below only when a clip genuinely has to hand off to another clip.

Structure every animation prompt in this order. The camera clause goes **second** —
after the continuity statement, before the acting — because it is the thing Grok most
often drops.

```
[1 CONTINUES]  The shot is already moving: <direction, speed> as the clip opens.
[2 CAMERA]     <move> at <slow/steady/fast>, <how far>, ending <framing>.
[3 ACTING]     <character> <expression + one physical action>. Dialogue: "<line>"
[4 END STATE]  The clip ends with the camera still <moving direction>, framing on <X>.
[5 HOLD]       Keep the exact art style of the input image: die-cut sticker cut-outs
               with white borders and soft drop shadows, over a warm textured colour
               background with paper grain. Do not flatten the background to white.
               Do not remove the sticker borders or drop shadows. Character design
               and colours unchanged, no new props, no text.
```

Move phrasing that Grok responds to (keep to these exact words):

- Push in — `slow dolly in, camera moves closer, framing tightens on the face`
- Pull back — `slow dolly out, camera retreats, more of the scene enters frame`
- Lateral track — `camera tracks steadily to the right, the foreground cut-outs slide past faster than the collage cards behind them`
- Whip pan — `fast whip pan to the left, heavy horizontal motion blur, the frame streaks`
- Tilt — `camera tilts down, the background field slides upward in frame`
- Arc — `camera arcs slowly around the subject` — **see the warning below**

> **The arc is the one move to avoid.** Our characters are flat die-cut stickers; they
> have no other side. Asking Grok to orbit one forces it to invent angles that do not
> exist, and it will pay for that by flattening the sticker treatment or redesigning the
> character outright. If you want weight on the punchline, use a post push-in instead.
> Reserve the arc for a case where nothing else will do, and expect to re-roll.

Always include `[5 HOLD]`. Camera prompts are the most common trigger for Grok
redesigning a character mid-clip.

**Expect to fight for the ending.** Grok honours the start of a clip far more reliably
than the end. If clip N does not end with motion, do not re-roll forever — re-roll two
or three times, then take the best one and lean on `whip-join.sh` in blur mode, which
fabricates the streak in post.

## 8. The handoff loop — the reliability trick

The single biggest change to the workflow. **Stop drawing frame N+1 from scratch.**

Current: draw all frames → animate each independently → stitch. Every clip starts from
a freshly drawn image, so every seam is a fresh chance for the model to have drifted.

New, for any pair joined by a camera move:

1. Animate clip N in Grok.
2. `./camera-flow/handoff-frame.sh clip-N.mp4 beat-N+1-in.png`
   Pulls the frame **3 frames before the end** — the true last frame is usually the
   most degraded, and stepping back costs nothing.
3. Open that PNG. Repair the cut-out edge, the white border and the drop shadow, fix any
   drift in the face, palette or background grain, and add whatever the next beat needs.
4. Feed *that* image to Grok as clip N+1's input.

Clip N+1 now starts from exactly where clip N ended — not from an approximation of it.
The seam becomes almost free.

Costs one repair pass per seam. Worth it. If your Grok build has an extend/continue
button, use that instead — same idea, less work.

## 9. Stitching

```bash
./camera-flow/whip-join.sh clip-01.mp4 clip-02.mp4 joined.mp4 left 0.12 blur
```

- Arg 4 — direction the **camera** travels: `left|right|up|down`. Must match the motion
  already in both clips.
- Arg 5 — seam length. **0.10–0.16s.** Longer reads as a dissolve, not a whip.
- Arg 6 — mode:
  - `blur` (default) — dissolves between two horizontally streaked frames. No hard
    edge, forgiving when Grok's motion is imperfect. **Start here.**
  - `slide` — stronger whip, but shows a travelling edge unless both clips genuinely
    move. Only use when the motion actually matched.

Chain more than two clips by running it repeatedly on the output. Both scripts were
run against real project frames; the blur seam produces a clean full-frame streak with
no visible edge.

T2/T3/T4 do **not** use this script — they need a hard cut on the matched frame. For
those, plain concat:

```bash
ffmpeg -y -i clip-01.mp4 -i clip-02.mp4 -filter_complex "[0:v][1:v]concat=n=2:v=1[v]" -map "[v]" -c:v libx264 -crf 18 -pix_fmt yuv420p joined.mp4
```

## 10. Budget: aim for zero seams, accept one

An 8–12 second Short that passes the six conditions in
`camera-flow/single-frame-prompting.md` needs **no seams at all** — one frame, one clip.
That is the target. When it genuinely cannot, the budget is **one seam.** Do not try to
make a 10-second video that flows through five scenes; it will look frantic, and each
seam is another failure point.

Recommended first target: **one hidden transition per video**, placed at the strongest
beat — the escalation-to-punchline hinge. Everything else stays as it is today. Add a
second seam only once the first one is landing invisibly.

## 11. Interaction with the hook rules — read this

Our rule is that seconds 0.0–0.7 show the crisis. A moving camera at frame 0 is fine,
**but never use the opening move to travel toward the crisis.** The crisis is in frame
at frame 0; the camera is already pushing in on it, or pulling back to widen it. A
camera that pans across empty background to *find* the problem is exactly the "character
walking into frame before anything happens" opening we banned.

Safe openings: **push in** on a crisis already framed, or **pull back** from a detail to
reveal the crisis is worse. Both add motion without delaying the information.

## 12. QC checklist before export

- [ ] The camera path fits in one sentence.
- [ ] Each seam pair shares camera height, travel direction, and one carry-over element.
- [ ] Screen direction is consistent — nobody swapped sides.
- [ ] Seam duration is 0.10–0.16s.
- [ ] Sticker treatment is identical across the seam: white border thickness, drop-shadow
      direction, background colour and grain, character design and palette.
- [ ] Exactly one speed change in the whole video.
- [ ] The crisis is visible at frame 0; the camera is not travelling toward it.
- [ ] Watched at 0.25× speed: the cut is not findable.
- [ ] Watched with sound off: the story still reads.

## 13. What we are not taking from the reference

- Their visual style, palette, staging, or subject matter. Ours stays die-cut sticker
  collage: white-bordered cut-outs with drop shadows over a warm textured colour field,
  torn-paper cards, our own palette.
- Continuous long takes. Our format is 8–12 seconds; a 33-second unbroken shot is the
  opposite of our retention structure.
- Camera movement as spectacle. Every move on this channel carries a meaning from the
  table in §4. If a move does not mean anything, cut it.

# The cartoon system — 20 Sep 2026

> Current direction, 12 October 2026: follow [Animated AI Parody Production Brief](YOUTUBE_CHANNEL_WORKING_MEMORY.md) for purpose, the two formats, sharing priority, cast/style, acting, duration and production. This document is a historical mechanics toolkit. Its dialogue-only-for-setup, every-line-removable, whole-body-only, unchanging-AI-face, flat-colour and single-frame-pair mandates are superseded. Retain useful visual readability and timing techniques without excluding captioned dialogue.

> **Update 23 October 2026:** visual styling, motion, props and sound now follow the Ember benchmark and the `stable-character-animation` skill (see YOUTUBE_CHANNEL_WORKING_MEMORY.md). Grok Imagine is no longer used, `camera-flow/` and the September episode packs/analyses this file cites were archived. Use this file only for its comedy and acting principles.

Companion to `PHYSICAL_COMEDY_RULES.md`, `CAMERA_FLOW_RULES.md` and
`FLAT_STYLE_AND_FRAME_PAIRS.md`. Episode pack: `VISUAL_EPISODE_PACK.md`.

This document covers **what kind of cartoon to make**, not what to make it about.
Premise selection is `RETENTION_RESEARCH.md` §6 and `COMPETITOR_TEARDOWN_AHHGPT.md` §D.

---

## 1. The principle

**We have been making an animated sitcom. We need to make a cartoon.**

Locked camera, two characters standing, real-world physics, the joke delivered in a
spoken line. That is a sitcom that happens to be drawn — and a camera does it for free.
Every episode that obeys real-world physics spends animation money and buys nothing.

People who stop for cartoons stop for *cartoon*: elastic physics, exaggerated bodies,
sharp timing, consequences that could not happen. "Cartoon" is not a look. It is a set
of comedy mechanics, and the look follows from them.

---

## 2. The gate: the mute test

> **Mute the video. If you cannot tell where the laugh is, it is not finished.**

Over 60% of mobile viewers watch with no sound (`RETENTION_RESEARCH.md` §4). Every
punchline we have shipped is a spoken line, which means the funniest moment of the video
does not exist for most of the people watching it. Subtitles do not fix this — reading a
line is not the same as getting a joke.

**The inversion that follows:**

| | Old | New |
|---|---|---|
| Punchline | dialogue | **animation** |
| Dialogue | punchline | **setup only** |

If the episode still works with every line removed, it is an animated joke. If it
collapses, it is a podcast with pictures.

---

## 3. The gag vocabulary

Six kinds of joke. Each one is a single **state change — A becomes B** — which is exactly
what frame-pair interpolation is good at. Pick one per episode. Never two.

| # | Vocabulary | The mechanic | Example | Build |
|---|---|---|---|---|
| 1 | **Volume / scale** | the response is physically enormous | a yes/no question; the answer buries the room | 1 clip |
| 2 | **Multiplication** | one becomes hundreds | "a few small changes" — four hundred of them | 1 clip |
| 3 | **Literal metaphor** | the idiom happens for real | "let me take a look at that" — he takes it and leaves | 1 clip |
| 4 | **Inside the machine** | cutaway to what is actually in there | one exhausted intern; forty Chads voting | 2 clips |
| 5 | **Deformation** | the body reacts, not the face | Chad inflates with pride; RK deflates like a punctured balloon | 1 clip |
| 6 | **Wrong-scale intrusion** | correct behaviour, catastrophic size | Chad forty feet tall, cheerfully helpful, at a funeral | 1 clip |

**How each becomes a frame pair.** Seed frame is the ordinary world with the situation
established. End frame is the same composition with the one thing changed — bigger,
multiplied, transformed, deformed. Nothing else in the frame moves. The comedy is the
delta, and a locked composition is what makes the delta readable.

---

## 4. The cast

**Decision, 20 Sep 2026: the cast is permanent, the setting is free.**

RK, Chad and Claude are fixed — same designs, same voices, same comic engines, every
episode. Recognition is the only thing on this channel that compounds: a hit with
recurring characters converts into an audience, a hit with strangers in it is a lottery
ticket. This supersedes nothing about the designs; it makes them load-bearing.

**The AI-workplace setting is retired.** Chad staying Chad does not require an office.
Chad at a funeral, in a car, at a wedding, in a hospital waiting room — same character,
different world. The characters are the asset; the office never was.

### 4.1 The engine is the asymmetry

RK has a full expressive face. Chad has dot eyes and a mouth line. That is not a
limitation, it is the oldest cartoon pairing there is — the volatile one and the
immovable one — and it should be designed for on purpose:

- **RK carries every emotional read.** His face is large in frame and exaggerated hard.
  Whole-body takes, not facial subtlety. Subtlety dies at phone size.
- **Chad's body does what his face cannot.** An unchanging smile on a body doing
  something insane is a gag. An unchanging smile on a body standing still is nothing.
- **Chad never changes, and that is the joke.** Everything around him escalates; he does
  not notice. The hit is never the punchline (`PHYSICAL_COMEDY_RULES.md` §2.1) — Chad's
  obliviousness is.

---

## 4.2 Continuous transform vs substitution — what Grok is actually asked for

This decides whether an episode is one clip or two, and getting it wrong is the main way
a visual gag dies.

**Continuous transform — Grok animates the change. One clip, one frame pair.**
The thing grows, multiplies, floods, piles up, inflates, deflates, melts. That is motion,
Grok is good at motion, and the morph *is* the gag. Vocabularies 1, 2, 3, 5, 6.

**Substitution — Grok never animates the change. Two clips, hard cut in post.**
A is replaced by B: the road becomes water, the handwritten card becomes a corporate
document, the room becomes a different room. Interpolating a substitution produces a
**dissolve**, which is the exact opposite of funny. The cut is the snap. Vocabulary 4,
and any gag where the end state is not a grown or deformed version of the start state.

This is the same constraint `FLAT_STYLE_AND_FRAME_PAIRS.md` §4 already states — *"the two
frames must be a plausible interpolation of each other"* — applied to gags. A substitution
violates it by design, so it is not a frame pair at all. It is two seeds and a cut.

For a two-clip build: clip A is the ordinary world with the setup performance, clip B
opens on the changed world with the reaction performance. Same camera, same colour field,
same character positions. Grok acts in both; the transformation happens in the join.

---

## 5. Timing — the part that fights the tool

**Cartoon timing is snap–hold–snap. Interpolation produces smooth drift.**

Grok gives a gentle continuous morph between the two frames. Comic timing is the
opposite: nothing, nothing, *BANG*. Interpolation smears the bang across two seconds and
kills it. **This is not fixable in the prompt.** It is fixed in post, and post is
therefore where the comedy actually gets made — not a finishing step.

The recipe, on top of `camera-flow/punchline-cut.sh`:

1. **Hold before the change.** Freeze the setup a beat longer than feels right. The hold
   is what makes the change land.
2. **Cut into the reaction.** Hard cut to the changed frame. Never let Grok ease into it.
3. **Speed-ramp the clip.** Slow through setup, snap through the transition, freeze on
   the result.
4. **SFX on the cut**, not on the drift. See §6.
5. **Hold the final image** for the loop. See §7.

One 10s Grok clip plus a held and ramped ending lands in the 11–14s target band.

---

## 6. Sound

In cartoons, SFX is not decoration — it is **timing made audible**. It tells the viewer
where the joke is. The boing, the thud, the rising whistle, the record scratch.

- One signature hit per episode, landing exactly on the cut.
- Music under, never over. It is a bed, not an event.
- Grok generates no music and no SFX; everything is added in Remotion, as now.

---

## 7. Loop

The last frame should make the first frame funnier. A visual gag loops literally and
cheaply: end on the changed image, cut back to the ordinary world, and the replay reads
as the same disaster starting again. Replays cost nothing and are counted.

End **exactly** on the payoff. Do not linger, and do not hold silence — silence signals
exits (`RETENTION_RESEARCH.md` §5).

---

## 8. Style

The 19 Sep flat-colour switch holds and supports all of the above. Bold flat shapes
survive phone size and the mute test; glossy pseudo-3D reads as generated.

- **Silhouette test.** Fill the frame with black. The gag should still read.
- High contrast, saturated single-colour field, no muddy midtones.
- Exaggerated proportions and exaggerated reactions.
- Consistent character designs, every episode, without drift.
- Emotion effects — anger marks, sweat, wide eyes, radial glow — carry more weight now
  that there is no collage. Use them.

---

## 9. Rules this changes

**Props.** `YOUTUBE_CHANNEL_WORKING_MEMORY.md` said *"props: at most one, and only if the
joke cannot exist without it. Default to none."* That rule fights visual comedy directly.
Replaced with:

> **No decorative props. Unlimited budget for the object the joke is about.**

When the prop *is* the punchline — the wall of text, the four hundred tabs, the toilet —
it is not clutter, it is the joke.

**Length.** Default moves from 8–12s to **11–14s**. Measured across all 37 uploads, the
10–14s band has both the best median views and the best stay rate; 6–9s is the worst
performing band on the channel. See §10 of this doc's companion analysis in
`DURATION_ANALYSIS.md`.

**Setting.** Free, per §4.

---

## 10. Pre-production checklist

Before a frame is generated:

- [ ] One gag vocabulary from §3, and only one.
- [ ] The punchline is a picture, not a line.
- [ ] Passes the mute test.
- [ ] Passes the eligibility test — funny to someone who has used ChatGPT twice and never
      heard of Claude (`RETENTION_RESEARCH.md` §6).
- [ ] Setting is an ordinary real-world place, not an AI office.
- [ ] Something is physically moving inside the first second.
- [ ] 3–6 words of hook text baked on frame 0.
- [ ] RK's reaction is a whole-body take.
- [ ] Chad does not change.
- [ ] The last frame makes the first frame funnier.
- [ ] 11–14 seconds.

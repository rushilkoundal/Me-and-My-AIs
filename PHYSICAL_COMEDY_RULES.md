# Physical comedy — the action system

> Technique reference: follow [Animated AI Parody Production Brief](YOUTUBE_CHANNEL_WORKING_MEMORY.md), locked 12 October 2026, for current purpose, formats, sharing priority, cast/style, acting, duration and shot-anchor workflow. Use these older action techniques only when they serve the incident. Spoken aftermath, violence, paper physics, constant motion and an unchanging AI expression are not requirements.

> **Update 23 October 2026:** visual styling, motion, props and sound now follow the Ember benchmark and the `stable-character-animation` skill (see YOUTUBE_CHANNEL_WORKING_MEMORY.md). Grok Imagine is no longer used, `camera-flow/` and the September episode packs/analyses this file cites were archived. Use this file only for its comedy and acting principles.

Companion to `CAMERA_FLOW_RULES.md` and `camera-flow/single-frame-prompting.md`.
Rewritten 19 Sep 2026.

**Premise: Grok Imagine animates full action in one clip** — entrances, contact,
grabbing, shaking, hitting, chasing, falling, two-character fights. So we design for
that and stop engineering around limits that aren't there. Earlier versions of this
document routed around contact by cutting the impact. That is withdrawn.

What follows is therefore **not** about what the tool can do. It is about what makes an
action beat render cleanly and land as comedy.

---

## 1. The problem we are fixing

Every recent episode is the same body language: two characters planted on the field,
facing each other, mouths moving, nothing else happening.
`AI_WORKPLACE_SITCOM_RULES.md` already forbids it — *"Avoid two characters merely
standing on a blank background and trading lines"* — and we do it anyway.

`ALGORITHM_DIAGNOSIS.md` says the best launch in weeks was the only video that **did
not** open on a static two-shot: the three agents popped in one after another across the
first two seconds. Motion in second one is the thing that worked.

`single-frame-prompting.md` conditions 2 and 5 ("Nobody enters", "Nothing new appears")
are what pushed us into the stage play. **Both are hereby narrowed** to: *nothing enters
that was not designed in the seed frame or produced by someone in it.* Characters
entering, moving, and making contact are all in scope.

---

## 2. The comedy rules — these are the real constraints

Capability was never the limit. These are.

### 2.1 The hit is never the punchline

> **The hit is the escalation. The punchline is what the AI says while being hit,
> or immediately after.**

Ending on the punch is just violence. Ending on Chad's obliviousness is the show.

### 2.2 RK's violence must accomplish nothing

This is the engine of the whole format. Chad is grabbed, shaken, thrown, flattened —
and he is **unharmed, unbothered, and still trying to help.** RK's rage is impotent.

That is not just funnier than winning, it's the truest thing about being angry at a
chatbot: you cannot make it feel your frustration. Keep that and the violence stays
comic rather than mean.

### 2.3 The AI never breaks character mid-assault

Chad keeps the bright helpful voice **while** being shaken. Claude stays measured and
smug **while** being dragged. The tonal mismatch between what's happening to the body
and what's coming out of the mouth is the joke. If the AI yelps, screams or gets angry,
the gag dies.

### 2.4 RK is provoked, never a bully

He swings because the AI has ruined something of his and is proud of it. He never starts
it. Keep it bloodless, cartoon-register, no injuries — Looney Tunes, not a beating.

### 2.5 Vary the action

`AI_WORKPLACE_SITCOM_RULES.md` warns against "mass-produced episodes with the same
staging." Never run the same physical gag two episodes in a row.

---

## 3. Writing an action beat so it renders well

Grok can do the action. It renders it *well* when the beat is written with geometry.
Six things to include:

1. **Name the contact point.** Not "RK grabs Chad" — *"RK grabs Chad by both shoulders."*
   Where the hands are is the single biggest factor in whether the limbs read correctly.
2. **Give a direction.** *"shakes him back and forth"*, *"throws him to the LEFT"*,
   *"drags him toward the desk."*
3. **Give a count.** *"shakes him twice"*, *"three quick shakes."* Countable constraints
   work for action the same way they work for dialogue lines.
4. **Say where the body ends up.** *"Chad ends flat on his back on the ground, still
   smiling."* Grok drops endings more often than beginnings — state the final pose.
5. **Specify the face separately from the body.** *"Chad's bright smile never changes
   for the entire clip."* Otherwise the expression follows the physics and you lose the
   joke.
6. **One action per beat window, but beats can be short.** A 10s clip can hold three or
   four distinct 2-second actions. What fails is two simultaneous actions inside one
   beat.

---

## 4. The time budget

Dialogue runs ~2.5–3 words/second. **Action needs room, so action episodes carry fewer
words than talking episodes.**

| Clip | Talking episode | Action episode |
|---|---|---|
| 6s | 12–14 words | 8–10 words + 1 action |
| 10s | 20–24 words | **14–18 words + 3 actions** |
| 15s | 30–35 words | 22–26 words + 4–5 actions |

**Default action episode: 10 seconds, ~16 words, three actions.** Anything wordier and
the action gets compressed into unreadable mush.

---

## 5. The action vocabulary

### Entrances — A

- **A1 Burst.** RK slams into frame already furious, evidence in hand. Lands frame-0
  crisis + emotion + object simultaneously. **The default opener for action episodes.**
- **A2 Pop-In.** Paper-sticker bounce into place. *(proven — `intro-agent-frames`)*
- **A3 Slide-In.** Character eases in behind an oblivious character. Dread, not shock.
- **A4 Chase-In.** Both characters enter already running.

### Escalation — B

- **B1 Vibrate.** RK shakes in place, fists clenched, anger marks.
- **B2 Grab.** Both hands on Chad's shoulders or collar.
- **B3 Shake.** The grab, plus back-and-forth. Chad keeps talking through it.
- **B4 Chase.** Around the desk, Chad still cheerfully explaining while running.
- **B5 Muffle.** RK's hand over Chad's mouth. Chad keeps talking through it.
- **B6 Tug.** Both pulling the same laptop/object in opposite directions.

### Impacts — C

- **C1 Punch.** Straight swing, Chad's head snaps, smile intact.
- **C2 Throw.** RK hurls Chad out of frame.
- **C3 Tackle.** RK launches, both go down.
- **C4 Headlock.** Chad continues generating a bulleted list from inside it.
- **C5 Flick.** RK flicks Chad and Chad tips over rigidly like a paper standee.
- **C6 Object strike.** RK swings the laptop / the evidence.

### Aftermaths — D

- **D1 Still Talking.** Chad on the floor, wrecked, delivering the punchline completely
  unbothered. **This is the channel's best gag and should be the default.**
- **D2 Instant Return.** Chad pops back into his original pose, undamaged, smiling.
  Perfect loop point.
- **D3 Reversal.** Chad is fine; RK is the one destroyed.
- **D4 Third Party.** Claude walks in, surveys the wreckage, says one smug line.

---

## 6. Paper physics — the house flavour

Optional, but it is what makes our violence *ours*. The characters are die-cut stickers,
so where a gag allows it, let them behave like paper rather than flesh: tipping over like
a knocked standee, fluttering down like a dropped sheet, crumpling into a ball with the
face still smiling, flattening into a pancake, peeling off the background by the white
border, coming back taped together.

Three reasons to reach for it: it's native to the locked style, it removes any question
about the violence register, and a crumpled Chad still chirping is funnier than a bruised
one. Mix it with straight cartoon action — don't make every episode a paper gag.

---

## 7. Camera and post

Unchanged from `CAMERA_FLOW_RULES.md` §3b: **Grok gets a locked camera, post does the
move.** Action does not change that, with one addition:

- **Put a shake on the impact frame in post.** 2–4 frames of 6–10px displacement on the
  contact makes a generated hit land twice as hard, costs nothing, and is retimeable.
- `punchline-cut.sh` still applies — cut to a close-up on the final line.
- `tighten.sh` matters more here, not less. Grok leaves dead air around action too.

---

## 8. Prompt blocks

The seven-block template from `single-frame-prompting.md` is unchanged. Blocks 1, 3, 6
stay as they are. Two amendments:

**Block 4 — write beats with the §3 geometry.** Example:

```
0–1.5s: RK BURSTS into frame from the LEFT, already furious, holding the <evidence>
        high in his right hand. Eyebrows down, mouth open.
        RK shouts, angry: "<line>"
        Chad is silent, mouth closed, smiling.

1.5–3.5s: Chad tilts his head and smiles brightly, proud of himself, completely
        unaware anything is wrong.
        Chad says, cheerful and helpful: "<line>"
        RK is silent, mouth closed.

3.5–6s: RK drops the <evidence>, grabs Chad by BOTH SHOULDERS with both hands and
        shakes him hard, back and forth, three times. Chad's body wobbles loosely.
        Chad's bright smile never changes.
        Nobody speaks.

6–8s:   RK throws Chad down to the RIGHT. Chad lands flat on his back on the ground,
        arms out, still smiling up at the ceiling.
        Chad says, cheerful, from the ground: "<punchline>"
        RK is silent.

8–10s:  RK's face goes completely blank, shoulders dropping, staring down at Chad.
        Nobody speaks.
```

**Block 7 — replace the no-contact clause with an identity clause:**

```
No style change. No character redesign. Do not flatten the background to white.
Do not remove the sticker borders or the drop shadows. Characters keep their exact
faces and clothing through all movement — no melting, no stretching, no extra or
duplicated arms, hands or legs. No camera move. No on-screen text.
```

The duplicated-limb warning replaces the old no-contact rule. That is the failure mode
to watch in action clips, and naming it explicitly is the defence.

---

## 9. Episode structure

The structure in `AI_WORKPLACE_SITCOM_RULES.md` is unchanged. Action maps onto it:

| Time | Beat | Action layer |
|---|---|---|
| 0.0–1.5s | Visible crisis | **A1 Burst** — RK already furious, evidence in hand |
| 1.5–3.5s | Which AI is in trouble | Chad's proud, oblivious explanation |
| 3.5–6s | Escalation | **B-beat** — grab, shake, chase, muffle |
| 6–8s | Reversal / punchline | **C-beat** into **D1** — the line from the floor |
| 8–10s | Strongest reaction | RK blank. Cut on it. Loop. |

Ready-to-shoot scripts: `ACTION_EPISODE_PACK.md`.

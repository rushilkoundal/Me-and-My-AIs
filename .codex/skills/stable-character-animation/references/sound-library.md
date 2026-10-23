# Sound sources and licences

Researched 23 October 2026 from official licence pages where they loaded; items
marked [unverified] need a check before relying on them. Videos are monetised on
YouTube and posted to Instagram, so only commercial-safe sources qualify. Keep each
downloaded sound's source URL and licence; `mix_audio.py` writes `credits.txt` from
the `credit` field of any cue or music entry.

## Sound effects (in order of preference)

1. **Kenney audio packs, CC0** (https://kenney.nl/assets/category:Audio): Impact
   Sounds (CC0 confirmed, 130 files), Interface Sounds, UI Audio, RPG Audio
   (footsteps, cloth). No attribution. Small, clean: pops, clicks, impacts.
   Check each pack's own page for its licence.
2. **Freesound, filtered to CC0 and CC BY** (https://freesound.org): the best
   source of cartoon boings, slide whistles, whooshes and squeaks. Licences vary per
   sound: avoid CC BY-NC and Sampling+. CC BY needs a credit line.
3. **Sonniss GameAudioGDC bundles** (https://sonniss.com/gameaudiogdc): royalty-free,
   no attribution, monetised YouTube allowed per its FAQ; no reselling and no AI/ML
   training. Huge (9-48 GB per year) and realistic: mine it for cloth, paper, phone,
   footsteps and whooshes.
4. Mixkit (free, attribution optional [partly verified]) and Pixabay sound effects
   (free, no attribution; download by hand, its terms ban scraping).

## Music (stings and short cues)

Ember uses music as short parody stings, rarely as a bed. Use short excerpts.

1. **YouTube Audio Library** (https://support.google.com/youtube/answer/3376882): usable
   in monetised YouTube videos and not claimed by Content ID; some tracks need a credit
   line. It doesn't cover Instagram, so check each track before cross-posting.
2. **Pixabay Music** (https://pixabay.com/service/license-summary/): free, no
   attribution, all platforms. Skip tracks marked with the Content ID shield and keep
   the licence certificate.
3. **Incompetech / Kevin MacLeod, CC BY 4.0**
   (https://incompetech.com/music/royalty-free/licenses/): many comedic and epic cues;
   requires the generated credit line.

For an "epic/game parody" sting, pick an original royalty-free cue in that style.
Never use the actual game, film or Ember soundtrack.

## Avoid

- BBC Sound Effects (RemArc licence: non-commercial only).
- Any CC BY-NC or Sampling+ material; Free Music Archive tracks unless the track page
  says CC BY or CC BY-SA.
- "No copyright music" uploads and compilations (frequent Content ID claims).
- Assuming free means no credit: Zapsplat free tier, Freesound CC BY, Incompetech and
  some Audio Library tracks all need one.

## Installed locally (channel workspace)

`tools/sfx/kenney/` (downloaded 23 October 2026, CC0, details in `LICENSES.json`):
Impact Sounds (130: footsteps on 5 surfaces, punches, soft/wood/metal/glass impacts),
Interface Sounds (100: clicks, ticks, questions, errors, confirmations, glitches),
UI Audio (52: clicks, switches, rollovers), RPG Audio (52: cloth, creaks, doors, coins,
books, chops). No whooshes or music in these packs: Kenney's Music Jingles (CC0) or
Freesound CC0 whooshes would fill that gap. Useful picks so far: `footstep_concrete_*`
(indoor steps), `impactPunch_heavy_000` (hit), `cloth1` (fast arm swish),
`question_001` (notice), `error_006` (deadpan button), `tick_00*` (small eye moves).

## Local library layout (channel workspace)

`tools/sfx/<source>/<files>` with a `LICENSES.json` per source folder that records
URL, licence and credit text. Name files by what they are (`impact-heavy-01.wav`,
`whoosh-short-02.wav`, `step-sneaker-03.wav`) so cues stay readable in manifests.

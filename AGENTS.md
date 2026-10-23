# Me and My AIs — agent instructions

Animated AI parody Shorts for YouTube and Instagram (@itsworld_of_ai). RK is the human
protagonist; Chad (ChatGPT), Claude and Grok are the AI characters.

## Read first, in this order

1. `YOUTUBE_CHANNEL_WORKING_MEMORY.md`: the standing production brief (purpose, formats,
   audience, Ember benchmark, workflow, voices, publishing rules). It overrides older docs.
2. The skill `.codex/skills/stable-character-animation/SKILL.md`: how every video is made.
   Use it for scene staging, drawings, assembly, smoothing, effects, sound and checks.
3. The current episode brief: `episodes/i-just-wanted-milk-and-eggs/BRIEF.md`.

Character identity authority: `output/character-bible-2026-10-03/approved-cast-reference.png`
(per-character sheets beside it). Attach these to every image-generation prompt.

## Working rules

- Generate artwork with the image-generation tool; assemble, smooth, mix and measure with the
  skill's scripts (`render_scene.py`, `inbetween_cels.py`, `mix_audio.py`, `measure_video.py`).
- Voices are ElevenLabs recordings supplied by the creator (RK = Andre, Chad = Miles). Never
  generate or clone voices. Claude and Grok voices are not chosen yet.
- Sounds: `tools/sfx/` only from commercial-safe sources; record each source in that folder's
  `LICENSES.json`. See the skill's `references/sound-library.md`.
- Ember (instagram.com/emberer00) is the benchmark for style, motion and sound. Copy the
  approach only: never use Ember's characters, artwork, music or audio, and never add its
  reels to this repo.
- Keep each episode's work in `episodes/<slug>/` (art, cels, manifests, audio, renders).
- Run `measure_video.py` on every render and report anything outside Ember's range.
- Never publish, post or upload anything without the creator's explicit approval.
- The repo is public: no credentials, personal data or unreleased third-party material.

## Prevent AI checks from generating video views

The creator requires that AI checks never play the channel's public YouTube videos.

- Use analytics, metadata, transcripts and comments retrieved without a video player, and
  local files for inspection.
- Do not open public watch pages, Shorts players, embedded players or channel trailers
  unless playback is reliably blocked before loading. Muting, pausing or a background tab
  doesn't count.
- If a tool can't guarantee that, use a non-playing source and report the limitation.

## Local tools not in the repo

- RIFE frame interpolation: portable `rife-ncnn-vulkan` release 20221029 from
  https://github.com/nihui/rife-ncnn-vulkan/releases (model `rife-v4.6`), placed in `tools/rife/`.
- FFmpeg (with ffprobe) on the PATH. Python 3 with Pillow, numpy and scipy.

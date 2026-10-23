RK AND CHAD — EMBER-STYLE PASS (effects + real sound)

Final: rk-chad-ember-pass.mp4 (3.75 s, 1080x1920, 24 fps). Art and timing are the
smoother test (../stable-movement-smooth-2026-10-23), unchanged.

Effects on RK's recoil (frame 47): radial speed lines on the anticipation (44-47),
two black/white impact frames (47-48), a decaying shake after (49-55).

Sound, built by the skill's mix_audio.py from frame-timed cues in scene.json:
Kenney CC0 effects (tools/sfx/kenney, see LICENSES.json there): concrete footsteps on
the walk contacts and brake, a rising "question" tone when RK notices the mug, a cloth
swish as his arms fly up, a heavy punch on the recoil, soft ticks on Chad's eye moves,
an interface error tone as the button on RK's final pose. A hard 0.5 s silence follows
the hit. A light room tone (synthesized locally, no licence needed) sits underneath.
Mastered to -14.0 LUFS, -1.3 dBTP. Credits (optional for CC0) are in audio/credits.txt.

Benchmark check (measure/): loudness, sync (100% of strong hits on a visible change)
and silence are inside Ember's range. Still below: share of frames with movement (40%
vs 47-88%) because the art is unchanged, and sound density (1.3 vs 1.5+ hits/s).
Rebuild: python3 build_ember_pass.py

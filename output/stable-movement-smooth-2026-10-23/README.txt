RK AND CHAD — SMOOTHER MOVEMENT TEST

Final: rk-chad-smooth-movement-test.mp4 (3.75 s, 1080 x 1920, 24 fps, same foley)
Compare: before-vs-smoother.mp4 (left: stable-movement-test-2026-10-23, right: this)

WALK — breakdown drawings
Re-sequenced with two unused approved drawings from the 22 October walk sheet:
00 contact -> 09 passing (new) -> 01 lift -> 02 lift -> 10 knee-up (new) -> 03 contact.
This replaces drawing 04, after which RK's torso jumped backwards. Sequence chosen by
the smallest registered pose changes across all 12 sheet drawings. Rows 2 and 3 of
that sheet are drawn 1.6% and 3.3% smaller and are calibrated once per row. Drawing
00 is registered by its shoe heel; the planted heel now holds within 6 px (was 20 px).
No RIFE on the walk: every remaining gap (0.4-0.6) exceeds the skill's 0.35 gate.
A truly fluid walk needs newly generated in-between drawings (no image generator here).

REACTION — RIFE in-betweens
13 RIFE candidates made with stable-character-animation/scripts/inbetween_cels.py;
8 kept after visual review, 5 rejected for see-through or doubled hands (pairs
01-02, 02-03, 07-08 and the middle of 05-06). Rejected frames hold the authored drawing.
Review sheets: assets/inbetweens/*-review.jpg. Decisions: smoothing-report.json.

Brake, Chad, stage, mug, foley and timing beyond the walk are unchanged.
Rebuild: python3 build_smooth.py, then
python3 ~/.claude/skills/stable-character-animation/scripts/render_scene.py scene.json --output-dir render
All 90 frames pass declared framing and planted-foot checks (render/geometry-audit.json).

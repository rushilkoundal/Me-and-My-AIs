RK AND CHAD — STABLE MOVEMENT TEST

Final: rk-chad-stable-movement-test.mp4
3.75 seconds; 1080 x 1920; 24 fps; 90 frames.

Action: RK walks in, notices the prop, brakes, recoils, and settles.
Both full bodies remain visible. The red mug rests on the visible table.
The camera, room, table, mug and actor scales are fixed.
Quiet original contact foley is included; there is no dialogue.

Editable sources:
- build_test.py prepares the stage, cleans/extracts the existing complete-body cels, and authors exposure timings.
- scene.json controls layer order, exposure timings, registration, floor contacts and framing.
- assets/cels/ contains the reusable RGBA whole-body drawings.
- assets/stage.png contains the fixed backdrop, support and mug.
- audio/original-foley.wav is the original sound stem.

Render with the installed stable-character-animation/scripts/render_scene.py helper.
The source drawings come from movement-test-2026-10-22, the earlier test preferred by the creator.
No detached-limb rotation, optical flow or crossfade interpolation was applied.

Review: all 90 frames passed declared framing and contact checks. Encoded contact sheet and reaction still were visually inspected. Geometry checks validate authored coordinates, not anatomical perfection.

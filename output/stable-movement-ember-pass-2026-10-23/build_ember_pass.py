"""Ember-style pass on the smooth RK walk-stop-react test: effects plus a frame-timed sound mix.

Reuses ../stable-movement-smooth-2026-10-23 art and timing unchanged. Adds impact
frames, shake and speed lines on RK's recoil, and a sound pass built by the skill's
mix_audio.py from Kenney CC0 packs in tools/sfx/kenney (see LICENSES.json there).
"""
from pathlib import Path
import json, os, subprocess, sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent/'stable-movement-smooth-2026-10-23'
SKILL = ROOT.parent.parent/'.codex/skills/stable-character-animation/scripts'
KENNEY = ROOT.parent.parent/'tools/sfx/kenney'
FPS = 24
CREDIT = 'Kenney (www.kenney.nl), CC0'
k = lambda pack, name: os.path.relpath(KENNEY/pack/'Audio'/name, ROOT)

# Faint room tone, synthesized here (no licence needed): soft brown noise with a slow drift.
import numpy as np, wave
(ROOT/'audio').mkdir(exist_ok=True)
n = int(3.75*48000); x = np.cumsum(np.random.default_rng(11).normal(0, 1, n)); x -= np.convolve(x, np.ones(4801)/4801, 'same')
x = x/np.abs(x).max()*.9
with wave.open(str(ROOT/'audio/room-tone.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000); w.writeframes((x*32767).astype('<i2').tobytes())

scene = json.loads((SRC/'scene.json').read_text())
rel = lambda p: str(Path('..')/SRC.name/p)
for layer in scene['layers']:
    if 'file' in layer: layer['file'] = rel(layer['file'])
    for row in layer.get('cels', []): row['file'] = rel(row['file'])
scene.pop('audio', None)
IMPACT = 47  # RK's biggest recoil drawing (rk-react-03) starts on frame 47
scene['effects'] = [
    dict(type='speed_lines', start=(IMPACT-3)/FPS, end=(IMPACT+1)/FPS, mode='radial', center=[560, 1250], count=34, inner=380, color='#3A3F3A'),
    dict(type='impact', start=IMPACT/FPS, end=(IMPACT+2)/FPS, hold=1, threshold=200),
    dict(type='shake', start=(IMPACT+2)/FPS, end=(IMPACT+9)/FPS, amplitude=16, decay=3.5),
]
cue = lambda file, frame, gain: dict(file=file, frame=frame, gain_db=gain, credit=CREDIT)
scene['sound'] = dict(
    cues=[cue(k('impact-sounds', 'footstep_concrete_000.ogg'), 0, -6),       # first contact
          cue(k('impact-sounds', 'footstep_concrete_001.ogg'), 11, -6),      # second contact
          cue(k('impact-sounds', 'footstep_concrete_003.ogg'), 14, -2),      # brake
          cue(k('interface-sounds', 'question_001.ogg'), 40, -10),          # notices the mug
          cue(k('rpg-audio', 'cloth1.ogg'), 41, -4),                         # arms fly up (anticipation)
          cue(k('impact-sounds', 'impactPunch_heavy_000.ogg'), IMPACT, 0),   # recoil hit
          cue(k('interface-sounds', 'error_006.ogg'), 61, -6),               # button on the final pose
          cue(k('interface-sounds', 'tick_001.ogg'), 52, -6),               # Chad's eyes slide over
          cue(k('interface-sounds', 'tick_002.ogg'), 55, -9),               # Chad's eyes return
          dict(file='audio/room-tone.wav', at=0, gain_db=-22)],              # light ambience bed
    silence=[dict(start=(IMPACT+8)/FPS, end=(IMPACT+20)/FPS)],
    target_lufs=-14, true_peak=-1)
(ROOT/'scene.json').write_text(json.dumps(scene, indent=2))
run = lambda *a: subprocess.run([sys.executable, *map(str, a)], check=True)
run(SKILL/'mix_audio.py', ROOT/'scene.json', '--out', ROOT/'audio/mix.wav')
scene['audio'] = 'audio/mix.wav'
(ROOT/'scene.json').write_text(json.dumps(scene, indent=2))
run(SKILL/'render_scene.py', ROOT/'scene.json', '--output-dir', ROOT/'render')
(ROOT/'render/scene.mp4').replace(ROOT/'rk-chad-ember-pass.mp4')
run(SKILL/'measure_video.py', ROOT/'rk-chad-ember-pass.mp4', '--out-dir', ROOT/'measure')

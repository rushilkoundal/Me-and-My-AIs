"""Smoother RK walk-stop-react: walk breakdown drawings + RIFE in-betweens on the reaction.

Starts from ../stable-movement-test-2026-10-23 (stage, Chad, brake, foley unchanged).
Walk: re-sequenced with two unused approved breakdowns from the 22 October sheet
(09 passing, 10 knee-up), chosen by the smallest registered pose changes. Row 2/3
drawings on that sheet are drawn smaller, so they get a one-off row calibration.
Reaction: RIFE in-betweens fill the held frames between authored drawings, only
where the stable-character-animation gate accepts the pose gap.
"""
from pathlib import Path
import json, shutil, subprocess, sys
import numpy as np
from scipy import ndimage
from PIL import Image

ROOT = Path(__file__).resolve().parent
WORK = ROOT.parent.parent
BASE = ROOT.parent/'stable-movement-test-2026-10-23'
SHEET = ROOT.parent/'movement-test-2026-10-22/cels/rk-walk'
SKILL = ROOT.parent.parent/'.codex/skills/stable-character-animation/scripts'
RIFE, MODEL = WORK/'tools/rife/rife-ncnn-vulkan', WORK/'tools/rife/rife-v4.6'
FPS = 24
# Sheet row heights at contact: 392.5, 386.3, 380.0 px; match row 1 once per row.
ROW_CAL = [1.0, 392.5/386.3, 392.5/380.0]

for folder in ['assets/cels', 'assets/inbetweens', 'audio', 'render']:
    (ROOT/folder).mkdir(parents=True, exist_ok=True)
for f in ['assets/stage.png', 'assets/rk-shadow.png', 'assets/chad-shadow.png', 'audio/original-foley.wav']:
    shutil.copy2(BASE/f, ROOT/f)
scene = json.loads((BASE/'scene.json').read_text())
for layer in scene['layers']:
    for row in layer.get('cels', []):
        if (BASE/row['file']).parent.name == 'cels':
            shutil.copy2(BASE/row['file'], ROOT/row['file'])
rk = next(l for l in scene['layers'] if l['id'] == 'rk')
meta = json.loads((SHEET/'rk-walk-measurements.json').read_text())['cels']

def walk_cel(i, side):
    """Same extraction as build_test.prepare(): main component, 3px pad, row calibration."""
    m = meta[i]; b = m['bbox']
    src = Image.open(m['file']).convert('RGBA')
    crop = [max(0, b[0]-3), max(0, b[1]-3), min(src.width, b[2]+3), min(src.height, b[3]+3)]
    arr = np.asarray(src.crop(crop)).copy()
    labels, _ = ndimage.label(arr[:, :, 3] >= 32, np.ones((3, 3)))
    counts = np.bincount(labels.ravel()); counts[0] = 0
    arr[~ndimage.binary_dilation(labels == counts.argmax(), iterations=2), 3] = 0
    k = ROW_CAL[i//4]
    cel = Image.fromarray(arr)
    cel = cel.resize((round(cel.width*k), round(cel.height*k)), Image.Resampling.LANCZOS)
    xs = sorted(p[0] for p in (m.get('lowest_band_contacts') or [f['contact'] for f in m['feet']]))
    point = lambda p: [round((p[0]-crop[0])*k, 4), round((p[1]-crop[1])*k, 4)]
    anchor = point([xs[-1] if side == 'right' else xs[0], m['floor_y']])
    file = f'assets/cels/rk-walk-{i:02d}-{side}.png'
    cel.save(ROOT/file)
    bbox = cel.getchannel('A').point(lambda a: 255 if a > 8 else 0).getbbox()
    return dict(file=file, anchor=anchor, subjects={'rk': list(bbox)},
                marks={'support': anchor, 'left_sole': point([xs[0], m['floor_y']]),
                       'right_sole': point([xs[-1], m['floor_y']])})

# Stride on the first support: contact, breakdown, lift, lift, knee-up passing, contact.
WALK = [(0, 0, 'right'), (3, 9, 'right'), (5, 1, 'right'), (7, 2, 'left'), (9, 10, 'left'), (11, 3, 'left')]
walk = [dict(walk_cel(i, side), start=f/FPS) for f, i, side in WALK]
# Drawing 00's measured contact sits ~20 world px ahead of its shoe heel; the
# other five agree within 6 px. Register 00 by the heel so the planted foot holds.
HEEL_FIX = 8.0  # 9.2 matches exactly but pushes the back shoe out of the safe area
for key in ('anchor',):
    walk[0][key] = [walk[0][key][0]+HEEL_FIX, walk[0][key][1]]
walk[0]['marks'] = dict(walk[0]['marks'], support=walk[0]['anchor'])
rest = [row for row in rk['cels'] if row['start'] >= 14/FPS - 1e-9]

# Reaction: fill each held gap with RIFE in-betweens where the gate allows.
react = [row for row in rest if 'rk-react' in row['file']]
# Visual review (assets/inbetweens/*-review.jpg): hands crossing the body ghost even
# under the gate. Rejected frames hold the previous drawing. None = whole pair.
REJECT = {'rk-react-01-to-02': None, 'rk-react-02-to-03': None,
          'rk-react-05-to-06': {1}, 'rk-react-07-to-08': None}
report = []
filled = []
for a, b in zip(react, react[1:]):
    fa, fb = round(a['start']*FPS), round(b['start']*FPS)
    gap = fb - fa
    prefix = Path(a['file']).stem.replace('-right', '') + '-to-' + Path(b['file']).stem.split('-')[2]
    times = [k/gap for k in range(1, gap)]
    cmd = [sys.executable, SKILL/'inbetween_cels.py', ROOT/a['file'], ROOT/b['file'],
           '--mark-a', '%s,%s' % tuple(a['marks']['support']), '--mark-b', '%s,%s' % tuple(b['marks']['support']),
           '--times', ','.join(f'{t:.4f}' for t in times), '--scale', str(rk['scale']),
           '--rife', RIFE, '--model', MODEL, '--out-dir', ROOT/'assets/inbetweens', '--prefix', prefix]
    p = subprocess.run(cmd, capture_output=True, text=True)
    rep = json.loads((ROOT/'assets/inbetweens'/f'{prefix}-report.json').read_text())
    rejected = REJECT.get(prefix, set())
    rejected = set(range(len(rep['inbetweens']))) if rejected is None else rejected
    report.append(dict(pair=[a['file'], b['file']], frames=[fa, fb], change=rep['silhouette_change'],
                       status=rep['status'], inbetweens=len(rep['inbetweens']),
                       rejected_after_review=sorted(rejected)))
    if p.returncode:
        continue
    for k, ib in enumerate(rep['inbetweens']):
        if k in rejected:
            continue
        file = f"assets/inbetweens/{ib['file']}"
        bbox = Image.open(ROOT/file).getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
        filled.append(dict(file=file, anchor=ib['anchor'], start=(fa+k+1)/FPS, subjects={'rk': list(bbox)},
                           marks={'support': ib['anchor']}))

rk['cels'] = sorted(walk + rest + filled, key=lambda r: r['start'])
scene['source_note'] = 'Smoothed from stable-movement-test-2026-10-23 by build_smooth.py'
(ROOT/'scene.json').write_text(json.dumps(scene, indent=2))
(ROOT/'smoothing-report.json').write_text(json.dumps(dict(
    walk_sequence=[dict(frame=f, drawing=f'rk-walk-{i:02d}', support=s) for f, i, s in WALK],
    walk_row_calibration=ROW_CAL, walk_interpolation='none: every walk gap exceeds the 0.35 RIFE gate',
    reaction_pairs=report, rife_frames=len(filled)), indent=2))
for r in report:
    print(r['frames'], r['change'], r['status'])
print('RIFE frames added:', len(filled))

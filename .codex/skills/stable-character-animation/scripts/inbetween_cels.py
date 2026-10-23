"""Generate RIFE in-between cels for one actor between two authored whole-body cels.

Both cels are registered on one authored mark (pelvis, planted sole) and flattened
on flat paper, so RIFE sees only the actor's pose change; scenery never enters the
model. The RGB result is re-matted to RGBA and cropped, with its anchor recorded,
so it drops into a render_scene.py manifest like any authored cel.

Requires Pillow, numpy, scipy and a local rife-ncnn-vulkan build with a model folder.
Nothing is downloaded. Every generated cel is a candidate: inspect the review sheet.
"""
from __future__ import annotations
import argparse, json, math, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw

PAPER = (245, 242, 233)

def parse_point(text):
    x, y = (float(v) for v in text.split(','))
    return x, y

def load(path, scale):
    im = Image.open(path).convert('RGBA')
    if scale != 1:
        im = im.resize((round(im.width*scale), round(im.height*scale)), Image.Resampling.LANCZOS)
    return im

def flatten(im, offset, size):
    canvas = Image.new('RGB', size, PAPER)
    canvas.paste(im, offset, im)
    return canvas

def matte(rgb):
    """Recover the actor from flat paper; contours close the interior whites."""
    a = np.asarray(rgb)
    dist = np.max(np.abs(a.astype(np.int16) - np.array(PAPER, dtype=np.int16)), axis=2)
    core = ndimage.binary_fill_holes(ndimage.binary_closing(dist > 16, iterations=1))
    labels, _ = ndimage.label(core, np.ones((3, 3)))
    sizes = np.bincount(labels.ravel()); sizes[0] = 0
    keep = ndimage.binary_fill_holes(np.isin(labels, np.flatnonzero(sizes > max(12, int(sizes.max()*.00008)))))
    rim = ndimage.binary_propagation(keep, mask=dist > 2) & ~keep
    alpha = np.zeros(dist.shape, dtype=np.uint8)
    alpha[keep] = 255
    alpha[rim] = np.clip((dist[rim]-2)*255/14, 0, 255).astype(np.uint8)
    return Image.fromarray(np.dstack([a, alpha]))

def run_rife(rife, model, a, b, t, out):
    cmd = [str(rife), '-0', str(a), '-1', str(b), '-o', str(out), '-m', str(model),
           '-s', f'{t:.6f}', '-z']
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode or not out.exists():
        raise RuntimeError(p.stderr[-2000:] or 'RIFE produced no frame')

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('cel_a', type=Path); ap.add_argument('cel_b', type=Path)
    ap.add_argument('--mark-a', type=parse_point, required=True, help='native x,y of the registration mark in cel A')
    ap.add_argument('--mark-b', type=parse_point, required=True, help='same body landmark in cel B')
    ap.add_argument('--count', type=int, default=1, help='evenly spaced in-betweens (ignored with --times)')
    ap.add_argument('--times', type=lambda s: [float(v) for v in s.split(',')], help='explicit 0..1 spacing, e.g. 0.25,0.6 for an ease')
    ap.add_argument('--scale', type=float, default=1.0, help='work scale; keep the shot scale so lines match')
    ap.add_argument('--rife', type=Path, required=True); ap.add_argument('--model', type=Path, required=True)
    ap.add_argument('--out-dir', type=Path, required=True); ap.add_argument('--prefix', default='inbetween')
    # Calibrated on RK cels (2026-10-23): <=0.31 clean, 0.29 soft fingers,
    # 0.66 broken shoe/missing hand, 0.78 see-through leg. See references/smoothing.md.
    ap.add_argument('--max-change', type=float, default=.35, help='reject pairs whose silhouettes differ more than this')
    ap.add_argument('--caution', type=float, default=.20, help='above this, check hands and shoes closely')
    ap.add_argument('--force', action='store_true', help='interpolate even when the pose gap is too large')
    args = ap.parse_args()
    times = args.times or [(i+1)/(args.count+1) for i in range(args.count)]
    if not times or any(not 0 < t < 1 for t in times):
        sys.exit('In-between times must lie strictly between 0 and 1')

    a, b = load(args.cel_a, args.scale), load(args.cel_b, args.scale)
    ma = [v*args.scale for v in args.mark_a]; mb = [v*args.scale for v in args.mark_b]
    # Shared canvas: both marks land on one pivot with generous padding.
    left = max(ma[0], mb[0]); top = max(ma[1], mb[1])
    right = max(a.width-ma[0], b.width-mb[0]); bottom = max(a.height-ma[1], b.height-mb[1])
    pad = 32
    pivot = (round(left+pad), round(top+pad))
    size = (round(left+right+2*pad), round(top+bottom+2*pad))
    size = (size[0]+size[0] % 2, size[1]+size[1] % 2)
    oa = (round(pivot[0]-ma[0]), round(pivot[1]-ma[1])); ob = (round(pivot[0]-mb[0]), round(pivot[1]-mb[1]))

    sil_a = np.zeros(size[::-1], bool); sil_b = np.zeros(size[::-1], bool)
    sil_a[oa[1]:oa[1]+a.height, oa[0]:oa[0]+a.width] = np.asarray(a.getchannel('A')) > 8
    sil_b[ob[1]:ob[1]+b.height, ob[0]:ob[0]+b.width] = np.asarray(b.getchannel('A')) > 8
    change = float((sil_a ^ sil_b).sum() / max(1, (sil_a | sil_b).sum()))
    report = dict(cel_a=str(args.cel_a), cel_b=str(args.cel_b), registration=[args.mark_a, args.mark_b],
                  silhouette_change=round(change, 4), max_change=args.max_change, model=str(args.model),
                  limitation='Model-generated candidates; inspect hands, shoes, face and emblem before use.',
                  inbetweens=[])
    args.out_dir.mkdir(parents=True, exist_ok=True)
    if change > args.max_change and not args.force:
        report['status'] = 'rejected: pose gap too large; author a breakdown drawing between these cels'
        (args.out_dir/f'{args.prefix}-report.json').write_text(json.dumps(report, indent=2))
        sys.exit(f'Silhouette change {change:.2f} > {args.max_change}: draw a breakdown instead (or --force to test).')

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        fa, fb = flatten(a, oa, size), flatten(b, ob, size)
        fa.save(tmp/'a.png'); fb.save(tmp/'b.png')
        mids = []
        for i, t in enumerate(times):
            raw = tmp/f'{i}.png'
            run_rife(args.rife, args.model, tmp/'a.png', tmp/'b.png', t, raw)
            rgb = Image.open(raw).convert('RGB')
            cel = matte(rgb); box = cel.getchannel('A').getbbox()
            cel = cel.crop(box)
            if args.scale != 1:
                # Back to native size: the manifest's layer scale applies to every cel.
                cel = cel.resize((round(cel.width/args.scale), round(cel.height/args.scale)), Image.Resampling.LANCZOS)
            name = f'{args.prefix}-{i:02d}.png'; cel.save(args.out_dir/name)
            # Native anchor of the pivot in the cropped cel, at the cel's own scale.
            anchor = [(pivot[0]-box[0])/args.scale, (pivot[1]-box[1])/args.scale]
            report['inbetweens'].append(dict(file=name, t=t, anchor=[round(v, 3) for v in anchor]))
            mids.append(rgb)
        # Review sheet: A, candidates, B at one scale.
        tiles = [fa, *mids, fb]; th = 480; tw = round(size[0]*th/size[1])
        sheet = Image.new('RGB', (tw*len(tiles), th+24), PAPER); d = ImageDraw.Draw(sheet)
        labels = ['A', *[f't={t:.2f}' for t in times], 'B']
        for k, (im, label) in enumerate(zip(tiles, labels)):
            sheet.paste(im.resize((tw, th), Image.Resampling.LANCZOS), (k*tw, 24))
            d.text((k*tw+6, 6), label, fill='#26332f')
        sheet.save(args.out_dir/f'{args.prefix}-review.jpg', quality=93)
    report['status'] = ('candidates written; check hands, fingers and shoes closely' if change > args.caution
                        else 'candidates written; visual review pending')
    if change > args.max_change:
        report['status'] = 'forced past the gate; expect ghosted or missing limbs'
    (args.out_dir/f'{args.prefix}-report.json').write_text(json.dumps(report, indent=2))
    print(json.dumps({k: report[k] for k in ['silhouette_change', 'inbetweens', 'status']}, indent=2))

if __name__ == '__main__':
    main()

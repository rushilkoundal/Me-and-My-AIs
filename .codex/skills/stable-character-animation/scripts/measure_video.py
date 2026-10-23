"""Measure a video's motion and sound and compare it with the Ember benchmark.

  python3 scripts/measure_video.py video.mp4 [--out-dir dir]

Reports cuts, share of frames with visible change, holds, loudness, sound hits per
second, how many strong hits land within 2 frames of a visible change, music-bed and
silence share. Writes <name>-measure.json and <name>-timeline.png. Needs numpy, scipy,
Pillow and FFmpeg. Works on local files only; never point it at a public player.
"""
from __future__ import annotations
import argparse, json, re, shutil, subprocess, sys
from pathlib import Path
import numpy as np
from scipy import ndimage, signal
from PIL import Image, ImageDraw

SR, HOP = 22050, 256
# Ember, 12 public reels measured 23 Oct 2026: (min, median, max). See references/benchmark-evidence.md.
BENCHMARK = {
    'integrated_lufs': (-14.4, -14.1, -14.0),
    'frames_with_visible_change_pct': (46.6, 61.5, 87.8),
    'holds_ge_12f_pct_time': (0.0, 22.2, 41.2),
    'sound_hits_per_s': (1.5, 2.4, 4.9),
    'strong_hits_on_visible_change_pct': (91.8, 100.0, 100.0),
    'near_silence_pct': (0.1, 17.5, 32.6),
}

def ff_bin(name):
    b = shutil.which(name) or str(Path.home()/'bin'/name)
    if not Path(b).exists():
        sys.exit(f'{name} is unavailable')
    return b

def measure(path: Path, out_dir: Path):
    ff = ff_bin('ffmpeg')
    probe = subprocess.run([ff_bin('ffprobe'), '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                            'stream=r_frame_rate', '-of', 'csv=p=0', str(path)], capture_output=True, text=True).stdout
    num, den = probe.strip().split('/'); fps = float(num)/float(den)
    raw = subprocess.run([ff, '-v', 'error', '-i', str(path), '-vf', 'scale=180:320', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         capture_output=True, check=True).stdout
    frames = np.frombuffer(raw, np.uint8).reshape(-1, 320, 180, 3)
    gray = frames.astype(np.float32) @ np.array([.299, .587, .114], np.float32)
    changed = (np.abs(np.diff(gray, axis=0)) > 18).mean(axis=(1, 2))
    q = (frames[:, ::2, ::2] // 32).reshape(len(frames), -1, 3)
    codes = q[..., 0]*64+q[..., 1]*8+q[..., 2]
    hists = np.stack([np.bincount(c, minlength=512) for c in codes]).astype(np.float32)
    hists /= hists.sum(1, keepdims=True)
    hist = 0.5*np.abs(np.diff(hists, axis=0)).sum(1)
    cuts = [i+1 for i in range(len(changed)) if changed[i] > .18 and hist[i] > .12]
    moving = changed > .0015
    n = len(frames); dur = n/fps
    events = sorted(set([0]+[i+1 for i, m in enumerate(moving) if m]+cuts+[n]))
    holds = np.diff(events)

    has_audio = subprocess.run([ff_bin('ffprobe'), '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index',
                                '-of', 'csv=p=0', str(path)], capture_output=True, text=True).stdout.strip() != ''
    res = dict(file=path.name, duration_s=round(dur, 2), fps=fps, cuts=len(cuts),
               frames_with_visible_change_pct=round(100*float(moving.mean()), 1),
               holds_ge_12f_pct_time=round(100*float(holds[holds >= 12].sum()/n), 1))
    onsets = np.array([]); S = None
    if has_audio:
        y = np.frombuffer(subprocess.run([ff, '-v', 'error', '-i', str(path), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                                         capture_output=True, check=True).stdout, np.float32)
        f, t, Z = signal.stft(y, SR, nperseg=1024, noverlap=1024-HOP); S = np.abs(Z)
        H = ndimage.median_filter(S, size=(1, 17)); P = ndimage.median_filter(S, size=(17, 1))
        mh = H**2/(H**2+P**2+1e-12)
        harm = (mh*S**2).sum(0)/((S**2).sum(0)+1e-12)
        rms_db = 10*np.log10((S**2).mean(0)+1e-12)
        flux = np.r_[0, np.maximum(0, np.diff(np.log1p(S*100), axis=1)).sum(0)]
        flux = (flux-np.median(flux))/(np.percentile(flux, 99)-np.median(flux)+1e-9)
        peaks, props = signal.find_peaks(flux, height=.35, distance=int(.09*SR/HOP), prominence=.25)
        onsets = t[peaks]; strong = onsets[props['peak_heights'] > .6]
        loud = rms_db > rms_db.max()-50
        music = ndimage.uniform_filter1d((harm > .6) & loud, int(.5*SR/HOP)) > .6
        vis = np.array([i+1 for i, m in enumerate(moving) if m])/fps
        sync = [abs(vis[np.argmin(np.abs(vis-x))]-x) <= 2/fps for x in strong] if len(vis) else []
        err = subprocess.run([ff, '-hide_banner', '-nostats', '-i', str(path), '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                             capture_output=True, text=True).stderr
        tail = err[err.rfind('Summary:'):]
        get = lambda k: float(re.search(k+r':\s+(-?[\d.]+)', tail).group(1))
        res.update(integrated_lufs=get('I'), true_peak_dbtp=get('Peak'),
                   sound_hits_per_s=round(len(onsets)/dur, 2),
                   strong_hits_on_visible_change_pct=round(100*float(np.mean(sync)), 1) if sync else None,
                   music_bed_pct=round(100*float(music.mean()), 1),
                   near_silence_pct=round(100*float((rms_db < rms_db.max()-38).mean()), 1))
    comparison = {}
    for k, (lo, med, hi) in BENCHMARK.items():
        v = res.get(k)
        comparison[k] = dict(value=v, ember_min=lo, ember_median=med, ember_max=hi,
                             status='n/a' if v is None else 'in range' if lo <= v <= hi else 'below' if v < lo else 'above')
    res['vs_ember'] = comparison
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir/f'{path.stem}-measure.json').write_text(json.dumps(res, indent=2))
    # Timeline: spectrogram, sound hits, visual change, cuts.
    W = 1600; img = Image.new('RGB', (W, 440), 'white'); d = ImageDraw.Draw(img)
    X = lambda s: int(s/dur*(W-1))
    if S is not None:
        sp = 20*np.log10(S[:300]+1e-6); sp = np.clip((sp-sp.max()+70)/70, 0, 1)
        img.paste(Image.fromarray((255*(1-sp[::-1])).astype(np.uint8)).resize((W, 220)).convert('RGB'), (0, 0))
        for o in onsets: d.line([(X(o), 225), (X(o), 300)], fill='#dd5500')
    for i, c in enumerate(changed): d.line([(X((i+1)/fps), 400), (X((i+1)/fps), 400-min(80, c*400))], fill='#555555')
    for c in cuts: d.line([(X(c/fps), 0), (X(c/fps), 440)], fill='#cc0000', width=2)
    for s in range(int(dur)+1): d.text((X(s)+2, 424), f'{s}s', fill='black')
    img.save(out_dir/f'{path.stem}-timeline.png')
    return res

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('video', type=Path); ap.add_argument('--out-dir', type=Path)
    a = ap.parse_args()
    res = measure(a.video, a.out_dir or a.video.parent)
    print(f"{'measure':38} {'ours':>8} {'Ember min/med/max':>22}  status")
    for k, c in res['vs_ember'].items():
        print(f"{k:38} {str(c['value']):>8} {c['ember_min']:>7}/{c['ember_median']}/{c['ember_max']:<7}  {c['status']}")

if __name__ == '__main__':
    main()

"""Build a scene's soundtrack from frame-timed cues in its manifest (Ember-style sound pass).

Reads the manifest's "sound" block, places every effect on its frame, adds music
stings and voices, ducks music under voices, cuts hard silences, then masters with
FFmpeg loudnorm (two passes) to -14 LUFS integrated / -1 dBTP. Writes the mix, a cue
report and credits.txt (attribution lines for sounds whose licence needs one).

  python3 scripts/mix_audio.py scene.json --out audio/mix.wav

Then set the manifest's "audio" to that file and render. Needs numpy and FFmpeg.
"""
from __future__ import annotations
import argparse, json, re, shutil, subprocess, sys
from pathlib import Path
import numpy as np

SR = 48000

def ffmpeg():
    ff = shutil.which('ffmpeg') or str(Path.home()/'bin/ffmpeg')
    if not Path(ff).exists():
        sys.exit('FFmpeg is unavailable; install/locate it before mixing')
    return ff

def load(path, ff):
    raw = subprocess.run([ff, '-v', 'error', '-i', str(path), '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()

def db(x):
    return 10**(x/20)

def ramp(n, fade_in, fade_out):
    g = np.ones(n, np.float32)
    a, b = min(n, int(fade_in*SR)), min(n, int(fade_out*SR))
    if a: g[:a] = np.linspace(0, 1, a)
    if b: g[n-b:] *= np.linspace(1, 0, b)
    return g

def place(bus, clip, start_s, gain_db=0.0, fade_in=0.0, fade_out=0.005, length_s=None, offset_s=0.0):
    clip = clip[int(offset_s*SR):]
    if length_s is not None:
        clip = clip[:int(length_s*SR)]
    a = int(round(start_s*SR)); clip = clip[:max(0, len(bus)-a)]
    if a < 0 or not len(clip):
        return
    bus[a:a+len(clip)] += clip*ramp(len(clip), fade_in, fade_out)[:, None]*db(gain_db)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('manifest', type=Path)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    ff = ffmpeg()
    doc = json.loads(args.manifest.read_text()); root = args.manifest.resolve().parent
    fps = int(doc.get('fps', 24)); dur = float(doc['duration']); snd = doc.get('sound', {})
    res = lambda p: Path(p) if Path(p).is_absolute() else root/p
    when = lambda c: c['frame']/fps if 'frame' in c else float(c['at'])
    n = int(round(dur*SR))
    sfx, music, voice = (np.zeros((n, 2), np.float32) for _ in range(3))
    cache = {}
    def clip(p):
        if p not in cache:
            if not res(p).is_file():
                sys.exit(f'Missing sound file: {p}')
            cache[p] = load(res(p), ff)
        return cache[p]
    report = []
    for c in snd.get('cues', []):
        place(sfx, clip(c['file']), when(c), c.get('gain_db', 0), c.get('fade_in', 0), c.get('fade_out', .005),
              c.get('length'), c.get('offset', 0))
        report.append(dict(kind='sfx', file=c['file'], time=round(when(c), 4), frame=round(when(c)*fps)))
    for m in snd.get('music', []):
        place(music, clip(m['file']), float(m['start']), m.get('gain_db', -6), m.get('fade_in', .02),
              m.get('fade_out', .06), float(m['end'])-float(m['start']), m.get('offset', 0))
        report.append(dict(kind='music', file=m['file'], start=m['start'], end=m['end']))
    for v in snd.get('voices', []):
        place(voice, clip(v['file']), when(v), v.get('gain_db', 0), .003, .01)
        report.append(dict(kind='voice', file=v['file'], time=round(when(v), 4)))
    # Duck music under voices with short shoulders.
    if voice.any():
        env = np.abs(voice).max(1) > 1e-3
        k = int(.08*SR)
        env = np.convolve(env.astype(np.float32), np.ones(2*k+1, np.float32), 'same') > 0
        g = np.where(env, db(snd.get('duck_db', -9)), 1.0).astype(np.float32)
        g = np.convolve(g, np.ones(k, np.float32)/k, 'same')
        music *= g[:, None]
    mix = sfx+music+voice
    # Hard silences (Ember's blocks): mute everything with 5 ms ramps to avoid clicks.
    for s in snd.get('silence', []):
        a, b = int(float(s['start'])*SR), int(float(s['end'])*SR)
        r = int(.005*SR)
        g = np.ones(n, np.float32); g[a:b] = 0
        g[max(0, a-r):a] = np.linspace(1, 0, a-max(0, a-r)); g[b:b+r] = np.linspace(0, 1, len(g[b:b+r]))
        mix *= g[:, None]
        report.append(dict(kind='silence', start=s['start'], end=s['end']))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    raw = args.out.with_suffix('.premaster.wav')
    subprocess.run([ff, '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', str(raw)],
                   input=np.clip(mix, -4, 4).astype(np.float32).tobytes(), check=True)
    I, TP = float(snd.get('target_lufs', -14)), float(snd.get('true_peak', -1))
    if not mix.any():
        sys.exit('The mix is silent; add cues before mastering')
    measure = lambda path: json.loads(re.findall(r'\{[^{}]*\}', subprocess.run(
        [ff, '-hide_banner', '-i', str(path), '-af', f'loudnorm=I={I}:TP={TP}:LRA=11:print_format=json', '-f', 'null', '-'],
        capture_output=True, text=True).stderr)[-1])
    m = measure(raw)
    # Short transients hit the true-peak ceiling before the loudness target, so raise
    # the gain into a true-peak limiter first; loudnorm then only trims linearly.
    gain = I-float(m['input_i'])
    if float(m['input_tp'])+gain > TP:
        limited = args.out.with_suffix('.limited.wav')
        subprocess.run([ff, '-v', 'error', '-y', '-i', str(raw), '-af',
                        f'volume={gain+0.5:.2f}dB,alimiter=limit={db(TP-0.6):.4f}:attack=1:release=40:level=disabled',
                        '-ar', str(SR), str(limited)], check=True)
        raw.unlink(); limited.replace(raw)
        m = measure(raw)
    af = (f"loudnorm=I={I}:TP={TP}:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run([ff, '-v', 'error', '-y', '-i', str(raw), '-af', af, '-ar', str(SR), str(args.out)], check=True)
    raw.unlink()
    check = subprocess.run([ff, '-hide_banner', '-nostats', '-i', str(args.out), '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                           capture_output=True, text=True).stderr
    tail = check[check.rfind('Summary:'):]
    got = {k: float(re.search(k+r':\s+(-?[\d.]+)', tail).group(1)) for k in ['I', 'Peak']}
    if got['I'] > I+0.2:
        # loudnorm's linear pass can land hot on short clips; trimming down is always peak-safe.
        trimmed = args.out.with_suffix('.trim.wav')
        subprocess.run([ff, '-v', 'error', '-y', '-i', str(args.out), '-af', f"volume={I-got['I']:.2f}dB", str(trimmed)], check=True)
        trimmed.replace(args.out)
        tail = subprocess.run([ff, '-hide_banner', '-nostats', '-i', str(args.out), '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                              capture_output=True, text=True).stderr
        tail = tail[tail.rfind('Summary:'):]
        got = {k: float(re.search(k+r':\s+(-?[\d.]+)', tail).group(1)) for k in ['I', 'Peak']}
    credits = sorted({f"{c['file']}: {c['credit']}" for c in snd.get('cues', [])+snd.get('music', []) if c.get('credit')})
    (args.out.parent/'credits.txt').write_text('\n'.join(credits)+('\n' if credits else ''))
    (args.out.parent/'mix-report.json').write_text(json.dumps(dict(
        target=dict(integrated_lufs=I, true_peak_dbtp=TP), measured=dict(integrated_lufs=got['I'], true_peak_dbtp=got['Peak']),
        cues=report), indent=2))
    print(f"{args.out}  {got['I']:.1f} LUFS, {got['Peak']:.1f} dBTP, {len(report)} cues")

if __name__ == '__main__':
    main()

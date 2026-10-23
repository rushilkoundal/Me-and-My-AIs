"""Render authored whole-cel scenes; validate framing and declared world contacts.

Requires Pillow plus FFmpeg for MP4. No model downloads, rigging or interpolation
of body artwork. All paths are relative to the manifest unless absolute.
Whole layers can travel on eased paths and loop cycles; frame effects (shake,
flash, impact frames, speed lines, echo) are drawn over the composite after checks.
"""
from __future__ import annotations
import argparse, hashlib, json, math, random, shutil, subprocess, sys
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageOps

class SceneError(ValueError):
    pass

def resolve(root, name):
    p = Path(name)
    return p if p.is_absolute() else root / p

def active(rows, t):
    valid = [r for r in rows if r['start'] <= t + 1e-8]
    if not valid:
        raise SceneError(f'No authored cel at time {t:.4f}')
    return valid[-1]

def _back(u, s=1.70158):
    return 1+(s+1)*(u-1)**3+s*(u-1)**2

def _spring(u, zeta=.35, cycles=2.2):
    # Damped settle that overshoots and lands exactly on 1 at u=1.
    w = 2*math.pi*cycles
    return 1-math.exp(-zeta*w*u)*math.cos(w*math.sqrt(1-zeta*zeta)*u)*(1-u)

EASES = {
    'linear': lambda u: u,
    'in': lambda u: u*u, 'out': lambda u: 1-(1-u)**2,
    'inout': lambda u: 2*u*u if u < .5 else 1-(-2*u+2)**2/2,
    'in3': lambda u: u**3, 'out3': lambda u: 1-(1-u)**3,
    'inout3': lambda u: 4*u**3 if u < .5 else 1-(-2*u+2)**3/2,
    'back': _back, 'spring': _spring,
    'hold': lambda u: 0.0 if u < 1 else 1.0,
}

def position(layer, t):
    """Root position from [seconds, x, y, ease?] keys; ease shapes the segment ending at that key."""
    keys = layer.get('position_keys')
    if not keys:
        return layer.get('position', [0, 0])
    if t <= keys[0][0]:
        return keys[0][1:3]
    for a, b in zip(keys, keys[1:]):
        if t <= b[0]:
            u = EASES[b[3] if len(b) > 3 else 'linear']((t-a[0])/(b[0]-a[0]))
            return [a[j] + u*(b[j]-a[j]) for j in [1, 2]]
    return keys[-1][1:3]

def cycle_row(layer, f, fps):
    """Looping drawings over a time window (walk/run/hammer cycles) on fixed exposures."""
    for c in layer.get('cycles', []):
        a, b = round(c['start']*fps), round(c['end']*fps)
        if a <= f < b:
            return c['frames'][((f-a)//int(c.get('hold', 2))) % len(c['frames'])]
    return None

class Scene:
    def __init__(self, manifest):
        self.path = Path(manifest).resolve()
        self.root = self.path.parent
        self.doc = json.loads(self.path.read_text())
        d = self.doc
        self.w, self.h = map(int, d.get('size', [1080, 1920]))
        self.fps = int(d.get('fps', 24))
        self.duration = float(d['duration'])
        if min(self.w, self.h, self.fps, self.duration) <= 0:
            raise SceneError('Size, fps and duration must be positive')
        self.n = round(self.duration*self.fps)
        if abs(self.n/self.fps-self.duration) > .0001:
            raise SceneError('Duration must resolve to whole output frames')
        self.safe = d.get('safe_area', [80, 180, 920, 1600])
        self.layers = sorted(d['layers'], key=lambda x: x.get('z', 0))
        ids = [x['id'] for x in self.layers]
        if len(ids) != len(set(ids)):
            raise SceneError('Layer ids must be unique')
        for layer in self.layers:
            if float(layer.get('scale', 1)) <= 0:
                raise SceneError('Layer scale must be positive')
            if not 0 <= float(layer.get('opacity', 1)) <= 1:
                raise SceneError('Layer opacity must be in 0..1')
            rows = layer.get('cels', [dict(start=0, file=layer.get('file'))])
            if not rows or rows[0]['start'] != 0 or any(a['start'] >= b['start'] for a,b in zip(rows,rows[1:])):
                raise SceneError(f"Cels need start0 and strictly increasing times: {layer['id']}")
            for row in rows:
                if any(k in row for k in ['scale', 'rotation', 'warp']):
                    raise SceneError('Use fixed layer scale and authored artwork, not per-cel distortion')
                if row['start'] < 0 or row['start'] >= self.duration:
                    raise SceneError('Cel start outside scene duration')
                if not row.get('file') or not resolve(self.root,row['file']).is_file():
                    raise SceneError(f"Missing cel file: {row.get('file')}")
            layer['_rows'] = rows
            keys = layer.get('position_keys', [])
            if any(len(x) not in (3, 4) for x in keys) or any(a[0]>=b[0] for a,b in zip(keys,keys[1:])):
                raise SceneError('Position keys must be increasing [seconds,x,y,ease?] records')
            if any(len(x) == 4 and x[3] not in EASES for x in keys):
                raise SceneError(f'Unknown ease; use one of {sorted(EASES)}')
            for c in layer.get('cycles', []):
                if not c.get('frames') or c['start'] >= c['end'] or int(c.get('hold', 2)) < 1:
                    raise SceneError(f"Cycle needs frames, start<end and hold>=1: {layer['id']}")
                for row in c['frames']:
                    if any(k in row for k in ['scale', 'rotation', 'warp']) or not resolve(self.root, row['file']).is_file():
                        raise SceneError(f"Cycle frame missing or distorted: {row.get('file')}")
        self.source_hashes = {r['file']:hashlib.sha256(resolve(self.root,r['file']).read_bytes()).hexdigest()
                              for l in self.layers for r in l['_rows']+[x for c in l.get('cycles', []) for x in c['frames']]}
        for e in d.get('effects', []):
            if e.get('type') not in EFFECTS or e.get('start', 0) >= e.get('end', self.duration):
                raise SceneError(f"Effects need a known type ({sorted(EFFECTS)}) and start<end: {e}")
        self._history = []

    @lru_cache(maxsize=256)
    def picture(self, file, scale, opacity):
        im = Image.open(resolve(self.root, file)).convert('RGBA')
        im = im.resize((round(im.width*scale), round(im.height*scale)), Image.Resampling.LANCZOS)
        if opacity != 1:
            im.putalpha(im.getchannel('A').point(lambda a: round(a*opacity)))
        return im

    def frame(self, f):
        t = f/self.fps
        canvas = Image.new('RGBA',(self.w,self.h),self.doc.get('background','#F3F1DF'))
        world = {}; boxes = []; failures = []
        for layer in self.layers:
            cel = cycle_row(layer, f, self.fps) or active(layer['_rows'],t)
            scale = float(layer.get('scale',1)); opacity = float(layer.get('opacity',1))
            anchor = cel.get('anchor',layer.get('anchor',[0,0])); pos = position(layer,t)
            tx,ty = round(pos[0]-anchor[0]*scale),round(pos[1]-anchor[1]*scale)
            pic = self.picture(cel['file'],scale,opacity)
            canvas.alpha_composite(pic,(tx,ty))
            def point(p):
                return [tx+p[0]*scale,ty+p[1]*scale]
            world[layer['id']] = {k:point(v) for k,v in cel.get('marks',layer.get('marks',{})).items()}
            regions = cel.get('subjects',layer.get('subjects',{})).copy()
            if layer.get('check_alpha_bounds'):
                b = pic.getchannel('A').point(lambda a:255 if a>8 else 0).getbbox()
                if b:
                    # Already scaled; convert back for common point transform.
                    regions[layer['id']+'_alpha']=[v/scale for v in b]
            for name,b in regions.items():
                q=point(b[:2])+point(b[2:]);boxes.append(dict(layer=layer['id'],subject=name,bbox=q))
                lo=self.safe
                if q[0]<lo[0] or q[1]<lo[1] or q[2]>lo[2] or q[3]>lo[3]:
                    failures.append(f'Framing: {name} {q} outside {lo}')
        for contact in self.doc.get('contacts',[]):
            if not contact.get('start',0)<=t<contact.get('end',self.duration):
                continue
            try:
                a=world[contact['layer']][contact['mark']]
                if 'other_layer' in contact:
                    b=world[contact['other_layer']][contact['other_mark']]
                else:
                    b=contact['world']
            except KeyError as exc:
                raise SceneError(f'Missing authored contact mark: {contact}') from exc
            distance=math.dist(a,b)
            if distance>contact.get('tolerance',3):
                failures.append(f"Contact {contact.get('name',contact['mark'])} moved {distance:.2f}px")
        if failures:
            raise SceneError(f'Frame{f},time{t:.4f}: '+'; '.join(failures))
        return canvas.convert('RGB'),dict(frame=f,time=t,boxes=boxes,marks=world)

    def render(self, f):
        """Checked frame plus effects; call in frame order so echo trails have history."""
        im, check = self.frame(f)
        clean = im
        for e in self.doc.get('effects', []):
            a, b = round(e.get('start', 0)*self.fps), round(e.get('end', self.duration)*self.fps)
            if a <= f < b:
                im = EFFECTS[e['type']](im, e, f-a, b-a, self)
        self._history = (self._history+[clean])[-8:]
        return im, check

# Frame effects. k = frame index inside the effect window, n = its length.
def fx_shake(im, e, k, n, scene):
    """Decaying whole-frame shake, re-picked on 2s so it reads as drawn."""
    rng = random.Random(e.get('seed', 7)*1000+k//int(e.get('hold', 2)))
    amp = float(e.get('amplitude', 18))*math.exp(-float(e.get('decay', 4))*k/max(1, n))
    dx, dy = round(rng.uniform(-amp, amp)), round(rng.uniform(-amp, amp))
    # Extend the frame's own edge pixels so the uncovered border never shows a seam.
    w, h = im.size; p = int(amp)+1
    big = Image.new('RGB', (w+2*p, h+2*p)); big.paste(im, (p, p))
    big.paste(im.crop((0, 0, w, 1)).resize((w, p)), (p, 0)); big.paste(im.crop((0, h-1, w, h)).resize((w, p)), (p, h+p))
    big.paste(big.crop((p, 0, p+1, h+2*p)).resize((p, h+2*p)), (0, 0))
    big.paste(big.crop((w+p-1, 0, w+p, h+2*p)).resize((p, h+2*p)), (w+p, 0))
    return big.crop((p-dx, p-dy, p-dx+w, p-dy+h))

def fx_flash(im, e, k, n, scene):
    """Full-frame flash that fades out across the window."""
    alpha = float(e.get('opacity', .85))*(1-k/max(1, n))
    return Image.blend(im, Image.new('RGB', im.size, e.get('color', '#FFFFFF')), alpha)

def fx_impact(im, e, k, n, scene):
    """Black-and-white impact frames: threshold the frame, inverting every `hold` frames."""
    g = ImageOps.grayscale(im).point(lambda v: 255 if v > int(e.get('threshold', 170)) else 0)
    if (k//int(e.get('hold', 1))) % 2 == int(e.get('invert_first', 1)):
        g = ImageOps.invert(g)
    return g.convert('RGB')

def fx_speed_lines(im, e, k, n, scene):
    """Radial (focus) or directional speed lines over the frame, re-drawn on 2s."""
    rng = random.Random(e.get('seed', 3)*1000+k//int(e.get('hold', 2)))
    im = im.copy(); d = ImageDraw.Draw(im); w, h = im.size
    cx, cy = e.get('center', [w/2, h/2]); color = e.get('color', '#26332F')
    reach = max(math.dist((cx, cy), c) for c in [(0, 0), (w, 0), (0, h), (w, h)])
    for _ in range(int(e.get('count', 28))):
        if e.get('mode', 'radial') == 'radial':
            # Lines start a clear ring away from the focus (the character) and run past the edge.
            ang = rng.uniform(0, 2*math.pi); r0 = float(e.get('inner', 420))*rng.uniform(1, 1.5)
            pts = [(cx+math.cos(ang)*r0, cy+math.sin(ang)*r0), (cx+math.cos(ang)*reach, cy+math.sin(ang)*reach)]
        else:
            ang = math.radians(float(e.get('angle', 180))); x, y = rng.uniform(0, w), rng.uniform(0, h)
            L = rng.uniform(.15, .45)*w
            pts = [(x, y), (x+math.cos(ang)*L, y+math.sin(ang)*L)]
        d.line(pts, fill=color, width=rng.choice([2, 3, 4]))
    return im

def fx_echo(im, e, k, n, scene):
    """Ghost trail of the previous frames (laughter, panic), strongest on recent ones."""
    out = im
    for i, old in enumerate(reversed(scene._history[-int(e.get('trail', 3)):])):
        out = Image.blend(out, ImageChops.darker(out, old), float(e.get('strength', .35))/(i+1))
    return out

EFFECTS = {'shake': fx_shake, 'flash': fx_flash, 'impact': fx_impact,
           'speed_lines': fx_speed_lines, 'echo': fx_echo}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest',type=Path)
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--check-only',action='store_true')
    args=parser.parse_args();scene=Scene(args.manifest)
    args.output_dir.mkdir(parents=True,exist_ok=True)
    selected=set(round(i*(scene.n-1)/min(11,scene.n-1)) for i in range(min(12,scene.n))) if scene.n>1 else {0}
    thumbs=[];audit=[]
    for f in range(scene.n):
        im,check=scene.render(f);audit.append(check)
        if f in selected:
            thumb=im.resize((216,384));ImageDraw.Draw(thumb).text((8,365),f'{f/scene.fps:.3f}s',fill='#24322f');thumbs.append(thumb)
    sheet=Image.new('RGB',(4*216,math.ceil(len(thumbs)/4)*384),'#f5f2ea')
    for j,im in enumerate(thumbs):sheet.paste(im,((j%4)*216,(j//4)*384))
    sheet.save(args.output_dir/'contact-sheet.jpg',quality=94)
    report=dict(duration=scene.duration,fps=scene.fps,frames=scene.n,size=[scene.w,scene.h],
                source_sha256=scene.source_hashes,geometry_checks='passed',
                limitation='Declared geometry only; inspect actual anatomy, identity, contacts and timing visually.',frame_audit=audit)
    (args.output_dir/'geometry-audit.json').write_text(json.dumps(report,indent=2))
    Scene(args.manifest).frame(scene.n//2)[0].resize((360,640)).save(args.output_dir/'phone-preview.png')
    if args.check_only:
        print('Geometry checks passed; visual contact sheet prepared.');return
    ff=shutil.which('ffmpeg')
    if not ff and (Path.home()/'bin/ffmpeg').is_file():ff=str(Path.home()/'bin/ffmpeg')
    if not ff:raise SceneError('FFmpeg is unavailable; install/locate it explicitly before MP4 export')
    output=args.output_dir/'scene.mp4'
    cmd=[ff,'-y','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{scene.w}x{scene.h}','-r',str(scene.fps),'-i','-']
    if scene.doc.get('audio'):
        audio=resolve(scene.root,scene.doc['audio'])
        if not audio.is_file():raise SceneError('Configured final audio mix is missing')
        cmd+=['-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:a','aac','-b:a','256k']
    cmd+=['-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-t',str(scene.duration),'-movflags','+faststart',str(output)]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        scene=Scene(args.manifest)  # fresh effect history for the encode pass
        for f in range(scene.n):process.stdin.write(scene.render(f)[0].tobytes())
        process.stdin.close()
        if process.wait():raise SceneError('FFmpeg encode failed')
    except BaseException:
        if process.poll() is None:process.terminate();process.wait()
        raise
    print(output)

if __name__=='__main__':
    try:main()
    except (SceneError,KeyError,TypeError) as e:
        print(f'Scene validation failed: {e}',file=sys.stderr);sys.exit(2)

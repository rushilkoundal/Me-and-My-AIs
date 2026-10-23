"""Prepare clean whole-body cels and a grounded stage for the installed skill.

No detached limbs, body warps, crossfades or generated in-betweens. Reuses the
creator's preferred 22 October drawings. Row calibrations compensate the source
sheet resolution once, in authoring; runtime actor scale is constant.
"""
from pathlib import Path
import json, math, wave
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'movement-test-2026-10-22'
W, H, FPS, DURATION, FLOOR = 1080, 1920, 24, 3.75, 1570
ROW_SCALES = {'rk-walk':[2.30]*3, 'rk-brake':[2.45,2.56,2.65],
              'rk-react':[2.50,2.53,2.64], 'chad-act':[1.30]*3}
ACTOR_SCALE = {'rk':2.07, 'chad':1.17}
DATA = {s:json.loads((SOURCE/'cels'/s/(s+'-measurements.json')).read_text())['cels']
        for s in ROW_SCALES}
for folder in ['assets/cels', 'audio', 'render']:
    (ROOT/folder).mkdir(parents=True, exist_ok=True)

report = []
prepared = {}

def prepare(sheet, i, support):
    key = (sheet,i,support)
    if key in prepared:
        return prepared[key]
    m = DATA[sheet][i]
    actor = 'chad' if sheet == 'chad-act' else 'rk'
    src = Image.open(m['file']).convert('RGBA')
    # Crop by the measured main character, with 3px antialias padding. The old
    # cel canvas also contains small neighbouring drawings outside this box.
    b = m['bbox']
    crop = [max(0,b[0]-3),max(0,b[1]-3),min(src.width,b[2]+3),min(src.height,b[3]+3)]
    arr = np.asarray(src.crop(crop)).copy()
    labels,n = ndimage.label(arr[:,:,3] >= 32, np.ones((3,3)))
    counts = np.bincount(labels.ravel()); counts[0] = 0
    main = labels == int(counts.argmax())
    # Preserve the antialiased fringe; discard detached exterior alpha specks.
    allowed = ndimage.binary_dilation(main, iterations=2)
    removed = int(np.count_nonzero((arr[:,:,3]>0) & ~allowed))
    arr[~allowed,3] = 0
    cel = Image.fromarray(arr)
    base = 1.30 if actor == 'chad' else 2.30
    calibration = ROW_SCALES[sheet][i//4]/base
    # Same calibration for a whole source row; no pose-by-pose height matching.
    size = [round(cel.width*calibration),round(cel.height*calibration)]
    cel = cel.resize(size,Image.Resampling.LANCZOS)
    contacts = m.get('lowest_band_contacts') or [f['contact'] for f in m['feet']]
    xs = sorted(p[0] for p in contacts)
    ax = max(xs) if support=='right' else min(xs) if support=='left' else sum(xs)/len(xs)
    if sheet=='rk-brake' and i in [6,7]:
        ax = {6:269,7:253}[i]
    def point(p):
        return [round((p[0]-crop[0])*calibration,4),round((p[1]-crop[1])*calibration,4)]
    anchor = point([ax,m['floor_y']])
    bbox = cel.getchannel('A').point(lambda a:255 if a>8 else 0).getbbox()
    file = f'assets/cels/{sheet}-{i:02d}-{support}.png'
    cel.save(ROOT/file)
    row = dict(file=file,anchor=anchor,subjects={actor:list(bbox)},
               marks={'support':anchor,'left_sole':point([min(xs),m['floor_y']]),
                      'right_sole':point([max(xs),m['floor_y']])})
    prepared[key] = row
    report.append(dict(source=m['file'],source_bbox=b,crop=crop,file=file,
                       row_calibration=calibration,actor_scale=ACTOR_SCALE[actor],
                       discarded_exterior_pixels=removed))
    return row

# Timings are output-frame numbers: walks, notices, brakes, recoils, settles.
# Whole drawings hold for 2–4 output frames in action and longer at the end.
RK = [
 (0,'rk-walk',0,'right'),(4,'rk-walk',1,'right'),
 (7,'rk-walk',2,'right'),(9,'rk-walk',4,'right'),
 (11,'rk-walk',3,'left'),
 (14,'rk-brake',0,'right'),(16,'rk-brake',1,'right'),
 (18,'rk-brake',2,'right'),(20,'rk-brake',4,'right'),
 (22,'rk-brake',5,'right'),(24,'rk-brake',6,'right'),
 (26,'rk-brake',7,'right'),(28,'rk-brake',8,'right'),
 (31,'rk-brake',9,'right'),(34,'rk-brake',10,'right'),
 (37,'rk-brake',11,'right'),
 (40,'rk-react',0,'right'),(43,'rk-react',1,'right'),
 (45,'rk-react',2,'right'),(47,'rk-react',3,'right'),
 (49,'rk-react',4,'right'),(51,'rk-react',5,'right'),
 (55,'rk-react',6,'right'),(58,'rk-react',7,'right'),
 (61,'rk-react',8,'right')]

# The leading shoe at the end of the first stride becomes the second support.
FIRST_SUPPORT = 370
SECOND_SUPPORT = FIRST_SUPPORT + (239-127)*ACTOR_SCALE['rk']
rk_cels=[]
for f,sheet,i,support in RK:
    row = prepare(sheet,i,support).copy();row['start']=f/FPS;rk_cels.append(row)
rk_position = [[0,FIRST_SUPPORT,FLOOR], [13/FPS,FIRST_SUPPORT,FLOOR],
               [14/FPS,SECOND_SUPPORT,FLOOR]]

# Chad stays put and gives one small eye reaction rather than continual bobbing.
CHAD = [(0,4),(43,5),(46,6),(48,7),(50,6),(52,5),(55,4)]
chad_cels=[]
for f,i in CHAD:
    row=prepare('chad-act',i,'center').copy();row['start']=f/FPS;chad_cels.append(row)

def stage():
    # Draw vector scenery at 2x and downsample once. All scenery is one fixed
    # source layer, so lines and support contacts cannot shimmer between cels.
    sc=2
    im=Image.new('RGBA',(W*sc,H*sc),'#f5f2e9')
    d=ImageDraw.Draw(im)
    def line(xy,fill,width=2):
        d.line([(round(x*sc),round(y*sc)) for x,y in xy],fill=fill,width=round(width*sc),joint='curve')
    def poly(xy,fill,outline=None,width=2):
        p=[(round(x*sc),round(y*sc)) for x,y in xy]
        d.polygon(p,fill=fill)
        if outline: d.line(p+[p[0]],fill=outline,width=round(width*sc),joint='curve')
    # Low contrast wall/window and baseboard; no unnecessary set decoration.
    d.rectangle((0,1518*sc,W*sc,H*sc),fill='#efede4')
    line([(0,1518),(1080,1518)],'#dad8ce',2)
    line([(0,1529),(1080,1529)],'#e4e1d8',1)
    line([(142,1005),(142,612),(454,612),(454,1005),(142,1005)],'#dedbd1',3)
    line([(298,614),(298,1003)],'#e0ddd3',2)
    line([(144,812),(451,812)],'#e0ddd3',2)
    line([(133,1015),(466,1015)],'#ddd9ce',3)
    line([(298,730),(310,710),(325,731),(339,723),(357,749)],'#e6e2d8',2)
    # A few restrained floor lines provide depth without competing with faces.
    line([(0,1772),(459,1529)],'#e3e0d6',1)
    line([(1080,1772),(667,1529)],'#e3e0d6',1)
    line([(0,1822),(1080,1822)],'#e5e2d9',1)
    # Fixed table behind the actors. Far legs first, then visible top thickness.
    poly([(673,1108),(687,1108),(683,1521),(670,1521)],'#dfdace','#bdb9af',2)
    poly([(779,1108),(791,1108),(801,1518),(789,1518)],'#dfdace','#bdb9af',2)
    poly([(650,1130),(663,1130),(649,1560),(636,1560)],'#dcd6ca','#b9b4a9',2.5)
    poly([(758,1130),(771,1130),(784,1560),(771,1560)],'#dcd6ca','#b9b4a9',2.5)
    poly([(626,1087),(778,1087),(810,1121),(626,1121)],'#e8e0d2','#aaa497',2.5)
    poly([(626,1121),(810,1121),(810,1133),(626,1133)],'#d9cfbf','#aaa497',2.5)
    # Small desaturated coffee ring lies flat on the table.
    d.ellipse((685*sc,1093*sc,749*sc,1107*sc),outline='#c1a28b',width=2*sc)
    im=im.resize((W,H),Image.Resampling.LANCZOS)
    # Reuse the approved prop drawing; the physical base is on the top plane.
    mug=Image.open(SOURCE/'assets/red-mug.png').convert('RGBA')
    a=np.asarray(mug).copy()
    lab,n=ndimage.label(a[:,:,3]>180,np.ones((3,3)))
    cnt=np.bincount(lab.ravel());cnt[0]=0
    keep=ndimage.binary_dilation(lab==cnt.argmax(),iterations=3)
    a[~keep,3]=0
    mug=Image.fromarray(a)
    bb=mug.getchannel('A').getbbox();mug=mug.crop(bb)
    mug=mug.resize((108,round(mug.height*108/mug.width)),Image.Resampling.LANCZOS)
    # Its bottom contour and a local shadow meet the tabletop at y1100.
    shadow=Image.new('RGBA',(W,H));sd=ImageDraw.Draw(shadow)
    sd.ellipse((665,1096,754,1106),fill=(65,43,29,45))
    im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(2)))
    im.alpha_composite(mug,(666,1100-mug.height))
    im.save(ROOT/'assets/stage.png')
    return dict(mug_base_y=1100,tabletop_plane_y=[1087,1121],mug_state='resting on tabletop',
                stage_is_fixed=True)

grounding=stage()

def make_shadow(file,width):
    im=Image.new('RGBA',(width+40,52));d=ImageDraw.Draw(im)
    d.ellipse((20,15,width+20,34),fill=(48,43,35,25))
    im.filter(ImageFilter.GaussianBlur(6)).save(ROOT/file)
make_shadow('assets/rk-shadow.png',290)
make_shadow('assets/chad-shadow.png',245)

def make_audio():
    # Quiet original foley; generated locally, not extracted from a reference.
    sr=48000;mix=np.zeros((round(DURATION*sr),2),dtype=np.float64)
    rng=np.random.default_rng(23)
    for t,amp in [(0.02,.11),(14/FPS,.12),(28/FPS,.075)]:
        n=int(.10*sr);tt=np.arange(n)/sr
        hiss=ndimage.gaussian_filter1d(rng.normal(0,1,n),1.3)
        sound=(np.sin(2*np.pi*(145*tt-240*tt*tt))*.4+hiss*.3)*np.exp(-tt*43)
        sound*=np.minimum(1,tt/.003)*amp
        off=round(t*sr)
        mix[off:off+n,0]+=sound*.9;mix[off:off+n,1]+=sound
    n=int(.16*sr);tt=np.arange(n)/sr
    cloth=ndimage.gaussian_filter1d(rng.normal(0,1,n),2)*np.sin(np.pi*tt/.16)**2*.009
    off=round(49/FPS*sr);mix[off:off+n]+=cloth[:,None]
    with wave.open(str(ROOT/'audio/original-foley.wav'),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr)
        w.writeframes((np.clip(mix,-1,1)*32767).astype('<i2').tobytes())
make_audio()

manifest = dict(size=[W,H],fps=FPS,duration=DURATION,background='#f5f2e9',
    safe_area=[60,180,960,1620],audio='audio/original-foley.wav',layers=[
      dict(id='fixed-stage',z=0,file='assets/stage.png',position=[0,0]),
      dict(id='rk-ground-shadow',z=1,file='assets/rk-shadow.png',anchor=[165,25],
           position_keys=[[0,260,1577],[.58,433,1577],[1.2,500,1577]]),
      dict(id='chad-ground-shadow',z=1,file='assets/chad-shadow.png',anchor=[142,25],position=[815,1577]),
      dict(id='rk',z=2,scale=ACTOR_SCALE['rk'],position_keys=rk_position,
           cels=rk_cels,check_alpha_bounds=True),
      dict(id='chad',z=3,scale=ACTOR_SCALE['chad'],position=[815,FLOOR],
           cels=chad_cels,check_alpha_bounds=True)
    ],contacts=[
      dict(name='first planted support',layer='rk',mark='support',world=[FIRST_SUPPORT,FLOOR],
           start=0,end=14/FPS,tolerance=1),
      dict(name='second planted support and stop',layer='rk',mark='support',
           world=[SECOND_SUPPORT,FLOOR],start=14/FPS,end=DURATION,tolerance=1),
      dict(name='Chad floor',layer='chad',mark='support',world=[815,FLOOR],tolerance=1)
    ])
(ROOT/'scene.json').write_text(json.dumps(manifest,indent=2))
(ROOT/'source-and-staging.json').write_text(json.dumps(dict(
    whole_body_cels=True,source= str(SOURCE),actor_scales=ACTOR_SCALE,preparation=report,
    grounding=grounding,final_hold_from=61/FPS,transform_limit='translation only, fixed actor scale',
    visual_review_required=True),indent=2))
print(ROOT/'scene.json')

"""Chapter 21 deck examples: every console session, whole program (or excerpt), chart and table the lecture deck shows. Nothing here
carries a result; examples_run_v1_0_0.py runs it all under the interpreter given (the uv Python 3.14.6 of the chapter 21 research environment
/home/claude/venv314_ch21_latest: Pillow 12.3.0, Matplotlib 3.11.2, NumPy 2.5.4, pyperclipimg 0.2.0; the rest is the standard library) and records the
results. A console group is one session: its rows run in order in one namespace (the deck check re-runs them per slide, one namespace per slide).
Every console row uses Pillow, Matplotlib (Agg) or the standard library, writes no file, and reads no clock and no network, so each can be typed into a
Python that has Pillow and prints the same text on any day. Rows of the first group (title) read the installed versions.

Programs: the twelve programs of the chapter's corpus (sen0414_ch21_corpus_base_v1_0_0.py), run and recorded under their own names (their lines are often
wider than a slide can show without wrapping), and the 'Cut' programs written for the deck, which do the same things in lines that fit a slide and save the
pictures the slides show. The four programs that need the book's own files (zophie.png, catlogo.png, guests.txt, resizeAndAddLogo.py) FETCH THE PUBLISHER'S ZIP
and check every file against the SHA-256 the study recorded; if the zip is missing or differs they print NOT EXECUTED, and the runner refuses to record that.
A picture a slide shows is saved by its program with keep(), named, sized and hashed in the program's own transcript; the program check runs the program
again and compares the picture with the one inside the .pptx. KIND says what a program's output depends on, so that honesty_check can require the matching
words on the slide that shows it:
  standin   the output comes from a LOCAL STAND-IN: a virtual X display (Xvfb) with the real xclip, where nobody sees the picture;
  none      the output depends on no stand-in (Pillow or Matplotlib making a file, or a pure function of the standard library)."""
__version__ = "1.0.0"
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("base21", os.path.join(HERE, "..", "sen0414_ch21_corpus_base_v1_0_0.py"))
B = importlib.util.module_from_spec(_s)
_s.loader.exec_module(B)

# the hidden lines of every Cut: imports, err(), wd(), the shipped files (checked against their SHA-256), keep() and done()
_SHIP = B.SHIPPED.replace("print('shipped files checked against their SHA-256:', ', '.join(sorted(FILESHA)))", "print('4 shipped files match their SHA-256')")
assert _SHIP != B.SHIPPED
_KEEP = r'''def sha(n): return hashlib.sha256(open(n, 'rb').read()).hexdigest()[:12]
def done(n):
    k = os.environ.get('CH21_KEEP')
    if k: shutil.copy(n, os.path.join(k, os.path.basename(n)))
    print('saved %s: %d bytes, sha256 %s' % (os.path.basename(n), os.path.getsize(n), sha(n)))
'''
_HEAD = B.HEAD + _KEEP
_HEADZ = B.HEAD + _SHIP + _KEEP

CONSOLES = {
    "title": ["import platform, importlib.metadata as m", "platform.python_version()", "m.version('pillow')", "m.version('matplotlib')"],
    "grid": ["from PIL import Image", "im = Image.new('1', (176, 176))", "im.size, im.mode", "176 * 176", "len(im.tobytes())", "im.getpixel((0, 0))",
             "im.putpixel((0, 0), 1)", "im.getpixel((0, 0))", "im.getpixel((1, 0))"],
    "box": ["from PIL import Image", "im = Image.new('RGB', (28, 27))", "im.crop((3, 1, 9, 6)).size", "(9 - 3) * (6 - 1)", "im.crop((9, 1, 3, 6))",
            "im.getpixel((28, 0))", "im.getpixel((-1, 0)) == im.getpixel((27, 0))"],
    "appb": ["from PIL import Image", "im = Image.new('RGB', (100, 100))", "im.crop((0, 50, 50, 50)).size", "im.crop((0, 50, 50, 100)).size"],
    "logo": ["compile('x = 816 – 100', 'listing', 'exec')", "type(compile('x = 816 - 100', 'listing', 'exec')).__name__", "300 / 1088 * 816", "int(300 / 1088 * 816)",
             "'UPPER.PNG'.endswith('.png')", "'UPPER.PNG'.lower().endswith('.png')"],
    "pins": ["from packaging.version import Version", "Version('3.9.2')", "Version('3.92')", "Version('3.92') == Version('3.9.2')", "Version('3.92') > Version('3.11.2')"],
    "window": ["import matplotlib as mpl; mpl.use('Agg')", "import matplotlib.pyplot as plt", "x = plt.plot([1, 2, 3])", "plt.show(); plt.show()",
               "len(plt.gca().lines), plt.get_fignums()", "plt.get_backend()"],
}

# ---- programs written for the deck (Cuts) ---------------------------------------------------------------------------------------
COLOURS_BODY = r'''names = ['red', 'green', 'lime', 'blue', 'CornflowerBlue', '#CCDDEE']
strip = Image.new('RGB', (len(names) * 60, 60))
for i, n in enumerate(names):
    print('%-15s' % n, ImageColor.getcolor(n, 'RGBA'))
    strip.paste(Image.new('RGB', (60, 60), n), (i * 60, 0))
print('Table 21-1 says Green is (0, 255, 0, 255); Pillow:',
      ImageColor.getcolor('green', 'RGBA'))
print(len(ImageColor.colormap), 'names;', err(lambda:
      ImageColor.getcolor('transparent', 'RGBA'))[0], 'for transparent')
d = wd(); strip.save('swatches.png'); done('swatches.png')
'''
COLOURS = _HEAD + COLOURS_BODY

BOXFIG_BODY = r'''im = Image.new('RGB', (28, 27), 'white')
draw = ImageDraw.Draw(im)
box = (3, 1, 9, 6)
draw.rectangle((3, 1, 8, 5), fill='orange')    # the last pixel is 8, 5
part = im.crop(box)
print('crop', box, '->', part.size, '| all orange:',
      set(part.getdata()) == {(255, 165, 0)})
print('one more column to the left is not:',
      set(im.crop((2, 1, 9, 6)).getdata()) == {(255, 165, 0)})
big = im.resize((280, 270), Image.Resampling.NEAREST)
g = ImageDraw.Draw(big)
for k in range(0, 281, 10): g.line([(k, 0), (k, 270)], fill='gray')
for k in range(0, 271, 10): g.line([(0, k), (280, k)], fill='gray')
d = wd(); big.save('boxTuple.png'); done('boxTuple.png')
'''
BOXFIG = _HEAD + BOXFIG_BODY

CROP_BODY = r'''d = wd(); shipped(d)
cat = Image.open('zophie.png')
face = cat.crop((335, 345, 565, 560))
print(cat.size, cat.mode, '->', face.size, face.mode)
print('right < left:', err(lambda: cat.crop((565, 345, 335, 560)))[1])
edge = cat.crop((700, 1000, 900, 1200))
print('past the edge:', edge.size, 'black', edge.getpixel((199, 199)))
face.save('face.png'); done('face.png')
'''
CROPFACE = _HEADZ + CROP_BODY

TILE_BODY = r'''d = wd(); shipped(d)
cat = Image.open('zophie.png'); face = cat.crop((335, 345, 565, 560))
tiled = cat.copy(); n = 0
for left in range(0, cat.width, face.width):
    for top in range(0, cat.height, face.height):
        tiled.paste(face, (left, top)); n += 1
print(n, 'pastes, the last at', (left, top))
print('paste returns', tiled.paste(face, (0, 0)))
corner = lambda im: im.getpixel((0, 0)) == face.getpixel((0, 0))
print('corner is the face: copy', corner(tiled), '| original', corner(cat))
tiled.resize((204, 272)).save('tiled.png'); done('tiled.png')
'''
TILECAT = _HEADZ + TILE_BODY

MASK_BODY = r'''d = wd(); shipped(d)
logo = Image.open('catlogo.png')
print(logo.size, logo.mode, 'corner pixel', logo.getpixel((0, 0)))
red = Image.new('RGBA', (100, 95), (200, 0, 0, 255))
masked = red.copy(); masked.paste(logo, (0, 0), logo)
plain = red.copy(); plain.paste(logo.convert('RGBA'), (0, 0))
print('masked:', masked.getpixel((0, 0)), 'plain:', plain.getpixel((0, 0)))
bg = Image.new('RGB', (1, 1), 'red')
blue = Image.new('RGBA', (1, 1), (0, 0, 255, 128))
bg.paste(blue, (0, 0), blue); print('alpha 128:', bg.getpixel((0, 0)))
both = Image.new('RGBA', (210, 95), 'white')
both.paste(masked, (0, 0)); both.paste(plain, (110, 0))
both.save('maskPair.png'); done('maskPair.png')
'''
MASKPAIR = _HEADZ + MASK_BODY

ROTATE_BODY = r'''im = Image.new('RGB', (120, 80))
im.putdata([(x * 2, y * 3, 160) for y in range(80) for x in range(120)])
r1 = im.rotate(20); r2 = im.convert('RGBA').rotate(20)
r3 = im.rotate(20, fillcolor='red'); r4 = im.rotate(20, expand=True)
for r in (r1, r2, r3): print(r.mode, r.getpixel((0, 0)))
print('rotate(20):', r1.size, '| expand=True:', r4.size)
print('rotate(90):', im.rotate(90).size, '| expand=True:',
      im.rotate(90, expand=True).size)
f = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
print('flip left-right:', f.getpixel((0, 0)) == im.getpixel((119, 0)))
print('resize floats:', err(lambda: im.resize((60.0, 40.5)))[1])
c = im.copy(); print('putpixel returns', c.putpixel((0, 0), (255, 0, 0)))
sheet = Image.new('RGB', (480, 300), '#d8d0c0')
for i, p in enumerate([im, r1, r2, r3, r4, im.rotate(90)]):
    mask = p if p.mode == 'RGBA' else None
    sheet.paste(p, ((i % 3) * 160 + 10, (i // 3) * 150 + 10), mask)
d = wd(); sheet.save('rotateSheet.png'); done('rotateSheet.png')
'''
ROTATESHEET = _HEAD + ROTATE_BODY

SAVE_BODY = r'''d = wd(); shipped(d)
cat = Image.open('zophie.png'); n = []
for q in (95, 75, 50, 30, 10):
    f = 'q%d.jpg' % q; cat.save(f, quality=q); n.append(os.path.getsize(f))
print('zophie.png:', os.path.getsize('zophie.png'), 'bytes')
print('JPEG bytes at q 95/75/50/30/10:', n)
cat.save('copy.png'); dpi = Image.open('copy.png').info.get('dpi')
print('PNG saved with no dpi: dpi =', dpi)
cat.save('c72.png', dpi=(72, 72))
back = Image.open('c72.png').info['dpi'][0]
print('dpi=(72, 72) reads back as', round(back, 3))
j = Image.open('q75.jpg').info
print('JPEG density, unit:', j.get('jfif_density'), j.get('jfif_unit'))
print('RGBA to JPEG:', *err(lambda: cat.convert('RGBA').save('x.jpg')))
face = (335, 345, 565, 560); pair = Image.new('RGB', (470, 215), 'white')
pair.paste(cat.crop(face), (0, 0))
pair.paste(Image.open('q10.jpg').crop(face), (240, 0))
pair.save('pngVsJpeg.png'); done('pngVsJpeg.png')
'''
SAVEFORMATS = _HEADZ + SAVE_BODY

LOGO_BODY = r'''d = wd(); shipped(d)
Image.new('RGB', (1200, 400), 'orange').save('panorama.png')
Image.new('RGB', (1200, 250), 'olive').save('strip.png')
Image.new('RGB', (900, 900), 'gray').save('UPPER.PNG')
r = subprocess.run([sys.executable, 'resizeAndAddLogo.py'],
                   capture_output=True, text=True)
print('exit', r.returncode, '| folder withLogo:')
for n in sorted(os.listdir('withLogo')):
    print(' ', n, Image.open('withLogo/' + n).size)
print('300 / 1088 * 816 =', 300 / 1088 * 816)
shutil.copy('withLogo/zophie.png', 'zophieLogo.png')
done('zophieLogo.png')
'''
ADDLOGO = _HEADZ + LOGO_BODY

DRAW_BODY = r'''im = Image.new('RGBA', (200, 200), 'white'); draw = ImageDraw.Draw(im)
draw.line([(0, 0), (199, 0), (199, 199), (0, 199), (0, 0)], fill='black')
draw.rectangle((20, 30, 60, 60), fill='blue')
draw.ellipse((120, 30, 160, 60), fill='red')
draw.polygon(((57, 87), (79, 62), (94, 85), (120, 90), (103, 113)),
             fill='brown')
for i in range(100, 200, 10):
    draw.line([(i, 0), (200, i - 100)], fill='green')
n = {c: k for k, c in im.getcolors(1000)}
print('blue pixels:', n[(0, 0, 255, 255)], '= 41 x 31 =', 41 * 31)
print('crop((20, 30, 60, 60)) is', im.crop((20, 30, 60, 60)).size)
print('green drawn:', (0, 128, 0, 255) in n,
      '| lime drawn:', (0, 255, 0, 255) in n)
print('reversed:', err(lambda: draw.rectangle((60, 60, 20, 30)))[1])
d = wd(); im.save('drawing.png'); done('drawing.png')
'''
DRAWINGPNG = _HEAD + DRAW_BODY

TEXT_BODY = r'''f = dejavu()
print('arial.ttf:', err(lambda: ImageFont.truetype('arial.ttf', 32)))
im = Image.new('RGBA', (240, 100), 'white'); draw = ImageDraw.Draw(im)
box = draw.textbbox((20, 20), 'Howdy', font=f)
print('textbbox', box, '-> width', box[2] - box[0],
      'height', box[3] - box[1])
draw.rectangle(box, outline='red')
draw.text((20, 20), 'Howdy', fill='purple', font=f)
print('textsize on ImageDraw:', hasattr(draw, 'textsize'),
      '| getsize on a font:', hasattr(f, 'getsize'))
w = [ImageFont.truetype('DejaVuSans.ttf', s).getlength('Howdy')
     for s in (16, 32, 64)]
print('Howdy is', [round(x) for x in w], 'px wide at 16, 32, 64')
d = wd(); im.save('howdy.png'); done('howdy.png')
'''
TEXTHOWDY = _HEAD + TEXT_BODY

SEAT_BODY = r'''d = wd(); shipped(d)
guests = open('guests.txt').read().splitlines()
f = ImageFont.truetype('DejaVuSans.ttf', 28); os.makedirs('cards')
sheet = Image.new('RGB', (len(guests) * 150, 190), '#d8d0c0'); wide = []
for i, g in enumerate(guests):
    card = Image.new('RGBA', (288, 360), 'white'); dr = ImageDraw.Draw(card)
    dr.rectangle((0, 0, 287, 359), outline='black')
    l, t, r, b = dr.textbbox((0, 0), g, font=f); wide.append(r - l)
    dr.text(((288 - (r - l)) // 2 - l, 200), g, fill='black', font=f)
    card.save('cards/%d.png' % i)
    sheet.paste(card.resize((144, 180)), (i * 150 + 3, 5))
print('name widths in px:', wide)
print(len(os.listdir('cards')), 'cards of', Image.open('cards/0.png').size)
sheet.save('seatingCards.png'); done('seatingCards.png')
'''
SEATINGCUT = _HEADZ + SEAT_BODY

TILEFOLD_BODY = r'''d = wd()
def make_tile(filename, across, down):
    tile = Image.open(filename); w, h = tile.size; n = 0
    out = Image.new('RGB', (w * across, h * down))
    for x in range(across):
        for y in range(down): out.paste(tile, (x * w, y * h)); n += 1
    return out.size, n
Image.new('RGB', (20, 50), 'tan').save('t.jpg')
print("make_tile('t.jpg', 6, 10):", make_tile('t.jpg', 6, 10),
      '(book: 120x500)')
def photo(p):
    try:
        with Image.open(p) as im: return im.width > 500 and im.height > 500
    except OSError: return False
for n, s in (('a.png', (800, 600)), ('b.png', (300, 300)),
             ('c.png', (600, 600))):
    Image.new('RGB', s).save(n)
open('notes.txt', 'w').write('x')
files = sorted(os.listdir('.'))
print('photos:', [f for f in files if photo(f)], 'of', files)
'''
TILEFOLDCUT = _HEAD + TILEFOLD_BODY

CLIP_BODY = r'''import atexit
disp = ':%d' % (110 + os.getpid() % 80)
xv = subprocess.Popen(['Xvfb', disp, '-screen', '0', '640x480x24'],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
atexit.register(lambda: (subprocess.run(['pkill', '-x', 'xclip']), xv.terminate()))
time.sleep(3)
def run(env):
    o, e = tempfile.TemporaryFile('w+'), tempfile.TemporaryFile('w+')
    subprocess.run([sys.executable, '-W', 'ignore', '-c', code], text=True,
                   stdin=subprocess.DEVNULL, stdout=o, stderr=e,
                   env=env, timeout=120)
    o.seek(0); e.seek(0)
    return o.read().strip().splitlines() + e.read().strip().splitlines()[-1:]
code = """
import pyperclipimg
from PIL import Image
a = Image.new('RGB', (40, 30), (10, 200, 30))
print('copy returns', pyperclipimg.copy(a))
b = pyperclipimg.paste()
print('paste', b.format, b.mode, b.size, list(b.getdata()) == list(a.getdata()))
"""
print('DISPLAY set:', *run(dict(os.environ, DISPLAY=disp)), sep='\n  ')
bare = {k: v for k, v in os.environ.items() if k != 'DISPLAY'}
print('no DISPLAY:', *run(bare), sep='\n  ')
'''
CLIPBOARDCUT = _HEAD + "import shutil\nassert shutil.which('Xvfb') and shutil.which('xclip'), 'NOT EXECUTED: Xvfb or xclip is missing'\n" + CLIP_BODY

PLOTS_BODY = r'''d = wd()
def fig(name, draw):
    plt.figure(figsize=(3, 2.4)); r = draw(); plt.title(name)
    plt.tight_layout(); plt.savefig(name + '.png'); plt.close('all'); return r
fig('line', lambda: plt.plot([1, 2, 3, 4], [1, 4, 9, 16]))
fig('scatter', lambda: plt.scatter([1, 2, 3, 4], [3, 1, 4, 2]))
bars = fig('bar', lambda: plt.bar(['spam', 'eggs', 'ham'], [3, 1, 2]))
pie = fig('pie', lambda: plt.pie([10, 20, 30, 40], labels=list('ABCD'),
                                 autopct='%1.0f%%'))
print('bar returns', type(bars).__name__, [b.get_height() for b in bars])
print('pie returns', type(pie).__name__, '| items:', len(tuple(pie)))
c = matplotlib.rcParams['axes.prop_cycle'].by_key()['color'][0]
print('line colour:', type(c).__name__, [round(v, 2) for v in c])
im = Image.open('line.png')
print('line.png', im.size, im.mode, 'dpi', round(im.info['dpi'][0]))
for n in ('line', 'scatter', 'bar', 'pie'): done(n + '.png')
'''
PLOTSFOUR = _HEAD + PLOTS_BODY

AGG_BODY = r'''d = wd()
def parts():
    ax = plt.gca(); return len(ax.lines), len(ax.patches)
plt.figure(figsize=(3, 2.4))
plt.plot([1, 2, 3]); plt.plot([3, 2, 1])
print('lines, bars:', parts(), plt.get_fignums())
print('show():', plt.show(), plt.get_fignums())
plt.bar(['a', 'b'], [1, 2])
print('after bar, same figure:', parts())
plt.tight_layout(); plt.savefig('accumulated.png')
plt.clf(); plt.plot([1, 2]); print('after clf():', parts())
plt.figure(); print('new figure:', plt.get_fignums()[-1], parts())
plt.close('all'); print('close("all"):', plt.get_fignums())
done('accumulated.png')
'''
AGGFIGURE = _HEAD + AGG_BODY

# ---- charts and tables (re-computed by the deck check) -----------------------------------------------------------------
CHARTS = {"jpegBytes": {
    "setup": "import io, os, zipfile, hashlib\nfrom PIL import Image\nZ = open('/home/claude/ch21_cache/ch21_materials.zip', 'rb').read()\n"
             "assert hashlib.sha256(Z).hexdigest() == 'dac627e807f69ee14913ba621a15dec1f98db739d76939555ba5360d05eba916'\n"
             "zf = zipfile.ZipFile(io.BytesIO(Z)); data = zf.read([n for n in zf.namelist() if n.endswith('/zophie.png') and '__MACOSX' not in n][0])\n"
             "im = Image.open(io.BytesIO(data)); im.load()\n"
             "def kb(**kw):\n    b = io.BytesIO(); im.save(b, **kw); return round(len(b.getvalue()) / 1024, 1)\n"
             "ROWS = [('PNG', round(len(data) / 1024, 1))] + [('JPEG %d' % q, kb(format='JPEG', quality=q)) for q in (95, 75, 50, 30, 10)]\n",
    "expr": "ROWS"}}

_PROBE = open(os.path.join(HERE, "probe_v1_0_0.py")).read() if os.path.exists(os.path.join(HERE, "probe_v1_0_0.py")) else ""
INTERPS = [("3.14.6 newest", "/home/claude/venv314_ch21_latest/bin/python"), ("3.14.6 pins", "/home/claude/venv314_ch21_pins/bin/python"),
           ("3.13.14 pins", "/home/claude/venv313_ch21_pins/bin/python"), ("3.14.6 empty", "/home/claude/venv314_ch21_bare/bin/python")]
_ROWS = [("Python", "Python"), ("Pillow", "Pillow"), ("Matplotlib", "Matplotlib"), ("filename is full path", "filename is absolute"),
         ("textsize() exists", "ImageDraw.textsize"), ("default font", "default font"), ("plt.pie() returns", "pie returns"),
         ("line colour is a", "line colour is"), ("savefig() of a line", "savefig"), ("legend()", "legend"), ("import", "import")]
TABLES = {
    "environments": {
        "setup": "import json, subprocess\nPROBE = %r\nINTERPS = %r\nres = []\nfor v, p in INTERPS:\n    r = subprocess.run([p, '-c', PROBE], capture_output=True, text=True)\n"
                 "    assert r.returncode == 0, (v, r.stderr[-300:])\n    res.append(json.loads(r.stdout))\nROWS = %r\n" % (_PROBE, INTERPS, _ROWS),
        "expr": "[['check'] + [v for v, p in INTERPS]] + [[label] + [x.get(key, '-') for x in res] for label, key in ROWS]"},
    "pillowReleases": {
        "setup": "import json, os\nR = json.load(open(os.path.join(HERE, '..', 'ch21-page', 'interpreter_record_v1_0_0.json')))['pillow releases']\n"
                 "def b(x): return 'yes' if x else 'no'\n",
        "expr": "[['Pillow'] + list(R)] + "
                "[['textsize()'] + [b(R[v]['ImageDraw.textsize'][0]) for v in R],"
                " ['getsize()'] + [b(R[v]['ImageFont.getsize'][0]) for v in R],"
                " ['FreeType default font'] + [b(R[v]['load_default class'][0] == 'FreeTypeFont') for v in R],"
                " ['size= accepted'] + [b(not str(R[v]['load_default(size=20) accepted'][0]).startswith('TypeError')) for v in R],"
                " ['filename is full path'] + [b(R[v]['Image.open(\"z.png\").filename is absolute'][0][0]) for v in R]]"},
}

PROGRAMS = {
    # the twelve programs of the corpus, recorded under their own names
    **{k: v for k, v in B.PROGRAMS.items()},
    "colorsSwatchCut_v1_0_0.py": (COLOURS, (), False),
    "boxTupleCut_v1_0_0.py": (BOXFIG, (), False),
    "cropFaceCut_v1_0_0.py": (CROPFACE, (), True),
    "tileCatCut_v1_0_0.py": (TILECAT, (), True),
    "maskPairCut_v1_0_0.py": (MASKPAIR, (), True),
    "rotateSheetCut_v1_0_0.py": (ROTATESHEET, (), False),
    "saveFormatsCut_v1_0_0.py": (SAVEFORMATS, (), True),
    "addLogoCut_v1_0_0.py": (ADDLOGO, (), True),
    "drawingPngCut_v1_0_0.py": (DRAWINGPNG, (), False),
    "textHowdyCut_v1_0_0.py": (TEXTHOWDY, (), False),
    "seatingCardsCut_v1_0_0.py": (SEATINGCUT, (), True),
    "tileFolderCut_v1_0_0.py": (TILEFOLDCUT, (), False),
    "clipboardCut_v1_0_0.py": (CLIPBOARDCUT, ("pyperclipimg",), False),
    "plotsFourCut_v1_0_0.py": (PLOTSFOUR, ("matplotlib",), False),
    "aggFigureCut_v1_0_0.py": (AGGFIGURE, ("matplotlib",), False),
}
KIND = {n: "none" for n in PROGRAMS}
STANDKEY = {}
for _n in ("clipboardOnXvfb_v1_0_0.py", "clipboardCut_v1_0_0.py"):
    KIND[_n] = "standin"; STANDKEY[_n] = ("Virtual display",)
# the pictures a slide shows: file name -> the program that makes it
IMAGES = {"swatches.png": "colorsSwatchCut_v1_0_0.py", "boxTuple.png": "boxTupleCut_v1_0_0.py", "face.png": "cropFaceCut_v1_0_0.py", "tiled.png": "tileCatCut_v1_0_0.py",
          "maskPair.png": "maskPairCut_v1_0_0.py", "rotateSheet.png": "rotateSheetCut_v1_0_0.py", "pngVsJpeg.png": "saveFormatsCut_v1_0_0.py",
          "zophieLogo.png": "addLogoCut_v1_0_0.py", "drawing.png": "drawingPngCut_v1_0_0.py", "howdy.png": "textHowdyCut_v1_0_0.py",
          "seatingCards.png": "seatingCardsCut_v1_0_0.py", "line.png": "plotsFourCut_v1_0_0.py", "scatter.png": "plotsFourCut_v1_0_0.py",
          "bar.png": "plotsFourCut_v1_0_0.py", "pie.png": "plotsFourCut_v1_0_0.py", "accumulated.png": "aggFigureCut_v1_0_0.py"}
EQUIV = {}
SUBSET = {}

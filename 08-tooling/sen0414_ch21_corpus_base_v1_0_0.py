#!/usr/bin/env python3
"""SEN0414 chapter 21 (Making Graphs and Manipulating Images, 3rd edition) - the shared base of the corpus, version 1.0.0.

Holds the chapter's whole programs as text, the single source the deck and the page's Lab tab both read, in the shape of sen0414_ch20_corpus_base_v1_0_0.py.
Each program is a complete script that exits 0 and prints what it printed on 2026-10-13 under Python 3.14.6 (uv) in the environment
/home/claude/venv314_ch21_latest (Pillow 12.3.0, Matplotlib 3.11.2, NumPy 2.5.4, pyperclipimg 0.2.0); the rest is the standard library.
Nothing is sent to any person or service. The four files of the book's online materials the programs use (zophie.png, catlogo.png, guests.txt and
resizeAndAddLogo.py) are FETCHED AT RUN TIME from the publisher's zip and checked against the SHA-256 the study recorded; if the zip cannot be reached or does
not match, the program prints "NOT EXECUTED" and the reason and stops (the files are never replaced by a copy). Programs that need no shipped file make their own pictures.
Programs that fetch the zip: cropPasteTile, tileMaker, seatingCards, addLogoProject; the program CLIPBOARD starts a virtual X display (Xvfb) of its own and the xclip program (a
LOCAL STAND-IN for a screen: it is real software, but nobody sees the picture); the others use no network. The record that reads the book's page and asks the public
services is sen0414_ch21_live_v1_0_0.py; the one that replays the chapter's listings is sen0414_ch21_thirdparty_v1_0_0.py.
"""
HEAD = r'''import io, os, sys, re, math, json, time, shutil, zipfile, hashlib, tempfile, warnings, subprocess, importlib.metadata as md
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageColor, ImageDraw, ImageFont
warnings.simplefilter('ignore')
def err(f):
    try: return ('ok', f())
    except BaseException as e: return (type(e).__name__, str(e))
def wd():
    d = tempfile.mkdtemp(); os.chdir(d); return d
def dejavu():
    return ImageFont.truetype('DejaVuSans.ttf', 32)
'''
SHIPPED = r'''ZIPSHA = '__ZIPSHA__'
FILESHA = {'zophie.png': '5c5bf02fd0c95cee5d490a6daf3f1c4ccbbcab9fdc59bd8bba9564cad1462ba1', 'catlogo.png': '107740e7ca46ce7642b6940ff1232689bc3d34eb14c026813a61cfae45385db0',
           'guests.txt': 'e6136e39f829ae7380be4969b780c72bd8022a1a97efc399f0f2002ce1fd5164', 'resizeAndAddLogo.py': '4291c7cedd9dcf37b792ee7c20485902ad746b2743f66873ccc953bf4681634a'}
def shipped(directory):
    """writes the four shipped files into directory, each checked against its SHA-256; prints NOT EXECUTED and stops (exit 0) when the zip cannot be had"""
    import urllib.request
    try:
        cache = os.environ.get('CH21_CACHE'); p = os.path.join(cache, 'ch21_materials.zip') if cache else None
        if p and os.path.exists(p): b = open(p, 'rb').read()
        else:
            rq = urllib.request.Request('https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0'})
            b = urllib.request.urlopen(rq, timeout=180).read()
    except Exception as e:
        print('NOT EXECUTED: the online materials could not be fetched (%s)' % type(e).__name__); sys.exit(0)
    if hashlib.sha256(b).hexdigest() != ZIPSHA:
        print('NOT EXECUTED: the zip differs from the one the study recorded (SHA-256 %s)' % hashlib.sha256(b).hexdigest()[:12]); sys.exit(0)
    z = zipfile.ZipFile(io.BytesIO(b)); names = [n for n in z.namelist() if '__MACOSX' not in n]
    for f, h in FILESHA.items():
        n = [x for x in names if x.endswith('/' + f)][0]; data = z.read(n)
        assert hashlib.sha256(data).hexdigest() == h, f
        open(os.path.join(directory, f), 'wb').write(data)
    print('shipped files checked against their SHA-256:', ', '.join(sorted(FILESHA)))
'''.replace('__ZIPSHA__', 'dac627e807f69ee14913ba621a15dec1f98db739d76939555ba5360d05eba916')

COLORS = HEAD + r'''# Chapter 21, "Colors and RGBA Values": names, hex strings, the table of the book, JPEG and the pixel density.
print('Pillow', md.version('pillow'))
for n in ('red', 'green', 'lime', 'blue', 'white', 'black', 'CornflowerBlue', 'cornflowerblue', '#CCDDEE', '#ccddee'):
    print(' ', n, ImageColor.getcolor(n, 'RGBA'))
print('colormap entries:', len(ImageColor.colormap), ImageColor.colormap['aliceblue'], '...', sorted(ImageColor.colormap)[-1])
print('Table 21-1 of the book lists Green as (0, 255, 0, 255); Pillow says green is', ImageColor.getcolor('green', 'RGBA'), 'and lime is', ImageColor.getcolor('lime', 'RGBA'))
print('transparent:', err(lambda: ImageColor.getcolor('transparent', 'RGBA')))
print('RGB mode of a name:', ImageColor.getcolor('green', 'RGB'), ' a short hex:', ImageColor.getcolor('#fa0', 'RGBA'))
im = Image.new('RGBA', (100, 200), 'purple'); print('new purple RGBA:', im.size, im.mode, im.getpixel((0, 0)), ' new with no colour:', Image.new('RGBA', (1, 1)).getpixel((0, 0)), Image.new('RGB', (1, 1)).getpixel((0, 0)))
d = wd(); im.save('a.png'); print('RGBA to JPEG:', err(lambda: im.save('a.jpg')))
im.convert('RGB').save('a.jpg'); print('after convert("RGB"): saved', os.path.getsize('a.jpg') > 0, ' unknown extension:', err(lambda: im.save('a.unknownext')))
png = Image.open('a.png'); print('PNG saved with no dpi has a density:', png.info.get('dpi'))
im.save('b.png', dpi=(72, 72)); print('PNG saved with dpi=(72, 72):', tuple(round(v, 3) for v in Image.open('b.png').info['dpi']), ' JPEG default:', Image.open('a.jpg').info.get('jfif_density'), Image.open('a.jpg').info.get('jfif_unit'))
'''
CROPPASTE = HEAD + SHIPPED + r'''# Chapter 21, "Cropping Images", "Pasting Images onto Other Images" and the tiling loop, on the book's zophie.png.
d = wd(); shipped(d)
cat = Image.open('zophie.png'); print('zophie.png:', cat.size, cat.format, cat.mode, ' width, height =', cat.width, cat.height)
print('filename as Pillow %s reports it:' % md.version('pillow'), cat.filename)
face = cat.crop((335, 345, 565, 560)); print('crop((335, 345, 565, 560)) ->', face.size, ' (right - left, bottom - top) =', (565 - 335, 560 - 345))
print('crop with right < left:', err(lambda: cat.crop((565, 345, 335, 560))))
print('crop that runs past the edge:', cat.crop((700, 1000, 900, 1200)).size, cat.crop((700, 1000, 900, 1200)).getpixel((199, 199)))
copy = cat.copy(); r = copy.paste(face, (0, 0)); print('paste returns', r, ' the corner of the copy equals the face corner:', copy.getpixel((0, 0)) == face.getpixel((0, 0)), ' the original is unchanged:', Image.open('zophie.png').getpixel((0, 0)) == cat.getpixel((0, 0)))
copy = cat.copy(); w, h = face.size; n = 0
for left in range(0, cat.width, w):
    for top in range(0, cat.height, h):
        copy.paste(face, (left, top)); n += 1
print('tiling loop: step %dx%d over %dx%d pastes' % (w, h, cat.width, cat.height), n, 'tiles')
big = cat.copy().resize((cat.width * 2, cat.height * 2)); print('resize((1632, 2176)):', big.size)
print('resize with floats:', err(lambda: cat.resize((408.0, 544.5))))
half = cat.resize((cat.width // 2, cat.height // 2)); print('resize to half:', half.size, ' int(300/1088*816) =', int(300 / 1088 * 816), ' the float is', 300 / 1088 * 816)
print('resize to a wrong shape squashes it:', cat.resize((cat.width, 100)).size)
j = cat.copy(); j.save('zophie.jpg'); print('JPEG bytes vs PNG bytes:', os.path.getsize('zophie.jpg'), os.path.getsize('zophie.png'))
from PIL import ImageChops
a = Image.open('zophie.png'); b = Image.open('zophie.jpg'); print('JPEG is lossy: largest difference in each channel after the round trip:', [hi for lo, hi in ImageChops.difference(a, b).getextrema()], ' mode', b.mode)
'''
ROTATE = HEAD + r'''# Chapter 21, "Rotating and Flipping Images" and "Changing Individual Pixels": the fill colour, expand, FLIP_LEFT_RIGHT, putpixel.
def grad():
    im = Image.new('RGB', (60, 40))
    for x in range(60):
        for y in range(40): im.putpixel((x, y), (x * 4 % 256, y * 6 % 256, (x + y) * 3 % 256))
    return im
g = grad(); print('gradient', g.size, g.mode, ' pixel (3, 2):', g.getpixel((3, 2)))
for deg in (90, 180, 270, 6):
    print('rotate(%d): %s, with expand=True: %s' % (deg, g.rotate(deg).size, g.rotate(deg, expand=True).size))
print('rotate(6) corner on an RGB image:', g.rotate(6).getpixel((0, 0)), ' on an RGBA image:', g.convert('RGBA').rotate(6).getpixel((0, 0)), ' with fillcolor:', g.rotate(6, fillcolor='red').getpixel((0, 0)))
print('rotate(90) on a 60x40 image keeps 60x40 and loses the corners, corner pixel', g.rotate(90).getpixel((0, 0)), '; transpose(ROTATE_90) turns the top-right pixel into the top-left one (counter-clockwise):', g.transpose(Image.Transpose.ROTATE_90).getpixel((0, 0)) == g.getpixel((59, 0)))
print('flip with Image.FLIP_LEFT_RIGHT:', g.transpose(Image.FLIP_LEFT_RIGHT).getpixel((0, 0)) == g.getpixel((59, 0)), ' with Image.Transpose.FLIP_LEFT_RIGHT:', g.transpose(Image.Transpose.FLIP_LEFT_RIGHT).getpixel((0, 0)) == g.getpixel((59, 0)))
print('FLIP_TOP_BOTTOM:', g.transpose(Image.Transpose.FLIP_TOP_BOTTOM).getpixel((0, 0)) == g.getpixel((0, 39)), ' ROTATE_90 size:', g.transpose(Image.Transpose.ROTATE_90).size)
c = g.copy(); print('putpixel returns', c.putpixel((0, 0), (255, 0, 0)), ' now', c.getpixel((0, 0)))
print('putpixel with a colour name:', err(lambda: c.putpixel((1, 0), 'red')), ' with ImageColor:', c.putpixel((1, 0), ImageColor.getcolor('red', 'RGB')), c.getpixel((1, 0)))
print('getpixel((60, 0)):', err(lambda: g.getpixel((60, 0))), ' getpixel((-1, 0)):', g.getpixel((-1, 0)), '== getpixel((59, 0)):', g.getpixel((-1, 0)) == g.getpixel((59, 0)))
print('putpixel on a tuple of the wrong length:', err(lambda: c.putpixel((2, 0), (1, 2))))
'''
DRAWING = HEAD + r'''# Chapter 21, "A Drawing Example": the book's 200x200 image (its listing as printed, with a white background), with the end points counted.
d = wd(); im = Image.new('RGBA', (200, 200), 'white'); draw = ImageDraw.Draw(im)
draw.line([(0, 0), (199, 0), (199, 199), (0, 199), (0, 0)], fill='black')
draw.rectangle((20, 30, 60, 60), fill='blue'); draw.ellipse((120, 30, 160, 60), fill='red')
draw.polygon(((57, 87), (79, 62), (94, 85), (120, 90), (103, 113)), fill='brown')
P0 = list(im.getdata()); count0 = lambda c: sum(1 for p in P0 if p == c)
print('blue rectangle (20, 30, 60, 60) paints', count0((0, 0, 255, 255)), 'pixels; 41 x 31 =', 41 * 31, ' (the ends are included, unlike crop)')
for i in range(100, 200, 10): draw.line([(i, 0), (200, i - 100)], fill='green')
im.save('drawing.png')
P = list(im.getdata()); count = lambda c: sum(1 for p in P if p == c)
print('crop((20, 30, 60, 60)) is', im.crop((20, 30, 60, 60)).size)
print('red ellipse pixels:', count((255, 0, 0, 255)) > 600, ' brown polygon pixels > 300:', count((165, 42, 42, 255)) > 300)
print('green (the colour name) as drawn:', ImageColor.getcolor('green', 'RGBA'), ' pixels of it:', count((0, 128, 0, 255)) > 100)
print('pixel (100, 0) after the green lines:', im.getpixel((100, 0)), ' pixel (50, 45) inside the rectangle:', im.getpixel((50, 45)), ' corner (0, 0):', im.getpixel((0, 0)))
print('a rectangle with the corners reversed:', err(lambda: draw.rectangle((60, 60, 20, 30), fill='blue')))
d2 = ImageDraw.Draw(Image.new('RGB', (50, 50), 'blue')); print('rectangle with no fill and no outline paints an outline in white:', (lambda i: (ImageDraw.Draw(i).rectangle((5, 5, 20, 20)), i.getpixel((5, 5)), i.getpixel((10, 10))))(Image.new('RGB', (50, 50), 'blue')))
print('ellipse((0, 0, 99, 99)) bounding box in a 100x100 image touches all four edges:', (lambda i: (ImageDraw.Draw(i).ellipse((0, 0, 99, 99), fill='white'), [i.getpixel((0, 49)), i.getpixel((99, 49)), i.getpixel((49, 0)), i.getpixel((49, 99))])[1])(Image.new('RGB', (100, 100))))
chk = Image.open('drawing.png'); print('saved and reloaded:', chk.size, chk.mode, chk.getpixel((50, 45)))
'''
TEXT = HEAD + r'''# Chapter 21, "Drawing Text": the fonts and the size of the text. 'arial.ttf' is not on this machine; DejaVu Sans is.
print('default font:', type(ImageFont.load_default()).__name__, ' size 10:', ImageFont.load_default().size)
print('arial.ttf:', err(lambda: ImageFont.truetype('arial.ttf', 32)))
f = dejavu(); print('DejaVuSans.ttf, 32:', type(f).__name__, f.size, f.getname())
im = Image.new('RGBA', (200, 200), 'white'); draw = ImageDraw.Draw(im)
box = draw.textbbox((100, 150), 'Howdy', font=f); print('textbbox((100, 150), "Howdy") =', box, ' width', box[2] - box[0], ' height', box[3] - box[1], ' the right edge is outside the 200-pixel image:', box[2] > 200)
print('textlength("Howdy") =', round(draw.textlength('Howdy', font=f), 2), ' font.getbbox("Howdy") =', f.getbbox('Howdy'), ' getlength:', round(f.getlength('Howdy'), 2))
draw.text((20, 150), 'Hello', fill='purple', font=f); print('textsize on ImageDraw:', hasattr(draw, 'textsize'), ' getsize on a font:', hasattr(f, 'getsize'))
print('text(...) returns', draw.text((20, 20), 'Hi', fill='black', font=ImageFont.load_default(size=20)))
inked = [(x, y) for x in range(200) for y in range(200) if im.getpixel((x, y))[:3] == (128, 0, 128)]; print('purple pixels exist:', len(inked) > 100, ' leftmost x >= 20:', min(p[0] for p in inked) >= 20)
big = ImageFont.truetype('DejaVuSans.ttf', 64); small = ImageFont.truetype('DejaVuSans.ttf', 16); print('width of "Hello" at 16, 32, 64 points:', [round(x.getlength('Hello')) for x in (small, f, big)])
print('the book says the size is in points; Pillow reads the size argument as pixels, so the same number gives the same height on every screen:', f.size)
d = wd(); im.save('text.png'); print('saved text.png', Image.open('text.png').size)
'''
TILEMAKER = HEAD + SHIPPED + r"""# Chapter 21, "Practice Project: Tile Maker": make_tile(filename, across, down) as the book specifies it, and the same loop with the shipped catlogo.png (mode LA).
d = wd(); shipped(d)
Image.new('RGB', (20, 50), 'tan').save('zophie_the_cat.jpg')
def make_tile(filename, across, down):
    tile = Image.open(filename); w, h = tile.size; out = Image.new('RGB', (w * across, h * down)); n = 0
    for x in range(across):
        for y in range(down):
            out.paste(tile, (x * w, y * h)); n += 1
    return out, n
t, n = make_tile('zophie_the_cat.jpg', 6, 10); print("make_tile('zophie_the_cat.jpg', 6, 10) on a 20x50 image:", t.size, n, 'tiles  (the book: 120x500, 60 tiles)')
logo = Image.open('catlogo.png'); print('catlogo.png:', logo.size, logo.mode, ' transparent corner pixel:', logo.getpixel((0, 0)))
out = Image.new('RGBA', (400, 300), 'white'); pastes = 0
for left in range(0, 400, logo.width):
    for top in range(0, 300, logo.height): out.paste(logo, (left, top), logo.convert('RGBA')); pastes += 1
print('tiling the logo over 400x300 with its own mask:', out.size, pastes, 'pastes; the transparent corner stays', out.getpixel((0, 0)), ' an opaque logo pixel is copied:', out.getpixel((50, 47)) != (255, 255, 255, 255))
nomask = Image.new('RGBA', (100, 95), 'white'); nomask.paste(logo.convert('RGBA'), (0, 0)); print('paste without the mask copies the transparent pixel as it is, alpha included:', nomask.getpixel((0, 0)))
rgb = Image.new('RGB', (200, 200), 'white'); rgb.paste(logo, (0, 0)); print('paste of an LA logo onto an RGB image with no mask runs:', rgb.getpixel((0, 0)), rgb.getpixel((50, 47)))
rgb2 = Image.new('RGB', (200, 200), 'white'); rgb2.paste(logo, (0, 0), logo); print('with itself as the mask:', rgb2.getpixel((0, 0)), rgb2.getpixel((50, 47)))
random_ok = [Image.open('zophie_the_cat.jpg').transpose(m).size for m in (Image.Transpose.FLIP_LEFT_RIGHT, Image.Transpose.ROTATE_90)]; print('the bonus: flipping keeps (20, 50), turning by 90 gives', random_ok)
"""
FOLDERS = HEAD + r'''# Chapter 21, "Practice Project: Photo Folder Finder": walks a tree and reports the folders where more than half the files are photos (both sides over 500 pixels).
d = wd()
def mk(path, size):
    os.makedirs(os.path.dirname(path), exist_ok=True); Image.new('RGB', size, 'gray').save(path)
mk('a/p1.png', (800, 600)); mk('a/p2.jpg', (900, 700)); open('a/notes.txt', 'w').write('x')
mk('b/small.png', (300, 300)); mk('b/wide.png', (2000, 400)); mk('b/c/q1.png', (600, 600)); mk('b/c/q2.JPG', (700, 800)); mk('b/c/q3.jpg', (650, 900)); open('b/c/readme.txt', 'w').write('x')
open('d/x.txt', 'w').write('x') if os.makedirs('d', exist_ok=True) is None else None
def photo(path):
    ext = os.path.splitext(path)[1].lower()
    if ext not in ('.png', '.jpg'): return False
    try:
        with Image.open(path) as im: return im.width > 500 and im.height > 500
    except OSError: return False
found = []
for folder, subs, files in os.walk('.'):
    subs.sort(); files.sort()
    if not files: continue
    n = sum(photo(os.path.join(folder, f)) for f in files)
    print('%-6s files %d, photos %d' % (folder, len(files), n))
    if n > len(files) / 2: found.append(folder)
print('photo folders:', sorted(found))
print('os.walk visits folders in the order the file system returns them (here subs.sort() fixes it) so the lines are the same on every machine')
'''
SEATING = HEAD + SHIPPED + r'''# Chapter 21, "Practice Project: Seating Cards": one 288x360 card for each name of guests.txt (a 4x5 inch card at 72 pixels per inch).
d = wd(); shipped(d)
guests = open('guests.txt').read().splitlines(); print('guests:', len(guests), guests)
f = ImageFont.truetype('DejaVuSans.ttf', 28); os.makedirs('cards')
for i, g in enumerate(guests):
    card = Image.new('RGBA', (288, 360), 'white'); dr = ImageDraw.Draw(card)
    dr.rectangle((0, 0, 287, 359), outline='black'); dr.ellipse((94, 20, 194, 120), fill='pink')
    l, t, r, b = dr.textbbox((0, 0), g, font=f); x = (288 - (r - l)) // 2 - l; dr.text((x, 200), g, fill='black', font=f); card.save('cards/%d.png' % i)
    print('card %d %-13s width of the name %3d fits: %s' % (i, g, r - l, r - l <= 288))
print('files:', sorted(os.listdir('cards')), ' sizes:', {Image.open('cards/' + n).size for n in os.listdir('cards')})
card = Image.open('cards/0.png'); print('black pixels on card 0:', sum(1 for p in card.getdata() if p[:3] == (0, 0, 0)) > 200, ' the border pixel (0, 0):', card.getpixel((0, 0)))
print('the book mentions a public domain flower image; the zip has no flower file:', [n for n in os.listdir('.') if 'flower' in n.lower()])
'''
LOGOPROGRAM = HEAD + SHIPPED + r'''# Chapter 21, "Project 16: Add a Logo": the shipped resizeAndAddLogo.py, run on the book's zophie.png and on three pictures made here.
d = wd(); shipped(d)
Image.new('RGB', (1200, 400), 'orange').save('panorama.png'); Image.new('RGB', (1200, 250), 'olive').save('strip.png'); Image.new('RGB', (500, 700), 'teal').save('tall.jpg'); Image.new('RGB', (900, 900), 'gray').save('UPPER.PNG'); open('notes.txt', 'w').write('x')
r = subprocess.run([sys.executable, 'resizeAndAddLogo.py'], capture_output=True, text=True); print('exit', r.returncode); print('\n'.join(sorted(r.stdout.splitlines())))
out = sorted(os.listdir('withLogo')); print('withLogo:', out)
for n in out: print(' ', n, Image.open('withLogo/' + n).size)
z = Image.open('withLogo/zophie.png'); logo = Image.open('catlogo.png'); print('zophie 816x1088 -> 225x300:', z.size == (225, 300), ' int((300 / 1088) * 816) =', int((300 / 1088) * 816))
print('the logo lands at', (z.width - logo.width, z.height - logo.height), 'the lower-right corner; pixel under the logo changed:', z.getpixel((z.width - 50, z.height - 47)) != Image.open('zophie.png').resize((225, 300)).getpixel((z.width - 50, z.height - 47)))
print('panorama 1200x400 (both sides over 300) ->', Image.open('withLogo/panorama.png').size, '; strip 1200x250 (one side not over 300) ->', Image.open('withLogo/strip.png').size, '(the program leaves the size when either side is 300 or less)')
print('UPPER.PNG skipped (the test is endswith(".png") on a case-sensitive string):', 'UPPER.PNG' not in out)
print('the shipped file holds an en dash (U+2013):', '–' in open('resizeAndAddLogo.py', encoding='utf-8').read(), ' (the printed listing of the page does)')
'''
MPLOBJ = HEAD + r'''# Chapter 21, "Making Graphs with Matplotlib": what pyplot returns, in Matplotlib %s.
print('Matplotlib', md.version('matplotlib'), 'backend', matplotlib.get_backend(), ' default figure', [float(v) for v in plt.figure().get_size_inches()], 'dpi', plt.gcf().dpi); plt.close('all')
ln, = plt.plot([1, 2, 3, 4], [1, 4, 9, 16]); print('plot returns a list of', type(ln).__name__, ' colour', ln.get_color(), ' second line colour', plt.plot([1, 2, 3, 4], [2, 3, 5, 7])[0].get_color())
print('xlabel/ylabel/title return:', plt.xlabel('X'), plt.ylabel('Y'), plt.title('T').get_text(), ' legend ->', type(plt.legend(['a', 'b'])).__name__)
plt.close('all'); bars = plt.bar(['spam', 'eggs', 'ham'], [3, 1, 2]); print('bar: container', type(bars).__name__, 'heights', [h.get_height() for h in bars], [type(h.get_height()).__name__ for h in bars], ' x labels', [t.get_text() for t in plt.gca().get_xticklabels()])
plt.close('all'); res = plt.pie([10, 20, 30, 40], labels=['A', 'B', 'C', 'D'], autopct='%1.1f%%'); print('pie returns', type(res).__name__, ' unpacks to', len(tuple(res)), ' autopct texts', [t.get_text() for t in res[2]], ' first wedge', res[0][0].theta1 - res[0][0].theta2 if False else (res[0][0].theta1, res[0][0].theta2))
print('pie without autopct unpacks to', len(tuple(plt.pie([1, 2, 3]))), ' (3.9.2 and earlier return a tuple; 3.11 returns a PieContainer)'); print('axes aspect after pie:', plt.gca().get_aspect())
plt.close('all'); plt.plot([1, 2, 3], label='a'); plt.xlabel('x'); b = io.BytesIO(); plt.savefig(b, format='png'); im = Image.open(io.BytesIO(b.getvalue())); print('savefig to PNG:', im.size, im.mode, ' dpi', tuple(round(v, 1) for v in im.info['dpi']))
b2 = io.BytesIO(); plt.savefig(b2, format='png', dpi=200); print('savefig(dpi=200):', Image.open(io.BytesIO(b2.getvalue())).size)
print('scatter returns', type(plt.scatter([1, 2], [3, 4])).__name__, ' hist returns', len(plt.hist([1, 2, 2, 3], bins=3)), 'items')
'''
AGGTK = HEAD + r'''# Chapter 21, "plt.show()" and what a figure keeps: the Agg backend has no window, so show() returns at once and the figure stays.
d = wd(); print('backend', matplotlib.get_backend(), '(no DISPLAY in this program: %s)' % ('DISPLAY' in os.environ))
def parts():
    ax = plt.gca(); return (len(ax.lines), len(ax.collections), len(ax.patches))
plt.plot([1, 2, 3], [1, 2, 3]); plt.plot([1, 2, 3], [3, 2, 1]); print('figures', plt.get_fignums(), ' lines, collections, patches:', parts()); plt.savefig('line.png')
print('show() returns', plt.show(), ' figures after show:', plt.get_fignums(), '(a window backend would close and forget the figure)')
plt.scatter([1, 2, 3], [1, 2, 3]); plt.savefig('scatter.png'); print('after scatter:', parts())
plt.bar(['a', 'b'], [1, 2]); plt.savefig('bar.png'); print('after bar:', parts(), '- the book\'s later examples draw on the same figure unless plt.figure() or plt.clf() is called')
plt.clf(); plt.plot([1, 2]); print('after plt.clf() and one plot:', parts()); plt.figure(); print('plt.figure() starts a new one, now figures', plt.get_fignums(), 'and parts', parts())
plt.close('all'); print('after close("all"):', plt.get_fignums())
cols = lambda n: len(set(Image.open(n).convert('RGB').getdata())); print('colours in line.png, scatter.png, bar.png:', cols('line.png'), cols('scatter.png'), cols('bar.png'))
plt.close('all'); plt.plot([1, 2, 3]); plt.savefig('first.png'); plt.show(); plt.savefig('second.png'); print('with Agg the second savefig after show() still holds the line:', cols('first.png') == cols('second.png'))
'''
CLIPBOARD = HEAD + r'''# Chapter 21, "Copying and Pasting Images" with pyperclipimg 0.2.0 and the real xclip, on a virtual X display (Xvfb) started here.
import shutil, subprocess
if not (shutil.which('Xvfb') and shutil.which('xclip')): print('NOT EXECUTED: Xvfb or xclip is not on the PATH'); sys.exit(0)
disp = ':%d' % (110 + os.getpid() % 80); xv = subprocess.Popen(['Xvfb', disp, '-screen', '0', '640x480x24'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(3)
code = r"""
import pyperclipimg, json
from PIL import Image
a = Image.new('RGB', (40, 30), (10, 200, 30)); a.putpixel((3, 4), (255, 0, 1))
r = pyperclipimg.copy(a); b = pyperclipimg.paste()
print(json.dumps([repr(r), type(b).__name__, b.format, b.mode, list(b.size), list(b.getdata()) == list(a.getdata())]))
"""
def child(c, env_extra, drop=()):
    e = dict(os.environ); e.update(env_extra)
    for k in drop: e.pop(k, None)
    fo = tempfile.TemporaryFile('w+'); fe = tempfile.TemporaryFile('w+')
    r = subprocess.run([sys.executable, '-W', 'ignore', '-c', c], stdin=subprocess.DEVNULL, stdout=fo, stderr=fe, text=True, env=e, timeout=120); fo.seek(0); fe.seek(0)
    return r.returncode, fo.read().strip(), (fe.read().strip().splitlines() or [''])[-1][:90]
try:
    print('with a display (copy returns, paste type, format, mode, size, same pixels):', child(code, {'DISPLAY': disp})[1])
    rc, out, e = child("import pyperclipimg\nfrom PIL import Image\nprint(repr(pyperclipimg.copy(Image.new('RGB', (4, 4)))))\ntry: pyperclipimg.paste()\nexcept Exception as x: print(type(x).__name__)", {}, ('DISPLAY',)); print('with no DISPLAY:', out.replace('\n', ' then paste raises '))
    print('pyperclipimg 0.2.0 is on the PATH of this program:', md.version('pyperclipimg'))
finally:
    subprocess.run(['pkill', '-x', 'xclip']); xv.terminate(); xv.wait()
'''
PROGRAMS = {
    'colorsAndModes_v1_0_0.py': (COLORS, (), False),
    'cropPasteTile_v1_0_0.py': (CROPPASTE, (), True),
    'rotateFlipPixels_v1_0_0.py': (ROTATE, (), False),
    'drawingPixelCounts_v1_0_0.py': (DRAWING, (), False),
    'textAndFonts_v1_0_0.py': (TEXT, (), False),
    'tileMaker_v1_0_0.py': (TILEMAKER, (), True),
    'photoFolderFinder_v1_0_0.py': (FOLDERS, (), False),
    'seatingCards_v1_0_0.py': (SEATING, (), True),
    'addLogoProject_v1_0_0.py': (LOGOPROGRAM, (), True),
    'pyplotReturns_v1_0_0.py': (MPLOBJ, ('matplotlib',), False),
    'aggFigureLifecycle_v1_0_0.py': (AGGTK, ('matplotlib',), False),
    'clipboardOnXvfb_v1_0_0.py': (CLIPBOARD, ('pyperclipimg',), False),
}
STAND_IN = {'clipboardOnXvfb_v1_0_0.py': 'a virtual display (Xvfb) with the real xclip; nobody sees the picture'}
FIXTURE_BASED = ['cropPasteTile_v1_0_0.py', 'tileMaker_v1_0_0.py', 'seatingCards_v1_0_0.py', 'addLogoProject_v1_0_0.py']

if __name__ == "__main__":
    # Usage: /home/claude/venv314_ch21_latest/bin/python sen0414_ch21_corpus_base_v1_0_0.py   (exits 1 if a program does not exit 0)
    import os, subprocess, sys
    bad = 0
    for name, (code, needs, live) in PROGRAMS.items():
        r = subprocess.run([sys.executable, "-W", "ignore", "-c", code], capture_output=True, text=True, timeout=400, stdin=subprocess.DEVNULL)
        bad += r.returncode != 0
        print("=== %s (exit %d)%s%s" % (name, r.returncode, " FETCHES THE ZIP" if live else "", " [local stand-in: %s]" % STAND_IN[name] if name in STAND_IN else "")); print(r.stdout.rstrip()[:3500]); print(r.stderr[-500:].rstrip())
    print("%d programs, %d did not exit 0" % (len(PROGRAMS), bad)); sys.exit(1 if bad else 0)

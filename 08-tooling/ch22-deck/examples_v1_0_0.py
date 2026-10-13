"""Chapter 22 deck examples: every console session, whole program (or excerpt), chart and table the lecture deck shows. Nothing here
carries a result; examples_run_v1_0_0.py runs it all under the interpreter given (the uv Python 3.14.6 of the chapter 22 research environment
/home/claude/venv314_ch22_latest: pytesseract 0.3.13, Pillow 12.3.0, NumPy 2.5.4, opencv-python-headless 5.0.0.93, PyAutoGUI 0.9.54; the rest is the
standard library) with the REAL Tesseract 5.3.4 of Ubuntu 24.04 (apt, English data = tessdata_fast) on the PATH, and records the results. A console group is
one session: its rows run in order in one namespace (the deck check re-runs them per slide, one namespace per slide).
Every console row uses pytesseract, Pillow or the standard library, writes no file, and reads no clock and no network.

Programs: the twelve programs of the chapter's corpus (sen0414_ch22_corpus_base_v1_0_0.py), run and recorded under their own names (their lines are often wider
than a slide can show without wrapping), and the 'Cut' programs written for the deck, which do the same things in lines that fit a slide and save the pictures the
slides show. The programs that need the book's own files (ocr-example.png, frankenstein.png, frankenstein_jpn.png) FETCH THE PUBLISHER'S ZIP (cached under
CH22_CACHE) and check every file against the SHA-256 the study recorded; if the zip is missing or differs they print NOT EXECUTED and stop, and the runner refuses to
record that. A picture a slide shows is saved by its program with done(), named, sized and hashed in the program's own transcript; the program check runs the
program again and compares the picture with the one inside the .pptx. KIND says what a program's output depends on, so that honesty_check can require the matching
words on the slide that shows it:
  standin   the output comes from a LOCAL STAND-IN: a virtual X display (Xvfb) on which the real ImageMagick display shows a page; nobody sees the screen;
  none      the output depends on no stand-in (Tesseract, NAPS2, poppler or ocrmypdf working on a file, or a pure function of the standard library).
Accuracy numbers are MEASURED single runs with the Tesseract version named on the slide (5.3.4 unless a slide says otherwise)."""
__version__ = "1.0.0"
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("base22", os.path.join(HERE, "..", "sen0414_ch22_corpus_base_v1_0_0.py"))
B = importlib.util.module_from_spec(_s)
_s.loader.exec_module(B)

# the hidden lines of every Cut: imports, helpers (err, wd, render, cer, ocr), the shipped files (checked against their SHA-256), the printed text of the page and done()
_SHIP = B.SHIPPED.replace("print('shipped files checked against their SHA-256:', ', '.join(sorted(FILESHA)))", "print('4 shipped files match their SHA-256')")
assert _SHIP != B.SHIPPED
_KEEP = r'''TRUTH = ("THE MODERN PROMETHEUS. 43 CHAPTER V. IT was on a dreary night of November, that I beheld the accomplishment of my toils. With an anxiety that almost amounted to agony, "
         "I collected the instruments of life around me, that I might infuse a spark of being into the lifeless thing that lay at my feet. It was already one in the morning ; "
         "the rain pattered dismally against the panes, and my candle was nearly burnt out, when, by the glimmer of the half-extinguished light, I saw the dull yellow eye of the creature open ; "
         "it breathed hard, and a convulsive motion agitated its limbs.")
def sha(n): return hashlib.sha256(open(n, 'rb').read()).hexdigest()[:12]
def done(n):
    k = os.environ.get('CH22_KEEP')
    if k: shutil.copy(n, os.path.join(k, os.path.basename(n)))
    print('saved %s: %d bytes, sha256 %s' % (os.path.basename(n), os.path.getsize(n), sha(n)))
'''
_HEAD = B.HEAD + _KEEP
_HEADZ = B.HEAD + _SHIP + _KEEP

CONSOLES = {
    "title": ["import platform, importlib.metadata as m", "platform.python_version()", "m.version('pytesseract')", "m.version('pillow')",
              "import pytesseract as t", "str(t.get_tesseract_version())"],
    "pins": ["import pkgutil, sys", "sys.version_info[:2]", "hasattr(pkgutil, 'find_loader')", "import inspect, pytesseract",
             "'find_loader' in inspect.getsource(pytesseract)", "from packaging.version import Version", "Version('0.3.10') < Version('0.3.13')"],
    "lang": ["import pytesseract as t", "g = t.get_languages(config='')", "g == sorted(g)", "'osd' in g, 'eng' in g, 'xyz' in g"],
}

# ---- programs written for the deck (Cuts) ---------------------------------------------------------------------------------------
FOURLINES_BODY = r'''d = wd(); shipped(d)
img = Image.open('ocr-example.png')
print(img.size, img.mode)
text = tess.image_to_string(img)
lines = text.split('\n')
print(type(text).__name__, len(text), 'characters,', text.count('\n'), 'line breaks')
for line in lines[:4]:
    print('|', line)
print('ends with', repr(text[-3:]), '| empty lines:', lines.count('') - 1)
img.crop((90, 0, 939, 200)).convert('RGB').save('ocrTop.png')
done('ocrTop.png')
'''
FOURLINES = _HEADZ + FOURLINES_BODY

FRANK_BODY = r'''d = wd(); shipped(d)
img = Image.open('frankenstein.png')
text = tess.image_to_string(img)
lines = text.split('\n')
print(img.size, img.mode, '->', len(text), 'characters,', len(lines), 'pieces')
for i in (0, 2, 4):
    print(i, repr(lines[i]))
print('the book prints Iv; the first word here is', lines[4].split()[0])
w, t = norm(text).split(' '), TRUTH.split(' ')
sm = difflib.SequenceMatcher(None, t, w)
print('words that differ:', [(t[a:b], w[c:e]) for g, a, b, c, e in sm.get_opcodes() if g != 'equal'])
print('character error rate against the printed page:', cer(TRUTH, text))
img.crop((90, 272, 1000, 316)).convert('RGB').save('frankLine.png')
done('frankLine.png')
'''
FRANKCUT = _HEADZ + FRANK_BODY

ERRORS_BODY = r'''d = wd()
F = ImageFont.truetype(FONTS['sans'], 32)
im = Image.new('L', (700, 60), 255)
ImageDraw.Draw(im).text((10, 10), 'Tesseract reads', font=F, fill=0)
print(repr(ocr(im)))
e = err(lambda: ocr(im, lang='xyz'))
print('lang xyz:', e[0], 'xyz.traineddata' in e[1])
print('timeout:', err(lambda: ocr(im, timeout=0.001)))
print('bytes:', err(lambda: ocr(b'x')))
tess.pytesseract.tesseract_cmd = '/nowhere/tesseract'
print('no program:', err(lambda: ocr(im))[0])
im.save('readsLine.png'); done('readsLine.png')
'''
ERRORSCUT = _HEAD + ERRORS_BODY

WORDS_BODY = r'''d = wd(); shipped(d)
img = Image.open('frankenstein.png')
dd = tess.image_to_data(img, output_type=tess.Output.DICT)
t, c, lv = dd['text'], dd['conf'], dd['level']
L, T, W, H = (dd[k] for k in ('left', 'top', 'width', 'height'))
ix = [i for i in range(len(t)) if t[i].strip()]
print(len(t), 'rows,', len(ix), 'words, levels', sorted(set(lv)))
print('conf above the word level:', sorted({c[i] for i in range(len(t)) if lv[i] < 5}))
for i in ix[6:9]:
    print(t[i], c[i], L[i], T[i], W[i], H[i])
low = [(t[i], c[i]) for i in ix if c[i] < 90]
print('mean', round(sum(c[i] for i in ix) / len(ix), 2), '| below 90:', low)
out = img.convert('RGB'); g = ImageDraw.Draw(out)
for i in ix:
    g.rectangle((L[i], T[i], L[i] + W[i], T[i] + H[i]), outline='red' if c[i] < 90 else 'green', width=2)
out.save('wordBoxes.png'); done('wordBoxes.png')
'''
WORDSCUT = _HEADZ + WORDS_BODY

HURTS_BODY = r'''d = wd()
def go(name, **kw):
    im, t = render(**kw); print('%-18s' % name, cer(t, ocr(im)))
for px in (6, 8, 10, 12, 24): go('letters %d px' % px, px=px)
for r in (2, 3, 5): go('tilted %d degrees' % r, rot=r)
for sd in (40, 60): go('noise sd %d' % sd, noise=sd)
inv, t = render(fg=255, bg=0)
print('white on black', cer(t, ocr(inv)))
off = '-c tessedit_do_invert=0'
print('invert off', cer(t, ocr(inv, config=off)))
sheet = Image.new('L', (900, 270), 255)
tiles = (('8 px', {'px': 8}, 0), ('12 px', {'px': 12}, 0), ('tilted 5 degrees', {'rot': 5}, 40), ('noise sd 60', {'noise': 60}, 10))
for i, (name, kw, y) in enumerate(tiles):
    p = render(**kw)[0]; x, yy = (i % 2) * 450, (i // 2) * 135
    ImageDraw.Draw(sheet).text((x + 6, yy + 2), name, fill=0)
    sheet.paste(p.crop((0, y, min(440, p.width), min(y + 110, p.height))), (x + 5, yy + 16))
sheet.save('hurts.png'); done('hurts.png')
'''
HURTSCUT = _HEAD + HURTS_BODY

CLEAN_BODY = r'''d = wd()
small, t = render(px=9, width=600)
print('9 px page:', cer(t, ocr(small)))
x2 = small.resize((small.width * 2, small.height * 2), Image.Resampling.LANCZOS)
print('enlarged 2 times:', cer(t, ocr(x2)))
print('told it is 300 dpi:', cer(t, ocr(small, config='--dpi 300')))
f = ImageFont.truetype(FONTS['sans'], 24); s = 'Tesseract reads this line.'
b = f.getbbox(s); tight = Image.new('L', (b[2] - b[0], b[3] - b[1]), 255)
ImageDraw.Draw(tight).text((-b[0], -b[1]), s, font=f, fill=0)
print('a tight crop', tight.size, '->', repr(ocr(tight).strip()))
framed = ImageOps.expand(tight, border=10, fill=255)
print('with a 10 px border', framed.size, '->', repr(ocr(framed).strip()))
sheet = Image.new('L', (620, 190), 255); sheet.paste(small.crop((0, 0, 600, 40)), (10, 5))
sheet.paste(x2.crop((0, 0, 600, 80)), (10, 55)); sheet.paste(framed, (10, 145)); sheet.save('cleaned.png'); done('cleaned.png')
'''
CLEANCUT = _HEAD + CLEAN_BODY

CV_BODY = r'''d = wd()
import cv2
im, t = render(rot=6)
dark = cv2.findNonZero(255 - np.asarray(im))
angle = cv2.minAreaRect(dark)[2]
print('minAreaRect:', round(angle, 1), '| CER turned', cer(t, ocr(im)))
fixed = im.rotate(angle, expand=True, fillcolor=255, resample=Image.BICUBIC)
print('CER turned back:', cer(t, ocr(fixed)))
nz, t2 = render(noise=60)
print('noise sd 60: CER', cer(t2, ocr(nz)))
med = Image.fromarray(cv2.medianBlur(np.asarray(nz), 3))
print('median filter 3: CER', cer(t2, ocr(med)))
flag = cv2.THRESH_BINARY + cv2.THRESH_OTSU
cut = cv2.threshold(np.asarray(med), 0, 255, flag)[1]
print('then Otsu: CER', cer(t2, ocr(Image.fromarray(cut))))
sheet = Image.new('L', (900, 290), 255)
tiles = (('turned 6 degrees', im, 30), ('turned back', fixed, 30), ('noise sd 60', nz, 10), ('median filter 3', med, 10))
for i, (name, p, y) in enumerate(tiles):
    x, yy = (i % 2) * 450, (i // 2) * 145
    ImageDraw.Draw(sheet).text((x + 6, yy + 2), name, fill=0)
    sheet.paste(p.crop((0, y, min(440, p.width), min(y + 110, p.height))), (x + 5, yy + 16))
sheet.save('cleanCv.png'); done('cleanCv.png')
'''
CVCUT = _HEAD + CV_BODY

PSM_BODY = r'''d = wd()
one, two = TEXT.split(' With ')
a, ta = render(one + '.', font='roman', px=24, width=430, pad=0)
b, tb = render('With ' + two, font='roman', px=24, width=430, pad=0)
page = Image.new('L', (a.width + 4 + b.width, max(a.height, b.height) + 30), 255)
page.paste(a, (0, 15)); page.paste(b, (a.width + 4, 15))
print('two columns 4 px apart, default mode:', cer(ta + ' ' + tb, ocr(page)))
left = page.crop((0, 0, a.width, page.height))
print('the left column cut out, --psm 6:', cer(ta, ocr(left, config='--psm 6')))
line, t = render('Order 4417-B shipped on 2026-10-13', px=28, width=640, pad=10)
print('one line, default:', repr(ocr(line).strip()))
print('one line, --psm 7:', repr(ocr(line, config='--psm 7').strip()))
wl = '--psm 7 -c tessedit_char_whitelist=0123456789-'
print('whitelist 0123456789-:', repr(ocr(line, config=wl).strip()))
print('timeout=0.001:', err(lambda: ocr(line, timeout=0.001)))
h = subprocess.check_output(['tesseract', '--help-psm'], text=True)
print('modes listed by --help-psm:', len(re.findall(r'^\s+\d+\s', h, re.M)))
page.save('columns.png'); done('columns.png')
'''
PSMCUT = _HEAD + PSM_BODY

HYPHEN_BODY = r'''d = wd(); shipped(d)
text = ocr(Image.open('ocr-example.png'))
known = {w.lower() for w in open('/usr/share/dict/words').read().split()}
def undo(t, strict=True):
    def join(m):
        w = m[1] + m[2]
        return w if not strict or w.lower() in known else m[1] + '-' + m[2]
    return re.sub(r'(\w+)-\n(\w+)', join, t)
broken = re.findall(r'(\w+)-\n(\w+)', text)
print(len(broken), 'line-end hyphens, first three:', ['-'.join(p) for p in broken[:3]])
s = 'The well-\nknown author of the straight-\nforward code.'
print('naive undo :', repr(undo(s, False)))
print('strict undo:', repr(undo(s)))
inv = 'Invoice 1058 Total 1,000.00 Order O8l0'
for px in (9, 12):
    im, t = render(inv, px=px, width=700, pad=10)
    o = norm(ocr(im, config='--psm 7')); print('%2d px:' % px, repr(o), cer(t, o))
text_img = Image.open('ocr-example.png').crop((190, 45, 860, 90)).convert('RGB')
text_img.save('hyphen.png'); done('hyphen.png')
'''
HYPHENCUT = _HEADZ + HYPHEN_BODY

CONF_BODY = r'''d = wd(); shipped(d)
img = Image.open('frankenstein.png')
dd = tess.image_to_data(img, output_type=tess.Output.DICT)
words = [(w, c) for w, c in zip(dd['text'], dd['conf']) if w.strip()]
known = {w.lower() for w in open('/usr/share/dict/words').read().split()}
odd = [w for w, c in words if w.isalpha() and w.lower() not in known]
print(len(words), 'words, mean confidence', round(sum(c for w, c in words) / len(words), 2))
print('words a spell check flags:', odd)
print('In and Motion are real words:', 'in' in known, 'motion' in known)
low = min(words, key=lambda x: x[1])
print('lowest confidence:', low, '| Motion:', dict(words)['Motion'])
i = [k for k, w in enumerate(dd['text']) if w == 'In'][0]
x, y, w, h = dd['left'][i], dd['top'][i], dd['width'][i], dd['height'][i]
img.crop((x - 20, y - 10, x + w + 120, y + h + 10)).convert('RGB').resize(((w + 140) * 3, (h + 20) * 3), Image.Resampling.LANCZOS).save('lowWord.png')
done('lowWord.png')
'''
CONFCUT = _HEADZ + CONF_BODY

LANG_BODY = r'''d = wd(); shipped(d)
print('installed packs:', tess.get_languages(config=''))
img = Image.open('frankenstein_jpn.png')
jpn = tess.image_to_string(img, lang='jpn')
j = [l for l in jpn.split('\n') if l.strip()]
print('lang=jpn:', len(j), 'lines; first line begins', j[0][:12])
e = tess.image_to_string(img, lang='eng')
print('lang=eng:', e[:12], '| Japanese characters:', sum(ord(c) > 0x2E80 for c in e))
MIX = 'The cat is 猫 and the dog is 犬 today'
mi = Image.new('L', (1000, 90), 255); F = ImageFont.truetype(FONTS['jp'], 40)
ImageDraw.Draw(mi).text((20, 20), MIX, font=F, fill=0)
for lg in ('eng', 'jpn', 'eng+jpn'):
    o = tess.image_to_string(mi, lang=lg, config='--psm 7').strip()
    print('mixed line, lang=%-8s' % lg, repr(o), cer(MIX, o))
img.crop((30, 30, 600, 120)).save('japanese.png'); done('japanese.png')
'''
LANGCUT = _HEADZ + LANG_BODY

PACKS_BODY = r'''d = wd()
F = ImageFont.truetype(FONTS['sans'], 32); t = 'Die Größe der Straße'
de = Image.new('L', (400, 80), 255)
ImageDraw.Draw(de).text((20, 20), t, font=F, fill=0)
ALL = '/home/claude/tessdata_fast_all'; P = '/home/claude/tessdata_%s/eng.traineddata'
def read(lg): return tess.image_to_string(de, lang=lg, config='--psm 7').strip()
print('lang=deu:', repr(read('deu')))
for lg in ('ger', 'German', 'eng+xyz'):
    e = err(lambda: read(lg)); print('lang=%-8s' % lg, e[0], e[1] if e[0] == 'ok' else '')
L = tess.get_languages(config='--tessdata-dir ' + ALL)
bad = [x for x in L if len(x) != 3]
print(len(L), 'packs:', L[:2], '...', L[-2:], '|', len(bad), 'not three letters:', bad[:2])
print('osd and equ in the list:', 'osd' in L, 'equ' in L)
sz = sum(os.path.getsize('%s/%s.traineddata' % (ALL, x)) for x in L)
sizes = [os.path.getsize(P % k) for k in ('fast', 'best', 'legacy')]
print('together: %.0f MB' % (sz / 1e6), '| eng fast, best, legacy:', sizes)
de.save('germanLine.png'); done('germanLine.png')
'''
PACKSCUT = _HEAD + PACKS_BODY

NAPS_BODY = r'''d = wd(); shipped(d)
def sh(*a): return subprocess.run(a, capture_output=True, text=True).stdout
args = ['-i', 'frankenstein.png', '-o', 'output.pdf', '--install',
        'ocr-eng', '--ocrlang', 'eng', '-n', '0', '-f', '-v']
win = r'C:\Program Files\NAPS2\NAPS2.Console.exe'
print('Windows path:', err(lambda: subprocess.run([win] + args))[0])
flat = ['flatpak', 'run', 'com.naps2.Naps2', 'console']
print('flatpak:', err(lambda: subprocess.run(flat + args))[0])
naps2_path = ['naps2', 'console']
proc = subprocess.run(naps2_path + args, capture_output=True)
out = proc.stdout
print('returncode', proc.returncode, '| stdout is', type(out).__name__)
print(out.decode().strip().splitlines()[-1])
txt = sh('pdftotext', 'output.pdf', '-')
n = re.search(r'Pages:\s+(\d+)', sh('pdfinfo', 'output.pdf')).group(1)
print('pages', n, '| chars', len(norm(txt)), '| CER', cer(TRUTH, txt))
'''
NAPSCUT = _HEADZ + NAPS_BODY

OVERWRITE_BODY = r'''d = wd(); shipped(d)
def sh(*a): return subprocess.run(a, capture_output=True, text=True).stdout
F = ImageFont.truetype(FONTS['sans'], 90); ims = []
for i in range(7):
    im = Image.new('L', (700, 300), 255)
    ImageDraw.Draw(im).text((40, 90), 'spam%d' % i, font=F, fill=0)
    ims.append(im)
ims[0].save('spam.pdf', save_all=True, append_images=ims[1:])
naps2_path = ['naps2', 'console']
opts = ['--ocrlang', 'eng', '-n', '0']
def pages(spec):
    sh(*naps2_path, '-i', spec, '-o', 'in.pdf', *opts, '-f')
    n = int(re.search(r'Pages:\s+(\d+)', sh('pdfinfo', 'in.pdf')).group(1))
    pt = lambda k: norm(sh('pdftotext', '-f', str(k), '-l', str(k), 'in.pdf', '-'))
    return [pt(k) for k in range(1, n + 1)]
base = ['-i', 'frankenstein.png', '-o', 'output.pdf'] + opts + ['-v']
for extra in (['-f'], [], ['-f']):
    r = subprocess.run(naps2_path + base + extra, capture_output=True, text=True)
    last = r.stdout.strip().splitlines()[-1].split('. Path')[0]
    print('with' if extra else 'without', '-f: rc', r.returncode, '|', last)
for spec in ('spam.pdf[0:2]', 'spam.pdf[-2:]', 'spam.pdf[1:6:2]'):
    print('-i', spec, '->', pages(spec))
sheet = Image.new('RGB', (7 * 100, 50), 'white')
for i, im in enumerate(ims):
    sheet.paste(im.resize((95, 40)).convert('RGB'), (i * 100 + 2, 5))
    if i in (1, 3, 5): ImageDraw.Draw(sheet).rectangle((i * 100, 2, i * 100 + 97, 47), outline='red', width=2)
sheet.save('pagesPicked.png'); done('pagesPicked.png')
'''
OVERWRITECUT = _HEADZ + OVERWRITE_BODY

PDF_BODY = r'''d = wd(); shipped(d)
OMP = '/home/claude/venv314_ch22_ocrmypdf/bin/ocrmypdf'
def sh(*a): return subprocess.run(a, capture_output=True, text=True).stdout
def chars(f): return len(norm(sh('pdftotext', f, '-')))
def om(*a): return subprocess.run([OMP, *a], capture_output=True, stdin=subprocess.DEVNULL).returncode
img = Image.open('frankenstein.png').convert('RGB')
img.save('image_only.pdf', resolution=150)
print('Pillow PDF:', chars('image_only.pdf'), 'chars')
b = tess.image_to_pdf_or_hocr(img, extension='pdf')
open('searchable.pdf', 'wb').write(b)
print('pytesseract:', b[:5], chars('searchable.pdf'), 'chars')
box = sh('pdftotext', '-bbox', 'searchable.pdf', '-')
print('word boxes:', box.count('<word'))
print('ocrmypdf, no dpi:', om('frankenstein.png', 'a.pdf'))
dpi = om('--image-dpi', '150', 'frankenstein.png', 'b.pdf')
print('--image-dpi 150:', dpi, chars('b.pdf'), 'chars')
print('on a PDF with text:', om('b.pdf', 'c.pdf'))
print('--skip-text:', om('--skip-text', 'b.pdf', 'd.pdf'))
'''
PDFCUT = _HEADZ + PDF_BODY

SCREEN_BODY = r'''disp = ':%d' % (120 + os.getpid() % 60)
xv = subprocess.Popen(['Xvfb', disp, '-screen', '0', '1280x1024x24'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(3)
env = dict(os.environ, DISPLAY=disp, XDG_SESSION_TYPE='x11', XAUTHORITY=os.path.join(d, 'x'))
open('x', 'w').close()
viewer = subprocess.Popen(['display', '-geometry', '+0+0', 'frankenstein.png'], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(3)
import atexit
atexit.register(lambda: (subprocess.run(['pkill', '-x', 'display-im6.q16']), xv.terminate(), xv.wait()))
cmd = [sys.executable, '-W', 'ignore', '-c']
kw = dict(capture_output=True, text=True, env=env, timeout=120)
code = """import pyautogui, pytesseract as tess
img = pyautogui.screenshot()
img.save('screen.png')
text = tess.image_to_string(img.crop(%s))
open('output.txt', 'a', encoding='utf-8').write(text)
print(img.size, len(text))"""
def run(box):
    return subprocess.run(cmd + [code % box], **kw)
for box in ('(400, 200, 1000, 800)', '(0, 0, 1130, 672)', '(0, 0, 1130, 672)'):
    r = run(box)
    print(box, '->', r.returncode, r.stdout.strip().splitlines()[-1])
print('output.txt:', len(open('output.txt', encoding='utf-8').read()), 'characters')
shot = Image.open('screen.png')
print('CER of the second run alone:', cer(TRUTH, ocr(shot.crop((0, 0, 1130, 672)))))
shot = shot.convert('RGB').resize((640, 512))
ImageDraw.Draw(shot).rectangle((200, 100, 500, 400), outline='red', width=3)
shot.save('screenShot.png'); done('screenShot.png')
'''
SCREENCUT = _HEADZ + "assert shutil.which('Xvfb') and shutil.which('display') and shutil.which('scrot'), 'NOT EXECUTED: Xvfb, display or scrot is missing'\nd = wd(); shipped(d)\n" + SCREEN_BODY

# ---- charts and tables (re-computed by the deck check) -----------------------------------------------------------------
_HEADSRC = B.HEAD
CHARTS = {
    "cerBySize": {
        "setup": "import os, warnings\n" + _HEADSRC.replace("import pytesseract as tess", "import pytesseract as tess") +
                 "ROWS = []\nfor px in (6, 8, 10, 12, 16, 24):\n    im, t = render(px=px)\n    ROWS.append(('%d px' % px, cer(t, ocr(im))))\n",
        "expr": "ROWS"},
    "dataBytes": {
        "setup": "import os\nROWS = [(k, round(os.path.getsize('/home/claude/' + p + '/eng.traineddata') / 1e6, 1)) for k, p in (('fast', 'tessdata_fast'), ('best', 'tessdata_best'), ('legacy', 'tessdata_legacy'))]\n",
        "expr": "ROWS"},
}

_PROBE = r'''
import json, sys, importlib.metadata as md, warnings
warnings.simplefilter('ignore')
r = {'Python': sys.version.split()[0]}
def v(n):
    try: return md.version(n)
    except md.PackageNotFoundError: return 'none'
r['pytesseract'] = v('pytesseract'); r['Pillow'] = v('pillow')
try:
    import pytesseract as t
    from PIL import Image, ImageDraw, ImageFont
    r['import'] = 'ok'
    im = Image.new('L', (420, 60), 255); ImageDraw.Draw(im).text((10, 10), 'Tesseract reads this', font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 32), fill=0)
    r['image_to_string'] = repr(t.image_to_string(im).strip())
    r['get_languages'] = str(len(t.get_languages(config=''))) + ' codes'
except BaseException as e:
    r['import'] = (type(e).__name__ + ': ' + str(e).split(' from ')[0]).replace(chr(10), ' ')
    r['image_to_string'] = '-'; r['get_languages'] = '-'
print(json.dumps(r))
'''
INTERPS = [("3.14.6 newest", "/home/claude/venv314_ch22_latest/bin/python"), ("3.14.6 pins", "/home/claude/venv314_ch22_pins/bin/python"),
           ("3.13.14 pins", "/home/claude/venv313_ch22_pins/bin/python"), ("3.14.6 empty", "/home/claude/venv314_ch22_bare/bin/python")]
_ROWS = [("Python", "Python"), ("pytesseract", "pytesseract"), ("Pillow", "Pillow"), ("import pytesseract", "import"), ("image_to_string()", "image_to_string"),
         ("get_languages()", "get_languages")]

_ENG_SETUP = r'''
import hashlib, io, os, re, subprocess, sys, zipfile
import pytesseract as tess
from PIL import Image
Z = open('/home/claude/ch22_cache/ch22_materials.zip', 'rb').read()
assert hashlib.sha256(Z).hexdigest() == 'dac627e807f69ee14913ba621a15dec1f98db739d76939555ba5360d05eba916'
zf = zipfile.ZipFile(io.BytesIO(Z)); img = Image.open(io.BytesIO(zf.read([n for n in zf.namelist() if n.endswith('/frankenstein.png') and '__MACOSX' not in n][0]))); img.load()
TRUTH = ("THE MODERN PROMETHEUS. 43 CHAPTER V. IT was on a dreary night of November, that I beheld the accomplishment of my toils. With an anxiety that almost amounted to agony, "
         "I collected the instruments of life around me, that I might infuse a spark of being into the lifeless thing that lay at my feet. It was already one in the morning ; "
         "the rain pattered dismally against the panes, and my candle was nearly burnt out, when, by the glimmer of the half-extinguished light, I saw the dull yellow eye of the creature open ; "
         "it breathed hard, and a convulsive motion agitated its limbs.")
def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1): cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]
def norm(t): return re.sub(r'\s+', ' ', t).strip()
ENG = [('4.1.1', '/home/claude/tesseract-4.1.1/bin/tesseract'), ('5.3.4', '/usr/bin/tesseract'), ('5.5.3', '/home/claude/tesseract-5.5.3/bin/tesseract')]
DATA = [('fast', '/home/claude/tessdata_fast'), ('best', '/home/claude/tessdata_best'), ('legacy+lstm', '/home/claude/tessdata_legacy')]
def cell(exe, data):
    tess.pytesseract.tesseract_cmd = exe; os.environ['TESSDATA_PREFIX'] = data
    o = norm(tess.image_to_string(img)); r = norm(TRUTH)
    return '%s  %s' % (re.search(r'V\.?\s+(\S+)', o).group(1), round(lev(r, o) / len(r), 4))
ROWS = [['Tesseract'] + [k for k, _ in DATA]] + [[v] + [cell(e, d) for _, d in DATA] for v, e in ENG]
'''
TABLES = {
    "environments": {
        "setup": "import json, subprocess\nPROBE = %r\nINTERPS = %r\nres = []\nfor v, p in INTERPS:\n    r = subprocess.run([p, '-c', PROBE], capture_output=True, text=True)\n"
                 "    assert r.returncode == 0, (v, r.stderr[-300:])\n    res.append(json.loads(r.stdout))\nROWS = %r\n" % (_PROBE, INTERPS, _ROWS),
        "expr": "[['check'] + [v for v, p in INTERPS]] + [[label] + [x.get(key, '-') for x in res] for label, key in ROWS]"},
    "engines": {"setup": _ENG_SETUP, "expr": "ROWS"},
    "configurations": {
        "setup": "import json, os\nT = json.load(open(os.path.join(HERE, '..', 'ch22-page', 'third_party_record_v1_0_0.json')))['items']\n"
                 "CF = list(T[0]['output'])\nNAME = {'LATEST / apt': 'apt 5.3.4, fast', 'LATEST / 5.5.3-fast': '5.5.3, fast', 'LATEST / 5.5.3-best': '5.5.3, best', 'LATEST / 4.1.1-fast': '4.1.1, fast',\n"
                 "        'LATEST / apt-all': 'apt 5.3.4, all packs', 'LATEST / 5.5.3-all': '5.5.3, all packs', 'PINS313 / apt': 'apt 5.3.4, fast', 'PINS / apt': 'apt 5.3.4, fast', 'BARE / apt': 'apt 5.3.4, fast'}\n"
                 "ROW = {'LATEST / apt': 'newest', 'LATEST / 5.5.3-fast': 'newest', 'LATEST / 5.5.3-best': 'newest', 'LATEST / 4.1.1-fast': 'newest', 'LATEST / apt-all': 'newest', 'LATEST / 5.5.3-all': 'newest', 'PINS313 / apt': 'pins', 'PINS / apt': 'pins', 'BARE / apt': 'empty'}\n"
                 "def n(i):\n    s = [x for l in T[i]['output']['ocr']['results'] for x in l['statements']]\n    return '%d of %d' % (sum(x['as printed']['matches the book'] for x in s), len(s))\n"
                 "def pkg(c, k):\n    v = T[0]['output'][c][k]\n    return '-' if v is None else str(v)\n",
        "expr": "[['row', 'Python', 'pytesseract', 'Pillow', 'Tesseract, data', 'statements = book']] + "
                "[[ROW[c], pkg(c, 'python'), pkg(c, 'pytesseract'), pkg(c, 'pillow'), NAME[c], n(3 + i)] for i, c in enumerate(CF)]"},
}

PROGRAMS = {
    # the twelve programs of the corpus, recorded under their own names
    **{k: v for k, v in B.PROGRAMS.items()},
    "fourLinesCut_v1_0_0.py": (FOURLINES, (), True),
    "frankCut_v1_0_0.py": (FRANKCUT, (), True),
    "errorsCut_v1_0_0.py": (ERRORSCUT, (), False),
    "wordsCut_v1_0_0.py": (WORDSCUT, (), True),
    "hurtsCut_v1_0_0.py": (HURTSCUT, (), False),
    "cleanCut_v1_0_0.py": (CLEANCUT, (), False),
    "cvCut_v1_0_0.py": (CVCUT, (), False),
    "psmCut_v1_0_0.py": (PSMCUT, (), False),
    "hyphenCut_v1_0_0.py": (HYPHENCUT, (), True),
    "confCut_v1_0_0.py": (CONFCUT, (), True),
    "langCut_v1_0_0.py": (LANGCUT, (), True),
    "packsCut_v1_0_0.py": (PACKSCUT, (), False),
    "naps2Cut_v1_0_0.py": (NAPSCUT, (), True),
    "overwriteCut_v1_0_0.py": (OVERWRITECUT, (), True),
    "pdfCut_v1_0_0.py": (PDFCUT, (), True),
    "screenCut_v1_0_0.py": (SCREENCUT, (), True),
}
KIND = {n: "none" for n in PROGRAMS}
STANDKEY = {}
for _n in ("ocrscreenOnXvfb_v1_0_0.py", "screenCut_v1_0_0.py"):
    KIND[_n] = "standin"; STANDKEY[_n] = ("Virtual display",)
# the pictures a slide shows: file name -> the program that makes it
IMAGES = {"ocrTop.png": "fourLinesCut_v1_0_0.py", "frankLine.png": "frankCut_v1_0_0.py", "readsLine.png": "errorsCut_v1_0_0.py", "wordBoxes.png": "wordsCut_v1_0_0.py",
          "hurts.png": "hurtsCut_v1_0_0.py", "cleaned.png": "cleanCut_v1_0_0.py", "cleanCv.png": "cvCut_v1_0_0.py", "columns.png": "psmCut_v1_0_0.py",
          "hyphen.png": "hyphenCut_v1_0_0.py", "lowWord.png": "confCut_v1_0_0.py", "japanese.png": "langCut_v1_0_0.py", "germanLine.png": "packsCut_v1_0_0.py",
          "pagesPicked.png": "overwriteCut_v1_0_0.py", "screenShot.png": "screenCut_v1_0_0.py"}
EQUIV = {}
SUBSET = {}

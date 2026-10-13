#!/usr/bin/env python3
"""SEN0414 chapter 22 (Recognizing Text in Images, 3rd edition) - the shared base of the corpus, version 1.0.0.

Holds the chapter's whole programs as text, the single source a deck or a page's Lab tab can read, in the shape of sen0414_ch21_corpus_base_v1_0_0.py.
Each program is a complete script that exits 0 and prints what it printed on 2026-10-13 under Python 3.14.6 (uv) in the environment
/home/claude/venv314_ch22_latest (pytesseract 0.3.13, Pillow 12.3.0, NumPy 2.5.4, opencv-python-headless 5.0.0.93, PyAutoGUI 0.9.54) with the REAL Tesseract 5.3.4 of
Ubuntu 24.04 (apt; English data = tessdata_fast) on the PATH. Programs that compare engines also use Tesseract 5.5.3 and 4.1.1 built from source and the tessdata_fast,
tessdata_best and legacy tessdata repositories cloned under /home/claude; NAPS2 8.5.1 is the .deb of naps2.com (it runs its own Tesseract 5.5.0); ocrmypdf 17.13.0 runs from
its own environment (/home/claude/venv314_ch22_ocrmypdf). Nothing is sent to any person or service. The files of the book's online materials the programs use
(ocr-example.png, frankenstein.png, frankenstein_jpn.png and preprocess_ocr.py) are FETCHED AT RUN TIME from the publisher's zip (or from the zip kept under the
CH22_CACHE folder when that variable is set) and checked against the SHA-256 the study recorded; if the zip cannot be reached or does not match, the program prints "NOT EXECUTED" and
the reason and stops (the files are never replaced by a copy). Programs that need no shipped file draw pages of known text themselves. Where a program needs software this machine
may lack (Xvfb, ImageMagick display, NAPS2, poppler, ocrmypdf, the second and third Tesseract) it prints NOT EXECUTED and the reason. The one step of the chapter that is not run
anywhere is the large language model.
LOCAL STAND-IN: ocrscreenOnXvfb_v1_0_0.py takes its screenshot of a virtual X display (Xvfb) on which the real ImageMagick display shows frankenstein.png; nobody sees the screen.
The record that reads the book's page and asks the public services is sen0414_ch22_live_v1_0_0.py; the one that replays the chapter's listings is sen0414_ch22_thirdparty_v1_0_0.py.
"""
HEAD = r'''import io, os, sys, re, math, json, time, shutil, zipfile, hashlib, tempfile, warnings, subprocess, difflib, importlib.metadata as md
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import pytesseract as tess
warnings.simplefilter('ignore')
if os.environ.get('CH22_TESS'): tess.pytesseract.tesseract_cmd = os.environ['CH22_TESS']
if os.environ.get('CH22_DATA'): os.environ['TESSDATA_PREFIX'] = os.environ['CH22_DATA']
FONTS = {'sans': '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 'serif': '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', 'mono': '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
         'bold': '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 'roman': '/usr/share/fonts/opentype/urw-base35/NimbusRoman-Regular.otf',
         'script': '/usr/share/fonts/opentype/urw-base35/Z003-MediumItalic.otf', 'jp': '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'}
TEXT = ('It was on a dreary night of November, that I beheld the accomplishment of my toils. With an anxiety that almost amounted to agony, '
        'I collected the instruments of life around me, that I might infuse a spark of being into the lifeless thing that lay at my feet.')
def err(f):
    try: return ('ok', f())
    except BaseException as e: return (type(e).__name__, str(e).splitlines()[0][:150] if str(e) else '')
def wd():
    d = tempfile.mkdtemp(); os.chdir(d); return d
def lev(a, b):
    if a == b: return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1): cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]
def norm(t): return re.sub(r'\s+', ' ', t).strip()
def cer(ref, hyp):
    """character error rate: edit distance of the two texts with every run of white space made one space, divided by the length of the reference"""
    r = norm(ref); return round(lev(r, norm(hyp)) / len(r), 4)
def wrap(text, font, width):
    d = ImageDraw.Draw(Image.new('L', (10, 10))); lines = []; cur = ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= width: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines
def render(text=TEXT, font='sans', px=24, fg=0, bg=255, width=900, pad=20, noise=0, rot=0, seed=1, dpi=None):
    """a page of known text: returns (grey image, the text as the lines it was wrapped into joined by spaces)"""
    f = ImageFont.truetype(FONTS.get(font, font), px); lines = wrap(text, f, width - 2 * pad); lh = int(px * 1.4)
    im = Image.new('L', (width, lh * len(lines) + 2 * pad), bg); d = ImageDraw.Draw(im)
    for i, l in enumerate(lines): d.text((pad, pad + i * lh), l, font=f, fill=fg)
    if rot: im = im.rotate(rot, expand=True, fillcolor=bg, resample=Image.Resampling.BICUBIC)
    if noise:
        a = np.asarray(im).astype(float) + np.random.default_rng(seed).normal(0, noise, (im.height, im.width)); im = Image.fromarray(np.clip(a, 0, 255).astype('uint8'))
    return im, ' '.join(lines)
def ocr(im, **k): return tess.image_to_string(im, **k)
'''
SHIPPED = r'''ZIPSHA = 'dac627e807f69ee14913ba621a15dec1f98db739d76939555ba5360d05eba916'
FILESHA = {'ocr-example.png': 'c875a04c8a51401f59848ea93bd754fb6095f9f1a0041e4878dd05eeb44b13b8', 'frankenstein.png': 'c2125e5ef6840d4f23dfba68021c52710290a4c8d3cafdbabf1f619c70b33851',
           'frankenstein_jpn.png': '3f812b8e5e396db6685f1cfe9e35639b9eaabd727cdb861e2663c6c768ca40fd', 'preprocess_ocr.py': 'e204109350e49c621159c3c8d656da3af564e368a9d0d84b95f222cfa583f377'}
def shipped(directory):
    """writes the shipped files into directory, each checked against its SHA-256; prints NOT EXECUTED and stops (exit 0) when the zip cannot be had"""
    import urllib.request
    try:
        cache = os.environ.get('CH22_CACHE'); p = os.path.join(cache, 'ch22_materials.zip') if cache else None
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
'''
OCR = HEAD + SHIPPED + r'''# Chapter 22, "OCR Fundamentals": the book's four lines on its own ocr-example.png, and what the page returns beyond the paragraph the book prints.
d = wd(); shipped(d)
BOOK = ["This book provides you with practice examples of how programming",
        "concepts are applied, with a collection of over 80 games, simulations, and dig-",
        "ital art programs. These aren't code snippets; they're full, runnable Python",
        "programs. You can copy their code to become familiar with how they work,",
        "experiment with your own changes, and then attempt to re-create them on",
        "your own as practice. After a while, you'll start to get ideas for your own pro-",
        "grams and, more importantly, know how to go about creating them."]
print('Tesseract', tess.get_tesseract_version(), ' pytesseract', md.version('pytesseract'), ' Pillow', md.version('pillow'))
img = Image.open('ocr-example.png'); print('ocr-example.png:', img.size, img.mode, 'dpi in the file:', img.info.get('dpi'))
text = tess.image_to_string(img); lines = text.split('\n')
print('the returned object is a', type(text).__name__, 'of', len(text), 'characters and', len(lines), 'lines; it ends with', repr(text[-3:]))
print('the first 7 lines equal the 7 lines the book prints:', lines[:7] == BOOK)
for a, b in zip(lines[:7], BOOK):
    if a != b: print('  differs:', repr(a), 'against the book', repr(b))
print('the book stops after those lines with --snip--; the page also returns the headings', [h for h in ('How to Design Small Programs', 'Who Is This Book For?') if h in text])
print('paragraph breaks (empty lines) in the result:', text.count('\n\n'))
print('line ends that keep a hyphen:', len(re.findall(r'-\n', text)), re.findall(r'\w+-\n\w+', text)[:3])
print('the line of the page that holds mazes:', [l for l in lines if 'mathematical puzzles' in l])
m = re.search(r'also 2\S+', text); print('the superscript of 2^8 comes back as:', repr(m.group(0)) if m else None)
print('the italic tictactoe.py comes back as:', re.findall(r'like (\S+)\.py', text))
print('the curly apostrophes of the page:', [w for w in re.findall(r"\S*[‘’']\S*", text)][:8])
print('the same image as RGB, as a path and as a numpy array give the same text:', tess.image_to_string(img.convert('RGB')) == text, tess.image_to_string('ocr-example.png') == text, tess.image_to_string(np.asarray(img)) == text)
'''
FRANK = HEAD + SHIPPED + r'''# Chapter 22, "Fixing Mistakes Using Large Language Models": the book's frankenstein.png listing, what it prints against what the book prints, and the confidence of every word.
d = wd(); shipped(d)
BOOK = """THE MODERN PROMETHEUS. 43

CHAPTER V.

Iv was on a dreary night of November, that I beheld the
accomplishment of my toils. With an anxiety that almost
amounted to agony, I collected the instruments of life
around me, that I might infuse a spark of being into the
lifeless thing that lay at my feet. It was already one in
the morning ; the rain pattered dismally against the panes,
and my candle was nearly burnt out, when, by the glimmer
of the half-extinguished light, I saw the dull yellow eye
of the creature open ; it breathed hard, and a convulsive
Motion agitated its limbs.
"""
# what is printed on the page of the 1831 print, read from the image (the first word is set with a large I and a small capital T)
TRUTH = ("THE MODERN PROMETHEUS. 43 CHAPTER V. IT was on a dreary night of November, that I beheld the accomplishment of my toils. With an anxiety that almost amounted to agony, "
         "I collected the instruments of life around me, that I might infuse a spark of being into the lifeless thing that lay at my feet. It was already one in the morning ; "
         "the rain pattered dismally against the panes, and my candle was nearly burnt out, when, by the glimmer of the half-extinguished light, I saw the dull yellow eye of the creature open ; "
         "it breathed hard, and a convulsive motion agitated its limbs.")
print('Tesseract', tess.get_tesseract_version(), ' language data eng:', hashlib.sha256(open(os.path.join(os.environ.get('TESSDATA_PREFIX', '/usr/share/tesseract-ocr/5/tessdata'), 'eng.traineddata'), 'rb').read()).hexdigest()[:12])
img = Image.open('frankenstein.png'); print('frankenstein.png:', img.size, img.mode)
text = tess.image_to_string(img)
print('output equals what the book prints:', text == BOOK, ' lines', len(text.split('\n')), 'against', len(BOOK.split('\n')))
for a, b in zip(text.split('\n'), BOOK.split('\n')):
    if a != b: print('  differs: got', repr(a), ' book', repr(b))
print('character error rate against the printed page:', cer(TRUTH, text), ' against the book\'s printed output:', cer(norm(BOOK), text))
w = [x for x in norm(text).split(' ')]; t = TRUTH.split(' ')
print('words:', len(w), 'against', len(t), ' words that differ from the page (aligned by difflib):', [(t[i1:i2], w[j1:j2]) for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, t, w).get_opcodes() if tag != 'equal'])
dd = tess.image_to_data(img, output_type=tess.Output.DICT)
words = [(x, c) for x, c in zip(dd['text'], dd['conf']) if x.strip()]
print('words with a confidence:', len(words), ' mean', round(sum(c for _, c in words) / len(words), 2), ' lowest', min(c for _, c in words))
print('words below 80:', [(x, c) for x, c in words if c < 80], ' below 90:', [(x, c) for x, c in words if c < 90])
print('the conf of the other words in the paragraph\'s first line:', [(x, round(c)) for x, c in words[:9]])
dicw = open('/usr/share/dict/words', encoding='utf-8').read().split() if os.path.exists('/usr/share/dict/words') else None
if dicw is None: print('NOT EXECUTED: no /usr/share/dict/words on this machine (the package wamerican)')
else:
    low = {x.lower() for x in dicw}
    toks = [t.lower() for x, _ in words for t in re.findall(r"[A-Za-z]+", x)]
    print('spell check against the', len(dicw), 'words of /usr/share/dict/words: tokens of the result not in it:', sorted({t for t in toks if t not in low}))
    print('the two wrong words the book names, as the spell checker sees them: iv', 'iv' in low, ' in', 'in' in low, ' it', 'it' in low, ' motion', 'motion' in low, ' (so neither is flagged)')
'''
LANGS = HEAD + SHIPPED + r'''# Chapter 22, "Recognizing Text in Non-English Languages": the language packs, the book's Japanese image, the wrong language, and 'eng+jpn', against text whose letters are known.
d = wd(); shipped(d)
print('installed language packs:', tess.get_languages(config=''))
t0 = tempfile.mkdtemp(); shutil.copy('/usr/share/tesseract-ocr/5/tessdata/eng.traineddata', t0); a = tess.get_languages(config='--tessdata-dir ' + t0); shutil.copy('/usr/share/tesseract-ocr/5/tessdata/deu.traineddata', t0); b = tess.get_languages(config='--tessdata-dir ' + t0)
print('a folder with eng.traineddata only:', a, '; after deu.traineddata is copied into it the next call gives', b, '(the list is read from the folder at every call)')
ALL = os.environ.get('CH22_ALLDATA', '/home/claude/tessdata_fast_all')
if os.path.isdir(ALL):
    L = tess.get_languages(config='--tessdata-dir ' + ALL); sz = sum(os.path.getsize(os.path.join(ALL, f)) for f in os.listdir(ALL) if f.endswith('.traineddata')); sc = sum(os.path.getsize(os.path.join(ALL, 'script', f)) for f in os.listdir(os.path.join(ALL, 'script')))
    print('all the packs of the tessdata_fast repository (commit 87416418, 2024-08-01):', len(L), 'codes; first ten', L[:10], ' last ten', L[-10:])
    print('  the book prints for the first ten', "['afr', 'amh', 'ara', 'asm', 'aze', 'aze_cyrl', 'bel', 'ben', 'bod', 'bos']", L[:10] == ['afr', 'amh', 'ara', 'asm', 'aze', 'aze_cyrl', 'bel', 'ben', 'bod', 'bos'], ' and for the last ten', L[-10:] == ['ton', 'tur', 'uig', 'ukr', 'urd', 'uzb', 'uzb_cyrl', 'vie', 'yid', 'yor'])
    print('  codes that are not three letters:', [x for x in L if len(x) != 3], ' osd and equ among them:', 'osd' in L, 'equ' in L, ' script models (a capital letter, left out of the list):', len(os.listdir(os.path.join(ALL, 'script'))))
    print('  size of the %d language files: %d bytes; with the script folder %d bytes (the book says about 600MB for all languages)' % (len(L), sz, sz + sc))
else: print('NOT EXECUTED: the tessdata_fast repository is not cloned at', ALL)
BOOKJ = ["第 5 剖 私が自分の労苦の成果を目の当たりにしたのは、11 月の芝鬱な夜でした。 ほとんど苦", "痛に等しい不安を抱えながら、 私は足元に横たわる生命のないものに存在の輝きを吹き込むこ"]
BOOKJL = ["だ有目、 しわが寄った顔色、 そしてまっすぐな黒い大と、 より恐ろしいコントラストを形成した", "だけでした。"]
img = Image.open('frankenstein_jpn.png'); print('frankenstein_jpn.png:', img.size, img.mode)
j = tess.image_to_string(img, lang='jpn'); jl = [l for l in j.split('\n') if l.strip()]
print('lang=jpn: lines', len(jl), 'characters', len(j.replace('\n', '')), ' first line:', jl[0])
print('  first two lines equal the book:', jl[:2] == BOOKJ, ' last two lines equal the book:', jl[-2:] == BOOKJL)
print('  character error rate of the first line against the book\'s printed first line:', cer(BOOKJ[0], jl[0]), ' of the second:', cer(BOOKJ[1], jl[1]))
print('  the book prints 第 5 剖 for the heading; here:', jl[0][:5], ' and 芝鬱 for 憂鬱; here:', re.search(r'月 ?の(.)鬱', jl[0]).group(1))
e = tess.image_to_string(img, lang='eng'); el = [l for l in e.split('\n') if l.strip()]
print('lang=eng (wrong): lines', len(el), ' first line:', el[0])
print('  share of characters that are letters A-Za-z:', round(sum(c.isalpha() and c.isascii() for c in e) / max(1, len(e.replace('\\n', ''))), 2), ' Japanese characters in the result:', sum(ord(c) > 0x2E80 for c in e))
print('  the book prints BS FABADOABOMEE as the gibberish of its first line; here the first line begins:', el[0][:12])
print('lang=jpn on the same image takes', end=' '); t0 = time.time(); tess.image_to_string(img, lang='jpn'); a = time.time() - t0; t0 = time.time(); tess.image_to_string(img, lang='eng'); b = time.time() - t0
print('%.1f s; lang=eng takes %.1f s' % (a, b))
# text whose letters are known
JP = '吾輩は猫である。名前はまだ無い。どこで生れたかとんと見当がつかぬ。'
def jpimg(text, px=36):
    f = ImageFont.truetype(FONTS['jp'], px); im = Image.new('L', (int(px * len(text)) + 40, px * 2), 255); ImageDraw.Draw(im).text((20, px // 2), text, font=f, fill=0); return im
ji = jpimg(JP)
for lg in ('jpn', 'eng', 'eng+jpn', 'jpn+eng'):
    print('generated Japanese line, lang=%-8s ->' % lg, repr(norm(tess.image_to_string(ji, lang=lg, config='--psm 7'))), ' CER', cer(JP.replace('', ' ').strip().replace(' ', ''), tess.image_to_string(ji, lang=lg, config='--psm 7').replace(' ', '')))
MIX = 'The cat is 猫 and the dog is 犬 today'
f = ImageFont.truetype(FONTS['jp'], 40); mi = Image.new('L', (1000, 90), 255); ImageDraw.Draw(mi).text((20, 20), MIX, font=f, fill=0)
for lg in ('eng', 'jpn', 'eng+jpn', 'jpn+eng'):
    o = tess.image_to_string(mi, lang=lg, config='--psm 7'); print('mixed line, lang=%-8s ->' % lg, repr(o.strip()), ' CER', cer(MIX, o.replace(' ', ' ')))
LINES = {'fra': 'Où êtes-vous allé après la fête ? Les œufs brûlés ont été mangés.', 'deu': 'Die Größe der Straße und die Übung machen das Mädchen schön.',
         'tur': 'Çocuğun şeker istediğini söyledi; İstanbul’da ışık ve öğretmen.', 'rus': 'Съешь же ещё этих мягких французских булок, да выпей чаю.'}
for lg, t in LINES.items():
    f = ImageFont.truetype(FONTS['sans'], 32); im = Image.new('L', (int(f.getlength(t)) + 40, 80), 255); ImageDraw.Draw(im).text((20, 20), t, font=f, fill=0)
    a = tess.image_to_string(im, lang='eng', config='--psm 7'); b = tess.image_to_string(im, lang=lg, config='--psm 7')
    print('%s: lang=eng CER %s %r | lang=%s CER %s %r' % (lg, cer(t, a), norm(a), lg, cer(t, b), norm(b)))
print('a pack that is not installed:', err(lambda: tess.image_to_string(Image.new('L', (50, 50), 255), lang='xyz')))
im1, t1 = render(px=24); a = tess.image_to_string(im1, lang='eng+xyz'); print('one of two packs missing (eng+xyz) on a page of known text: no exception, CER', cer(t1, a), '- the complaint of Tesseract goes to the error stream that pytesseract does not show')
print('a name written the book\'s way, not a code (lang=Japanese):', err(lambda: tess.image_to_string(Image.new('L', (50, 50), 255), lang='Japanese')))
print('data file sizes in bytes:', {f: os.path.getsize(os.path.join(os.environ.get('TESSDATA_PREFIX', '/usr/share/tesseract-ocr/5/tessdata'), f)) for f in sorted(os.listdir(os.environ.get('TESSDATA_PREFIX', '/usr/share/tesseract-ocr/5/tessdata'))) if f.endswith('.traineddata')})
'''
HURTS = HEAD + r'''# Chapter 22, "Preprocessing an Image": how the character error rate moves with the size, the font, the tilt, the noise, the contrast, the colours and the margin of a page of known text.
print('Tesseract', tess.get_tesseract_version(), ' pytesseract', md.version('pytesseract'), ' Pillow', md.version('pillow'), ' text of', len(norm(TEXT)), 'characters; every number is a character error rate (0 = perfect, 1 = nothing right)')
def row(label, **k):
    im, truth = render(**k); out = ocr(im); print('  %-34s %-12s CER %-7s %s' % (label, str(im.size), cer(truth, out), repr(norm(out))[:48])); return cer(truth, out)
print('size of the letters (DejaVu Sans, pixels per em):')
for px in (6, 8, 10, 12, 16, 24, 40, 64): row('%d px' % px, px=px)
print('font:')
for f in ('sans', 'serif', 'mono', 'bold', 'roman', 'script'): row(f, font=f)
print('tilt (degrees, white corners):')
for r in (0, 1, 2, 3, 4, 5, 7, 10, 15, 30, 90): row('rotated %d' % r, rot=r)
print('noise (Gaussian, standard deviation in grey levels):')
for n in (0, 30, 40, 50, 60, 80): row('noise %d' % n, noise=n)
print('colours:')
row('black on white'); row('white on black', fg=255, bg=0); row('dark grey on light grey', fg=120, bg=170); row('mid grey on grey (fg 150, bg 190)', fg=150, bg=190); row('fg 170, bg 190', fg=170, bg=190)
print('margin around the text (pad in pixels):')
for p in (0, 2, 5, 20): row('pad %d' % p, pad=p)
print('declared resolution (Tesseract reads the dpi of the file or the --dpi option; with none it estimates it):')
d = wd(); im, truth = render(px=10)
for dpi in (None, 70, 150, 300, 600):
    if dpi: im.save('page.png', dpi=(dpi, dpi))
    else: im.save('page.png')
    o = tess.image_to_string('page.png'); o2 = tess.image_to_string(im, config='--dpi %d' % dpi) if dpi else None
    print('  10 px letters, PNG file with dpi %-5s CER %-7s | PIL image with --dpi %-5s CER %s' % (dpi, cer(truth, o), dpi, cer(truth, o2) if o2 is not None else '-'))
'''
CV = HEAD + SHIPPED + r'''# Chapter 22, "Preprocessing an Image": the steps of the book's list, done with Pillow, NumPy and OpenCV, and the character error rate before and after, on pages of known text and on the book's frankenstein.png.
import cv2
d = wd(); shipped(d)
print('Tesseract', tess.get_tesseract_version(), ' OpenCV', cv2.__version__, ' NumPy', np.__version__)
def gray(im): return im.convert('L')
def otsu(im): return Image.fromarray(cv2.threshold(np.asarray(gray(im)), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1])
def fixed(im, t=127): return Image.fromarray(cv2.threshold(np.asarray(gray(im)), t, 255, cv2.THRESH_BINARY)[1])
def scale(im, k): return im.resize((im.width * k, im.height * k), Image.Resampling.LANCZOS)
def median(im, k=3): return Image.fromarray(cv2.medianBlur(np.asarray(gray(im)), k))
def border(im, n=20): return ImageOps.expand(gray(im), border=n, fill=255)
def invert_if_dark(im):
    g = gray(im); return ImageOps.invert(g) if np.asarray(g).mean() < 128 else g
def skew_angle(im):
    """the angle at which the sum of every row of the dark pixels has the largest variance, searched from -20 to 20 degrees in steps of 0.5"""
    a = 255 - np.asarray(gray(im).resize((im.width // 2, im.height // 2)));  best = (-1, 0)
    for ang in np.arange(-20, 20.5, 0.5):
        r = np.asarray(Image.fromarray(a).rotate(float(ang), resample=Image.Resampling.BILINEAR)).sum(axis=1).astype(float); v = r.var()
        if v > best[0]: best = (v, float(ang))
    return best[1]
def deskew(im):
    a = skew_angle(im); return gray(im).rotate(a, expand=True, fillcolor=255, resample=Image.Resampling.BICUBIC), a
def run(label, im, truth, **k):
    o = ocr(im, **k); c = cer(truth, o); print('  %-40s CER %s' % (label, c)); return c
print('small letters (8 px): gray, scaled up, scaled and thresholded')
im, t = render(px=8); run('as rendered', im, t); run('Lanczos x2', scale(im, 2), t); run('Lanczos x3', scale(im, 3), t); run('Lanczos x4', scale(im, 4), t); run('x3 then Otsu', otsu(scale(im, 3)), t)
print('tilted page: found angle and CER after deskew')
for r in (3, 5, 10, 30):
    im, t = render(rot=r); out, a = deskew(im); print('  rotated %d: skew found %+.1f' % (r, a), end=''); run('', out, t)
print('noisy page (std 60 and 80): median filter, threshold')
for n in (60, 80):
    im, t = render(noise=n); print(' noise', n); run('as rendered', im, t); run('median 3', median(im, 3), t); run('median 5', median(im, 5), t); run('Otsu', otsu(im), t); run('median 3 then Otsu', otsu(median(im, 3)), t)
print('a dark scanner border and an inverted page')
im, t = render(); bd = ImageOps.expand(im, border=60, fill=0); run('dark border 60 px around', bd, t); run('same with border cropped by 60', bd.crop((60, 60, bd.width - 60, bd.height - 60)), t)
inv, t = render(fg=255, bg=0); run('white on black as it is', inv, t); run('inverted by the program', invert_if_dark(inv), t)
print('the book\'s frankenstein.png (an 1831 page, the printed text read from the image)')
TRUTH = ("THE MODERN PROMETHEUS. 43 CHAPTER V. IT was on a dreary night of November, that I beheld the accomplishment of my toils. With an anxiety that almost amounted to agony, "
         "I collected the instruments of life around me, that I might infuse a spark of being into the lifeless thing that lay at my feet. It was already one in the morning ; "
         "the rain pattered dismally against the panes, and my candle was nearly burnt out, when, by the glimmer of the half-extinguished light, I saw the dull yellow eye of the creature open ; "
         "it breathed hard, and a convulsive motion agitated its limbs.")
fr = Image.open('frankenstein.png').convert('RGB')
def first(o):
    m = re.search(r'V\.?\s+(\S+)', norm(o)); return m.group(1) if m else None
for label, im in (('as shipped', fr), ('grey', gray(fr)), ('Otsu', otsu(fr)), ('fixed 127', fixed(fr)), ('fixed 100', fixed(fr, 100)), ('scaled x2', scale(fr, 2)), ('scaled x2 then Otsu', otsu(scale(fr, 2))), ('median 3', median(fr)), ('border 20', border(fr))):
    o = ocr(im); print('  %-24s CER %-7s first word of the chapter: %s' % (label, cer(TRUTH, o), first(o)))
print('mode of the shipped file:', fr0.mode if False else Image.open('frankenstein.png').mode, '(a palette image; the grey copy of it is a different picture to the engine)')
print('the shipped preprocess_ocr.py: compiles:', err(lambda: compile(open('preprocess_ocr.py').read(), 'preprocess_ocr.py', 'exec'))[0], ' run as a program:', end=' ')
r = subprocess.run([sys.executable, 'preprocess_ocr.py'], capture_output=True, text=True, cwd=d); print(r.returncode, r.stderr.strip().splitlines()[-1])
'''
SEG = HEAD + r'''# Chapter 22, "Preprocessing an Image" (columns) and the page segmentation modes of Tesseract: what --psm changes on a line, a word, a digit, scattered labels and two columns.
print('Tesseract', tess.get_tesseract_version())
F = ImageFont.truetype(FONTS['roman'], 26)
def column(text, w=420):
    lines = wrap(text, F, w); im = Image.new('L', (w, 36 * len(lines) + 30), 255); d = ImageDraw.Draw(im)
    for i, l in enumerate(lines): d.text((0, 15 + 36 * i), l, font=F, fill=0)
    return im, ' '.join(lines)
A = 'The first column tells of a long journey by train across the northern plains in winter, with snow on every hill and smoke above every roof of the small villages along the line.'
B = 'The second column begins with the market of the town, where the baker sold bread and the clerk counted coins until the bell of the church rang twice and the square became empty.'
ca, ta = column(A); cb, tb = column(B)
def pair(gutter):
    h = max(ca.height, cb.height); im = Image.new('L', (ca.width + gutter + cb.width, h), 255); im.paste(ca, (0, 0)); im.paste(cb, (ca.width + gutter, 0)); return im
print('two columns, gutter in pixels: CER of the whole page with psm 3, and CER when each column is cut out and read alone (psm 6)')
for g in (2, 4, 6, 8, 12, 24):
    im = pair(g); whole = ocr(im); a = ocr(im.crop((0, 0, ca.width, im.height)), config='--psm 6'); b = ocr(im.crop((ca.width + g, 0, im.width, im.height)), config='--psm 6')
    print('  gutter %3d px: whole page %s lines %d | columns apart %s' % (g, cer(ta + ' ' + tb, whole), len([l for l in whole.split('\n') if l.strip()]), cer(ta + ' ' + tb, a + ' ' + b)))
im = pair(8); o = ocr(im); print('with gutter 8 the first two lines of the page read:', [l for l in o.split('\n') if l.strip()][:2])
print('single line, single word, single digit, scattered labels: output of every mode (-- means no text)')
line, tl = render('The quick brown fox jumps over the lazy dog', font='roman', px=36, width=900, pad=20)
word, tw = render('Python', font='roman', px=60, width=300, pad=20)
digit, td = render('7', font='roman', px=90, width=120, pad=20)
sparse = Image.new('L', (700, 300), 255); sd = ImageDraw.Draw(sparse); SF = ImageFont.truetype(FONTS['roman'], 30)
for (x, y, t) in ((20, 20, 'Name'), (400, 40, 'Total'), (60, 150, 'Date'), (420, 200, 'Page 3'), (250, 100, 'Paid')): sd.text((x, y), t, font=SF, fill=0)
ts = 'Name Total Date Page 3 Paid'
def show(label, im, truth, modes):
    for m in modes:
        o = err(lambda: ocr(im, config='--psm %d' % m)); o = o[1] if o[0] == 'ok' else o[0]
        print('  %-18s psm %2d -> %-52s' % (label, m, repr(norm(o))[:52]))
show('line', line, tl, (3, 6, 7, 8, 13)); show('word', word, tw, (3, 7, 8, 10, 13)); show('digit', digit, td, (3, 7, 8, 10, 13)); show('scattered labels', sparse, ts, (3, 6, 11, 12))
print('mode 0 (orientation and script only) with image_to_string:', err(lambda: ocr(line, config='--psm 0')))
print('mode 2 and 14 (not in this build) with image_to_string:', err(lambda: ocr(line, config='--psm 2')), err(lambda: ocr(line, config='--psm 14')))
print('mode 1 (automatic with orientation and script detection) on the line image:', repr(norm(ocr(line, config='--psm 1'))))
'''
INTERNALS = HEAD + SHIPPED + r'''# Chapter 22, "Installing Tesseract and PyTesseract" and "OCR Fundamentals": what pytesseract runs, what it can return, and what it raises when the program, the language or the time is missing.
d = wd(); shipped(d)
print('pytesseract', md.version('pytesseract'), ' requires:', md.requires('pytesseract'), ' Python', sys.version.split()[0])
print('where the program is found: shutil.which("tesseract") =', shutil.which('tesseract'), ' version', tess.get_tesseract_version(), type(tess.get_tesseract_version()).__name__)
# the command line that pytesseract starts
calls = []; real = subprocess.Popen
class Spy(real):
    def __init__(self, args, *a, **k): calls.append([os.path.basename(args[0])] + [re.sub(r'tess_\w+', 'tess_XXXX', x) for x in args[1:]]); super().__init__(args, *a, **k)
subprocess.Popen = Spy
img = Image.open('frankenstein.png'); tess.image_to_string(img); tess.image_to_string(img, lang='eng', config='--psm 6'); tess.image_to_data(img); tess.image_to_osd(img); tess.image_to_boxes(img); tess.image_to_pdf_or_hocr(img, extension='hocr')
subprocess.Popen = real
for c in calls: print('  runs:', ' '.join(c))
print('the image is handed over as a temporary file named tess_..._input.PNG and the answer is read from tess_....txt, which pytesseract deletes afterwards')
print('a path as a string is passed through unchanged (no copy made):', end=' ')
calls.clear(); subprocess.Popen = Spy; tess.image_to_string('frankenstein.png'); subprocess.Popen = real; print(calls[0][1:2])
print('an alpha channel is replaced by white before the file is written: transparent text on nothing reads as', repr(norm(ocr(Image.new('RGBA', (400, 100), (0, 0, 0, 0))))), '; black text with alpha 255 on RGBA reads', end=' ')
t = Image.new('RGBA', (500, 100), (0, 0, 0, 0)); ImageDraw.Draw(t).text((20, 30), 'Hello World', font=ImageFont.truetype(FONTS['sans'], 36), fill=(0, 0, 0, 255)); print(repr(norm(ocr(t))))
print('what each function returns on frankenstein.png:')
s = tess.image_to_string(img); dd = tess.image_to_data(img); dc = tess.image_to_data(img, output_type=tess.Output.DICT); bx = tess.image_to_boxes(img); os_ = tess.image_to_osd(img); h = tess.image_to_pdf_or_hocr(img, extension='hocr'); pd_ = tess.image_to_pdf_or_hocr(img, extension='pdf')
print('  image_to_string', type(s).__name__, len(s), '| image_to_data', type(dd).__name__, len(dd.split('\n')), 'lines of 12 tab separated columns:', dd.split('\n')[0].replace('\t', ','))
print('  Output.DICT keys', list(dc), '| levels present', sorted(set(dc['level'])), '(1 page, 2 block, 3 paragraph, 4 line, 5 word)')
print('  image_to_boxes', type(bx).__name__, len(bx.strip().split('\n')), 'boxes (one per character), first:', bx.split('\n')[0], '| image_to_osd:', os_.replace('\n', ' | ').strip(' |'))
print('  hocr', type(h).__name__, 'bytes', len(h), 'ocrx_word elements:', h.count(b'ocrx_word'), '| pdf', type(pd_).__name__, 'starts', pd_[:8], 'bytes', len(pd_))
print('  bytes and dict forms:', type(tess.image_to_string(img, output_type=tess.Output.BYTES)).__name__, type(tess.image_to_string(img, output_type=tess.Output.DICT)).__name__, list(tess.image_to_string(img, output_type=tess.Output.DICT)))
print('the box of a character has its origin at the bottom left of the image (y grows upward), unlike Pillow: first character', bx.split('\n')[1], 'of a', img.size, 'image')
print('errors:')
print('  a time limit that is too short:', err(lambda: tess.image_to_string(img, timeout=0.01)))
print('  an object that is not an image:', err(lambda: tess.image_to_string(b'not an image')))
print('  a file that does not exist:', err(lambda: tess.image_to_string('no-such-file.png')))
print('  a path to a text file:', (open('notes.txt', 'w').write('aaaa\nbbbb\n'), err(lambda: tess.image_to_string('notes.txt')))[1])
print('  lang that is not a code:', err(lambda: tess.image_to_string(img, lang='english')))
print('  osd on a blank image:', err(lambda: tess.image_to_osd(Image.new('L', (100, 100), 255))))
print('  psm 0 with image_to_string / image_to_osd works:', err(lambda: tess.image_to_string(img, config='--psm 0'))[0], err(lambda: tess.image_to_osd(img))[0])
# a child that cannot find the program
code = "import pytesseract as t, sys\nfrom PIL import Image\ntry:\n    t.image_to_string(Image.new('L', (20, 20)))\nexcept BaseException as e:\n    print(type(e).__name__, '|', e, '| subclass of EnvironmentError:', isinstance(e, EnvironmentError))\n"
r = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, env={'PATH': '/nonexistent', 'HOME': d}); print('PATH without tesseract:', r.stdout.strip())
code2 = code.replace("t.image_to_string(", "setattr(t.pytesseract, 'tesseract_cmd', '/usr/bin/tesseract') or t.image_to_string(")
r = subprocess.run([sys.executable, '-c', code2], capture_output=True, text=True, env={'PATH': '/nonexistent', 'HOME': d}); print('same, with pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract" set first:', r.stdout.strip() or 'no exception (the text of a blank image is empty)')
'''
ENGINES = HEAD + SHIPPED + r'''# Chapter 22, "Fixing Mistakes" and its remark that "the exact results may vary as the language packs are updated": the same images through three Tesseract versions and three kinds of language data.
d = wd(); shipped(d)
ENG = {'4.1.1': '/home/claude/tesseract-4.1.1/bin/tesseract', '5.3.4': '/usr/bin/tesseract', '5.5.3': '/home/claude/tesseract-5.5.3/bin/tesseract'}
DATA = {'fast': '/home/claude/tessdata_fast', 'best': '/home/claude/tessdata_best', 'legacy+lstm': '/home/claude/tessdata_legacy'}
have = {v: p for v, p in ENG.items() if os.path.exists(p)}; hd = {k: p for k, p in DATA.items() if os.path.exists(p)}
if not have or not hd: print('NOT EXECUTED: the Tesseract builds or the language data are not on this machine'); sys.exit(0)
for k, p in hd.items(): print('data %-12s eng.traineddata %9d bytes sha256 %s' % (k, os.path.getsize(p + '/eng.traineddata'), hashlib.sha256(open(p + '/eng.traineddata', 'rb').read()).hexdigest()[:12]))
print('the data of the apt package tesseract-ocr-eng 4.1.0 (Ubuntu 24.04):', hashlib.sha256(open('/usr/share/tesseract-ocr/5/tessdata/eng.traineddata', 'rb').read()).hexdigest()[:12], '(equal to fast:', open('/usr/share/tesseract-ocr/5/tessdata/eng.traineddata', 'rb').read() == open(DATA['fast'] + '/eng.traineddata', 'rb').read(), ')')
TRUTH = ("THE MODERN PROMETHEUS. 43 CHAPTER V. IT was on a dreary night of November, that I beheld the accomplishment of my toils. With an anxiety that almost amounted to agony, "
         "I collected the instruments of life around me, that I might infuse a spark of being into the lifeless thing that lay at my feet. It was already one in the morning ; "
         "the rain pattered dismally against the panes, and my candle was nearly burnt out, when, by the glimmer of the half-extinguished light, I saw the dull yellow eye of the creature open ; "
         "it breathed hard, and a convulsive motion agitated its limbs.")
fr = Image.open('frankenstein.png'); small, ts = render(px=8); mid, tm = render(px=24)
def first(o):
    m = re.search(r'V\.?\s+(\S+)', norm(o)); return m.group(1) if m else None
print('%-6s %-12s | frankenstein.png: CER, first word, last word | 8 px page CER | 24 px page CER (DejaVu Sans)' % ('engine', 'data'))
for v, p in have.items():
    tess.pytesseract.tesseract_cmd = p
    for k, dp in hd.items():
        os.environ['TESSDATA_PREFIX'] = dp
        r = err(lambda: (lambda o: (cer(TRUTH, o), first(o), norm(o).split(' ')[-2:-1][0] if norm(o) else None))(ocr(fr)))
        a = err(lambda: cer(ts, ocr(small))); b = err(lambda: cer(tm, ocr(mid)))
        print('%-6s %-12s | %-34s | %-8s | %s' % (v, k, r[1] if r[0] == 'ok' else r[0], a[1] if a[0] == 'ok' else a[0], b[1] if b[0] == 'ok' else b[0]))
print('legacy engine (--oem 0) needs the legacy data; with the fast data:')
for v, p in have.items():
    tess.pytesseract.tesseract_cmd = p
    for k in ('fast', 'legacy+lstm'):
        os.environ['TESSDATA_PREFIX'] = DATA[k]; r = err(lambda: cer(TRUTH, ocr(fr, config='--oem 0'))); print('  %-6s %-12s --oem 0: %s' % (v, k, r[1] if r[0] == 'ok' else r[1][:90]))
print('white text on black, which the book says to avoid:')
inv, ti = render(fg=255, bg=0)
for v, p in have.items():
    tess.pytesseract.tesseract_cmd = p; os.environ['TESSDATA_PREFIX'] = DATA['fast']; print('  %-6s fast: CER %s' % (v, cer(ti, ocr(inv))))
print('the Japanese heading line of the book image with the Japanese data of each kind (first 12 characters):')
jimg = Image.open('frankenstein_jpn.png')
for v, p in have.items():
    tess.pytesseract.tesseract_cmd = p
    for k in ('fast', 'best'):
        os.environ['TESSDATA_PREFIX'] = DATA[k]; o = [l for l in ocr(jimg, lang='jpn').split('\n') if l.strip()]; print('  %-6s %-5s %s ... %s lines' % (v, k, o[0][:30], len(o)))
'''
NAPS = HEAD + SHIPPED + r'''# Chapter 22, "The NAPS2 Scanner Application": the book's subprocess listing run as printed and with the Linux path, its arguments, and its mini language for the input, against the real NAPS2 console.
d = wd(); shipped(d)
if not shutil.which('naps2') or not shutil.which('pdftotext'): print('NOT EXECUTED: naps2 or pdftotext is not on the PATH'); sys.exit(0)
print('NAPS2 package:', subprocess.run(['dpkg-query', '-W', '-f', '${Package} ${Version}', 'naps2'], capture_output=True, text=True).stdout)
def pages(pdf): return int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
def text(pdf, p=None):
    a = ['pdftotext'] + (['-f', str(p), '-l', str(p)] if p else []) + [pdf, '-']; return subprocess.run(a, capture_output=True, text=True).stdout
TRUTH = ("THE MODERN PROMETHEUS. 43 CHAPTER V. IT was on a dreary night of November, that I beheld the accomplishment of my toils. With an anxiety that almost amounted to agony, "
         "I collected the instruments of life around me, that I might infuse a spark of being into the lifeless thing that lay at my feet. It was already one in the morning ; "
         "the rain pattered dismally against the panes, and my candle was nearly burnt out, when, by the glimmer of the half-extinguished light, I saw the dull yellow eye of the creature open ; "
         "it breathed hard, and a convulsive motion agitated its limbs.")
args = ['-i', 'frankenstein.png', '-o', 'output.pdf', '--install', 'ocr-eng', '--ocrlang', 'eng', '-n', '0', '-f', '-v']
print('the Windows path of the book on this machine:', err(lambda: subprocess.run([r'C:\Program Files\NAPS2\NAPS2.Console.exe'] + args, capture_output=True)))
print('the Linux path of the book (flatpak):', err(lambda: subprocess.run(['flatpak', 'run', 'com.naps2.Naps2', 'console'] + args, capture_output=True)))
naps2_path = ['naps2', 'console']   # the .deb package of naps2.com installs /usr/bin/naps2
t0 = time.time(); proc = subprocess.run(naps2_path + args, capture_output=True); dt = time.time() - t0
print('the book\'s call with naps2_path = [\'naps2\', \'console\']: returncode', proc.returncode, ' type of stdout', type(proc.stdout).__name__, )
vl = proc.stdout.decode().strip().splitlines(); print('  verbose output (the line about the ocr-eng component, "Installing ocr-eng..." the first time and "The specified component is already installed." later, left out):', [l for l in vl if 'ocr-eng' not in l and 'component' not in l], ' install line present:', len(vl) == 6)
print('  output.pdf: pages', pages('output.pdf'), ' bytes', os.path.getsize('output.pdf'), ' selectable text found by pdftotext:', len(norm(text('output.pdf'))), 'characters')
n = text('output.pdf'); p = ocr(Image.open('frankenstein.png'))
print('  CER of the PDF text against the page:', cer(TRUTH, n), ' CER of pytesseract with the apt Tesseract against the page:', cer(TRUTH, p), ' first words:', re.search(r'V\.?\s+(\S+)', norm(n)).group(1), re.search(r'V\.?\s+(\S+)', norm(p)).group(1))
r = subprocess.run(naps2_path + ['-i', 'frankenstein.png', '-o', 'output.pdf', '--ocrlang', 'eng', '-n', '0'], capture_output=True, text=True); print('the same call without -f when output.pdf exists: returncode', r.returncode, ' says:', r.stdout.strip())
print('the program NAPS2 runs for the text (read with strace):', end=' ')
if shutil.which('strace'):
    r = subprocess.run(['strace', '-f', '-e', 'trace=openat,execve', '-o', 'st.log'] + naps2_path + ['-i', 'frankenstein.png', '-o', 'o2.pdf', '--ocrlang', 'eng', '-n', '0', '-f'], capture_output=True)
    log = open('st.log').read(); ex = re.findall(r'execve\("(/usr/lib/naps2/[^"]*tesseract)"', log); dt = sorted(set(re.findall(r'openat\([^"]*"([^"]*traineddata)"[^)]*\) = \d', log)))
    print(ex[:1], 'with', dt); print('  its version:', subprocess.run([ex[0], '--version'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout.splitlines()[0])
else: print('NOT EXECUTED: strace is not installed')
print('the apt Tesseract of pytesseract is', tess.get_tesseract_version(), 'so the two programs differ; the command line of NAPS2 passes -l eng -c tessedit_create_hocr=1 -c hocr_font_info=1 (the hOCR output becomes the invisible text of the PDF)')
# the mini language of -i
F = ImageFont.truetype(FONTS['sans'], 90)
def label(t):
    im = Image.new('L', (700, 300), 255); ImageDraw.Draw(im).text((40, 90), t, font=F, fill=0); return im
for t in ('cat', 'dog', 'moose'): label(t).save(t + '.png')
def mkpdf(name, labels): ims = [label(t) for t in labels]; ims[0].save(name, save_all=True, append_images=ims[1:])
mkpdf('spam.pdf', ['spam%d' % i for i in range(7)]); mkpdf('eggs.pdf', ['eggs%d' % i for i in range(3)])
print('made spam.pdf (7 pages spam0 to spam6), eggs.pdf (3 pages eggs0 to eggs2), cat.png, dog.png, moose.png; reading the result pages back with pdftotext')
for spec in ('cat.png;dog.png;moose.png', 'spam.pdf[0];spam.pdf[5];eggs.pdf', 'spam.pdf[0:2];eggs.pdf[-1]', 'spam.pdf[-2:]', 'spam.pdf[1:6:2]', 'dog.png;cat.png;dog.png'):
    out = 'in.pdf'; r = subprocess.run(naps2_path + ['-i', spec, '-o', out, '--ocrlang', 'eng', '-n', '0', '-f'], capture_output=True, text=True)
    if r.returncode or not os.path.exists(out): print('  -i %-36r returncode %d %s' % (spec, r.returncode, (r.stdout + r.stderr).strip()[:100])); continue
    print('  -i %-36r pages %d: %s' % (spec, pages(out), [norm(text(out, i)) for i in range(1, pages(out) + 1)])); os.remove(out)
'''
PDFS = HEAD + SHIPPED + r'''# Chapter 22, "The NAPS2 Scanner Application" (searchable PDFs) and its pointer to ocrmypdf: the same page made into a PDF with embedded text three ways, and read back.
d = wd(); shipped(d)
if not shutil.which('pdftotext') or not shutil.which('pdftoppm'): print('NOT EXECUTED: poppler-utils (pdftotext, pdftoppm) is not on the PATH'); sys.exit(0)
OMP = os.environ.get('CH22_OCRMYPDF', '/home/claude/venv314_ch22_ocrmypdf/bin/ocrmypdf')
TRUTH = ("THE MODERN PROMETHEUS. 43 CHAPTER V. IT was on a dreary night of November, that I beheld the accomplishment of my toils. With an anxiety that almost amounted to agony, "
         "I collected the instruments of life around me, that I might infuse a spark of being into the lifeless thing that lay at my feet. It was already one in the morning ; "
         "the rain pattered dismally against the panes, and my candle was nearly burnt out, when, by the glimmer of the half-extinguished light, I saw the dull yellow eye of the creature open ; "
         "it breathed hard, and a convulsive motion agitated its limbs.")
def pdftext(f): return subprocess.run(['pdftotext', f, '-'], capture_output=True, text=True).stdout
def info(f): i = subprocess.run(['pdfinfo', f], capture_output=True, text=True).stdout; return {k: (re.search(k + r':\s+(.*)', i).group(1).strip() if re.search(k + r':\s+(.*)', i) else None) for k in ('Pages', 'Producer', 'PDF version')}
img = Image.open('frankenstein.png').convert('RGB')
img.save('image_only.pdf', resolution=150)
print('1. Pillow saves the picture as a PDF (resolution=150):', info('image_only.pdf'), ' characters pdftotext finds:', len(norm(pdftext('image_only.pdf'))), '(a picture of text, nothing to select or search)')
b = tess.image_to_pdf_or_hocr(img, extension='pdf'); open('pytess.pdf', 'wb').write(b)
print('2. pytesseract.image_to_pdf_or_hocr(img, extension="pdf"):', type(b).__name__, len(b), 'bytes', info('pytess.pdf'), ' characters pdftotext finds:', len(norm(pdftext('pytess.pdf'))), ' CER of that text against the page:', cer(TRUTH, pdftext('pytess.pdf')))
bb = subprocess.run(['pdftotext', '-bbox', 'pytess.pdf', '-'], capture_output=True, text=True).stdout; print('   word boxes in the text layer (pdftotext -bbox):', bb.count('<word'), ' first:', re.search(r'<word [^>]*>[^<]*</word>', bb).group(0)[:100])
subprocess.run(['pdftoppm', '-r', '150', '-png', 'image_only.pdf', 'render'], check=True); png = sorted(f for f in os.listdir('.') if f.startswith('render'))[0]
im2 = Image.open(png); print('3. pdftoppm -r 150 renders the page of image_only.pdf to', png, im2.size, im2.mode, 'dpi in the PNG:', tuple(round(x) for x in im2.info.get('dpi', ())), ' OCR of the rendered page: CER', cer(TRUTH, ocr(im2)))
print('4. ocrmypdf', end=' ')
if not os.path.exists(OMP): print('NOT EXECUTED: ocrmypdf is not installed at', OMP)
else:
    print(subprocess.run([OMP, '--version'], capture_output=True, text=True).stdout.strip(), '- the checks need a Tesseract on the PATH:', shutil.which('tesseract'))
    def om(*a):
        fo = tempfile.TemporaryFile('w+'); fe = tempfile.TemporaryFile('w+'); r = subprocess.run([OMP] + list(a), stdout=fo, stderr=fe, stdin=subprocess.DEVNULL, timeout=300); fe.seek(0); e = fe.read().strip().splitlines(); return r.returncode, (e[-1][:150] if e else '')
    print('   image with no resolution in its metadata:', om('frankenstein.png', 'a.pdf'), os.path.exists('a.pdf'))
    print('   the same with --image-dpi 150:', om('--image-dpi', '150', 'frankenstein.png', 'b.pdf'), info('b.pdf'), 'text characters', len(norm(pdftext('b.pdf'))), 'CER', cer(TRUTH, pdftext('b.pdf')))
    print('   a PDF that already has text, without options:', om('b.pdf', 'c.pdf'), os.path.exists('c.pdf'))
    print('   with --skip-text:', om('--skip-text', 'b.pdf', 'd.pdf'), ' with --force-ocr:', om('--force-ocr', 'b.pdf', 'e.pdf'))
    print('   the image-only PDF of step 1 (it has a resolution of 150):', om('image_only.pdf', 'f.pdf'), 'CER', cer(TRUTH, pdftext('f.pdf')), ' with --sidecar the text goes to a file too:', om('--sidecar', 'f.txt', '--force-ocr', 'image_only.pdf', 'g.pdf'), len(norm(open('f.txt').read())), 'characters')
'''
SCREEN = HEAD + SHIPPED + r'''# Chapter 22, "Practice Program: Browser Text Scraper": the template of ocrscreen.py completed, run against a real screen (a virtual X display with the book's frankenstein.png shown in a window), twice, so that the appending can be seen.
d = wd(); shipped(d)
if not (shutil.which('Xvfb') and shutil.which('display') and shutil.which('scrot')): print('NOT EXECUTED: Xvfb, ImageMagick display or scrot is not on the PATH'); sys.exit(0)
TEMPLATE = """import pyautogui
import pytesseract as tess

# The coordinates for the text portion. Change as needed:
LEFT = %d
TOP = %d
RIGHT = %d
BOTTOM = %d

# Capture a screenshot:
img = pyautogui.screenshot()

# Crop the screenshot to the text portion:
img = img.crop((LEFT, TOP, RIGHT, BOTTOM))

# Run OCR on the cropped image:
text = tess.image_to_string(img)

# Add the OCR text to the end of output.txt:
with open('output.txt', 'a', encoding='utf-8') as f:
    f.write(text)
print('screenshot', pyautogui.size(), 'cropped to', img.size, 'and', len(text), 'characters appended')
"""
TRUTH = ("THE MODERN PROMETHEUS. 43 CHAPTER V. IT was on a dreary night of November, that I beheld the accomplishment of my toils. With an anxiety that almost amounted to agony, "
         "I collected the instruments of life around me, that I might infuse a spark of being into the lifeless thing that lay at my feet. It was already one in the morning ; "
         "the rain pattered dismally against the panes, and my candle was nearly burnt out, when, by the glimmer of the half-extinguished light, I saw the dull yellow eye of the creature open ; "
         "it breathed hard, and a convulsive motion agitated its limbs.")
disp = ':%d' % (120 + os.getpid() % 60); xauth = os.path.join(d, 'empty.Xauthority'); open(xauth, 'w').close()
xv = subprocess.Popen(['Xvfb', disp, '-screen', '0', '1280x1024x24'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(3)
env = dict(os.environ, DISPLAY=disp, XDG_SESSION_TYPE='x11', XAUTHORITY=xauth)
def run(args):
    fo = tempfile.TemporaryFile('w+'); fe = tempfile.TemporaryFile('w+'); r = subprocess.run([sys.executable, '-W', 'ignore', 'ocrscreen.py'], stdout=fo, stderr=fe, stdin=subprocess.DEVNULL, env=env, timeout=120); fo.seek(0); fe.seek(0)
    return r.returncode, [l for l in fo.read().strip().splitlines() if 'xauth' not in l.lower()]
try:
    viewer = subprocess.Popen(['display', '-geometry', '+0+0', 'frankenstein.png'], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(3)
    print('the window shows frankenstein.png, 1130 x 672, at the top left of a 1280 x 1024 screen')
    open('ocrscreen.py', 'w').write(TEMPLATE % (400, 200, 1000, 800))
    print('run 1, the constants of the template (400, 200, 1000, 800):', run(None)); a = open('output.txt', encoding='utf-8').read(); print('  output.txt now:', len(a), 'characters; first lines:', a.split('\n')[:2], ' CER against the whole page:', cer(TRUTH, a))
    open('ocrscreen.py', 'w').write(TEMPLATE % (0, 0, 1130, 672)); os.remove('output.txt')
    print('run 2, the constants set to the text portion (0, 0, 1130, 672):', run(None)); b = open('output.txt', encoding='utf-8').read(); print('  output.txt now:', len(b), 'characters; CER against the whole page:', cer(TRUTH, b), ' equal to OCR of the file itself:', b == ocr(Image.open('frankenstein.png')))
    print('run 3, the same again (the next scrolled page in the real use):', run(None)); c = open('output.txt', encoding='utf-8').read(); print('  output.txt now:', len(c), 'characters, which is', len(b), '* 2 =', 2 * len(b), ':', len(c) == 2 * len(b), ' lines in the file:', len(c.split('\n')))
    r = subprocess.run([sys.executable, '-W', 'ignore', '-c', 'import pyautogui'], capture_output=True, text=True, env={k: v for k, v in env.items() if k != 'DISPLAY'}); print('the same import with no DISPLAY:', r.returncode, r.stderr.strip().splitlines()[-1])
    r = subprocess.run([sys.executable, '-W', 'ignore', '-c', 'import pyautogui; pyautogui.screenshot()'], capture_output=True, text=True, env={k: v for k, v in env.items() if k != 'XDG_SESSION_TYPE'}); print('a screenshot without XDG_SESSION_TYPE=x11 (scrot is installed):', r.returncode, r.stderr.strip().splitlines()[-1][:110] if r.returncode else 'ok')
    r = subprocess.run([sys.executable, '-W', 'ignore', '-c', 'import pyautogui'], capture_output=True, text=True, env={k: v for k, v in env.items() if k != 'XAUTHORITY'}, cwd=d); print('the import with the display but no ~/.Xauthority file:', r.returncode, r.stderr.strip().splitlines()[-1].replace(os.path.expanduser('~'), '~')[:110] if r.returncode else 'ok')
finally:
    subprocess.run(['pkill', '-x', 'display-im6.q16']); xv.terminate(); xv.wait()
'''
HYPHENS = HEAD + SHIPPED + r'''# Chapter 22, "Preprocessing an Image" (what to expect of the text) and "Fixing Mistakes Using Large Language Models": hyphens, white space and digits in what OCR returns, and what code can and cannot repair.
d = wd(); shipped(d)
text = ocr(Image.open('ocr-example.png')); words = set(open('/usr/share/dict/words', encoding='utf-8').read().split()) if os.path.exists('/usr/share/dict/words') else None
if words is None: print('NOT EXECUTED: no /usr/share/dict/words on this machine (the package wamerican)'); sys.exit(0)
low = {w.lower() for w in words}
print('line-end hyphens in the OCR text of ocr-example.png:', re.findall(r'(\w+)-\n(\w+)', text))
def undo(t, strict=True):
    """joins a word broken by a hyphen at the end of a line; with strict=True only when the joined word is in the word list, otherwise the hyphen is kept"""
    def f(m):
        j = m.group(1) + m.group(2)
        return j if (not strict or j.lower() in low) else m.group(1) + '-' + m.group(2)
    return re.sub(r'(\w+)-\n(\w+)', f, t)
print('every hyphen undone:', len(re.findall(r'-\n', text)), 'line-end hyphens, left after strict undo:', len(re.findall(r'-\n', undo(text))), '; joined words:', [a + b for a, b in re.findall(r'(\w+)-\n(\w+)', text) if (a + b).lower() in low])
sample = 'The well-\nknown author of the self-\ncontained programs wrote the straight-\nforward code.'
print('a text with two real compounds broken at the line end:'); print('  naive undo :', repr(undo(sample, strict=False))); print('  strict undo:', repr(undo(sample)))
para = re.sub(r'(?<!\n)\n(?!\n)', ' ', undo(text)); print('paragraphs on one line (single line breaks turned to spaces):', len([p for p in para.split('\n\n') if p.strip()]), 'paragraph blocks, first 70 characters:', repr(para[:70]))
print('white space: runs of two or more spaces in the OCR text:', len(re.findall(r'  +', text)), ' tabs:', text.count('\t'), ' trailing spaces at line ends:', len(re.findall(r' \n', text)), ' the text of a heading in the image, "How to Design Small Programs":', 'How to Design Small Programs' in text, '(its bold typeface and size are not in the string)')
print('numbers and letters that look alike, on a small invoice-like line (DejaVu Sans, pixels per em):')
LINE = 'Invoice 1058 Total 1,000.00 Order O8l0 Ref lI1| 0O0'
for px in (9, 12, 18, 32):
    im, t = render(LINE, px=px, width=900, pad=10); o = norm(ocr(im, config='--psm 7')); print('  %2d px: %-58r CER %s' % (px, o, cer(t, o)))
print('digits only image (a bill in DejaVu Sans Mono, 14 px) read with and without a whitelist:')
D = '0123456789 0O8B 5S 1l 2Z 6G'; im, t = render(D, font='mono', px=14, width=500, pad=10)
print('  plain       :', repr(norm(ocr(im, config='--psm 7'))), ' truth', repr(D)); print('  digits only :', repr(norm(ocr(im, config='--psm 7 -c tessedit_char_whitelist=0123456789 '))))
print('the book\'s sample prompt for a large language model is', len('The following is the text output from an OCR scan. Correct any spacing, missing characters, or inaccurately recognized characters from it. Do not correct spelling or grammar mistakes that exist in the original text. Put paragraphs on a single line and undo the hyphenated words that are broken across the end of a line. Only give the corrected text without explaining what OCR is or any other preface. Here is the text:'), 'characters long; sending it needs an online service with a key or a local model')
print('NOT EXECUTED: the large language model step of the chapter (no key for an online service, no local model on this machine)')
'''
PROGRAMS = {
    'ocrFundamentals_v1_0_0.py': (OCR, (), True),
    'frankensteinPage_v1_0_0.py': (FRANK, (), True),
    'languagesAndPacks_v1_0_0.py': (LANGS, (), True),
    'whatHurtsAccuracy_v1_0_0.py': (HURTS, (), False),
    'preprocessingWithOpenCV_v1_0_0.py': (CV, (), True),
    'segmentationModes_v1_0_0.py': (SEG, (), False),
    'pytesseractInternals_v1_0_0.py': (INTERNALS, (), True),
    'enginesAndData_v1_0_0.py': (ENGINES, (), True),
    'naps2Pdf_v1_0_0.py': (NAPS, (), True),
    'pdfRoutes_v1_0_0.py': (PDFS, (), True),
    'ocrscreenOnXvfb_v1_0_0.py': (SCREEN, (), True),
    'hyphensAndDigits_v1_0_0.py': (HYPHENS, (), True),
}
STAND_IN = {'ocrscreenOnXvfb_v1_0_0.py': 'a virtual display (Xvfb) with the real ImageMagick display; nobody sees the screen'}
FIXTURE_BASED = ['ocrFundamentals_v1_0_0.py', 'frankensteinPage_v1_0_0.py', 'languagesAndPacks_v1_0_0.py', 'preprocessingWithOpenCV_v1_0_0.py', 'pytesseractInternals_v1_0_0.py', 'enginesAndData_v1_0_0.py', 'naps2Pdf_v1_0_0.py', 'pdfRoutes_v1_0_0.py', 'ocrscreenOnXvfb_v1_0_0.py', 'hyphensAndDigits_v1_0_0.py']

if __name__ == "__main__":
    # Usage: /home/claude/venv314_ch22_latest/bin/python sen0414_ch22_corpus_base_v1_0_0.py   (exits 1 if a program does not exit 0)
    import os, subprocess, sys
    bad = 0
    for name, (code, needs, live) in PROGRAMS.items():
        r = subprocess.run([sys.executable, "-W", "ignore", "-c", code], capture_output=True, text=True, timeout=900, stdin=subprocess.DEVNULL)
        bad += r.returncode != 0
        print("=== %s (exit %d)%s%s" % (name, r.returncode, " FETCHES THE ZIP" if live else "", " [local stand-in: %s]" % STAND_IN[name] if name in STAND_IN else "")); print(r.stdout.rstrip()[:3500]); print(r.stderr[-500:].rstrip())
    print("%d programs, %d did not exit 0" % (len(PROGRAMS), bad)); sys.exit(1 if bad else 0)

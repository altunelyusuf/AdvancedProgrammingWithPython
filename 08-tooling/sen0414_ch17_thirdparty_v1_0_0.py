#!/usr/bin/env python3
"""Chapter 17 (PDF and Word Documents): runs the chapter's own programs, whole, and the chapter's interactive statements, under the given
interpreter, and writes or checks their recorded output.
What is fetched at run time and kept in a cache directory (CH17_CACHE, default the system temp directory): the chapter page
(https://automatetheboringstuff.com/3e/chapter17.html, its sha256 is compared with the chapterDigest of the book's own chapter ontology) and
the zip of the 3rd edition's online materials (No Starch Press, sha256 dac627e8...a916) that holds the files the chapter uses
(Recursion_Chapter1.pdf, watermark.pdf, demo.docx, zophie.png, guests.txt, dictionary.txt) and the book's own scripts. None of those files is
stored in the repository; every file is checked against the sha256 recorded here before it is used.
Three environments, all Python 3.14.6 installed with uv, are named by environment variables and by the first argument's directory:
  LATEST  the newest releases on 2026-10-12: pypdf 6.20.1, python-docx 1.2.0, pdfminer.six 20260107, Pillow 12.3.0, cryptography 50.0.2
  PINS    the versions Appendix A of the book pins (pypdf 5.0.1, python-docx 1.1.2, pdfminer.six 20240706); Pillow 10.4.0 has no wheel for 3.14
          and could not be built here (no libjpeg headers), so PINS carries the newest Pillow
  BARE    pypdf 6.20.1 alone (no Pillow, no cryptography), to see what the optional dependencies do
The environments are named by CH17_LATEST, CH17_PINS and CH17_BARE (paths of their python), defaults /home/claude/venv314_ch17_latest/bin/python,
/home/claude/venv314_ch17_pins/bin/python and /home/claude/venv314_ch17_bare/bin/python.
Not executed here: Microsoft Word itself, any PDF viewer's display, the language model clean-up of the text, a display of any file in a browser.
A line that starts with MEASURED is a timing; it is recorded and is not compared by the check.
Usage: sen0414_ch17_thirdparty_v1_0_0.py write|check [python]   (python defaults to the LATEST environment)
Record: 08-tooling/ch17-page/third_party_record_v1_0_0.json"""
__version__ = "1.0.0"
import json, os, re, subprocess, sys, tempfile
MODE = sys.argv[1]
LATEST = os.environ.get("CH17_LATEST", "/home/claude/venv314_ch17_latest/bin/python")
PINS = os.environ.get("CH17_PINS", "/home/claude/venv314_ch17_pins/bin/python")
BARE = os.environ.get("CH17_BARE", "/home/claude/venv314_ch17_bare/bin/python")
PY = sys.argv[2] if len(sys.argv) > 2 else LATEST
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REC = os.path.join(REPO, "08-tooling", "ch17-page", "third_party_record_v1_0_0.json")
GET = r'''import os, io, zipfile, hashlib, shutil, tempfile, urllib.request, html, re, json, subprocess, sys
UA = 'Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0'
CACHE = os.environ.get('CH17_CACHE') or tempfile.gettempdir()
ZIPSHA = 'dac627e807f69ee14913ba621a15dec1f98db739d76939555ba5360d05eba916'
SHA = {'Recursion_Chapter1.pdf': 'd943896e0bd2241d5d8d819b43c197225c5e87c23a4b852c4819e74261bbad29', 'watermark.pdf': '535a8584c4476491d9b7c1b3b987c269f86f0cd51f937dba0a46cfad31937d74',
       'demo.docx': 'b43b21137d7d69b16e9e1ec7ebb75e0e2f053d8947cd2ddcf79d60a0dfe5f121', 'zophie.png': '5c5bf02fd0c95cee5d490a6daf3f1c4ccbbcab9fdc59bd8bba9564cad1462ba1',
       'dictionary.txt': 'dc4042ec00f36acbb1c2c514c86db9d48348a1cfa8ec1bf105c08910bc094d3f', 'guests.txt': 'e6136e39f829ae7380be4969b780c72bd8022a1a97efc399f0f2002ce1fd5164',
       'extractpdftext.py': '84a3fb70fc362c555f5c4239b4b445c2aa727e3d04b8820771d3333513a3670a', 'extractpdfimages.py': '1a5893ea05e9627167871522c92318cdd7b268efcab4a3c2516b542729c0cef0',
       'combine_pdfs.py': '07dcdf353f0bc2f3f251ae2da3076cba62c46a98a2ac3234193f9d0f494bb1f7', 'readDocx.py': '544a900d6bcbf3a4312dd4c8f3f6c54792553dccc0a13370ce10b8be8ed05172'}
PREFIX = 'Automate_the_Boring_Stuff_3e_onlinematerials/'
LATEST = os.environ.get('CH17_LATEST', '/home/claude/venv314_ch17_latest/bin/python')
PINS = os.environ.get('CH17_PINS', '/home/claude/venv314_ch17_pins/bin/python')
BARE = os.environ.get('CH17_BARE', '/home/claude/venv314_ch17_bare/bin/python')
def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=120).read()
def chapter():
    p = os.path.join(CACHE, 'ch17_chapter.html')
    if not os.path.exists(p):
        open(p + '.part', 'wb').write(fetch('https://automatetheboringstuff.com/3e/chapter17.html')); os.replace(p + '.part', p)
    return open(p, 'rb').read()
def materials():
    p = os.path.join(CACHE, 'ch17_materials.zip')
    if not os.path.exists(p):
        open(p + '.part', 'wb').write(fetch('https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip')); os.replace(p + '.part', p)
    assert hashlib.sha256(open(p, 'rb').read()).hexdigest() == ZIPSHA, 'the online materials differ from the recorded zip'
    return p
def shipped(name):
    b = zipfile.ZipFile(materials()).read(PREFIX + name)
    assert hashlib.sha256(b).hexdigest() == SHA[name], name + ' differs from the recorded file'
    return b
def work(*names):
    d = tempfile.mkdtemp()
    for n in names: open(os.path.join(d, n), 'wb').write(shipped(n))
    os.chdir(d); return d
def pres():
    h = chapter().decode('utf-8')
    return [html.unescape(re.sub(r'<[^>]+>', '', x)) for x in re.findall(r'<pre\b[^>]*>.*?</pre>', h, re.S)]
def sh(cmd, **k):
    r = subprocess.run(cmd, capture_output=True, text=True, **k); return r
MARK = re.compile('[❶-❿]')
def unmark(text):
    """the book's numbered markers stand in the margin: at the start of a line they are dropped, after indentation they count as two columns"""
    out = []
    for ln in text.split('\n'):
        m = re.match(r'^(\s*)[❶-❿] ', ln)
        out.append((ln[m.end():] if not m.group(1) else m.group(1) + '  ' + ln[m.end():]) if m else ln)
    return '\n'.join(out)
def make_pdf(pages):
    """a small valid PDF 1.4: each page is a text (Helvetica, 612 x 792) or a dict(content=<content stream>, size=(w, h))"""
    objs = ["<< /Type /Catalog /Pages 2 0 R >>", None, "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    kids = []
    for i, p in enumerate(pages):
        if isinstance(p, str): p = {"content": "BT /F1 18 Tf 72 720 Td (%s) Tj ET" % p, "size": (612, 792)}
        w, h = p.get("size", (612, 792)); s = p["content"]
        pn = len(objs) + 1; kids.append(pn)
        objs.append("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %d %d] /Resources << /Font << /F1 3 0 R >> >> /Contents %d 0 R >>" % (w, h, pn + 1))
        objs.append("<< /Length %d >>\nstream\n%s\nendstream" % (len(s), s))
    objs[1] = "<< /Type /Pages /Kids [%s] /Count %d >>" % (" ".join("%d 0 R" % k for k in kids), len(kids))
    b = b"%PDF-1.4\n"; offs = []
    for i, o in enumerate(objs, 1):
        offs.append(len(b)); b += ("%d 0 obj\n%s\nendobj\n" % (i, o)).encode("latin-1")
    x = len(b); b += ("xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)).encode()
    for o in offs: b += ("%010d 00000 n \n" % o).encode()
    return b + ("trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, x)).encode()
'''
REPLAY = r'''import sys, gc, contextlib
PRES = pres()
MARK = re.compile('[❶-❿]\\s?')
def parse(block):
    block = MARK.sub('', block)
    lines = block.rstrip('\n').split('\n'); items = []; cur = None
    def complete(t):
        try: compile(t + '\n', '<s>', 'single'); return True
        except SyntaxError as e:
            m = str(e)
            return not ('unterminated' in m or 'never closed' in m or 'EOF' in m or 'expected an indented' in m)
    for ln in lines:
        if ln.startswith('>>> ') or ln == '>>>':
            cur = {'src': ln[4:], 'out': [], 'open': True}; items.append(cur)
            if complete(cur['src']): cur['open'] = False
            continue
        if ln.startswith('...') and cur is not None and cur['open']:
            cur['src'] += '\n' + ln[4:]
            if ln.strip() == '...': cur['open'] = False
            continue
        if cur is not None and cur['open']:
            sep = '' if cur['src'].endswith(' ') or ln.startswith(' ') else ' '
            cur['src'] += sep + ln
            if complete(cur['src']): cur['open'] = False
            continue
        if ln.startswith('...') and cur is not None: continue
        if cur is not None: cur['out'].append(ln)
    return items
def norm(t):
    t = re.sub(r'\s+', '', t)
    t = re.sub(r'0x[0-9A-Fa-f]+', '0xADDR', t); t = re.sub(r'id:\d+', 'id:N', t); t = re.sub(r'IndirectObject\(\d+,\d+,\d+\)', 'IndirectObject(N)', t)
    return t
def match(expected, got):
    e = norm('\n'.join(expected)); g = norm(got)
    if '--snip--' in e:
        a, b = e.split('--snip--', 1)
        return 'match' if g.startswith(a) and g.endswith(b) else 'differs'
    return 'match' if e == g else 'differs'
d = work('Recursion_Chapter1.pdf', 'watermark.pdf', 'demo.docx', 'zophie.png'); ns = {'__name__': '__main__'}; rows = []
sys.path.insert(0, d)
for bi, blk in enumerate(PRES):
    if bi == 19: open('readDocx.py', 'w').write(blk)
    if '>>> ' not in MARK.sub('', blk)[:12]: continue
    for it in parse(blk):
        src = it['src']; buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(src + '\n', '<chapter>', 'single'), ns)
            got = buf.getvalue()
        except BaseException as e:
            t = type(e); q = t.__qualname__ if t.__module__ == 'builtins' else t.__module__ + '.' + t.__qualname__
            got = buf.getvalue() + 'Traceback (most recent call last):\n--snip--\n%s: %s' % (q, e)
        exp = it['out']
        rows.append((bi, src, '\n'.join(exp), got.rstrip('\n'), match(exp, got)))
from collections import Counter
c = Counter(r[4] for r in rows)
print('statements', len(rows), dict(sorted(c.items())))
for bi, src, exp, got, v in rows:
    if v != 'match':
        one = lambda s: re.sub(r'\s+', ' ', s)[:110]
        print('block %d %s | %s | printed: %s | got: %s' % (bi, v, one(src), one(exp), one(got)))
'''
PROGS = [
 ("The environments: interpreter, packages and their versions, in the three environments of the study", GET + r'''for name, py in (('LATEST', LATEST), ('PINS', PINS), ('BARE', BARE)):
    r = sh([py, '-I', '-c', "import sys, importlib.metadata as m\nv = lambda n: m.version(n) if n in {d.metadata['Name'].lower() for d in m.distributions()} | {d.metadata['Name'] for d in m.distributions()} else None\nprint(sys.version.split()[0], {n: v(n) for n in ('pypdf', 'python-docx', 'pdfminer.six', 'pillow', 'cryptography', 'lxml')})"])
    print(name, r.stdout.strip() or r.stderr.strip()[-200:])
'''),
 ("The chapter page: size, sha256 against the chapterDigest of the book's chapter ontology, and what it holds", GET + r'''h = chapter(); d = hashlib.sha256(h).hexdigest()
P = pres(); t = h.decode('utf-8'); txt = html.unescape(re.sub(r'<[^>]+>', '', t))
repl = [p for p in P if re.sub('[❶-❿] ?', '', p).lstrip().startswith('>>>')]
print(len(h), d, d == '00cb1643dca3afd3b75bfd9ce7ad594f3dd80f8606de1cffe40b8583846b4789')
print('pre blocks', len(P), 'interactive', len(repl), 'figures', sorted(set(re.findall(r'Figure 17-\d+', txt)), key=lambda s: int(s.split('-')[1])), 'images', len(re.findall(r'<img\b', t)), 'tables', len(re.findall(r'<table\b', t)))
print('statements', sum(1 for p in repl for ln in re.sub('[❶-❿] ?', '', p).split('\n') if ln.startswith('>>> ')))
print('practice questions', len(re.findall(r'^\s*\d+\.\s{2}', txt, re.M)), '| practice programs', re.findall(r'<h4[^>]*>(PDF Paranoia|Custom Invitations|PDF Password Breaker)', t))
'''),
 ("The online materials of the 3rd edition: the zip and the files in it that chapter 17 uses or that are the book's own scripts for it", GET + r'''p = materials(); b = open(p, 'rb').read()
z = zipfile.ZipFile(p)
print(len(b), hashlib.sha256(b).hexdigest())
names = [n for n in z.namelist() if not n.endswith('/') and '/._' not in n and not n.split('/')[-1].startswith('._')]
print(len(names), 'files')
for n in sorted(names):
    f = n.split('/')[-1]
    if f in SHA or re.search(r'pdf|docx|guest|dictionary|zophie|encrypt|invit|word', f, re.I):
        x = z.read(n); print(f, len(x), hashlib.sha256(x).hexdigest()[:16], 'recorded' if f in SHA and hashlib.sha256(x).hexdigest() == SHA[f] else 'not recorded')
print('no encrypted.pdf, helloworld.docx or restyled.docx in the zip:', not any(re.search(r'encrypted|helloworld|restyled', n) for n in names))
'''),
 ("The shipped PDFs and the Word file: what is in them", GET + r'''import pypdf, docx
work('Recursion_Chapter1.pdf', 'watermark.pdf', 'demo.docx', 'zophie.png')
for name in ('Recursion_Chapter1.pdf', 'watermark.pdf'):
    r = pypdf.PdfReader(name); m = r.metadata
    print(name, 'pages', len(r.pages), 'version', r.pdf_header, 'encrypted', r.is_encrypted, 'mediabox', [float(x) for x in r.pages[0].mediabox], 'producer', m.producer if m else None, 'creator', m.creator if m else None)
r = pypdf.PdfReader('Recursion_Chapter1.pdf')
print('rotation of page 1', r.pages[0].rotation, '| outline entries', len(r.outline), '| xmp metadata', r.xmp_metadata is not None)
print('images per page', [len(p.images) for p in r.pages])
d = docx.Document('demo.docx')
print('demo.docx paragraphs', [(p.style.name, p.text) for p in d.paragraphs])
print('tables', len(d.tables), 'sections', len(d.sections), 'inline shapes', len(d.inline_shapes))
import zipfile as zf
print(sorted(zf.ZipFile('demo.docx').namelist()))
print(sh(['pdfinfo', 'Recursion_Chapter1.pdf']).stdout.split('\n')[:14])
'''),
 ("Every statement of the chapter's interactive listings, replayed in order under the newest releases, against the printed output", GET + r'''import pypdf, docx
''' + REPLAY),
 ("The same replay under the versions Appendix A of the book pins (pypdf 5.0.1, python-docx 1.1.2), with the interpreter 3.14.6", GET + "CHILD = %r\n" % (GET + "import pypdf, docx, importlib.metadata as md\nprint('pypdf', pypdf.__version__, 'python-docx', md.version('python-docx'))\n" + REPLAY) + r'''r = subprocess.run([PINS, '-I', '-c', CHILD], capture_output=True, text=True, env=dict(os.environ, CH17_CACHE=CACHE))
print(r.stdout.strip() or r.stderr.strip()[-600:])
'''),
]
PROGS += [
 ("The chapter's text extraction listing (extractpdftext.py), as printed, whole, on the shipped chapter PDF under the newest releases", GET + r'''work('Recursion_Chapter1.pdf')
src = unmark(pres()[1]); open('extractpdftext_printed.py', 'w').write(src)
shipped_script = shipped('extractpdftext.py').decode()
print('printed listing equals the shipped extractpdftext.py (ignoring the final newline):', src.strip() == shipped_script.replace('\r\n', '\n').strip(), '| the shipped file has Windows line endings:', '\r\n' in shipped_script)
r = sh([LATEST, '-I', 'extractpdftext_printed.py'])
print('exit', r.returncode, '| stderr lines naming fontTools:', sum('fontTools is required' in l for l in r.stderr.split('\n')), '| other stderr:', [l[:90] for l in r.stderr.split('\n') if l and 'fontTools' not in l][:3])
t = open('recursion.txt', encoding='utf-8').read()
print('characters', len(t), 'lines', t.count('\n'), 'words', len(t.split()))
print(repr(t[:170]))
print('page text joined without a separator: page 1 ends', repr(t[t.index('Sweigart') + 8: t.index('Sweigart') + 40]))
'''),
 ("The chapter's image extraction listing (extractpdfimages.py), as printed, whole, under the newest releases and under the versions Appendix A pins", GET + r'''for name, py in (('LATEST', LATEST), ('PINS', PINS)):
    work('Recursion_Chapter1.pdf')
    src = unmark(pres()[4]); open('extractpdfimages_printed.py', 'w').write(src)
    if name == 'LATEST': print('printed listing equals the shipped extractpdfimages.py (ignoring the final newline):', src.strip() == shipped('extractpdfimages.py').decode().replace('\r\n', '\n').strip())
    r = sh([py, '-I', 'extractpdfimages_printed.py'])
    lines = r.stdout.split('\n')
    reading = [l for l in lines if l.startswith('Reading')]
    wrote = [l for l in lines if l.startswith('Wrote')]
    files = sorted(f for f in os.listdir('.') if re.match(r'\d+_page', f))
    print(name, 'exit', r.returncode, '| reading lines', len(reading), '| wrote lines', len(wrote), '| files', len(files), '| bytes', sum(os.path.getsize(f) for f in files), '| skipped:', [l for l in lines if l.startswith('Skipped')], '| stderr:', r.stderr.strip()[-100:] or None)
    print(name, 'images per page', [int(re.search(r'- (\d+) images', l).group(1)) for l in reading])
    print(name, 'first lines', lines[:3], '| page 7:', [l for l in lines if 'page7' in l or 'page 7' in l])
print('printed sample: page 1 had 7 images (Im0.jpg, Im1.png, ...), page 7 skipped with "not enough image data", pages 17 and 18 had 0')
'''),
 ("Project 12 (combine_pdfs.py) as printed, whole: the steps put together, the book's own file, the corrected program, and a second run", GET + r'''d = work(); os.chdir(d)
open('A_cover.pdf', 'wb').write(make_pdf(['A cover', 'A page two', 'A page three']))
open('b_report.pdf', 'wb').write(make_pdf(['B cover', 'B page two', 'B page three', 'B page four']))
open('c_one.pdf', 'wb').write(make_pdf(['C only page']))
P = pres()
step1, step2, step3 = unmark(P[15]), unmark(P[16]), unmark(P[17])
loop = step2.split('--snip--')[1].strip('\n'); save = step3.split('--snip--')[1].strip('\n')
printed = step1.rstrip('\n').split('# TODO: Loop')[0] + '\n' + loop + '\n\n' + save + '\n'
open('combine_printed.py', 'w').write(printed)
r = sh([LATEST, '-I', 'combine_printed.py']); print('as printed: exit', r.returncode, '|', r.stderr.strip().splitlines()[-1])
fixed = printed.replace('pdf_files.append', 'pdf_filenames.append'); open('combine_fixed.py', 'w').write(fixed)
r = sh([LATEST, '-I', 'combine_fixed.py']); print('with pdf_files renamed pdf_filenames: exit', r.returncode, r.stderr.strip()[-120:])
import pypdf
c = pypdf.PdfReader('combined.pdf'); print('combined.pdf pages', len(c.pages), [p.extract_text() for p in c.pages])
print('sort order: plain', sorted(['Zebra.pdf', 'apple.pdf']), 'with key=str.lower', sorted(['Zebra.pdf', 'apple.pdf'], key=str.lower))
print('order of files', sorted([f for f in os.listdir('.') if f.endswith('.pdf')], key=str.lower), '| plain sort', sorted([f for f in os.listdir('.') if f.endswith('.pdf')]))
r = sh([LATEST, '-I', 'combine_fixed.py']); c2 = pypdf.PdfReader('combined.pdf')
print('second run: exit', r.returncode, 'pages', len(c2.pages), [p.extract_text() for p in c2.pages])
open('shipped_combine_pdfs.py', 'wb').write(shipped('combine_pdfs.py'))
r = sh([LATEST, '-I', 'shipped_combine_pdfs.py']); print('the shipped combine_pdfs.py: exit', r.returncode, '|', r.stderr.strip().splitlines()[-1])
s = shipped('combine_pdfs.py').decode(); print('the shipped file names pdf_files in its loop:', 'for pdf_filename in pdf_files:' in s, '| PdfWriter without pypdf prefix:', 'writer = PdfWriter()' in s)
'''),
 ("get_text() of readDocx.py as printed and as shipped, on demo.docx", GET + r'''import docx
work('demo.docx'); 
src = unmark(pres()[19]); ns = {}; exec(src, ns)
a = ns['get_text']('demo.docx')
s = shipped('readDocx.py').decode(); ns2 = {}; exec(s, ns2); b = ns2['get_text']('demo.docx')
print('printed:', repr(a))
print('shipped:', repr(b))
print('shipped joins with a blank line (two newlines):', "'\\n\\n'.join" in s, '| equal:', a == b)
print('the page prints the result of print(get_text(...)) as six lines; the document has', len(docx.Document('demo.docx').paragraphs), 'paragraphs, the last one empty:', repr(docx.Document('demo.docx').paragraphs[-1].text))
print('indent variant of the text:', repr('\n'.join('  ' + p.text for p in docx.Document('demo.docx').paragraphs[:2])))
'''),
 ("The default style names the chapter prints against the styles of a new document and of demo.docx", GET + r'''import docx, warnings
from docx.enum.style import WD_STYLE_TYPE
printed = re.findall(r"'([^']*)'", pres()[23])
new = docx.Document(); names = [s.name for s in new.styles]
work('demo.docx'); demo = docx.Document('demo.docx'); dnames = [s.name for s in demo.styles]
print('names printed', len(printed), '| in a new document', len(names), '| in demo.docx', len(dnames))
print('printed names not in a new document:', [n for n in printed if n not in names])
print('printed names not in demo.docx:', [n for n in printed if n not in dnames])
print('styles of a new document by kind:', {k.name: sum(1 for s in new.styles if s.type == k) for k in WD_STYLE_TYPE})
for n in ('List Number ', 'MacroText', 'macro', 'Quote', 'Quote Char', 'Heading 1', 'Title'):
    p = new.add_paragraph('x')
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        try: p.style = n; res = p.style.name
        except Exception as e: res = type(e).__name__ + ': ' + str(e)[:60]
    print(repr(n), '->', res, [str(x.message)[:60] for x in w])
print('character styles that end in Char:', sorted(n for n in names if n.endswith(' Char'))[:5], '...', len([n for n in names if n.endswith(' Char')]))
p = new.add_paragraph('x'); r = p.add_run('y')
for n in ('Quote', 'Quote Char'):
    try: r.style = n; print('run style', n, 'accepted')
    except Exception as e: print('run style', n, type(e).__name__, str(e))
try: new.styles['NoSuchStyle']
except KeyError as e: print('unknown style:', type(e).__name__, e)
st = new.styles.add_style('Invitation Name', WD_STYLE_TYPE.PARAGRAPH); print('custom style created in code:', st.name, st.type)
'''),
 ("Table 17-1: which of the twelve text attributes exist on a Run and which only on its font, and what the tri-state values write", GET + r'''import docx
d = docx.Document(); r = d.add_paragraph('z').add_run('text')
for a in ('bold', 'italic', 'underline', 'strike', 'double_strike', 'all_caps', 'small_caps', 'shadow', 'outline', 'rtl', 'imprint', 'emboss'):
    print('%-14s on Run: %-5s on Run.font: %s' % (a, a in dir(type(r)), a in dir(type(r.font))))
r.strike = True
print('after run.strike = True: no error; run.font.strike is', r.font.strike, '| the XML has a strike element:', '<w:strike' in r._r.xml)
r.font.strike = True
print('after run.font.strike = True: font.strike', r.font.strike, '| the XML has a strike element:', '<w:strike' in r._r.xml)
q = d.add_paragraph('q').add_run('t')
print('fresh run bold/italic/underline:', q.bold, q.italic, q.underline, '| xml run properties:', '<w:rPr' in q._r.xml)
q.bold = True; print('bold True ->', q.bold, 'xml', re.findall(r'<w:b[ /][^>]*>', q._r.xml))
q.bold = False; print('bold False ->', q.bold, 'xml', re.findall(r'<w:b[ /][^>]*>', q._r.xml))
q.bold = None; print('bold None ->', q.bold, 'xml', re.findall(r'<w:b[ /][^>]*>', q._r.xml))
from docx.enum.text import WD_UNDERLINE
q.underline = True; print('underline True ->', repr(q.underline), re.findall(r'<w:u [^>]*>', q._r.xml))
q.underline = WD_UNDERLINE.DOUBLE; print('underline DOUBLE ->', repr(q.underline), re.findall(r'<w:u [^>]*>', q._r.xml))
q.underline = False; print('underline False ->', repr(q.underline), re.findall(r'<w:u [^>]*>', q._r.xml))
'''),
 ("Headings and breaks: the levels add_heading accepts, the style each gets, and where WD_BREAK is found", GET + r'''import docx
d = docx.Document()
for lv in (-1, 0, 1, 4, 5, 9, 10):
    try: print(lv, '->', d.add_heading('Header %d' % lv, lv).style.name)
    except Exception as e: print(lv, '->', type(e).__name__, e)
try: d.add_heading('x', '1')
except Exception as e: print("'1' ->", type(e).__name__, e)
print('docx.enum.text.WD_BREAK is reachable after import docx alone:', hasattr(docx, 'enum') and hasattr(docx.enum.text, 'WD_BREAK'), '| docx.shared.Inches:', hasattr(docx, 'shared'))
print('WD_BREAK.PAGE =', docx.enum.text.WD_BREAK.PAGE.name, docx.enum.text.WD_BREAK.PAGE.value, '| members', sorted(m.name for m in docx.enum.text.WD_BREAK))
d = docx.Document(); d.add_paragraph('This is on the first page!')
d.paragraphs[0].runs[0].add_break(docx.enum.text.WD_BREAK.PAGE); d.add_paragraph('This is on the second page!')
print('page break element:', re.findall(r'<w:br [^>]*>', d.paragraphs[0].runs[0]._r.xml), '| paragraphs', len(d.paragraphs))
r = d.paragraphs[1].runs[0]; r.add_break(); print('line break element:', re.findall(r'<w:br[ /][^>]*>', r._r.xml), '| paragraph text', repr(d.paragraphs[1].text))
d.add_paragraph('a\tb\nc'); print('tab and newline in text become elements:', re.findall(r'<w:(?:tab|br)/>', d.paragraphs[-1].runs[0]._r.xml), repr(d.paragraphs[-1].text))
'''),
 ("add_picture: the size in EMU for width and height given together and apart, the aspect ratio, and what is stored in the file", GET + r'''import docx
from docx.shared import Inches, Cm
work('zophie.png'); d = docx.Document()
a = d.add_picture('zophie.png', width=Inches(1), height=Cm(4)); b = d.add_picture('zophie.png', width=Inches(1)); c = d.add_picture('zophie.png')
print('image 816 x 1088 pixels, ratio', round(816 / 1088, 4))
for label, s in (('width=Inches(1), height=Cm(4)', a), ('width=Inches(1) only', b), ('neither', c)):
    print('%-30s width %8d EMU (%.3f in) height %8d EMU (%.3f in) ratio %.4f' % (label, s.width, s.width / 914400, s.height, s.height / 914400, s.width / s.height))
print('Inches(1) =', int(Inches(1)), 'EMU, Cm(4) =', int(Cm(4)), 'EMU, one cm =', int(Cm(1)))
print('paragraphs added by add_picture:', len(d.paragraphs), '| runs each:', [len(p.runs) for p in d.paragraphs], '| inline shapes', len(d.inline_shapes))
d.save('pics.docx'); z = zipfile.ZipFile('pics.docx'); m = [n for n in z.namelist() if n.startswith('word/media')]
print('media parts', m, '| stored image equals zophie.png byte for byte:', z.read(m[0]) == open('zophie.png', 'rb').read(), '| three pictures, one stored copy')
'''),
 ("What a .docx file is: a ZIP of XML parts; a new document from the package's template; reading it back", GET + r'''import docx
d = docx.Document(); cp = d.core_properties
print('new document: author', repr(cp.author), 'created', cp.created, 'revision', cp.revision, 'styles', len(d.styles), 'paragraphs', len(d.paragraphs), 'sections', len(d.sections))
d.add_paragraph('Hello, world!'); d.save('hw.docx'); z = zipfile.ZipFile('hw.docx')
print(len(z.namelist()), 'parts:', sorted(z.namelist()))
body = z.read('word/document.xml').decode()
print('body:', re.search(r'<w:body>(.*?)<w:sectPr', body, re.S).group(1))
print('first bytes of the file:', open('hw.docx', 'rb').read(4), '| mimetype of the main part:', re.search(r'PartName="/word/document.xml" ContentType="([^"]+)"', z.read('[Content_Types].xml').decode()).group(1))
p = d.add_paragraph('A plain paragraph with some '); p.add_run('bold').bold = True; p.add_run(' and some '); p.add_run('italic').italic = True
print('runs', [r.text for r in p.runs], '| the text', repr(p.text))
print('run elements in the paragraph XML:', p._p.xml.count('<w:r>'))
t = d.add_table(rows=1, cols=2); t.cell(0, 0).text = 'in a table'; d.sections[0].header.paragraphs[0].text = 'IN THE HEADER'
print('Document.paragraphs', [x.text for x in d.paragraphs], '| the table text and the header text are elsewhere:', t.cell(0, 0).text, '|', d.sections[0].header.paragraphs[0].text)
from docx.oxml import parse_xml
q = d.add_paragraph('before '); q._p.append(parse_xml('<w:hyperlink xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:r><w:t>linked</w:t></w:r></w:hyperlink>'))
print('paragraph with a hyperlink: text', repr(q.text), 'runs', [r.text for r in q.runs])
'''),
 ("The shipped demo.docx: restyling it as the chapter does, saving, reading back, and the Word package it came from", GET + r'''import docx
work('demo.docx'); d = docx.Document('demo.docx')
print([(p.style.name, p.text) for p in d.paragraphs])
core = d.core_properties; print('core properties: created', core.created, 'modified', core.modified, '| the file was last saved by a person, not by python-docx:', core.last_modified_by != 'python-docx')
z = zipfile.ZipFile('demo.docx'); print('app.xml:', re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', z.read('docProps/app.xml').decode()))[:120])
d.paragraphs[0].style = 'Normal'; d.paragraphs[1].runs[0].style = 'Quote Char'; d.paragraphs[1].runs[1].underline = True; d.paragraphs[1].runs[3].underline = True; d.save('restyled.docx')
x = docx.Document('restyled.docx')
print('restyled:', x.paragraphs[0].style.name, [(r.text, r.style.name, r.underline) for r in x.paragraphs[1].runs])
print('runs of the second paragraph: bold values', [r.bold for r in docx.Document('demo.docx').paragraphs[1].runs], '| italic values', [r.italic for r in docx.Document('demo.docx').paragraphs[1].runs])
print('run texts', [r.text for r in docx.Document('demo.docx').paragraphs[1].runs])
'''),
 ("LibreOffice 24.2 opens the files the chapter creates: conversion to PDF, page counts and the text it shows (Microsoft Word itself was not available)", GET + r'''import docx
from docx.enum.text import WD_BREAK
work('demo.docx', 'zophie.png')
d = docx.Document(); d.add_paragraph('Hello, world!'); d.save('helloworld.docx')
d = docx.Document(); d.add_paragraph('Hello world!'); p1 = d.add_paragraph('This is a second paragraph.'); d.add_paragraph('This is a yet another paragraph.'); p1.add_run(' This text is being added to the second paragraph.'); d.save('multipleParagraphs.docx')
d = docx.Document()
for i in range(5): d.add_heading('Header %d' % i, i)
d.save('headings.docx')
d = docx.Document(); d.add_paragraph('This is on the first page!'); d.paragraphs[0].runs[0].add_break(WD_BREAK.PAGE); d.add_paragraph('This is on the second page!'); d.save('twoPage.docx')
d = docx.Document(); d.add_picture('zophie.png', width=docx.shared.Inches(1), height=docx.shared.Cm(4)); d.save('picture.docx')
dm = docx.Document('demo.docx'); dm.paragraphs[0].style = 'Normal'; dm.paragraphs[1].runs[0].style = 'Quote Char'; dm.paragraphs[1].runs[1].underline = True; dm.paragraphs[1].runs[3].underline = True; dm.save('restyled.docx')
files = ['helloworld.docx', 'multipleParagraphs.docx', 'headings.docx', 'twoPage.docx', 'picture.docx', 'restyled.docx', 'demo.docx']
r = sh(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', 'out'] + files, timeout=600)
print('soffice exit', r.returncode, '| converted', sorted(os.listdir('out')) if os.path.isdir('out') else None)
import pypdf
for f in files:
    q = 'out/' + f.replace('.docx', '.pdf')
    if os.path.exists(q):
        rd = pypdf.PdfReader(q); print('%-24s pages %d  text %r' % (f, len(rd.pages), ' / '.join(p.extract_text().replace('\n', ' | ')[:90] for p in rd.pages)))
print(sh(['soffice', '--version']).stdout.strip())
print('pdfinfo of twoPage.pdf:', [l for l in sh(['pdfinfo', 'out/twoPage.pdf']).stdout.split('\n') if l.startswith(('Pages', 'Producer', 'Page size'))])
'''),
 ("The PDF file itself: header, objects, cross-reference table, trailer; how text is stored; a drawing over text does not remove it; a scan has no text", GET + r'''import pypdf
from PIL import Image, ImageDraw
b = make_pdf(['Page one', 'Page two']); open('a.pdf', 'wb').write(b)
print('first line', b.split(b'\n')[0], '| ends with', b[-6:].strip(), '| startxref', re.search(rb'startxref\n(\d+)', b).group(1).decode(), '| xref at that offset:', b[int(re.search(rb'startxref\n(\d+)', b).group(1)):][:4])
print('objects', re.findall(rb'(\d+) 0 obj', b), '| a content stream:', re.search(rb'stream\n(.*?)\nendstream', b, re.S).group(1))
r = pypdf.PdfReader('a.pdf'); print('pypdf reads', len(r.pages), 'pages', [p.extract_text() for p in r.pages], r.pdf_header, '| qpdf --check:', 'No syntax or stream encoding errors found' in sh(['qpdf', '--check', 'a.pdf']).stdout)
open('red.pdf', 'wb').write(make_pdf([{'content': 'BT /F1 18 Tf 72 720 Td (Salary: 120000 USD) Tj ET 0 0 0 rg 60 710 300 30 re f'}]))
print('text under a black box: pypdf', repr(pypdf.PdfReader('red.pdf').pages[0].extract_text()), '| pdftotext', repr(sh(['pdftotext', 'red.pdf', '-']).stdout.strip()))
im = Image.new('RGB', (200, 100), 'white'); ImageDraw.Draw(im).text((10, 40), 'SCANNED TEXT', fill='black'); im.save('scan.pdf')
s = pypdf.PdfReader('scan.pdf'); print('image-only PDF: pages', len(s.pages), 'text', repr(s.pages[0].extract_text()), 'images', len(s.pages[0].images), s.pages[0].images[0].name)
print('writing with pypdf records its name as the producer:', (lambda w, o: (w.append('a.pdf'), w.write(o), pypdf.PdfReader(io.BytesIO(o.getvalue())).metadata)[2])(pypdf.PdfWriter(), io.BytesIO()))
big = pypdf.PdfWriter(); big.append('a.pdf', (0, 1)); big.write('one.pdf'); print('pages of one.pdf', len(pypdf.PdfReader('one.pdf').pages))
'''),
]
PROGS += [
 ("The optional dependencies, in an environment with pypdf alone: text, images, RC4 and AES encryption, reading an AES file", GET + r'''import subprocess
CODE = r"""
import pypdf, io, os, logging, sys, tempfile
os.chdir(tempfile.mkdtemp())
logging.disable(logging.CRITICAL)
def t(label, f):
    try: v = f()
    except BaseException as e: v = 'EXC %s.%s: %s' % (type(e).__module__, type(e).__name__, str(e)[:80])
    print('%-44s %s' % (label, v))
open('a.pdf', 'wb').write(__MAKE__)
open('r.pdf', 'wb').write(open(sys.argv[1], 'rb').read())
import importlib.util
print('Pillow importable:', importlib.util.find_spec('PIL') is not None, '| cryptography importable:', importlib.util.find_spec('cryptography') is not None, '| fontTools importable:', importlib.util.find_spec('fontTools') is not None)
r = pypdf.PdfReader('a.pdf')
t('extract_text', lambda: r.pages[0].extract_text())
R = pypdf.PdfReader('r.pdf')
t('len(page.images) of chapter page 1', lambda: len(R.pages[0].images))
t('image.name and len(image.data)', lambda: [(i.name, len(i.data)) for i in R.pages[0].images][:2])
t('image.image (a Pillow image)', lambda: type(R.pages[0].images[0].image).__name__)
t('extract_text of chapter page 1', lambda: repr(R.pages[0].extract_text()[:20]))
def rc4():
    w = pypdf.PdfWriter(); w.append('a.pdf'); w.encrypt('swordfish'); w.write('rc4.pdf'); return 'written, ' + str(pypdf.PdfReader('rc4.pdf').decrypt('swordfish').name)
t('encrypt() with no algorithm (RC4)', rc4)
def aes():
    w = pypdf.PdfWriter(); w.append('a.pdf'); w.encrypt('swordfish', algorithm='AES-256'); w.write('aes.pdf'); return 'written'
t("encrypt(algorithm='AES-256')", aes)
def aes128():
    w = pypdf.PdfWriter(); w.append('a.pdf'); w.encrypt('swordfish', algorithm='AES-128'); w.write('aes128.pdf'); return 'written'
t("encrypt(algorithm='AES-128')", aes128)
t('encrypt() then write() (AES-128)', lambda: os.path.exists('aes128.pdf'))
"""
CODE = CODE.replace('__MAKE__', repr(make_pdf(['Page one'])))
work('Recursion_Chapter1.pdf'); RP = os.path.abspath('Recursion_Chapter1.pdf')
for name, py in (('BARE', BARE), ('LATEST', LATEST)):
    r = sh([py, '-I', '-c', CODE, RP]); print('---', name); print(r.stdout.rstrip() or r.stderr.strip()[-300:])
'''),
 ("Removed and renamed names of PyPDF that older tutorials use, under the newest release and the pinned one", GET + r'''import subprocess
CODE = r"""
import pypdf, warnings
print('pypdf', pypdf.__version__)
for n in ('PdfFileReader', 'PdfFileWriter', 'PdfMerger', 'PdfReader', 'PdfWriter'):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        try:
            o = getattr(pypdf, n); res = 'name exists'
            if n == 'PdfMerger':
                try: o(); res += ', calling it works'
                except Exception as e: res += ', calling it raises %s: %s' % (type(e).__name__, str(e))
        except Exception as e: res = '%s: %s' % (type(e).__name__, e)
    print('%-14s %s' % (n, res))
print('names on PdfReader/PageObject in the old camelCase style:', [m for m in ('getPage', 'numPages', 'isEncrypted', 'getNumPages') if hasattr(pypdf.PdfReader, m)], [m for m in ('mergePage', 'extractText', 'rotateClockwise') if hasattr(pypdf.PageObject, m)])
import io
src_pdf = io.BytesIO(__MAKE__)
w = pypdf.PdfWriter(); w.append(src_pdf, (0, 3)); n0 = len(w.pages)
try: w.merge(1, src_pdf, (0, 2)); print('merge(1, file, (0, 2)) with 3 pages in the writer and 6 in the file: writer has', len(w.pages), 'pages')
except Exception as e: print('merge(1, file, (0, 2)):', type(e).__name__, str(e)[:80])
w = pypdf.PdfWriter(); w.append(src_pdf, (0, 3)); w.merge(1, src_pdf, pages=(0, 2)); print('merge(1, file, pages=(0, 2)): writer has', len(w.pages), 'pages')
w = pypdf.PdfWriter(); w.append(src_pdf, (0, 3)); w.merge(1, src_pdf, None, (0, 2)); print('merge(1, file, None, (0, 2)): writer has', len(w.pages), 'pages')
print('names in the style the chapter uses:', [m for m in ('decrypt', 'pages', 'is_encrypted') if hasattr(pypdf.PdfReader, m)], [m for m in ('extract_text', 'merge_page', 'rotate') if hasattr(pypdf.PageObject, m)], [m for m in ('append', 'merge', 'encrypt', 'add_blank_page', 'insert_blank_page', 'write') if hasattr(pypdf.PdfWriter, m)])
"""
CODE = CODE.replace('__MAKE__', repr(make_pdf(['p%d' % i for i in range(6)])))
for name, py in (('LATEST', LATEST), ('PINS', PINS)):
    r = sh([py, '-I', '-c', CODE]); print('---', name); print(r.stdout.rstrip() or r.stderr.strip()[-300:])
import docx
d = sh([os.environ.get('CH17_DOCX02', '/home/claude/venv314_ch17_docx02/bin/python'), '-I', '-c', "import docx"])
print('--- the package named docx (0.2.4) that the chapter warns against, in Python 3.14.6:', (d.stderr.strip().splitlines() or ['imported'])[-1])
'''),
 ("Page operations on the shipped chapter PDF: append, list against tuple, merge, rotate, blank pages, watermark, and what each leaves", GET + r'''import pypdf, inspect, logging
logging.disable(logging.CRITICAL)
work('Recursion_Chapter1.pdf', 'watermark.pdf')
R = pypdf.PdfReader('Recursion_Chapter1.pdf'); RT = [p.extract_text() for p in R.pages]
def pg(w): return len(w.pages)
def src(w): return [RT.index(p.extract_text()) for p in w.pages]
w = pypdf.PdfWriter(); w.append('Recursion_Chapter1.pdf', (0, 5)); print('append (0, 5):', pg(w), 'pages, source page indexes', src(w))
w = pypdf.PdfWriter(); w.append('Recursion_Chapter1.pdf', (0, 5, 2)); print('append (0, 5, 2):', pg(w), 'pages, source page indexes', src(w))
w = pypdf.PdfWriter(); w.append('Recursion_Chapter1.pdf', [0, 5]); print('append [0, 5]:', pg(w), 'pages, source page indexes', src(w))
w = pypdf.PdfWriter(); w.append('Recursion_Chapter1.pdf', [0, 1, 2, 3, 4]); print('append [0, 1, 2, 3, 4]:', pg(w), 'pages')
v = pypdf.PdfWriter(); v.append('Recursion_Chapter1.pdf', [0, 1, 2, 3, 4]); w.merge(2, 'Recursion_Chapter1.pdf', (0, 5))
print('merge(2, file, (0, 5)) as the chapter writes it, on 5 pages:', pg(w), 'pages (the whole file of 18 went in), source page indexes', src(w))
v.merge(2, 'Recursion_Chapter1.pdf', pages=(0, 5)); print('merge(2, file, pages=(0, 5)):', pg(v), 'pages, source page indexes', src(v))
print('merge signature', str(inspect.signature(pypdf.PdfWriter.merge)).split(', pages')[0].split('(self, ')[1] + ', pages ...', '| append signature', str(inspect.signature(pypdf.PdfWriter.append)).split(', pages')[0].split('(self, ')[1] + ', pages ...')
a = pypdf.PdfWriter(); a.append('Recursion_Chapter1.pdf'); print('write() returns', (lambda o: (a.write(o)[0], type(a.write(o)[1]).__name__))(io.BytesIO()))
w = pypdf.PdfWriter(); w.append('Recursion_Chapter1.pdf', (0, 5)); w.write('first_five_pages.pdf'); print('first_five_pages.pdf: pages', len(pypdf.PdfReader('first_five_pages.pdf').pages), 'bytes', os.path.getsize('first_five_pages.pdf'), 'of the original', os.path.getsize('Recursion_Chapter1.pdf'), '| metadata', pypdf.PdfReader('first_five_pages.pdf').metadata)
try: x = pypdf.PdfWriter(); x.append('Recursion_Chapter1.pdf', (0, 99)); print('(0, 99):', len(x.pages), 'pages')
except Exception as e: print('(0, 99):', type(e).__name__, e)
try: x = pypdf.PdfWriter(); x.append('Recursion_Chapter1.pdf', [0, 99]); print('[0, 99]:', len(x.pages), 'pages')
except Exception as e: print('[0, 99]:', type(e).__name__, e)
print('(1, 1) adds', len((lambda x: (x.append('Recursion_Chapter1.pdf', (1, 1)), x)[1])(pypdf.PdfWriter()).pages), 'pages (an empty range; a one-page PDF in Project 12 adds nothing and raises nothing)')
w = pypdf.PdfWriter(); w.append('Recursion_Chapter1.pdf'); outs = [w.pages[i].rotate(90) for i in range(len(w.pages))]
print('rotate(90) returns', type(outs[0]).__name__, '| rotation of the pages', {p.rotation for p in w.pages}, '| the first keys of what the shell would print:', sorted(k for k in outs[0].keys())[:3])
for ang in (45, 360, 450, -90, 180):
    q = pypdf.PdfWriter(); q.append('Recursion_Chapter1.pdf', (0, 1)); q.pages[0].rotate(90)
    try: q.pages[0].rotate(ang); print('rotate(90) then rotate(%d): rotation %d' % (ang, q.pages[0].rotation))
    except Exception as e: print('rotate(%d):' % ang, type(e).__name__, e)
try: q.pages[0].rotate(90.0); print('rotate(90.0) ok, rotation', q.pages[0].rotation)
except Exception as e: print('rotate(90.0):', type(e).__name__, e)
print('rotation is stored as /Rotate:', q.pages[0].get('/Rotate'), '| the content stream is unchanged by rotate')
w = pypdf.PdfWriter(); w.append('Recursion_Chapter1.pdf', (0, 1))
print('signature of insert_blank_page', str(inspect.signature(pypdf.PdfWriter.insert_blank_page)).split('->')[0].strip())
b = w.add_blank_page(); print('add_blank_page: size', [float(x) for x in b.mediabox][2:], 'pages', pg(w))
big = pypdf.PdfWriter(); big.append('watermark.pdf'); big.append('Recursion_Chapter1.pdf', (0, 1))
print('sizes of a letter page followed by a 546 x 708 page:', [[float(x) for x in p.mediabox][2:] for p in big.pages])
big.add_blank_page(); print('add_blank_page at the end takes the size of the last page:', [float(x) for x in big.pages[-1].mediabox][2:])
big.insert_blank_page(index=1); print('insert_blank_page(index=1) between them takes', [float(x) for x in big.pages[1].mediabox][2:], '(the page now after it, not the page before it)')
big.insert_blank_page(2); print('insert_blank_page(2) positional: width 2, so the page is', [float(x) for x in big.pages[0].mediabox][2:], 'at index 0, and the blank page at index 2 is', 'untouched' if len(big.pages) > 3 else '')
try: pypdf.PdfWriter().add_blank_page()
except Exception as e: print('blank page in an empty writer:', type(e).__name__)
wm = pypdf.PdfReader('watermark.pdf').pages[0]
w = pypdf.PdfWriter(); w.append('Recursion_Chapter1.pdf', (0, 3))
for p in w.pages: p.merge_page(wm, over=False)
w.write('with_watermark.pdf')
print('merge_page(wm, over=False): pages', len(pypdf.PdfReader('with_watermark.pdf').pages), '| bytes of the three-page copy', os.path.getsize('with_watermark.pdf'), 'against', os.path.getsize('first_five_pages.pdf'), 'for five pages without it | text of page 1 before:', repr(RT[0][:14]), 'after:', repr(pypdf.PdfReader('with_watermark.pdf').pages[0].extract_text()[:20]), '| the watermark page alone yields', repr(wm.extract_text()[:20]))
w2 = pypdf.PdfWriter(); w2.append('Recursion_Chapter1.pdf', (0, 1)); w2.pages[0].merge_page(wm, over=True); print('over=True: also fine, pages', len(w2.pages), '| signature', str(inspect.signature(pypdf.PageObject.merge_page)))
r = sh(['pdftoppm', '-r', '20', '-png', '-f', '1', '-l', '1', 'with_watermark.pdf', 'wm']); print('pdftoppm renders the watermarked page:', r.returncode == 0 and any(f.startswith('wm') for f in os.listdir('.')))
'''),
 ("Encryption: what encrypt() writes by default and with AES-256, how qpdf and pdftotext see it, the empty user password, and decrypt()'s return values", GET + r'''import pypdf, logging
logging.disable(logging.CRITICAL)
work('Recursion_Chapter1.pdf')
def enc(name, *a, **k):
    w = pypdf.PdfWriter(); w.append('Recursion_Chapter1.pdf', (0, 2)); w.encrypt(*a, **k); w.write(name)
enc('rc4.pdf', 'swordfish'); enc('aes.pdf', 'swordfish', algorithm='AES-256'); enc('two.pdf', 'userpw', 'ownerpw', algorithm='AES-256'); enc('emptyuser.pdf', '', 'ownerpw', algorithm='AES-256'); enc('aes128.pdf', 'swordfish', algorithm='AES-128'); enc('rc40.pdf', 'swordfish', use_128bit=False)
for f in ('rc4.pdf', 'aes128.pdf', 'rc40.pdf', 'aes.pdf'):
    d = pypdf.PdfReader(f).trailer['/Encrypt']
    q = sh(['qpdf', '--show-encryption', '--password=swordfish', f]).stdout
    m = re.search(r'file encryption method: (\S+)', q); mm = re.search(r'R = (\d)', q)
    print('%-12s /V %s /R %s /Length %s | qpdf: R = %s, file encryption method: %s' % (f, d['/V'], d['/R'], d.get('/Length'), mm.group(1), m.group(1) if m else 'not stated'))
r = pypdf.PdfReader('aes.pdf')
print('is_encrypted', r.is_encrypted)
try: r.pages[0]
except Exception as e: print('pages[0]:', type(e).__module__ + '.' + type(e).__name__, '-', e)
try: len(r.pages)
except Exception as e: print('len(pages):', type(e).__name__)
try: r.metadata
except Exception as e: print('metadata:', type(e).__name__)
for pw in ('an incorrect password', '', 'Swordfish', 'swordfish'):
    x = pypdf.PdfReader('aes.pdf'); res = x.decrypt(pw); print('decrypt(%r) -> %s (value %d)' % (pw, res.name, res.value))
for pw in ('userpw', 'ownerpw', 'swordfish'):
    x = pypdf.PdfReader('two.pdf'); print('two passwords: decrypt(%r) ->' % pw, x.decrypt(pw).name)
x = pypdf.PdfReader('two.pdf'); x.decrypt('userpw'); print('user permissions with default flags:', int(x.user_access_permissions), '| text readable:', repr(x.pages[0].extract_text()[:12]))
x = pypdf.PdfReader('emptyuser.pdf'); print('empty user password: is_encrypted', x.is_encrypted, '| pages readable without decrypt():', len(x.pages), repr(x.pages[0].extract_text()[:12]), '| qpdf asks for a password:', 'invalid password' in sh(['qpdf', '--check', 'emptyuser.pdf']).stderr)
x = pypdf.PdfReader('aes.pdf'); x.decrypt('swordfish'); w = pypdf.PdfWriter(); w.append(x); w.write('decrypted.pdf'); y = pypdf.PdfReader('decrypted.pdf'); print('decrypted copy: is_encrypted', y.is_encrypted, 'pages', len(y.pages), '| qpdf --check: ', 'File is not encrypted' in sh(['qpdf', '--check', 'decrypted.pdf']).stdout)
try: pypdf.PdfWriter().append('aes.pdf')
except Exception as e: print('append of the encrypted path:', type(e).__name__, e)
print('pdftotext without a password:', sh(['pdftotext', 'aes.pdf', '-']).stderr.strip(), '| with -upw swordfish:', repr(sh(['pdftotext', '-upw', 'swordfish', 'aes.pdf', '-']).stdout[:20]))
print('two PDFs from the same writer differ because of random salts: ', open('aes.pdf', 'rb').read() != (lambda: (enc('aes2.pdf', 'swordfish', algorithm='AES-256'), open('aes2.pdf', 'rb').read())[1])())
'''),
]
PROGS += [
 ("Practice program 1, PDF Paranoia: encrypt every PDF under a folder with a password from the command line, check the copy, delete the original; then decrypt them again, skipping a wrong password", GET + r'''import pypdf
ENC = r"""# paranoia_encrypt.py - encrypts every PDF under a folder; usage: paranoia_encrypt.py <folder> <password>
import os, sys, pypdf
folder_root, password = sys.argv[1], sys.argv[2]
for folder, subfolders, filenames in os.walk(folder_root):
    for filename in filenames:
        if not filename.lower().endswith('.pdf') or filename.lower().endswith('_encrypted.pdf'):
            continue
        path = os.path.join(folder, filename)
        reader = pypdf.PdfReader(path)
        if reader.is_encrypted:
            print('Skipping (already encrypted):', path); continue
        writer = pypdf.PdfWriter()
        writer.append(reader)
        writer.encrypt(password, algorithm='AES-256')
        new_path = path[:-4] + '_encrypted.pdf'
        with open(new_path, 'wb') as file:
            writer.write(file)
        check = pypdf.PdfReader(new_path)
        if check.is_encrypted and check.decrypt(password) != pypdf.PasswordType.NOT_DECRYPTED and len(check.pages) == len(reader.pages):
            os.remove(path); print('Encrypted and removed the original:', path)
        else:
            os.remove(new_path); print('The copy could not be verified, original kept:', path)
"""
DEC = r"""# paranoia_decrypt.py - decrypts copies of every encrypted PDF under a folder; usage: paranoia_decrypt.py <folder> <password>
import os, sys, pypdf
folder_root, password = sys.argv[1], sys.argv[2]
for folder, subfolders, filenames in os.walk(folder_root):
    for filename in filenames:
        if not filename.lower().endswith('.pdf'):
            continue
        path = os.path.join(folder, filename)
        reader = pypdf.PdfReader(path)
        if not reader.is_encrypted:
            continue
        if reader.decrypt(password) == pypdf.PasswordType.NOT_DECRYPTED:
            print('Wrong password for', path, '- continuing'); continue
        writer = pypdf.PdfWriter()
        writer.append(reader)
        out = path[:-len('_encrypted.pdf')] + '_decrypted.pdf' if path.endswith('_encrypted.pdf') else path[:-4] + '_decrypted.pdf'
        with open(out, 'wb') as file:
            writer.write(file)
        print('Decrypted copy:', out)
"""
d = work(); open('paranoia_encrypt.py', 'w').write(ENC); open('paranoia_decrypt.py', 'w').write(DEC)
os.makedirs('tree/sub/deeper'); open('tree/notes.txt', 'w').write('not a pdf')
open('tree/a.pdf', 'wb').write(make_pdf(['A1', 'A2'])); open('tree/sub/b.pdf', 'wb').write(make_pdf(['B1'])); open('tree/sub/deeper/C.PDF', 'wb').write(make_pdf(['C1', 'C2', 'C3']))
w = pypdf.PdfWriter(); w.append(io.BytesIO(make_pdf(['X1']))); w.encrypt('other-password', algorithm='AES-256'); w.write('tree/sub/already.pdf')
def listing(): return sorted(os.path.relpath(os.path.join(a, f), 'tree') for a, _, fs in os.walk('tree') for f in fs)
print('before', listing())
r = sh([LATEST, '-I', 'paranoia_encrypt.py', 'tree', 'swordfish']); print('encrypt exit', r.returncode); print(r.stdout.rstrip()); print(r.stderr.strip()[-200:])
print('after ', listing())
r = sh([LATEST, '-I', 'paranoia_decrypt.py', 'tree', 'wrong']); print('decrypt with a wrong password, exit', r.returncode); print('\n'.join(sorted(r.stdout.rstrip().split('\n'))))
r = sh([LATEST, '-I', 'paranoia_decrypt.py', 'tree', 'swordfish']); print('decrypt with swordfish, exit', r.returncode); print('\n'.join(sorted(r.stdout.rstrip().split('\n'))))
print('after ', listing())
print('texts of the decrypted copies:', {f: [p.extract_text() for p in pypdf.PdfReader('tree/' + f).pages] for f in listing() if f.endswith('_decrypted.pdf')})
print('the password stands in the command line, which any program that lists processes can read (see CWE-214, source in the research record)')
'''),
 ("Practice program 2, Custom Invitations: styles made in code, one invitation per page from guests.txt, the trailing page break, and the pages LibreOffice counts", GET + r'''import docx
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_BREAK, WD_ALIGN_PARAGRAPH
from docx.shared import Pt
work('guests.txt')
raw = open('guests.txt', 'rb').read()
print('guests.txt:', len(raw), 'bytes,', raw.count(b'\n'), 'newlines,', repr(raw.decode().splitlines()), '| the page prints the last name as RoboCop')
t = docx.Document()
for name, size, bold in (('Invite Lead', 16, False), ('Invite Name', 36, True), ('Invite Detail', 14, False)):
    st = t.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH); st.base_style = t.styles['Normal']; st.font.size = Pt(size); st.font.bold = bold; st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
t.save('template.docx')
def make(trailing_break):
    doc = docx.Document('template.docx')
    guests = [g for g in open('guests.txt').read().splitlines() if g.strip()]
    for i, g in enumerate(guests):
        doc.add_paragraph('It would be a pleasure to have the company of', 'Invite Lead')
        doc.add_paragraph(g, 'Invite Name')
        doc.add_paragraph('at 11010 Memory Lane on the Evening of', 'Invite Detail')
        doc.add_paragraph('April 1st', 'Invite Detail')
        last = doc.add_paragraph('at 7 o' + chr(39) + 'clock', 'Invite Detail')
        if trailing_break or i < len(guests) - 1: last.runs[-1].add_break(WD_BREAK.PAGE)
    return doc
import pypdf
for label, tb in (('page break after every invitation, the last one too', True), ('page break between invitations only', False)):
    doc = make(tb); fn = 'invites_%s.docx' % ('all' if tb else 'between'); doc.save(fn)
    sh(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', 'out', fn], timeout=600)
    rd = pypdf.PdfReader('out/' + fn.replace('.docx', '.pdf'))
    print('%-58s paragraphs %d, pages %d, names on the pages %s, last page blank: %s' % (label, len(doc.paragraphs), len(rd.pages), [p.extract_text().split('\n')[1] if len(p.extract_text().split('\n')) > 1 else '' for p in rd.pages], rd.pages[-1].extract_text().strip() == ''))
print('styles of the template: ', [s.name for s in docx.Document('template.docx').styles if s.name.startswith('Invite')], '| styles used by the invitations:', sorted({p.style.name for p in make(False).paragraphs}))
'''),
 ("Practice program 3, PDF Password Breaker: the book's dictionary.txt, what it holds, and the speed of decrypt() with AES-256 and with RC4", GET + r'''import pypdf, time, logging
logging.disable(logging.CRITICAL)
work('dictionary.txt')
words = open('dictionary.txt').read().split('\n'); ws = [w for w in words if w]
print('lines', len(ws), '| unique', len(set(ws)), '| shortest', min(map(len, ws)), 'longest', max(map(len, ws)), '| all lowercase letters:', all(w.isalpha() and w.islower() for w in ws), '| the page says over 44,000 words; this is', round(len(ws) / 44000, 1), 'times that')
print('the first words', ws[:6], '| in the dictionary:', {w: (w in set(ws)) for w in ('swordfish', 'sword', 'fish', 'password', 'recursion', 'dog', 'cat', 'the')})
print('88,000 attempts per the page; both forms of every line are', 2 * len(ws), 'attempts')
def breaker(reader, candidates):
    n = 0
    for word in candidates:
        for form in (word, word.upper()):
            n += 1
            if reader.decrypt(form) != pypdf.PasswordType.NOT_DECRYPTED: return form, n
    return None, n
def make(pw, alg):
    w = pypdf.PdfWriter(); w.append(io.BytesIO(make_pdf(['secret page']))); 
    if alg: w.encrypt(pw, algorithm=alg)
    else: w.encrypt(pw)
    b = io.BytesIO(); w.write(b); return b.getvalue()
for label, alg in (('AES-256', 'AES-256'), ('RC4 (the default)', None)):
    for pw in (ws[2999], ws[1499].upper()):
        data = make(pw, alg); r = pypdf.PdfReader(io.BytesIO(data)); t0 = time.perf_counter(); found, n = breaker(r, ws[:5000]); dt = time.perf_counter() - t0
        print('%-18s password %-10r found %-10r after %5d attempts' % (label, pw, found, n))
        print('MEASURED %s: %.1f ms per attempt, so %d attempts would take %.0f s' % (label, dt / n * 1000, 2 * len(ws), dt / n * 2 * len(ws)))
data = make('swordfish', 'AES-256'); r = pypdf.PdfReader(io.BytesIO(data)); found, n = breaker(r, ws[:3000])
print('the book is encrypted with swordfish, which is not in the dictionary: in the first 3000 words found', found, 'after', n, 'attempts')
'''),
 ("The twelve practice questions answered by code", GET + r'''import docx, pypdf, logging
logging.disable(logging.CRITICAL)
work('Recursion_Chapter1.pdf', 'demo.docx')
w = pypdf.PdfWriter(); w.append('Recursion_Chapter1.pdf', (0, 2))
try:
    with open('t.pdf', 'w') as f: w.write(f)
except Exception as e: print('Q1 text mode "w":', type(e).__name__, str(e)[:60])
with open('t.pdf', 'wb') as f: print('Q1 "wb":', w.write(f)[0])
r = pypdf.PdfReader('Recursion_Chapter1.pdf'); print('Q2 page 5 is reader.pages[4]:', r.pages[4].extract_text()[:12].replace('\n', ' '), '| the same on a writer:', w.pages[1] is not None, '| there is no page index 18:', end=' ')
try: r.pages[18]
except IndexError as e: print(type(e).__name__)
e = pypdf.PdfWriter(); e.append('Recursion_Chapter1.pdf', (0, 1)); e.encrypt('swordfish', algorithm='AES-256'); e.write('enc.pdf')
x = pypdf.PdfReader('enc.pdf')
try: x.pages[0]
except Exception as ex: print('Q3 before decrypt:', type(ex).__name__)
print('Q3 x.decrypt("swordfish") ->', x.decrypt('swordfish').name, '| then page 1 text', repr(x.pages[0].extract_text()[:8]))
p = pypdf.PdfWriter(); p.append('Recursion_Chapter1.pdf', (0, 1)); p.pages[0].rotate(-90); print('Q4 rotate(-90): rotation', p.pages[0].rotation, '(stored as written; the viewer shows the page turned a quarter turn counterclockwise)')
d = docx.Document('demo.docx'); print('Q5 docx.Document("demo.docx") ->', type(d).__module__ + '.' + type(d).__name__)
para = d.paragraphs[1]; print('Q6 a Paragraph holds Runs:', type(para).__name__, len(para.runs), 'runs; a Run is one stretch of one style:', [(r.text, r.bold, r.italic) for r in para.runs])
print('Q7 doc.paragraphs ->', type(d.paragraphs).__name__, len(d.paragraphs))
run = para.runs[1]
print('Q8 attributes on a Run:', [a for a in ('bold', 'underline', 'italic', 'strike', 'outline') if hasattr(run, a) and a in dir(type(run))], '| the rest are on run.font:', [a for a in ('strike', 'outline') if a in dir(type(run.font))])
fresh = docx.Document().add_paragraph('x').add_run('y')
print('Q9 None/True/False:', [(v, (setattr(fresh, 'bold', v), fresh.bold)[1]) for v in (True, False, None)])
print('Q10 docx.Document() ->', len(docx.Document().paragraphs), 'paragraphs')
n = docx.Document(); print('Q11 doc.add_paragraph("Hello, there!") ->', repr(n.add_paragraph('Hello, there!').text))
levels = []
for i in range(-1, 11):
    try: n.add_heading('h', i); levels.append(i)
    except ValueError: pass
print('Q12 heading levels accepted:', levels, '(0 is the Title style)')
'''),
]
PROGS += [
 ("The pdfminer.six fallback of the chapter's listing: the same text from both libraries on the shipped PDF, and eleven damaged files given to both", GET + r'''import pypdf, logging
import pdfminer.high_level as hl, pdfminer
logging.disable(logging.CRITICAL)
work('Recursion_Chapter1.pdf')
a = ''.join(p.extract_text() for p in pypdf.PdfReader('Recursion_Chapter1.pdf').pages); b = hl.extract_text('Recursion_Chapter1.pdf')
print('pypdf: characters %d, words %d, form feeds %d | pdfminer.six: characters %d, words %d, form feeds %d' % (len(a), len(a.split()), a.count('\x0c'), len(b), len(b.split()), b.count('\x0c')))
print('pypdf starts', repr(a[:60]))
print('pdfminer starts', repr(b[:90]))
print('the chapter heading in pdfminer is spaced:', 'W H A T   I S   R E C U R S I O N ?' in b, '| in pypdf it is intact:', 'WHAT IS RECURSION?' in a)
good = make_pdf(['Page one', 'Page two'])
variants = [('intact', good), ('truncated before xref', good[:good.index(b'xref')]), ('startxref points elsewhere', re.sub(rb'startxref\n\d+', b'startxref\n5', good)), ('no startxref and trailer', good[:good.index(b'xref')] + b'%%EOF'),
            ('garbage before the header', b'garbage\n' * 50 + good), ('page tree without /Type /Pages', good.replace(b'/Type /Pages', b'/Type /Foo')), ('wrong stream /Length', good.replace(b'/Length 38', b'/Length 5')), ('empty file', b''),
            ('text that is not a PDF', b'hello world'), ('page without /Contents', good.replace(b'/Contents 5 0 R', b'')), ('page with no font resource', good.replace(b'/Font << /F1 3 0 R >>', b'/Font << >>'))]
both_fail = only_pypdf_fails = only_pdfminer_fails = 0
for label, data in variants:
    res = []
    try: res.append('pypdf ' + repr(''.join(p.extract_text() for p in pypdf.PdfReader(io.BytesIO(data)).pages)[:24]))
    except Exception as e: res.append('pypdf raises ' + type(e).__name__)
    try: res.append('pdfminer ' + repr(hl.extract_text(io.BytesIO(data))[:24]))
    except Exception as e: res.append('pdfminer raises ' + type(e).__name__)
    f1, f2 = 'raises' in res[0], 'raises' in res[1]
    both_fail += f1 and f2; only_pypdf_fails += f1 and not f2; only_pdfminer_fails += f2 and not f1
    print('%-32s %s | %s' % (label, res[0], res[1]))
print('pypdf raises and pdfminer succeeds (the case the fallback is for):', only_pypdf_fails, '| both raise:', both_fail, '| only pdfminer raises:', only_pdfminer_fails)
'''),
]
def run(code):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1"); env.pop("PYTHONPATH", None)
    r = subprocess.run([PY, "-W", "ignore", "-c", code], capture_output=True, text=True, env=env, timeout=1800, cwd=tempfile.mkdtemp())
    o = (r.stdout if r.returncode == 0 else r.stdout + "FAILED: " + (r.stderr.strip().splitlines() or ["?"])[-1]).rstrip("\n")
    return re.sub(r"0x[0-9a-f]{6,}", "0x...", o)   # the address of an object differs from run to run
if __name__ == "__main__":
    out = [{"what": w, "code": c, "output": run(c)} for w, c in PROGS]
    strip = lambda s: "\n".join(l for l in s.split("\n") if not l.startswith("MEASURED"))
    if MODE == "write":
        ver = subprocess.run([PY, "-c", "import sys, pypdf, docx, importlib.metadata as m; print(sys.version.split()[0], 'pypdf', pypdf.__version__, 'python-docx', m.version('python-docx'))"], capture_output=True, text=True).stdout.strip()
        json.dump({"_version": "1.0.0", "_note": "Recorded by sen0414_ch17_thirdparty_v1_0_0.py write; every output was printed by the program beside it under the interpreter named in the field python. The chapter page and the online materials are fetched at run time and not kept in the repository. A line that starts with MEASURED is a timing on the machine of the day.", "python": ver, "items": out}, open(REC, "w"), indent=1, ensure_ascii=False)
        print("recorded", len(out), "programs to", REC)
        for o in out:
            if "FAILED" in o["output"]: print("  FAILED:", o["what"], "|", o["output"][-200:])
    else:
        old = json.load(open(REC))["items"]; bad = [a["what"] for a, b in zip(old, out) if strip(a["output"]) != strip(b["output"]) or a["code"] != b["code"]]
        print("%d programs; %d differ" % (len(out), len(bad)))
        for b in bad: print("  DIFFERS", b)
        sys.exit(1 if bad else 0)

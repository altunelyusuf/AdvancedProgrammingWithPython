#!/usr/bin/env python3
"""Chapter 18 (CSV, JSON, and XML Files): runs the chapter's own programs, whole, and the chapter's interactive statements, under the given
interpreter, and writes or checks their recorded output.
What is fetched at run time and kept in a cache directory (CH18_CACHE, default the system temp directory): the chapter page
(https://automatetheboringstuff.com/3e/chapter18.html, its sha256 is compared with the chapterDigest of the book's own chapter ontology), the
table of contents (https://automatetheboringstuff.com/3e/) and the zip of the 3rd edition's online materials (No Starch Press, sha256 dac627e8...a916)
that holds the files the chapter uses (exampleWithHeader3.csv, example3.xlsx, removeCsvHeader.zip, excelSpreadsheets.zip, censuspopdata.xlsx,
produceSales3.xlsx) and the book's own script removeCsvHeader.py. None of those files is stored in the repository; every file is checked against the
sha256 recorded here before it is used. The chapter ships no example3.csv, no my_data.xml and no JSON or XML file; the programs make them from the
text the chapter prints.
Three environments, all Python 3.14.6 installed with uv, are named by environment variables:
  LATEST  the newest releases on 2026-10-12: xmltodict 1.0.4, openpyxl 3.1.5, defusedxml 0.7.1, lxml 6.1.3 (xml.etree, csv and json are the standard library)
  PINS    the versions Appendix A of the book pins: xmltodict 0.13.0, openpyxl 3.1.5
  BARE    no package at all, to see what a reader gets who has not installed xmltodict
The environments are named by CH18_LATEST, CH18_PINS and CH18_BARE (paths of their python), defaults /home/claude/venv314_ch18_latest/bin/python,
/home/claude/venv314_ch18_pins/bin/python and /home/claude/venv314_ch18_bare/bin/python.
Not executed here: Microsoft Excel itself (Figure 18-1 is a picture of it), Windows (the double-spaced file of Figure 18-1 is reproduced by writing
the line ending Windows text mode writes), the Mu editor, a display of any file in a browser.
A line that starts with MEASURED is a timing; it is recorded and is not compared by the check.
Usage: sen0414_ch18_thirdparty_v1_0_0.py write|check [python]   (python defaults to the LATEST environment)
Record: 08-tooling/ch18-page/third_party_record_v1_0_0.json"""
__version__ = "1.0.0"
import json, os, re, subprocess, sys, tempfile
MODE = sys.argv[1] if len(sys.argv) > 1 else "check"
LATEST = os.environ.get("CH18_LATEST", "/home/claude/venv314_ch18_latest/bin/python")
PINS = os.environ.get("CH18_PINS", "/home/claude/venv314_ch18_pins/bin/python")
BARE = os.environ.get("CH18_BARE", "/home/claude/venv314_ch18_bare/bin/python")
PY = sys.argv[2] if len(sys.argv) > 2 else LATEST
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REC = os.path.join(REPO, "08-tooling", "ch18-page", "third_party_record_v1_0_0.json")
GET = r'''import os, io, zipfile, hashlib, shutil, tempfile, urllib.request, html, re, json, subprocess, sys, contextlib, warnings
UA = 'Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0'
CACHE = os.environ.get('CH18_CACHE') or tempfile.gettempdir()
ZIPSHA = 'dac627e807f69ee14913ba621a15dec1f98db739d76939555ba5360d05eba916'
SHA = {'exampleWithHeader3.csv': '4d238719835ede046f0bb0cbf8806c572a04925f35ee29633127e93792728b7f', 'example3.xlsx': 'b1dc19bd6286554124dff48ef3bb5c5f547afd0168f01943e384ba2400eeebfa',
       'removeCsvHeader.py': 'ac28848d5450c3ecb962243a62444fa25e456ebb39834fb23dcdacd27e34a180', 'removeCsvHeader.zip': '484771efbcd87f89566f7e55928635f14594674622056200017c4cef712e6d3e',
       'excelSpreadsheets.zip': '828f30a2d42d2616e5c67d97f1d9832d5b93609e2a0cddee6cda0530d326abef', 'produceSales3.xlsx': 'bdf2349a380c70f76ecf5ab0a793c5a3f35144c16dca14816af252d94e07b17e',
       'demo.docx': 'b43b21137d7d69b16e9e1ec7ebb75e0e2f053d8947cd2ddcf79d60a0dfe5f121',
       'censuspopdata.xlsx': 'f5e649370d4ed3878240ee7ead2a0c9ddd8a41da839b905f8fc17c3e664ba439'}
PREFIX = 'Automate_the_Boring_Stuff_3e_onlinematerials/'
LATEST = os.environ.get('CH18_LATEST', '/home/claude/venv314_ch18_latest/bin/python')
PINS = os.environ.get('CH18_PINS', '/home/claude/venv314_ch18_pins/bin/python')
BARE = os.environ.get('CH18_BARE', '/home/claude/venv314_ch18_bare/bin/python')
def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=120).read()
def cached(name, url):
    p = os.path.join(CACHE, name)
    if not os.path.exists(p):
        open(p + '.part', 'wb').write(fetch(url)); os.replace(p + '.part', p)
    return open(p, 'rb').read()
def chapter(): return cached('ch18_chapter.html', 'https://automatetheboringstuff.com/3e/chapter18.html')
def toc(): return cached('ch18_toc.html', 'https://automatetheboringstuff.com/3e/')
def materials():
    p = os.path.join(CACHE, 'ch18_materials.zip')
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
    return subprocess.run(cmd, capture_output=True, text=True, **k)
def unmark(text):
    """the book's numbered markers stand in the margin: at the start of a line they are dropped, after indentation they count as two columns"""
    out = []
    for ln in text.split('\n'):
        m = re.match(r'^(\s*)[❶-❿] ', ln)
        out.append((ln[m.end():] if not m.group(1) else m.group(1) + '  ' + ln[m.end():]) if m else ln)
    return '\n'.join(out)
def listing_removeCsvHeader():
    """Project 13 as the three steps print it, put together: step 1 up to its TODO, the body of step 2, the body of step 3"""
    P = pres(); s1, s2, s3 = unmark(P[12]), unmark(P[13]), unmark(P[14])
    head = s1.split('    # TODO: Read the CSV file')[0].rstrip() + '\n\n'
    mid = s2.split('--snip--', 1)[1].split('    # TODO: Write the CSV file.')[0].strip('\n')
    tail = s3.rsplit('--snip--', 1)[1].strip('\n')
    return head + mid + '\n\n' + tail + '\n'
CHAPTER_CSV = None
def printed_csv():
    return pres()[0]
def make_example3():
    """example3.csv as the reader makes it: the text the chapter prints, saved with a text editor (one line feed at the end of each row)"""
    open('example3.csv', 'w', newline='').write(printed_csv().rstrip('\n') + '\n')
def make_my_data():
    """my_data.xml as the reader makes it: the XML the chapter prints before 'Reading XML Files'"""
    open('my_data.xml', 'w', encoding='utf-8').write(pres()[20].rstrip('\n') + '\n')
'''
REPLAY = r'''PRES = pres()
MARK = re.compile('[❶-❿][ \t]?')
def parse(block, join=''):
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
            cur['src'] += join + ln
            if complete(cur['src']): cur['open'] = False
            continue
        if ln.startswith('...') and cur is not None: continue
        if cur is not None: cur['out'].append(ln)
    return items
def norm(t):
    t = re.sub(r'\s+', '', t)
    t = re.sub(r'0x[0-9A-Fa-f]+', '0xADDR', t)
    return t
def match(expected, got):
    e = norm('\n'.join(expected)); g = norm(got)
    if '--snip--' in e:
        a, b = e.split('--snip--', 1)
        return 'match' if g.startswith(a) and g.endswith(b) else 'differs'
    return 'match' if e == g else 'differs'
def replay(skip=(), label='', repair=False):
    d = work('exampleWithHeader3.csv'); make_example3(); make_my_data(); ns = {'__name__': '__main__'}; rows = []
    for bi, blk in enumerate(PRES):
        if bi in skip: continue
        if '>>> ' not in MARK.sub('', blk)[:12]: continue
        for it in parse(blk):
            src = it['src'].replace('\u201d', '"') if repair else it['src']; buf = io.StringIO()
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
    print(label + 'statements', len(rows), dict(sorted(c.items())))
    for bi, src, exp, got, v in rows:
        if v != 'match':
            one = lambda s: re.sub(r'\s+', ' ', s)[:130]
            print('block %d %s | %s | printed: %s | got: %s' % (bi, v, one(src), one(exp), one(got)))
'''
PROGS = []
PROGS += [
 ("The environments: interpreter, packages and their versions, in the three environments of the study", GET + r'''for name, py in (('LATEST', LATEST), ('PINS', PINS), ('BARE', BARE)):
    r = sh([py, '-I', '-c', "import sys, importlib.metadata as m\nd = {x.metadata['Name']: x.version for x in m.distributions()}\nprint(sys.version.split()[0], dict(sorted(d.items())))"])
    print(name, r.stdout.strip() or r.stderr.strip()[-200:])
r = sh([LATEST, '-I', '-c', "import sys, csv, json, xml.etree.ElementTree as ET, pyexpat, platform\nprint('csv version', csv.__version__, '| json version', json.__version__, '| expat', pyexpat.EXPAT_VERSION, '| _elementtree C accelerator', ET.Element.__module__, '|', platform.system(), platform.release())"])
print(r.stdout.strip() or r.stderr.strip()[-200:])
'''),
 ("The chapter page: size, sha256 against the chapterDigest of the book's chapter ontology, what it holds and the chapter numbers it names", GET + r'''h = chapter(); d = hashlib.sha256(h).hexdigest()
P = pres(); t = h.decode('utf-8'); txt = html.unescape(re.sub(r'<[^>]+>', '', t))
repl = [p for p in P if re.sub('[❶-❿] ?', '', p).lstrip().startswith('>>>')]
print(len(h), d, d == 'c998127be7342ac419f9f884a60aea6ef837e3dba1c2deada1e977a6a20a01dc')
print('pre blocks', len(P), 'interactive', len(repl), 'figures', sorted(set(re.findall(r'Figure 18-\d+', txt))), 'tables', len(re.findall(r'<table\b', t)))
print('statements', sum(1 for p in repl for ln in re.sub('[❶-❿] ?', '', p).split('\n') if ln.startswith('>>> ')))
print('chapter images (not the book covers):', [re.search(r'src="([^"]+)"', i).group(1) + ' alt=' + repr((re.search(r'alt="([^"]*)"', i) or [0, None])[1]) for i in re.findall(r'<img\b[^>]*>', t) if 'cover-' not in i])
print('practice questions', len(re.findall(r'^\s*\d+\.\s{2}', txt, re.M)), '| headings', [re.sub(r'<[^>]+>', '', x).strip() for x in re.findall(r'<h[345][^>]*>.*?</h[345]>', t, re.S)])
toc_t = html.unescape(re.sub(r'<[^>]+>', '\n', toc().decode('utf-8')))
titles = dict(re.findall(r'Chapter (\d+) - ([^\n]+)', toc_t))
for m in re.finditer(r'[^.]*\bChapter (\d+)\b[^.]*\.', txt):
    s = re.sub(r'\s+', ' ', m.group()).strip()
    if 'Chapter 18' in s and 'CSV, JSON' in s: continue
    print('names chapter', m.group(1), '(%s):' % titles.get(m.group(1)), s[:170])
print('Appendix B answers for chapter 18 are on the page:', 'appendixb' in t)
'''),
 ("The online materials of the 3rd edition: the zip and the files in it that chapter 18 uses, and the files the chapter needs that are not in it", GET + r'''p = materials(); b = open(p, 'rb').read()
z = zipfile.ZipFile(p)
print(len(b), hashlib.sha256(b).hexdigest())
names = [n for n in z.namelist() if not n.endswith('/') and '/._' not in n and not n.split('/')[-1].startswith('._')]
print(len(names), 'files')
for n in sorted(names):
    f = n.split('/')[-1]
    if f in SHA or re.search(r'\.(csv|json|xml|tsv)$|^example|header|excel|NAICS|my_data|produce|census', f, re.I):
        x = z.read(n); print(f, len(x), hashlib.sha256(x).hexdigest()[:16], 'recorded' if f in SHA and hashlib.sha256(x).hexdigest() == SHA[f] else 'not recorded')
for want in ('example3.csv', 'my_data.xml', 'output.csv', 'example3.xlsx', 'exampleWithHeader3.csv', 'removeCsvHeader.zip', 'excelSpreadsheets.zip'):
    print(want, 'is in the zip:', any(n.endswith('/' + want) for n in names))
print('any .json or .xml file in the zip:', [n for n in names if re.search(r'\.(json|xml)$', n)])
'''),
 ("The shipped files: exampleWithHeader3.csv (bytes, line endings, year), example3.xlsx (cells and formats), what the two zips really contain", GET + r'''d = work('exampleWithHeader3.csv', 'example3.xlsx', 'removeCsvHeader.zip', 'excelSpreadsheets.zip')
b = open('exampleWithHeader3.csv', 'rb').read(); print('exampleWithHeader3.csv', len(b), 'bytes; CRLF line endings', b.count(b'\r\n'), '; bare LF', b.count(b'\n') - b.count(b'\r\n'), '; years in the file', sorted(set(re.findall(rb'/(\d{4}) ', b))), '; first line', b.split(b'\r\n')[0])
printed = pres()[0]; print('the chapter prints years', sorted(set(re.findall(r'/(\d{4}) ', printed))), 'and the shipped file has', len(b.decode().strip().split('\r\n')) - 1, 'data rows against', len(printed.strip().split('\n')), 'printed rows')
print('rows equal apart from the year:', [r.replace('/2025 ', '/2035 ') for r in b.decode().strip().split('\r\n')[1:]] == printed.strip().split('\n'))
import openpyxl
wb = openpyxl.load_workbook('example3.xlsx'); ws = wb['Sheet1']
print('example3.xlsx sheets', wb.sheetnames, '| Sheet1 size', ws.max_row, ws.max_column)
for row in ws.iter_rows():
    print([(c.value.isoformat() if hasattr(c.value, 'isoformat') else c.value) for c in row], '| number format of A:', row[0].number_format)
for zn in ('removeCsvHeader.zip', 'excelSpreadsheets.zip'):
    z = zipfile.ZipFile(zn); L = z.infolist()
    kinds = {}
    for i in L:
        head = z.read(i.filename)[:4]; k = os.path.splitext(i.filename)[1] + ' ' + ('PK (a ZIP or Office file)' if head[:2] == b'PK' else 'plain text' if all(32 <= c < 127 or c in (9, 10, 13) for c in z.read(i.filename)[:200]) else 'binary')
        kinds[k] = kinds.get(k, 0) + 1
    print(zn, len(L), 'members; extensions and content:', kinds, '| first', L[0].filename, '| last', L[-1].filename)
print('excelSpreadsheets.zip holds any .xlsx member:', any(i.filename.endswith('.xlsx') for i in zipfile.ZipFile('excelSpreadsheets.zip').infolist()))
'''),
 ("Every statement of the chapter's interactive listings, replayed in the order the page prints them, exactly as printed (the curly quotation mark of the two xml_string literals stays), under the newest releases", GET + r'''import xmltodict
''' + REPLAY + r'''replay(label='as printed, in the order of the page: ')
'''),
 ("The same replay with the curly closing quotation mark of the two xml_string literals replaced by a straight one, still in the order of the page (my_data.xml is parsed before root is used again)", GET + r'''import xmltodict
''' + REPLAY + r'''replay(label='quotation mark repaired, in the order of the page: ', repair=True)
'''),
 ("The same replay, quotation mark repaired, with the one statement block that rebinds root (ET.parse of my_data.xml) left out, so that root stays the Element parsed from the string", GET + r'''import xmltodict
''' + REPLAY + r'''replay(skip=(25,), label='quotation mark repaired, without the parse() block: ', repair=True)
'''),
 ("The two repaired replays under the versions Appendix A of the book pins (xmltodict 0.13.0, openpyxl 3.1.5), with the interpreter 3.14.6", GET + "CHILD = %r\n" % (GET + "import xmltodict, importlib.metadata as md\nprint('xmltodict', md.version('xmltodict'))\n" + REPLAY + "replay(label='quotation mark repaired, in the order of the page: ', repair=True)\nreplay(skip=(25,), label='quotation mark repaired, without the parse() block: ', repair=True)\n") + r'''r = subprocess.run([PINS, '-I', '-c', CHILD], capture_output=True, text=True, env=dict(os.environ, CH18_CACHE=CACHE))
print(r.stdout.strip() or r.stderr.strip()[-600:])
'''),
 ("The statements the page cannot hold as typed: json_string wrapped over four lines, and the two xml_string literals with their curly closing quotation mark", GET + r'''import xml.etree.ElementTree as ET, json, xmltodict
from xml.parsers.expat import ExpatError
P = pres(); MK = re.compile('[❶-❿][ \t]?')
js = re.search(r"json_string = '.*?\}\]\}'", MK.sub('', P[18]), re.S).group()
print('json_string as typed: %d lines, %d line breaks inside the quotes' % (len(js.split('\n')), js.count('\n')))
try: compile(js, '<typed>', 'exec')
except SyntaxError as e: print('as typed:', type(e).__name__, e.msg)
good = js.replace('\n', ''); ns = {}; exec(good, ns); print('line breaks removed:', json.loads(ns['json_string'])['address'], '| the string has', len(ns['json_string']), 'characters')
for bi in (24, 31):
    xs = re.search(r'xml_string = (""".*?""")', MK.sub('', P[bi]), re.S).group(1); lit = eval(xs)
    print('block %d xml_string: %d line breaks in the string, curly quotes %s' % (bi, lit.count('\n'), [c for c in lit if c in '\u201c\u201d']))
    parse = ET.fromstring if bi == 24 else xmltodict.parse
    try: parse(lit); print('  as typed: parsed')
    except (ET.ParseError, ExpatError) as e: print('  as typed:', type(e).__module__ + '.' + type(e).__name__, e)
    straight = lit.replace('\u201d', '"')
    r = parse(straight)
    if bi == 24: print('  curly quote replaced, line breaks kept: street text', repr(r[4][0].text), '| first phone number', repr(list(r.iter('number'))[0].text), '| zip', repr(list(r.iter('zip'))[0].text))
    else: print('  curly quote replaced, line breaks kept:', {k: r['person']['address'][k] for k in r['person']['address']}, list(r['person']['phone']['phoneEntry'][0].items()))
    flat = parse(straight.replace('\n', ''))
    if bi == 24: print('  curly quote replaced, line breaks removed: street text', repr(flat[4][0].text), '| first phone number', repr(list(flat.iter('number'))[0].text))
    else: print('  curly quote replaced, line breaks removed:', dict(flat['person']['address']), list(flat['person']['phone']['phoneEntry'][0].items()))
'''),
]
PROGS += [
 ("Reading CSV: what csv.reader returns, that every value is a string, that a reader is used once, that a filename string is not refused, a closed file, and why split(',') is not enough", GET + r'''import csv
d = work(); make_example3()
with open('example3.csv') as f: data = list(csv.reader(f))
print(len(data), 'rows;', 'first row', data[0], '| types in the first row', [type(v).__name__ for v in data[0]], '| row 6 col 1', data[6][1])
f = open('example3.csv'); r = csv.reader(f); a = list(r); b = list(r); f.close()
print('first list() gives', len(a), 'rows, a second list() on the same reader gives', len(b), '| type of the reader', type(r).__name__, '| has __len__', hasattr(r, '__len__'), '| has __getitem__', hasattr(r, '__getitem__'))
rows = list(csv.reader('example3.csv')); print('csv.reader(<the filename string>) is not refused: it iterates over the characters,', len(rows), 'rows, the first three', rows[:3])
print('csv.reader over a list of strings:', list(csv.reader(['a,b', 'c,"d,e"', ''])))
f = open('example3.csv'); r = csv.reader(f); f.close()
try: next(r)
except ValueError as e: print('reading after close():', type(e).__name__, e)
line = '"Hello, world!",eggs,bacon,ham'
print('split(",") :', line.split(','), '| csv.reader:', next(csv.reader([line])))
print('line_num starts at', csv.reader([]).line_num, 'and after one row of a file reads', end=' ')
f = open('example3.csv'); r = csv.reader(f); next(r); print(r.line_num, end=' | after all rows '); list(r); print(r.line_num); f.close()
print('csv.reader needs a text file; a file opened in binary mode:', end=' ')
try:
    with open('example3.csv', 'rb') as g: next(csv.reader(g))
except csv.Error as e: print(type(e).__name__, e)
print('a bare carriage return inside an unquoted field of a line read without newline="":', end=' ')
try: list(csv.reader(['a,b\rc,d\n']))
except csv.Error as e: print(type(e).__name__, e)
print('empty line gives', list(csv.reader(['', 'x']))[0], '| a file without the final line feed:', list(csv.reader(['a,b', 'c,d'])))
'''),
 ("line_num is the number of lines read, not the number of records: a header cell with a line break, and the book's Project 13 test against it", GET + r'''import csv, io
text = '"Name\n(first)",Age\nAlice,30\nBob,25\n'
r = csv.reader(io.StringIO(text)); rows = []
for row in r:
    print('record', row, '| line_num', r.line_num)
r = csv.reader(io.StringIO(text)); kept = []
for row in r:
    if r.line_num == 1: continue
    kept.append(row)
print("the book's test (line_num == 1) keeps", len(kept), 'of 3 records and the header is still there:', kept[0])
r = csv.reader(io.StringIO(text)); next(r, None); print('next(reader, None) skips the header record:', list(r))
r = csv.DictReader(io.StringIO(text)); print('DictReader on it: fieldnames', r.fieldnames, '| rows', [dict(x) for x in r], '| line_num after', r.line_num)
print('the same text with a normal one-line header, the book test works:', end=' ')
r = csv.reader(io.StringIO('Name,Age\nAlice,30\nBob,25\n')); print([row for row in r if r.line_num != 1])
'''),
 ("Writing CSV: output.csv byte for byte, the return values of writerow, what the writer quotes, what it does to None, True and floats, and what reading it back returns", GET + r'''import csv
d = work()
f = open('output.csv', 'w', newline=''); w = csv.writer(f)
print(w.writerow(['spam', 'eggs', 'bacon', 'ham']), w.writerow(['Hello, world!', 'eggs', 'bacon', 'ham']), w.writerow([1, 2, 3.141592, 4])); f.close()
b = open('output.csv', 'rb').read(); print(b); print('the book prints these three lines; the file has CRLF line endings:', b.count(b'\r\n'), 'and', len(b), 'bytes')
f = open('output.csv', newline=''); back = list(csv.reader(f)); f.close(); print('read back', back, '| types', [type(v).__name__ for v in back[2]])
import io
def line(row, **k):
    s = io.StringIO(newline=''); csv.writer(s, **k).writerow(row); return s.getvalue()
print([line(['a b', ' lead', 'trail ', '']), line(['say "hi"', 'x']), line(['two\nlines', 'x']), line([None, True, 1.0, 10**20, 1e-7, 2.50]), line(['É', 'ü', '日本']), line([['x', 1], ('t',)]), line(['a,b'], delimiter=';'), line(['a;b', 'c'], delimiter=';')])
print('writerows and a generator:', end=' '); s = io.StringIO(newline=''); w = csv.writer(s); w.writerows((i, i * i) for i in range(3)); print(repr(s.getvalue()))
print('a dict as a row writes its keys:', repr(line({'a': 1, 'b': 2})))
print('writerow(5):', end=' ')
try: csv.writer(io.StringIO()).writerow(5)
except csv.Error as e: print(type(e).__name__, e)
print('writing to a file opened with "rb":', end=' ')
try: csv.writer(open('output.csv', 'rb')).writerow(['x'])
except Exception as e: print(type(e).__module__ + '.' + type(e).__name__, e)
'''),
 ("Figure 18-1: the double-spaced file. What the line ending of Windows text mode does to the writer's CRLF, shown in bytes, in what csv.reader returns, and in the rows a spreadsheet program (LibreOffice 24.2) opens", GET + r'''import csv, openpyxl
d = work()
rows = [['spam', 'eggs', 'bacon', 'ham'], ['Hello, world!', 'eggs', 'bacon', 'ham'], [1, 2, 3.141592, 4]]
for label, nl in (('newline="" (the book)', ''), ('Windows text mode, no newline argument: every "\\n" becomes "\\r\\n"', '\r\n'), ('Linux text mode, no newline argument', None)):
    name = 'out_%s.csv' % ('empty' if nl == '' else 'crlf' if nl == '\r\n' else 'default')
    with open(name, 'w', newline=nl) as f:
        w = csv.writer(f); [w.writerow(r) for r in rows]
    b = open(name, 'rb').read()
    print(label, '->', b[:22], '... CRLF', b.count(b'\r\n'), 'CRCRLF', b.count(b'\r\r\n'), '| csv.reader sees', len(list(csv.reader(open(name, newline='')))), 'rows incl. empty ones', [len(r) for r in csv.reader(open(name, newline=''))])
r = sh(['soffice', '--headless', '--convert-to', 'xlsx', '--outdir', 'conv', 'out_crlf.csv', 'out_empty.csv'], timeout=300)
for n in ('out_empty', 'out_crlf'):
    ws = openpyxl.load_workbook('conv/%s.xlsx' % n).active
    print('LibreOffice opens', n + '.csv', 'as', ws.max_row, 'rows:', [[c.value for c in row] for row in ws.iter_rows()])
print('Figure 18-1 shows rows 1, 3 and 5 filled and rows 2 and 4 empty: the CRCRLF file gives the same layout')
'''),
 ("Using tabs instead of commas: output.tsv byte for byte, the return values 21, 30 and 16, reading it back with the default delimiter and with delimiter='\\t', and the dialect excel-tab", GET + r'''import csv, io
d = work()
f = open('output.tsv', 'w', newline=''); w = csv.writer(f, delimiter='\t', lineterminator='\n\n')
print(w.writerow(['spam', 'eggs', 'bacon', 'ham']), w.writerow(['Hello, world!', 'eggs', 'bacon', 'ham']), w.writerow([1, 2, 3.141592, 4])); f.close()
b = open('output.tsv', 'rb').read(); print(b)
print('the page prints the file as:', repr(pres()[7][:60]))
print('read with csv.reader defaults:', list(csv.reader(open('output.tsv', newline=''))))
print('read with delimiter="\\t":   ', list(csv.reader(open('output.tsv', newline=''), delimiter='\t')))
print('read with delimiter="\\t" and lineterminator="\\n\\n" (the reader ignores lineterminator):', list(csv.reader(open('output.tsv', newline=''), delimiter='\t', lineterminator='\n\n')) == list(csv.reader(open('output.tsv', newline=''), delimiter='\t')))
print('empty rows in the file:', sum(1 for r in csv.reader(open('output.tsv', newline=''), delimiter='\t') if r == []))
s = io.StringIO(newline=''); csv.writer(s, dialect='excel-tab').writerow(['a', 'b c', 'd\te']); print('dialect excel-tab:', repr(s.getvalue()), '| dialects registered', sorted(csv.list_dialects()))
print('the delimiter must be one character:', end=' ')
try: csv.writer(io.StringIO(), delimiter='\t\t')
except TypeError as e: print(type(e).__name__, e)
'''),
 ("DictReader and DictWriter: the list the chapter prints against the list the shipped file gives, fieldnames, restkey and restval, missing and extra keys, DictWriter return values, row type", GET + r'''import csv, io
d = work('exampleWithHeader3.csv'); make_example3()
f = open('exampleWithHeader3.csv'); rd = csv.DictReader(f); data = list(rd); f.close()
print('the shipped file gives', len(data), 'dictionaries; the page prints 6 (it leaves out the first row, 4/5 13:34 Apples 73); fieldnames', rd.fieldnames, '| row type', type(data[0]).__name__)
print('the page prints', len(re.findall(r"\{'Timestamp'", pres()[8].split('...')[0])), 'dictionaries in the first list; the loop below it prints', len([l for l in pres()[8].split('\n') if re.match(r'4/\d+/2035', l)]), 'lines')
f = open('example3.csv'); rd = csv.DictReader(f, ['time', 'name', 'amount']); r0 = next(rd); print('with the made-up headers', r0, '| fieldnames', rd.fieldnames); f.close()
f = open('example3.csv'); rd = csv.DictReader(f); print('without headers the first row becomes the keys:', rd.fieldnames); f.close()
print('a row longer than the header:', list(csv.DictReader(io.StringIO('a,b\n1,2,3,4\n'))), '| with restkey', list(csv.DictReader(io.StringIO('a,b\n1,2,3,4\n'), restkey='extra')))
print('a row shorter than the header:', list(csv.DictReader(io.StringIO('a,b,c\n1\n'))), '| with restval', list(csv.DictReader(io.StringIO('a,b,c\n1\n'), restval='?')))
print('a blank line is skipped by DictReader:', list(csv.DictReader(io.StringIO('a,b\n\n1,2\n'))))
print('duplicate header names, the last value wins:', list(csv.DictReader(io.StringIO('a,a\n1,2\n'))))
print('a header-only file:', list(csv.DictReader(io.StringIO('a,b\n'))), '| an empty file: fieldnames', csv.DictReader(io.StringIO('')).fieldnames)
f = open('output.csv', 'w', newline=''); w = csv.DictWriter(f, ['Name', 'Pet', 'Phone'])
print(w.writeheader(), w.writerow({'Name': 'Alice', 'Pet': 'cat', 'Phone': '555-1234'}), w.writerow({'Name': 'Bob', 'Phone': '555-9999'}), w.writerow({'Phone': '555-5555', 'Name': 'Carol', 'Pet': 'dog'})); f.close()
print(open('output.csv', 'rb').read())
try: csv.DictWriter(io.StringIO(), ['Name']).writerow({'Name': 'x', 'Age': 1})
except ValueError as e: print('an extra key:', type(e).__name__, e)
s = io.StringIO(newline=''); csv.DictWriter(s, ['Name'], extrasaction='ignore').writerow({'Name': 'x', 'Age': 1}); print('extrasaction="ignore":', repr(s.getvalue()), '| restval="n/a" for a missing key:', end=' ')
s = io.StringIO(newline=''); csv.DictWriter(s, ['a', 'b'], restval='n/a').writerow({'a': 1}); print(repr(s.getvalue()))
try: csv.DictWriter(io.StringIO(), ['a']).writerow(['not', 'a', 'dict'])
except Exception as e: print('a list given to DictWriter.writerow:', type(e).__name__, e)
print('a BOM at the start of the file becomes part of the first key:', list(csv.DictReader(io.StringIO('﻿Name,Age\nA,1\n'))), '| with utf-8-sig:', list(csv.DictReader(io.TextIOWrapper(io.BytesIO('﻿Name,Age\nA,1\n'.encode('utf-8')), encoding='utf-8-sig'))))
'''),
]
PROGS += [
 ("What the csv module offers that the chapter does not mention: quoting constants (QUOTE_STRINGS and QUOTE_NOTNULL are new in 3.12), the field size limit, the Sniffer, strict mode, skipinitialspace, escapechar", GET + r'''import csv, io
print('quoting constants:', {n: getattr(csv, n) for n in dir(csv) if n.startswith('QUOTE_')})
def line(row, **k):
    s = io.StringIO(newline=''); csv.writer(s, **k).writerow(row); return s.getvalue()
row = ['a', 1, 2.5, None, '', 'b,c']
for q in ('QUOTE_MINIMAL', 'QUOTE_ALL', 'QUOTE_NONNUMERIC', 'QUOTE_NONE', 'QUOTE_STRINGS', 'QUOTE_NOTNULL'):
    try: print('%-17s' % q, repr(line(row, quoting=getattr(csv, q), escapechar='\\' if q == 'QUOTE_NONE' else None)))
    except Exception as e: print('%-17s' % q, type(e).__name__, e)
print('reading with QUOTE_NONNUMERIC turns unquoted fields into floats:', list(csv.reader(['"a",1,2.5'], quoting=csv.QUOTE_NONNUMERIC)))
smp = '"a",,"",3'
print('reading', smp, ': default', list(csv.reader([smp])), '| QUOTE_NOTNULL (an unquoted empty field is None)', list(csv.reader([smp], quoting=csv.QUOTE_NOTNULL)), '| QUOTE_STRINGS (None, and unquoted fields become floats)', list(csv.reader([smp], quoting=csv.QUOTE_STRINGS)))
print('QUOTE_STRINGS on an unquoted word:', end=' ')
try: list(csv.reader(['a,1'], quoting=csv.QUOTE_STRINGS))
except ValueError as e: print(type(e).__name__, e)
print('field_size_limit default', csv.field_size_limit())
try: list(csv.reader(['x' * (csv.field_size_limit() + 1)]))
except csv.Error as e: print('a field of', csv.field_size_limit() + 1, 'characters:', type(e).__name__, e)
sniff = csv.Sniffer(); sample = 'a;b;c\n1;2;3\n4;5;6\n'; dia = sniff.sniff(sample)
print('Sniffer: delimiter', repr(dia.delimiter), 'quotechar', repr(dia.quotechar), 'has_header', sniff.has_header(sample), '| rows', list(csv.reader(sample.splitlines(), dia)))
print('skipinitialspace:', list(csv.reader(['a, "b,c", d'])), list(csv.reader(['a, "b,c", d'], skipinitialspace=True)))
print('strict mode on a quote inside an unquoted field:', list(csv.reader(['a,b"c,d'])), end=' ')
try: list(csv.reader(['"a"x,b'], strict=True))
except csv.Error as e: print('| strict:', type(e).__name__, e)
print('escapechar:', repr(line(['a,b', 'c'], quoting=csv.QUOTE_NONE, escapechar='\\')), list(csv.reader(['a\\,b,c'], escapechar='\\')))
print('QUOTE_NONE with a delimiter in the field and no escapechar:', end=' ')
try: line(['a,b'], quoting=csv.QUOTE_NONE)
except csv.Error as e: print(type(e).__name__, e)
print('quotechar empty is refused (3.11):', end=' ')
try: csv.writer(io.StringIO(), quotechar='')
except Exception as e: print(type(e).__name__, e)
print('Dialect attributes of csv.excel:', {k: getattr(csv.excel, k) for k in ('delimiter', 'quotechar', 'doublequote', 'skipinitialspace', 'lineterminator', 'quoting')})
print('csv.__version__', csv.__version__, '| csv.reader is', csv.reader.__module__ if hasattr(csv.reader, '__module__') else None, '| csv module file', csv.__file__.split('/')[-1], '| public names', len([n for n in dir(csv) if not n.startswith('_')]))
'''),
 ("The claim that a for loop saves memory: peak memory of list(reader) against a loop over the reader, on a generated file of 300,000 rows, and the time of each", GET + r'''import csv, tracemalloc, time
d = work()
with open('big.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['id', 'name', 'amount'])
    for i in range(300000): w.writerow([i, 'name%d' % i, i * 3])
print('big.csv', os.path.getsize('big.csv'), 'bytes;', 'rows', 300001)
def peak(fn):
    tracemalloc.start(); t = time.perf_counter(); r = fn(); cur, pk = tracemalloc.get_traced_memory(); tracemalloc.stop(); return r, pk, time.perf_counter() - t
def as_list():
    with open('big.csv', newline='') as f: return len(list(csv.reader(f)))
def as_loop():
    n = 0
    with open('big.csv', newline='') as f:
        for row in csv.reader(f): n += 1
    return n
def as_loop_sum():
    t = 0
    with open('big.csv', newline='') as f:
        for row in csv.DictReader(f): t += int(row['amount'])
    return t
a, pa, ta = peak(as_list); b, pb, tb = peak(as_loop); c, pc, tc = peak(as_loop_sum)
print('rows counted by list(reader):', a, '| by the loop:', b, '| sum of the amount column in a DictReader loop:', c)
print('MEASURED peak memory: list(reader) %.1f MiB, loop %.3f MiB (ratio %.0f)' % (pa / 2**20, pb / 2**20, pa / pb), '| time: list %.2f s, loop %.2f s, DictReader loop %.2f s' % (ta, tb, tc))
print('the loop needs far less memory than list():', pb * 20 < pa)
'''),
 ("open() without an encoding, as every listing of the chapter calls it: the default encoding here, UTF-8 mode, the EncodingWarning that python -X warn_default_encoding raises on the chapter's statements, and a non-ASCII file read with the wrong encoding", GET + r'''import locale, csv
d = work(); make_example3()
print('locale.getencoding()', locale.getencoding(), '| sys.flags.utf8_mode', sys.flags.utf8_mode, '| sys.flags.warn_default_encoding', sys.flags.warn_default_encoding, '| open().encoding', open('example3.csv').encoding, '| PYTHONUTF8 set', 'PYTHONUTF8' in os.environ)
code = "import csv, warnings\nwarnings.simplefilter('always')\nf = open('example3.csv'); r = csv.reader(f); rows = list(r); f.close()\nf = open('output.csv', 'w', newline=''); w = csv.writer(f); w.writerow(['x']); f.close()\nf = open('example3.csv', encoding='utf-8'); list(csv.reader(f)); f.close()\n"
r = sh([sys.executable, '-X', 'warn_default_encoding', '-c', code])
print('with -X warn_default_encoding the three open() calls (two without encoding) raise', len([l for l in r.stderr.split('\n') if 'EncodingWarning' in l]), 'EncodingWarning:', [l.strip()[:110] for l in r.stderr.split('\n') if 'EncodingWarning' in l][:2])
r = sh([sys.executable, '-c', code]); print('without the flag the same code writes to stderr:', repr(r.stderr))
open('turkish.csv', 'w', encoding='utf-8', newline='').write('Ad,Şehir\nÇilek,İstanbul\n')
print('read as UTF-8:', list(csv.reader(open('turkish.csv', encoding='utf-8', newline=''))))
print('read as cp1252 (the default encoding of Windows in the United States):', end=' ')
try: print(list(csv.reader(open('turkish.csv', encoding='cp1252', newline=''))))
except UnicodeDecodeError as e: print(type(e).__name__, e)
print('read as cp1254 (the Turkish Windows code page):', end=' ')
try: print(list(csv.reader(open('turkish.csv', encoding='cp1254', newline=''))))
except UnicodeDecodeError as e: print(type(e).__name__, e)
open('turkish_cp1254.csv', 'w', encoding='cp1254', newline='').write('Ad,Şehir\nÇilek,İstanbul\n')
print('a file saved as cp1254 read as UTF-8:', end=' ')
try: print(list(csv.reader(open('turkish_cp1254.csv', encoding='utf-8', newline=''))))
except UnicodeDecodeError as e: print(type(e).__name__, e)
open('bom.csv', 'wb').write(b'\xef\xbb\xbfName,Age\nA,1\n')
print('a file with a BOM (what Excel saves as "CSV UTF-8"): utf-8 gives', list(csv.reader(open('bom.csv', encoding='utf-8', newline='')))[0], '| utf-8-sig gives', list(csv.reader(open('bom.csv', encoding='utf-8-sig', newline='')))[0])
'''),
 ("Project 13 (removeCsvHeader.py): the three steps put together, run whole on the 100 files of removeCsvHeader.zip, against the printed output, the shipped script, line endings and a second run", GET + r'''import csv
d = work('removeCsvHeader.zip', 'removeCsvHeader.py'); zipfile.ZipFile('removeCsvHeader.zip').extractall('.')
printed = listing_removeCsvHeader(); open('removeCsvHeader_printed.py', 'w').write(printed)
sp = shipped('removeCsvHeader.py').decode().replace('\r\n', '\n')
print('the program assembled from the three steps: %d lines; the shipped removeCsvHeader.py: %d lines; text equal: %s' % (printed.count('\n'), sp.count('\n'), printed.strip() == sp.strip()))
import ast
print('the two programs have the same syntax tree (they differ in comments, one comment-only line at the top and the wrapped open() call):', ast.dump(ast.parse(printed)) == ast.dump(ast.parse(sp)), '| shipped file has Windows line endings:', b'\r\n' in shipped('removeCsvHeader.py'))
before = sorted(f for f in os.listdir('.') if f.endswith('.csv')); sizes = {f: os.path.getsize(f) for f in before}
r = sh([sys.executable, 'removeCsvHeader_printed.py']); out = r.stdout.split('\n')
print('exit', r.returncode, '| stderr', repr(r.stderr[:80]), '| lines printed', len([l for l in out if l.startswith('Removing')]), '| the lines have the form', repr(re.sub(r'\d{4}', 'NNNN', out[0])))
order = [l.split(' ')[3].rstrip('.') for l in out if l.startswith('Removing')]
print('the order of the lines is the order of os.listdir, sorted:', order == sorted(order), '| the page shows 1048, 1218 ... 9834, 9986, which is the sorted order, the first sorted names being', sorted(order)[:3], '(os.listdir returns the names in an order the operating system chooses)')
print('files in headerRemoved:', len(os.listdir('headerRemoved')), '| the .csv files in the folder are unchanged in size:', all(os.path.getsize(f) == sizes[f] for f in before))
ok = bad = 0; crlf_in = crlf_out = lf_in = quoted_nl = 0; rowsum_in = rowsum_out = 0
for f in before:
    a = open(f, newline='').read(); b = open('headerRemoved/' + f, newline='').read()
    crlf_in += a.count('\r\n'); lf_in += a.count('\n') - a.count('\r\n'); crlf_out += b.count('\r\n')
    ra = list(csv.reader(open(f, newline=''))); rb = list(csv.reader(open('headerRemoved/' + f, newline='')))
    rowsum_in += len(ra); rowsum_out += len(rb)
    if ra[1:] == rb: ok += 1
    else: bad += 1
    quoted_nl += any('\n' in c for row in ra for c in row)
print('every output equals the input without its first record:', ok, 'of', ok + bad, '| records in', rowsum_in, 'out', rowsum_out, '| files with a line break inside a field:', quoted_nl)
print('line endings of the 100 input files: CRLF', crlf_in, 'bare LF', lf_in, '| of the outputs: CRLF', crlf_out, '(csv.writer writes CRLF whatever the input had; these inputs already had it, so their line endings do not change)')
print('first header cell', open(before[0]).readline().split(',')[0], '| NAICS_data_1048.csv input', len(open('NAICS_data_1048.csv', newline='').read()), 'bytes, output', len(open('headerRemoved/NAICS_data_1048.csv', newline='').read()), 'bytes')
r2 = sh([sys.executable, 'removeCsvHeader_printed.py']); print('second run: exit', r2.returncode, '| same output lines', r2.stdout == r.stdout, '| outputs identical to the first run:', all(open('headerRemoved/' + f, newline='').read() == open('headerRemoved/' + f, newline='').read() for f in before))
print('non-ASCII bytes in the 100 input files:', sum(1 for f in before for c in open(f, 'rb').read() if c > 127))
'''),
 ("Project 13 under conditions the chapter does not test: a file with only a header, an empty file, no final line feed, a BOM, a header with a line break, and the program run on its own output", GET + r'''import csv
d = work(); os.makedirs('t'); os.chdir('t')
open('only_header.csv', 'w', newline='').write('a,b\r\n')
open('empty.csv', 'w').write('')
open('no_lf.csv', 'w', newline='').write('a,b\r\n1,2\r\n3,4')
open('bom.csv', 'wb').write(b'\xef\xbb\xbfa,b\r\n1,2\r\n')
open('multiline_header.csv', 'w', newline='').write('"a\nb",c\r\n1,2\r\n')
open('notes.txt', 'w').write('not a csv')
open('UPPER.CSV', 'w').write('x\n1\n')
open('sub.csv', 'w').write('')
src = listing_removeCsvHeader(); open('prog.py', 'w').write(src)
r = sh([sys.executable, 'prog.py']); print('exit', r.returncode, '| stdout', r.stdout.split('\n')[:9], '| last stderr line', (r.stderr.strip().splitlines() or ['-'])[-1][:120])
for f in sorted(os.listdir('headerRemoved')): print(f, open('headerRemoved/' + f, 'rb').read())
print('UPPER.CSV is skipped by endswith(".csv"):', 'UPPER.CSV' not in os.listdir('headerRemoved'))
os.makedirs('../u/folder.csv'); open('../u/prog.py', 'w').write(src); r = sh([sys.executable, 'prog.py'], cwd='../u'); print('a folder whose name ends in .csv:', 'exit', r.returncode, (r.stderr.strip().splitlines() or ['-'])[-1])
'''),
]
PROGS += [
 ("JSON as the chapter teaches it: loads and dumps on the Alice data, the printed compact line against the real one, indent=2 against the printed listing, and what the Python data looks like", GET + r'''import json
JS = '{"name": "Alice Doe", "age": 30, "car": null, "programmer": true, "address": {"street": "100 Larkin St.", "city": "San Francisco", "zip": "94102"}, "phone": [{"type": "mobile", "number": "415-555-7890"}, {"type": "work", "number": "415-555-1234"}]}'
data = json.loads(JS)
print(type(data).__name__, [(k, type(v).__name__) for k, v in data.items()])
print(data)
compact = json.dumps(data); print(compact == JS, len(compact), 'characters')
printed = re.sub(r'\s+', '', re.sub('[❶-❿][ \t]?', '', pres()[19]).split('>>> print(json_string)')[1].split('>>> json_string')[0]); print('the compact line the page prints equals the real one (whitespace aside):', printed == re.sub(r'\s+', '', compact))
pretty = json.dumps(data, indent=2); print(pretty)
page_pretty = pres()[17].rstrip('\n'); print('indent=2 output equals the pretty JSON listing of the page (block 17):', pretty == page_pretty, '| lines', len(pretty.split('\n')), '| characters', len(pretty))
print('the printed listing of the Python data structure (block 16) is Python, not JSON, and evaluates to the same dict:', eval(pres()[16]) == data)
print('round trip:', json.loads(json.dumps(data)) == data, '| loads of the pretty text:', json.loads(pretty) == data, '| bool and None:', data['programmer'] is True, data['car'] is None, '| age is', type(data['age']).__name__)
print('separators=(",", ":") compact form:', len(json.dumps(data, separators=(',', ':'))), 'characters;', 'indent="\\t":', repr(json.dumps({'a': [1]}, indent='\t')), '; indent=0:', repr(json.dumps({'a': [1]}, indent=0)), '; indent=None:', repr(json.dumps({'a': [1]})))
print('sort_keys=True first keys:', list(json.loads(json.dumps(data, sort_keys=True))), '| the key order of the input is kept without it:', list(json.loads(JS)) == list(data))
print('json.dumps returns', type(compact).__name__, '| json.loads accepts bytes (3.6+):', json.loads(b'[1, 2]'), '| a file object is refused by loads:', end=' ')
try: json.loads(open('/dev/null'))
except TypeError as e: print(type(e).__name__, e)
'''),
 ("What JSON does to Python values the chapter's list of data types leaves out: tuples, integer keys, floats, NaN, non-ASCII text, and what it refuses", GET + r'''import json, decimal, datetime, collections, enum
print('ensure_ascii default:', json.dumps({'name': 'Müller', 'city': 'İstanbul', 'emoji': '\U0001f600'}), '| ensure_ascii=False:', json.dumps({'name': 'Müller', 'city': 'İstanbul'}, ensure_ascii=False))
print('tuple ->', json.dumps((1, 2)), '| round trip', json.loads(json.dumps((1, 2))), '| set:', end=' ')
try: json.dumps({1, 2})
except TypeError as e: print(type(e).__name__, e)
print('integer, float and None keys:', json.dumps({1: 'a', 2.5: 'b', None: 'd'}), '| round trip keys', list(json.loads(json.dumps({1: 'a', 2.5: 'b', None: 'd'}))), '| True and 1 are the same key in Python, so', json.dumps({1: 'a', True: 'c'}))
print('a tuple as a key:', end=' ')
try: json.dumps({(1, 2): 'x'})
except TypeError as e: print(type(e).__name__, e)
print('floats:', json.dumps([1.0, 0.1 + 0.2, 1e20, 1e-7, 3.141592, 10**30]), '| NaN and infinity:', json.dumps([float('nan'), float('inf'), -float('inf')]), '| allow_nan=False:', end=' ')
try: json.dumps(float('nan'), allow_nan=False)
except ValueError as e: print(type(e).__name__, e)
print('the Python parser accepts what RFC 8259 does not allow:', json.loads('[NaN, Infinity, -Infinity]'))
for label, v in (('datetime', datetime.datetime(2035, 4, 5, 13, 34)), ('Decimal', decimal.Decimal('1.5')), ('bytes', b'x'), ('complex', 1j), ('a file object', open('/dev/null')), ('an object', object())):
    try: json.dumps(v)
    except TypeError as e: print('%-13s' % label, type(e).__name__, e)
print('default=str:', json.dumps({'when': datetime.datetime(2035, 4, 5, 13, 34), 'x': decimal.Decimal('1.5')}, default=str))
class Color(enum.IntEnum): RED = 1
class S(str, enum.Enum): A = 'a'
print('int- and str-derived enums (3.4+):', json.dumps([Color.RED, S.A]), '| OrderedDict:', json.dumps(collections.OrderedDict(a=1)), '| dict subclass and a namedtuple:', json.dumps(collections.namedtuple('P', 'x y')(1, 2)))
print('an integer of 5000 digits:', end=' ')
try: json.loads('1' * 5000)
except ValueError as e: print(type(e).__name__, str(e)[:90])
print('with parse_int=float or a bigger int limit through int():', type(json.loads('1' * 5000, parse_int=lambda s: s[:5])).__name__)
print('nesting 100000 deep:', end=' ')
try: json.loads('[' * 100000 + ']' * 100000)
except RecursionError as e: print(type(e).__name__)
print('duplicate keys, the last wins:', json.loads('{"a": 1, "a": 2}'), '| object_pairs_hook keeps both:', json.loads('{"a": 1, "a": 2}', object_pairs_hook=list))
print('what the round trip loses: tuple -> list', json.loads(json.dumps({'t': (1, 2)})) == {'t': (1, 2)}, '| int key -> str key', json.loads(json.dumps({1: 1})) == {1: 1})
'''),
 ("The syntax claims of the JSON section tested one by one: what json.loads accepts and the exact message for each thing the chapter says JSON does not allow", GET + r'''import json
cases = [('trailing comma in an array, the chapter\'s example', '["spam", "eggs",]'), ('the valid array of the chapter', '["spam", "eggs"]'), ('trailing comma in an object', '{"a": 1,}'), ('single-quoted string', "{'a': 1}"), ('a JavaScript comment', '{"a": 1} // note'), ('a comment inside', '{"a": /* x */ 1}'), ('a multiline string (a raw line feed inside the quotes)', '"a\nb"'),
         ('the same string with the escape \\n', '"a\\nb"'), ('Python None', '{"a": None}'), ('Python True', '[True]'), ('JavaScript null, true and false', '[null, true, false]'), ('an unquoted key', '{a: 1}'), ('a leading zero', '[01]'), ('a plus sign', '[+1]'), ('a hexadecimal number', '[0x10]'),
         ('a decimal point with no digit', '[1.]'), ('an exponent', '[1e2, 1E-2]'), ('a top-level number (allowed since RFC 7159)', '3'), ('a top-level string', '"x"'), ('an empty string', ''), ('only whitespace', '  '), ('two values', '{} {}'), ('a form feed as whitespace', '[1,\x0c2]'), ('a no-break space as whitespace', '[1, 2]'), ('a tab and a carriage return as whitespace', '[1,\t\r\n2]'),
         ('a tab inside a string', '"a\tb"'), ('an invalid escape', '"\\q"'), ('a lone surrogate escape', '"\\ud800"'), ('a Unicode escape', '"\\u00fc"')]
for label, text in cases:
    try: print('%-58s ok  %r' % (label, json.loads(text)))
    except json.JSONDecodeError as e: print('%-58s ERR %s | msg=%r lineno=%d colno=%d pos=%d' % (label, e, e.msg, e.lineno, e.colno, e.pos))
print('strict=False allows the control character in a string:', repr(json.loads('"a\tb"', strict=False)))
print('bytes with a BOM:', end=' ')
try: print('accepted:', json.loads(b'\xef\xbb\xbf{}'), '(the encoding is detected as', json.detect_encoding(b'\xef\xbb\xbf{}') + ')')
except json.JSONDecodeError as e: print(e)
print('str with a BOM:', end=' ')
try: json.loads('﻿{}')
except json.JSONDecodeError as e: print(e)
print('UTF-16 bytes are detected (3.6+):', json.loads('["é"]'.encode('utf-16')), '| JSONDecodeError is a subclass of', json.JSONDecodeError.__mro__[1].__name__)
'''),
 ("Where the chapter stops: json.load and json.dump (files) are not in it. A round trip through a file, the encoding the file should have, what happens with a wrong one, and the notes Python 3.14 adds to serialization errors", GET + r'''import json
d = work()
data = {'name': 'Alice Doe', 'city': 'İstanbul', 'n': [1, 2.5, None, True]}
with open('person.json', 'w', encoding='utf-8') as f: print('json.dump returns', json.dump(data, f, indent=2, ensure_ascii=False))
print(open('person.json', 'rb').read())
with open('person.json', encoding='utf-8') as f: back = json.load(f)
print('json.load equals the data:', back == data, '| json.loads(file.read()) equals it:', json.loads(open('person.json', encoding='utf-8').read()) == data)
with open('person_ascii.json', 'w') as f: json.dump(data, f)
print('json.dump with the default ensure_ascii=True writes only ASCII:', all(c < 128 for c in open('person_ascii.json', 'rb').read()), '|', open('person_ascii.json').read())
try: json.load(open('person.json', encoding='cp1252')); print('read with cp1252: no error, but the text is wrong:', json.load(open('person.json', encoding='cp1252'))['city'])
except Exception as e: print('read with cp1252:', type(e).__name__, e)
print('json.load on a file opened with "rb" works (bytes are decoded as UTF-8):', json.load(open('person.json', 'rb')) == data)
try: json.dump(data, open('x.json', 'wb'))
except TypeError as e: print('json.dump to a binary file:', type(e).__name__, e)
print('Python 3.14 notes on serialization errors:')
for obj in ({'a': [1, {2, 3}]}, [{'k': {'x': object()}}], {'a': 1, (1, 2): 3}):
    try: json.dumps(obj)
    except TypeError as e: print('  ', e, '| notes:', getattr(e, '__notes__', None))
print('python -m json (a command-line JSON tool; 3.14 allows -m json, earlier releases need -m json.tool):')
r = sh([sys.executable, '-m', 'json', 'person.json']); print('  exit', r.returncode, r.stdout.replace('\n', ' ')[:90], r.stderr.strip()[-80:])
r = sh([sys.executable, '-m', 'json.tool', '--compact', 'person.json']); print('  json.tool --compact:', r.returncode, r.stdout.strip()[:80])
'''),
]
PROGS += [
 ("Reading XML with ElementTree: root, tag, text, the children as a list, indexing, iteration, iter('number'); the types, and that text is None only where nothing is between the tags", GET + r'''import xml.etree.ElementTree as ET
C = '<person><name>Alice Doe</name><age>30</age><programmer>true</programmer><car xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/><address><street>100 Larkin St.</street><city>San Francisco</city><zip>94102</zip></address><phone><phoneEntry><type>mobile</type><number>415-555-7890</number></phoneEntry><phoneEntry><type>work</type><number>415-555-1234</number></phoneEntry></phone></person>'
root = ET.fromstring(C)
print(type(root), '| tag', root.tag, '| children', [e.tag for e in root], '| len', len(root), '| list(root) is a list of', {type(e).__name__ for e in list(root)})
print('root[0].text', repr(root[0].text), '| age text and type', repr(root[1].text), type(root[1].text).__name__, '| programmer', repr(root[2].text), '| car text', repr(root[3].text), '| car text is None', root[3].text is None, '| root[3].text == None', root[3].text == None)
print('root[4][0].tag', root[4][0].tag, '| text', repr(root[4][0].text), '| address text', repr(root[4].text), '| last child', root[-1].tag, '| slice', [e.tag for e in root[1:3]])
print('index out of range:', end=' ')
try: root[6]
except IndexError as e: print(type(e).__name__, e)
for elem in root.iter('number'): print(elem.tag, '--', elem.text)
print('iter() order (document order, depth first):', [e.tag for e in root.iter()])
print('iter() includes the root itself:', next(root.iter()) is root, '| iter(tag) count', len(list(root.iter('type'))), '| the children of root only:', len(list(root)), 'against all descendants', len(list(root.iter())) - 1)
print('the chapter says list(root) "should return a list of its immediate child elements":', [e.tag for e in list(root)])
print('attrib of car:', root[3].attrib, '| get:', root[3].get('{http://www.w3.org/2001/XMLSchema-instance}nil'), '| get("xsi:nil")', root[3].get('xsi:nil'))
print('the chapter says "any self-closing tags, like <car/>, will use None for their text":', ET.fromstring('<car/>').text, ET.fromstring('<car></car>').text, repr(ET.fromstring('<car> </car>').text), repr(ET.fromstring('<car>0</car>').text))
print('a self-closing tag and an empty pair are the same to the parser:', ET.tostring(ET.fromstring('<car></car>')), ET.tostring(ET.fromstring('<car/>')))
print('repr of an element:', repr(root)[:22], '| tail of name:', repr(root[0].tail), '| the string must not contain an encoding declaration with str? ', end='')
print(ET.fromstring('<?xml version="1.0" encoding="UTF-8"?><a>é</a>').text, '| with bytes:', ET.fromstring('<?xml version="1.0" encoding="UTF-8"?><a>é</a>'.encode('utf-8')).text)
print('a str with an encoding declaration of another encoding:', end=' ')
try: print(ET.fromstring('<?xml version="1.0" encoding="ISO-8859-1"?><a>é</a>').text)
except ET.ParseError as e: print(type(e).__name__, e)
'''),
 ("my_data.xml and ET.parse: the pretty-printed document of the chapter. The text of an element that only holds other elements is the whitespace between the tags, not None, so the printed loops differ", GET + r'''import xml.etree.ElementTree as ET
d = work(); make_my_data()
tree = ET.parse('my_data.xml'); root = tree.getroot()
print(type(tree).__name__, type(root).__name__, root.tag, '| children', [e.tag for e in root])
print('root.text', repr(root.text), '| address.text', repr(root[4].text), '| phone.text', repr(root[5].text), '| street.tail', repr(root[4][0].tail), '| last child tail', repr(root[5].tail))
print('the loop of the chapter (for elem in root: print(elem.tag, "--", elem.text)) on the file:')
for elem in root: print('  ', elem.tag, '--', repr(elem.text))
print('the printed output has None for address and phone; the file gives None only for', [e.tag for e in root.iter() if e.text is None])
print('text.strip() or None gives the printed values:', [(e.tag, (e.text or '').strip() or None) for e in root])
print('root[3] (car):', root[3].tag, root[3].text, root[3].attrib)
print('ET.parse accepts a file name, a path-like and an open binary file:', ET.parse('my_data.xml').getroot().tag, ET.parse(open('my_data.xml', 'rb')).getroot().tag)
print('ET.parse of a file that does not exist:', end=' ')
try: ET.parse('nothing.xml')
except OSError as e: print(type(e).__name__, e)
print('ET.parse of text that is not XML:', end=' ')
open('bad.xml', 'w').write('<a><b></a>')
try: ET.parse('bad.xml')
except ET.ParseError as e: print(type(e).__name__, e, '| position', e.position, '| code', e.code)
print('the page names the file my_data.xml but ships none; the study made it from block 20: bytes', os.path.getsize('my_data.xml'))
'''),
 ("Namespaces and xsi:nil: what ElementTree makes of the car element, whether the null is understood, and what the serialiser writes when the tree is parsed and written again", GET + r'''import xml.etree.ElementTree as ET
XSI = 'http://www.w3.org/2001/XMLSchema-instance'
doc = '<person><car xsi:nil="true" xmlns:xsi="%s"/><note xsi:nil="false" xmlns:xsi="%s">text</note><other xsi:nil="true" xmlns:xsi="%s">not empty</other></person>' % (XSI, XSI, XSI)
root = ET.fromstring(doc)
for e in root: print(e.tag, '| attrib', e.attrib, '| text', repr(e.text), '| the nil attribute', e.get('{%s}nil' % XSI))
print('ElementTree stores the attribute under its full name {namespace-uri}local-name; xmlns:xsi is not kept as an attribute; nothing turns nil into None (an element with xsi:nil="true" and text keeps its text)')
print('parse then tostring:', ET.tostring(root, encoding='unicode'))
print('the prefix xsi is already in the default prefix map of the module (ET.register_namespace changes nothing here); a namespace that is not in the map gets ns0:', ET.tostring(ET.fromstring('<a xmlns:p="urn:x"><p:b p:c="1"/></a>'), encoding='unicode'), '| after register_namespace("p", "urn:x"):', end=' ')
ET.register_namespace('p', 'urn:x'); print(ET.tostring(ET.fromstring('<a xmlns:p="urn:x"><p:b p:c="1"/></a>'), encoding='unicode'))
print('the same document after the registration, as the chapter writes it by hand with set("xmlns:xsi", ...):')
person = ET.Element('person'); car = ET.SubElement(person, 'car'); car.set('xsi:nil', 'true'); car.set('xmlns:xsi', XSI)
s = ET.tostring(person, encoding='unicode'); print(s, '| parses back:', ET.fromstring(s)[0].attrib)
print('an undeclared prefix is a well-formedness error for the parser:', end=' ')
try: ET.fromstring('<a xsi:nil="true"/>')
except ET.ParseError as e: print(type(e).__name__, e)
print('the chapter ET.tostring writes xsi:nil as an ordinary attribute whose name contains a colon; no check is made:', ET.tostring(ET.Element('a', {'x:y': '1'})))
print('attribute names are not validated when set:', ET.tostring(ET.Element('a', {'1 bad': '1'})), '| tag not validated:', ET.tostring(ET.Element('a b')))
q = ET.QName(XSI, 'nil'); print('QName text', q.text, '| equals the key', q.text == '{%s}nil' % XSI)
'''),
 ("Writing XML as the chapter does: every statement of its Element, SubElement and set listing, the tostring result against the printed string (the space before the slash), bytes against str, and pretty printing", GET + r'''import xml.etree.ElementTree as ET
person = ET.Element('person'); name = ET.SubElement(person, 'name'); name.text = 'Alice Doe'; age = ET.SubElement(person, 'age'); age.text = '30'
programmer = ET.SubElement(person, 'programmer'); programmer.text = 'true'; car = ET.SubElement(person, 'car'); car.set('xsi:nil', 'true'); car.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
address = ET.SubElement(person, 'address'); street = ET.SubElement(address, 'street'); street.text = '100 Larkin St.'
b = ET.tostring(person, encoding='utf-8'); s = b.decode('utf-8'); print(type(b).__name__, b[:30], '...'); print(s)
printed = re.sub(r'\s+', '', re.sub('[❶-❿][ \t]?', '', pres()[33]).split('\n', 1)[1])[1:-1]
print('the string the page prints, whitespace aside, equals the real one:', printed == re.sub(r'\s+', '', s), '| the real one has " />" (space before the slash), the page prints "/>":', s.count(' />'), 'against', pres()[33].count(' />'))
print('equal exactly, once the space before the slash is removed from the real one:', re.sub(r'\s+', '', s.replace(' />', '/>')) == printed)
print('encoding="unicode" returns str directly:', type(ET.tostring(person, encoding='unicode')).__name__, ET.tostring(person, encoding='unicode') == s, '| default encoding us-ascii returns bytes:', type(ET.tostring(person)).__name__, ET.tostring(person) == b)
print('encoding="utf-8" (in any case) writes no XML declaration; utf-16 and iso-8859-1 do:', ET.tostring(person, encoding='UTF-8')[:12], ET.tostring(ET.Element('a'), encoding='utf-16')[:30], ET.tostring(ET.Element('a'), encoding='iso-8859-1'))
print('xml_declaration=True:', ET.tostring(ET.Element('a'), encoding='utf-8', xml_declaration=True))
print('short_empty_elements=False:', ET.tostring(car, encoding='unicode', short_empty_elements=False))
t = ET.Element('t'); t.text = 'a < b & c > d "q" \'s\''; t.set('v', 'a "b" & <c> \n x')
print('escaping:', ET.tostring(t, encoding='unicode'))
u = ET.Element('u'); u.text = 'Müller İstanbul 日本'
print('non-ASCII text with the default encoding becomes character references:', ET.tostring(u), '| with utf-8:', ET.tostring(u, encoding='utf-8'))
ET.indent(person); print('ET.indent (3.9+) pretty prints in place:'); print(ET.tostring(person, encoding='unicode'))
print('attribute order is the order of set() (3.8+):', ET.tostring(ET.fromstring('<a z="1" b="2" m="3"/>'), encoding='unicode'))
print('a non-string text is refused when written:', end=' ')
e = ET.Element('n'); e.text = 30
try: ET.tostring(e)
except TypeError as ex: print(type(ex).__name__, ex)
print('a non-string attribute value:', end=' ')
try: ET.tostring(ET.Element('n', {'k': 1}))
except TypeError as ex: print(type(ex).__name__, ex)
import io; f = io.BytesIO(); ET.ElementTree(person).write(f, encoding='utf-8', xml_declaration=True); print('ElementTree.write:', f.getvalue()[:60])
ET.dump(ET.fromstring('<a><b>x</b></a>'))
'''),
 ("What the chapter does not say about Element: comments are dropped, a document with several roots is refused, the truth value of an Element is deprecated, find, findall and the XPath subset, and findtext", GET + r'''import xml.etree.ElementTree as ET, warnings
three = pres()[21]; print('the page\'s three-person text:', repr(three[:60]))
try: ET.fromstring(three)
except ET.ParseError as e: print('three roots:', type(e).__name__, e)
print('one root and a comment:', ET.tostring(ET.fromstring('<a><!-- ignored --><b/></a>')), '| with a comment kept:', ET.tostring(ET.fromstring('<a><!-- ignored --><b/></a>', ET.XMLParser(target=ET.TreeBuilder(insert_comments=True)))))
doc = ET.fromstring('<people><person id="1"><name>Alice</name><phone type="mobile">1</phone><phone type="work">2</phone></person><person id="2"><name>Bob</name></person></people>')
print('find first child:', doc.find('person/name').text, '| findall', [e.text for e in doc.findall('.//phone')], '| findtext', doc.findtext('person/name'), doc.findtext('person/nothing'), repr(doc.findtext('person/nothing', default='?')))
print('XPath subset: attribute predicate', [e.text for e in doc.findall(".//phone[@type='work']")], '| position', doc.find('person[2]/name').text, '| by attribute value', doc.find("person[@id='2']/name").text, '| wildcard', len(doc.findall('person/*')), '| parent search by predicate', [e.tag for e in doc.findall('.//name/..')])
print('find returns None when nothing matches:', doc.find('nothing'), '| .text of that fails:', end=' ')
try: doc.find('nothing').text
except AttributeError as e: print(type(e).__name__, e)
print('the truth value of an Element:')
empty = ET.Element('x'); full = ET.fromstring('<a><b/></a>')
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always'); r = (bool(empty), bool(full), bool(doc.find('nothing')))
    print('  bool(<x/>), bool(<a><b/></a>), bool(None):', r, '| warnings:', sorted({(x.category.__name__, str(x.message)[:90]) for x in w}))
print('  found-element test that works: `if elem is not None`; `if elem:` tests the number of children (and warns since 3.12):', 'in the Python documentation')
print('an element is also a sequence:', len(doc), doc[0].tag, [e.tag for e in reversed(doc)], 'append/remove:', end=' ')
n = ET.Element('n'); k = ET.SubElement(n, 'k'); n.remove(k); n.append(ET.Element('z')); n.insert(0, ET.Element('y')); print([e.tag for e in n])
print('the chapter says "XPath can locate elements": the module implements a subset:', end=' ')
try: doc.findall('person[name="Alice"]'); print('person[name="Alice"] accepted:', [e.get('id') for e in doc.findall('person[name="Alice"]')])
except Exception as e: print(type(e).__name__, e)
try: doc.xpath('//name')
except AttributeError as e: print('| doc.xpath:', type(e).__name__, e)
'''),
 ("xmltodict as the chapter uses it, in the two environments: the printed dictionary, the lists that are not lists, what stays a string, what unparse returns, the options, and what a reader without the package sees", GET + r'''import xmltodict, importlib.metadata as md, json
print('xmltodict', md.version('xmltodict'), '| the module file', xmltodict.__file__.split('/')[-1], '| exports', sorted(n for n in dir(xmltodict) if not n.startswith('_'))[:12])
C = '<person><name>Alice Doe</name><age>30</age><programmer>true</programmer><car xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/><address><street>100 Larkin St.</street><city>San Francisco</city><zip>94102</zip></address><phone><phoneEntry><type>mobile</type><number>415-555-7890</number></phoneEntry><phoneEntry><type>work</type><number>415-555-1234</number></phoneEntry></phone></person>'
r = xmltodict.parse(C); print(r); print('type of the result', type(r).__name__, '| of the person', type(r['person']).__name__)
PRINTED = "{'person': {'name': 'Alice Doe', 'age': '30', 'programmer': 'true', 'car': {'@xsi:nil': 'true', '@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance'}, 'address': {'street': '100 Larkin St.', 'city': 'San Francisco', 'zip': '94102'}, 'phone': {'phoneEntry': [{'type': 'mobile', 'number': '415-555-7890'}, {'type': 'work', 'number': '415-555-1234'}]}}}"
print('equal to the printed dictionary:', repr(r) == PRINTED, '| as data:', r == eval(PRINTED))
print('every value is a string:', {type(v).__name__ for v in (r['person']['age'], r['person']['programmer'], r['person']['address']['zip'])}, '| car is', r['person']['car'])
one = xmltodict.parse('<phone><phoneEntry><type>mobile</type></phoneEntry></phone>'); two = xmltodict.parse('<phone><phoneEntry><type>mobile</type></phoneEntry><phoneEntry><type>work</type></phoneEntry></phone>')
print('one entry gives a dict, two give a list:', type(one['phone']['phoneEntry']).__name__, type(two['phone']['phoneEntry']).__name__, '| force_list:', xmltodict.parse('<phone><phoneEntry><type>mobile</type></phoneEntry></phone>', force_list=('phoneEntry',)))
print('attributes and text together:', xmltodict.parse('<a href="x">link</a>'), '| attr_prefix="" :', xmltodict.parse('<a href="x">link</a>', attr_prefix=''), '| text with attributes only:', xmltodict.parse('<a href="x"/>'), '| an empty element:', xmltodict.parse('<a><b/></a>'))
print('unparse of the result:', xmltodict.unparse(r)[:150])
print('unparse(pretty=True):'); print(xmltodict.unparse({'a': {'@id': '1', 'b': ['x', 'y']}}, pretty=True, full_document=False))
back = xmltodict.parse(xmltodict.unparse(r)); print('parse(unparse(r)) equals r:', back == r)
print('json.dumps of the result:', json.dumps(r)[:120])
print('process_namespaces=True:', xmltodict.parse(C, process_namespaces=True)['person']['car'])
print('a comment, mixed content and whitespace:', xmltodict.parse('<a>x<b>y</b>z</a>'), xmltodict.parse('<a> padded </a>'), xmltodict.parse('<a> padded </a>', strip_whitespace=False))
print('two roots:', end=' ')
try: xmltodict.parse('<a/><b/>')
except Exception as e: print(type(e).__module__ + '.' + type(e).__name__, e)
print('a bytes input:', xmltodict.parse(b'<a>1</a>'), '| a dict_constructor:', type(xmltodict.parse('<a><b>1</b></a>', dict_constructor=dict)).__name__)
print('what a reader without the package sees:', end=' ')
r2 = sh([BARE, '-I', '-c', 'import xmltodict']); print(r2.stderr.strip().splitlines()[-1])
'''),
]
PROGS += [
 ("XML entity attacks against the parser the chapter uses: the billion laughs file, a quadratic blowup, an external entity, and what the Python 3.14 documentation says; run in a child process with a memory limit and a time limit", GET + r'''import xml.etree.ElementTree as ET, resource, time
import xmltodict, defusedxml.ElementTree as DET
from defusedxml import EntitiesForbidden, DTDForbidden, ExternalReferenceForbidden
ents = '<!ENTITY lol "lol">' + ''.join('<!ENTITY lol%d "%s">' % (i, ('&lol;' if i == 1 else '&lol%d;' % (i - 1)) * 10) for i in range(1, 10))
laughs = '<?xml version="1.0"?><!DOCTYPE lolz [' + ents + ']><lolz>&lol9;</lolz>'
print('the file is', len(laughs), 'bytes; fully expanded it would be', 3 * 10 ** 9, 'characters (lol9 = 10^9 times "lol")')
CHILD = r"""
import sys, resource, time, xml.etree.ElementTree as ET
resource.setrlimit(resource.RLIMIT_AS, (2 * 2**30, 2 * 2**30))
t = time.perf_counter()
try:
    r = ET.fromstring(sys.stdin.read()); print('parsed; text length', len(r.text or ''))
except BaseException as e: print(type(e).__module__ + '.' + type(e).__name__, str(e)[:140])
print('MEASURED seconds %.2f' % (time.perf_counter() - t))
"""
def child(doc, label):
    r = subprocess.run([sys.executable, '-c', CHILD], input=doc, capture_output=True, text=True, timeout=120)
    lines = (r.stdout.strip() or r.stderr.strip()[-150:]).split('\n')
    print('%-34s' % label, ' | '.join(l for l in lines if not l.startswith('MEASURED')))
    for l in lines:
        if l.startswith('MEASURED'): print(l, '(' + label + ')')
child(laughs, 'billion laughs, ElementTree')
big = 'x' * 50000
quad = '<?xml version="1.0"?><!DOCTYPE b [<!ENTITY a "%s">]><b>%s</b>' % (big, '&a;' * 50000)
print('the quadratic blowup file is', len(quad), 'bytes; expanded it would be', 50000 * 50000, 'characters')
child(quad, 'quadratic blowup, ElementTree')
small = '<?xml version="1.0"?><!DOCTYPE b [<!ENTITY a "hello">]><b>&a;&a;</b>'
child(small, 'a small internal entity')
ext = '<?xml version="1.0"?><!DOCTYPE b [<!ENTITY x SYSTEM "file:///etc/hostname">]><b>&x;</b>'
child(ext, 'an external entity (file:///etc/hostname)')
ext2 = '<?xml version="1.0"?><!DOCTYPE b [<!ENTITY % p SYSTEM "http://127.0.0.1:9/x.dtd"> %p;]><b>text</b>'
child(ext2, 'an external parameter entity')
for label, fn in (('defusedxml, billion laughs', lambda: DET.fromstring(laughs)), ('defusedxml, small internal entity', lambda: DET.fromstring(small)), ('defusedxml, external entity', lambda: DET.fromstring(ext)), ('defusedxml, no DTD at all', lambda: DET.fromstring('<a>1</a>').text), ('defusedxml, forbid_dtd=True', lambda: DET.fromstring(small, forbid_dtd=True))):
    try: print('%-34s' % label, 'parsed', fn())
    except (EntitiesForbidden, DTDForbidden, ExternalReferenceForbidden) as e: print('%-34s' % label, type(e).__name__, str(e)[:100])
XC = "import xmltodict, sys, resource, importlib.metadata as md\nresource.setrlimit(resource.RLIMIT_AS, (2 * 2**30, 2 * 2**30))\nfor label, doc in (('small internal entity', sys.argv[1]), ('billion laughs', sys.argv[2])):\n    try: print(' ', label, 'parsed', xmltodict.parse(doc))\n    except BaseException as e: print(' ', label, type(e).__module__ + '.' + type(e).__name__, str(e)[:100])\n"
for name, py in (('LATEST', LATEST), ('PINS', PINS)):
    r = subprocess.run([py, '-I', '-c', XC, small, laughs], capture_output=True, text=True, timeout=120)
    print('xmltodict', name, sh([py, '-I', '-c', 'import importlib.metadata as m; print(m.version("xmltodict"))']).stdout.strip() + ':'); print((r.stdout or r.stderr[-200:]).rstrip())
doc = cached('ch18_pydoc_xml.html', 'https://docs.python.org/3.14/library/xml.html').decode('utf-8')
t = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', doc)))
i = t.find('The built-in XML parsers'); j = t.find('Check pyexpat.EXPAT_VERSION')
print('Python 3.14 documentation, XML security:', t[i:j + 28].replace(' .', '.'))
import pyexpat; print('pyexpat.EXPAT_VERSION of this interpreter:', pyexpat.EXPAT_VERSION)
'''),
 ("Three ways to read the same XML, the DOM and the SAX approaches the chapter names against ElementTree: the same answer, and the memory each needs on a document of 200,000 elements", GET + r'''import xml.etree.ElementTree as ET, xml.dom.minidom as minidom, xml.sax, tracemalloc, time
C = '<person><name>Alice Doe</name><age>30</age><phone><phoneEntry><type>mobile</type><number>415-555-7890</number></phoneEntry><phoneEntry><type>work</type><number>415-555-1234</number></phoneEntry></phone></person>'
print('ElementTree:', [e.text for e in ET.fromstring(C).iter('number')])
dom = minidom.parseString(C); print('minidom (DOM):', [n.firstChild.data for n in dom.getElementsByTagName('number')], '| the document element', dom.documentElement.tagName, '| node types are', type(dom).__name__, type(dom.documentElement).__name__)
class H(xml.sax.ContentHandler):
    def __init__(self): super().__init__(); self.on = False; self.out = []
    def startElement(self, name, attrs): self.on = name == 'number'
    def characters(self, content):
        if self.on: self.out.append(content)
    def endElement(self, name): self.on = False
h = H(); xml.sax.parseString(C.encode(), h); print('SAX:', h.out)
print('minidom.toprettyxml:'); print(minidom.parseString(C).toprettyxml(indent='  ')[:210])
N = 200000
open('big.xml', 'w').write('<items>' + ''.join('<item id="%d"><name>n%d</name><qty>%d</qty></item>' % (i, i, i % 7) for i in range(N)) + '</items>')
print('big.xml', os.path.getsize('big.xml'), 'bytes,', N, 'items')
def peak(fn):
    tracemalloc.start(); t = time.perf_counter(); r = fn(); cur, pk = tracemalloc.get_traced_memory(); tracemalloc.stop(); return r, pk, time.perf_counter() - t
def et_tree(): return sum(int(e.text) for e in ET.parse('big.xml').getroot().iter('qty'))
def et_iter():
    t = 0
    for ev, e in ET.iterparse('big.xml', events=('end',)):
        if e.tag == 'qty': t += int(e.text)
        e.clear()
    return t
def dom_tree(): return sum(int(n.firstChild.data) for n in minidom.parse('big.xml').getElementsByTagName('qty'))
class Q(xml.sax.ContentHandler):
    def __init__(self): super().__init__(); self.on = False; self.t = 0
    def startElement(self, name, attrs): self.on = name == 'qty'
    def characters(self, c):
        if self.on: self.t += int(c)
    def endElement(self, name): self.on = False
def sax_stream(): q = Q(); xml.sax.parse('big.xml', q); return q.t
res = {}
for label, fn in (('ElementTree parse (whole tree)', et_tree), ('ElementTree iterparse with clear()', et_iter), ('minidom (DOM, whole tree)', dom_tree), ('SAX (stream)', sax_stream)):
    r, pk, t = peak(fn); res[label] = (r, pk, t)
print('the sum of qty is the same in all four:', len({v[0] for v in res.values()}) == 1, '=', res['SAX (stream)'][0])
for label, (r, pk, t) in res.items(): print('MEASURED %-36s peak %7.1f MiB  %.2f s' % (label, pk / 2**20, t))
print('streaming needs far less memory than a whole tree:', res['SAX (stream)'][1] * 100 < res['ElementTree parse (whole tree)'][1] and res['ElementTree iterparse with clear()'][1] * 5 < res['ElementTree parse (whole tree)'][1], '| minidom needs more than ElementTree:', res['minidom (DOM, whole tree)'][1] > res['ElementTree parse (whole tree)'][1])
print('iterparse without clear() keeps the whole tree alive:', end=' ')
def et_iter_noclear():
    t = 0
    for ev, e in ET.iterparse('big.xml', events=('end',)):
        if e.tag == 'qty': t += int(e.text)
    return t
r, pk, t = peak(et_iter_noclear); print('MEASURED peak %.1f MiB' % (pk / 2**20))
'''),
 ("The three formats side by side on the chapter's Alice data: sizes, what each keeps of the types after a round trip, why CSV cannot hold the nesting, and the two formats the chapter skips (TOML is in the standard library since 3.11, YAML is not)", GET + r'''import json, csv, io, xml.etree.ElementTree as ET, xmltodict, tomllib
data = {'name': 'Alice Doe', 'age': 30, 'car': None, 'programmer': True, 'address': {'street': '100 Larkin St.', 'city': 'San Francisco', 'zip': '94102'}, 'phone': [{'type': 'mobile', 'number': '415-555-7890'}, {'type': 'work', 'number': '415-555-1234'}]}
x_pretty = pres()[20].rstrip('\n'); x_compact = re.sub(r'>\s+<', '><', x_pretty)
print('characters: JSON compact', len(json.dumps(data)), '| JSON indent=2', len(json.dumps(data, indent=2)), '| XML as printed (indented)', len(x_pretty), '| XML without the whitespace', len(x_compact), '| Python repr', len(repr(data)))
print('XML as printed is well-formed:', ET.fromstring(x_pretty).tag, '| the XML needs', round(len(x_compact) / len(json.dumps(data)), 2), 'times the characters of the compact JSON')
j = json.loads(json.dumps(data)); print('JSON round trip keeps every type:', j == data, {k: type(v).__name__ for k, v in j.items()})
x = xmltodict.parse(x_pretty)['person']; print('XML (xmltodict) gives strings only:', {k: (type(v).__name__, v if not isinstance(v, dict) else '...') for k, v in x.items() if k in ('age', 'programmer', 'car')})
r = ET.fromstring(x_pretty); print('XML (ElementTree) gives strings only:', type(r.find('age').text).__name__, repr(r.find('age').text), repr(r.find('programmer').text))
flat = {'name': data['name'], 'age': data['age'], 'car': data['car'], 'programmer': data['programmer'], 'street': data['address']['street'], 'city': data['address']['city'], 'zip': data['address']['zip'], 'phone1_type': data['phone'][0]['type'], 'phone1_number': data['phone'][0]['number'], 'phone2_type': data['phone'][1]['type'], 'phone2_number': data['phone'][1]['number']}
s = io.StringIO(newline=''); w = csv.DictWriter(s, list(flat)); w.writeheader(); w.writerow(flat); print(s.getvalue().strip().split('\r\n')[1])
back = next(csv.DictReader(io.StringIO(s.getvalue()))); print('CSV needs a flat row (the chapter: "rows of data that share the same columns"); after a round trip:', {k: back[k] for k in ('age', 'car', 'programmer')}, '| types', {type(v).__name__ for v in back.values()})
print('a person with three phones needs a different set of columns, so the file is no longer rectangular in meaning:', len({'phone1_type', 'phone2_type', 'phone3_type'} - set(flat)), 'new columns')
T = 'name = "Alice Doe"\nage = 30\nprogrammer = true\n[address]\nstreet = "100 Larkin St."\ncity = "San Francisco"\nzip = "94102"\n[[phone]]\ntype = "mobile"\nnumber = "415-555-7890"\n[[phone]]\ntype = "work"\nnumber = "415-555-1234"\n'
t = tomllib.loads(T); print('tomllib (3.11+, read only):', t == {k: v for k, v in data.items() if k != 'car'}, '| TOML has no null: the key car is absent;', 'tomllib has dumps:', hasattr(tomllib, 'dumps'), '| names', sorted(n for n in dir(tomllib) if not n.startswith('_')))
print('TOML keeps types:', {k: type(v).__name__ for k, v in t.items() if k in ('age', 'programmer')}, '| and dates:', tomllib.loads('d = 2035-04-05T13:34:02')['d'].__class__.__name__)
print('YAML: import yaml in the study environment:', end=' ')
r = sh([sys.executable, '-I', '-c', 'import yaml']); print(r.stderr.strip().splitlines()[-1])
print('shelve (named by the chapter) is binary and Python-only:', end=' ')
import shelve, dbm; db = shelve.open('db'); db['d'] = data; db.close(); b = open([f for f in os.listdir('.') if f.startswith('db')][0], 'rb').read()[:8]; print('first bytes of the file', b, '| dbm backend', dbm.whichdb('db'), '| files', sorted(f for f in os.listdir('.') if f.startswith('db')))
'''),
 ("The eleven practice questions answered by running code, with the answers Appendix B of the book prints beside them", GET + r'''import csv, json, io, xml.etree.ElementTree as ET
d = work(); make_example3()
b = cached('ch18_appendixb.html', 'https://automatetheboringstuff.com/3e/appendixb.html').decode('utf-8')
t = html.unescape(re.sub(r'<[^>]+>', '', b)); i = t.find('Chapter 18\n'); i = [m.start() for m in re.finditer(r'Chapter 18', t)][-1]; j = t.find('Chapter 19', i)
ans = re.sub(r'\s+', ' ', t[i:j]); print('Appendix B, chapter 18, as printed:', ans[:1500])
print()
print('Q1 CSV cannot hold: other data types than strings:', {type(v).__name__ for v in next(csv.reader(open('example3.csv')))}, '| fonts, widths, merged cells, images and charts have no place in a text file of comma-separated lines')
print('Q2 a file object, or any iterable of strings:', next(csv.reader(open('example3.csv')))[1], next(csv.reader(['x,y']))[1], '| a writer takes any object with write():', end=' ')
s = io.StringIO(); csv.writer(s).writerow(['a']); print(repr(s.getvalue()))
print('Q3 the modes of the File objects: text mode for both ("r" and "w" with newline=""), not rb and wb:')
try: next(csv.reader(open('example3.csv', 'rb')))
except csv.Error as e: print('   csv.reader on a file opened "rb":', type(e).__name__, e)
try: csv.writer(open('o.csv', 'wb')).writerow(['a'])
except Exception as e: print('   csv.writer on a file opened "wb":', type(e).__name__, e)
w = csv.writer(open('o.csv', 'w', newline='')); w.writerow(['a']); print('   "w" with newline="" works:', w.writerow(['b']))
print('Q4 writerow takes a list (any iterable) and returns the number of characters written:', csv.writer(io.StringIO()).writerow(('a', 'b')), '| writerows takes a list of rows')
f = io.StringIO(newline=''); w = csv.writer(f, delimiter='|', lineterminator='!\n'); w.writerow(['a', 'b']); w.writerow(['c', 'd']); print('Q5 delimiter separates cells, lineterminator ends rows (writer only):', repr(f.getvalue()), '| the reader ignores lineterminator:', list(csv.reader(['a|b!', 'c|d!'], delimiter='|')))
print('Q6 all three are plain text:', all(isinstance(x, str) for x in (json.dumps({}), ET.tostring(ET.Element('a'), encoding='unicode'), 'a,b')))
print('Q7', json.loads.__name__, json.loads('{"a": null}'), '| Q8', json.dumps.__name__, json.dumps({'a': None}))
print('Q9 XML (tags in angle brackets, like HTML): <person><name>Alice</name></person> parses as', ET.fromstring('<person><name>Alice</name></person>')[0].tag)
print('Q10', json.dumps(None), '| Q11', json.dumps([True, False]))
'''),
 ("Practice Program: the Excel-to-CSV converter. The printed skeleton, a converter written to it, run on example3.xlsx, produceSales3.xlsx and censuspopdata.xlsx, the dates it writes against the CSV text of the chapter, the 26 files of excelSpreadsheets.zip, and what LibreOffice writes", GET + r'''import csv, openpyxl, time
d = work('example3.xlsx', 'produceSales3.xlsx', 'censuspopdata.xlsx', 'excelSpreadsheets.zip')
sk = pres()[34]
try: compile(sk, '<skeleton>', 'exec')
except SyntaxError as e: print('the skeleton as printed:', type(e).__name__, e.msg, '(line %d)' % e.lineno, '| it uses wb, sheet and csv_file that it never defines, and calls no import')
SOL = """import csv, os, openpyxl
for excel_file in sorted(os.listdir('.')):
    if not excel_file.endswith('.xlsx'):
        continue
    wb = openpyxl.load_workbook(excel_file)
    for sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]
        csv_filename = os.path.splitext(excel_file)[0] + '_' + sheet.title + '.csv'
        csv_file = open(csv_filename, 'w', newline='', encoding='utf-8')
        csv_writer = csv.writer(csv_file)
        max_row, max_column = sheet.max_row, sheet.max_column
        for row_num in range(1, max_row + 1):
            row_data = []
            for col_num in range(1, max_column + 1):
                row_data.append(sheet.cell(row=row_num, column=col_num).value)
            csv_writer.writerow(row_data)
        csv_file.close()
        print('wrote', csv_filename)
"""
open('excel_to_csv.py', 'w').write(SOL)
t = time.perf_counter(); r = sh([sys.executable, 'excel_to_csv.py']); el = time.perf_counter() - t
print('exit', r.returncode, '| stderr', r.stderr.strip()[-100:] or None); print(r.stdout)
print('MEASURED seconds for the three workbooks: %.1f' % el)
import openpyxl as ox
ws = ox.load_workbook('produceSales3.xlsx').active
print('the skeleton evaluates sheet.max_column once for every row; each evaluation visits every cell of the sheet (produceSales3.xlsx:', ws.max_row, 'rows,', ws.max_column, 'columns):')
for n in (250, 500, 1000, 2000):
    t = time.perf_counter()
    for r in range(1, n + 1):
        for c in range(1, ws.max_column + 1): ws.cell(row=r, column=c).value
    a = time.perf_counter() - t; t = time.perf_counter(); mc = ws.max_column
    for r in range(1, n + 1):
        for c in range(1, mc + 1): ws.cell(row=r, column=c).value
    print('MEASURED first %4d rows: max_column inside the row loop %.2f s, hoisted %.3f s' % (n, a, time.perf_counter() - t))
print('the loop as the skeleton nests it costs time proportional to rows times cells; the converter above hoists both limits out of the loops')
print('example3_Sheet1.csv:'); print(open('example3_Sheet1.csv', newline='').read().replace('\r\n', '\n'))
print('Sheet2 and Sheet3 are empty sheets:', open('example3_Sheet2.csv', 'rb').read(), open('example3_Sheet3.csv', 'rb').read())
printed = [l.split(',') for l in pres()[0].strip().split('\n')]; got = list(csv.reader(open('example3_Sheet1.csv', newline='')))
print('first row the chapter prints', printed[0], '| the program writes', got[0], '| equal:', printed == got)
r = sh(['soffice', '--headless', '--convert-to', 'csv:Text - txt - csv (StarCalc):44,34,76,1,,0,false,true,false,false,false,-1', '--outdir', 'lo', 'example3.xlsx'], timeout=300)
print('LibreOffice writes one CSV per sheet with the option -1:', sorted(os.listdir('lo')), '| first file:'); print(open('lo/' + sorted(os.listdir('lo'))[0], newline='').read().replace('\r\n', '\n')[:400])
print('records written: produceSales3_Sheet.csv', sum(1 for _ in csv.reader(open('produceSales3_Sheet.csv', newline=''))), '| files produced:', sorted(f for f in os.listdir('.') if f.endswith('.csv'))[:8], '...', len([f for f in os.listdir('.') if f.endswith('.csv')]))
zipfile.ZipFile('excelSpreadsheets.zip').extractall('xl'); os.chdir('xl'); shutil.copy('../excel_to_csv.py', '.')
r = sh([sys.executable, 'excel_to_csv.py']); print('the program in the folder of excelSpreadsheets.zip: exit', r.returncode, '| output', repr(r.stdout), '| the folder holds', len(os.listdir('.')) - 1, 'files, all .csv, none .xlsx')
print('what a spreadsheet file with dates, formulas and a rich title does:')
wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Q1 Sales'; import datetime
ws.append([datetime.date(2035, 4, 5), datetime.datetime(2035, 4, 5, 13, 34, 2), 1.5, '=SUM(C1:C1)', None, True, 'text with, comma'])
wb.save('t.xlsx')
w2 = openpyxl.load_workbook('t.xlsx'); print('  values', [c.value for c in w2.active[1]], '| with data_only=True', [c.value for c in openpyxl.load_workbook('t.xlsx', data_only=True).active[1]])
s = io.StringIO(newline=''); csv.writer(s).writerow([c.value for c in w2.active[1]]); print('  csv line:', repr(s.getvalue()))
for bad in ('a/b', 'a[b]', 'a:b', 'a?b'):
    try: wb.create_sheet(bad); print('  sheet title', repr(bad), 'accepted')
    except Exception as e: print('  sheet title', repr(bad[:12]), type(e).__name__, e)
print('what the chapter\'s own title rule gives for "Sheet1" of example3.xlsx: example3_Sheet1.csv (the pattern <excel filename>_<sheet title>.csv)')
'''),
 ("Names an older tutorial uses and whether the Python 3.14 standard library still has them, and the modules the chapter names, imported", GET + r'''import importlib, warnings
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always'); import xml.etree.cElementTree as cET
print('import xml.etree.cElementTree: ok; same Element class as ElementTree:', cET.Element is __import__('xml.etree.ElementTree').etree.ElementTree.Element, '| warnings raised on import:', [(x.category.__name__, str(x.message)[:80]) for x in w], '| the module file', cET.__file__.split('/')[-1], '| the 3.14 documentation says the alias is deprecated since 3.3')
for name in ('xml.etree.cElementTree', 'xml.etree.ElementTree', 'xml.dom', 'xml.dom.minidom', 'xml.sax', 'xml.parsers.expat', 'csv', 'json', 'shelve', 'tomllib', 'simplejson', 'lxml', 'defusedxml', 'xmltodict'):
    try: m = importlib.import_module(name); print('%-28s import ok' % name, getattr(m, '__version__', ''))
    except ImportError as e: print('%-28s %s: %s' % (name, type(e).__name__, str(e)[:70]))
import xml.etree.ElementTree as ET, csv, json
e = ET.Element('a'); ET.SubElement(e, 'b')
print('Element methods of Python 2 tutorials:', {n: hasattr(e, n) for n in ('getchildren', 'getiterator', 'iter', 'iterfind', 'findall', 'itertext')})
print('ElementTree.getiterator:', hasattr(ET.ElementTree, 'getiterator'), '| ET.XMLTreeBuilder:', hasattr(ET, 'XMLTreeBuilder'), '| ET.XMLParser:', hasattr(ET, 'XMLParser'), '| ET.XMLPullParser:', hasattr(ET, 'XMLPullParser'), '| ET.indent:', hasattr(ET, 'indent'), '| ET.canonicalize:', hasattr(ET, 'canonicalize'))
print('csv names: QUOTE_STRINGS', hasattr(csv, 'QUOTE_STRINGS'), '| csv.excel_tab', hasattr(csv, 'excel_tab'), '| csv.unix_dialect', hasattr(csv, 'unix_dialect'))
print('json names: JSONDecodeError', hasattr(json, 'JSONDecodeError'), '| json.tool', importlib.import_module('json.tool').__name__, '| json.loads encoding keyword (removed 3.9):', end=' ')
try: json.loads('{}', encoding='utf-8')
except TypeError as ex: print(type(ex).__name__, str(ex)[:70])
print('open(..., "U") (universal newlines, removed 3.11):', end=' ')
try: open(__file__ if '__file__' in globals() else '/etc/hostname', 'U')
except ValueError as ex: print(type(ex).__name__, ex)
'''),
 ("The XML statements of the chapter tested one by one: case, quotes, attributes against subelements, single root (well-formed, not valid), comments, SVG, RSS and Atom, and the parts of a .docx file", GET + r'''import xml.etree.ElementTree as ET
d = work('demo.docx')
def t(label, text):
    try: r = ET.fromstring(text); print('%-62s ok  %s' % (label, ET.tostring(r, encoding='unicode')[:70]))
    except ET.ParseError as e: print('%-62s ERR %s' % (label, e))
t('tag names are case-sensitive: <A></a>', '<A></a>')
t('"any case": <Person><NAME>x</NAME></Person>', '<Person><NAME>x</NAME></Person>')
t('attribute value in single quotes', "<a b='1'/>")
t('attribute value without quotes (HTML allows it)', '<a b=1/>')
t('attribute with no value (HTML allows it)', '<a disabled/>')
t('the same attribute twice', '<a b="1" b="2"/>')
t('an unclosed tag (HTML allows <br>)', '<a><br></a>')
t('overlapping tags', '<a><b><c></b></c></a>')
t('a comment', '<a><!-- ignored --></a>')
t('two hyphens inside a comment', '<a><!-- a -- b --></a>')
t('a less-than sign in text', '<a>1 < 2</a>')
t('an ampersand in text', '<a>fish & chips</a>')
t('&amp; and &lt; escapes', '<a>fish &amp; chips &lt; 5</a>')
t('an HTML entity (&nbsp;) that XML does not define', '<a>x&nbsp;y</a>')
t('a CDATA section', '<a><![CDATA[1 < 2 & 3]]></a>')
t('a tag name starting with a digit', '<1a/>')
t('a tag name with a space', '<a b/>')
t('the address written with attributes (the chapter)', '<address street="100 Larkin St." city="San Francisco" zip="94102" />')
t('the XML declaration after whitespace', ' <?xml version="1.0"?><a/>')
t('empty input', '')
print('"valid" in the chapter ("A document with multiple roots ... is not valid"): the W3C term is well-formed; "valid" means conforming to a DTD or schema. ElementTree checks well-formedness only: a document with a DOCTYPE it does not satisfy parses:', ET.fromstring('<!DOCTYPE a [<!ELEMENT a (b)>]><a><c/></a>').tag)
a = ET.fromstring('<address street="100 Larkin St." city="San Francisco" zip="94102" />'); print('the attribute form:', a.attrib, '| the subelement form gives', {e.tag: e.text for e in ET.fromstring('<address><street>100 Larkin St.</street><city>San Francisco</city><zip>94102</zip></address>')})
svg = '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="20"><rect width="40" height="20" fill="teal"/><text x="5" y="14">hi</text></svg>'
r = ET.fromstring(svg); print('SVG is XML:', r.tag, '| the elements are', [e.tag for e in r], '| with the namespace stripped', [e.tag.split('}')[1] for e in r])
rss = '<rss version="2.0"><channel><title>Feed</title><item><title>One</title><link>http://example.org/1</link></item><item><title>Two</title></item></channel></rss>'
print('RSS items:', [i.findtext('title') for i in ET.fromstring(rss).iter('item')])
atom = '<feed xmlns="http://www.w3.org/2005/Atom"><title>Feed</title><entry><title>One</title></entry></feed>'
print('Atom needs the namespace in the search:', ET.fromstring(atom).findall('entry'), ET.fromstring(atom).findall('{http://www.w3.org/2005/Atom}entry'), ET.fromstring(atom).findall('a:entry', {'a': 'http://www.w3.org/2005/Atom'}))
z = zipfile.ZipFile('demo.docx'); names = z.namelist(); body = ET.fromstring(z.read('word/document.xml')); W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
print('.docx is a ZIP:', zipfile.is_zipfile('demo.docx'), '| parts', len(names), names[:5], '| paragraphs in word/document.xml:', len(list(body.iter(W + 'p'))), '| text:', ''.join(x.text or '' for x in body.iter(W + 't'))[:60])
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
        ver = subprocess.run([PY, "-c", "import sys, importlib.metadata as m; print(sys.version.split()[0], 'xmltodict', m.version('xmltodict'), 'openpyxl', m.version('openpyxl'))"], capture_output=True, text=True).stdout.strip()
        json.dump({"_version": "1.0.0", "_note": "Recorded by sen0414_ch18_thirdparty_v1_0_0.py write; every output was printed by the program beside it under the interpreter named in the field python. The chapter page and the online materials are fetched at run time and not kept in the repository. A line that starts with MEASURED is a timing on the machine of the day.", "python": ver, "items": out}, open(REC, "w"), indent=1, ensure_ascii=False)
        print("recorded", len(out), "programs to", REC)
        for o in out:
            if "FAILED" in o["output"]: print("  FAILED:", o["what"], "|", o["output"][-200:])
    else:
        old = json.load(open(REC))["items"]; bad = [a["what"] for a, b in zip(old, out) if strip(a["output"]) != strip(b["output"]) or a["code"] != b["code"]]
        print("%d programs; %d differ" % (len(out), len(bad)))
        for b in bad: print("  DIFFERS", b)
        sys.exit(1 if bad else 0)

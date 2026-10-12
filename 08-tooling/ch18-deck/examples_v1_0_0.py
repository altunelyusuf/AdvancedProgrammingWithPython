"""Chapter 18 deck examples: every console session, whole program (or excerpt), chart and table the lecture deck shows. Nothing here
carries a result; examples_run_v1_0_0.py runs it all under the interpreter given (the uv Python 3.14.6 of the chapter 18 research
environment /home/claude/venv314_ch18_latest, with xmltodict 1.0.4, defusedxml 0.7.1, openpyxl 3.1.5 and lxml 6.1.3 installed; csv, json
and xml.etree.ElementTree are the standard library) and records the results. A console group is one session: its rows run in order in one
namespace (the deck check re-runs them per slide, one namespace per slide). No console row touches the network or the file system: each
uses only text and io objects made in memory, so each can be typed into a Python in a browser that offers the standard library (xmltodict
and defusedxml are not in the standard library; no console row uses them except the title slide's version rows, and the programs that
import them are listed in the run; none of this was tried in a browser by this build). A row that would print an object whose repr holds a
memory address is written as an assignment to _ or reads an attribute instead.

Programs come from sen0414_ch18_corpus_base_v1_0_0.py, all twelve, run and recorded under their own names. A corpus line is often wider than a
slide can show without wrapping, so the slides show deck-written copies (the corpus program cut into pieces that fit a slide, with
comments); the first five lines of every program are the corpus HEAD (imports, a temporary folder, the sample EXAMPLE and the helper save())
and are not shown. SUBSET lists the copies whose printed lines must all be lines the corpus original printed, in the same order; EQUIV
lists copies whose transcript must equal the original's.
KIND says what a program's output depends on, so that honesty_check can require the matching words on the slide that shows it. Every
program of this chapter builds its own files in a temporary folder and needs no network, so none is 'live'; the programs that stand a
Python object in for a Windows machine are 'emulated' and the slide that shows one must say EMULATED."""
__version__ = "1.0.0"
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("base18", os.path.join(HERE, "..", "sen0414_ch18_corpus_base_v1_0_0.py"))
B = importlib.util.module_from_spec(_s)
_s.loader.exec_module(B)
_HEAD = B.HEAD

CONSOLES = {
    "title": ["import platform, importlib.metadata as m", "platform.python_version()", "m.version('xmltodict')", "m.version('defusedxml')"],
    "csvnames": ["import csv", "sorted(csv.list_dialects())", "len([n for n in dir(csv) if n.startswith('QUOTE_')])", "csv.field_size_limit()"],
    "split": ["import csv", "line = 'Alice,30,\"San Francisco, CA\"'", "line.split(',')", "next(csv.reader([line]))"],
    "appb": ["import csv, io", "list(csv.reader(io.BytesIO(b'a,b\\r\\n')))", "csv.writer(io.BytesIO()).writerow(['a'])",
             "list(csv.reader(io.StringIO('a,b\\r\\n')))"],
    "limits": ["import csv, io", "csv.field_size_limit()", "next(csv.reader(['x' * 131073]))", "q = csv.QUOTE_NOTNULL",
               "list(csv.reader(io.StringIO('a,,\"\"\\r\\n'), quoting=q))",
               "list(csv.reader(['a\\tb'], dialect='excel-tab'))"],
    "jsonstrict": ["import json", "json.loads('[\"spam\", \"eggs\"]')", "json.loads('[\"spam\", \"eggs\",]')"],
}

# ---- programs written for the deck ---------------------------------------------------------------------------------------------
READER = _HEAD + '''# Reading: list(), a for loop with line_num, and a reader used once.
save('example.csv', EXAMPLE)   # 4 records, one with a line break
with open('example.csv', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    rows = list(reader)
    print(rows[3])
    print('a second list():', list(reader))
with open('example.csv', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print('Row #' + str(reader.line_num) + ' ' + str(row))
print({type(v).__name__ for r in rows for v in r})
print(hasattr(reader, '__len__'), hasattr(reader, '__getitem__'))
'''

MEMORY = _HEAD + '''# A for loop over the reader keeps one row in memory; list() keeps them all.
import tracemalloc
def peak(use_list):
    rows = ''.join('%d,n%d,%s\\r\\n' % (i, i, 'x' * 40) for i in range(60000))
    save('big.csv', rows)
    with open('big.csv', encoding='utf-8', newline='') as f:
        tracemalloc.start(); r = csv.reader(f)
        if use_list: n = len(list(r))
        else: n = sum(1 for _ in r)
        p = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    return n, p
a, b = peak(True), peak(False)
print('rows', a[0], b[0], '| list() peaks over 10x the loop:', a[1] > 10 * b[1])
'''

WRITER = _HEAD + '''# The writer: writerow() returns the length written; types are converted.
with open('o.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    print(w.writerow(['spam', 'eggs', 'bacon', 'ham']))
    print(w.writerow(['Hello, world!', 'eggs', 'bacon', 'ham']))
    print(w.writerow([1, 3.141592, None, '', True]))
for line in open('o.csv', 'rb'): print(line)
with open('t.tsv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\\t', lineterminator='\\n')
    w.writerow(['a', 'b c', 'd'])
    w.writerows([['x', 'y', 'z']])
print(open('t.tsv', 'rb').read())
'''

NEWLINE = _HEAD + '''# Windows turns \\n into \\r\\n when a file is opened without newline=''.
# EMULATED: a TextIOWrapper asked for that translation stands in for Windows.
for label, nl in (("newline=''", ''), ('Windows default', '\\r\\n')):
    buf = io.BytesIO()
    t = io.TextIOWrapper(buf, encoding='utf-8', newline=nl)
    csv.writer(t).writerow(['a', 'b']); t.flush()
    data = buf.getvalue()
    back = io.StringIO(data.decode(), newline='')
    print(label, data, list(csv.reader(back)))
'''

DICTS = _HEAD + '''# DictReader: the first row gives the keys; restkey and restval for short and long rows.
save('example.csv', 'Name,Age\\r\\nAlice,30\\r\\nBob\\r\\nCarol,41,extra,more\\r\\n')
with open('example.csv', encoding='utf-8', newline='') as f:
    for row in csv.DictReader(f): print(dict(row))
with open('example.csv', encoding='utf-8', newline='') as f:
    for row in csv.DictReader(f, restkey='rest', restval='?'): print(dict(row))
with open('out.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, ['Name', 'Age'])
    print(w.writeheader(), w.writerow({'Name': 'Dave', 'Age': 5}))
    print(w.writerow({'Name': 'Eve'}))
    try: w.writerow({'Name': 'Frank', 'Age': 9, 'City': 'Rome'})
    except ValueError as e: print('ValueError:', e)
print(open('out.csv', 'rb').read())
'''

ENCODING = _HEAD + '''# Excel's "CSV UTF-8" starts with a byte order mark; open() needs an encoding.
text = 'Name,City\\r\\nZoe,İstanbul\\r\\n'
save('u.csv', text, 'utf-8-sig')
raw = open('u.csv', 'rb').read()
print(raw[:3], raw[3:12])
print(repr(open('u.csv', encoding='utf-8', newline='').readline()))
print(repr(open('u.csv', encoding='utf-8-sig', newline='').readline()))
with open('u.csv', encoding='utf-8', newline='') as f:
    print(list(next(csv.DictReader(f))))
print(raw.decode('cp1252', errors='replace')[:12])
save('c.csv', 'Ad,Sehir\\r\\nZoe,Şişli\\r\\n', 'cp1254')
try: open('c.csv', encoding='utf-8').read()
except UnicodeDecodeError as e: print('UnicodeDecodeError:', e.reason)
'''

PROJECT = _HEAD + '''# Project 13 on generated files; the last four lines use a header with a line break.
from pathlib import Path
Path('headerRemoved').mkdir(exist_ok=True)
save('f0.csv', 'h1,h2\\r\\n1,1\\r\\n1,2\\r\\n'); save('empty.csv', '')
for csv_filename in sorted(Path('.').glob('*.csv')):
    print('Removing header from ' + csv_filename.name + '...')
    with open(csv_filename, encoding='utf-8', newline='') as f_in:
        reader = csv.reader(f_in); next(reader, None)
        out = Path('headerRemoved') / csv_filename.name
        with open(out, 'w', encoding='utf-8', newline='') as f_out:
            csv.writer(f_out).writerows(reader)
for n in ('f0', 'empty'):
    print(open('headerRemoved/%s.csv' % n, 'rb').read())
save('multi.csv', '"Name\\r\\n(first)",Age\\r\\nAlice,30\\r\\n')
with open('multi.csv', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    print([row for row in reader if reader.line_num != 1])
'''

JSONB = _HEAD + '''# json.loads() and json.dumps(): the chapter's six types, indent, and a round trip.
js = '{"name": "Alice", "age": 30, "car": null, "ok": true}'
data = json.loads(js)
print(data, type(data).__name__)
print(data['car'] is None, data['ok'] is True)
print(json.dumps(data) == js)
print(json.dumps(data, indent=2))
'''

JTYPES = _HEAD + '''# What JSON does to Python values on the way out and back.
d = {'t': (1, 2), 1: 'a', None: 'c'}
s = json.dumps(d); print(s)
print(json.loads(s))
print(json.dumps({'city': 'İstanbul'}))
print(json.dumps({'city': 'İstanbul'}, ensure_ascii=False))
for v in ({1, 2}, b'x', 1j, {(1, 2): 3}):
    try: json.dumps(v)
    except TypeError as e: print(type(e).__name__, e)
'''

JGAPS = _HEAD + '''# NaN, a file, a byte order mark, a long integer and the notes of Python 3.14.
print(json.dumps(float('nan')), json.loads('[Infinity]'))
with open('p.json', 'w', encoding='utf-8') as f:
    json.dump({'city': 'İstanbul', 'n': [1, None, True]}, f,
              ensure_ascii=False)
print(open('p.json', 'rb').read())
print(json.load(open('p.json', encoding='utf-8')))
print(json.loads(b'\\xef\\xbb\\xbf[1]'))
try: json.loads('\\ufeff[1]')
except json.JSONDecodeError as e: print('str with a BOM:', e.msg)
try: json.loads('1' * 5000)
except ValueError as e: print('long integer:', str(e)[:31])
try: json.dumps([0, {'a': {1}}])
except TypeError as e:
    for note in e.__notes__: print('note:', note)
'''

ETREAD = _HEAD + '''# ElementTree reading: the root, its children, text, document order and find().
import xml.etree.ElementTree as ET
doc = ('<person><name>Alice Doe</name><age>30</age><car/>'
       '<address><city>San Francisco</city></address>'
       '<phone type="mobile">415</phone>'
       '<phone type="work">123</phone></person>')
root = ET.fromstring(doc)
print(root.tag, [c.tag for c in root])
print(root[0].text, repr(root[2].text), repr(root.text))
print([e.tag for e in root.iter()])
print(root.find('address/city').text)
print([p.get('type') for p in root.findall('phone')])
print(root.find('phone[@type="work"]').text, root.find('nothing'))
age = root.find('age').text
print('age is a', type(age).__name__, '| converted:', int(age) + 1)
'''

ETTRAPS = _HEAD + '''# What the chapter's statements leave out: whitespace, the truth value, errors and iterparse.
import warnings, xml.etree.ElementTree as ET
a = ET.fromstring('<a>\\n  <b>x</b>\\n  <c><d/></c>\\n</a>')
print(repr(a.text), repr(a[0].tail), repr(a[1].text))
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always'); print(bool(a[0]))
print([x.category.__name__ for x in w], a.find('zzz') is None)
for bad in ('<a><b></a>', '<a/><b/>', '<A></a>', '<a b=1/>'):
    try: ET.fromstring(bad)
    except ET.ParseError as e: print(bad, '->', e)
data = io.BytesIO(b'<r><i>x</i><i>y</i><i>z</i></r>')
for event, el in ET.iterparse(data, events=('end',)):
    print(event, el.tag, el.text); el.clear()
'''

ETWRITE = _HEAD + '''# Writing: SubElement, set, tostring and its space, indent, and a prefix nobody declared.
import xml.etree.ElementTree as ET
p = ET.Element('p')
c = ET.SubElement(p, 'car'); c.set('xsi:nil', 'true')
ET.SubElement(p, 'note').text = 'a < b & "c"'
print(ET.tostring(p)[:16])
print(ET.tostring(p, encoding='unicode'))
ET.indent(p); print(ET.tostring(p, encoding='unicode'))
try: ET.fromstring(ET.tostring(p, encoding='unicode'))
except ET.ParseError as e: print('ParseError:', e)
'''

ETNS = _HEAD + '''# Reading a namespaced attribute and a namespaced name.
import xml.etree.ElementTree as ET
XSI = 'http://www.w3.org/2001/XMLSchema-instance'
X = ('<person xmlns:xsi="%s"><car xsi:nil="true"/>'
     '<boat xsi:nil="true">full</boat></person>' % XSI)
r = ET.fromstring(X)
print(repr(r[0].text), repr(r[1].text))
print(r[0].attrib)
A = 'http://example.org/a'
n = ET.fromstring('<a:r xmlns:a="%s"><a:i>1</a:i><i>2</i></a:r>' % A)
print(n.tag, [c.tag for c in n])
print(n.find('{%s}i' % A).text, n.find('i').text)
print(n.find('a:i', {'a': A}).text)
'''

XTD = _HEAD + '''# xmltodict: strings, one entry against many, attributes with @, and unparse.
import xmltodict
X = ('<person><name>Alice Doe</name><age>30</age>'
     '<phone type="mobile">415</phone></person>')
d = xmltodict.parse(X)
print(type(d['person']['age']).__name__, d['person']['phone'])
print(xmltodict.parse('<a><b>1</b></a>'))
print(xmltodict.parse('<a><b>1</b><b>2</b></a>'))
print(xmltodict.parse('<a><b>1</b></a>', force_list=('b',)))
print(xmltodict.unparse(d, pretty=True))
back = xmltodict.parse(xmltodict.unparse(d))
print(back == d, xmltodict.parse('<a><b/></a>'))
'''

SECURITY = _HEAD + '''# A billion laughs, an external entity, and defusedxml.
import xml.etree.ElementTree as ET
import defusedxml, defusedxml.ElementTree as DET
def ent(i):
    return '<!ENTITY l%d "%s">' % (i, ('&l%d;' % (i - 1)) * 10)
ents = ''.join(ent(i) for i in range(1, 10))
laughs = '<!DOCTYPE d [<!ENTITY l0 "lol">' + ents + ']><d>&l9;</d>'
try: ET.fromstring(laughs)
except ET.ParseError as e: print(len(laughs), 'bytes:', str(e)[:44])
try: DET.fromstring(laughs)
except defusedxml.EntitiesForbidden as e: print(type(e).__name__)
ext = ('<!DOCTYPE d [<!ENTITY x SYSTEM "file:///etc/hostname">]>'
       '<d>&x;</d>')
try: ET.fromstring(ext)
except ET.ParseError as e: print('external entity:', e)
'''


PROGRAMS = dict(B.PROGRAMS)
for _n, _c in (("readerCut", READER), ("memoryCut", MEMORY), ("writerCut", WRITER), ("newlineCut", NEWLINE), ("dictsCut", DICTS),
               ("encodingCut", ENCODING), ("project13Cut", PROJECT), ("jsonBasicsCut", JSONB), ("jsonTypesCut", JTYPES),
               ("jsonGapsCut", JGAPS), ("etReadCut", ETREAD), ("etTrapsCut", ETTRAPS), ("etWriteCut", ETWRITE), ("etNamespaceCut", ETNS),
               ("xmltodictCut", XTD), ("securityCut", SECURITY)):
    PROGRAMS[_n + "_v1_0_0.py"] = (_c, (), False)

# copy -> original: every printed line of the copy must be a line the original printed, in the same order (SUBSET); a copy that prints its
# own lines (another way of printing, shorter lines) is not listed and is checked only by being run again. EQUIV (a copy whose transcript
# must equal the original's) lists copies that print exactly what the original prints.
SUBSET = {}
EQUIV = {}
KIND = {n: "none" for n in PROGRAMS}
KIND["newlineCut_v1_0_0.py"] = "emulated"
LIVEKEY = {}
EMUKEY = {"newlineCut_v1_0_0.py": ("EMULATED",)}

# ---- charts and tables: each a setup and one expression --------------------------------------------------------------------------
_SIZES = ("import json, xml.etree.ElementTree as ET\n"
          "A = {'name': 'Alice Doe', 'age': 30, 'car': None, 'programmer': True, 'address': {'street': '100 Larkin St.', 'city': 'San Francisco', 'zip': '94102'}, 'phone': [{'type': 'mobile', 'number': '415-555-7890'}, {'type': 'work', 'number': '415-555-1234'}]}\n"
          "NS = 'xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"'\n"
          "XS = '<person><name>Alice Doe</name><age>30</age><programmer>true</programmer><car xsi:nil=\"true\" ' + NS + '/><address><street>100 Larkin St.</street><city>San Francisco</city><zip>94102</zip></address><phone><phoneEntry><type>mobile</type><number>415-555-7890</number></phoneEntry><phoneEntry><type>work</type><number>415-555-1234</number></phoneEntry></phone></person>'\n"
          "def sizes():\n"
          "    t = ET.fromstring(XS); ET.indent(t)\n"
          "    return [['JSON, compact', len(json.dumps(A))], ['JSON, indent=2', len(json.dumps(A, indent=2))],\n"
          "            ['XML, compact', len(XS)], ['XML, ET.indent()', len(ET.tostring(t, encoding='unicode'))]]\n")
CHARTS = {"formatSizes": {"setup": _SIZES, "expr": "sizes()"}}
_QUOTE = ("import csv, io\n"
          "def line(q):\n"
          "    s = io.StringIO(newline=''); kw = {'escapechar': '\\\\'} if q == 'QUOTE_NONE' else {}\n"
          "    csv.writer(s, quoting=getattr(csv, q), **kw).writerow(['a b', 'c,d', 7, None, '']); return s.getvalue()\n")
_REFUSE = ("import json\n"
           "def msg(t):\n"
           "    try: json.loads(t); return 'accepted'\n"
           "    except json.JSONDecodeError as e: return '%s (column %d)' % (e.msg, e.colno)\n")
TABLES = {
    "quotingConstants": {"setup": _QUOTE,
                         "expr": "[['quoting=', 'the line written']] + [[q, repr(line(q))] for q in ('QUOTE_MINIMAL', 'QUOTE_ALL', 'QUOTE_NONNUMERIC', 'QUOTE_NONE', 'QUOTE_STRINGS', 'QUOTE_NOTNULL')]"},
    "jsonRefusals": {"setup": _REFUSE,
                     "expr": "[['text', 'json.loads says']] + [[repr(t), msg(t)] for t in ('[\"spam\", \"eggs\",]', \"{'a': 1}\", '{\"a\": 1} // c', '[None]', '[NaN]', '')]"}}

# ---- runs under other environments of the research (recorded, then used in a card) ---------------------------------------------------
BARE_CODE = ("for name in ('xmltodict', 'defusedxml', 'csv'):\n"
             "    try:\n"
             "        __import__(name); print(name, 'imported')\n"
             "    except ImportError as e:\n"
             "        print(type(e).__name__, '-', e)\n")
PINS_CODE = ("import importlib.metadata as m, xmltodict\n"
             "small = ('<?xml version=\"1.0\"?><!DOCTYPE d [<!ENTITY a \"lol\"><!ENTITY b \"&a;&a;&a;&a;&a;&a;&a;&a;&a;&a;\">]><d>&b;</d>')\n"
             "ents = ''.join('<!ENTITY l%d \"%s\">' % (i, ('&l%d;' % (i - 1)) * 10) for i in range(1, 10))\n"
             "laughs = '<!DOCTYPE d [<!ENTITY l0 \"lol\">' + ents + ']><d>&l9;</d>'\n"
             "print('xmltodict', m.version('xmltodict'))\n"
             "for name, doc in (('small entity', small), ('billion laughs', laughs)):\n"
             "    try:\n"
             "        print(name, 'parsed', xmltodict.parse(doc))\n"
             "    except Exception as e:\n"
             "        print(name, type(e).__name__, e)\n")

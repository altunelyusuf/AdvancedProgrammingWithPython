#!/usr/bin/env python3
"""SEN0414 chapter 18 (CSV, JSON, and XML Files, 3rd edition) - the shared base of the corpus, version 1.0.0.

Holds the chapter's whole programs as text, the single source the deck and the page's Lab tab both read, in the shape of
sen0414_ch17_corpus_base_v1_0_0.py. Each program is a complete script that exits 0 and prints what it printed on 2026-10-12 under
Python 3.14.6 (uv) with xmltodict 1.0.4 and defusedxml 0.7.1 (the environment /home/claude/venv314_ch18_latest; csv, json and
xml.etree.ElementTree are the standard library, the other two are not, so the file is run with that interpreter). All twelve programs
write their own small files in a temporary folder and need no network, so none is marked LIVE (the record that reads the book's
page and the files it ships is sen0414_ch18_thirdparty_v1_0_0.py). The chapter's code is kept as printed apart from the changes a
comment names: files are opened with encoding='utf-8' and newline='' because the chapter names no encoding (finding on the encoding),
and the Windows double spacing is emulated with an io.TextIOWrapper asked for the CRLF newline because no Windows machine was used.

Programs: CSVREADER, CSVWRITER, DICTRW, DIALECTENC, JSONBASICS, JSONFILES, ETREAD, ETWRITE, NSNIL, XMLSEC, XMLTODICT and the practice
program PROJ13 (Project 13, removing the header row of every CSV file, on generated files; the study's run on the shipped files is in
ch18-page/third_party_record).
"""
HEAD = r'''import io, os, re, sys, tempfile, csv, json
os.chdir(tempfile.mkdtemp())
EXAMPLE = 'Name,Age,City\r\nAlice,30,"San Francisco, CA"\r\nBob,25,"He said ""hi"""\r\nCarol,41,"two\r\nlines"\r\n'
def save(name, text, enc='utf-8'):
    with open(name, 'w', encoding=enc, newline='') as f: f.write(text)
'''
CSVREADER = HEAD + r'''# The reader of the chapter: list(), a for loop with line_num, and a reader that can be looped over once.
save('example.csv', EXAMPLE)
with open('example.csv', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    rows = list(reader)
    print(rows)
    print('a second list():', list(reader), '| every value is a string:', {type(v).__name__ for r in rows for v in r})
with open('example.csv', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print('Row #' + str(reader.line_num) + ' ' + str(row))
print('hasattr __len__, __getitem__:', hasattr(reader, '__len__'), hasattr(reader, '__getitem__'))
import tracemalloc
def peak(use_list):
    save('big.csv', ''.join('%d,name%d,%s\r\n' % (i, i, 'x' * 40) for i in range(60000)))
    with open('big.csv', encoding='utf-8', newline='') as f:
        tracemalloc.start(); r = csv.reader(f)
        if use_list: n = len(list(r))
        else: n = sum(1 for _ in r)
        p = tracemalloc.get_traced_memory()[1]; tracemalloc.stop(); return n, p
a, b = peak(True), peak(False)
print('rows', a[0], b[0], '| list() peak is more than 10 times the loop peak:', a[1] > 10 * b[1])
'''
CSVWRITER = HEAD + r'''# The writer of the chapter: writerow() returns the length written, the types it converts, and newline='' against the double spacing.
with open('output.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    print(w.writerow(['spam', 'eggs', 'bacon', 'ham']), w.writerow(['Hello, world!', 'eggs', 'bacon', 'ham']), w.writerow([1, 3.141592, None, '', True]))
print(open('output.csv', 'rb').read())
with open('tabs.tsv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['a', 'b c', 'd']); w.writerows([['x', 'y', 'z']])
print(open('tabs.tsv', 'rb').read())
# Windows translates \n to \r\n on write: emulated with a TextIOWrapper that is asked for that newline.
for label, nl in (('newline=""', ''), ('no newline argument on Windows', '\r\n')):
    buf = io.BytesIO(); t = io.TextIOWrapper(buf, encoding='utf-8', newline=nl)
    csv.writer(t).writerow(['a', 'b']); t.flush()
    print(label, buf.getvalue(), '| rows read back:', list(csv.reader(io.StringIO(buf.getvalue().decode(), newline=''))))
'''
DICTRW = HEAD + r'''# DictReader and DictWriter: the first row as keys, restkey and restval, and the error for an extra key.
save('example.csv', 'Name,Age\r\nAlice,30\r\nBob\r\nCarol,41,extra,more\r\n')
with open('example.csv', encoding='utf-8', newline='') as f:
    for row in csv.DictReader(f): print(dict(row))
with open('example.csv', encoding='utf-8', newline='') as f:
    print([dict(r) for r in csv.DictReader(f, restkey='rest', restval='?')])
with open('example.csv', encoding='utf-8', newline='') as f:
    print([dict(r) for r in csv.DictReader(f, fieldnames=['a', 'b', 'c'])][0])
with open('out.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, ['Name', 'Age'])
    print(w.writeheader(), w.writerow({'Name': 'Dave', 'Age': 5}), w.writerow({'Name': 'Eve'}))
    try: w.writerow({'Name': 'Frank', 'Age': 9, 'City': 'Rome'})
    except ValueError as e: print('ValueError:', e)
print(open('out.csv', 'rb').read())
'''
DIALECTENC = HEAD + r'''# Dialects, quoting constants, embedded line breaks and the encoding the chapter does not name.
print(sorted(csv.list_dialects()), [n for n in dir(csv) if n.startswith('QUOTE_')])
def line(row, **k):
    s = io.StringIO(newline=''); csv.writer(s, **k).writerow(row); return s.getvalue()
for q in ('QUOTE_MINIMAL', 'QUOTE_ALL', 'QUOTE_NONNUMERIC', 'QUOTE_NONE', 'QUOTE_STRINGS', 'QUOTE_NOTNULL'):
    try: print('%-17s' % q, repr(line(['a b', 'c,d', 7, None, ''], quoting=getattr(csv, q), **({'escapechar': '\\'} if q == 'QUOTE_NONE' else {}))))
    except Exception as e: print('%-17s' % q, type(e).__name__, e)
print(repr(line(['a', 'b\tc'], dialect='excel-tab')), list(csv.reader(['a\t"b c"\td'], dialect='excel-tab')))
print('embedded line break round trip:', list(csv.reader(io.StringIO(EXAMPLE, newline='')))[3])
text = 'Name,City\r\nZoe,İstanbul\r\n'
save('u.csv', text, 'utf-8-sig'); print('BOM first bytes', open('u.csv', 'rb').read()[:3], '| read as utf-8:', repr(open('u.csv', encoding='utf-8', newline='').readline()), '| as utf-8-sig:', repr(open('u.csv', encoding='utf-8-sig', newline='').readline()))
save('c.csv', 'Name,City\r\nZoe,Zürich\r\n', 'cp1252')
try: open('c.csv', encoding='utf-8').read()
except UnicodeDecodeError as e: print('UnicodeDecodeError:', e.reason)
print('read cp1252 bytes as latin-1 gives mojibake for utf-8 text:', open('u.csv', 'rb').read().decode('cp1252', errors='replace')[:12])
print('field_size_limit', csv.field_size_limit())
try: list(csv.reader(['x' * (csv.field_size_limit() + 1)]))
except csv.Error as e: print('csv.Error:', e)
'''
JSONBASICS = HEAD + r'''# JSON as the chapter teaches it, and the syntax it refuses.
js = '{"name": "Alice Doe", "age": 30, "car": null, "programmer": true, "phone": [{"type": "mobile", "number": "415-555-7890"}]}'
data = json.loads(js)
print(data, type(data).__name__, data['car'] is None, data['programmer'] is True)
print(json.dumps(data) == js)
print(json.dumps(data, indent=2))
for label, t in (('trailing comma', '["spam", "eggs",]'), ('single quotes', "{'a': 1}"), ('comment', '{"a": 1} // c'), ('raw newline', '"a\nb"'), ('None', '[None]'), ('NaN', '[NaN]'), ('empty', '')):
    try: print('%-15s' % label, 'accepted', json.loads(t))
    except json.JSONDecodeError as e: print('%-15s' % label, e.msg, '| line', e.lineno, 'column', e.colno)
'''
JSONFILES = HEAD + r'''# What JSON does to Python values, and a round trip through a file.
d = {'t': (1, 2), 1: 'a', 2.5: 'b', None: 'c', 'city': 'İstanbul', 'f': 1.0, 'big': 10**20}
s = json.dumps(d); print(s, '| back:', json.loads(s))
print(json.dumps(d, ensure_ascii=False))
for v in ({1, 2}, b'x', 1j, object(), {(1, 2): 3}):
    try: json.dumps(v)
    except TypeError as e: print(type(e).__name__, e)
print(json.dumps(float('nan')), json.loads('[Infinity]'))
with open('p.json', 'w', encoding='utf-8') as f: json.dump({'city': 'İstanbul', 'n': [1, None, True]}, f, indent=2, ensure_ascii=False)
print(open('p.json', 'rb').read())
print(json.load(open('p.json', encoding='utf-8')), json.load(open('p.json', 'rb')))
print(json.loads(b'\xef\xbb\xbf[1]'))
try: json.loads('﻿[1]')
except json.JSONDecodeError as e: print('str with a BOM:', e.msg)
try: json.loads('1' * 5000)
except ValueError as e: print('long integer:', str(e)[:60])
'''
ETREAD = HEAD + r'''# ElementTree reading: the root, children, text, iteration order, find and a subset of XPath.
import xml.etree.ElementTree as ET
XML = '<person>\n  <name>Alice Doe</name>\n  <age>30</age>\n  <car/>\n  <address><street>100 Larkin St.</street><city>San Francisco</city></address>\n  <phone type="mobile">415-555-7890</phone>\n  <phone type="work">415-555-1234</phone>\n</person>'
root = ET.fromstring(XML)
print(root.tag, [c.tag for c in root], root[0].text, repr(root[2].text), repr(root.text))
print([e.tag for e in root.iter()])
print(root.find('name').text, root.find('address/city').text, [p.attrib['type'] for p in root.findall('phone')], root.find('phone[@type="work"]').text, root.find('nothing'))
print([e.text for e in root.findall('.//street')], root.get('x'), root.find('phone').get('type'))
print('age is a', type(root.find('age').text).__name__, '| converted:', int(root.find('age').text) + 1)
import warnings
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always'); bool(root); print('truth value of an element:', [x.category.__name__ for x in w])
tree = ET.ElementTree(root); print(tree.getroot() is root)
try: ET.fromstring('<a><b></a>')
except ET.ParseError as e: print('ParseError:', e)
try: ET.fromstring('<a/><b/>')
except ET.ParseError as e: print('two roots:', e)
'''
ETWRITE = HEAD + r'''# ElementTree writing: SubElement, set, tostring and its space before the slash, indent and writing a file.
import xml.etree.ElementTree as ET
p = ET.Element('person'); ET.SubElement(p, 'name').text = 'Alice Doe'
c = ET.SubElement(p, 'car'); c.set('xsi:nil', 'true')
ET.SubElement(p, 'note').text = 'a < b & "c"'
print(ET.tostring(p, encoding='unicode'))
print(ET.tostring(p), ET.tostring(p, encoding='utf-8'))
ET.indent(p); print(ET.tostring(p, encoding='unicode'))
ET.ElementTree(p).write('p.xml', encoding='utf-8', xml_declaration=True)
print(open('p.xml', 'rb').read())
try: ET.fromstring(ET.tostring(p, encoding='unicode'))
except ET.ParseError as e: print('the output uses xsi: without declaring it, so parsing it again fails:', e)
'''
NSNIL = HEAD + r'''# Namespaces and xsi:nil: ElementTree does not interpret the attribute.
import xml.etree.ElementTree as ET
X = '<person xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><car xsi:nil="true"/><boat xsi:nil="true">full</boat></person>'
r = ET.fromstring(X)
print(r[0].attrib, repr(r[0].text), r[1].attrib, repr(r[1].text))
N = '<a:root xmlns:a="http://example.org/a"><a:item>1</a:item><item>2</item></a:root>'
n = ET.fromstring(N); print(n.tag, [c.tag for c in n], n.find('{http://example.org/a}item').text, n.find('item').text, n.find('a:item', {'a': 'http://example.org/a'}).text)
'''
XMLSEC = HEAD + r'''# XML from someone else: entity expansion, external entities, and defusedxml. The bomb is small (a few thousand expansions).
import xml.etree.ElementTree as ET, defusedxml.ElementTree as DET, defusedxml
small = '<?xml version="1.0"?><!DOCTYPE d [<!ENTITY a "lol"><!ENTITY b "&a;&a;&a;&a;&a;&a;&a;&a;&a;&a;"><!ENTITY c "&b;&b;&b;&b;&b;&b;&b;&b;&b;&b;">]><d>&c;</d>'
print('ElementTree expands the entities:', len(ET.fromstring(small).text), 'characters')
try: DET.fromstring(small)
except defusedxml.EntitiesForbidden as e: print('defusedxml:', type(e).__name__, isinstance(e, ValueError))
print(DET.fromstring('<a>ok</a>').text)
ext = '<?xml version="1.0"?><!DOCTYPE d [<!ENTITY x SYSTEM "file:///etc/hostname">]><d>&x;</d>'
try: print('external entity with ElementTree:', repr(ET.fromstring(ext).text))
except ET.ParseError as e: print('external entity with ElementTree: not fetched,', e)
try: DET.fromstring('<!DOCTYPE d []><d/>', forbid_dtd=True)
except defusedxml.DTDForbidden as e: print('DTDForbidden')
import xmltodict
try: print(xmltodict.parse(small))
except Exception as e: print('xmltodict:', type(e).__name__, str(e)[:70])
'''
XMLTODICT = HEAD + r'''# xmltodict: strings, one entry against many, attributes with @, and unparse.
import xmltodict
X = '<person><name>Alice Doe</name><age>30</age><phone type="mobile">415</phone></person>'
d = xmltodict.parse(X); print(d, type(d['person']['age']).__name__)
print(xmltodict.parse('<a><b>1</b></a>'), xmltodict.parse('<a><b>1</b><b>2</b></a>'), xmltodict.parse('<a><b>1</b></a>', force_list=('b',)))
print(xmltodict.unparse(d, pretty=True))
print(xmltodict.parse(xmltodict.unparse(d)) == d, xmltodict.parse('<a><b/></a>'))
'''
PROJ13 = HEAD + r'''# Project 13 as the chapter describes it, on generated files: remove the header row of every CSV file in the working directory.
from pathlib import Path
Path('headerRemoved').mkdir(exist_ok=True)
for i in range(3): save('f%d.csv' % i, 'h1,h2\r\n' + ''.join('%d,%d\r\n' % (i, j) for j in range(3)))
save('empty.csv', ''); save('headeronly.csv', 'h1,h2\r\n')
for csv_filename in sorted(Path('.').glob('*.csv')):
    print('Removing header from ' + csv_filename.name + '...')
    with open(csv_filename, encoding='utf-8', newline='') as f_in:
        reader = csv.reader(f_in); next(reader, None)
        with open(Path('headerRemoved') / csv_filename.name, 'w', encoding='utf-8', newline='') as f_out:
            csv.writer(f_out).writerows(reader)
print(sorted(p.name for p in Path('headerRemoved').iterdir()))
print(open('headerRemoved/f1.csv', 'rb').read(), open('headerRemoved/empty.csv', 'rb').read(), open('headerRemoved/headeronly.csv', 'rb').read())
'''
PROGRAMS = {
    'csvReader_v1_0_0.py': (CSVREADER, (), False),
    'csvWriter_v1_0_0.py': (CSVWRITER, (), False),
    'dictReaderWriter_v1_0_0.py': (DICTRW, (), False),
    'dialectsAndEncoding_v1_0_0.py': (DIALECTENC, (), False),
    'jsonBasics_v1_0_0.py': (JSONBASICS, (), False),
    'jsonTypesAndFiles_v1_0_0.py': (JSONFILES, (), False),
    'elementTreeReading_v1_0_0.py': (ETREAD, (), False),
    'elementTreeWriting_v1_0_0.py': (ETWRITE, (), False),
    'namespacesAndNil_v1_0_0.py': (NSNIL, (), False),
    'xmlSecurity_v1_0_0.py': (XMLSEC, (), False),
    'xmltodictRoundTrip_v1_0_0.py': (XMLTODICT, (), False),
    'practiceRemoveCsvHeader_v1_0_0.py': (PROJ13, (), False),
}
FIXTURE_BASED = []

if __name__ == "__main__":
    # Usage: /home/claude/venv314_ch18_latest/bin/python sen0414_ch18_corpus_base_v1_0_0.py   (exits 1 if a program does not exit 0)
    import os, subprocess, sys
    bad = 0
    for name, (code, needs, live) in PROGRAMS.items():
        r = subprocess.run([sys.executable, "-W", "ignore", "-c", code], capture_output=True, text=True, timeout=300)
        bad += r.returncode != 0
        print("=== %s (exit %d)%s" % (name, r.returncode, " LIVE" if live else "")); print(r.stdout.rstrip()[:1600]); print(r.stderr[-300:].rstrip())
    print("%d programs, %d did not exit 0" % (len(PROGRAMS), bad)); sys.exit(1 if bad else 0)

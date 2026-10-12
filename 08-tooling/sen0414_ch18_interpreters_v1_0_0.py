#!/usr/bin/env python3
"""Chapter 18: runs one program, the chapter's csv, json and xml.etree.ElementTree operations in a row together with a replay of the chapter's 97
interactive statements, under every installed 3.14 patch release (3.14.0 to 3.14.6, `uv python install 3.14.N`) and, for comparison, under 3.15 (a beta, 3.15.0b4, the newest uv offers), 3.13,
3.12 and 3.11, and records what each printed. It answers the question chapters 13 to 17 answered with a difference: does anything the chapter
teaches change between the patch releases of Python 3.14, and between 3.14 and the releases before it? The only package is xmltodict 1.0.4 (put in
place for each interpreter by `uv run --with`); csv, json and xml.etree.ElementTree are the standard library of each interpreter, so a difference
comes from the interpreter. The program needs the chapter page and the files the replay uses (fetched and checked by the helper code of
sen0414_ch18_thirdparty_v1_0_0.py, kept in the system temp directory or in CH18_CACHE). python runs in isolated mode, each interpreter by
`uv run --no-project`.
Usage: sen0414_ch18_interpreters_v1_0_0.py   (needs uv on PATH)   -> ch18-page/interpreter_record_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "08-tooling", "ch18-page", "interpreter_record_v1_0_0.json")
SRC = open(os.path.join(HERE, "sen0414_ch18_thirdparty_v1_0_0.py"), encoding="utf-8").read()
GET = re.search(r"GET = r'''(.*?)'''\n", SRC, re.S).group(1)
REPLAY = re.search(r"REPLAY = r'''(.*?)'''\n", SRC, re.S).group(1)
PROG = GET + REPLAY + r'''
import logging, hashlib, io, csv, json, importlib.metadata as md, xml.etree.ElementTree as ET, pyexpat, locale
import xmltodict
res = {}
def w(f):
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter('always')
        try: v = f()
        except Exception as e: v = type(e).__name__ + ': ' + str(e)[:90]
    return [v, sorted({x.category.__name__ for x in seen})]
res['series'] = sys.version.split()[0].rsplit('.', 1)[0] + '.x'
res['xmltodict'] = md.version('xmltodict')
res['expat'] = pyexpat.EXPAT_VERSION
res['default encoding'] = [locale.getencoding(), sys.flags.utf8_mode]
# the replay of the 97 statements, both repaired variants
def cap(**k):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): replay(**k)
    return buf.getvalue()
o1 = cap(repair=True, label='x: '); o2 = cap(skip=(25,), repair=True, label='x: ')
res['replay, in the order of the page'] = o1.split('\n')[0].split(': ', 1)[1]
res['replay, without the parse() block'] = o2.split('\n')[0].split(': ', 1)[1]
res['replay, blocks that differ in the order of the page'] = sorted(set(re.findall(r'^block (\d+) differs', o1, re.M)))
os.chdir(tempfile.mkdtemp())
# csv
def csvbat():
    out = {}
    out['quote constants'] = sorted(n for n in dir(csv) if n.startswith('QUOTE_'))
    def line(row, **k):
        s = io.StringIO(newline=''); csv.writer(s, **k).writerow(row); return s.getvalue()
    out['writerow'] = line(['Hello, world!', 'eggs', 1, 3.141592, None, '', True])
    out['reader'] = list(csv.reader(['a,"b,c",d', '', ' e ,f']))
    out['field_size_limit'] = csv.field_size_limit()
    out['DictWriter header'] = [csv.DictWriter(io.StringIO(), ['a']).writeheader(), type(next(csv.DictReader(['a,b', '1,2']))).__name__]
    try: list(csv.reader(['x,y\rz\n']))
    except csv.Error as e: out['bare CR error'] = str(e)
    try: csv.writer(io.StringIO(), quotechar='')
    except Exception as e: out['empty quotechar'] = type(e).__name__ + ': ' + str(e)
    try: line(['a,b'], quoting=csv.QUOTE_NONE)
    except csv.Error as e: out['QUOTE_NONE error'] = str(e)
    out['escapechar round trip'] = list(csv.reader([line(['a\\b', 'c,d'], escapechar='\\', quoting=csv.QUOTE_NONE).strip()], escapechar='\\'))
    out['tsv'] = line(['a', 'b c', 'd\te'], dialect='excel-tab')
    return out
res['csv'] = w(csvbat)
# json
def jsonbat():
    out = {}
    data = {'name': 'Alice Doe', 'age': 30, 'car': None, 'programmer': True}
    out['dumps'] = json.dumps(data); out['dumps indent=2'] = json.dumps(data, indent=2)
    for k, t in (('trailing comma array', '["spam", "eggs",]'), ('trailing comma object', '{"a": 1,}'), ('single quotes', "{'a': 1}"), ('comment', '{"a": 1} // c'), ('empty', ''), ('control char', '"a\nb"')):
        try: json.loads(t); out[k] = 'accepted'
        except json.JSONDecodeError as e: out[k] = e.msg
    try: json.loads('1' * 5000)
    except ValueError as e: out['5000 digits'] = str(e)[:60]
    try: json.dumps({'a': [1, {2}]})
    except TypeError as e: out['dumps error notes'] = [str(e), getattr(e, '__notes__', None)]
    out['NaN'] = json.dumps(float('nan')); out['key coercion'] = json.dumps({1: 'a', 2.5: 'b', None: 'c'})
    out['bytes with BOM'] = json.loads(b'\xef\xbb\xbf[1]')
    out['json.__version__'] = json.__version__
    r = subprocess.run([sys.executable, '-m', 'json', '-'], input='{"a":1}', capture_output=True, text=True); out['python -m json'] = [r.returncode, re.sub(r'/\S+', '<path>', r.stderr.strip().splitlines()[-1]) if r.returncode else r.stdout.strip().replace('\n', ' ')]
    return out
res['json'] = w(jsonbat)
# xml.etree
def xmlbat():
    out = {}
    C = '<person><name>Alice Doe</name><car xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/><address><street>100 Larkin St.</street></address></person>'
    r = ET.fromstring(C)
    out['tostring'] = ET.tostring(r, encoding='unicode'); out['car attrib'] = r[1].attrib; out['texts'] = [r[1].text, r[2].text]
    p = ET.Element('p'); ET.SubElement(p, 'c').set('xsi:nil', 'true'); out['tostring utf-8'] = ET.tostring(p, encoding='utf-8')
    out['truth'] = w(lambda: [bool(ET.Element('x')), bool(r)])
    out['indent'] = hasattr(ET, 'indent'); out['XMLPullParser.flush'] = hasattr(ET.XMLPullParser, 'flush'); out['iterparse close (3.13)'] = hasattr(ET.iterparse(io.BytesIO(b'<a/>')), 'close')
    out['getchildren'] = hasattr(r, 'getchildren')
    try: ET.fromstring('<a><b></a>')
    except ET.ParseError as e: out['ParseError'] = str(e)
    try: ET.fromstring('<a/><b/>')
    except ET.ParseError as e: out['two roots'] = str(e)
    laughs = '<?xml version="1.0"?><!DOCTYPE lolz [<!ENTITY lol "lol">' + ''.join('<!ENTITY lol%d "%s">' % (i, ('&lol;' if i == 1 else '&lol%d;' % (i - 1)) * 10) for i in range(1, 10)) + ']><lolz>&lol9;</lolz>'
    import resource; resource.setrlimit(resource.RLIMIT_AS, (3 * 2**30, 3 * 2**30))
    try: ET.fromstring(laughs); out['billion laughs'] = 'parsed'
    except BaseException as e: out['billion laughs'] = type(e).__name__ + ': ' + str(e)[:80]
    out['xmltodict'] = xmltodict.parse(C)
    try: import xml.etree.cElementTree; out['cElementTree'] = 'imports'
    except ImportError as e: out['cElementTree'] = 'ImportError'
    import tomllib; out['tomllib'] = tomllib.loads('a = 1')
    return out
res['xml'] = w(xmlbat)
# open() default encoding warning
r = subprocess.run([sys.executable, '-X', 'warn_default_encoding', '-c', "open('/etc/hostname').close()"], capture_output=True, text=True)
res['EncodingWarning from open() with -X warn_default_encoding'] = 'EncodingWarning' in r.stderr
print(json.dumps(res, sort_keys=True, default=repr))
'''
INTERPRETERS = ["3.11", "3.12", "3.13", "3.14.0", "3.14.1", "3.14.2", "3.14.3", "3.14.4", "3.14.5", "3.14.6", "3.15"]
def run(py):
    env = dict(os.environ); env.pop("PYTHONPATH", None); env.setdefault("CH18_CACHE", os.environ.get("CH18_CACHE", ""))
    if not env["CH18_CACHE"]: env.pop("CH18_CACHE")
    r = subprocess.run(["uv", "run", "--no-project", "--python", py, "--with", "xmltodict==1.0.4", "python", "-I", "-c", PROG], capture_output=True, text=True, env=env, timeout=900)
    if r.returncode != 0: return {"error": (r.stderr.strip().splitlines() or ["?"])[-1]}
    return json.loads(r.stdout.strip().splitlines()[-1])
if __name__ == "__main__":
    results = {}
    for py in INTERPRETERS:
        v = subprocess.run(["uv", "run", "--no-project", "--python", py, "python", "-c", "import sys; print(sys.version.split()[0])"], capture_output=True, text=True).stdout.strip()
        results[v or py] = run(py); print(py, v, "ok" if "error" not in results[v or py] else results[v or py]["error"])
    def flat(r):
        out = {}
        for k, v in r.items():
            if k in ("csv", "json", "xml") and isinstance(v, list) and isinstance(v[0], dict):
                for kk, vv in v[0].items(): out["%s: %s" % (k, kk)] = vv
                out["%s: warnings raised while it ran" % k] = v[1]
            elif k != "series": out[k] = v
        return out
    fl = {v: flat(r) for v, r in results.items()}
    keys = sorted({k for r in fl.values() for k in r})
    differ = {}
    for k in keys:
        vals = {}
        for v, r in fl.items(): vals.setdefault(json.dumps(r.get(k), sort_keys=True), []).append(v)
        if len(vals) > 1: differ[k] = [[json.loads(a), b] for a, b in vals.items()]
    json.dump({"_version": "1.0.0", "observed": datetime.date.today().isoformat(), "_note": "Recorded by sen0414_ch18_interpreters_v1_0_0.py: one program (the chapter's csv, json and xml.etree.ElementTree operations and a replay of its 97 statements) under each interpreter, xmltodict 1.0.4 in each. 'differ' lists the items whose value is not the same under every interpreter, each value with the interpreters that gave it; the items not listed were identical everywhere.",
               "program_after_the_helper_code": PROG.split("import logging, hashlib", 1)[1], "interpreters": list(results), "results": results, "items compared": len(keys), "differ": differ}, open(OUT, "w"), indent=1, ensure_ascii=False)
    print("recorded", len(results), "interpreters; items that differ:", sorted(differ))

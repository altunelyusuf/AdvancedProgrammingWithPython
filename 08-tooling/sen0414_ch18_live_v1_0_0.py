#!/usr/bin/env python3
"""Chapter 18 (CSV, JSON, and XML Files): observes, once, what the public sources the chapter names answer today, and writes what it saw with the
date. A web site changes and the files of the online materials may be replaced; the record is an observation of the day, not something
the build can re-check, and no check reads it.
What it does: fetches the chapter page and compares its SHA-256 with the digest the book's own ontology records; counts what is on the page
(listings, figures with the HTTP status of each image, tables, practice questions) and asks every external link of the chapter once without
following a redirect; downloads the online materials of the 3rd edition and checks the files chapter 18 uses against the SHA-256 the research
recorded, and lists what the zip does not hold (no example3.csv, no my_data.xml, no JSON or XML file at all); reads the newest releases and upload
dates of the packages on PyPI (xmltodict, openpyxl, defusedxml, lxml, simplejson); reads Appendix A for the versions the book pins and Appendix B for
the answers to the chapter's questions; opens the pages that give the stories their dates (Wikipedia, the Python 2.5 and 2.6 'What's New' pages,
the W3C first edition of XML 1.0); asks python.org which release is the newest and uv which 3.14 and 3.15 releases it can install; and opens every
source of the research record and checks that the passages the research relies on are on the page. Nothing is posted anywhere and every URL is
asked once. In place of the brute-force attack that chapter 17's version of this script timed, this one has no long-running step: it runs in
about two minutes. NOT EXECUTED: Microsoft Excel (the numbers of Figure 18-1 and of the Excel formats come from LibreOffice 24.2), the language
model clean-up of the chapter, a Windows computer (the effect of text mode on line endings was reproduced by asking io.TextIOWrapper for the
translation Windows does).
Run it with an interpreter that has requests and Beautiful Soup.
Usage: sen0414_ch18_live_v1_0_0.py   -> ch18-page/live_observations_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, hashlib, io, json, os, re, subprocess, sys, tempfile, zipfile
import requests, bs4
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "08-tooling", "ch18-page", "live_observations_v1_0_0.json")
UA = {"User-Agent": "SEN0414-research/1.0 (teaching; altunel.yusuf@gmail.com)"}
BROWSER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0"}
obs = []
def see(what, f):
    try: v = f()
    except Exception as e: v = "raised %s: %s" % (type(e).__name__, str(e)[:200])
    obs.append({"what": what, "saw": v})
import time
def get(u, **k):
    k.setdefault("headers", BROWSER)
    for attempt in range(6):       # a site that answers 429 (too many requests) or drops the connection is asked again after a pause; the status of the last answer is the one recorded
        try:
            r = requests.get(u, timeout=90, **k)
            if r.status_code != 429: return r
        except requests.ConnectionError:
            if attempt == 5: raise
        time.sleep(20)
    return r
def sha(b): return hashlib.sha256(b).hexdigest()
def norm(t): return re.sub(r"\s+", " ", t)
def visible(r):
    s = bs4.BeautifulSoup(r.text, "html.parser")
    for x in s(["script", "style"]): x.decompose()
    return norm(s.get_text(" "))
WORK = tempfile.mkdtemp()

# every source of the research record: id, URL, the passages the research relies on
SOURCES = [
    ('P01', 'https://automatetheboringstuff.com/3e/chapter18.html', ['Versatile Plaintext Formats', 'removeCsvHeader.py', 'Excel-to-CSV Converter', 'xmltodict', 'which we covered in Chapter 18']),
    ('P02', 'https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip', []),
    ('P03', 'https://automatetheboringstuff.com/3e/', ['CSV, JSON, and XML Files']),
    ('P04', 'https://nostarch.com/automate-boring-stuff-python-3rd-edition', ['Automate the Boring Stuff with Python']),
    ('P05', 'https://automatetheboringstuff.com/3e/appendixa.html', ['xmltodict==0.13.0', 'openpyxl==3.1.5']),
    ('P06', 'https://automatetheboringstuff.com/3e/appendixb.html', ['File objects need to be opened in read-binary', 'XML’s format resembles HTML']),
    ('P07', 'https://docs.python.org/3.14/library/csv.html', ["newline=''", 'excel-tab', 'QUOTE_STRINGS', 'field_size_limit', 'The number of lines read from the source iterator']),
    ('P08', 'https://docs.python.org/3.14/library/json.html', ['Infinity', 'ensure_ascii', 'specified by RFC 7159', 'byte order mark', 'python -m json']),
    ('P09', 'https://docs.python.org/3.14/library/xml.etree.elementtree.html', ['XML security', 'Testing the truth value of an Element emits DeprecationWarning', 'limited support for XPath', 'register_namespace', 'iterparse']),
    ('P10', 'https://docs.python.org/3.14/library/xml.html', ['Expat versions lower than 2.7.2', 'billion laughs', 'decompression bomb']),
    ('P11', 'https://docs.python.org/3.14/library/xml.dom.minidom.html', ['toprettyxml']),
    ('P12', 'https://docs.python.org/3.14/library/xml.sax.html', ['SAX']),
    ('P13', 'https://docs.python.org/3.14/library/pyexpat.html', ['SetBillionLaughsAttackProtectionActivationThreshold']),
    ('P14', 'https://docs.python.org/3.14/library/tomllib.html', ['readable and binary file object']),
    ('P15', 'https://docs.python.org/3.14/library/io.html', ['UTF-8 Mode', 'Opt-in EncodingWarning', 'universal newlines']),
    ('P16', 'https://docs.python.org/3.14/library/functions.html', ['if encoding is not specified the encoding used is platform-dependent']),
    ('P17', 'https://docs.python.org/3.14/whatsnew/3.14.html', ['Add exception notes for JSON serialization errors', 'python -m json']),
    ('P18', 'https://docs.python.org/3/whatsnew/3.13.html', ['Add the close() method for the iterator returned by iterparse()']),
    ('P19', 'https://docs.python.org/3/whatsnew/3.12.html', ['csv.QUOTE_NOTNULL and csv.QUOTE_STRINGS', 'Testing the truth value']),
    ('P20', 'https://docs.python.org/3/whatsnew/3.11.html', ['universal newline', 'tomllib']),
    ('P21', 'https://docs.python.org/3/whatsnew/3.9.html', ['The encoding parameter of json.loads() has been removed']),
    ('P22', 'https://docs.python.org/3.14/library/locale.html', ['getencoding']),
    ('P23', 'https://docs.python.org/3.14/library/tracemalloc.html', ['peak']),
    ('P24', 'https://docs.python.org/3.14/library/codecs.html', ['utf-8-sig']),
    ('P25', 'https://docs.python.org/3.14/library/dbm.html', ['dbm.sqlite3', 'shelve']),
    ('P26', 'https://peps.python.org/pep-0686/', ['Python will enable UTF-8 mode by default from Python 3.15']),
    ('P27', 'https://peps.python.org/pep-0305/', ['CSV File API', 'Final']),
    ('P28', 'https://www.rfc-editor.org/rfc/rfc4180', ['CRLF', 'The last record in the file may or may not have an ending line break', 'October 2005', 'text/csv']),
    ('P29', 'https://www.rfc-editor.org/rfc/rfc8259', ['STD 90', 'December 2017', 'MUST NOT add a byte order mark', 'Infinity and NaN']),
    ('P30', 'https://www.rfc-editor.org/rfc/rfc4627', ['July 2006', 'Crockford']),
    ('P31', 'https://www.rfc-editor.org/rfc/rfc7159', ['March 2014', 'Obsoletes: 4627']),
    ('P32', 'https://www.rfc-editor.org/rfc/rfc3629', ['UTF-8']),
    ('P33', 'https://ecma-international.org/publications-and-standards/standards/ecma-404/', ['2nd edition, December 2017']),
    ('P34', 'https://www.json.org/json-en.html', ['ECMA-404']),
    ('P35', 'https://www.w3.org/TR/xml/', ['Fifth Edition', '26 November 2008', 'well-formed']),
    ('P36', 'https://www.w3.org/TR/1998/REC-xml-19980210', ['10-February-1998', 'Extensible Markup Language']),
    ('P37', 'https://www.w3.org/TR/xml-names/', ['Third Edition', '8 December 2009', 'QName']),
    ('P38', 'https://www.w3.org/TR/xmlschema-1/', ['xsi:nil', 'nillable']),
    ('P39', 'https://www.iana.org/assignments/media-types/text/csv', ['text/csv', '4180', 'Shafranovich']),
    ('P40', 'https://pypi.org/pypi/xmltodict/json', ['Makes working with XML feel like you are working with JSON']),
    ('P41', 'https://openpyxl.readthedocs.io/en/stable/', ['Excel 2010 xlsx/xlsm']),
    ('P42', 'https://pypi.org/pypi/openpyxl/json', ['openpyxl']),
    ('P43', 'https://pypi.org/pypi/defusedxml/json', ['defusing XML bombs']),
    ('P44', 'https://pypi.org/pypi/lxml/json', ['lxml']),
    ('P45', 'https://pypi.org/pypi/simplejson/json', ['simplejson']),
    ('P46', 'https://en.wikipedia.org/wiki/Comma-separated_values', ['IBM Fortran (level H extended) compiler under OS/360', 'list-directed']),
    ('P47', 'https://en.wikipedia.org/wiki/JSON', ['first JSON message in April 2001', 'ISO/IEC 21778:2017']),
    ('P48', 'https://en.wikipedia.org/wiki/XML', ['Jon Bosak', 'February 10, 1998']),
    ('P49', 'https://en.wikipedia.org/wiki/Billion_laughs_attack', ['exponential entity expansion', 'lol9']),
    ('P50', 'https://en.wikipedia.org/wiki/Douglas_Crockford', ['JSLint', 'popularized the JSON data format']),
    ('P51', 'https://www.loc.gov/preservation/digital/formats/fdd/fdd000323.shtml', ['RFC 4180']),
    ('P52', 'https://www.loc.gov/preservation/digital/formats/fdd/fdd000381.shtml', ['RFC 4627 and ECMA-404']),
    ('P53', 'https://www.loc.gov/preservation/digital/formats/fdd/fdd000075.shtml', ['W3C']),
    ('P54', 'https://cwe.mitre.org/data/definitions/776.html', ['XML Entity Expansion']),
    ('P55', 'https://cwe.mitre.org/data/definitions/611.html', ['Improper Restriction of XML External Entity Reference']),
    ('P56', 'https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing', ['XML External Entity']),
    ('P57', 'https://docs.python.org/3/whatsnew/2.6.html', ['json (originally called simplejson) was written by Bob Ippolito', 'released on October 1, 2008']),
    ('P58', 'https://docs.python.org/3/whatsnew/2.5.html', ['ElementTree library for processing XML has been added to the standard library as xml.etree', 'Python 2.5 was released on September 19, 2006']),
    ('P59', 'https://help.libreoffice.org/latest/en-US/text/shared/guide/csv_params.html', ['Field delimiter', 'Text delimiter']),
    ('P60', 'https://docs.astral.sh/uv/', ['extremely fast Python package and project manager']),
    ('P61', 'https://docs.astral.sh/uv/concepts/python-versions/', ['Python versions', 'uv python install']),
    ('P62', 'https://www.python.org/downloads/', ['Python 3.15.0', 'Python 3.14.8']),
    ('P63', 'https://www.python.org/downloads/release/python-3140/', ['Python 3.14.0 has been superseded by']),
    ('P64', 'https://docs.python.org/3.15/whatsnew/3.15.html', ['Python now uses UTF-8 as the default encoding', 'array_hook']),
]
def sources():
    out = []
    for pid, url, phrases in SOURCES:
        try:
            r = get(url, headers=BROWSER if "nostarch.com" in url else UA); ctype = r.headers.get("content-type", "")
            if "zip" in ctype or url.endswith(".zip"): t = ""
            else:
                if "html" in ctype or "text/plain" in ctype:
                    try: t = r.content.decode("utf-8")
                    except UnicodeDecodeError: t = r.text
                else: t = r.text
                if "html" in ctype:
                    s = bs4.BeautifulSoup(t, "html.parser")
                    for x in s(["script", "style"]): x.decompose()
                    t = s.get_text(" ")
            t = norm(t).replace("\u2019", "'")
            out.append([pid, r.status_code, len(r.content), {p: (norm(p).replace("\u2019", "'").lower() in t.lower()) for p in phrases}])
        except Exception as e: out.append([pid, "unreachable: %s" % type(e).__name__, 0, {}])
    return out

# 0. the chapter and the book's own record of it
ch = get("https://automatetheboringstuff.com/3e/chapter18.html", headers=UA)
DIGEST = "c998127be7342ac419f9f884a60aea6ef837e3dba1c2deada1e977a6a20a01dc"
ONTO = "/home/claude/Ontologies/automate-python-book-3e/01-ontologies/automate_python_3e_ch18_v1_0_0.ttl"
see("chapter 18 page: status, bytes, SHA-256, equal to the chapterDigest of the book ontology (read from its file when present)", lambda: [ch.status_code, len(ch.content), sha(ch.content), sha(ch.content) == DIGEST, (DIGEST in open(ONTO).read()) if os.path.exists(ONTO) else "ontology file not present"])
soup = bs4.BeautifulSoup(ch.text, "html.parser"); text = norm(soup.get_text(" "))
see("chapter 18 page: number of listings (pre elements), figure captions, tables, images and the HTTP status of each image file", lambda: [len(soup.find_all("pre")), sorted(set(re.findall(r"Figure 18-\d+", text))), len(soup.find_all("table")), [(i["src"], get("https://automatetheboringstuff.com/3e/" + i["src"]).status_code) for i in soup.find_all("img") if i.get("src")]])
see("chapter 18 page: alt text of the pictures (an empty alt on the figure of the chapter is a finding for readers who cannot see it)", lambda: [i.get("alt") for i in soup.find_all("img")])
see("chapter 18 page: the headings of the chapter in order", lambda: [(h.name, norm(h.get_text())) for h in soup.find_all(["h2", "h3", "h4", "h5"])])
STATEMENTS = ("which we covered in Chapter 18", "rows of data that share the same columns", "Download the ZIP file excelSpreadsheets.zip", "open('output.csv', 'w', newline='')", "any self-closing tags", "is not valid",
              "can store all Python data types in binary shelf files", "skips the less popular but still useful YAML and TOML formats", "You can loop over the reader object only once", "XPath can locate", "example_file = open('example3.csv')")
see("chapter 18 page: statements the research relies on (each is on the page of the book: True)", lambda: {s: (norm(s) in text) for s in STATEMENTS})
see("chapter 18 page: words the chapter never uses although the modules need them (False means absent from the page)", lambda: {s: s.lower() in text.lower() for s in ("encoding='utf-8'", "json.load(", "json.dump(", "defusedxml", "QUOTE_", "Sniffer", "iterparse", "lxml", "BOM", "untrusted", "well-formed", "security", "EncodingWarning", "utf-8-sig")})
ext = sorted({a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("http") and "automatetheboringstuff.com" not in a["href"]})
def link_status():
    out = []
    for u in ext:
        try:
            r = requests.get(u, timeout=60, headers=BROWSER, allow_redirects=False); out.append([u, r.status_code, r.headers.get("Location", "")[:100]])
        except Exception as e: out.append([u, "unreachable: %s" % type(e).__name__, ""])
    return out
see("chapter 18 page: every external link of the chapter, asked once without following a redirect: URL, HTTP status, Location", link_status)
see("chapter 18 page: every URL that appears in the text of the chapter", lambda: sorted({u.rstrip(".,)") for u in re.findall(r"https?://[\w./?=&#%~:+-]+", text) if "automatetheboringstuff.com/3e/chapter18" not in u}))
def appendix():
    a = get("https://automatetheboringstuff.com/3e/appendixa.html", headers=UA); t = visible(a)
    return [a.status_code, re.findall(r"(?:xmltodict|openpyxl|defusedxml|lxml)\s*[=~<>]+\s*[\w.]+", t), "xmltodict==0.13.0" in t, "openpyxl==3.1.5" in t]
see("Appendix A of the book: status, the pins of the packages chapter 18 uses, whether the two pins the study replayed are on the page", appendix)
def appendixb():
    a = get("https://automatetheboringstuff.com/3e/appendixb.html", headers=UA); t = visible(a)
    i = t.find("Chapter 18 1."); j = t.find("Chapter 19", i)
    return [a.status_code, t[i:j][:1500]]
see("Appendix B of the book: the answers printed for the eleven questions of chapter 18", appendixb)

# 1. the online materials
mat = get("https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip")
see("online materials of the 3rd edition: status, bytes, SHA-256 of the zip", lambda: [mat.status_code, len(mat.content), sha(mat.content)])
RECORDED = {'exampleWithHeader3.csv': '4d238719835ede046f0bb0cbf8806c572a04925f35ee29633127e93792728b7f', 'example3.xlsx': 'b1dc19bd6286554124dff48ef3bb5c5f547afd0168f01943e384ba2400eeebfa',
       'removeCsvHeader.py': 'ac28848d5450c3ecb962243a62444fa25e456ebb39834fb23dcdacd27e34a180', 'removeCsvHeader.zip': '484771efbcd87f89566f7e55928635f14594674622056200017c4cef712e6d3e',
       'excelSpreadsheets.zip': '828f30a2d42d2616e5c67d97f1d9832d5b93609e2a0cddee6cda0530d326abef', 'produceSales3.xlsx': 'bdf2349a380c70f76ecf5ab0a793c5a3f35144c16dca14816af252d94e07b17e',
       'demo.docx': 'b43b21137d7d69b16e9e1ec7ebb75e0e2f053d8947cd2ddcf79d60a0dfe5f121',
       'censuspopdata.xlsx': 'f5e649370d4ed3878240ee7ead2a0c9ddd8a41da839b905f8fc17c3e664ba439'}

def materials():
    z = zipfile.ZipFile(io.BytesIO(mat.content)); names = [n for n in z.namelist() if not n.endswith("/") and "/._" not in n and not n.split("/")[-1].startswith("._")]
    got = {n.split("/")[-1]: sha(z.read(n)) for n in names if n.split("/")[-1] in RECORDED}
    base = [n.split("/")[-1] for n in names]
    return {"files": len(names), "each recorded file is there with the recorded SHA-256": {k: got.get(k) == v for k, v in RECORDED.items()},
            "files chapter 18 names or needs that the zip does not hold": {n: (n in base) for n in ("example3.csv", "my_data.xml", "output.csv", "example3.xlsx", "exampleWithHeader3.csv", "removeCsvHeader.zip", "excelSpreadsheets.zip")},
            "any .json or .xml file in the zip": [n for n in names if re.search(r"\.(json|xml)$", n, re.I)]}
see("online materials: the files (without the macOS resource forks), whether the files chapter 18 uses match the SHA-256 recorded by the study, and which files the chapter needs that the zip does not hold", materials)
def inner_zips():
    z = zipfile.ZipFile(io.BytesIO(mat.content)); P = "Automate_the_Boring_Stuff_3e_onlinematerials/"; out = {}
    for n in ("excelSpreadsheets.zip", "removeCsvHeader.zip"):
        zz = zipfile.ZipFile(io.BytesIO(z.read(P + n))); m = [x for x in zz.namelist() if not x.endswith("/") and "__MACOSX" not in x]
        out[n] = {"members": len(m), "extensions": sorted({os.path.splitext(x)[1].lower() for x in m}), "first": m[0], "last": m[-1]}
    return out
see("online materials: what the two zips inside it hold (the Practice Program tells the reader to test an Excel converter on excelSpreadsheets.zip)", inner_zips)

# 2. the packages on PyPI
def pypi():
    out = {}
    for n in ("xmltodict", "openpyxl", "defusedxml", "lxml", "simplejson", "et-xmlfile"):
        j = requests.get("https://pypi.org/pypi/%s/json" % n, headers=UA, timeout=60).json(); v = j["info"]["version"]
        out[n] = [v, (j["releases"][v][0]["upload_time"] if j["releases"].get(v) else None), j["info"].get("requires_python"), len(j["releases"])]
    return out
see("PyPI: newest release of each package the study uses or names: version, upload time, Requires-Python, number of releases", pypi)
def pinned():
    out = {}
    for n, v in (("xmltodict", "0.13.0"), ("xmltodict", "1.0.0"), ("openpyxl", "3.1.5")):
        j = requests.get("https://pypi.org/pypi/%s/%s/json" % (n, v), headers=UA, timeout=60).json()
        out["%s %s" % (n, v)] = [j["urls"][0]["upload_time"] if j["urls"] else None, j["info"].get("requires_python")]
    return out
see("PyPI: the upload time and Requires-Python of the releases the book pins (xmltodict 0.13.0, openpyxl 3.1.5) and of xmltodict 1.0.0", pinned)
def first_releases():
    out = {}
    for n in ("xmltodict", "openpyxl", "defusedxml", "simplejson"):
        j = requests.get("https://pypi.org/pypi/%s/json" % n, headers=UA, timeout=60).json()
        t = sorted((f[0]["upload_time"], v) for v, f in j["releases"].items() if f)
        out[n] = [t[0], t[-1]]
    return out
see("PyPI: the first and the last upload of xmltodict, openpyxl, defusedxml and simplejson (time, version)", first_releases)

# 3. the dates that the stories rest on
def wp(u, needles, w=140):
    t = visible(get(u, headers=UA)); r = {}
    for n in needles:
        i = t.find(n); r[n] = t[max(0, i - w): i + len(n) + w] if i >= 0 else None
    return r
see("Wikipedia, Comma-separated values: the IBM Fortran sentence of 1972 and the sentence on RFC 4180", lambda: wp("https://en.wikipedia.org/wiki/Comma-separated_values", ["IBM Fortran (level H extended) compiler under OS/360", "RFC 4180"]))
see("Wikipedia, JSON: Crockford and the first JSON message", lambda: wp("https://en.wikipedia.org/wiki/JSON", ["sent the first JSON message in April 2001"]))
see("Wikipedia, XML: the first publication and Jon Bosak", lambda: wp("https://en.wikipedia.org/wiki/XML", ["First published February 10, 1998", "Jon Bosak developed a charter"]))
see("Wikipedia, Billion laughs attack: the sentence on the name and the entry for CVE-2003-1564", lambda: wp("https://en.wikipedia.org/wiki/Billion_laughs_attack", ["It is also referred to as an XML bomb", "CVE-2003-1564"]))
see("Python 2.5 What's New: the ElementTree sentence; Python 2.6 What's New: the json sentence", lambda: [wp("https://docs.python.org/3/whatsnew/2.5.html", ["has been added to the standard library as xml.etree"]), wp("https://docs.python.org/3/whatsnew/2.6.html", ["written by Bob Ippolito"])])
see("W3C, XML 1.0 first edition: the date on the Recommendation", lambda: wp("https://www.w3.org/TR/1998/REC-xml-19980210", ["W3C Recommendation 10-February-1998"]))
see("RFC 4180 and RFC 8259: the dates and the rules the research quotes", lambda: [wp("https://www.rfc-editor.org/rfc/rfc4180", ["The last record in the file may or may not have an ending line break"]), wp("https://www.rfc-editor.org/rfc/rfc8259", ["MUST NOT add a byte order mark", "Infinity and NaN"])])

# 4. Python and the tools
py = get("https://docs.python.org/3.14/library/csv.html", headers=UA)
see("Python documentation of csv: the release the page describes", lambda: re.search(r"(3\.\d+\.\d+) documentation", visible(py), re.I).group(1))
pyd = get("https://www.python.org/downloads/", headers=UA)
see("python.org downloads page: the newest release it offers and the list of releases with their dates", lambda: [re.findall(r"Download Python (3\.\d+\.\d+)", visible(pyd))[:2], re.findall(r"Python (3\.1[345]\.\d+) ([A-Z][a-z]+\.? \d+, \d{4})", visible(pyd))[:8]])
see("python.org: the page of Python 3.14.0 and what it says of newer releases", lambda: re.findall(r"Python 3\.14\.0 has been superseded by Python (3\.\d+\.\d+)", visible(get("https://www.python.org/downloads/release/python-3140/", headers=UA))))
def uvlist():
    r = subprocess.run(["uv", "python", "list", "--all-versions"], capture_output=True, text=True)
    return sorted({m for m in re.findall(r"cpython-(3\.1[45]\.\d+[a-z0-9]*)-linux-x86_64-gnu", r.stdout)}, key=lambda s: [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", s)])
see("uv (python list --all-versions): the 3.14 and 3.15 releases of CPython for this machine that uv knew on the day", uvlist)
def soffice():
    r = subprocess.run(["soffice", "--version"], capture_output=True, text=True); return r.stdout.strip()
see("LibreOffice installed on the build machine (stood in for Excel in Figure 18-1)", soffice)
see("Python 3.15 'What's New': the sentences on UTF-8 as the default encoding and on __version__ of csv and json", lambda: wp("https://docs.python.org/3.15/whatsnew/3.15.html", ["Python now uses UTF-8 as the default encoding", "The __version__ , version and VERSION attributes have been deprecated"], 200))

see("every source of the research record opened: id, HTTP status, bytes, and whether each passage the research relies on is on the page", sources)
json.dump({"_version": "1.0.0", "observed": datetime.date.today().isoformat(), "with": "requests %s, beautifulsoup4 %s, Python %s" % (requests.__version__, bs4.__version__, sys.version.split()[0]),
           "_note": "Single requests made on the day named, through the build machine's proxy, to the public pages and files the chapter names. Microsoft Excel and Word were not used. A record of one observation; web sites change and nothing re-checks it.",
           "items": obs}, open(OUT, "w"), indent=1, ensure_ascii=False)
print("observed", len(obs), "things on", datetime.date.today())

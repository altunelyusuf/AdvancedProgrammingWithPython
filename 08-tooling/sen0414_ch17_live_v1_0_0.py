#!/usr/bin/env python3
"""Chapter 17 (PDF and Word Documents): observes, once, what the public sources the chapter names answer today, and writes what it saw with the
date. A web site changes and the files of the online materials may be replaced; the record is an observation of the day, not something
the build can re-check, and no check reads it.
What it does: starts, in two child processes, the brute-force attack of the chapter's third practice program in its worst case (the
book's own dictionary.txt, 349,900 words, both cases of every word, 699,800 attempts, against a password that is not in the dictionary)
on a PDF written by pypdf with RC4 (the default) and with AES-256, and times them; fetches the chapter page and compares its SHA-256 with
the digest the book's own ontology records; counts what is on the page (listings, figures with the HTTP status of each image, tables)
and asks every external link of the chapter once without following a redirect; downloads the online materials of the 3rd edition and
checks the files chapter 17 uses against the SHA-256 the research recorded; reads the newest releases and upload dates of the packages on
PyPI; reads Appendix A for the versions the book pins; opens the pages that give the stories their dates (Wikipedia, the pypdf history
page); and opens every source of the research record and checks that the passages the research relies on are on the page. Nothing is
posted anywhere and every URL is asked once. NOT EXECUTED: Microsoft Word, a PDF viewer, the language model clean-up of the chapter.
Run it with an interpreter that has requests and Beautiful Soup, with pdftotext (poppler) installed and the environment of the study
at /home/claude/venv314_ch17_latest (pypdf, Pillow and cryptography); it takes about 45 minutes, nearly all of it the attack.
Usage: sen0414_ch17_live_v1_0_0.py   -> ch17-page/live_observations_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, hashlib, io, json, os, re, subprocess, sys, tempfile, zipfile
import requests, bs4
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "08-tooling", "ch17-page", "live_observations_v1_0_0.json")
LATEST = os.environ.get("CH17_LATEST_PY", "/home/claude/venv314_ch17_latest/bin/python")
UA = {"User-Agent": "SEN0414-research/1.0 (teaching; altunel.yusuf@gmail.com)"}
BROWSER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0"}
obs = []
def see(what, f):
    try: v = f()
    except Exception as e: v = "raised %s: %s" % (type(e).__name__, str(e)[:200])
    obs.append({"what": what, "saw": v})
def get(u, **k):
    k.setdefault("headers", BROWSER)
    return requests.get(u, timeout=90, **k)
def sha(b): return hashlib.sha256(b).hexdigest()
def norm(t): return re.sub(r"\s+", " ", t)
def visible(r):
    s = bs4.BeautifulSoup(r.text, "html.parser")
    for x in s(["script", "style"]): x.decompose()
    return norm(s.get_text(" "))
WORK = tempfile.mkdtemp()

# 6. every source of the research record
SOURCES = [
    ('P01', 'https://automatetheboringstuff.com/3e/chapter17.html', ['Post-Processing with AI', 'PDF Paranoia', 'Custom Invitations', 'PDF Password Breaker', 'merge_page()']),
    ('P02', 'https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip', []),
    ('P03', 'https://automatetheboringstuff.com/3e/', ['PDF and Word Documents']),
    ('P04', 'https://nostarch.com/automate-boring-stuff-python-3rd-edition', ['Automate the Boring Stuff with Python']),
    ('P05', 'https://automatetheboringstuff.com/3e/appendixa.html', ['PyPDF==5.0.1', 'python-docx==1.1.2']),
    ('P06', 'https://pypdf.readthedocs.io/en/stable/', ['pypdf']),
    ('P07', 'https://pypdf.readthedocs.io/en/stable/user/extract-text.html', ['extraction_mode']),
    ('P08', 'https://pypdf.readthedocs.io/en/latest/user/post-processing-in-text-extraction.html', ['outside the scope of pypdf', 'Dehyphenation']),
    ('P09', 'https://pypdf.readthedocs.io/en/stable/user/extract-images.html', ['images']),
    ('P10', 'https://pypdf.readthedocs.io/en/stable/user/merging-pdfs.html', ['PdfWriter', 'append']),
    ('P11', 'https://pypdf.readthedocs.io/en/stable/user/encryption-decryption.html', ['AES-256']),
    ('P12', 'https://pypdf.readthedocs.io/en/stable/user/add-watermark.html', ['watermark', 'merge_page']),
    ('P13', 'https://pypdf.readthedocs.io/en/stable/user/installation.html', ['If you plan to use image extraction, you need Pillow', 'Encryption using RC4 is supported using the regular installation']),
    ('P14', 'https://pypdf.readthedocs.io/en/stable/modules/PdfWriter.html', ['insert_blank_page', 'merge']),
    ('P15', 'https://pypdf.readthedocs.io/en/stable/modules/PageObject.html', ['rotate', 'merge_page']),
    ('P16', 'https://pypdf.readthedocs.io/en/stable/meta/CHANGELOG.html', ['PdfMerger', '5.0.0']),
    ('P17', 'https://pypdf.readthedocs.io/en/stable/meta/history.html', ['In 2005, Mathieu Fenniak launched pyPdf', 'At the end of 2011']),
    ('P18', 'https://pypdf.readthedocs.io/en/stable/user/security.html', ['security']),
    ('P19', 'https://python-docx.readthedocs.io/en/latest/user/quickstart.html', ['add_paragraph', 'add_heading']),
    ('P20', 'https://python-docx.readthedocs.io/en/latest/user/text.html', ['Run', 'paragraph']),
    ('P21', 'https://python-docx.readthedocs.io/en/latest/user/styles-understanding.html', ['style_id', 'stable, unique identifier']),
    ('P22', 'https://python-docx.readthedocs.io/en/latest/user/styles-using.html', ['style', 'Quote']),
    ('P23', 'https://python-docx.readthedocs.io/en/latest/api/document.html', ['add_heading', 'add_picture']),
    ('P24', 'https://python-docx.readthedocs.io/en/latest/api/text.html', ['visible-text portion of any hyperlinks', 'corresponding to the <w:r> elements', 'converted to the appropriate XML form for a tab']),
    ('P25', 'https://python-docx.readthedocs.io/en/latest/user/install.html', ['lxml']),
    ('P26', 'https://python-docx.readthedocs.io/en/latest/', ['python-docx']),
    ('P27', 'https://pdfminersix.readthedocs.io/en/latest/', ['pdfminer']),
    ('P28', 'https://pypi.org/pypi/pypdf/json', ['pypdf']),
    ('P29', 'https://pypi.org/pypi/docx/json', ['Steve Canny']),
    ('P30', 'https://pypi.org/pypi/python-docx/json', ['python-docx']),
    ('P31', 'https://pypi.org/pypi/pdfminer.six/json', ['pdfminer']),
    ('P32', 'https://pypi.org/pypi/pdfplumber/json', ['pdfplumber']),
    ('P33', 'https://pypi.org/pypi/reportlab/json', ['reportlab']),
    ('P34', 'https://docs.python.org/3.14/library/zipfile.html', ['ZipFile']),
    ('P35', 'https://docs.python.org/3.14/library/os.html', ['os.walk', 'listdir']),
    ('P36', 'https://docs.python.org/3.14/howto/sorting.html', ['key']),
    ('P37', 'https://docs.python.org/3.14/library/io.html', ['BytesIO']),
    ('P38', 'https://www.loc.gov/preservation/digital/formats/fdd/fdd000277.shtml', ['Version 1.7 was published as ISO 32000-1 in July 2008']),
    ('P39', 'https://www.loc.gov/preservation/digital/formats/fdd/fdd000397.shtml', ['Office Open XML']),
    ('P40', 'https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/PDF32000_2008.pdf', ['cross-reference table', 'trailer']),
    ('P41', 'https://qpdf.readthedocs.io/en/stable/cli.html', ['show-encryption']),
    ('P42', 'https://www.libreoffice.org', ['LibreOffice']),
    ('P43', 'https://cwe.mitre.org/data/definitions/214.html', ['Invocation of Process Using Visible Sensitive Information']),
    ('P44', 'https://en.wikipedia.org/wiki/Redaction', ['the original text remains in the file']),
    ('P45', 'https://en.wikipedia.org/wiki/John_Warnock', ['In the spring of 1991, Warnock outlined a system called']),
    ('P46', 'https://en.wikipedia.org/wiki/Zip_(file_format)', ['Phil Katz', '14 February 1989']),
    ('P47', 'https://en.wikipedia.org/wiki/Office_Open_XML', ['7 December 2006', 'ISO/IEC 29500:2008']),
    ('P48', 'https://en.wikipedia.org/wiki/Adobe_Acrobat', ['June 15, 1993']),
    ('P49', 'https://learn.microsoft.com/en-us/office/open-xml/open-xml-sdk', ['Open XML']),
    ('P50', 'https://docs.astral.sh/uv/', ['uv']),
    ('P51', 'https://www.python.org/downloads/', ['Download Python']),
    ('P52', 'https://www.libreoffice.org/discover/writer/', ['Writer']),
]
def sources():
    out = []
    for pid, url, phrases in SOURCES:
        try:
            r = requests.get(url, timeout=120, headers=BROWSER if "nostarch.com" in url else UA); t = r.text
            ctype = r.headers.get("content-type", "")
            if "pdf" in ctype or url.endswith(".pdf"):
                p = os.path.join(WORK, pid + ".pdf"); open(p, "wb").write(r.content)
                t = subprocess.run(["pdftotext", "-l", "60", p, "-"], capture_output=True, text=True).stdout
            elif "zip" in ctype or url.endswith(".zip"):
                t = ""
            elif "json" in ctype:
                pass
            elif "html" in ctype:
                s = bs4.BeautifulSoup(t, "html.parser")
                for x in s(["script", "style"]): x.decompose()
                t = s.get_text(" ")
            t = norm(t); out.append([pid, r.status_code, len(r.content), {p: (p.lower() in t.lower()) for p in phrases}])
        except Exception as e: out.append([pid, "unreachable: %s" % type(e).__name__, 0, {}])
    return out

if "--sources-only" in sys.argv:
    # a second pass over the sources only, written into the existing record in place of the first pass (the attack is not run again)
    prev = json.load(open(OUT)); prev["items"] = [o for o in prev["items"] if not o["what"].startswith("every source of the research record opened")]
    prev["items"].append({"what": "every source of the research record opened (second pass, after the phrases were refined): id, HTTP status, bytes, and whether each passage the research relies on is on the page", "saw": sources()})
    prev["_sources_second_pass"] = datetime.date.today().isoformat() + ": the sources were opened again with the refined phrases; every other item is from the first pass"
    json.dump(prev, open(OUT, "w"), indent=1, ensure_ascii=False); print("sources re-read"); sys.exit(0)

# 0. the materials first, because the attack needs the dictionary and the chapter PDF
mat = get("https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip")
ZIPPATH = os.path.join(WORK, "materials.zip"); open(ZIPPATH, "wb").write(mat.content)
BRUTE = r'''
import sys, io, time, json, zipfile, pypdf
zpath, algo = sys.argv[1], sys.argv[2]
z = zipfile.ZipFile(zpath); P = "Automate_the_Boring_Stuff_3e_onlinematerials/"
pdf = z.read(P + "Recursion_Chapter1.pdf"); words = [w for w in z.read(P + "dictionary.txt").decode().split("\n") if w]
w = pypdf.PdfWriter(); w.append(io.BytesIO(pdf), (0, 2))
if algo == "RC4": w.encrypt("swordfish")
else: w.encrypt("swordfish", algorithm=algo)
b = io.BytesIO(); w.write(b)
r = pypdf.PdfReader(io.BytesIO(b.getvalue())); t = time.perf_counter(); n = 0; found = None
for word in words:
    for guess in (word, word.upper()):
        n += 1
        if r.decrypt(guess).name != "NOT_DECRYPTED": found = guess
    if found: break
print(json.dumps({"algorithm": algo, "words": len(words), "attempts": n, "found": found, "seconds": round(time.perf_counter() - t, 1), "pypdf": pypdf.__version__}))
'''
attacks = {a: subprocess.Popen([LATEST, "-c", BRUTE, ZIPPATH, a], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for a in ("RC4", "AES-256")}

# 1. the chapter and the book's own record of it
ch = get("https://automatetheboringstuff.com/3e/chapter17.html", headers=UA)
DIGEST = "00cb1643dca3afd3b75bfd9ce7ad594f3dd80f8606de1cffe40b8583846b4789"
ONTO = "/home/claude/Ontologies/automate-python-book-3e/01-ontologies/automate_python_3e_ch17_v1_0_0.ttl"
see("chapter 17 page: status, bytes, SHA-256, equal to the chapterDigest of the book ontology (read from its file when present)", lambda: [ch.status_code, len(ch.content), sha(ch.content), sha(ch.content) == DIGEST, (DIGEST in open(ONTO).read()) if os.path.exists(ONTO) else "ontology file not present"])
soup = bs4.BeautifulSoup(ch.text, "html.parser"); text = norm(soup.get_text(" "))
see("chapter 17 page: number of listings (pre elements), figure captions, tables, images and the HTTP status of each image file", lambda: [len(soup.find_all("pre")), sorted(set(re.findall(r"Figure 17-\d+", text)), key=lambda s: int(s.split("-")[1])), len(soup.find_all("table")), [(i["src"], get("https://automatetheboringstuff.com/3e/" + i["src"]).status_code) for i in soup.find_all("img") if i.get("src")]])
see("chapter 17 page: alt text of the pictures", lambda: [i.get("alt") for i in soup.find_all("img")])
see("chapter 17 page: the headings of the chapter in order", lambda: [(h.name, norm(h.get_text())) for h in soup.find_all(["h3", "h4"])])
STATEMENTS = ("Install the package by following the instructions in Appendix A", "The second argument to this method is the tuple (0, 5)", "writer.merge(2, 'Recursion_Chapter1.pdf', (0, 5))",
              "The size of the new page will be the same as that of the preceding page", "'AES-256' argument implements a recommended modern encryption algorithm", "pdf_files.append(filename)",
              "Be sure to install Python-Docx, not Docx", "an integer ranging from 0 to 4", "'List Number '", "'MacroText'", "You should try both the upperc", "over 44,000", "88,000", "Table 17-1")
see("chapter 17 page: statements the research relies on (each is on the page of the book: True)", lambda: {s: (norm(s) in text or norm(s) in norm(ch.text)) for s in STATEMENTS})
see("chapter 17 page: words the chapter never uses although the libraries need them (False means absent from the page)", lambda: {s: s.lower() in text.lower() for s in ("Pillow", "cryptography", "pip install", "insert_blank_page(2", "DependencyError", "FileNotDecryptedError", "extraction_mode", "layout")})
ext = sorted({a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("http") and "automatetheboringstuff.com" not in a["href"]})
def link_status():
    out = []
    for u in ext:
        try:
            r = requests.get(u, timeout=60, headers=BROWSER, allow_redirects=False); out.append([u, r.status_code, r.headers.get("Location", "")[:100]])
        except Exception as e: out.append([u, "unreachable: %s" % type(e).__name__, ""])
    return out
see("chapter 17 page: every external link of the chapter, asked once without following a redirect: URL, HTTP status, Location", link_status)
plain = [m for m in re.findall(r"https?://[\w./?=&#%~:+-]+", text)]
see("chapter 17 page: every URL that appears in the text of the chapter", lambda: sorted({u.rstrip(".,)") for u in plain if "automatetheboringstuff.com/3e/chapter17" not in u}))
def appendix():
    a = get("https://automatetheboringstuff.com/3e/appendixa.html", headers=UA); t = visible(a)
    return [a.status_code, re.findall(r"(?:PyPDF|pypdf|python-docx|Python-Docx|pdfminer\.six|Pillow|cryptography)[=~<>]*[\w.]*", t)[:20], "PyPDF==5.0.1" in t, "python-docx==1.1.2" in t]
see("Appendix A of the book: status, the package names and pins it prints, whether the two pins the study replayed are on the page", appendix)

# 2. the online materials
see("online materials of the 3rd edition: status, bytes, SHA-256 of the zip", lambda: [mat.status_code, len(mat.content), sha(mat.content)])
RECORDED = {"Recursion_Chapter1.pdf": "d943896e0bd2241d5d8d819b43c197225c5e87c23a4b852c4819e74261bbad29", "watermark.pdf": "535a8584c4476491d9b7c1b3b987c269f86f0cd51f937dba0a46cfad31937d74", "demo.docx": "b43b21137d7d69b16e9e1ec7ebb75e0e2f053d8947cd2ddcf79d60a0dfe5f121", "zophie.png": "5c5bf02fd0c95cee5d490a6daf3f1c4ccbbcab9fdc59bd8bba9564cad1462ba1", "dictionary.txt": "dc4042ec00f36acbb1c2c514c86db9d48348a1cfa8ec1bf105c08910bc094d3f", "guests.txt": "e6136e39f829ae7380be4969b780c72bd8022a1a97efc399f0f2002ce1fd5164", "extractpdftext.py": "84a3fb70fc362c555f5c4239b4b445c2aa727e3d04b8820771d3333513a3670a", "extractpdfimages.py": "1a5893ea05e9627167871522c92318cdd7b268efcab4a3c2516b542729c0cef0", "combine_pdfs.py": "07dcdf353f0bc2f3f251ae2da3076cba62c46a98a2ac3234193f9d0f494bb1f7", "readDocx.py": "544a900d6bcbf3a4312dd4c8f3f6c54792553dccc0a13370ce10b8be8ed05172"}
def materials():
    z = zipfile.ZipFile(io.BytesIO(mat.content)); names = [n for n in z.namelist() if not n.endswith("/") and "/._" not in n and not n.split("/")[-1].startswith("._")]
    got = {n.split("/")[-1]: sha(z.read(n)) for n in names if n.split("/")[-1] in RECORDED}
    return {"files": len(names), "each recorded file is there with the recorded SHA-256": {k: got.get(k) == v for k, v in RECORDED.items()}, "no encrypted.pdf, helloworld.docx or restyled.docx in the zip": not any(re.search(r"encrypted\.pdf|helloworld\.docx|restyled\.docx", n) for n in names), "entries naming pdf, docx or word": [n for n in names if re.search(r"pdf|docx|word", n, re.I)][:30]}
see("online materials: the files (without the macOS resource forks), whether the files chapter 17 uses match the SHA-256 recorded by the study", materials)
def shipped_facts():
    z = zipfile.ZipFile(io.BytesIO(mat.content)); P = "Automate_the_Boring_Stuff_3e_onlinematerials/"
    p = os.path.join(WORK, "rc.pdf"); open(p, "wb").write(z.read(P + "Recursion_Chapter1.pdf"))
    info = subprocess.run(["pdfinfo", p], capture_output=True, text=True).stdout
    return {"pdfinfo": [l for l in info.splitlines() if l.split(":")[0] in ("Pages", "Encrypted", "Page size", "PDF version", "Producer", "Creator")], "dictionary.txt lines": z.read(P + "dictionary.txt").count(b"\n"), "guests.txt": z.read(P + "guests.txt").decode()}
see("online materials: what pdfinfo says of Recursion_Chapter1.pdf (poppler), the lines of dictionary.txt and the text of guests.txt", shipped_facts)

# 3. the packages on PyPI
def pypi():
    out = {}
    for n in ("pypdf", "PyPDF2", "python-docx", "docx", "pdfminer.six", "pillow", "cryptography", "pdfplumber", "reportlab", "lxml"):
        j = requests.get("https://pypi.org/pypi/%s/json" % n, headers=UA, timeout=60).json(); v = j["info"]["version"]
        out[n] = [v, (j["releases"][v][0]["upload_time"] if j["releases"].get(v) else None), j["info"].get("requires_python"), len(j["releases"])]
    return out
see("PyPI: newest release of each package the study uses or names: version, upload time, Requires-Python, number of releases", pypi)
def first_releases():
    out = {}
    for n in ("pypdf", "PyPDF2", "python-docx", "docx"):
        j = requests.get("https://pypi.org/pypi/%s/json" % n, headers=UA, timeout=60).json()
        t = sorted((f[0]["upload_time"], v) for v, f in j["releases"].items() if f)
        out[n] = [t[0], t[-1]]
    return out
see("PyPI: the first and the last upload of pypdf, PyPDF2, python-docx and docx (time, version)", first_releases)
def docx_meta():
    j = requests.get("https://pypi.org/pypi/docx/json", headers=UA, timeout=60).json()["info"]
    return [j["author"], j["summary"], j["version"], (j.get("home_page") or "")[:80], bool(j.get("description") and "python-docx" in j["description"])]
see("PyPI: the package docx that the chapter says not to install: author, summary, version, home page, whether its description mentions python-docx", docx_meta)

# 4. the dates that the stories rest on
def wp(u, needles, w=120):
    t = visible(get(u, headers=UA)); r = {}
    for n in needles:
        i = t.find(n); r[n] = t[max(0, i - w): i + len(n) + w] if i >= 0 else None
    return r
see("Wikipedia, John Warnock: the sentence on Camelot", lambda: wp("https://en.wikipedia.org/wiki/John_Warnock", ["In the spring of 1991, Warnock outlined a system called"]))
see("Wikipedia, ZIP: the first release and the inventors", lambda: wp("https://en.wikipedia.org/wiki/Zip_(file_format)", ["Initial release 14 February 1989", "designed by Phil Katz of PKWARE"]))
see("Wikipedia, Office Open XML: the first release, the ISO publication", lambda: wp("https://en.wikipedia.org/wiki/Office_Open_XML", ["Initial release 7 December 2006", "ISO/IEC 29500:2008) was published in November 2008"]))
see("pypdf history page: the origin in 2005 and the fork at the end of 2011", lambda: wp("https://pypdf.readthedocs.io/en/stable/meta/history.html", ["In 2005, Mathieu Fenniak launched pyPdf", "At the end of 2011"], 200))
see("Wikipedia, Redaction: the sentence on black rectangles over text in PDF", lambda: wp("https://en.wikipedia.org/wiki/Redaction", ["the original text remains in the file"], 200))

# 5. Python and the tools
py = get("https://docs.python.org/3.14/library/zipfile.html", headers=UA)
see("Python documentation of zipfile: the release the page describes", lambda: re.search(r"(3\.\d+\.\d+) Documentation", visible(py)).group(1))
pyd = get("https://www.python.org/downloads/", headers=UA)
see("python.org downloads page: the newest release it offers", lambda: re.findall(r"Download Python (3\.\d+\.\d+)", visible(pyd))[:3])
see("qpdf documentation: the option the study uses to read the encryption of a file", lambda: "show-encryption" in get("https://qpdf.readthedocs.io/en/stable/cli.html", headers=UA).text)
see("LibreOffice home page: the version it offers for download", lambda: re.findall(r"LibreOffice (\d+\.\d+\.\d+)", visible(get("https://www.libreoffice.org/download/download-libreoffice/", headers=UA)))[:3])

see("every source of the research record opened: id, HTTP status, bytes, and whether each passage the research relies on is on the page", sources)

# 7. the attack, last, because it takes the longest
def attack_result():
    res = []
    for a, p in attacks.items():
        so, se = p.communicate(); res.append(json.loads(so) if p.returncode == 0 else "raised: %s" % se.strip().splitlines()[-1])
    return res
see("the worst case of the PDF Password Breaker run to the end (book's dictionary.txt, both cases of every word, a password that is not in it) on a file written by pypdf: RC4 (the default of encrypt()) and AES-256, started together on a machine with two cores", attack_result)
json.dump({"_version": "1.0.0", "observed": datetime.date.today().isoformat(), "with": "requests %s, beautifulsoup4 %s, Python %s; the attack under %s" % (requests.__version__, bs4.__version__, sys.version.split()[0], LATEST),
           "_note": "Single requests made on the day named, through the build machine's proxy, to the public pages and files the chapter names. Microsoft Word and a PDF viewer were not used. A record of one observation; web sites change and nothing re-checks it. The attack timings are those of one machine with two cores running both attacks at once.",
           "items": obs}, open(OUT, "w"), indent=1, ensure_ascii=False)
print("observed", len(obs), "things on", datetime.date.today())

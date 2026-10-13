#!/usr/bin/env python3
"""Chapter 22 (Recognizing Text in Images): observes, once, what the public sources the chapter names answer today, what the files the book ships hold, what the package
index says about pytesseract, Pillow, OCRmyPDF, OpenCV and PyAutoGUI, and what real OCR software on the machine does, and writes what it saw with the date. A web site changes
and the files of the online materials may be replaced; the record is an observation of the day, not something the build can re-check, and no check reads it.
What it does: fetches the chapter page and compares its SHA-256 with the digest the book's own ontology records; counts what is on the page (listings, figures, practice
questions), asks every external link of the chapter once without following a redirect, and asks for each picture of the chapter; reads Appendix A for the versions the book
pins and Appendix B for the answers to the chapter's seven questions; downloads the online materials of the 3rd edition and looks for every file the chapter names; asks the
two autbor.com links of the chapter where they lead and what is on the pages; reads the newest releases of pytesseract, Pillow, OCRmyPDF, opencv-python-headless and PyAutoGUI
on PyPI; opens every source of the research record and checks that the passages the research relies on are on the page.
On the machine itself it asks each Tesseract (the apt 5.3.4 and the builds 5.5.3 and 4.1.1) for its version, library versions, page segmentation modes and parameters, and
runs a few small experiments (the inversion switch, pytesseract's batch and multi-output calls, the line in pytesseract 0.3.10 that fails under Python 3.14).
NOT EXECUTED and said so: Windows and macOS installers, Homebrew, a physical scanner, a large language model, a photograph from Wikimedia Commons.
Run it with an interpreter that has requests and Beautiful Soup (/home/claude/venv314_web/bin/python); the local part uses CH22_LATEST (/home/claude/venv314_ch22_latest/bin/python).
Usage: sen0414_ch22_live_v1_0_0.py   -> ch22-page/live_observations_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, hashlib, io, json, os, re, shutil, subprocess, sys, tempfile, time, zipfile
import requests, bs4
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "08-tooling", "ch22-page", "live_observations_v1_0_0.json")
UA = {"User-Agent": "SEN0414-research/1.0 (academic course; altunel.yusuf@gmail.com)"}
BROWSER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0"}
PYTHON = os.environ.get("CH22_LATEST", "/home/claude/venv314_ch22_latest/bin/python")
PINS = os.environ.get("CH22_PINS", "/home/claude/venv314_ch22_pins/bin/python")
HOME = "/home/claude"
obs = []
def see(what, f):
    try: v = f()
    except Exception as e: v = "raised %s: %s" % (type(e).__name__, str(e)[:200])
    obs.append({"what": what, "saw": v})
def get(u, **k):
    k.setdefault("headers", UA)
    for attempt in range(6):       # a site that answers 429 or drops the connection is asked again after a pause; the status of the last answer is the one recorded
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
SOURCES = [
    ('P01', 'https://automatetheboringstuff.com/3e/chapter22.html', ['PyTesseract', 'NAPS2', 'ocr-example.png', 'frankenstein.png', 'Iv', 'exact results may vary', 'tess.get_languages()', 'eng+jpn', 'ocrmypdf', 'Browser Text Scraper', 'preprocessingocr', 'embeddedfrankenstein', 'Python modules obscure these details']),
    ('P02', 'https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip', []),
    ('P03', 'https://automatetheboringstuff.com/3e/', ['Recognizing Text in Images']),
    ('P04', 'https://nostarch.com/automate-boring-stuff-python-3rd-edition', ['Recognizing Text in Images']),
    ('P05', 'https://automatetheboringstuff.com/3e/appendixa.html', ['pytesseract==0.3.10', 'pillow==10.4.0', 'openai-whisper']),
    ('P06', 'https://automatetheboringstuff.com/3e/appendixb.html', ['Tesseract recognizes English by default', "lang='eng+jpn'", 'NAPS2 can be run from a Python script']),
    ('P07', 'https://tesseract-ocr.github.io/tessdoc/', ['Tesseract']),
    ('P08', 'https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html', ['300 dpi', 'Otsu', 'Sauvola', 'deskew', 'tessedit_write_images', 'tessedit_char_whitelist', '--psm', 'pixRemoveAlpha', 'for 4.x version use dark text on light background', 'Missing borders']),
    ('P09', 'https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html', ['--oem 1', '--tessdata-dir', 'tesseract images/eurotext.png - -l eng']),
    ('P10', 'https://tesseract-ocr.github.io/tessdoc/Data-Files.html', ['tessdata_fast', 'tessdata_best', 'oem', 'Linux distributions', 'Integer models']),
    ('P11', 'https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html', ['jpn', 'aze_cyrl', 'tessdata_fast']),
    ('P12', 'https://tesseract-ocr.github.io/tessdoc/Installation.html', ['apt', 'brew', 'UB Mannheim', 'tesseract-ocr']),
    ('P13', 'https://tesseract-ocr.github.io/tessdoc/FAQ.html', ['handwriting recognition', 'searchable PDF', 'page separators', 'multiple images in a single run']),
    ('P14', 'https://raw.githubusercontent.com/tesseract-ocr/tesseract/main/doc/tesseract.1.asc', ['ISO 639-2', 'eng+deu+fra', '--psm', 'Sparse text', 'open-sourced by HP and UNLV in 2005', 'developed at Google until 2018', 'not implemented']),
    ('P15', 'https://raw.githubusercontent.com/tesseract-ocr/tesseract/main/README.md', ['Tesseract', 'LSTM', 'Leptonica', 'Apache']),
    ('P16', 'https://raw.githubusercontent.com/tesseract-ocr/tessdata_fast/main/README.md', ['fast', 'integer']),
    ('P17', 'https://raw.githubusercontent.com/tesseract-ocr/tessdata_best/main/README.md', ['best', 'LSTM']),
    ('P18', 'https://research.google/pubs/an-overview-of-the-tesseract-ocr-engine/', ['Tesseract']),
    ('P19', 'https://pypi.org/pypi/pytesseract/json', ['pytesseract', 'Pillow', 'Apache']),
    ('P20', 'https://raw.githubusercontent.com/madmaze/pytesseract/master/README.rst', ['image_to_string', 'get_languages', 'image_to_pdf_or_hocr', 'timeout', 'image_to_alto_xml', 'tesseract_cmd']),
    ('P21', 'https://raw.githubusercontent.com/madmaze/pytesseract/master/pytesseract/pytesseract.py', ['def image_to_string', 'def get_languages', 'TesseractNotFoundError', 'subprocess.Popen', 'tess_', 'discard and replace the alpha channel with white background']),
    ('P22', 'https://www.naps2.com/doc/command-line', ['--ocrlang', '--install', '--noprofile', 'naps2 console', 'flatpak run com.naps2.Naps2 console']),
    ('P23', 'https://www.naps2.com/download', ['Flatpak', '8.']),
    ('P24', 'https://ocrmypdf.readthedocs.io/en/latest/', ['searchable', 'OCRmyPDF']),
    ('P25', 'https://pypi.org/pypi/ocrmypdf/json', ['ocrmypdf']),
    ('P26', 'https://pypi.org/pypi/opencv-python-headless/json', ['opencv-python-headless']),
    ('P27', 'https://docs.python.org/3.14/library/subprocess.html', ['capture_output', 'returncode', 'check_output']),
    ('P28', 'https://docs.python.org/3.14/whatsnew/3.14.html', ['pkgutil', 'find_loader', 'Removed']),
    ('P29', 'https://en.wikipedia.org/wiki/Levenshtein_distance', ['Vladimir Levenshtein', '1965', 'edit distance']),
    ('P30', 'https://en.wikipedia.org/wiki/Word_error_rate', ['word error rate', 'Levenshtein']),
    ('P31', 'https://iso639-3.sil.org/code_tables/639/data', ['ISO 639 Code Tables', 'Set 1, 2, or 3']),
    ('P32', 'https://www.loc.gov/standards/iso639-2/php/code_list.php', ['jpn', 'Japanese']),
    ('P33', 'https://pyautogui.readthedocs.io/en/latest/screenshot.html', ['screenshot', 'Pillow', 'locateOnScreen', 'scrot']),
    ('P34', 'https://pypi.org/pypi/pyautogui/json', ['pyautogui']),
    ('P35', 'https://en.wikipedia.org/wiki/Optical_character_recognition', ['Kurzweil', 'Hyman Eli Goldberg', 'Optophone', 'January 13, 1976', 'omni-font', 'Statistical Machine']),
    ('P36', 'https://en.wikipedia.org/wiki/Tesseract_(software)', ['Hewlett-Packard', '1985', '2005', '2006', 'Mannheim', 'one of the most accurate open-source OCR engines']),
    ('P37', 'https://en.wikipedia.org/wiki/Emanuel_Goldberg', ['Statistical Machine', 'microfilm', 'Zeiss Ikon']),
    ('P38', 'https://en.wikipedia.org/wiki/Kurzweil_Computer_Products', ['Xerox', '1974', 'blind']),
    ('P39', 'https://en.wikipedia.org/wiki/ReCAPTCHA', ['September 2009', 'The New York Times', 'digitization of books']),
    ('P40', 'https://en.wikipedia.org/wiki/Frankenstein', ['1818', '1831', 'Mary Shelley', 'anonymously']),
    ('P41', 'https://autbor.com/preprocessingocr', ['placeholder', 'OpenCV', 'Tesseract']),
    ('P42', 'https://autbor.com/embeddedfrankenstein/', ['Frankenstein']),
    ('P43', 'https://en.wikipedia.org/wiki/Otsu%27s_method', ['Nobuyuki Otsu', 'threshold', '1979']),
    ('P44', 'https://pypi.org/pypi/pillow/json', ['pillow']),
    ('P45', 'https://pillow.readthedocs.io/en/stable/reference/Image.html', ['convert', 'resize', 'rotate', 'crop']),
    ('P46', 'https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html', ['dpi', 'PNG', 'TIFF', 'PDF']),
    ('P47', 'https://pillow.readthedocs.io/en/stable/releasenotes/12.0.0.html', ['3.14']),
    ('P48', 'https://pillow.readthedocs.io/en/stable/installation/python-support.html', ['3.14', '3.10']),
    ('P49', 'https://docs.astral.sh/uv/concepts/python-versions/', ['uv python install']),
    ('P50', 'https://www.python.org/downloads/', ['Python 3.14']),
    ('P51', 'https://pillow.readthedocs.io/en/stable/reference/ImageOps.html', ['expand', 'autocontrast', 'invert', 'grayscale']),
    ('P52', 'https://docs.python.org/3.14/library/difflib.html', ['SequenceMatcher', 'get_opcodes']),
    ('P53', 'https://en.wikipedia.org/wiki/Hewlett-Packard', ['Palo Alto']),
]
def sources():
    out = []
    for pid, url, phrases in SOURCES:
        try:
            r = get(url, headers=BROWSER if "nostarch.com" in url else UA); ctype = r.headers.get("content-type", "")
            if "zip" in ctype or url.endswith((".zip", ".pdf")): t = ""
            else:
                t = r.content.decode("utf-8", "replace")
                if "html" in ctype:
                    s = bs4.BeautifulSoup(t, "html.parser")
                    for x in s(["script", "style"]): x.decompose()
                    t = s.get_text(" ")
            t = norm(t).replace("’", "'")
            out.append([pid, r.status_code, len(r.content), {p: (norm(p).replace("’", "'").lower() in t.lower()) for p in phrases}])
        except Exception as e: out.append([pid, "unreachable: %s" % type(e).__name__, 0, {}])
    return out

# 0. the chapter and the book's own record of it
ch = get("https://automatetheboringstuff.com/3e/chapter22.html")
DIGEST = "4228da08b22649e4c3dd4b5aa9d6346bae3fd50f1ac9f9a8e5a31a80d0416232"
ONTO = "/home/claude/Ontologies/automate-python-book-3e/01-ontologies/automate_python_3e_ch22_v1_0_0.ttl"
see("chapter 22 page: status, bytes, SHA-256, equal to the chapterDigest of the book ontology (read from its file when present)", lambda: [ch.status_code, len(ch.content), sha(ch.content), sha(ch.content) == DIGEST, (DIGEST in open(ONTO).read()) if os.path.exists(ONTO) else "ontology file not present"])
soup = bs4.BeautifulSoup(ch.text, "html.parser"); text = norm(soup.get_text(" "))
IMGS = [i["src"] for i in soup.find_all("img") if i.get("src") and "cover" not in i["src"]]
def image_dims():
    d = tempfile.mkdtemp(); rows = []
    for k, src in enumerate(IMGS):
        r = get("https://automatetheboringstuff.com/3e/" + src); p = os.path.join(d, "i%d.img" % k); open(p, "wb").write(r.content); rows.append([src, r.status_code, len(r.content)])
    code = "import sys, json; from PIL import Image; print(json.dumps([list(Image.open(p).size) for p in sys.argv[1:]]))"
    sizes = json.loads(subprocess.run([PYTHON, "-c", code] + [os.path.join(d, "i%d.img" % k) for k in range(len(IMGS))], capture_output=True, text=True).stdout)
    shutil.rmtree(d); return [r + [s] for r, s in zip(rows, sizes)]
see("chapter 22 page: number of listings (pre elements), figure captions, tables, and the HTTP status, bytes and pixel size of each picture of the chapter (the pictures are asked for and measured, not kept)", lambda: [len(soup.find_all("pre")), sorted(set(re.findall(r"Figure 22-\d+", text))), sorted(set(re.findall(r"Table 22-\d+", text))), len(soup.find_all("table")), image_dims()])
see("chapter 22 page: the headings of the chapter in order", lambda: [(h.name, norm(h.get_text())) for h in soup.find_all(["h2", "h3", "h4", "h5"])])
STATEMENTS = ("more formally called optical character recognition (OCR)", "extract text from an image in four lines of code", "You cannot, say, take a photo of the back of a car", "Tesseract is intended for print documents rather than photos or handwritten text",
              "The exact results may vary as the language packs are updated", "Installing all languages adds about 600MB", "mostly three-character ISO 639-3 language codes", "while 'aze' is the ISO 639-3 code", "tess.image_to_string(img, lang='eng+jpn')",
              "NAPS2 does not make its application window appear", "'-n', '0'", "'--install', 'ocr-eng'", "Python's list slice syntax", "I also recommend the ocrmypdf package", "Tesseract is also designed to work with typewritten dark text on light backgrounds",
              "Preprocessing Images for OCR with Python and OpenCV", "Don't scan multicolumn images", "Use dark text on a light background, not white text on a black background", "Add a small white border", "Remove small bits of")
see("chapter 22 page: statements the research relies on (each is on the page of the book: True)", lambda: {s: (norm(s).replace("’", "'").lower() in text.replace("’", "'").lower()) for s in STATEMENTS})
see("chapter 22 page: words the chapter never uses although the topic needs them (False means absent from the page)", lambda: {s: s.lower() in text.lower() for s in ("psm", "page segmentation", "confidence", "image_to_data", "image_to_boxes", "tessdata", "tessdata_best", "tessdata_fast", "traineddata", "OEM", "LSTM", "dpi", "binar", "threshold", "grayscale", "deskew", "OpenCV", "NumPy", "whitelist", "hocr", "image_to_pdf_or_hocr", "timeout", "TesseractNotFoundError", "tesseract_cmd", "character error rate", "EasyOCR", "PaddleOCR", "Leptonica", "neural")})
ext = sorted({a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("http") and "automatetheboringstuff.com" not in a["href"]})
def link_status():
    out = []
    for u in ext:
        try:
            r = requests.get(u, timeout=60, headers=BROWSER, allow_redirects=False); out.append([u, r.status_code, r.headers.get("Location", "")[:100]])
        except Exception as e: out.append([u, "unreachable: %s" % type(e).__name__, ""])
    return out
see("chapter 22 page: every external link of the chapter, asked once without following a redirect: URL, HTTP status, Location", link_status)
see("chapter 22 page: every URL that appears in the text of the chapter", lambda: sorted({u.rstrip(".,)") for u in re.findall(r"https?://[\w./?=&#%~:+-]+", text) if "automatetheboringstuff.com/3e/chapter22" not in u}))
def autbor():
    out = {}
    for u in ("https://autbor.com/preprocessingocr", "https://autbor.com/embeddedfrankenstein/"):
        hops = []; cur = u
        for _ in range(6):
            r = requests.get(cur, timeout=60, headers=BROWSER, allow_redirects=False); hops.append([cur, r.status_code])
            if r.status_code in (301, 302, 303, 307, 308) and r.headers.get("Location"): cur = requests.compat.urljoin(cur, r.headers["Location"])
            else: break
        s = bs4.BeautifulSoup(r.text, "html.parser"); title = norm(s.title.get_text()) if s.title else ""
        for x in s(["script", "style"]): x.decompose()
        body = norm(s.get_text(" "))
        out[u] = {"hops": hops, "title": title, "visible characters": len(body), "placeholder note on the page": "placeholder" in body.lower(), "iframes": [i.get("src", "")[:100] for i in s.find_all("iframe")] if False else [i.get("src", "")[:100] for i in bs4.BeautifulSoup(r.text, "html.parser").find_all(["iframe", "embed", "object"])], "first 160 characters": body[:160]}
    return out
see("the two autbor.com links of the chapter followed through their redirects: where they end, the title of the page, whether it says it is a placeholder, what it embeds", autbor)
def appendix():
    a = get("https://automatetheboringstuff.com/3e/appendixa.html"); t = visible(a)
    return [a.status_code, re.findall(r"(?:pillow|pytesseract|pyautogui|openai-whisper)\s*[=~<>]*\s*[\w.]*", t)[:8], "pytesseract==0.3.10" in t, "pillow==10.4.0" in t, re.findall(r"The pytesseract package[^.]{0,200}\.", t)[:1]]
see("Appendix A of the book: status, the pins of the packages chapter 22 names, whether pytesseract is pinned to 0.3.10 and Pillow to 10.4.0, and the sentence about pytesseract", appendix)
def appendixb():
    a = get("https://automatetheboringstuff.com/3e/appendixb.html"); t = visible(a)
    i = t.find("Chapter 22 1."); j = t.find("Chapter 23", i)
    return [a.status_code, t[i:j][:1500]]
see("Appendix B of the book: the answers printed for the seven questions of chapter 22", appendixb)
def bookpage():
    r = get("https://nostarch.com/automate-boring-stuff-python-3rd-edition", headers=BROWSER); t = visible(r)
    links = [a["href"] for a in bs4.BeautifulSoup(r.text, "html.parser").find_all("a", href=True) if re.search(r"zip|download|code|github", a["href"], re.I)]
    return [r.status_code, len(r.content), {w: len(re.findall(w, t, re.I)) for w in ("Recognizing Text", "Tesseract", "OCR", "NAPS2")}, links[:8]]
see("the book page at nostarch.com that the chapter points to for the online resources: how often words occur on the page, and the download links on it", bookpage)
mat = get("https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip", headers=BROWSER)
see("online materials of the 3rd edition: status, bytes, SHA-256 of the zip", lambda: [mat.status_code, len(mat.content), sha(mat.content)])
def materials():
    z = zipfile.ZipFile(io.BytesIO(mat.content)); names = [n for n in z.namelist() if not n.endswith("/") and "__MACOSX" not in n and not n.split("/")[-1].startswith("._")]
    base = {n.split("/")[-1]: n for n in names}
    texts = {n.split("/")[-1]: z.read(n).decode("utf-8", "replace") for n in names if n.endswith(".py")}
    hits = lambda pat: sorted(k for k, v in texts.items() if re.search(pat, v))
    named = ["ocr-example.png", "frankenstein.png", "frankenstein_jpn.png", "preprocess_ocr.py", "ocrscreen.py", "output.pdf", "cat.png", "dog.png", "moose.png", "spam.pdf", "eggs.pdf", "output.txt"]
    return {"files": len(names), "python files": len(texts), "files of the chapter that the zip holds": {n: (n in base) for n in named}, "files in the zip whose name suggests this chapter": [n for n in names if re.search(r"ocr|frankenstein|tesseract|naps|preprocess|scan", n, re.I)],
            "python files that import pytesseract": hits(r"pytesseract"), "python files that import cv2": hits(r"import\s+cv2"), "python files that mention NAPS2": hits(r"(?i)naps2"),
            "sha256 of the three images and preprocess_ocr.py": {n: sha(z.read(base[n])) for n in ("ocr-example.png", "frankenstein.png", "frankenstein_jpn.png", "preprocess_ocr.py")}, "dictionary.txt bytes": len(z.read(base["dictionary.txt"])) if "dictionary.txt" in base else None}
see("online materials: the files, and whether each file the chapter names is in them", materials)
def shipped_py():
    z = zipfile.ZipFile(io.BytesIO(mat.content)); n = [x for x in z.namelist() if x.endswith("/preprocess_ocr.py") and "__MACOSX" not in x][0]; s = z.read(n).decode()
    p = bs4.BeautifulSoup(get("https://autbor.com/preprocessingocr").text, "html.parser").get_text()
    return {"lines": len(s.splitlines()), "raises FileNotFileError (a name that does not exist)": "FileNotFileError" in s, "page of autbor.com raises FileNotFoundError": "FileNotFoundError" in p, "binarize() calls grayscale_image (not defined in the file)": "grayscale_image" in s, "defines a function named open (hides the built-in open)": "def open(" in s}
see("online materials: preprocess_ocr.py against the placeholder page of autbor.com", shipped_py)
def pypi():
    out = {}
    for n in ("pytesseract", "pillow", "ocrmypdf", "opencv-python-headless", "pyautogui", "numpy"):
        j = get("https://pypi.org/pypi/%s/json" % n).json(); i = j["info"]; rel = j["releases"].get(i["version"], [])
        out[n] = {"version": i["version"], "uploaded": rel[0]["upload_time"][:10] if rel else None, "requires_python": i["requires_python"], "requires_dist": sorted((i["requires_dist"] or []))[:10], "yanked": bool(rel and rel[0].get("yanked"))}
    return out
see("PyPI: the newest release, its upload date, Requires-Python and dependencies of pytesseract, Pillow, OCRmyPDF, opencv-python-headless, PyAutoGUI and NumPy", pypi)
def pytess_releases():
    j = get("https://pypi.org/pypi/pytesseract/json").json(); rel = j["releases"]
    def ver(v): return [int(x) for x in re.findall(r"\d+", v)[:4]]
    vs = sorted(rel, key=ver)
    return {"releases": len(vs), "all": {v: rel[v][0]["upload_time"][:10] for v in vs if rel[v]}}
see("PyPI: every release of pytesseract with its upload date (the book pins 0.3.10)", pytess_releases)
see("sources of the research record: for each, the HTTP status, the bytes, and whether each passage the research relies on is on the page", sources)

# 1. real OCR software on the machine
ENG = {"apt 5.3.4": ("/usr/bin/tesseract", "/usr/share/tesseract-ocr/5/tessdata"), "5.5.3 (built from the tag)": (HOME + "/tesseract-5.5.3/bin/tesseract", HOME + "/tessdata_fast"), "4.1.1 (built from the tag)": (HOME + "/tesseract-4.1.1/bin/tesseract", HOME + "/tessdata_fast")}
def run(cmd, env=None, timeout=300):
    e = dict(os.environ); e.update(env or {})
    r = subprocess.run(cmd, capture_output=True, text=True, env=e, timeout=timeout, stdin=subprocess.DEVNULL); return (r.stdout + r.stderr).strip()
def engines():
    out = {}
    for k, (exe, data) in ENG.items():
        env = {"TESSDATA_PREFIX": data}
        v = run([exe, "--version"], env).splitlines(); langs = run([exe, "--list-langs"], env).splitlines()
        psm = run([exe, "--help-psm"], env); params = run([exe, "--print-parameters"], env)
        out[k] = {"version lines": [l.strip() for l in v[:4]], "languages listed (first line is the folder)": langs[0] if langs else "", "number of languages": len(langs) - 1, "psm modes printed by --help-psm": re.findall(r"^\s*(\d+)[|\s]", psm, re.M), "psm 2 text": [l.strip() for l in psm.splitlines() if re.match(r"\s*2[|\s]", l)], "configs and tessconfigs folders in the data folder": [os.path.isdir(data + "/configs"), os.path.isdir(data + "/tessconfigs")],
                  "parameters": {p: (re.search(r"^%s\s+(\S*)" % p, params, re.M).group(1) if re.search(r"^%s\s+(\S*)" % p, params, re.M) else "absent") for p in ("tessedit_do_invert", "thresholding_method", "user_defined_dpi", "tessedit_char_whitelist", "textord_heavy_nr", "invert_threshold")}}
    return out
see("each Tesseract on the machine: version and library lines, number of languages, the page segmentation modes it prints, and some parameters (absent means the program does not know the parameter)", engines)
EXP = r'''
import os, re, sys, json, tempfile, shutil, importlib.metadata as md
from PIL import Image, ImageDraw, ImageFont
import pytesseract as tess
def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1): cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]
def cer(ref, hyp): h = re.sub(r'\s+', ' ', hyp).strip(); return round(lev(ref, h) / len(ref), 4)
TEXT = 'It was on a dreary night of November, that I beheld the accomplishment of my toils.'
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', 28)
def page(fg, bg):
    im = Image.new('L', (int(f.getlength(TEXT)) + 40, 76), bg); ImageDraw.Draw(im).text((20, 15), TEXT, font=f, fill=fg); return im
d = tempfile.mkdtemp(); os.chdir(d); res = {}
inv = page(255, 0); pos = page(0, 255)
res['white on black, default'] = cer(TEXT, tess.image_to_string(inv))
res['white on black, -c tessedit_do_invert=0'] = cer(TEXT, tess.image_to_string(inv, config='-c tessedit_do_invert=0'))
res['black on white, -c tessedit_do_invert=0'] = cer(TEXT, tess.image_to_string(pos, config='-c tessedit_do_invert=0'))
pos.save('a.png'); page(0, 255).save('b.png'); open('images.txt', 'w').write('a.png\nb.png\n')
res['image_to_string of a list file (images.txt, two images): characters, number of copies of the line'] = (lambda t: [len(t), t.count('dreary')])(tess.image_to_string('images.txt'))
res['image_to_alto_xml: type, starts with, String elements'] = (lambda x: [type(x).__name__, x[:5].decode() if isinstance(x, bytes) else x[:5], x.count(b'<String ') if isinstance(x, bytes) else x.count('<String ')])(tess.image_to_alto_xml(pos))
try:
    t, b = tess.run_and_get_multiple_output(pos, extensions=['txt', 'box']); res['run_and_get_multiple_output txt+box: types, characters, boxes'] = [type(t).__name__, len(t), len(b.strip().split('\n'))]
except BaseException as e: res['run_and_get_multiple_output txt+box'] = type(e).__name__ + ': ' + str(e)[:100]
res['image_to_data TSV first line and a word line'] = tess.image_to_data(pos).split('\n')[0].split('\t'), tess.image_to_data(pos).split('\n')[5].split('\t')
res['conf of -1 rows (blocks, paragraphs, lines carry -1)'] = sorted({c for c in tess.image_to_data(pos, output_type=tess.Output.DICT)['conf']})[:3]
res['pytesseract.get_languages(config="") equals tesseract --list-langs'] = tess.get_languages(config='')
res['image_to_string with config --psm 7 and a trailing form feed'] = repr(tess.image_to_string(pos, config='--psm 7')[-3:])
res['pytesseract.image_to_string(pos) with lang="eng" repeated twice equals'] = tess.image_to_string(pos, lang='eng') == tess.image_to_string(pos)
print(json.dumps(res, ensure_ascii=False))
'''
def experiments():
    d = tempfile.mkdtemp(); p = os.path.join(d, "exp.py"); open(p, "w").write(EXP); out = {}
    for k in ("apt 5.3.4", "5.5.3 (built from the tag)"):
        exe, data = ENG[k]; data = ENG["apt 5.3.4"][1]; env = dict(os.environ); env["PATH"] = os.path.dirname(exe) + ":" + env["PATH"]; env["TESSDATA_PREFIX"] = data; env["PYTHONDONTWRITEBYTECODE"] = "1"
        r = subprocess.run([PYTHON, "-W", "ignore", p], capture_output=True, text=True, env=env, stdin=subprocess.DEVNULL, timeout=600)
        out[k] = json.loads(r.stdout.strip().splitlines()[-1]) if r.returncode == 0 else r.stderr[-300:]
    return out
see("pytesseract and Tesseract experiments on a page drawn here (character error rate; inversion switch; list file; ALTO; multiple outputs; confidence of container rows), with the apt Tesseract and with 5.5.3", experiments)
def find_loader():
    r = subprocess.run([PINS, "-c", "import importlib.util as u, os; print(os.path.dirname(u.find_spec('pytesseract').origin))"], capture_output=True, text=True)
    m = []
    if r.returncode == 0:
        for fn in sorted(os.listdir(r.stdout.strip())):
            if fn.endswith(".py"): m += [fn + ": " + l.strip() for l in open(os.path.join(r.stdout.strip(), fn), encoding="utf-8").read().splitlines() if "find_loader" in l]
    r2 = subprocess.run([PINS, "-c", "import pytesseract"], capture_output=True, text=True, stdin=subprocess.DEVNULL)
    return {"lines of pytesseract 0.3.10 that mention find_loader": m, "import under the Python of that environment": [r2.returncode, (r2.stderr.strip().splitlines() or [""])[-1][:120]], "python of that environment": subprocess.run([PINS, "-c", "import sys; print(sys.version.split()[0])"], capture_output=True, text=True).stdout.strip()}
see("pytesseract 0.3.10, the release Appendix A pins, under Python 3.14: the line that uses pkgutil.find_loader and the import error", find_loader)
def tools():
    out = {}
    for t in ("pdftotext", "pdfinfo", "pdftoppm", "naps2", "Xvfb", "scrot", "strace"):
        out[t] = shutil.which(t)
    out["naps2 package"] = run(["dpkg-query", "-W", "-f", "${Package} ${Version}", "naps2"]); out["poppler-utils"] = run(["dpkg-query", "-W", "-f", "${Version}", "poppler-utils"])
    out["fonts used (DejaVu, Nimbus Roman, Z003, IPAGothic)"] = [os.path.exists(p) for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/opentype/urw-base35/NimbusRoman-Regular.otf", "/usr/share/fonts/opentype/urw-base35/Z003-MediumItalic.otf", "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf")]
    return out
see("tools of the machine the research programs use besides Tesseract: where they are and which versions", tools)
see("data files: eng.traineddata of each kind, its size and SHA-256 prefix, and whether it equals the file the main branch of its GitHub repository serves today (fetched from raw.githubusercontent.com)", lambda: {k: [os.path.getsize(p + "/eng.traineddata"), sha(open(p + "/eng.traineddata", "rb").read())[:16], (lambda r: [r.status_code, sha(r.content)[:16] == sha(open(p + "/eng.traineddata", "rb").read())[:16]])(get("https://raw.githubusercontent.com/tesseract-ocr/%s/main/eng.traineddata" % repo, headers=BROWSER))] for k, (p, repo) in {"tessdata_fast": (HOME + "/tessdata_fast", "tessdata_fast"), "tessdata_best": (HOME + "/tessdata_best", "tessdata_best"), "tessdata (legacy and LSTM)": (HOME + "/tessdata_legacy", "tessdata")}.items()})
json.dump({"_version": __version__, "observed": datetime.date.today().isoformat(), "with": "requests %s, beautifulsoup4 %s, Python %s" % (requests.__version__, bs4.__version__, sys.version.split()[0]),
           "_note": "Single requests made on the day named, through the build machine's proxy, to the public pages and files the chapter names; the PyPI JSON of six packages; and experiments with real OCR software on the build machine (apt Tesseract 5.3.4, builds of 5.5.3 and 4.1.1, pytesseract 0.3.13). Nothing was posted anywhere. Not executed: Windows, macOS, a physical scanner, a large language model, a photograph from Wikimedia Commons. github.com pages answer 403 through the proxy, so only raw.githubusercontent.com files were used.",
           "items": obs}, open(OUT, "w"), indent=1, ensure_ascii=False)
print(len(obs), "observations ->", OUT)

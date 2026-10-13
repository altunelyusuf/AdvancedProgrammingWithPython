#!/usr/bin/env python3
"""Chapter 21 (Making Graphs and Manipulating Images): observes, once, what the public sources the chapter names answer today, what the files the book ships hold,
what the package index says about Pillow, Matplotlib and pyperclipimg, and what real picture software on the machine does, and writes what it saw with the date.
A web site changes and the files of the online materials may be replaced; the record is an observation of the day, not something the build can re-check, and no check reads it.
What it does: fetches the chapter page and compares its SHA-256 with the digest the book's own ontology records; counts what is on the page (listings, figures, tables,
practice questions), asks every external link of the chapter once without following a redirect, and asks for each picture of the chapter; reads Appendix A for the
versions the book pins and Appendix B for the answers to the chapter's twelve questions; downloads the online materials of the 3rd edition and looks for every file the
chapter names and compares the shipped resizeAndAddLogo.py with the listing; reads the second edition's chapter 19 for what the chapter replaced; reads the newest
releases of Pillow, Matplotlib and pyperclipimg on PyPI and, for every release of Pillow and of Matplotlib, whether a wheel exists for CPython 3.14; opens every source of
the research record and checks that the passages the research relies on are on the page.
On the machine itself it starts a virtual X server (Xvfb) and, on it, runs Image.show() with the real viewer (xdg-open starting ImageMagick's display) and takes a
screenshot of the screen to see the picture; copies a Pillow image to the clipboard with pyperclipimg and the real xclip and pastes it back, and asks what happens with no
display, with text on the clipboard and with no xclip; asks Matplotlib which backend it chooses with and without a display; and runs the life of a figure through
plt.show() with the real TkAgg window.
NOT EXECUTED and said so: Windows and macOS (their clipboard code, their font folders, the black fill of a rotation on Windows), a physical monitor, a Wayland clipboard
(wl-copy), a photograph from Wikimedia Commons (the API answered 429).
Run it with an interpreter that has requests and Beautiful Soup (/home/claude/venv314_web/bin/python); the local part uses CH21_LATEST (/home/claude/venv314_ch21_latest/bin/python).
Usage: sen0414_ch21_live_v1_0_0.py   -> ch21-page/live_observations_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, hashlib, io, json, os, re, shutil, subprocess, sys, tempfile, time, zipfile
import requests, bs4
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "08-tooling", "ch21-page", "live_observations_v1_0_0.json")
UA = {"User-Agent": "SEN0414-research/1.0 (academic course; altunel.yusuf@gmail.com)"}
BROWSER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0"}
PYTHON = os.environ.get("CH21_LATEST", "/home/claude/venv314_ch21_latest/bin/python")
obs = []
def see(what, f):
    try: v = f()
    except Exception as e: v = "raised %s: %s" % (type(e).__name__, str(e)[:200])
    obs.append({"what": what, "saw": v})
def get(u, **k):
    k.setdefault("headers", UA)
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
SOURCES = [
    ('P01', 'https://automatetheboringstuff.com/3e/chapter21.html', ['Pillow', 'Matplotlib', 'Table 21-1', 'Project 16: Add a Logo', '72 pixels per inch', 'points (rather than pixels)', 'On Windows, a black background', 'Tile Maker', 'Seating Cards']),
    ('P02', 'https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip', []),
    ('P03', 'https://automatetheboringstuff.com/3e/', ['Making Graphs and Manipulating Images']),
    ('P04', 'https://nostarch.com/automate-boring-stuff-python-3rd-edition', ['Making Graphs and Manipulating Images']),
    ('P05', 'https://automatetheboringstuff.com/3e/appendixa.html', ['pillow==10.4.0', 'matplotlib==3.92', 'pyperclipimg']),
    ('P06', 'https://automatetheboringstuff.com/3e/appendixb.html', ['ImageColor.getcolor', 'box tuple', 'plt.show()']),
    ('P07', 'https://automatetheboringstuff.com/2e/chapter19/', ['Pillow', 'textsize', 'ImageFont', 'FLIP_LEFT_RIGHT', 'Zophie']),
    ('P08', 'https://pillow.readthedocs.io/en/stable/reference/Image.html', ['crop', 'paste', 'rotate', 'transpose', 'putpixel', 'FLIP_LEFT_RIGHT', 'expand', 'fillcolor', 'resample', 'thumbnail']),
    ('P09', 'https://pillow.readthedocs.io/en/stable/reference/ImageColor.html', ['getcolor', 'HTML', 'CSS3']),
    ('P10', 'https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html', ['rectangle', 'ellipse', 'polygon', 'textbbox', 'textlength', 'width', 'fill']),
    ('P11', 'https://pillow.readthedocs.io/en/stable/reference/ImageFont.html', ['truetype', 'load_default', 'pixels', 'Windows', 'macOS', 'XDG']),
    ('P12', 'https://pillow.readthedocs.io/en/stable/handbook/tutorial.html', ['Image.open', 'crop', 'paste']),
    ('P13', 'https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html', ['dpi', 'pHYs', 'JPEG', 'PNG', 'quality']),
    ('P14', 'https://pillow.readthedocs.io/en/stable/handbook/concepts.html', ['RGBA', 'mode', 'LA']),
    ('P15', 'https://pillow.readthedocs.io/en/stable/reference/ImageGrab.html', ['grabclipboard', 'xclip', 'wl-paste']),
    ('P16', 'https://pillow.readthedocs.io/en/stable/reference/ImageShow.html', ['show', 'viewer', 'xdg-open']),
    ('P17', 'https://pillow.readthedocs.io/en/stable/releasenotes/9.1.0.html', ['Transpose', 'FLIP_LEFT_RIGHT', 'deprecat']),
    ('P18', 'https://pillow.readthedocs.io/en/stable/releasenotes/9.4.0.html', ['constants', 'FLIP_LEFT_RIGHT']),
    ('P19', 'https://pillow.readthedocs.io/en/stable/releasenotes/10.0.0.html', ['textsize', 'getsize', 'ANTIALIAS', 'constants']),
    ('P20', 'https://pillow.readthedocs.io/en/stable/releasenotes/10.1.0.html', ['load_default', 'size']),
    ('P21', 'https://pillow.readthedocs.io/en/stable/releasenotes/11.0.0.html', ['Python 3.13']),
    ('P22', 'https://pillow.readthedocs.io/en/stable/releasenotes/12.0.0.html', ['3.14']),
    ('P23', 'https://pillow.readthedocs.io/en/stable/deprecations.html', ['getdata', 'Removed', 'textsize']),
    ('P24', 'https://pillow.readthedocs.io/en/stable/installation/python-support.html', ['3.14', '3.10']),
    ('P25', 'https://pillow.readthedocs.io/en/stable/about.html', ['PIL', 'fork', 'Fredrik']),
    ('P26', 'https://pillow.readthedocs.io/en/stable/releasenotes/index.html', ['12.3.0']),
    ('P27', 'https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html', ['Line2D', 'marker', 'color']),
    ('P28', 'https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html', ['PathCollection', 'marker']),
    ('P29', 'https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html', ['BarContainer', 'categor']),
    ('P30', 'https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.pie.html', ['autopct', 'startangle', 'PieContainer', 'Previously the wedges and texts were returned in a tuple']),
    ('P31', 'https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.show.html', ['block', 'interactive', 'non-interactive']),
    ('P32', 'https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html', ['dpi', 'format', 'bbox_inches']),
    ('P33', 'https://matplotlib.org/stable/users/explain/figure/api_interfaces.html', ['pyplot', 'Axes', 'implicit']),
    ('P34', 'https://matplotlib.org/stable/users/explain/figure/backends.html', ['Agg', 'TkAgg', 'interactive', 'non-interactive']),
    ('P35', 'https://matplotlib.org/stable/users/explain/figure/interactive.html', ['show', 'block', 'interactive']),
    ('P36', 'https://matplotlib.org/stable/api/prev_api_changes/api_changes_3.11.0.html', ['3.11']),
    ('P37', 'https://matplotlib.org/stable/install/dependencies.html', ['Python', 'Tk', 'Pillow']),
    ('P38', 'https://raw.githubusercontent.com/asweigart/pyperclipimg/main/README.md', ['xclip', 'wl-copy', 'pyperclipimg']),
    ('P39', 'https://pypi.org/pypi/pillow/json', ['pillow']),
    ('P40', 'https://pypi.org/pypi/matplotlib/json', ['matplotlib']),
    ('P41', 'https://pypi.org/pypi/pyperclipimg/json', ['pyperclipimg']),
    ('P42', 'https://www.w3.org/TR/png-3/', ['IHDR', 'pHYs', '89 50 4E 47', 'alpha']),
    ('P43', 'https://www.rfc-editor.org/rfc/rfc2083', ['PNG', '1997', 'Boutell']),
    ('P44', 'https://www.w3.org/Graphics/JPEG/itu-t81.pdf', []),
    ('P45', 'https://www.w3.org/Graphics/JPEG/jfif3.pdf', []),
    ('P46', 'https://www.w3.org/TR/css-color-4/', ['rebeccapurple', 'lime', 'darkgray']),
    ('P47', 'https://docs.python.org/3.14/library/os.html', ['arbitrary order', 'listdir', 'walk']),
    ('P48', 'https://docs.python.org/3.14/library/struct.html', ['big-endian', 'network']),
    ('P49', 'https://docs.python.org/3.14/whatsnew/3.14.html', ['copy', '3.14']),
    ('P50', 'https://docs.python.org/3.14/library/tkinter.html', ['Tk', '9.0']),
    ('P51', 'https://www.tcl-lang.org/software/tcltk/9.0.html', ['9.0']),
    ('P52', 'https://en.wikipedia.org/wiki/Russell_A._Kirsch', ['176', 'Walden', 'SEAC', '1957']),
    ('P53', 'https://en.wikipedia.org/wiki/Alpha_compositing', ['Catmull', 'Smith', 'Porter', 'Duff', '1984']),
    ('P54', 'https://en.wikipedia.org/wiki/PNG', ['GIF', '1996', 'Boutell', 'W3C']),
    ('P55', 'https://en.wikipedia.org/wiki/JPEG', ['1992', 'Joint Photographic Experts Group', 'ITU']),
    ('P56', 'https://en.wikipedia.org/wiki/Matplotlib', ['John D. Hunter', '2003', 'MATLAB']),
    ('P57', 'https://en.wikipedia.org/wiki/Python_Imaging_Library', ['Fredrik Lundh', 'Pillow']),
    ('P58', 'https://en.wikipedia.org/wiki/Web_colors', ['Lime', 'Green', 'rebeccapurple', 'Gray']),
    ('P59', 'https://docs.astral.sh/uv/concepts/python-versions/', ['uv python install']),
    ('P60', 'https://www.python.org/downloads/', ['Python 3.14']),
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
ch = get("https://automatetheboringstuff.com/3e/chapter21.html")
DIGEST = "cb9e204bc3d3455abe51f81c96b6360f01491635805b5bea65e93643cb186a28"
ONTO = "/home/claude/Ontologies/automate-python-book-3e/01-ontologies/automate_python_3e_ch21_v1_0_0.ttl"
see("chapter 21 page: status, bytes, SHA-256, equal to the chapterDigest of the book ontology (read from its file when present)", lambda: [ch.status_code, len(ch.content), sha(ch.content), sha(ch.content) == DIGEST, (DIGEST in open(ONTO).read()) if os.path.exists(ONTO) else "ontology file not present"])
soup = bs4.BeautifulSoup(ch.text, "html.parser"); text = norm(soup.get_text(" "))
IMGS = [i["src"] for i in soup.find_all("img") if i.get("src") and "cover" not in i["src"]]
def image_dims():
    d = tempfile.mkdtemp(); rows = []
    for k, src in enumerate(IMGS):
        r = get("https://automatetheboringstuff.com/3e/" + src); p = os.path.join(d, "i%d.jpg" % k); open(p, "wb").write(r.content); rows.append([src, r.status_code, len(r.content)])
    code = "import sys, json; from PIL import Image; print(json.dumps([list(Image.open(p).size) for p in sys.argv[1:]]))"
    sizes = json.loads(subprocess.run([PYTHON, "-c", code] + [os.path.join(d, "i%d.jpg" % k) for k in range(len(IMGS))], capture_output=True, text=True).stdout)
    shutil.rmtree(d); return [r + [s] for r, s in zip(rows, sizes)]
see("chapter 21 page: number of listings (pre elements), figure captions, tables, and the HTTP status, bytes and pixel size of each picture of the chapter (the pictures are asked for and measured, not kept)", lambda: [len(soup.find_all("pre")), sorted(set(re.findall(r"Figure 21-\d+", text)), key=lambda x: [int(n) for n in re.findall(r"\d+", x)]), sorted(set(re.findall(r"Table 21-\d+", text))), len(soup.find_all("table")), image_dims()])
see("chapter 21 page: the headings of the chapter in order", lambda: [(h.name, norm(h.get_text())) for h in soup.find_all(["h2", "h3", "h4", "h5"])])
STATEMENTS = ("Table 21-1", "Pillow uses the same standard color names as HTML", "Pillow represents green with (0, 255, 0, 255)", "more than 100 standard color names", "the box tuple (3, 1, 9, 6)",
              "(816, 1088)", "'Portable network graphics'", "(230, 215)", "points (rather than pixels)", "72 pixels per inch", "a 4×5-inch card would require a 288×360-pixel image",
              "On Windows, a black background will fill in any gaps", "On macOS and Linux, transparent pixels will fill in the gaps instead", "225×300", "The default graph",
              "default to white if left unspecified", "A public domain flower image is also available", "will block and not return until the user closes this window",
              "either does nothing or displays an empty window", "To save an image file of the graph, you must call plt.savefig() before calling plt.show()", "20×50-pixel image", "120×500 image with 60 tiles")
see("chapter 21 page: statements the research relies on (each is on the page of the book: True)", lambda: {s: (norm(s) in text) for s in STATEMENTS})
see("chapter 21 page: words the chapter never uses although the topic needs them (False means absent from the page)", lambda: {s: s.lower() in text.lower() for s in ("thumbnail", "convert(", "ImageOps", "ImageFilter", "alpha_composite", "textbbox", "textlength", "textsize", "getsize", "load_default", "resample", "LANCZOS", "EXIF", "dpi", "quality",
      "figure(", "subplots", "tight_layout", "plt.close", "backend", "Agg", "Axes", "numpy", "context manager", "with Image.open", "close()", "mode", "RGB ", "JPEG quality", "GIF", "WebP", "alpha channel", "premultipl", "gamma", "sRGB", "plt.xlim", "bbox_inches", "savefig(")})
ext = sorted({a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("http") and "automatetheboringstuff.com" not in a["href"]})
def link_status():
    out = []
    for u in ext:
        try:
            r = requests.get(u, timeout=60, headers=BROWSER, allow_redirects=False); out.append([u, r.status_code, r.headers.get("Location", "")[:100]])
        except Exception as e: out.append([u, "unreachable: %s" % type(e).__name__, ""])
    return out
see("chapter 21 page: every external link of the chapter, asked once without following a redirect: URL, HTTP status, Location", link_status)
see("chapter 21 page: every URL that appears in the text of the chapter", lambda: sorted({u.rstrip(".,)") for u in re.findall(r"https?://[\w./?=&#%~:+-]+", text) if "automatetheboringstuff.com/3e/chapter21" not in u}))
def appendix():
    a = get("https://automatetheboringstuff.com/3e/appendixa.html"); t = visible(a)
    return [a.status_code, re.findall(r"(?:pillow|matplotlib|pyperclipimg|pyperclip|requests)\s*[=~<>]+\s*[\w.]+", t), "pillow==10.4.0" in t, "matplotlib==3.92" in t, "matplotlib==3.9.2" in t, re.findall(r"pyperclipimg[^.]{0,60}", t)[:2]]
see("Appendix A of the book: status, the pins of the packages chapter 21 names, whether Pillow is pinned to 10.4.0, whether Matplotlib is pinned to 3.92 (a version that does not exist) or to 3.9.2, and how pyperclipimg is listed", appendix)
def appendixb():
    a = get("https://automatetheboringstuff.com/3e/appendixb.html"); t = visible(a)
    i = t.find("Chapter 21 1."); j = t.find("Chapter 22", i)
    return [a.status_code, t[i:j][:2400]]
see("Appendix B of the book: the answers printed for the twelve questions of chapter 21", appendixb)
def bookpage():
    r = get("https://nostarch.com/automate-boring-stuff-python-3rd-edition", headers=BROWSER); t = visible(r)
    links = [a["href"] for a in bs4.BeautifulSoup(r.text, "html.parser").find_all("a", href=True) if re.search(r"zip|download|code|github", a["href"], re.I)]
    return [r.status_code, len(r.content), {w: len(re.findall(w, t, re.I)) for w in ("Making Graphs", "Pillow", "Matplotlib", "zophie", "catlogo")}, links[:8]]
see("the book page at nostarch.com that the chapter points to for the online resources: how often words occur on the page, and the download links on it", bookpage)
mat = get("https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip", headers=BROWSER)
see("online materials of the 3rd edition: status, bytes, SHA-256 of the zip", lambda: [mat.status_code, len(mat.content), sha(mat.content)])
def materials():
    z = zipfile.ZipFile(io.BytesIO(mat.content)); names = [n for n in z.namelist() if not n.endswith("/") and "__MACOSX" not in n and not n.split("/")[-1].startswith("._")]
    base = {n.split("/")[-1]: n for n in names}
    texts = {n.split("/")[-1]: z.read(n).decode("utf-8", "replace") for n in names if n.endswith(".py")}
    hits = lambda pat: sorted(k for k, v in texts.items() if re.search(pat, v))
    named = ["zophie.png", "catlogo.png", "guests.txt", "resizeAndAddLogo.py", "zophie_xmas_tree.png", "me_and_zophie.png", "zophie_the_cat.jpg", "zophie.jpg", "flower.png", "flower.jpg", "tiles.py"]
    chap = [n for n in names if re.search(r"flower|zophie|catlogo|guests|resizeandaddlogo|tile|seating|photo", n, re.I)]
    return {"files": len(names), "python files": len(texts), "files of the chapter that the zip holds": {n: (n in base) for n in named}, "files in the zip whose name suggests this chapter": chap,
            "python files that import PIL": hits(r"(from|import)\s+PIL"), "python files that import matplotlib": hits(r"import\s+matplotlib"), "python files that import pyperclipimg": hits(r"pyperclipimg"),
            "images in the zip (png, jpg, gif)": [n for n in names if re.search(r"\.(png|jpe?g|gif)$", n, re.I)], "sha256 of zophie.png, catlogo.png, guests.txt and resizeAndAddLogo.py": {n: sha(z.read(base[n])) for n in ("zophie.png", "catlogo.png", "guests.txt", "resizeAndAddLogo.py")}}
see("online materials: the files, and whether each file the chapter names is in them", materials)
def shipped_vs_listing():
    z = zipfile.ZipFile(io.BytesIO(mat.content)); n = [x for x in z.namelist() if x.endswith("/resizeAndAddLogo.py") and "__MACOSX" not in x][0]
    s = z.read(n).decode(); lines = [l.strip() for l in s.splitlines() if l.strip() and not l.strip().startswith("#")]
    pre = [re.sub(r"[❶-❿] ?", "", l.replace("–", "-")).strip() for p in soup.find_all("pre") for l in p.get_text().splitlines()]
    missing = [l for l in lines if l not in pre and l.split("#")[0].rstrip() not in [x.split("#")[0].rstrip() for x in pre]]
    return {"code lines of the shipped file": len(lines), "lines not found among the lines of the listings (after removing the callout numbers and writing the en dash as a minus sign)": missing,
            "does the file contain an en dash": "–" in s, "first comment line": s.splitlines()[0]}
see("online materials: the shipped resizeAndAddLogo.py against the listings of the chapter", shipped_vs_listing)
def second_edition():
    r = get("https://automatetheboringstuff.com/2e/chapter19/"); t = visible(r)
    return [r.status_code, {w: len(re.findall(w, t)) for w in ("Pillow", "textsize", "ImageFont", "FLIP_LEFT_RIGHT", "Zophie", "matplotlib", "Matplotlib", "pyperclipimg", "pyperclip", "putpixel", "ImageDraw", "getcolor", "resize", "rotate", "load_default")}]
see("the second edition's chapter 19 (Manipulating Images), which this chapter replaced: how often each name occurs on the page", second_edition)
def pypi():
    out = {}
    for n in ("pillow", "matplotlib", "pyperclipimg", "numpy"):
        j = get("https://pypi.org/pypi/%s/json" % n).json(); i = j["info"]; rel = j["releases"].get(i["version"], [])
        out[n] = {"version": i["version"], "uploaded": rel[0]["upload_time"][:10] if rel else None, "requires_python": i["requires_python"], "requires_dist": sorted((i["requires_dist"] or []))[:14], "yanked": bool(rel and rel[0].get("yanked"))}
    return out
see("PyPI: the newest release, its upload date, Requires-Python and dependencies of Pillow, Matplotlib, pyperclipimg and NumPy", pypi)
def wheels():
    def ver(v): return [int(x) for x in re.findall(r"\d+", v)[:3]] + [0] * (3 - len(re.findall(r"\d+", v)[:3]))
    res = {}
    for n in ("pillow", "matplotlib"):
        j = get("https://pypi.org/pypi/%s/json" % n).json(); rel = j["releases"]; vs = sorted((v for v in rel if re.fullmatch(r"\d+\.\d+\.\d+", v) and rel[v]), key=ver)
        first = next((v for v in vs if any("cp314-cp314-" in f["filename"] and "manylinux" in f["filename"] and "x86_64" in f["filename"] for f in rel[v])), None)
        want = ("9.5.0", "10.0.0", "10.4.0", "11.0.0", "11.3.0", "12.0.0", "12.3.0") if n == "pillow" else ("3.7.5", "3.8.4", "3.9.2", "3.10.0", "3.10.6", "3.10.7", "3.10.8", "3.11.0", "3.11.2")
        res[n] = {"releases with a plain x.y.z number": len(vs), "first release with a CPython 3.14 manylinux x86_64 wheel": first,
                  "per release: [uploaded, has a cp314 wheel, has a cp313 wheel, has an sdist]": {v: ([rel[v][0]["upload_time"][:10], any("cp314-cp314-" in f["filename"] for f in rel[v]), any("cp313-cp313-" in f["filename"] for f in rel[v]), any(f["packagetype"] == "sdist" for f in rel[v])] if v in rel and rel[v] else "no such release") for v in want}}
        res[n]["a release numbered 3.92 exists"] = ("3.92" in rel) if n == "matplotlib" else None
    return res
see("PyPI: for Pillow and Matplotlib, the first release with a CPython 3.14 wheel and the wheels of the releases the study names (the book pins Pillow 10.4.0 and 'matplotlib==3.92')", wheels)
see("sources of the research record: for each, the HTTP status, the bytes, and whether each passage the research relies on is on the page", sources)

# 1. real picture software on the machine (a virtual X server, Xvfb, with the real viewer, clipboard program and Tk)
LOCAL_SRC = r'''import sys, os, json, time, subprocess, tempfile, shutil, hashlib, importlib.metadata as md
obs = []
def see(what, f):
    try: v = f()
    except BaseException as e: v = 'raised %s: %s' % (type(e).__name__, str(e).splitlines()[0][:200] if str(e) else '')
    obs.append([what, v])
Z = os.environ['ZOPHIE']; DISP = os.environ['DISP']; PY = sys.executable
def child(code, env_extra=None, drop=(), timeout=120, path=None):
    e = dict(os.environ); e.update(env_extra or {})
    for k in drop: e.pop(k, None)
    if path is not None: e['PATH'] = path
    fo = tempfile.TemporaryFile('w+'); fe = tempfile.TemporaryFile('w+')
    r = subprocess.run([PY, '-W', 'ignore', '-c', code], stdin=subprocess.DEVNULL, stdout=fo, stderr=fe, text=True, env=e, timeout=timeout)
    fo.seek(0); fe.seek(0); so = fo.read(); se = fe.read()
    return (so.strip(), (se.strip().splitlines() or [''])[-1][:200], r.returncode)
CLIP = """
from PIL import Image
import pyperclipimg, json
im = Image.open(%r)
a = pyperclipimg.copy(im); b = pyperclipimg.paste()
print(json.dumps([repr(a), type(b).__name__, b.format, b.mode, list(b.size), list(b.getdata()) == list(im.getdata())]))
""" % Z
def clipboard_roundtrip():
    out, err, rc = child(CLIP, {'DISPLAY': DISP}); return json.loads(out) if rc == 0 else [out, err, rc]
see('pyperclipimg 0.2.0 with the real xclip on the virtual display: copy(zophie) then paste(): what copy returns, the type, format and mode of what paste returns, its size, and whether every pixel is equal to the original', clipboard_roundtrip)
see('the clipboard targets after pyperclipimg.copy(), asked with xclip -t TARGETS: the program that holds the clipboard offers the image as image/png', lambda: (child(CLIP, {'DISPLAY': DISP}), subprocess.run(['xclip', '-selection', 'clipboard', '-t', 'TARGETS', '-o'], capture_output=True, text=True, env={**os.environ, 'DISPLAY': DISP}).stdout.split())[1])
see('pyperclipimg.copy() with no DISPLAY (a server, a container): what it returns, whether it raises, and what paste() then does', lambda: child("""
from PIL import Image
import pyperclipimg, json
im = Image.open(%r)
a = pyperclipimg.copy(im)
try: b = repr(pyperclipimg.paste())
except Exception as e: b = type(e).__name__ + ': ' + str(e)[:70]
print(json.dumps([repr(a), b]))""" % Z, drop=('DISPLAY',)))
def put_text(t):
    p = subprocess.Popen(['xclip', '-selection', 'clipboard', '-i'], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env={**os.environ, 'DISPLAY': DISP}, start_new_session=True)
    p.stdin.write(t.encode()); p.stdin.close(); time.sleep(0.7)

see('paste() when the clipboard holds text (put there with xclip) instead of an image: the exception', lambda: (put_text('hello'), child("import re, pyperclipimg\ntry: print(repr(pyperclipimg.paste()))\nexcept Exception as e: print(type(e).__name__ + ': ' + re.sub('0x[0-9a-f]+', '0xADDR', str(e)[:70]))", {'DISPLAY': DISP}))[1])
see('import pyperclipimg on Linux with no xclip and no wl-copy on the PATH: the exception and its text', lambda: child("import pyperclipimg", {'DISPLAY': DISP}, path='/nonexistent'))
see('Pillow ImageGrab.grabclipboard() and the programs it needs on Linux (the version of Pillow, and which of xclip, wl-paste are on the PATH)', lambda: [md.version('pillow'), shutil.which('xclip') is not None, shutil.which('wl-paste') is not None, shutil.which('xsel') is not None])
def backend(display):
    out, err, rc = child("import matplotlib; import matplotlib.pyplot as plt; print(matplotlib.get_backend())", {'DISPLAY': DISP} if display else {}, drop=() if display else ('DISPLAY', 'MPLBACKEND')); return out or err
see('Matplotlib: which backend it picks by itself (matplotlib.get_backend() after importing pyplot) with a display (the virtual one) and with none', lambda: {'DISPLAY set': backend(True), 'no DISPLAY': backend(False)})
TKLIFE = """
import os, time, json, matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from PIL import Image
x_values = [0, 1, 2, 3, 4, 5]; y_values1 = [10, 13, 15, 18, 16, 20]; y_values2 = [9, 11, 18, 16, 17, 19]
plt.plot(x_values, y_values1); plt.plot(x_values, y_values2)
plt.savefig('lg.png'); fig = plt.gcf()
res = {'figures before show': plt.get_fignums(), 'lines before show': len(fig.axes[0].lines)}
t = fig.canvas.new_timer(interval=700); t.add_callback(lambda: plt.close(fig)); t.start(); t0 = time.time()
r = plt.show(); res['show returned'] = repr(r); res['show blocked for at least 0.6 s'] = (time.time() - t0) >= 0.6
res['figures after show'] = plt.get_fignums()
res['second plt.show() with no figure left returned at once'] = (lambda t1: (plt.show(), time.time() - t1 < 0.5)[1])(time.time())
plt.savefig('after.png')
res['figures after savefig made a new one'] = plt.get_fignums(); res['lines on the new figure'] = len(plt.gcf().axes[0].lines) if plt.gcf().axes else 0
a = Image.open('lg.png').convert('RGB'); b = Image.open('after.png').convert('RGB')
res['lg.png and after.png: size, colours in each'] = [list(a.size), len(a.getcolors(10**6)), list(b.size), len(b.getcolors(10**6))]
t = plt.gcf().canvas.new_timer(interval=700); t.add_callback(lambda: plt.close('all')); t.start(); t0 = time.time(); plt.show()
res['plt.show() of the new empty figure blocked for at least 0.6 s'] = (time.time() - t0) >= 0.6
print(json.dumps(res))
"""
def tk_life():
    d = tempfile.mkdtemp(); out, err, rc = child("import os; os.chdir(%r)\n" % d + TKLIFE, {'DISPLAY': DISP}); shutil.rmtree(d); return json.loads(out.splitlines()[-1]) if rc == 0 else [out[-200:], err, rc]
see('Matplotlib 3.11.2 with the real TkAgg window on the virtual display: the life of a figure through savefig, show (the window is closed by a timer 0.7 s after it opens), a second show, and a savefig after the window was closed', tk_life)
print(json.dumps(obs))
'''
def local():
    d = tempfile.mkdtemp(); src = os.path.join(d, "live_local.py"); open(src, "w").write(LOCAL_SRC)
    mats = zipfile.ZipFile(io.BytesIO(mat.content)); n = [x for x in mats.namelist() if x.endswith("/zophie.png") and "__MACOSX" not in x][0]; zp = os.path.join(d, "zophie.png"); open(zp, "wb").write(mats.read(n))
    disp = ":%d" % (60 + os.getpid() % 30)
    xv = subprocess.Popen(["Xvfb", disp, "-screen", "0", "1280x1024x24"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(3)
    try:
        env = {**os.environ, "DISP": disp, "ZOPHIE": zp}
        fo = tempfile.TemporaryFile('w+'); fe = tempfile.TemporaryFile('w+')
        r = subprocess.run([PYTHON, src], stdin=subprocess.DEVNULL, stdout=fo, stderr=fe, text=True, env=env, timeout=600)
        fo.seek(0); fe.seek(0); r.stdout = fo.read(); r.stderr = fe.read()
        res = [{"what": w, "saw": s} for w, s in json.loads(r.stdout.strip().splitlines()[-1])] if r.returncode == 0 else [{"what": "local clipboard and Tk experiments failed", "saw": r.stderr[-600:]}]
        res.append({"what": "Image.show() of zophie.png on the virtual display with the real viewer, and a screenshot of the screen taken with ImageMagick's import: the viewer processes, and how many of 6 probe pixels of zophie.png are found at the same place in the screenshot", "saw": show_screenshot(disp, zp, d)})
        return res
    finally:
        subprocess.run(["pkill", "-x", "display-im6.q16"]); xv.terminate(); xv.wait(); shutil.rmtree(d, ignore_errors=True)
def show_screenshot(disp, zp, d):
    env = {**os.environ, "DISPLAY": disp}
    code = "from PIL import Image, ImageShow; im = Image.open(%r); print(repr(im.show()), [type(v).__name__ for v in ImageShow._viewers])" % zp
    fo = tempfile.TemporaryFile("w+"); fe = tempfile.TemporaryFile("w+")
    r = subprocess.run([PYTHON, "-W", "ignore", "-c", code], stdout=fo, stderr=fe, text=True, env=env, timeout=60, stdin=subprocess.DEVNULL); time.sleep(4)
    fo.seek(0); fe.seek(0); r.stdout = fo.read(); r.stderr = fe.read()
    ps = subprocess.run(["ps", "-eo", "args"], capture_output=True, text=True).stdout.splitlines(); procs = sorted({re.sub(r"/tmp/\S+", "TEMPFILE", l.strip()) for l in ps if l.strip().split(" ")[0].rsplit("/", 1)[-1].startswith("display")})
    shot = os.path.join(d, "shot.png"); subprocess.run(["import", "-window", "root", shot], env=env, timeout=60, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    code2 = "import json, sys; from PIL import Image; s = Image.open(sys.argv[1]).convert('RGB'); z = Image.open(sys.argv[2]).convert('RGB'); P = [(10, 10), (100, 50), (200, 300), (50, 200), (300, 100), (400, 20)]; best = (0, 0, 0)\nfor ox in range(600, 700):\n    for oy in range(600, 700):\n        ok = sum(1 for i, j in P if s.getpixel((ox + i, oy + j)) == z.getpixel((i, j)))\n        if ok > best[0]: best = (ok, ox, oy)\nprint(json.dumps([list(s.size), best[0], len(P), z.size[0] > s.size[0] // 2]))"
    r2 = subprocess.run([PYTHON, "-W", "ignore", "-c", code2, shot, zp], capture_output=True, text=True)
    return {"Image.show() printed": r.stdout.strip(), "stderr": r.stderr.strip()[-120:], "viewer processes found": procs, "screenshot size, probe pixels matched, number of probes, picture wider than half the screen": json.loads(r2.stdout) if r2.returncode == 0 else r2.stderr[-200:]}
try: obs.extend(local())
except Exception as e: obs.append({"what": "local picture software", "saw": "raised %s: %s" % (type(e).__name__, str(e)[:200])})

json.dump({"_version": __version__, "observed": datetime.date.today().isoformat(), "with": "requests %s, beautifulsoup4 %s, Python %s" % (requests.__version__, bs4.__version__, sys.version.split()[0]),
           "_note": "Single requests made on the day named, through the build machine's proxy, to the public pages and files the chapter names; the PyPI JSON of four packages; and experiments with real picture software on the build machine: a virtual X server (Xvfb) with ImageMagick's display as the viewer that Image.show() starts, xclip as the clipboard program of pyperclipimg, and a Tk window for Matplotlib. Nothing was posted anywhere. Not executed: Windows, macOS, a physical monitor, Wayland, a photograph from Wikimedia Commons.",
           "items": obs}, open(OUT, "w"), indent=1, ensure_ascii=False)
print(len(obs), "observations ->", OUT)

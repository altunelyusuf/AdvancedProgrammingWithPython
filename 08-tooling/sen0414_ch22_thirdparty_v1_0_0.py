#!/usr/bin/env python3
"""Chapter 22 (Recognizing Text in Images): runs the chapter's own listings, whole and as printed, under the given interpreter and Tesseract, and writes or checks their recorded output.
What is fetched at run time and kept in a cache directory (CH22_CACHE, default the system temp directory): the chapter page
(https://automatetheboringstuff.com/3e/chapter22.html; its sha256 is compared with the chapterDigest of the book's own chapter ontology, 4228da08...6232) and the
online materials of the 3rd edition (the zip that No Starch Press links from its book page, sha256 dac627e8...916), from which ocr-example.png, frankenstein.png,
frankenstein_jpn.png and preprocess_ocr.py are taken and hash-checked. Nothing of either is stored in the repository.
The listings are not typed in here: every REPL listing is parsed from the page itself (the prompt lines, the continuation lines and the printed output that follows them;
the lines of a statement that the typesetting broke inside an open bracket are joined) and every statement is run in the order of the book, in one shell session per group, as
printed. The page has 8 listings: 1 (ocr-example.png), 2 (frankenstein.png), 3 (the output of the language model, text, not code), 4 (get_languages), 5 (lang='jpn'),
6 (lang='eng' on the Japanese image), 7 (the NAPS2 call with subprocess) and 8 (the template of ocrscreen.py, a program).
Environments (rows of the record), all with Python 3.14.6 unless named, installed with uv:
  LATEST       pytesseract 0.3.13, Pillow 12.3.0, NumPy 2.5.4: /home/claude/venv314_ch22_latest
  PINS313      the versions Appendix A of the book pins, pytesseract 0.3.10 and Pillow 10.4.0, under Python 3.13.14 (/home/claude/venv313_ch22_pins), because ...
  PINS         ... under 3.14.6 the pinned pytesseract cannot even be imported (pkgutil.find_loader was removed in 3.14): /home/claude/venv314_ch22_pins
  BARE         no package at all
and engines (the program that pytesseract starts, found through the PATH): the apt package tesseract-ocr 5.3.4 with its tessdata_fast data (Ubuntu 24.04), Tesseract 5.5.3 and
4.1.1 built from the tags of github.com/tesseract-ocr/tesseract into /home/claude/tesseract-5.5.3 and /home/claude/tesseract-4.1.1, and the language data of the repositories
tessdata_fast and tessdata_best (raw files of the main branch), and the whole tessdata_fast repository at commit 87416418 (2024-08-01, 126 language files) for the listing
that asks for all languages.
Two modes: HEADLESS (no DISPLAY) and DISPLAY (a virtual X server, Xvfb, started here, with real ImageMagick display, scrot and the empty ~/.Xauthority that python-xlib wants).
Not executed: Windows, macOS, the installers of Tesseract and NAPS2 for them, the large language model, a physical scanner.
Usage: sen0414_ch22_thirdparty_v1_0_0.py write|check
Record: 08-tooling/ch22-page/third_party_record_v1_0_0.json"""
__version__ = "1.0.0"
import difflib, hashlib, html, io, json, os, re, shutil, subprocess, sys, tempfile, time, urllib.request, zipfile
MODE = sys.argv[1] if len(sys.argv) > 1 else "check"
HOME = "/home/claude"
LATEST = os.environ.get("CH22_LATEST", HOME + "/venv314_ch22_latest/bin/python")
PINS = os.environ.get("CH22_PINS", HOME + "/venv314_ch22_pins/bin/python")
PINS13 = os.environ.get("CH22_PINS13", HOME + "/venv313_ch22_pins/bin/python")
BARE = os.environ.get("CH22_BARE", HOME + "/venv314_ch22_bare/bin/python")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REC = os.path.join(REPO, "08-tooling", "ch22-page", "third_party_record_v1_0_0.json")
CACHE = os.environ.get("CH22_CACHE") or tempfile.gettempdir()
DIGEST = "4228da08b22649e4c3dd4b5aa9d6346bae3fd50f1ac9f9a8e5a31a80d0416232"
ZIPSHA = "dac627e807f69ee14913ba621a15dec1f98db739d76939555ba5360d05eba916"
FILESHA = {"ocr-example.png": "c875a04c8a51401f59848ea93bd754fb6095f9f1a0041e4878dd05eeb44b13b8", "frankenstein.png": "c2125e5ef6840d4f23dfba68021c52710290a4c8d3cafdbabf1f619c70b33851",
           "frankenstein_jpn.png": "3f812b8e5e396db6685f1cfe9e35639b9eaabd727cdb861e2663c6c768ca40fd", "preprocess_ocr.py": "e204109350e49c621159c3c8d656da3af564e368a9d0d84b95f222cfa583f377"}
UA = {"User-Agent": "SEN0414-research/1.0 (academic course; altunel.yusuf@gmail.com)"}
BROWSER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0"}
ENGINES = {"apt": (None, None), "5.5.3-fast": (HOME + "/tesseract-5.5.3/bin", HOME + "/tessdata_fast"), "5.5.3-best": (HOME + "/tesseract-5.5.3/bin", HOME + "/tessdata_best"),
           "4.1.1-fast": (HOME + "/tesseract-4.1.1/bin", HOME + "/tessdata_fast"), "apt-all": (None, HOME + "/tessdata_fast_all"), "5.5.3-all": (HOME + "/tesseract-5.5.3/bin", HOME + "/tessdata_fast_all")}
ROWS = [("LATEST", LATEST, "apt"), ("LATEST", LATEST, "5.5.3-fast"), ("LATEST", LATEST, "5.5.3-best"), ("LATEST", LATEST, "4.1.1-fast"), ("LATEST", LATEST, "apt-all"), ("LATEST", LATEST, "5.5.3-all"),
        ("PINS313", PINS13, "apt"), ("PINS", PINS, "apt"), ("BARE", BARE, "apt")]
def fetch(url, path, headers):
    if not os.path.exists(path):
        open(path + ".part", "wb").write(urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=180).read()); os.replace(path + ".part", path)
    return open(path, "rb").read()
def chapter():
    b = fetch("https://automatetheboringstuff.com/3e/chapter22.html", os.path.join(CACHE, "ch22_chapter.html"), UA)
    assert hashlib.sha256(b).hexdigest() == DIGEST, "the chapter page differs from the one the study recorded"
    return b.decode("utf-8")
def materials():
    """the files of the online materials the replay needs, as {name: bytes}, each hash-checked"""
    b = fetch("https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip", os.path.join(CACHE, "ch22_materials.zip"), BROWSER)
    assert hashlib.sha256(b).hexdigest() == ZIPSHA, "the online materials differ from the zip the study recorded"
    z = zipfile.ZipFile(io.BytesIO(b)); out = {}
    for n in z.namelist():
        base = n.split("/")[-1]
        if base in FILESHA and "__MACOSX" not in n:
            out[base] = z.read(n); assert hashlib.sha256(out[base]).hexdigest() == FILESHA[base], base
    assert set(out) == set(FILESHA); return out
def pres():
    return [html.unescape(re.sub(r"<[^>]+>", "", p)) for p in re.findall(r"<pre[^>]*>(.*?)</pre>", chapter(), re.S)]
def depth(s):
    return sum(s.count(c) for c in "([{") - sum(s.count(c) for c in ")]}")
def parse_repl(text):
    """statements of an interactive listing: [(source, expected output)]. A line without a prompt that follows a statement whose brackets are still open belongs to the statement."""
    out = []; cur = None
    for raw in text.split("\n"):
        l = raw.rstrip()
        if cur is not None and not cur["out"] and depth("\n".join(cur["src"])) > 0 and not l.startswith(">>>"):
            cur["src"].append(l[4:] if l.startswith("... ") else l.lstrip("."))
        elif l.startswith(">>> ") or l == ">>>":
            cur = {"src": [l[4:]], "out": []}; out.append(cur)
        elif l.startswith("...") and cur is not None and not cur["out"]:
            cur["src"].append(l[4:] if l.startswith("... ") else l[3:])
        elif cur is not None: cur["out"].append(l)
    res = []
    for c in out:
        src = "\n".join(c["src"]).rstrip("\n"); exp = "\n".join(c["out"]).strip("\n")
        res.append((src, exp))
    return res
def groups():
    P = pres()
    L = {n: parse_repl(P[n - 1]) for n in (1, 2, 4, 5, 6, 7)}
    return P, L
TITLES = {1: "the four lines on ocr-example.png", 2: "the frankenstein.png listing", 4: "tess.get_languages()", 5: "the Japanese image with lang='jpn'", 6: "the Japanese image with lang='eng'", 7: "the NAPS2 call with subprocess.run()"}
REPAIRS = {(7, "naps2_path = "): ("naps2_path = [r'C:\\Program Files\\NAPS2\\NAPS2.Console.exe']  # Windows", "naps2_path = ['naps2', 'console']  # the .deb package of naps2.com on Linux")}
HARNESS = r'''import sys, os, io, json, re, tempfile, contextlib, time, hashlib, difflib, warnings, shutil, importlib.metadata as md
spec = json.load(open(os.environ['SPEC_FILE']))
os.chdir(tempfile.mkdtemp())
for n in spec['files']: shutil.copy(os.path.join(spec['dir'], n), n)
def norm(t): return re.sub(r'\s+', '', t)
def clean(t): return t.replace(os.getcwd(), 'DIR')
def lines(t): return [l.strip() for l in t.split('\n') if l.strip()]
def matches(got, exp):
    if '--snip--' in exp:
        head, tail = exp.split('--snip--', 1); g = norm(got)
        return g.startswith(norm(head)) and g.endswith(norm(tail))
    return norm(got) == norm(exp)
def differences(got, exp):
    """lines of the output that differ from the lines the book prints (the head before --snip-- against the first lines of the output, the tail against the last lines)"""
    gl = lines(got); out = []
    if '--snip--' in exp:
        head, tail = exp.split('--snip--', 1); hl, tl = lines(head), lines(tail)
        pairs = list(zip(gl[:len(hl)], hl)) + (list(zip(gl[-len(tl):], tl)) if tl else [])
    else: pairs = list(zip(gl, lines(exp)))
    for a, b in pairs:
        if norm(a) != norm(b): out.append({'got': a, 'book': b})
    return out[:8]
NS = {}; res = []
def run_stmt(src, n):
    buf = io.StringIO(); shown = []; old = sys.displayhook; sys.displayhook = lambda v: (shown.append(repr(v)) if v is not None else None)
    try:
        with contextlib.redirect_stdout(buf), warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            exec(compile(src.rstrip('\n') + '\n', '<listing %d>' % n, 'single'), NS)
        got = (buf.getvalue() + ''.join(s + '\n' for s in shown)).strip()
        return {'printed': clean(got)[:3500], 'chars': len(got), 'sha12': hashlib.sha256(got.encode()).hexdigest()[:12], 'raised': None, 'warnings': sorted({'%s: %s' % (x.category.__name__, str(x.message)[:90]) for x in w}), '_full': clean(got)}
    except BaseException as e:
        return {'printed': clean(buf.getvalue().strip())[:300], 'chars': 0, 'sha12': None, 'raised': clean('%s: %s' % (type(e).__name__, str(e).splitlines()[0][:150] if str(e) else '')), 'warnings': [], '_full': ''}
    finally: sys.displayhook = old
for n, title, stmts in spec['listings']:
    rows = []
    for src, exp, repaired in stmts:
        row = {'source': src}
        variants = (('as printed', src), ('repaired', repaired)) if not spec.get('use_repairs') else (('as printed', repaired or src),)
        if spec.get('use_repairs') and repaired: row['source replaced by'] = repaired
        for label, code in variants:
            if code is None: continue
            r = run_stmt(code, n); full = r.pop('_full'); r['matches the book'] = matches(full, exp) and r['raised'] is None
            if exp and r['raised'] is None and not r['matches the book']: r['differences from the book'] = differences(full, exp)
            row[label] = r
            if label == 'as printed' and r['raised'] is None: break
        row['book prints'] = exp[:300]; rows.append(row)
    res.append({'listing': n, 'what': title, 'statements': rows})
probes = {}
for e in spec.get('probe', []):
    try: probes[e] = repr(eval(e, NS))[:300]
    except BaseException as x: probes[e] = '%s: %s' % (type(x).__name__, str(x)[:100])
json.dump({'results': res, 'probes after the listings': probes}, open(os.environ['RESULT_FILE'], 'w'), default=repr, ensure_ascii=False)
'''
ENVINFO = r'''import sys, platform, importlib.metadata as md, json, shutil, subprocess, os
out = {'python': sys.version.split()[0]}
for n in ('pytesseract', 'pillow', 'numpy', 'opencv-python-headless', 'pyautogui', 'packaging'):
    try: out[n] = md.version(n)
    except md.PackageNotFoundError: out[n] = None
t = shutil.which('tesseract'); out['tesseract on the PATH'] = t
if t:
    r = subprocess.run([t, '--version'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True); out['tesseract --version'] = r.stdout.splitlines()[0]
print(json.dumps(out))'''
def env_for(engine, display=None, extra=None):
    e = dict(os.environ); e["PYTHONDONTWRITEBYTECODE"] = "1"
    eng, data = ENGINES[engine]
    if eng: e["PATH"] = eng + ":" + e["PATH"]
    if data: e["TESSDATA_PREFIX"] = data
    else: e.pop("TESSDATA_PREFIX", None)
    if display: e.update({"DISPLAY": display, "XDG_SESSION_TYPE": "x11", "XAUTHORITY": display_auth()})
    else: e.pop("DISPLAY", None)
    e.update(extra or {}); return e
def display_auth():
    p = os.path.join(tempfile.gettempdir(), "ch22_empty_Xauthority"); open(p, "a").close(); return p
class Xvfb:
    def __enter__(self):
        self.disp = ":%d" % (60 + os.getpid() % 30)
        self.p = subprocess.Popen(["Xvfb", self.disp, "-screen", "0", "1280x1024x24"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(3)
        return self.disp
    def __exit__(self, *a):
        subprocess.run(["pkill", "-x", "display-im6.q16"]); self.p.terminate(); self.p.wait()
def spec_file(spec):
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False); json.dump(spec, f); f.close(); return f.name
PROBE7 = ["proc.returncode", "__import__('os').path.exists('output.pdf')", "__import__('os').path.getsize('output.pdf') > 1000", "type(proc.stdout).__name__", "proc.stdout.decode().strip().splitlines()[-1]"]
def listings_spec(L, which, names, fdir, use_repairs=False):
    items = []
    for n in which:
        rows = []
        for src, exp in L[n]:
            rep = None
            for (ln, key), (a, b) in REPAIRS.items():
                if ln == n and src.startswith(key): rep = b
            rows.append([src, exp, rep])
        items.append([n, TITLES[n], rows])
    return {"listings": items, "files": names, "dir": fdir, "use_repairs": use_repairs, "probe": PROBE7 if 7 in which else []}
def run_harness(py, env, spec):
    """output in files, not pipes: a viewer or daemon started below keeps the pipes of its parent open"""
    env = dict(env); env["SPEC_FILE"] = spec_file(spec); res = tempfile.NamedTemporaryFile(suffix=".json", delete=False); res.close(); env["RESULT_FILE"] = res.name
    err = tempfile.NamedTemporaryFile(suffix=".err", delete=False)
    p = subprocess.Popen([py, "-W", "ignore::ResourceWarning", "-c", HARNESS], stdout=subprocess.DEVNULL, stderr=err, env=env, stdin=subprocess.DEVNULL)
    try: rc = p.wait(timeout=1200)
    except subprocess.TimeoutExpired: p.kill(); rc = -9
    if rc or not os.path.getsize(res.name): return {"harness failed": open(err.name).read().strip()[-400:]}
    return json.load(open(res.name))
def sh(py, code, env=None, timeout=300, cwd=None):
    r = subprocess.run([py, "-W", "ignore::ResourceWarning", "-c", code], capture_output=True, text=True, env=env or os.environ, timeout=timeout, stdin=subprocess.DEVNULL, cwd=cwd)
    return r.stdout.strip(), r.stderr.strip(), r.returncode
def record():
    items = []; P, L = groups(); mats = materials(); fdir = tempfile.mkdtemp(prefix="ch22files")
    for k, v in mats.items(): open(os.path.join(fdir, k), "wb").write(v)
    names = ["ocr-example.png", "frankenstein.png", "frankenstein_jpn.png"]
    n_statements = sum(len(v) for v in L.values())
    items.append({"what": "The rows of the study: interpreter, packages and the Tesseract on the PATH of each row", "output": {"%s / %s" % (n, e): json.loads(sh(p, ENVINFO, env_for(e))[0]) for n, p, e in ROWS}})
    items.append({"what": "The chapter page: %d listings found; 6 of them are interactive or code and replayed here statement by statement (%d statements), listing 3 is the text of a language model's answer and listing 8 is the template of a program" % (len(P), n_statements),
                  "output": {"listings": len(P), "replayed": sorted(L), "statements": n_statements, "figures": sorted(set(re.findall(r"Figure 22-\d", chapter()))), "sha256": hashlib.sha256(chapter().encode()).hexdigest()}})
    items.append({"what": "The files of the online materials the replay uses, and their sha256 (checked against the hashes the study recorded)", "output": {k: [hashlib.sha256(v).hexdigest(), len(v)] for k, v in mats.items()}})
    with Xvfb() as disp:
        for name, py, eng in ROWS:
            out = {"ocr": run_harness(py, env_for(eng), listings_spec(L, [1, 2, 4, 5, 6], names, fdir))}
            if name == "LATEST" and eng == "apt":
                out["naps2"] = run_harness(py, env_for(eng), listings_spec(L, [7], names, fdir))
                out["naps2 with the Linux path"] = run_harness(py, env_for(eng), listings_spec(L, [7], names, fdir, use_repairs=True))
            items.append({"what": "Replay as printed, row %s with Tesseract %s (listings 1, 2, 4, 5 and 6 in one shell session%s)" % (name, eng, ", listing 7 as printed and with the Linux path in two more" if "naps2" in out else ""), "output": out})
        # the inline claim: lang='eng+jpn'
        code = ("import pytesseract as tess\nfrom PIL import Image\nimg = Image.open('frankenstein_jpn.png')\nt = tess.image_to_string(img, lang='eng+jpn')\nl = [x for x in t.split('\\n') if x.strip()]\n"
                "import json; print(json.dumps({'lines': len(l), 'first': l[0], 'last': l[-1]}, ensure_ascii=False))")
        for eng in ("apt", "5.5.3-fast"):
            d = tempfile.mkdtemp(prefix="ch22eng"); shutil.copy(os.path.join(fdir, "frankenstein_jpn.png"), d)
            r = subprocess.run([LATEST, "-c", code], capture_output=True, text=True, cwd=d, env=env_for(eng), stdin=subprocess.DEVNULL)
            items.append({"what": "The inline claim that tess.image_to_string(img, lang='eng+jpn') recognizes both, row LATEST with Tesseract %s" % eng, "output": json.loads(r.stdout) if r.returncode == 0 else {"failed": r.stderr[-300:]}})
        # listing 8 as printed, with and without a display
        tmpl = P[7]; d = tempfile.mkdtemp(prefix="ch22tmpl"); open(os.path.join(d, "ocrscreen.py"), "w").write(tmpl)
        out = {}
        for label, env in (("with a virtual display", env_for("apt", disp)), ("without DISPLAY", env_for("apt"))):
            r = subprocess.run([LATEST, "-W", "ignore", "ocrscreen.py"], capture_output=True, text=True, cwd=d, env=env, stdin=subprocess.DEVNULL, timeout=120)
            out[label] = {"returncode": r.returncode, "stdout": [l for l in r.stdout.splitlines() if "xauth" not in l.lower()], "last line of stderr": (r.stderr.strip().splitlines() or [""])[-1][:140], "output.txt created": os.path.exists(os.path.join(d, "output.txt"))}
        items.append({"what": "Listing 8, the template of ocrscreen.py, run as printed (its TODO lines are comments, so it takes a screenshot and crops it and nothing more)", "output": out})
        # the shipped preprocessing file, as a program and as a module
        d = tempfile.mkdtemp(prefix="ch22pre"); open(os.path.join(d, "preprocess_ocr.py"), "wb").write(mats["preprocess_ocr.py"])
        out = {}
        compiled = sh(LATEST, "import sys\ntry:\n    compile(open('preprocess_ocr.py').read(), 'preprocess_ocr.py', 'exec'); print('compiles')\nexcept SyntaxError as e: print('SyntaxError', e.msg, e.lineno)", env_for("apt"), cwd=d)
        for label, py in (("LATEST (OpenCV 5.0.0.93 installed)", LATEST), ("BARE (no OpenCV)", BARE)):
            r = subprocess.run([py, "-W", "ignore", "preprocess_ocr.py"], capture_output=True, text=True, cwd=d, env=env_for("apt"), stdin=subprocess.DEVNULL)
            out[label] = {"returncode": r.returncode, "last line of stderr": (r.stderr.strip().splitlines() or [""])[-1][:140]}
        names_defined = sh(LATEST, "import re\ns = open('preprocess_ocr.py').read()\nd = set(re.findall(r'^def (\\w+)', s, re.M)); u = set(re.findall(r'\\b(grayscale_image|open_image|open_cv2_image|save_cv2_image|FileNotFileError)\\b', s))\nprint(sorted(d)); print(sorted(u - d))", env_for("apt"), cwd=d)[0]
        items.append({"what": "preprocess_ocr.py of the online materials (the OpenCV helpers the chapter points to): does it compile, and what happens when it is run", "output": {"compile": compiled[0], "run": out, "functions defined and names used but never defined": names_defined.splitlines()}})
    return items
def digest(it):
    t = json.dumps(it, sort_keys=True, ensure_ascii=False)
    for a, b in ((r"0x[0-9a-f]{6,}", "0xADDR"), (r"subprocess \d+", "subprocess PID"), (r"tess_\w+", "tess_X"), (r"/tmp/tmp[0-9a-z_]{8}", "/tmp/tmpDIR")): t = re.sub(a, b, t)
    return t
if __name__ == "__main__":
    if MODE == "write":
        items = record()
        json.dump({"_version": __version__, "_note": "Recorded by sen0414_ch22_thirdparty_v1_0_0.py write; every output was printed by the program beside it under the interpreter and Tesseract named in the item, on a machine in the zone Europe/Istanbul. The chapter page and the online materials are fetched at run time and not kept in the repository. The Windows, macOS and Flatpak parts of the chapter were not executed; the NAPS2 call ran with the .deb package of NAPS2 8.5.1 for Linux.",
                   "python": "3.14.6 (LATEST, PINS, BARE) and 3.13.14 (PINS313)", "items": items}, open(REC, "w"), indent=1, ensure_ascii=False)
        n = 0
        for i in items:
            o = i["output"]
            if isinstance(o, dict):
                for g in o.values():
                    if isinstance(g, dict) and "results" in g: n += sum(len(l["statements"]) for l in g["results"])
        print("recorded", len(items), "items,", n, "statement runs ->", REC)
    else:
        old = json.load(open(REC))["items"]; new = record(); bad = [i for i, (a, b) in enumerate(zip(old, new)) if digest(a["output"]) != digest(b["output"])]
        print("items checked:", len(new), "differences:", bad); sys.exit(1 if bad else 0)

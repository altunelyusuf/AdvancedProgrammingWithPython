#!/usr/bin/env python3
"""Chapter 21 (Making Graphs and Manipulating Images): runs the chapter's own listings, whole and as printed, under the given interpreter, and writes or
checks their recorded output.
What is fetched at run time and kept in a cache directory (CH21_CACHE, default the system temp directory): the chapter page
(https://automatetheboringstuff.com/3e/chapter21.html; its sha256 is compared with the chapterDigest of the book's own chapter ontology, cb9e204b...a28) and the
online materials of the 3rd edition (the zip that No Starch Press links from its book page, sha256 dac627e8...916), from which zophie.png, catlogo.png and
guests.txt are taken and hash-checked. Nothing of either is stored in the repository.
The listings are not typed in here: every REPL listing is parsed from the page itself (the prompt lines, the continuation lines and the printed output that follows
them; the callout numbers of the typesetting are removed with the one space that follows them) and every statement is run in the order of the book, in one shell
session per group, as printed. The program of Project 16 is assembled from the four fragments of the book (Steps 1 to 4, which print --snip-- between them).
Environments, all Python 3.14.6 installed with uv, named by environment variables:
  LATEST  the newest releases on 2026-10-13: Pillow 12.3.0, Matplotlib 3.11.2, NumPy 2.5.4, pyperclipimg 0.2.0
  PINS    the versions Appendix A of the book pins: Pillow 10.4.0 and the Matplotlib that the book writes as 3.92 (no such release exists; 3.9.2, the evident
          intention, is installed instead); pyperclipimg is not pinned and is not installed in this environment
  PINS313 the same two pinned versions (Pillow 10.4.0, Matplotlib 3.9.2) under Python 3.13.14, the newest interpreter for which both have wheels, because under 3.14.6
          the pinned Matplotlib raises RecursionError in its first savefig() (see the PINS record); it is the way to see what the book's own versions print
  BARE    no package at all, to see what a reader gets who has installed nothing
named by CH21_LATEST, CH21_PINS, CH21_PINS13 and CH21_BARE (paths of their python), defaults /home/claude/venv31{4,4,3,4}_ch21_{latest,pins,pins,bare}/bin/python.
Two modes: HEADLESS (no DISPLAY and a PATH without any picture viewer, so what a server or a container gives) and DISPLAY (a virtual X server, Xvfb, started
here on its own display number, with xdg-open, ImageMagick's display and xclip on the PATH; Matplotlib then uses the TkAgg backend, and each window that
plt.show() opens is closed 0.6 seconds after it opened by a timer, which is what a reader's click on the close button does). A virtual screen is not a monitor,
but the windows, the viewer process and the clipboard are the real ones.
Not executed: Windows and macOS (the Windows folder of listing 4, the black fill of a rotation on Windows, the Quartz and pywin32 clipboard code), a physical screen.
Usage: sen0414_ch21_thirdparty_v1_0_0.py write|check [python]   (python defaults to the LATEST environment)
Record: 08-tooling/ch21-page/third_party_record_v1_0_0.json"""
__version__ = "1.0.0"
import hashlib, html, io, json, os, re, shutil, subprocess, sys, tempfile, time, urllib.request, zipfile
MODE = sys.argv[1] if len(sys.argv) > 1 else "check"
LATEST = os.environ.get("CH21_LATEST", "/home/claude/venv314_ch21_latest/bin/python")
PINS = os.environ.get("CH21_PINS", "/home/claude/venv314_ch21_pins/bin/python")
BARE = os.environ.get("CH21_BARE", "/home/claude/venv314_ch21_bare/bin/python")
PINS13 = os.environ.get("CH21_PINS13", "/home/claude/venv313_ch21_pins/bin/python")
PY = sys.argv[2] if len(sys.argv) > 2 else LATEST
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REC = os.path.join(REPO, "08-tooling", "ch21-page", "third_party_record_v1_0_0.json")
CACHE = os.environ.get("CH21_CACHE") or tempfile.gettempdir()
DIGEST = "cb9e204bc3d3455abe51f81c96b6360f01491635805b5bea65e93643cb186a28"
ZIPSHA = "dac627e807f69ee14913ba621a15dec1f98db739d76939555ba5360d05eba916"
FILESHA = {"zophie.png": "5c5bf02fd0c95cee5d490a6daf3f1c4ccbbcab9fdc59bd8bba9564cad1462ba1", "catlogo.png": "107740e7ca46ce7642b6940ff1232689bc3d34eb14c026813a61cfae45385db0",
           "guests.txt": "e6136e39f829ae7380be4969b780c72bd8022a1a97efc399f0f2002ce1fd5164", "resizeAndAddLogo.py": "4291c7cedd9dcf37b792ee7c20485902ad746b2743f66873ccc953bf4681634a"}
UA = {"User-Agent": "SEN0414-research/1.0 (academic course; altunel.yusuf@gmail.com)"}
BROWSER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0"}
def fetch(url, path, headers):
    if not os.path.exists(path):
        open(path + ".part", "wb").write(urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=180).read()); os.replace(path + ".part", path)
    return open(path, "rb").read()
def chapter():
    b = fetch("https://automatetheboringstuff.com/3e/chapter21.html", os.path.join(CACHE, "ch21_chapter.html"), UA)
    assert hashlib.sha256(b).hexdigest() == DIGEST, "the chapter page differs from the one the study recorded"
    return b.decode("utf-8")
def materials():
    """the files of the online materials the replay needs, as {name: bytes}, each hash-checked"""
    b = fetch("https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip", os.path.join(CACHE, "ch21_materials.zip"), BROWSER)
    assert hashlib.sha256(b).hexdigest() == ZIPSHA, "the online materials differ from the zip the study recorded"
    z = zipfile.ZipFile(io.BytesIO(b)); out = {}
    for n in z.namelist():
        base = n.split("/")[-1]
        if base in FILESHA and "__MACOSX" not in n:
            out[base] = z.read(n); assert hashlib.sha256(out[base]).hexdigest() == FILESHA[base], base
    assert set(out) == set(FILESHA); return out
def pres():
    return [html.unescape(re.sub(r"<[^>]+>", "", p)) for p in re.findall(r"<pre[^>]*>(.*?)</pre>", chapter(), re.S)]
def clean(l):
    """removes the callout numbers of the typesetting. A callout at the start of a line goes with the space after it; a callout that stands after the indentation of a
    line takes the place of two columns of that indentation (the typesetter put the number into the margin of the indented code), so it is replaced by two spaces; a
    callout at the end of a line goes with the space before it"""
    l = re.sub(r" ?[\u2776-\u277f]$", "", l)
    m = re.match(r"^((?:\.\.\.|>>>)?)(\s*)[\u2776-\u277f] ?", l)
    if m: l = m.group(1) + m.group(2) + ("  " if (m.group(1) or m.group(2)) else "") + l[m.end():]
    l = re.sub(r"[\u2776-\u277f] ?", "", l)
    return l.rstrip()
def parse_repl(text):
    """statements of an interactive listing: [(source, expected output)]"""
    out = []; cur = None
    for raw in text.split("\n"):
        l = clean(raw)
        if l.startswith(">>> ") or l == ">>>":
            cur = {"src": [l[4:]], "out": []}; out.append(cur)
        elif l.startswith("...") and cur is not None and not cur["out"]:
            cur["src"].append(l[4:] if l.startswith("... ") else l[3:])
        elif cur is not None: cur["out"].append(l)
    res = []
    for c in out:
        src = "\n".join(c["src"]).rstrip("\n"); exp = "\n".join(c["out"]).strip("\n")
        if src.strip().startswith("#"): continue           # a statement that is only a comment
        res.append((src, exp))
    return res
def assembled(P):
    """the program of Project 16 from the four fragments (listings 16 to 19 of the page, numbered 1 to 31): Step 1 up to the logo size, Step 2 from os.makedirs,
    Step 3 and Step 4 from their first comment; each fragment is cut at its --snip-- lines"""
    def body(n):
        return [clean(l) for l in P[n - 1].split("\n")]
    s1, s2, s3, s4 = body(16), body(17), body(18), body(19)
    i = next(k for k, l in enumerate(s1) if l.startswith("# TODO: Loop"))
    part1 = s1[:i]
    j = next(k for k, l in enumerate(s2) if l.startswith("os.makedirs")); k2 = max(k for k, l in enumerate(s2) if l.strip() == "--snip--")
    part2 = s2[j:k2]
    j = next(k for k, l in enumerate(s3) if l.strip().startswith("# Check if the image needs")); k3 = max(k for k, l in enumerate(s3) if l.strip() == "--snip--")
    part3 = s3[j:k3]
    j = next(k for k, l in enumerate(s4) if l.strip().startswith("# Add the logo")); part4 = [l for l in s4[j:] if l.strip()]
    lines = part1 + [""] + part2 + part3 + part4
    return "\n".join(l for l in lines if not (l.strip() == "" and False)).rstrip("\n") + "\n"
def groups():
    """the groups the harness runs, each in one process: REPL listings of the Pillow part, of the Matplotlib part, the assembled program, the skeleton"""
    P = pres(); L = {}
    for n in list(range(1, 16)) + list(range(21, 31)):
        L[n] = parse_repl(P[n - 1])
    prog = assembled(P)
    return P, L, prog
TITLES = {1: "ImageColor.getcolor() and the colour names", 2: "list(ImageColor.colormap)", 3: "Image.open() and show()", 4: "os.chdir() to a Windows folder", 5: "size, filename, format, save to .jpg",
          6: "Image.new() and save()", 7: "crop()", 8: "copy()", 9: "paste() of a crop", 10: "the nested loops that tile the face", 11: "resize()", 12: "rotate() by 90, 180 and 270",
          13: "rotate(6) with and without expand", 14: "transpose() with the FLIP constants", 15: "getpixel() and putpixel()", 21: "ImageDraw.Draw()", 22: "the drawing example",
          23: "from PIL import ImageFont", 24: "text() and truetype('arial.ttf')", 25: "pyperclipimg.copy() and paste()", 26: "plt.plot(), savefig() and show()",
          27: "plt.scatter()", 28: "plt.bar()", 29: "plt.pie()", 30: "marker, color, label, legend, labels, title and grid"}
GROUPS = {"pillow": list(range(1, 16)) + list(range(21, 26)), "matplotlib": list(range(26, 31))}
REPAIRS = {(24, "arial.ttf"): ("arial.ttf", "DejaVuSans.ttf"), (14, "FLIP_LEFT_RIGHT"): ("Image.FLIP_LEFT_RIGHT", "Image.Transpose.FLIP_LEFT_RIGHT"),
           (14, "FLIP_TOP_BOTTOM"): ("Image.FLIP_TOP_BOTTOM", "Image.Transpose.FLIP_TOP_BOTTOM")}

HARNESS = r'''import sys, os, io, json, re, tempfile, contextlib, time, hashlib, warnings, importlib.metadata as md
spec = json.load(open(os.environ['SPEC_FILE'])); MODE = os.environ['REPLAY_MODE']; SHOW = MODE == 'display'
os.chdir(tempfile.mkdtemp())
import shutil
for n in spec['files']: shutil.copy(os.path.join(spec['dir'], n), n)
def norm(t): return re.sub(r'\s+', '', re.sub(r'0x[0-9A-Fa-f]+', '0xADDR', t))
CWD = os.getcwd()
def clean(t): return t.replace(CWD, 'DIR')
keep = []
try:
    import matplotlib.pyplot as _plt
    _orig = _plt.show
    def _show(*a, **k):
        t0 = time.time(); before = list(_plt.get_fignums())
        if SHOW:
            for n in before:
                f = _plt.figure(n); tm = f.canvas.new_timer(interval=600); tm.add_callback(lambda f=f: _plt.close(f)); tm.start(); keep.append(tm)
        r = _orig(*a, **k)
        note.append({'plt.show': {'figures open before': before, 'returned': repr(r), 'figures open after': list(_plt.get_fignums()), 'blocked for at least half a second': (time.time() - t0) >= 0.5}})
        return r
    _plt.show = _show
except Exception: pass
note = []
def run_stmt(src, n, label):
    buf = io.StringIO(); shown = []; old = sys.displayhook; sys.displayhook = lambda v: (shown.append(repr(v)) if v is not None else None)
    try:
        with contextlib.redirect_stdout(buf), warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            exec(compile(src.rstrip('\n') + '\n', '<listing %d>' % n, 'single'), NS)
        got = (buf.getvalue() + ''.join(s + '\n' for s in shown)).strip()
        return {'printed': clean(got)[:500], 'full': clean(got), 'raised': None, 'warnings': sorted({'%s: %s' % (x.category.__name__, str(x.message)[:90]) for x in w})}
    except BaseException as e:
        return {'printed': clean((buf.getvalue() + ''.join(s + '\n' for s in shown)).strip())[:300], 'full': '', 'raised': clean('%s: %s' % (type(e).__name__, str(e).splitlines()[0][:140] if str(e) else '')), 'warnings': []}
    finally: sys.displayhook = old
def matches(got, exp):
    if '--snip--' in exp:
        head, tail = exp.split('--snip--', 1); head = norm(head); tail = norm(tail); g = norm(got)
        return g.startswith(head) and g.endswith(tail)
    if ' ... ' in exp:
        head, tail = exp.split(' ... ', 1); g = norm(got); return g.startswith(norm(head)) and g.endswith(norm(tail))
    return norm(got) == norm(exp)
NS = {}
res = []
for n, title, stmts in spec['listings']:
    rows = []
    for src, exp, repaired in stmts:
        note.clear(); row = {'source': src}
        for label, code in (('as printed', src), ('repaired', repaired)):
            if code is None: continue
            r = run_stmt(code, n, label); r['matches the book'] = matches(r.pop('full'), exp) and r['raised'] is None; row[label] = r
            if note: r['observed'] = list(note)
            if 'savefig' in code:
                try:
                    import matplotlib.pyplot as plt; ax = plt.gcf().axes[0]; r['axes at the moment of saving'] = {'lines': len(ax.lines), 'collections': len(ax.collections), 'patches': len(ax.patches)}
                except Exception as e: r['axes at the moment of saving'] = type(e).__name__
            if label == 'as printed' and r['raised'] is None: break
        row['book prints'] = exp[:300]; rows.append(row)
    res.append({'listing': n, 'what': title, 'statements': rows})
files = {}
if spec.get('inspect'):
    try:
        from PIL import Image
        for f in sorted(os.listdir('.')):
            if f.lower().endswith(('.png', '.jpg')) and f not in spec['files']:
                try:
                    im = Image.open(f); files[f] = [im.format, im.mode, list(im.size), os.path.getsize(f)]
                except Exception as e: files[f] = type(e).__name__
    except ImportError: files = 'Pillow is not installed'
json.dump({'results': res, 'files written': files}, open(os.environ['RESULT_FILE'], 'w'), default=repr)
'''
PROG_HARNESS = r'''import sys, os, io, json, re, tempfile, contextlib, subprocess
spec = json.load(open(os.environ['SPEC_FILE']))
d = tempfile.mkdtemp(); os.chdir(d)
import shutil
for n in spec['files']: shutil.copy(os.path.join(spec['dir'], n), n)
out = {}
for label, src in spec['programs']:
    for f in os.listdir('.'):
        if os.path.isdir(f): __import__('shutil').rmtree(f)
    try: compile(src, '<resizeAndAddLogo>', 'exec'); ok = None
    except SyntaxError as e: ok = '%s: %s (line %s)' % (type(e).__name__, e.msg, e.lineno)
    row = {'compiles': ok is None, 'compile error': ok}
    if ok is None:
        r = subprocess.run([sys.executable, '-c', src], capture_output=True, text=True, cwd=d)
        row['exit'] = r.returncode; row['stdout'] = sorted(r.stdout.strip().splitlines()); row['stderr'] = r.stderr.strip().splitlines()[-1:] if r.stderr else []
        if os.path.isdir('withLogo'):
            from PIL import Image
            row['withLogo'] = {f: [list(Image.open('withLogo/' + f).size), Image.open('withLogo/' + f).mode] for f in sorted(os.listdir('withLogo'))}
    out[label] = row
print(json.dumps(out))
'''
ENVINFO = r'''import sys, platform, importlib.metadata as md, json
out = {'python': sys.version.split()[0], 'platform': platform.platform()}
for n in ('pillow', 'matplotlib', 'numpy', 'pyperclipimg', 'contourpy', 'fonttools', 'kiwisolver', 'cycler', 'pyparsing', 'python-dateutil', 'packaging'):
    try: out[n] = md.version(n)
    except md.PackageNotFoundError: out[n] = None
try:
    from PIL import features
    out['Pillow features'] = {k: features.version(k) for k in ('freetype2', 'jpg', 'zlib', 'raqm', 'libpng', 'webp', 'lcms2')}
except Exception as e: out['Pillow features'] = type(e).__name__
try:
    import matplotlib; out['matplotlib backend with no display'] = matplotlib.get_backend()
except Exception as e: out['matplotlib backend with no display'] = type(e).__name__
print(json.dumps(out))'''
def sh(py, code, env=None, timeout=600):
    e = dict(os.environ); e.update(env or {})
    r = subprocess.run([py, "-W", "ignore::ResourceWarning", "-c", code], capture_output=True, text=True, env=e, timeout=timeout)
    return r.stdout.strip(), r.stderr.strip(), r.returncode
def scratch_bin():
    """a PATH for the headless mode: only xclip and xsel (the clipboard programs), no viewer"""
    d = tempfile.mkdtemp(prefix="ch21bin")
    for p in ("xclip", "xsel", "xvfb-run"):
        w = shutil.which(p)
        if w and p != "xvfb-run": os.symlink(w, os.path.join(d, p))
    return d
class Xvfb:
    def __enter__(self):
        self.disp = ":%d" % (60 + os.getpid() % 30)
        self.p = subprocess.Popen(["Xvfb", self.disp, "-screen", "0", "1280x1024x24"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(3)
        return self.disp
    def __exit__(self, *a):
        subprocess.run(["pkill", "-x", "display-im6.q16"]); self.p.terminate(); self.p.wait()
def env_for(mode, disp=None):
    """the environment of a harness process: HEADLESS has no DISPLAY, no MPLBACKEND and a PATH with only the clipboard programs; DISPLAY has the virtual display and TkAgg"""
    e = dict(os.environ); e["PYTHONDONTWRITEBYTECODE"] = "1"; e["REPLAY_MODE"] = mode
    if mode == "headless":
        e.pop("DISPLAY", None); e.pop("MPLBACKEND", None); e["PATH"] = scratch_bin()
    else:
        e["DISPLAY"] = disp; e["MPLBACKEND"] = "TkAgg"
    return e
def run_harness(py, mode, disp, spec):
    """runs the harness with its output in files, not pipes, because a viewer that Image.show() starts keeps the pipes of its parent open after the harness has ended"""
    env = env_for(mode, disp); env["SPEC_FILE"] = spec_file(spec); res = tempfile.NamedTemporaryFile(suffix=".json", delete=False); res.close(); env["RESULT_FILE"] = res.name
    err = tempfile.NamedTemporaryFile(suffix=".err", delete=False)
    p = subprocess.Popen([py, "-W", "ignore::ResourceWarning", "-c", HARNESS], stdout=subprocess.DEVNULL, stderr=err, env=env)
    try: rc = p.wait(timeout=900)
    except subprocess.TimeoutExpired: p.kill(); rc = -9
    subprocess.run(["pkill", "-x", "display-im6.q16"])
    if rc or not os.path.getsize(res.name): return {"harness failed": open(err.name).read().strip()[-400:]}
    return json.load(open(res.name))
def spec_file(spec):
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False); json.dump(spec, f); f.close(); return f.name
def listings_spec(L, which, files_hex, inspect):
    items = []
    for n in which:
        rows = []
        for src, exp in L[n]:
            rep = None
            for (ln, key), (a, b) in REPAIRS.items():
                if ln == n and key in src and a in src: rep = src.replace(a, b)
            rows.append([src, exp, rep])
        items.append([n, TITLES[n], rows])
    return {"listings": items, "files": files_hex["names"], "dir": files_hex["dir"], "inspect": inspect}
def summarise(rep):
    rows = []
    for g, r in rep.items():
        if "results" not in r: rows.append([g, r]); continue
        for l in r["results"]:
            for s in l["statements"]:
                for k in ("as printed", "repaired"):
                    if k in s: rows.append([l["listing"], s["source"][:90], k, s[k]["matches the book"], s[k]["raised"]])
    return rows
def record():
    items = []; P, L, prog = groups(); mats = materials()
    fdir = tempfile.mkdtemp(prefix="ch21files")
    for k in ("zophie.png", "catlogo.png"): open(os.path.join(fdir, k), "wb").write(mats[k])
    files_hex = {"names": ["zophie.png", "catlogo.png"], "dir": fdir}
    n_statements = sum(len(v) for v in L.values())
    items.append({"what": "The environments: interpreter, packages and their versions in the four environments of the study", "output": {n: json.loads(sh(p, ENVINFO)[0]) for n, p in (("LATEST", LATEST), ("PINS", PINS), ("PINS313", PINS13), ("BARE", BARE))}})
    items.append({"what": "The chapter page: %d listings found; %d of them are interactive and replayed here statement by statement (%d statements); the program of Project 16 is assembled from 4 fragments; the skeleton of the last practice program is run as printed" % (len(P), len(L), n_statements),
                  "output": [len(P), len(L), n_statements]})
    fixed = {"zophie.png": hashlib.sha256(mats["zophie.png"]).hexdigest(), "catlogo.png": hashlib.sha256(mats["catlogo.png"]).hexdigest()}
    items.append({"what": "The files of the online materials the replay uses, and their sha256 (checked against the hashes the study recorded)", "output": fixed})
    skeleton_src = "\n".join(clean(l) for l in P[30].split("\n"))
    prog_printed = prog; prog_fixed = prog.replace("–", "-")
    shipped = mats["resizeAndAddLogo.py"].decode()
    with Xvfb() as disp:
        for env_name, p in (("LATEST", LATEST), ("PINS", PINS), ("PINS313", PINS13), ("BARE", BARE)):
            for mode in ("headless", "display"):
                if env_name == "BARE" and mode == "display": continue
                out = {}
                for gname, which in GROUPS.items():
                    out[gname] = run_harness(p, mode, disp, listings_spec(L, which, files_hex, gname == "pillow"))
                items.append({"what": "Replay as printed, environment %s, mode %s (groups: the Pillow listings 1-15 and 21-25 in one shell session, the Matplotlib listings 26-30 in another)" % (env_name, mode), "output": out})
        prog_files = files_hex
        for env_name, p in (("LATEST", LATEST), ("PINS", PINS), ("PINS313", PINS13)):
            spec = {"files": prog_files["names"], "dir": prog_files["dir"], "programs": [["the program as the book prints it (steps 1 to 4 joined)", prog_printed], ["the same with the en dash of listing 19 written as a minus sign", prog_fixed], ["the file resizeAndAddLogo.py of the online materials", shipped]]}
            so, se, rc = sh(p, PROG_HARNESS, {"SPEC_FILE": spec_file(spec), "PYTHONDONTWRITEBYTECODE": "1"})
            items.append({"what": "Project 16 run in a folder that holds zophie.png and catlogo.png, environment %s" % env_name, "output": json.loads(so.splitlines()[-1]) if rc == 0 else {"failed": se[-300:]}})
        spec = {"files": prog_files["names"], "dir": prog_files["dir"], "programs": [["the skeleton of the last practice program as printed", skeleton_src]]}
        so, se, rc = sh(LATEST, PROG_HARNESS, {"SPEC_FILE": spec_file(spec), "PYTHONDONTWRITEBYTECODE": "1"})
        items.append({"what": "The skeleton of the last practice program, run as printed (environment LATEST)", "output": json.loads(so.splitlines()[-1]) if rc == 0 else {"failed": se[-300:]}})
    items.append({"what": "The assembled program of Project 16 as the book prints it, and the first characters of the line the en dash is in (to show the code point)", "output": [prog_printed, [ (l, [hex(ord(c)) for c in l if ord(c) > 127]) for l in prog_printed.splitlines() if any(ord(c) > 127 for c in l)]]})
    return items
def digest(it):
    import re  # memory addresses and process numbers and temporary folder names change on every run and are not behaviour
    return re.sub(r"/tmp/tmp[0-9a-z_]{8}", "/tmp/tmpDIR", re.sub(r"subprocess \d+", "subprocess PID", re.sub(r"0x[0-9a-f]{6,}", "0xADDR", json.dumps(it, sort_keys=True))))
if MODE == "write":
    items = record()
    json.dump({"_version": __version__, "_note": "Recorded by sen0414_ch21_thirdparty_v1_0_0.py write; every output was printed by the program beside it under the interpreter named in the item, on a machine in the zone Europe/Istanbul. The chapter page and the online materials are fetched at run time and not kept in the repository. The Matplotlib that the book pins as 3.92 does not exist; the PINS environment holds 3.9.2. Listings that open a window ran against a virtual X display (Xvfb) with real viewer, clipboard and Tk windows; nothing ran on Windows or macOS.", "python": "3.14.6; Pillow 12.3.0 and Matplotlib 3.11.2 (LATEST); Pillow 10.4.0 and Matplotlib 3.9.2 (PINS, and PINS313 under Python 3.13.14)", "items": items}, open(REC, "w"), indent=1, ensure_ascii=False)
    n = sum(len(summarise(i["output"])) for i in items if isinstance(i["output"], dict) and "pillow" in i["output"])
    print("recorded", len(items), "items,", n, "statement runs ->", REC)
else:
    old = json.load(open(REC))["items"]; new = record(); bad = [i for i, (a, b) in enumerate(zip(old, new)) if digest(a["output"]) != digest(b["output"])]
    print("items checked:", len(new), "differences:", bad); sys.exit(1 if bad else 0)

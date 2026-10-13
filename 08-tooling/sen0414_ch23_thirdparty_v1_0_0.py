#!/usr/bin/env python3
"""Chapter 23 (Controlling the Keyboard and Mouse): runs the chapter's own listings, whole and as printed, under the given interpreters and package sets on a private virtual X display
(Xvfb with the openbox window manager; two real Tk windows stand in for the file editor and for the Submit button; NOT a real screen), and writes or checks their recorded output.
What is fetched at run time and kept in a cache directory (CH23_CACHE, default the system temp directory): the chapter page (https://automatetheboringstuff.com/3e/chapter23.html; its
sha256 is compared with the chapterDigest of the book's own chapter ontology, 7b31e433...1fd7). Nothing of it is stored in the repository.
The listings are not typed in here: every listing is parsed from the page itself (the prompt lines, the continuation lines and the printed output that follows them; the numbered
call-out marks of the typesetting are dropped) and every statement is run in the order of the book, in one session, as printed. The page has 25 listings: 21 interactive sessions or
one-line calls, 2 programs (spiralDraw.py and the try statement, run as code) and 2 groups of plain statements (the four keyDown/keyUp lines and the hotkey line, run line by line). pyautogui.mouseInfo() blocks until its window is closed, so it runs in a child process for 4 seconds and is then stopped.
Rows of the record (Python 3.14.6 unless named, installed with uv; the packages of each row are named in the record):
  LATEST       PyAutoGUI 0.9.54, PyScreeze 1.0.1, Pillow 12.3.0, NumPy 2.5.4, OpenCV 5.0.0.93 (Tk 9.0.3): /home/claude/venv314_ch23_latest
  NOCV         the same without NumPy and OpenCV: /home/claude/venv314_ch23_nocv
  OLDSCREEZE   PyScreeze 0.1.28 (the release before the exception became the default) with PyAutoGUI 0.9.54: /home/claude/venv314_ch23_oldscreeze
  TK86         Python 3.12.3 of Ubuntu with Tk 8.6.14, PyAutoGUI 0.9.54: /home/claude/venv312_ch23_tk86
  BARE         no package at all: /home/claude/venv314_ch23_bare
Not executed: Windows, macOS, a real screen, a physical mouse or keyboard, more than one monitor, Wayland, an application that blocks synthetic input beyond the xterm default, Paint and Mu.
Usage: sen0414_ch23_thirdparty_v1_0_0.py write|check
Record: 08-tooling/ch23-page/third_party_record_v1_0_0.json"""
__version__ = "1.0.0"
import hashlib, html, json, os, re, subprocess, sys, tempfile, time, urllib.request
MODE = sys.argv[1] if len(sys.argv) > 1 else "check"
HOME = "/home/claude"
ROWS = [("LATEST", os.environ.get("CH23_LATEST", HOME + "/venv314_ch23_latest/bin/python")), ("NOCV", os.environ.get("CH23_NOCV", HOME + "/venv314_ch23_nocv/bin/python")),
        ("OLDSCREEZE", os.environ.get("CH23_OLDSCREEZE", HOME + "/venv314_ch23_oldscreeze/bin/python")), ("TK86", os.environ.get("CH23_TK86", HOME + "/venv312_ch23_tk86/bin/python")),
        ("BARE", os.environ.get("CH23_BARE", HOME + "/venv314_ch23_bare/bin/python"))]
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REC = os.path.join(REPO, "08-tooling", "ch23-page", "third_party_record_v1_0_0.json")
CACHE = os.environ.get("CH23_CACHE") or tempfile.gettempdir()
DIGEST = "7b31e4333cd9784edea41303bf20b13b6a091198a43450542881eb3715f71fd7"
UA = {"User-Agent": "SEN0414-research/1.0 (academic course; altunel.yusuf@gmail.com)"}
def chapter():
    p = os.path.join(CACHE, "ch23_chapter.html")
    if not os.path.exists(p):
        open(p + ".part", "wb").write(urllib.request.urlopen(urllib.request.Request("https://automatetheboringstuff.com/3e/chapter23.html", headers=UA), timeout=120).read()); os.replace(p + ".part", p)
    b = open(p, "rb").read(); assert hashlib.sha256(b).hexdigest() == DIGEST, "the chapter page differs from the one the study recorded"
    return b.decode("utf-8")
def pres(): return [html.unescape(re.sub(r"<[^>]+>", "", p)) for p in re.findall(r"<pre[^>]*>(.*?)</pre>", chapter(), re.S)]
def depth(s): return sum(s.count(c) for c in "([{") - sum(s.count(c) for c in ")]}")
def clean(t): return re.sub(r"[❶-❿] ?", "", t)
def parse_repl(text):
    """statements of an interactive listing: [(source, expected output)]. A line without a prompt that follows a statement whose brackets are still open belongs to the statement."""
    out = []; cur = None
    for raw in clean(text).split("\n"):
        l = raw.rstrip()
        if cur is not None and not cur["out"] and depth("\n".join(cur["src"])) > 0 and not l.startswith(">>>"):
            cur["src"].append(l[4:] if l.startswith("... ") else l.lstrip("."))
        elif l.startswith(">>> ") or l == ">>>": cur = {"src": [l[4:]], "out": []}; out.append(cur)
        elif l.startswith("...") and cur is not None and not cur["out"]: cur["src"].append(l[4:] if l.startswith("... ") else l[3:])
        elif cur is not None: cur["out"].append(l)
    return [("\n".join(c["src"]).rstrip("\n"), "\n".join(c["out"]).strip("\n")) for c in out]
def listings():
    """[(number, title, kind, [(source, expected output)])] for the 25 listings of the page"""
    P = pres(); res = []
    for n, p in enumerate(P, 1):
        first = [l for l in clean(p).split("\n") if l.strip()][0]
        if first.startswith(">>>"): res.append((n, "listing %d" % n, "repl", parse_repl(p)))
        elif n in (23, 24): res.append((n, "listing %d" % n, "statements", [(l, "") for l in clean(p).strip().split("\n")]))
        else: res.append((n, "listing %d" % n, "program", [(clean(p).strip("\n"), "")]))
    return res
HARNESS = r"""import os, sys, contextlib
os.environ['CH23_LATEST'] = sys.executable
import io, os, sys, re, json, time, shutil, signal, tempfile, warnings, subprocess, importlib.metadata as md
warnings.simplefilter('ignore')
LATEST = os.environ.get('CH23_LATEST', '/home/claude/venv314_ch23_latest/bin/python')
NOCV = os.environ.get('CH23_NOCV', '/home/claude/venv314_ch23_nocv/bin/python')
TK86 = os.environ.get('CH23_TK86', '/home/claude/venv312_ch23_tk86/bin/python')
OLDSCREEZE = os.environ.get('CH23_OLDSCREEZE', '/home/claude/venv314_ch23_oldscreeze/bin/python')
OBSERVER = r'''
import sys, os, json, time, tkinter as tk
cfg = json.loads(sys.argv[1]); log = open(cfg['log'], 'a', buffering=1)
root = tk.Tk(); root.title(cfg.get('title', 'observer')); root.geometry(cfg.get('geometry', '600x400+100+100'))
if cfg.get('scaling'): root.tk.call('tk', 'scaling', cfg['scaling'])
mode = cfg.get('mode', 'events')
def q(v): return None if v == '??' else v
def put(e, kind):
    s = getattr(e, 'state', 0)
    log.write(json.dumps({'t': time.time(), 'type': kind, 'x': q(getattr(e, 'x', None)), 'y': q(getattr(e, 'y', None)), 'x_root': q(getattr(e, 'x_root', None)), 'y_root': q(getattr(e, 'y_root', None)),
         'num': q(getattr(e, 'num', None)), 'delta': q(getattr(e, 'delta', None)), 'keysym': q(getattr(e, 'keysym', None)), 'char': q(getattr(e, 'char', None)),
         'state': s if isinstance(s, int) else str(s), 'send_event': bool(getattr(e, 'send_event', False))}) + '\n')
for ev, kind in (('<Motion>', 'Motion'), ('<ButtonPress>', 'ButtonPress'), ('<ButtonRelease>', 'ButtonRelease'), ('<MouseWheel>', 'MouseWheel'), ('<KeyPress>', 'KeyPress'), ('<KeyRelease>', 'KeyRelease'), ('<Double-ButtonPress-1>', 'DoubleClick'), ('<Triple-ButtonPress-1>', 'TripleClick')):
    root.bind(ev, lambda e, k=kind: put(e, k), add='+')
ent = txt = None; blist = []
if mode in ('events', 'text'):
    ent = tk.Entry(root, width=40); ent.pack(side='top', fill='x'); txt = tk.Text(root, height=cfg.get('lines', 8)); txt.pack(side='top', fill='both', expand=True)
    txt.bind('<Control-a>', lambda e: (txt.tag_add('sel', '1.0', 'end-1c'), 'break')[1])
    if cfg.get('fill'): txt.insert('1.0', '\n'.join('line %d' % i for i in range(1, cfg['fill'] + 1)))
    if cfg.get('focus', 'entry') == 'entry': root.after(200, lambda: ent.focus_force())
    else: root.after(200, lambda: txt.focus_force())
if mode == 'paint':
    cv = tk.Canvas(root, width=cfg.get('w', 600), height=cfg.get('h', 400), bg='white', highlightthickness=0); cv.pack(); last = {}
    def move(e):
        if 'p' in last and (e.state & 0x100): cv.create_line(*last['p'], e.x, e.y, fill='black', width=2)
        last['p'] = (e.x, e.y)
    cv.bind('<Motion>', move); cv.bind('<ButtonPress-1>', lambda e: last.update(p=(e.x, e.y)))
if mode == 'button':
    root.configure(bg=cfg.get('bg', '#828790'))
    for i, (bx, by) in enumerate(cfg.get('buttons', [[100, 100]])):
        b = tk.Button(root, text=cfg.get('label', 'Submit'), font=('Helvetica', cfg.get('fsize', 12)), command=lambda i=i: log.write(json.dumps({'t': time.time(), 'type': 'Command', 'button': i}) + '\n'))
        b.place(x=bx, y=by); blist.append(b)
def dump():
    st = {'entry': ent.get() if ent else None, 'text': txt.get('1.0', 'end-1c') if txt else None, 'top': txt.index('@0,0') if txt else None, 'rootx': root.winfo_rootx(), 'rooty': root.winfo_rooty(), 'w': root.winfo_width(), 'h': root.winfo_height(),
          'buttons': [[b.winfo_rootx(), b.winfo_rooty(), b.winfo_width(), b.winfo_height()] for b in blist], 'tk': root.tk.call('info', 'patchlevel')}
    open(cfg['state'] + '.tmp', 'w').write(json.dumps(st)); os.replace(cfg['state'] + '.tmp', cfg['state']); root.after(50, dump)
root.after(100, dump); root.mainloop()
'''
class Desk:
    # a private virtual X display (Xvfb, not a real screen) with an optional window manager (openbox); everything started on it is stopped on exit
    def __init__(self, w=1920, h=1080, depth=24, wm=True):
        self.w, self.h, self.depth, self.wm = w, h, depth, wm; self.kids = []; self.dir = tempfile.mkdtemp(prefix='desk'); self.saved = {}
    def start(self, argv, name, env=None):
        p = subprocess.Popen(argv, stdout=open(os.path.join(self.dir, name + '.out'), 'wb'), stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, env=env or self.env, start_new_session=True); self.kids.append(p); return p
    def out(self, name): return open(os.path.join(self.dir, name + '.out'), errors='replace').read()
    def __enter__(self):
        n = 100 + os.getpid() % 800
        while os.path.exists('/tmp/.X11-unix/X%d' % n) or os.path.exists('/tmp/.X%d-lock' % n): n += 1
        self.n = n; self.display = ':%d' % n
        env = dict(os.environ); env.pop('WAYLAND_DISPLAY', None); env.update({'DISPLAY': self.display, 'XDG_SESSION_TYPE': 'x11', 'PYTHONDONTWRITEBYTECODE': '1'})
        xa = os.path.join(self.dir, 'Xauthority'); open(xa, 'w').close(); env['XAUTHORITY'] = xa; self.env = env
        for k in ('DISPLAY', 'XDG_SESSION_TYPE', 'XAUTHORITY', 'WAYLAND_DISPLAY'): self.saved[k] = os.environ.get(k)
        self.x = self.start(['Xvfb', self.display, '-screen', '0', '%dx%dx%d' % (self.w, self.h, self.depth), '-nolisten', 'tcp', '-noreset'], 'xvfb', env)
        for _ in range(200):
            if os.path.exists('/tmp/.X11-unix/X%d' % n): break
            time.sleep(0.05)
        else: raise RuntimeError('Xvfb did not start')
        time.sleep(0.2); os.environ.update({'DISPLAY': self.display, 'XDG_SESSION_TYPE': 'x11', 'XAUTHORITY': xa}); os.environ.pop('WAYLAND_DISPLAY', None)
        if self.wm:
            self.start(['openbox'], 'openbox')
            for _ in range(200):
                if 'window id' in subprocess.run(['xprop', '-root', '_NET_SUPPORTING_WM_CHECK'], capture_output=True, text=True, env=env).stdout: break
                time.sleep(0.05)
        return self
    def __exit__(self, *a):
        for p in reversed(self.kids):
            try: os.killpg(p.pid, signal.SIGTERM)
            except Exception: pass
        for p in reversed(self.kids):
            try: p.wait(timeout=5)
            except Exception:
                try: os.killpg(p.pid, signal.SIGKILL)
                except Exception: pass
        for k, v in self.saved.items():
            if v is None: os.environ.pop(k, None)
            else: os.environ[k] = v
        shutil.rmtree(self.dir, ignore_errors=True)
    def sh(self, *argv, **kw):
        r = subprocess.run(list(argv), capture_output=True, text=True, env=self.env, stdin=subprocess.DEVNULL, timeout=kw.get('timeout', 60)); return r.stdout.strip()
    def observer(self, mode='events', geometry='600x400+100+100', **kw):
        k = len(self.kids); cfg = dict(mode=mode, geometry=geometry, log=os.path.join(self.dir, 'ev%d.jsonl' % k), state=os.path.join(self.dir, 'st%d.json' % k), **kw)
        open(cfg['log'], 'w').close(); p = self.start([LATEST if kw.get('py') is None else kw['py'], '-c', OBSERVER, json.dumps(cfg)], 'obs%d' % k)
        for _ in range(300):
            if os.path.exists(cfg['state']): break
            time.sleep(0.05)
        else: raise RuntimeError('observer did not appear: ' + self.out('obs%d' % k)[-300:])
        time.sleep(0.4); return Obs(cfg, p)
class Obs:
    def __init__(self, cfg, p): self.cfg, self.p = cfg, p
    def close(self):
        try: os.killpg(self.p.pid, signal.SIGTERM); self.p.wait(timeout=5)
        except Exception: pass
    def events(self, settle=True):
        if settle: self.settle()
        out = []
        for l in open(self.cfg['log']):
            try: out.append(json.loads(l))
            except ValueError: pass
        return out
    def state(self): return json.load(open(self.cfg['state']))
    def entry(self): self.settle(); time.sleep(0.12); return self.state()['entry']
    def text(self): self.settle(); time.sleep(0.12); return self.state()['text']
    def clear(self): self.settle(); open(self.cfg['log'], 'w').close()
    def settle(self, quiet=0.25, limit=10):
        n = -1; t0 = time.time()
        while time.time() - t0 < limit:
            m = len(self.events(settle=False))
            if m == n: return m
            n = m; time.sleep(quiet)
        return n
    def kinds(self, *types, key=None):
        ev = [e for e in self.events() if not types or e['type'] in types]
        return [(e['type'], e[key]) if key else e['type'] for e in ev]
def child(code, py=None, env=None, timeout=120, cwd=None):
    # runs code in a new interpreter (default the LATEST venv) and returns (return code, stdout lines without Xlib warnings, last stderr line)
    r = subprocess.run([py or LATEST, '-W', 'ignore', '-c', code], capture_output=True, text=True, env=env or os.environ, timeout=timeout, stdin=subprocess.DEVNULL, cwd=cwd)
    return r.returncode, [l for l in r.stdout.splitlines() if 'xauth' not in l], (r.stderr.strip().splitlines() or [''])[-1][:160]

# the replay harness: runs the listings of the chapter, statement by statement, on a private virtual X display (Xvfb with openbox), as printed
spec = json.load(open(os.environ['SPEC_FILE']))
def norm(t): return re.sub(r'\s+', '', t)
def lines(t): return [l.strip() for l in t.split('\n') if l.strip()]
def matches(got, exp): return norm(got) == norm(exp)
def differences(got, exp):
    gl, el = lines(got), lines(exp); out = []
    for a, b in zip(gl, el):
        if norm(a) != norm(b): out.append({'got': a, 'book': b})
    if len(gl) != len(el): out.append({'lines printed': len(gl), 'lines in the book': len(el)})
    return out[:6]
NS = {}; results = []; probes = {}
desk = Desk(); desk.__enter__()
try:
    text = desk.observer(geometry='800x500+50+50', mode='events', focus='text', title='editor'); tst = text.state()
    cfg_btn = dict(mode='button', geometry='400x300+1000+300', buttons=[[100, 100]], label='Submit')
    btn = desk.observer(**cfg_btn); bx, by, bw, bh = btn.state()['buttons'][0]
    os.chdir(tempfile.mkdtemp())
    probes['the editor window (observer) opened at'] = [tst['rootx'], tst['rooty'], tst['w'], tst['h']]
    probes['the Submit button of the second window: left, top, width, height'] = [bx, by, bw, bh]
    shots = None
    try:
        import pyautogui
        pyautogui.screenshot().crop((bx, by, bx + bw, by + bh)).save('submit.png'); shots = 'submit.png saved from a screenshot of the button'
    except BaseException as e: shots = 'submit.png not made: %s: %s' % (type(e).__name__, str(e).splitlines()[0][:100] if str(e) else '')
    probes['submit.png'] = shots
    def run_stmt(src, n, mode):
        buf = io.StringIO(); shown = []; old = sys.displayhook; sys.displayhook = lambda v: (shown.append(repr(v)) if v is not None else None)
        t0 = time.time()
        try:
            with contextlib.redirect_stdout(buf), warnings.catch_warnings(record=True) as wr:
                warnings.simplefilter('always')
                exec(compile(src.rstrip('\n') + '\n', '<listing %d>' % n, mode), NS)
            got = (buf.getvalue() + ''.join(s + '\n' for s in shown)).strip()
            return {'printed': got[:600], 'raised': None, 'seconds': round(time.time() - t0, 1), 'warnings': sorted({'%s: %s' % (x.category.__name__, str(x.message)[:80]) for x in wr if x.category.__name__ != 'ResourceWarning'})}, got
        except BaseException as e:
            return {'printed': buf.getvalue().strip()[:300], 'raised': '%s: %s' % (type(e).__name__, str(e).splitlines()[0][:150] if str(e) else ''), 'seconds': round(time.time() - t0, 1), 'warnings': []}, ''
        finally: sys.displayhook = old
    for n, title, kind, stmts in spec['listings']:
        rows = []
        for src, exp in stmts:
            row = {'source': src}
            if src.strip() == 'pyautogui.mouseInfo()':
                p = desk.start([sys.executable, '-W', 'ignore', '-c', 'import pyautogui; pyautogui.mouseInfo()'], 'mi'); time.sleep(4)
                alive = p.poll() is None; err = [l for l in desk.out('mi').splitlines() if 'Error' in l][-1:]
                row['as printed'] = {'printed': '', 'raised': None if alive else (err[0][:150] if err else 'exited %s' % p.returncode), 'note': 'the call blocks until its window is closed, so it ran in a child process for 4 seconds: %s' % ('the MouseInfo window was still open' if alive else 'the child had exited')}
                if alive: os.killpg(p.pid, signal.SIGTERM)
                row['book prints'] = exp[:200]; rows.append(row); continue
            r, got = run_stmt(src, n, 'exec' if kind == 'program' else 'single')
            r['matches the book'] = (matches(got, exp) and r['raised'] is None)
            if exp and r['raised'] is None and not r['matches the book']: r['differences from the book'] = differences(got, exp)
            row['as printed'] = r; row['book prints'] = exp[:300]; rows.append(row)
        results.append({'listing': n, 'what': title, 'statements': rows})
    time.sleep(0.5)
    try: probes['position after the listings'] = list(NS['pyautogui'].position())
    except BaseException as e: probes['position after the listings'] = type(e).__name__
    probes['text of the editor window after the listings'] = text.text()
    probes['entry of the editor window'] = text.entry()
    probes['Submit clicks seen by the button window'] = [e['button'] for e in btn.events() if e['type'] == 'Command']
    probes['events seen by the editor window: key presses, button presses'] = [len([e for e in text.events() if e['type'] == 'KeyPress']), len([e for e in text.events() if e['type'] == 'ButtonPress'])]
finally:
    desk.__exit__(None)
json.dump({'results': results, 'probes after the listings': probes}, open(os.environ['RESULT_FILE'], 'w'), default=repr, ensure_ascii=False)
"""
def sh(py, code, env=None, timeout=300):
    r = subprocess.run([py, "-W", "ignore::ResourceWarning", "-c", code], capture_output=True, text=True, env=env or os.environ, timeout=timeout, stdin=subprocess.DEVNULL)
    return r.stdout.strip(), r.stderr.strip(), r.returncode
ENVINFO = r"""import sys, importlib.metadata as md, json
out = {'python': sys.version.split()[0]}
for n in ('pyautogui', 'pyscreeze', 'pymsgbox', 'pytweening', 'pygetwindow', 'mouseinfo', 'pyperclip', 'python3-xlib', 'pillow', 'numpy', 'opencv-python-headless'):
    try: out[n] = md.version(n)
    except md.PackageNotFoundError: out[n] = None
try: import tkinter; out['Tk'] = tkinter.Tcl().eval('info patchlevel')
except BaseException as e: out['Tk'] = type(e).__name__
print(json.dumps(out))"""
def run_row(py, specs):
    """output in files, not pipes: a window or the display server started below keeps the pipes of its parent open"""
    env = dict(os.environ); env.pop("DISPLAY", None); env.pop("WAYLAND_DISPLAY", None)
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False); json.dump(specs, f); f.close(); env["SPEC_FILE"] = f.name
    res = tempfile.NamedTemporaryFile(suffix=".json", delete=False); res.close(); env["RESULT_FILE"] = res.name
    err = tempfile.NamedTemporaryFile(suffix=".err", delete=False)
    p = subprocess.Popen([py, "-W", "ignore", "-c", HARNESS], stdout=subprocess.DEVNULL, stderr=err, env=env, stdin=subprocess.DEVNULL)
    try: rc = p.wait(timeout=1500)
    except subprocess.TimeoutExpired: p.kill(); rc = -9
    if rc or not os.path.getsize(res.name): return {"harness failed": open(err.name).read().strip()[-500:]}
    return json.load(open(res.name))
def record():
    L = listings(); n_statements = sum(len(s) for _, _, _, s in L); items = []
    spec = {"listings": [list(x) for x in L]}
    items.append({"what": "The rows of the study: interpreter, packages and Tk of each row", "output": {n: json.loads(sh(p, ENVINFO)[0]) for n, p in ROWS}})
    t = chapter()
    items.append({"what": "The chapter page: %d listings found and replayed statement by statement (%d statements); figures and the table counted" % (len(L), n_statements),
                  "output": {"listings": len(L), "kinds": {k: sum(1 for x in L if x[2] == k) for k in ("repl", "program", "statements")}, "statements": n_statements, "figures": sorted(set(re.findall(r"Figure 23-\d", t))), "tables": sorted(set(re.findall(r"Table 23-\d", t))), "sha256": hashlib.sha256(t.encode()).hexdigest()}})
    for name, py in ROWS:
        items.append({"what": "Replay as printed, row %s (all 25 listings in one session on a private virtual X display, Xvfb with openbox; not a real screen)" % name, "output": run_row(py, spec)})
    return items
def tally(items):
    out = {}
    for i in items:
        o = i["output"]
        if isinstance(o, dict) and "results" in o:
            c = {"statements": 0, "matched the book": 0, "ran without an exception": 0, "raised": 0}
            for l in o["results"]:
                for s in l["statements"]:
                    r = s["as printed"]; c["statements"] += 1; c["raised"] += bool(r.get("raised")); c["ran without an exception"] += not r.get("raised"); c["matched the book"] += bool(r.get("matches the book"))
            out[i["what"].split(",")[1].split(" (")[0].strip()] = c
    return out
def digest(it):
    t = json.dumps(it, sort_keys=True, ensure_ascii=False)
    for a, b in ((r"0x[0-9a-f]{6,}", "0xADDR"), (r'"seconds": [0-9.]+', '"seconds": T'), (r"/tmp/\w+", "/tmp/X")): t = re.sub(a, b, t)
    return t
if __name__ == "__main__":
    if MODE == "write":
        items = record()
        json.dump({"_version": __version__, "_note": "Recorded by sen0414_ch23_thirdparty_v1_0_0.py write; every output was printed by the program beside it under the interpreter and package set named in the item, on a private virtual X display (Xvfb with openbox, two Tk windows as stand-ins) on a machine in the zone Europe/Istanbul. The chapter page was fetched and its sha256 equals the chapterDigest of the book's own chapter ontology. Seconds are what the statement took on that run.",
                   "python": "3.14.6 (LATEST, NOCV, OLDSCREEZE, BARE) and 3.12.3 (TK86)", "tally": tally(items), "items": items}, open(REC, "w"), indent=1, ensure_ascii=False)
        print("recorded", len(items), "items ->", REC); print(json.dumps(tally(items), indent=1))
    else:
        old = json.load(open(REC))["items"]; new = record(); bad = [i for i, (a, b) in enumerate(zip(old, new)) if digest(a["output"]) != digest(b["output"])]
        print("items checked:", len(new), "differences:", bad); sys.exit(1 if bad else 0)

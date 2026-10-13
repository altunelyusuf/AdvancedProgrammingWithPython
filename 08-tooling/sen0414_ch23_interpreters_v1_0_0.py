#!/usr/bin/env python3
"""Chapter 23 (Controlling the Keyboard and Mouse): runs one program, what PyAutoGUI does on a virtual X display (Xvfb, with the Tk observer window that logs every delivered event
and xev for the wheel buttons; NOT a real screen), under every installed 3.14 patch release (3.14.0 to 3.14.6) and, for comparison, under 3.15 (a beta), 3.13, 3.12 and 3.11,
with the newest PyAutoGUI and its packages the index offers for each interpreter (`uv run --no-project --with pyautogui --with pillow --with python3-xlib`), and records what
each printed. It then runs a smaller program over the releases of the packages themselves: PyAutoGUI 0.9.40, 0.9.41, 0.9.50 and 0.9.54 with PyScreeze 0.1.28 and 1.0.1 (on 3.12),
PyScreeze 0.1.27 to 1.0.1 with PyAutoGUI 0.9.54 (on 3.14.6), Pillow 9.5.0 to 12.3.0 (on 3.12) and PyMsgBox 1.0.9 and 2.0.1, because the chapter says that locateOnScreen() returned
None "in versions of PyAutoGUI before 1.0.0" and the newest PyAutoGUI is 0.9.54. A release that cannot run is recorded as NOT EXECUTED with the last lines uv or Python printed.
The operating system is Ubuntu 24.04; Xvfb, openbox, xev, xdotool, scrot and xclip come from apt; the Tk of each interpreter is whatever its build holds (the record names it).
Nothing leaves the machine and nothing controls anything but the private display the program starts and stops. Windows and macOS were not executed.
Usage: sen0414_ch23_interpreters_v1_0_0.py   (needs uv on PATH)   -> ch23-page/interpreter_record_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "08-tooling", "ch23-page", "interpreter_record_v1_0_0.json")
PROG = r"""import os, sys
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

# one program for every interpreter: what PyAutoGUI does on a virtual X display, observed as delivered events (the body that follows HEAD)
res = {}
def w(f):
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter('always')
        try: v = f()
        except BaseException as e: v = type(e).__name__ + ': ' + (str(e).splitlines() or [''])[0][:100]
    return [v, sorted({x.category.__name__ for x in seen if x.category.__name__ != 'ResourceWarning'})]
res['series'] = sys.version.split()[0].rsplit('.', 1)[0] + '.x'
res['versions'] = [md.version(n) for n in ('pyautogui', 'pyscreeze', 'pymsgbox', 'pytweening', 'pillow')]
res['Tk version of this interpreter'] = w(lambda: __import__('tkinter').Tcl().eval('info patchlevel'))[0]
with Desk() as d:
    import pyautogui; res['PAUSE, FAILSAFE at import'] = [pyautogui.PAUSE, pyautogui.FAILSAFE]; pyautogui.PAUSE = 0
    res['import pyautogui: warnings'] = w(lambda: __import__('pyautogui').__version__)
    res['size, named tuple'] = w(lambda: [tuple(pyautogui.size()), type(pyautogui.size()).__name__])
    res['moveTo then position'] = w(lambda: (pyautogui.moveTo(321, 123), tuple(pyautogui.position()))[1])
    res['fail-safe points'] = w(lambda: sorted(pyautogui.FAILSAFE_POINTS))
    def fs():
        pyautogui.moveTo(0, 0)
        try: pyautogui.click(); return 'no exception'
        except pyautogui.FailSafeException: return 'FailSafeException'
    res['click while the pointer is in the corner'] = w(fs)
    try:
        o = d.observer(geometry='1920x1080+0+0', mode='paint', w=1900, h=1000)
        pyautogui.FAILSAFE = False; pyautogui.moveTo(700, 400); o.clear()
        def click_events():
            pyautogui.click(710, 405); ev = o.events(); return [(e['type'], e['num'], e['send_event']) for e in ev if e['type'].startswith('Button')]
        res['click: events delivered'] = w(click_events)
        def scroll_events():
            x = d.start(['xev', '-geometry', '300x200+1500+100', '-event', 'mouse'], 'xev'); time.sleep(0.8); pyautogui.moveTo(1600, 200); rows = []
            def btns():
                time.sleep(0.4); t = d.out('xev'); open(os.path.join(d.dir, 'xev.out'), 'w').close(); return [int(b) for a, b in re.findall(r'(ButtonPress) event.*?button (\d)', t, re.S)]
            btns()
            for f in (lambda: pyautogui.scroll(3), lambda: pyautogui.scroll(-2), lambda: pyautogui.hscroll(1)): f(); rows.append(btns())
            os.killpg(x.pid, signal.SIGTERM); pyautogui.moveTo(700, 400); return rows
        res['scroll(3), scroll(-2), hscroll(1): wheel buttons'] = w(scroll_events)
        def drag_events():
            pyautogui.moveTo(500, 500); o.clear(); pyautogui.drag(300, 0, duration=0.25); ev = o.events()
            return [[e['type'], e['num']] for e in ev if e['type'].startswith('Button')], len([e for e in ev if e['type'] == 'Motion']), sorted({e['state'] for e in ev if e['type'] == 'Motion'})
        res['drag: buttons, motions, button state'] = w(drag_events)
        o.close()
    except Exception as e: res['observer block failed at: ' + "o = d.observer(geometry='1920x1080+0+0'"] = str(e)[:140]
    try:
        o = d.observer(geometry='600x400+100+100'); st = o.state(); pyautogui.moveTo(st['rootx'] + 100, st['rooty'] + 10); pyautogui.click(); o.clear()
        def typed():
            pyautogui.write('Hello, world!'); return o.entry()
        res['write: text received'] = w(typed)
        def hot():
            o.clear(); pyautogui.hotkey('ctrl', 'alt', 'shift', 's'); return [(e['type'][3:], e['keysym']) for e in o.events()]
        res['hotkey(ctrl, alt, shift, s): events'] = w(hot)
        def silent():
            o.clear(); before = o.entry(); pyautogui.press('nokey'); pyautogui.write('café'); return o.entry()[len(before):]
        res['unknown key name and a character outside the table'] = w(silent)
        o.close()
    except Exception as e: res['observer block failed at: ' + "o = d.observer(geometry='600x400+100+100')"] = str(e)[:140]
    d.sh('xsetroot', '-solid', '#828790'); time.sleep(0.2)
    res['pixel(50, 200), pixelMatchesColor'] = w(lambda: [tuple(pyautogui.pixel(50, 200)), pyautogui.pixelMatchesColor(50, 200, (130, 135, 144))])
    res['screenshot: size, mode, type'] = w(lambda: (lambda im: [im.size, im.mode, type(im).__name__])(pyautogui.screenshot()))
    try:
        o = d.observer(mode='button', geometry='400x300+300+200', buttons=[[100, 100]]); x, y, bw, bh = o.state()['buttons'][0]; os.chdir(d.dir)
        pyautogui.screenshot().crop((x, y, x + bw, y + bh)).save('submit.png')
        res['locateOnScreen: box'] = w(lambda: [int(v) for v in pyautogui.locateOnScreen('submit.png')])
        res['locateCenterOnScreen: point'] = w(lambda: [int(v) for v in pyautogui.locateCenterOnScreen('submit.png')])
        from PIL import Image; im = Image.open('submit.png').convert('RGB'); im.putpixel((3, 3), (0, 0, 0)); im.save('off.png')
        def nf():
            try: pyautogui.locateOnScreen('off.png'); return 'found'
            except Exception as e: return type(e).__module__ + '.' + type(e).__name__
        res['locateOnScreen of an image that is one pixel off'] = w(nf)
        res['confidence keyword'] = w(lambda: 'found' if pyautogui.locateOnScreen('off.png', confidence=0.9) else 'None')
        o.close()
    except Exception as e: res['observer block failed at: ' + "o = d.observer(mode='button'"] = str(e)[:140]
    res['window functions on this platform'] = w(lambda: [sys.platform, [n for n in ('getActiveWindow', 'getAllWindows', 'getWindowsWithTitle', 'getAllTitles') if hasattr(pyautogui, n)]])
    res['KEYBOARD_KEYS: count, shift alias'] = w(lambda: [len(pyautogui.KEYBOARD_KEYS), 'shiftleft' in pyautogui.KEYBOARD_KEYS])
    p = d.start([sys.executable, '-W', 'ignore', '-c', 'import pyautogui; pyautogui.mouseInfo()'], 'mi'); time.sleep(3.5)
    res['mouseInfo(): window after 3.5 s'] = w(lambda: ['running' if p.poll() is None else 'exited %s' % p.returncode, [l for l in d.out('mi').splitlines() if 'Error' in l][-1:]])
    res['import pyautogui without DISPLAY'] = w(lambda: child("import pyautogui", py=sys.executable, env={k: v for k, v in os.environ.items() if k != 'DISPLAY'})[2][:60])
import importlib.util
res['compile the X11 backend: warnings'] = w(lambda: (lambda src: compile(src, 'x11.py', 'exec') and 'compiled')(open(os.path.join(os.path.dirname(importlib.util.find_spec('pyautogui').origin), '_pyautogui_x11.py')).read()))
print(json.dumps(res, sort_keys=True, default=repr))
"""
MATRIX = r"""import os, sys
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

# a smaller program for the releases of the packages themselves: what the locate functions do with an image that is one pixel off, the Box type, the screenshot and pixel calls
res = {}
def w(f):
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter('always')
        try: v = f()
        except BaseException as e: v = type(e).__module__ + '.' + type(e).__name__ + ': ' + (str(e).splitlines() or [''])[0][:80]
    return [v, sorted({x.category.__name__ for x in seen if x.category.__name__ != 'ResourceWarning'})]
res['python'] = sys.version.split()[0]
res['versions'] = {n: (md.version(n) if n in [d.metadata['Name'].lower() for d in md.distributions()] else None) for n in ('pyautogui', 'pyscreeze', 'pymsgbox', 'pillow')}
with Desk() as d:
    import pyautogui, pyscreeze; pyautogui.PAUSE = 0
    from PIL import Image
    res['pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION'] = getattr(pyscreeze, 'USE_IMAGE_NOT_FOUND_EXCEPTION', 'absent')
    res['pyautogui.useImageNotFoundException'] = hasattr(pyautogui, 'useImageNotFoundException')
    o = d.observer(mode='button', geometry='400x300+300+200', buttons=[[100, 100]]); x, y, bw, bh = o.state()['buttons'][0]; os.chdir(d.dir)
    res['screenshot: size, mode'] = w(lambda: (lambda im: [im.size, im.mode])(pyautogui.screenshot()))
    pyautogui.screenshot().crop((x, y, x + bw, y + bh)).save('submit.png')
    im = Image.open('submit.png').convert('RGB'); im.putpixel((3, 3), (0, 0, 0)); im.save('off.png')
    res['locateOnScreen: exact image'] = w(lambda: (lambda b: [type(b).__name__, [int(v) for v in b]])(pyautogui.locateOnScreen('submit.png')))
    res['locateOnScreen: image one pixel off'] = w(lambda: repr(pyautogui.locateOnScreen('off.png')))
    res['click(image one pixel off)'] = w(lambda: pyautogui.click('off.png'))
    res['pixel(0, 0) type'] = w(lambda: type(pyautogui.pixel(0, 0)).__name__)
    res['pixelMatchesColor tolerance keyword'] = w(lambda: pyautogui.pixelMatchesColor(0, 0, tuple(pyautogui.pixel(0, 0)), tolerance=1))
    res['exception class hierarchy'] = w(lambda: [pyautogui.ImageNotFoundException.__mro__[1].__name__, pyautogui.FailSafeException.__mro__[1].__name__] if hasattr(pyautogui, 'ImageNotFoundException') else 'ImageNotFoundException absent')
    res['hold context manager'] = hasattr(pyautogui, 'hold')
    res['write is typewrite'] = pyautogui.write is getattr(pyautogui, 'typewrite', None)
    res['KEYBOARD_KEYS count'] = len(pyautogui.KEYBOARD_KEYS)
    o.close()
print(json.dumps(res, sort_keys=True, default=repr))
"""
MSGBOX = r"""import sys, json, inspect, importlib.metadata as md
import pymsgbox
res = {'pymsgbox': md.version('pymsgbox'), 'python': sys.version.split()[0]}
res['functions'] = sorted(n for n in ('alert', 'confirm', 'prompt', 'password') if hasattr(pymsgbox, n))
res['signatures'] = {n: str(inspect.signature(getattr(pymsgbox, n))) for n in ('alert', 'confirm', 'prompt', 'password')}
res['constants'] = [pymsgbox.OK_TEXT, pymsgbox.CANCEL_TEXT, pymsgbox.TIMEOUT_RETURN_VALUE]
res['exceptions'] = sorted(n for n in dir(pymsgbox) if n.endswith('Exception'))
print(json.dumps(res, sort_keys=True))
"""
INTERPRETERS = ["3.11", "3.12", "3.13", "3.14.0", "3.14.1", "3.14.2", "3.14.3", "3.14.4", "3.14.5", "3.14.6", "3.15"]
BASE = ["pyautogui", "pillow", "python3-xlib"]
PYAUTOGUI = [("0.9.40", "0.1.28"), ("0.9.40", "1.0.1"), ("0.9.41", "0.1.28"), ("0.9.41", "1.0.1"), ("0.9.50", "0.1.28"), ("0.9.50", "1.0.1"), ("0.9.54", "0.1.28"), ("0.9.54", "1.0.1")]
PYSCREEZE = ["0.1.27", "0.1.28", "0.1.29", "0.1.30", "1.0.0", "1.0.1"]
PILLOWS = ["9.5.0", "10.0.0", "10.4.0", "11.0.0", "11.3.0", "12.0.0", "12.3.0"]
MSGBOXES = ["1.0.9", "2.0.0", "2.0.1"]
def uv(py, withs, code, timeout=900, extra=()):
    env = dict(os.environ); env.pop("PYTHONPATH", None); env["TZ"] = "Europe/Istanbul"; env.pop("WAYLAND_DISPLAY", None)
    cmd = ["uv", "run", "--no-project", "--python", py] + list(extra)
    for x in withs: cmd += ["--with", x]
    out = open(os.path.join(os.environ.get("TMPDIR", "/tmp"), "ch23_interp.out"), "w+"); err = open(os.path.join(os.environ.get("TMPDIR", "/tmp"), "ch23_interp.err"), "w+")
    try: r = subprocess.run(cmd + ["python", "-I", "-c", code], stdout=out, stderr=err, env=env, timeout=timeout, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired: return {"NOT EXECUTED or failed": "timed out after %d s" % timeout}
    out.seek(0); err.seek(0); so = out.read(); se = err.read()
    if r.returncode != 0 or not so.strip():
        e = [l for l in se.strip().splitlines() if l.strip()]
        return {"NOT EXECUTED or failed": " | ".join(e[-3:])[:420]}
    return json.loads(so.strip().splitlines()[-1])
def compare(results):
    keys = sorted({k for r in results.values() for k in r if k not in ("series", "versions", "python", "pyautogui", "pyscreeze", "pillow", "pymsgbox", "Tk version of this interpreter")})
    differ = {}
    for k in keys:
        vals = {}
        for v, r in results.items():
            if "NOT EXECUTED or failed" in r: continue
            vals.setdefault(json.dumps(r.get(k), sort_keys=True), []).append(v)
        if len(vals) > 1: differ[k] = [[json.loads(a), b] for a, b in vals.items()]
    return keys, differ
if __name__ == "__main__":
    results = {}
    for py in INTERPRETERS:
        v = subprocess.run(["uv", "run", "--no-project", "--python", py, "python", "-c", "import sys; print(sys.version.split()[0])"], capture_output=True, text=True).stdout.strip()
        results[v or py] = uv(py, BASE, PROG); print(py, v, "ok" if "NOT EXECUTED or failed" not in results[v or py] else results[v or py]["NOT EXECUTED or failed"], flush=True)
    results["3.14.6 with OpenCV"] = uv("3.14.6", BASE + ["numpy", "opencv-python-headless"], PROG); print("3.14.6 with OpenCV", "ok" if "NOT EXECUTED or failed" not in results["3.14.6 with OpenCV"] else results["3.14.6 with OpenCV"], flush=True)
    keys, differ = compare(results)
    pa = {}
    for a, s in PYAUTOGUI:
        k = "pyautogui %s with pyscreeze %s on 3.12" % (a, s); pa[k] = uv("3.12", ["pyautogui==" + a, "pyscreeze==" + s, "pillow", "python3-xlib"], MATRIX); print(k, "ok" if "NOT EXECUTED or failed" not in pa[k] else pa[k], flush=True)
    for s in PYSCREEZE:
        k = "pyscreeze %s with pyautogui 0.9.54 on 3.14.6" % s; pa[k] = uv("3.14.6", ["pyautogui==0.9.54", "pyscreeze==" + s, "pillow", "python3-xlib"], MATRIX); print(k, "ok" if "NOT EXECUTED or failed" not in pa[k] else pa[k], flush=True)
    pkeys, pdiffer = compare(pa)
    pil = {}
    for v in PILLOWS:
        pil[v] = uv("3.12", ["pyautogui==0.9.54", "pillow==" + v, "python3-xlib"], MATRIX); print("pillow", v, "ok" if "NOT EXECUTED or failed" not in pil[v] else pil[v], flush=True)
    lkeys, ldiffer = compare(pil)
    mb = {}
    for v in MSGBOXES:
        mb[v] = uv("3.14.6", ["pymsgbox==" + v], MSGBOX); print("pymsgbox", v, "ok" if "NOT EXECUTED or failed" not in mb[v] else mb[v], flush=True)
    mkeys, mdiffer = compare(mb)
    json.dump({"_version": "1.0.0", "observed": datetime.date.today().isoformat(), "_note": "Recorded by sen0414_ch23_interpreters_v1_0_0.py: one program (PyAutoGUI calls observed as delivered events on a virtual X display, Xvfb, not a real screen) under every installed Python 3.14 patch release and the 3.15 beta, 3.13, 3.12 and 3.11, with the newest packages for each; the same checks across releases of PyAutoGUI, PyScreeze, Pillow and PyMsgBox. A result is what the program printed on the day on this machine (Ubuntu 24.04, Europe/Istanbul); a row that cannot run says NOT EXECUTED or failed and why. Windows and macOS were not executed.",
               "program": PROG, "matrix program": MATRIX, "msgbox program": MSGBOX, "interpreters": list(results), "results": results, "items compared": len(keys), "differ": differ,
               "package release rows": pa, "package items compared": len(pkeys), "package differ": pdiffer, "pillow releases": pil, "pillow items compared": len(lkeys), "pillow differ": ldiffer,
               "pymsgbox releases": mb, "pymsgbox items compared": len(mkeys), "pymsgbox differ": mdiffer}, open(OUT, "w"), indent=1, ensure_ascii=False)
    print("recorded", len(results), "interpreter rows;", len(keys), "items; items that differ:", sorted(differ)); print("package rows:", len(pa), sorted(pdiffer)); print("pillow runs:", len(pil), sorted(ldiffer)); print("pymsgbox runs:", len(mb), sorted(mdiffer))

#!/usr/bin/env python3
"""SEN0414 chapter 23 (Controlling the Keyboard and Mouse, 3rd edition) - the shared base of the corpus, version 1.0.0.

Holds the chapter's whole programs as text, the single source a deck or a page's Lab tab can read, in the shape of sen0414_ch22_corpus_base_v1_0_0.py.
Each program is a complete script that exits 0 and prints what it printed on 2026-10-13 under Python 3.14.x (uv) in the environment /home/claude/venv314_ch23_latest
(PyAutoGUI 0.9.54 and its dependencies, pyperclip) whose interpreter runs the file (the variable CH23_LATEST overrides the interpreter the windows are started with).
Every program that moves a pointer or sends keys starts ITS OWN virtual X display (Xvfb, with the openbox window manager where a program needs one) and real X clients
(a Tk window, xterm, xdotool, xclip) on it, and stops them at the end: nothing is sent to the screen of this machine or to any person or service. What the programs print is
what the X clients RECEIVED, so it is labelled "virtual display (Xvfb), not a real screen". A real screen, Windows or macOS permissions, HiDPI, several monitors, applications that
block synthetic input and a Wayland compositor are NOT EXECUTED anywhere here. The record that reads the book's page and asks the public services is sen0414_ch23_live_v1_0_0.py;
the one that replays the chapter's listings is sen0414_ch23_thirdparty_v1_0_0.py.
LOCAL STAND-IN: every program with a window uses the virtual display (Xvfb); nobody sees it.
"""
HEAD = r"""import io, os, sys, re, json, time, shutil, signal, tempfile, warnings, subprocess, importlib.metadata as md
warnings.simplefilter('ignore')
LATEST = os.environ.get('CH23_LATEST', sys.executable)
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
        xa = os.path.join(self.dir, 'Xauthority'); open(xa, 'w').close(); subprocess.run(['xauth', '-f', xa, 'add', ':999', '.', '00112233445566778899aabbccddeeff'], capture_output=True, stdin=subprocess.DEVNULL); env['XAUTHORITY'] = xa; self.env = env
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
os.chdir(tempfile.mkdtemp(prefix='ch23work'))
"""
SPIRAL = HEAD + r'''# Chapter 23, "Controlling the Mouse": the book's spiral drawing program, run on a virtual display where a paint-like window records what the drag draws.
with Desk(wm=False) as d:
    import pyautogui; pyautogui.PAUSE = 0
    o = d.observer(geometry='700x500+0+0', mode='paint', w=700, h=500); pyautogui.moveTo(350, 250); time.sleep(0.3); o.clear()
    pyautogui.mouseDown(button='left'); dist = 200; steps = 0
    while dist > 0:
        pyautogui.drag(dist, 0, duration=0.05, button='left'); dist -= 5
        pyautogui.drag(0, dist, duration=0.05, button='left')
        pyautogui.drag(-dist, 0, duration=0.05, button='left'); dist -= 5
        pyautogui.drag(0, -dist, duration=0.05, button='left'); steps += 4
    pyautogui.mouseUp(button='left'); ev = o.events()
    im = pyautogui.screenshot().crop((0, 0, 700, 500)).convert('L'); dark = sum(1 for v in im.getdata() if v < 128)
    print('virtual display (Xvfb), not a real screen; the spiral program made', steps, 'drag calls')
    bp = [e['num'] for e in ev if e['type'] in ('ButtonPress', 'DoubleClick', 'TripleClick')]; br = [e['num'] for e in ev if e['type'] == 'ButtonRelease']
    print('press events (Tk reports quick repeats as double and triple clicks):', len(bp), 'ButtonRelease events:', len(br), 'buttons used:', sorted(set(bp + br)), '(each drag() call presses and releases the button itself)')
    print('motion events seen:', sum(e['type'] == 'Motion' for e in ev) > 100, ' dark pixels in the screenshot of the canvas:', dark > 500)
    o.close()
'''
MOVE = HEAD + r'''# Chapter 23, "Moving the Mouse": moveTo, move, position, size and onScreen, with the real pointer position read back from the X server.
with Desk(wm=False) as d:
    import pyautogui; pyautogui.PAUSE = 0
    print('virtual display (Xvfb), not a real screen; size():', tuple(pyautogui.size()), ' onScreen(10, 10):', pyautogui.onScreen(10, 10), ' onScreen(-1, 5):', pyautogui.onScreen(-1, 5), ' onScreen(1920, 5):', pyautogui.onScreen(1920, 5))
    pyautogui.moveTo(100, 200); print('moveTo(100, 200) -> position()', tuple(pyautogui.position()), ' xdotool says', d.sh('xdotool', 'getmouselocation').split(' screen')[0])
    pyautogui.move(30, -40); print('move(30, -40) ->', tuple(pyautogui.position()))
    pyautogui.moveTo(None, 500); print('moveTo(None, 500) keeps x ->', tuple(pyautogui.position()))
    t = time.perf_counter(); pyautogui.moveTo(900, 500, duration=1); el = time.perf_counter() - t
    print('moveTo(900, 500, duration=1) took about one second:', 0.9 < el < 1.6, '->', tuple(pyautogui.position()))
    pyautogui.moveTo(300.7, 400.2); print('float coordinates moveTo(300.7, 400.2) ->', tuple(pyautogui.position()))
    p = pyautogui.position(); print('position() is a named tuple:', type(p).__name__, p.x, p.y)
'''
CLICKS = HEAD + r'''# Chapter 23, "Clicking the Mouse", "Dragging" and "Scrolling": every button, the double click, a drag and a wheel turn, as the window under the pointer receives them.
with Desk(wm=False) as d:
    import pyautogui; pyautogui.PAUSE = 0
    o = d.observer(geometry='1920x1080+0+0', mode='paint', w=1900, h=1000); pyautogui.moveTo(700, 400); time.sleep(0.3); res = {}
    for name, call in (('click()', lambda: pyautogui.click()), ("button='middle'", lambda: pyautogui.click(button='middle')), ("button='right'", lambda: pyautogui.click(200, 250, button='right')), ('doubleClick()', lambda: pyautogui.doubleClick())):
        time.sleep(0.7); o.clear(); call(); res[name] = [(e['type'], e['num']) for e in o.events() if e['type'] in ('ButtonPress', 'DoubleClick')]
    for k, v in res.items(): print('virtual display (Xvfb);', k, '-> events seen', v)
    pyautogui.moveTo(500, 500); o.clear(); pyautogui.drag(300, 0, duration=0.25); ev = o.events()
    print('drag(300, 0): button events', [(e['type'], e['num']) for e in ev if e['type'].startswith('Button')], ' at least 5 motion events:', sum(e['type'] == 'Motion' for e in ev) >= 5, ' end', tuple(pyautogui.position()))
    def wheel(f):
        o.clear(); f(); return [(e['type'], e['delta'], e['num']) for e in o.events() if e['type'] in ('MouseWheel', 'ButtonPress')]
    print('scroll(3) ->', wheel(lambda: pyautogui.scroll(3)), '\n  scroll(-2) ->', wheel(lambda: pyautogui.scroll(-2)), '\n  hscroll(1) ->', wheel(lambda: pyautogui.hscroll(1)), '\n  (Tk 9 reports the wheel as MouseWheel with a delta; X buttons 4 and 5 are the vertical wheel, 6 and 7 the horizontal one)')
    o.close()
'''
FAILSAFE = HEAD + r'''# Chapter 23, "Pauses and Fail-Safes": PAUSE, FAILSAFE and the exception raised when the pointer goes to a corner.
with Desk(wm=False) as d:
    import pyautogui
    print('virtual display (Xvfb); default PAUSE', pyautogui.PAUSE, ' default FAILSAFE', pyautogui.FAILSAFE, ' FAILSAFE_POINTS', pyautogui.FAILSAFE_POINTS)
    pyautogui.PAUSE = 0.5; t = time.perf_counter(); pyautogui.moveTo(100, 100); pyautogui.moveTo(200, 200); el = time.perf_counter() - t
    print('two calls with PAUSE = 0.5 took about a second:', 0.9 < el < 1.6)
    pyautogui.PAUSE = 0; pyautogui.moveTo(300, 300); pyautogui.moveTo(0, 0); print('moveTo(0, 0) itself raises nothing (the target is in FAILSAFE_POINTS); position', tuple(pyautogui.position()))
    try: pyautogui.moveTo(500, 500); print('the next call from the corner raised nothing, position', tuple(pyautogui.position()))
    except pyautogui.FailSafeException as e: print('the next call, started while the pointer is in the corner, raises', type(e).__name__, '; position stays', tuple(pyautogui.position()))
    pyautogui.FAILSAFE = False; pyautogui.moveTo(0, 1079); pyautogui.FAILSAFE = True
    try: pyautogui.click()
    except pyautogui.FailSafeException: print('click() in the bottom-left corner raises FailSafeException as well')
    pyautogui.FAILSAFE = False; pyautogui.moveTo(0, 0); pyautogui.moveTo(600, 600); print('FAILSAFE = False: the same call from the corner goes through, position', tuple(pyautogui.position()))
'''
SHOT = HEAD + r'''# Chapter 23, "Screenshots", "Analyzing the Screenshot" and "Image Recognition": screenshot, getpixel, pixelMatchesColor and locateOnScreen on a window of known colours.
with Desk(wm=False) as d:
    import pyautogui, pyscreeze; pyautogui.PAUSE = 0
    o = d.observer(mode='button', geometry='400x300+200+150', bg='#ff0000', buttons=[[100, 100]], label='Submit'); time.sleep(0.5)
    im = pyautogui.screenshot(); print('virtual display (Xvfb); screenshot():', type(im).__name__, im.size, im.mode)
    print('getpixel((210, 160)) in the red window:', im.getpixel((210, 160)), ' outside it (5, 5):', im.getpixel((5, 5)))
    print('pyautogui.pixelMatchesColor(210, 160, (255, 0, 0)):', pyautogui.pixelMatchesColor(210, 160, (255, 0, 0)), ' with (255, 0, 1):', pyautogui.pixelMatchesColor(210, 160, (255, 0, 1)), ' tolerance=5:', pyautogui.pixelMatchesColor(210, 160, (255, 0, 1), tolerance=5))
    st = o.state(); bx, by, bw, bh = st['buttons'][0]; btn = im.crop((bx, by, bx + bw, by + bh)); btn.save('submit.png')
    try: box = pyautogui.locateOnScreen('submit.png'); print('locateOnScreen found it:', tuple(box) == (bx, by, bw, bh), ' centre is', tuple(int(v) for v in pyautogui.center(box)), 'expected', (bx + bw // 2, by + bh // 2))
    except Exception as e: print('locateOnScreen raised', type(e).__name__)
    print('locateAllOnScreen count:', len(list(pyautogui.locateAllOnScreen('submit.png'))))
    blank = btn.point(lambda v: 255 - v); blank.save('missing.png')
    try: print('an image that is not on the screen ->', pyautogui.locateOnScreen('missing.png'))
    except pyautogui.ImageNotFoundException as e: print('an image that is not on the screen raises', type(e).__name__)
    print('PyScreeze', pyscreeze.__version__ if hasattr(pyscreeze, '__version__') else md.version('pyscreeze'))
    o.close()
'''
TYPE = HEAD + r'''# Chapter 23, "Sending Keystrokes" and "Hotkey Combinations": write, press, keyDown, keyUp and hotkey into a window that logs what it receives.
with Desk() as d:
    import pyautogui; pyautogui.PAUSE = 0
    o = d.observer(mode='text', geometry='600x400+100+100', focus='text'); time.sleep(0.5); pyautogui.click(300, 300); time.sleep(0.3)
    pyautogui.write('Hello, world!', interval=0.02); print('virtual display (Xvfb); write(\'Hello, world!\') ->', repr(o.text()))
    pyautogui.press('enter'); pyautogui.write('Tab'); pyautogui.press(['left', 'left', 'backspace']); print('after enter, "Tab", two lefts and a backspace ->', repr(o.text()))
    pyautogui.write('x\ty'); print('a tab character in write() ->', repr(o.text()[-4:]))
    before = o.text(); pyautogui.write('äö€'); print('non-ASCII in write() adds nothing (unknown keys are ignored):', o.text() == before)
    pyautogui.hotkey('ctrl', 'a'); pyautogui.press('delete'); print('hotkey(ctrl, a) and delete -> text now', repr(o.text()))
    o.clear(); pyautogui.keyDown('shift'); pyautogui.press('a'); pyautogui.keyUp('shift'); ev = o.events(); print('shift down, a, shift up -> keysyms', [(e['type'], e['keysym']) for e in ev if e['type'].startswith('Key')])
    print('the number of keyboard names:', len(pyautogui.KEYBOARD_KEYS), ' "enter" in it:', 'enter' in pyautogui.KEYBOARD_KEYS, ' "ctrl" in it:', 'ctrl' in pyautogui.KEYBOARD_KEYS)
    o.close()
'''
MSGBOX = HEAD + r'''# Chapter 23, "Displaying Message Boxes": alert, confirm, prompt and password boxes answered by a script on a virtual display (Tk 9 of the uv Python opens no window, so the dialogs are not driven here).
with Desk() as d:
    import pyautogui
    names = [n for n in ('alert', 'confirm', 'prompt', 'password') if callable(getattr(pyautogui, n, None))]
    print('virtual display (Xvfb); message box functions in pyautogui:', names)
    print('pymsgbox version recorded by the package:', md.version('pymsgbox'), '; Tk of this Python:', __import__('tkinter').TkVersion)
    code = "import pyautogui; print(repr(pyautogui.confirm('Go on?', 'Q', buttons=['Yes', 'No'])))"
    p = d.start([sys.executable, '-W', 'ignore', '-c', code], 'msgbox'); time.sleep(3)
    if p.poll() is None:
        wins = d.sh('xdotool', 'search', '--name', 'Q'); print('a window titled Q exists:', bool(wins.strip()))
        if wins.strip(): d.sh('xdotool', 'key', 'Return'); time.sleep(1)
        print('the box returned:', d.out('msgbox').strip().splitlines()[-1:] if d.out('msgbox').strip() else None, ' process ended:', p.poll() is not None)
    else: print('NOT EXECUTED as a dialog: the child ended at once;', d.out('msgbox').strip().splitlines()[-1:])
'''
BUSY = HEAD + r'''# Chapter 23, "Project: Looking Busy": a script that nudges the pointer by one pixel at intervals, with the number of motion events a window sees, then stops.
with Desk(wm=False) as d:
    import pyautogui; pyautogui.PAUSE = 0
    o = d.observer(geometry='1920x1080+0+0', mode='paint', w=1900, h=1000); pyautogui.moveTo(600, 400); time.sleep(0.3); o.clear(); n = 0
    t0 = time.time()
    while time.time() - t0 < 2.2:
        pyautogui.move(1, 0); time.sleep(0.4); pyautogui.move(-1, 0); time.sleep(0.4); n += 2
    ev = [e for e in o.events() if e['type'] == 'Motion']
    print('virtual display (Xvfb); move(1, 0) and move(-1, 0) calls:', n, '| motion events the window received:', len(ev), '| back at', tuple(pyautogui.position()))
    print('every move was exactly one pixel:', {abs(a['x_root'] - b['x_root']) for a, b in zip(ev, ev[1:])})
    o.close()
'''
CLIP = HEAD + r'''# Chapter 23, "Project: Reading the Clipboard" style use of pyperclip on a virtual display, with the real xclip as the clipboard mechanism.
with Desk(wm=False) as d:
    import pyperclip
    print('virtual display (Xvfb); pyperclip', md.version('pyperclip'), )
    pyperclip.copy('Hello from pyperclip'); print('copy then paste ->', repr(pyperclip.paste()))
    print('xclip reads the same selection:', repr(d.sh('xclip', '-o', '-selection', 'clipboard')))
    pyperclip.copy(''); print('empty string ->', repr(pyperclip.paste()))
    pyperclip.copy('multi\nline'); print('two lines ->', repr(pyperclip.paste()))
    try: pyperclip.copy(123); print('copy(123) ->', repr(pyperclip.paste()))
    except Exception as e: print('copy(123) raises', type(e).__name__)
'''
GEOM = HEAD + r'''# Chapter 23, "Getting the Window Geometry" - the window functions of PyAutoGUI exist on Windows only; here the same facts come from xdotool and xwininfo on a virtual display.
with Desk() as d:
    import pyautogui
    print('virtual display (Xvfb); PyAutoGUI has getActiveWindow on this platform:', hasattr(pyautogui, 'getActiveWindow'), ' getAllTitles:', hasattr(pyautogui, 'getAllTitles'))
    o = d.observer(mode='events', geometry='500x300+120+80', title='geometry-demo'); time.sleep(0.5)
    wid = d.sh('xdotool', 'search', '--name', 'geometry-demo').split()[0]
    print('xdotool getwindowgeometry:', d.sh('xdotool', 'getwindowgeometry', wid).replace(wid, 'ID'))
    st = o.state(); print('Tk reports the client area at', (st['rootx'], st['rooty']), 'size', (st['w'], st['h']))
    d.sh('xdotool', 'windowmove', wid, '300', '200'); d.sh('xdotool', 'windowsize', wid, '640', '360'); time.sleep(0.5); st = o.state(); print('after windowmove 300 200 and windowsize 640 360 ->', (st['rootx'], st['rooty']), (st['w'], st['h']))
    print('the openbox frame adds a title bar and borders: client y is below the requested y:', st['rooty'] > 200)
    o.close()
'''
CHECK = HEAD + r'''# Chapter 23, "Planning Your GUI Automation Script": a checklist for a GUI script - confirm the window is there, wait until it is ready, log each step, stop on a surprise.
import logging
with Desk() as d:
    import pyautogui; pyautogui.PAUSE = 0.05
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(levelname)s %(message)s', force=True)
    log = logging.getLogger('gui'); log.info('virtual display (Xvfb), not a real screen; screen %s', tuple(pyautogui.size()))
    def wait_for(img, timeout):
        t0 = time.time()
        while time.time() - t0 < timeout:
            try: return pyautogui.locateOnScreen(img)
            except pyautogui.ImageNotFoundException: time.sleep(0.2)
        return None
    o = d.observer(mode='button', geometry='400x300+200+150', bg='#00aa00', buttons=[[100, 100]], label='Submit'); time.sleep(0.5)
    bx, by, bw, bh = o.state()['buttons'][0]; pyautogui.screenshot().crop((bx, by, bx + bw, by + bh)).save('btn.png')
    box = wait_for('btn.png', 3); log.info('button found: %s', box is not None)
    if box is None: sys.exit(1)
    pyautogui.click(pyautogui.center(box)); time.sleep(0.4); cmds = [e for e in o.events() if e['type'] == 'Command']; log.info('commands the window received: %d', len(cmds))
    from PIL import Image
    Image.open('btn.png').convert('RGB').point(lambda v: 255 - v).save('absent.png')
    log.info('an inverted copy of the button, waited for 1 s: %s', wait_for('absent.png', 1))
    assert len(cmds) == 1; o.close()
'''
XTEST = HEAD + r'''# Chapter 23 background: keys sent by PyAutoGUI (XTEST) and by xdotool key --window, as a Tk window and an xterm receive them; what is printed is what was observed, with no claim about which route an application accepts beyond that.
with Desk() as d:
    import pyautogui; pyautogui.PAUSE = 0
    o = d.observer(mode='text', geometry='500x300+100+100', focus='text'); time.sleep(0.5); pyautogui.click(300, 250); time.sleep(0.3); o.clear()
    pyautogui.write('ab'); ev = [e for e in o.events() if e['type'] == 'KeyPress']; print('virtual display (Xvfb); PyAutoGUI (XTEST) key presses seen:', [(e['keysym'], e['send_event']) for e in ev])
    wid = d.sh('xdotool', 'search', '--name', 'observer').split()[0]; o.clear()
    d.sh('xdotool', 'key', '--window', wid, 'c'); time.sleep(0.4); ev = [e for e in o.events() if e['type'] == 'KeyPress']; print('xdotool key --window key presses seen:', [(e['keysym'], e['send_event']) for e in ev])
    xt = d.start(['xterm', '-title', 'xt', '-e', 'sh', '-c', 'cat > %s' % os.path.join(d.dir, 'xt.txt')], 'xterm'); time.sleep(1.5)
    xid = d.sh('xdotool', 'search', '--name', '^xt$').split()[0]
    d.sh('xdotool', 'key', '--window', xid, 'q', 'Return'); time.sleep(0.5)
    pyautogui.moveTo(100, 100); pyautogui.moveTo(30, 30); d.sh('xdotool', 'windowfocus', xid); time.sleep(0.4); pyautogui.write('z'); pyautogui.press('enter'); time.sleep(0.8)
    got = open(os.path.join(d.dir, 'xt.txt'), errors='replace').read() if os.path.exists(os.path.join(d.dir, 'xt.txt')) else ''
    print('what the xterm shell received: xdotool "q" present:', 'q' in got, '| XTEST "z" present:', 'z' in got)
    o.close()
'''
PROGRAMS = {
    'spiralDrawing_v1_0_0.py': (SPIRAL, (), False),
    'mouseMoveAndPosition_v1_0_0.py': (MOVE, (), False),
    'clicksDragAndScroll_v1_0_0.py': (CLICKS, (), False),
    'pauseAndFailSafe_v1_0_0.py': (FAILSAFE, (), False),
    'screenshotPixelAndLocate_v1_0_0.py': (SHOT, (), False),
    'typingAndHotkeys_v1_0_0.py': (TYPE, (), False),
    'messageBoxes_v1_0_0.py': (MSGBOX, (), False),
    'lookingBusy_v1_0_0.py': (BUSY, (), False),
    'clipboardReader_v1_0_0.py': (CLIP, (), False),
    'windowGeometry_v1_0_0.py': (GEOM, (), False),
    'guiScriptChecklist_v1_0_0.py': (CHECK, (), False),
    'xtestVersusSendEvent_v1_0_0.py': (XTEST, (), False),
}
STAND_IN = {name: 'a virtual display (Xvfb) with real X clients; nobody sees the screen' for name in PROGRAMS}

if __name__ == "__main__":
    # Usage: /home/claude/venv314_ch23_latest/bin/python sen0414_ch23_corpus_base_v1_0_0.py   (exits 1 if a program does not exit 0)
    import os, subprocess, sys
    bad = 0
    for name, (code, needs, live) in PROGRAMS.items():
        r = subprocess.run([sys.executable, "-W", "ignore", "-c", code], capture_output=True, text=True, timeout=900, stdin=subprocess.DEVNULL)
        bad += r.returncode != 0
        print("=== %s (exit %d) [local stand-in: %s]" % (name, r.returncode, STAND_IN[name])); print(r.stdout.rstrip()[:3500]); print(r.stderr[-500:].rstrip())
    print("%d programs, %d did not exit 0" % (len(PROGRAMS), bad)); sys.exit(1 if bad else 0)

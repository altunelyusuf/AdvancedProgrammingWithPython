"""Chapter 23 deck examples: every console session, whole program (or excerpt), chart and table the lecture deck shows. Nothing here
carries a result; examples_run_v1_0_0.py runs it all under the interpreter given (the uv Python 3.14.6 of the chapter 23 research environment
/home/claude/venv314_ch23_latest: PyAutoGUI 0.9.54, PyScreeze 1.0.1, PyMsgBox 2.0.1, PyTweening 1.2.0, PyGetWindow 0.0.9, MouseInfo 0.1.3, pyperclip 1.11.0, python3-xlib 0.15,
Pillow 12.3.0, NumPy 2.5.4, opencv-python-headless 5.0.0.93; the rest is the standard library) and records the results. A console group is one session: its rows run in order
in one namespace (the deck check re-runs them per slide, one namespace per slide). Every console row uses the standard library only, writes no file and reads no clock and no network.

Programs: the twelve programs of the chapter's corpus (sen0414_ch23_corpus_base_v1_0_0.py), run and recorded under their own names (their lines are often wider than a slide can
show without wrapping), and the 'Cut' programs written for the deck, which do the same things in lines that fit a slide and save the pictures the slides show. EVERY
program starts ITS OWN virtual X display (Xvfb, with the openbox window manager where it needs one) and real X clients on it (a Tk window, xdotool, xclip, xterm,
the MouseInfo window); what a program prints is what those clients RECEIVED. Nothing is sent to the screen of this machine, to a person or to a service. A picture a slide shows is
saved by its program with done(), named, sized and hashed in the program's own transcript; the program check runs the program again and compares the picture with the
one inside the .pptx. KIND says what a program's output depends on, so that honesty_check can require the matching words on the slide that shows it:
  standin   the output comes from a LOCAL STAND-IN: a virtual X display (Xvfb) on which real X clients run; nobody sees the screen. EVERY program of this chapter is of this kind.
Counts that depend on timing are printed as the booleans they are (for example "took about one second: True"); a program whose transcript differs between two runs is refused
by the runner, which runs every program twice."""
__version__ = "1.0.0"
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("base23", os.path.join(HERE, "..", "sen0414_ch23_corpus_base_v1_0_0.py"))
B = importlib.util.module_from_spec(_s)
_s.loader.exec_module(B)

# the hidden lines of every Cut: the imports, Desk (a private virtual display), Obs (the window that logs what it receives), child(), then the small helpers (done, keys, btns, presses, ints, sendkey, grab, shotof, mark, ask) and VD
_KEEP = r'''import hashlib
def sha(n): return hashlib.sha256(open(n, 'rb').read()).hexdigest()[:12]
def done(n):
    k = os.environ.get('CH23_KEEP')
    if k: shutil.copy(n, os.path.join(k, os.path.basename(n)))
    print('saved %s: %d bytes, sha256 %s' % (os.path.basename(n), os.path.getsize(n), sha(n)))
def keys(o): return [(e['type'][3:], e['keysym'], e['send_event']) for e in o.events() if e['type'].startswith('Key')]
def btns(o): return [(e['type'][6:], e['num'], e['send_event']) for e in o.events() if e['type'].startswith('Button')]
def presses(o): return [(e['type'].replace('ButtonPress', 'Press'), e['num']) for e in o.events() if e['type'] in ('ButtonPress', 'DoubleClick', 'TripleClick')]
def cmds(o): return [e['button'] for e in o.events() if e['type'] == 'Command']
def short(t): return t.replace('Exception', '').replace('Error', '')
def ints(b): return tuple(int(v) for v in b)
def sendkey(d, title, ch):
    import Xlib.display, Xlib.protocol.event as XE
    dp = Xlib.display.Display(d.display); wid = int(d.sh('xdotool', 'search', '--name', title).split()[0])
    win = dp.create_resource_object('window', wid); kc = dp.keysym_to_keycode(ord(ch))
    ev = dict(time=0, root=dp.screen().root, window=win, same_screen=1, child=0, root_x=0, root_y=0, event_x=10, event_y=10, state=0, detail=kc)
    for cls in (XE.KeyPress, XE.KeyRelease): win.send_event(cls(**ev), propagate=True)
    dp.sync()
def grab(d, wid, name, hmax=None):
    from PIL import Image
    v = dict(l.split('=') for l in d.sh('xdotool', 'getwindowgeometry', '--shell', wid).split())
    d.sh('scrot', '-o', 'full.png'); x, y, w, h = (int(v[k]) for k in ('X', 'Y', 'WIDTH', 'HEIGHT'))
    Image.open('full.png').crop((x - 4, y - 30, x + w + 4, y + (hmax or h) + 4)).convert('RGB').save(name); done(name)
def xywh(o): s = o.state(); return (s['rootx'], s['rooty'], s['w'], s['h'])
def shotof(o, name, h):
    import pyautogui; st = o.state()
    pyautogui.screenshot().crop((st['rootx'], st['rooty'], st['rootx'] + st['w'], st['rooty'] + h)).convert('RGB').save(name); done(name)
def mark(shot, box, name):
    from PIL import ImageDraw
    out = shot.crop((180, 130, 620, 450)).convert('RGB'); x, y = box.left - 180, box.top - 130
    ImageDraw.Draw(out).rectangle((x - 3, y - 3, x + box.width + 2, y + box.height + 2), outline='red', width=3); out.save(name); done(name)
def ask(d, call, keys, text=None):
    code = "import pyautogui; print(repr(pyautogui.%s))" % call
    p = d.start([LATEST, '-W', 'ignore', '-c', code], 'box')
    for _ in range(100):
        if d.sh('xdotool', 'search', '--name', '^Q$'): break
        time.sleep(0.1)
    time.sleep(0.5)
    if text: d.sh('xdotool', 'type', text)
    for k in keys: d.sh('xdotool', 'key', k)
    p.wait(timeout=10); return d.out('box').strip().splitlines()[-1]
'''
_HEAD = B.HEAD + _KEEP
VD = "virtual display (Xvfb), not a real screen"

CONSOLES = {
    "title": ["import platform, importlib.metadata as m", "platform.python_version()", "m.version('pyautogui')", "m.version('pyscreeze')", "m.version('pillow')",
              "m.version('pymsgbox')"],
    "pins": ["import importlib.metadata as m, sys", "sys.version_info[:2]", "m.version('pyautogui') < '1.0.0'", "m.version('pyscreeze') >= '1.0.0'",
             "import os", "_ = os.environ.pop('DISPLAY', None)", "import pyautogui"],
}

# ---- programs written for the deck (Cuts) ---------------------------------------------------------------------------------------
def _cut(body): return _HEAD + "VD = %r\n" % VD + body

WAYLAND_BODY = r"""with Desk(wm=False) as d:
    print(VD, '| three children')
    env = dict(d.env); env.pop('DISPLAY')
    print('no DISPLAY    :', child('import pyautogui', env=env)[2])
    env = dict(d.env, XDG_SESSION_TYPE='wayland')
    shot = 'import pyautogui; pyautogui.screenshot()'
    move = 'import pyautogui as p; p.moveTo(300, 200); print(p.position())'
    rc, out, err = child(shot, env=env)
    print('wayland screenshot(): exit', rc, '|', err.split(':')[0])
    rc, out, err = child(move, env=env)
    print('wayland moveTo(300, 200): exit', rc, '| position', out[0])
"""
WAYLANDCUT = _cut(WAYLAND_BODY)

XTEST_BODY = r"""with Desk() as d:
    import pyautogui; pyautogui.PAUSE = 0
    print(VD, '| XTEST:', 'XTEST' in d.sh('xdpyinfo'))
    o = d.observer(); st = o.state()
    pyautogui.click(st['rootx'] + 50, st['rooty'] + 10)
    print('click :', btns(o))
    o.clear(); pyautogui.press('w')
    print('PyAutoGUI w :', keys(o))
    o.clear(); sendkey(d, 'observer', 'q')
    print('SendEvent q :', keys(o))
    print('both reached the entry:', repr(o.entry()))
"""
XTESTCUT = _cut(XTEST_BODY)

PAUSE_BODY = r"""with Desk(wm=False) as d:
    import pyautogui
    print(VD, '| PAUSE', pyautogui.PAUSE, '| FAILSAFE', pyautogui.FAILSAFE)
    pyautogui.PAUSE = 0.3
    def waits(f, *a):
        t = time.perf_counter(); f(*a)
        return time.perf_counter() - t > 0.25
    for f, a in ((pyautogui.moveTo, (50, 60)), (pyautogui.click, ()),
                 (pyautogui.press, ('shift',)), (pyautogui.position, ()),
                 (pyautogui.onScreen, (5, 5))):
        print('%-9s waits after the call:' % f.__name__, waits(f, *a))
"""
PAUSECUT = _cut(PAUSE_BODY)

CORNERS_BODY = r"""with Desk(wm=False) as d:
    import pyautogui; pyautogui.PAUSE = 0
    print(VD, '| size', tuple(pyautogui.size()))
    print('FAILSAFE_POINTS', sorted(pyautogui.FAILSAFE_POINTS))
    def fires(x, y):
        pyautogui.FAILSAFE = False; pyautogui.moveTo(x, y); pyautogui.FAILSAFE = True
        try: pyautogui.moveTo(500, 500)
        except pyautogui.FailSafeException: return True
        return False
    for xy in ((0, 0), (1919, 1079), (1, 1)): print(xy, 'raises:', fires(*xy))
    d.sh('xrandr', '--fb', '1280x720'); time.sleep(0.3)
    code = 'import pyautogui as p; print(tuple(p.size()), max(p.FAILSAFE_POINTS))'
    here = (tuple(pyautogui.size()), max(pyautogui.FAILSAFE_POINTS))
    print('after xrandr --fb 1280x720: this process', here)
    print('a new process', child(code, env=d.env)[1][0])
"""
CORNERSCUT = _cut(CORNERS_BODY)

MOVE_BODY = r"""with Desk(wm=False) as d:
    import pyautogui; pyautogui.PAUSE = 0
    o = d.observer(geometry='1920x1080+0+0', mode='paint', w=1900, h=1000)
    print(VD)
    for dur in (0, 0.1, 0.25, 0.5, 1.0):
        pyautogui.moveTo(500, 500); time.sleep(0.3); o.clear()
        pyautogui.moveTo(900, 700, duration=dur)
        n = sum(e['type'] == 'Motion' for e in o.events())
        print('moveTo(900, 700, duration=%s): %2d motion events' % (dur, n))
    for x, y in ((-50, -50), (5000, 5000)):
        pyautogui.FAILSAFE = False; pyautogui.moveTo(x, y)
        print('moveTo(%s, %s) ->' % (x, y), tuple(pyautogui.position()))
"""
MOVECUT = _cut(MOVE_BODY)

CLICK_BODY = r"""with Desk(wm=False) as d:
    import pyautogui; pyautogui.PAUSE = 0
    o = d.observer(geometry='1920x1080+0+0', mode='paint', w=1900, h=1000)
    pyautogui.moveTo(700, 400); time.sleep(0.3); print(VD)
    for call in ("click()", "click(button='middle')", "rightClick()",
                 "doubleClick()", "tripleClick()", "click(clicks=2, interval=0.6)"):
        time.sleep(0.7); o.clear(); eval('pyautogui.' + call)
        print('%-30s' % call, presses(o))
"""
CLICKCUT = _cut(CLICK_BODY)

DRAG_BODY = r"""with Desk(wm=False) as d:
    import pyautogui; pyautogui.PAUSE = 0
    o = d.observer(geometry='700x500+0+0', mode='paint', w=700, h=500)
    pyautogui.moveTo(200, 160); time.sleep(0.3); n = 0
    distance, change = 300, 20
    while distance > 0:
        pyautogui.drag(distance, 0, duration=0.05); distance -= change
        pyautogui.drag(0, distance, duration=0.05)
        pyautogui.drag(-distance, 0, duration=0.05); distance -= change
        pyautogui.drag(0, -distance, duration=0.05); n += 4
    im = pyautogui.screenshot().crop((0, 0, 700, 500)).convert('L')
    box = im.point(lambda v: 255 * (v < 128)).getbbox()
    print(VD); print('spiral:', n, 'drag calls, ink inside the box', box)
    ev = [e['type'] for e in o.events()]
    print('presses', ev.count('ButtonPress'), '| releases', ev.count('ButtonRelease'))
    im.convert('RGB').save('spiral.png'); done('spiral.png')
"""
DRAGCUT = _cut(DRAG_BODY)

SCROLL_BODY = r"""with Desk() as d:
    import pyautogui; pyautogui.PAUSE = 0
    print(VD)
    for name, py in (('Tk 9', LATEST), ('Tk 8.6', TK86)):
        o = d.observer(mode='text', focus='text', fill=300, lines=12, py=py)
        st = o.state(); top = lambda: int(o.state()['top'].split('.')[0])
        pyautogui.moveTo(st['rootx'] + 100, st['rooty'] + 150); row = {}
        for n in (-1, -2, -3, -10):
            pyautogui.scroll(60); time.sleep(0.4); b = top()
            pyautogui.scroll(n); o.settle(); time.sleep(0.4); row[n] = top() - b
        print('lines moved, %s %s:' % (name, st['tk']), row); o.close()
"""
SCROLLCUT = _cut(SCROLL_BODY)

MOUSEINFO_BODY = r"""with Desk() as d:
    print(VD, '| mouseInfo() in two interpreters')
    cmd = 'import pyautogui; pyautogui.mouseInfo()'
    for name, py in (('Tk 9.0.3, Python 3.14.6', LATEST),
                     ('Tk 8.6.14, Python 3.12.3', TK86)):
        p = d.start([py, '-W', 'ignore', '-c', cmd], 'mi'); time.sleep(4)
        win = d.sh('xdotool', 'search', '--name', 'MouseInfo').split()
        err = d.out('mi').strip().splitlines()[-1] if p.poll() else ''
        err = err.split(': must')[0].replace('_tkinter.', '')
        print('%-25s' % name, 'running:', p.poll() is None, '| window:', bool(win), err)
        if win:
            for _ in range(4): d.sh('xdotool', 'key', 'Tab'); time.sleep(0.2)
            grab(d, win[0], 'mouseInfo.png', hmax=250)
        if p.poll() is None: os.killpg(p.pid, signal.SIGTERM)
"""
MOUSEINFOCUT = _cut(MOUSEINFO_BODY)

SHOT_BODY = r"""with Desk(wm=False) as d:
    import pyautogui; pyautogui.PAUSE = 0
    d.observer(mode='button', geometry='400x300+200+150', bg='#b0b0af',
               buttons=[[100, 100]]); time.sleep(0.5)
    im = pyautogui.screenshot(); inside = (210, 160)
    print(VD, '|', type(im).__name__, im.size, im.mode)
    cases = (((176, 176, 175), 0), ((177, 176, 175), 0), ((177, 176, 175), 1))
    ok = [pyautogui.pixelMatchesColor(*inside, c, tolerance=t) for c, t in cases]
    print('pixelMatchesColor ->', ok)
    print('pixel(210, 160) ->', pyautogui.pixel(*inside), '| (5, 5)', im.getpixel((5, 5)))
    try: pyautogui.pixel(inside)
    except TypeError as e: print('pixel((210, 160)) raises TypeError:', e)
    im.resize((480, 270)).save('screen.png'); done('screen.png')
"""
SHOTCUT = _cut(SHOT_BODY)

LOCATE_BODY = r"""with Desk(wm=False) as d:
    import pyautogui; pyautogui.PAUSE = 0
    o = d.observer(mode='button', geometry='400x300+200+150', bg='#00aa00',
                   buttons=[[100, 100], [100, 180]]); time.sleep(0.5)
    shot = pyautogui.screenshot(); bx, by, bw, bh = o.state()['buttons'][0]
    shot.crop((bx, by, bx + bw, by + bh)).save('submit.png')
    box = pyautogui.locateOnScreen('submit.png')
    boxes = list(pyautogui.locateAllOnScreen('submit.png'))
    print(VD, '| found', ints(box))
    print('locateAll', [ints(b) for b in boxes], '| center', ints(pyautogui.center(box)))
    o.clear(); pyautogui.click(boxes[1]); time.sleep(0.4)
    print('click(boxes[1]) pressed button', cmds(o)); mark(shot, box, 'located.png')
"""
LOCATECUT = _cut(LOCATE_BODY)

MATCH_BODY = r"""with Desk(wm=False) as d:
    import pyautogui; pyautogui.PAUSE = 0
    o = d.observer(mode='button', geometry='400x300+200+150', bg='#00aa00',
                   buttons=[[100, 100]]); time.sleep(0.5)
    bx, by, bw, bh = o.state()['buttons'][0]
    btn = pyautogui.screenshot().crop((bx, by, bx + bw, by + bh))
    btn.save('exact.png'); btn.putpixel((5, 5), (0, 0, 0)); btn.save('off.png')
    calls = ("'exact.png'", "'off.png'", "'off.png', confidence=0.9",
             "'off.png', grayscale=True")
    probe = ("import pyautogui as p\n"
             "try: print(type(p.locateOnScreen(%s)).__name__)\n"
             "except Exception as e: print(type(e).__name__)")
    print(VD, '| exact, off, off 0.9, off gray')
    for name, py in (('OpenCV', LATEST), ('no OpenCV', NOCV),
                     ('PyScreeze 0.1.28', OLDSCREEZE)):
        r = [child(probe % c, py=py, env=d.env)[1][0] for c in calls]
        print('%-17s' % name, [short(x) for x in r])
"""
MATCHCUT = _cut(MATCH_BODY)

WINDOW_BODY = r"""with Desk() as d:
    import pyautogui
    names = ('getActiveWindow', 'getAllWindows', 'getWindowsAt',
             'getWindowsWithTitle', 'getAllTitles', 'getActiveWindowTitle')
    have = [n for n in names if hasattr(pyautogui, n)]
    print(VD, '| window functions in pyautogui:', have)
    err = child('import pygetwindow', env=d.env)[2]
    print('import pygetwindow ->', err.split(':')[0])
    o = d.observer(mode='events', geometry='500x300+120+80', title='demo'); time.sleep(0.5)
    wid = d.sh('xdotool', 'search', '--name', 'demo').split()[0]
    print('Tk client area x, y, w, h', xywh(o))
    d.sh('xdotool', 'windowmove', wid, '300', '200')
    d.sh('xdotool', 'windowsize', wid, '640', '360'); time.sleep(0.5)
    print('after windowmove 300 200 and windowsize 640 360', xywh(o))
    print('openbox adds a title bar, so client y is below 200:', xywh(o)[1] > 200)
    grab(d, wid, 'frame.png')
"""
WINDOWCUT = _cut(WINDOW_BODY)

TYPE_BODY = r"""with Desk() as d:
    import pyautogui; pyautogui.PAUSE = 0
    o = d.observer(mode='text', geometry='600x300+100+100', focus='text')
    time.sleep(0.5); pyautogui.click(300, 250); time.sleep(0.3)
    print(VD); pyautogui.write('Hello, world!'); print(repr(o.text()))
    pyautogui.write(['a', 'b', 'left', 'left', 'X', 'Y'])
    print('write([a, b, left, left, X, Y]) ->', repr(o.text()))
    pyautogui.keyDown('shift'); pyautogui.press('4'); pyautogui.keyUp('shift')
    print('shift down, 4, shift up ->', repr(o.text()[-3:]))
    pyautogui.hotkey('ctrl', 'a'); pyautogui.press('delete')
    print('hotkey(ctrl, a), delete ->', repr(o.text()))
    pyautogui.write('Hello, world!'); pyautogui.click(1000, 800); time.sleep(0.6)
    shotof(o, 'typed.png', 120)
"""
TYPECUT = _cut(TYPE_BODY)

KEYS_BODY = r"""with Desk() as d:
    import pyautogui; pyautogui.PAUSE = 0
    o = d.observer(mode='text', geometry='600x300+100+100', focus='text')
    time.sleep(0.5); pyautogui.click(300, 250); time.sleep(0.3)
    print(VD, '| KEYBOARD_KEYS:', len(pyautogui.KEYBOARD_KEYS), 'names')
    for call in ("press('nokey')", "press('SHIFT')", "keyDown('nokey')"):
        try: eval('pyautogui.' + call); r = 'raised nothing'
        except Exception as e: r = type(e).__name__
        print('%-18s' % call, r, '| typed', repr(o.text()))
    pyautogui.write(['a', 'nokey', 'b']); pyautogui.write('café')
    print('write a, nokey, b, then café typed', repr(o.text()))
    print('A in the list:', 'A' in pyautogui.KEYBOARD_KEYS)
"""
KEYSCUT = _cut(KEYS_BODY)

CLIP_BODY = r"""with Desk() as d:
    import pyautogui, pyperclip; pyautogui.PAUSE = 0
    o = d.observer(mode='text', focus='text',
                   geometry='600x300+100+100')
    time.sleep(0.5); pyautogui.click(300, 250); time.sleep(0.3)
    print(VD, '| pyperclip', md.version('pyperclip'))
    pyautogui.write('Hello, world!\nsecond line')
    o.clear(); pyautogui.hotkey('ctrl', 'alt', 'shift', 's')
    ks = [k.split('_')[0] for t, k, s in keys(o)]
    print('down, then up:', *ks)
    pyautogui.hotkey('ctrl', 'a'); pyautogui.hotkey('ctrl', 'c')
    time.sleep(1); text = pyperclip.paste()
    print('paste():', repr(text))
    pyautogui.press('end'); pyautogui.hotkey('ctrl', 'v')
    print('ctrl+v pasted it again:', o.text() == text * 2)
"""
CLIPCUT = _cut(CLIP_BODY)

BOX_BODY = r"""with Desk() as d:
    print(VD, '| message boxes answered with the keyboard')
    print('confirm + Return   ->', ask(d, "confirm('Go?', 'Q')", ['Return']))
    print('confirm + Escape   ->', ask(d, "confirm('Go?', 'Q')", ['Escape']))
    print('prompt + Return    ->', ask(d, "prompt('Name?', 'Q')", ['Return']))
    print('prompt + Escape    ->', ask(d, "prompt('Name?', 'Q')", ['Escape']))
    print('password + typing  ->', ask(d, "password('Pass?', 'Q')", ['Return'], 's3cret'))
    t = time.perf_counter(); r = ask(d, "confirm('Go?', 'Q', timeout=1500)", [])
    took = time.perf_counter() - t - 0.5
    print('confirm(timeout=1500) ->', r, '| about 1.5 s:', 1.2 < took < 3.0)
"""
BOXCUT = _cut(BOX_BODY)

BUSY_BODY = r"""with Desk(wm=False) as d:
    import pyautogui; pyautogui.PAUSE = 0
    idle = lambda: int(d.sh('xprintidle'))
    pyautogui.moveTo(800, 500); xs = []
    print(VD, '| looking busy')
    for _ in range(3):
        pyautogui.move(-1, 0); xs.append(pyautogui.position().x)
        pyautogui.move(1, 0); xs.append(pyautogui.position().x)
    print('x after each move:', xs, '| ends at', tuple(pyautogui.position()))
    time.sleep(1.2); print('idle after a wait:', idle() > 1000)
    pyautogui.position(); pyautogui.size()
    print('after position() and size(): still idle:', idle() > 1000)
    pyautogui.move(1, 0); print('after move(1, 0): idle was reset:', idle() < 400)
    time.sleep(1.2); pyautogui.press('shift')
    print('after press(shift): idle was reset:', idle() < 400)
"""
BUSYCUT = _cut(BUSY_BODY)

# ---- charts and tables (re-computed by the deck check) -----------------------------------------------------------------
CHARTS = {
    "moveEvents": {
        "setup": "import json, os, re\nR = json.load(open(os.path.join(HERE, 'examples_out_v1_0_0.json')))['_programs']['moveCut_v1_0_0.py']['transcript']\n"
                 "ROWS = [('%s s' % m.group(1), int(m.group(2))) for m in re.finditer(r'duration=([0-9.]+)\\): +(\\d+) motion events', R)]\n",
        "expr": "ROWS"},
    "scrollLines": {
        "setup": "import json, os, re\nR = json.load(open(os.path.join(HERE, 'examples_out_v1_0_0.json')))['_programs']['scrollCut_v1_0_0.py']['transcript']\n"
                 "ROWS = []\nfor m in re.finditer(r'lines moved, (Tk [0-9.]+) [0-9.]+: (\\{.*\\})', R):\n    for k, v in eval(m.group(2)).items():\n        ROWS.append(('%s, %d' % (m.group(1), k), v))\n",
        "expr": "ROWS"},
}

_PROBE = r'''
import json, sys, importlib.metadata as md, warnings
warnings.simplefilter('ignore')
r = {'Python': sys.version.split()[0]}
def v(n):
    try: return md.version(n)
    except md.PackageNotFoundError: return 'none'
r['PyAutoGUI'] = v('pyautogui'); r['PyScreeze'] = v('pyscreeze'); r['Pillow'] = v('pillow'); r['OpenCV'] = v('opencv-python-headless')
try:
    import tkinter; r['Tk'] = str(tkinter.Tcl().eval('info patchlevel'))
except BaseException as e:
    r['Tk'] = type(e).__name__
try:
    import pyautogui
    r['import'] = 'ok'; r['size()'] = str(tuple(pyautogui.size()))
except BaseException as e:
    r['import'] = type(e).__name__; r['size()'] = '-'
print(json.dumps(r))
'''
INTERPS = [("3.14.6 newest", "/home/claude/venv314_ch23_latest/bin/python"), ("3.14.6 no OpenCV", "/home/claude/venv314_ch23_nocv/bin/python"),
           ("3.14.6 PyScreeze 0.1.28", "/home/claude/venv314_ch23_oldscreeze/bin/python"), ("3.12.3 Tk 8.6", "/home/claude/venv312_ch23_tk86/bin/python"),
           ("3.14.6 empty", "/home/claude/venv314_ch23_bare/bin/python")]
_ROWS = [("Python", "Python"), ("PyAutoGUI", "PyAutoGUI"), ("PyScreeze", "PyScreeze"), ("OpenCV", "OpenCV"), ("Tk", "Tk"), ("import pyautogui", "import"), ("size()", "size()")]

_XVFB = r'''
import os, subprocess, time
N = 300 + os.getpid() % 500
while os.path.exists('/tmp/.X11-unix/X%d' % N) or os.path.exists('/tmp/.X%d-lock' % N): N += 1
XV = subprocess.Popen(['Xvfb', ':%d' % N, '-screen', '0', '1920x1080x24', '-nolisten', 'tcp'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
for _ in range(200):
    if os.path.exists('/tmp/.X11-unix/X%d' % N): break
    time.sleep(0.05)
time.sleep(0.3)
ENV = {k: v for k, v in os.environ.items() if k not in ('WAYLAND_DISPLAY', 'PYTHONPATH')}; ENV.update(DISPLAY=':%d' % N, XDG_SESSION_TYPE='x11')
'''

TABLES = {
    "environments": {
        "setup": "import json, subprocess\n" + _XVFB + "PROBE = %r\nINTERPS = %r\nres = []\ntry:\n    for v, p in INTERPS:\n"
                 "        r = subprocess.run([p, '-c', PROBE], capture_output=True, text=True, env=ENV, stdin=subprocess.DEVNULL)\n"
                 "        assert r.returncode == 0, (v, r.stderr[-300:])\n        res.append(json.loads(r.stdout.strip().splitlines()[-1]))\nfinally:\n    XV.terminate(); XV.wait()\n"
                 "ROWS = %r\ndef fmt(v, key):\n    if key == 'size()': return v.strip('()').replace(', ', 'x')\n    return v.replace('ModuleNotFoundError', 'ModuleNotFound')\n" % (_PROBE, INTERPS, _ROWS),
        "expr": "[['check'] + [v for v, p in INTERPS]] + [[label] + [fmt(x.get(key, '-'), key) for x in res] for label, key in ROWS]"},
    "releases": {
        "setup": "import json, os, re\nT = json.load(open(os.path.join(HERE, '..', 'ch23-page', 'interpreter_record_v1_0_0.json')))['package release rows']\n"
                 "def row(n):\n    m = re.match(r'pyautogui (\\S+) with pyscreeze (\\S+) on (\\S+)', n)\n    if m: return [m.group(1), m.group(2), m.group(3)]\n"
                 "    m = re.match(r'pyscreeze (\\S+) with pyautogui (\\S+) on (\\S+)', n)\n    return [m.group(2), m.group(1), m.group(3)]\n"
                 "def cell(n):\n    v = T[n].get('click(image one pixel off)')\n    if v is None: return 'does not import'\n    return v[0].replace('builtins.', '').replace('pyautogui.', '').rstrip(': ').replace('non-iterable NoneType object', 'None').replace(\"'NoneType' object is not subscriptable\", 'None is not subscriptable')\n"
                 "ROWS = [row(n) + [cell(n)] for n in T]\n",
        "expr": "[['PyAutoGUI', 'PyScreeze', 'Python', 'click, image one pixel off']] + ROWS"},
    "configurations": {
        "setup": "import json, os\nT = json.load(open(os.path.join(HERE, '..', 'ch23-page', 'third_party_record_v1_0_0.json')))['items']\n"
                 "CF = list(T[0]['output'])\nROW = {'LATEST': 'newest', 'NOCV': 'no OpenCV', 'OLDSCREEZE': 'PyScreeze 0.1.28', 'TK86': 'Python 3.12.3, Tk 8.6', 'BARE': 'empty'}\n"
                 "def n(i):\n    s = [x for l in T[i]['output']['results'] for x in l['statements']]\n    return '%d of %d' % (sum(bool(x['as printed'].get('matches the book')) for x in s), len(s))\n"
                 "def ran(i):\n    s = [x for l in T[i]['output']['results'] for x in l['statements']]\n    return '%d' % sum(not x['as printed'].get('raised') for x in s)\n"
                 "def pkg(c, k):\n    v = T[0]['output'][c][k]\n    return '-' if v is None else str(v)\n",
        "expr": "[['row', 'Python', 'PyAutoGUI', 'PyScreeze', 'Tk', 'ran without an exception', 'statements = book']] + "
                "[[ROW[c], pkg(c, 'python'), pkg(c, 'pyautogui'), pkg(c, 'pyscreeze'), pkg(c, 'Tk'), ran(2 + i), n(2 + i)] for i, c in enumerate(CF)]"},
}

PROGRAMS = {
    # the twelve programs of the corpus, recorded under their own names
    **{k: v for k, v in B.PROGRAMS.items()},
    "waylandCut_v1_0_0.py": (WAYLANDCUT, (), True),
    "xtestCut_v1_0_0.py": (XTESTCUT, (), True),
    "pauseCut_v1_0_0.py": (PAUSECUT, (), True),
    "cornersCut_v1_0_0.py": (CORNERSCUT, (), True),
    "moveCut_v1_0_0.py": (MOVECUT, (), True),
    "clickCut_v1_0_0.py": (CLICKCUT, (), True),
    "dragCut_v1_0_0.py": (DRAGCUT, (), True),
    "scrollCut_v1_0_0.py": (SCROLLCUT, (), True),
    "mouseinfoCut_v1_0_0.py": (MOUSEINFOCUT, (), True),
    "shotCut_v1_0_0.py": (SHOTCUT, (), True),
    "locateCut_v1_0_0.py": (LOCATECUT, (), True),
    "matchCut_v1_0_0.py": (MATCHCUT, (), True),
    "windowCut_v1_0_0.py": (WINDOWCUT, (), True),
    "typeCut_v1_0_0.py": (TYPECUT, (), True),
    "keysCut_v1_0_0.py": (KEYSCUT, (), True),
    "clipCut_v1_0_0.py": (CLIPCUT, (), True),
    "boxCut_v1_0_0.py": (BOXCUT, (), True),
    "busyCut_v1_0_0.py": (BUSYCUT, (), True),
}
KIND = {n: "standin" for n in PROGRAMS}
STANDKEY = {n: ("Virtual display", "not a real screen") for n in PROGRAMS}
# the pictures a slide shows: file name -> the program that makes it
IMAGES = {"spiral.png": "dragCut_v1_0_0.py", "mouseInfo.png": "mouseinfoCut_v1_0_0.py", "screen.png": "shotCut_v1_0_0.py", "located.png": "locateCut_v1_0_0.py",
          "frame.png": "windowCut_v1_0_0.py", "typed.png": "typeCut_v1_0_0.py"}
EQUIV = {}
SUBSET = {}

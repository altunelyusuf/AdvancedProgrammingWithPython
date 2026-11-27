"""Chapter 23 lab helpers, version 1.0.0 (SEN0414, Lineage14): the hidden helpers of the chapter 23 deck examples. They start a PRIVATE virtual X display (Xvfb, with the window manager openbox where an example needs one),
real X clients on it (a Tk window that logs every event it receives, xdotool, xclip) and stop them again. Nothing is sent to the screen of this machine, to a person or to a service; what an example prints is what those
clients RECEIVED. The base is the chapter's corpus base (sen0414_ch23_corpus_base_v1_0_0.py); begin() starts the next display and forgets the PyAutoGUI modules of the previous one, so that every example connects to its own display."""
__version__ = "1.0.0"
import importlib.util
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("base23", os.path.join(_HERE, "..", "..", "sen0414_ch23_corpus_base_v1_0_0.py"))
B = importlib.util.module_from_spec(_s)
_s.loader.exec_module(B)
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
exec(B.HEAD + _KEEP, globals())

_PURGE = ("pyautogui", "pyscreeze", "pymsgbox", "pytweening", "pygetwindow", "mouseinfo", "Xlib", "pyperclip")
_cur = [None]


def end():
    if _cur[0] is not None:
        _cur[0].__exit__(None, None, None)
        _cur[0] = None


def begin(wm=True):
    """end the previous display, start a new one and return it (os.environ['DISPLAY'] points to it)"""
    end()
    for m in list(sys.modules):
        if m.split(".")[0] in _PURGE:
            del sys.modules[m]
    os.chdir(tempfile.mkdtemp(prefix="ch23work"))   # each example works in its own folder; the builder keeps it so that a result visual can read the files the example saved
    d = Desk(wm=wm)
    d.__enter__()
    _cur[0] = d
    return d


import atexit
atexit.register(end)

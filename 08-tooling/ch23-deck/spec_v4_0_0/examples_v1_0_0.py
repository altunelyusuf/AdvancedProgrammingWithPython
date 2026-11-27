"""Chapter 23 deck examples, version 1.0.0 (SEN0414, Lineage14): the 15 code examples of the chapter 23 lecture deck (Controlling the Keyboard and Mouse), in slide order = page-tab order.
Every example runs the real PyAutoGUI 0.9.54 on a PRIVATE virtual X display (Xvfb, with the window manager openbox where an example needs one): nobody sees that display and nothing is sent to the screen of this machine.
The hidden `setup` lines start the display (begin()) and a small Tk window `watch` that logs every event it receives, so an example can print what the program on the display RECEIVED. Windows and macOS were not run.
`groups` are the code boxes of a slide with the explanation beside each; every box parses on its own."""
__version__ = "1.0.0"

LAB = ["from lab23_v1_0_0 import *"]


def _s(wm, *more):
    return LAB + ["d = begin(wm=%s)" % wm] + list(more)


FAST = "import pyautogui; pyautogui.PAUSE = 0"
PAINT = "watch = d.observer(geometry='1920x1080+0+0', mode='paint', w=1900, h=1000)"
TEXT = "watch = d.observer(mode='text', geometry='600x300+100+100', focus='text')"
CLICKTEXT = ["time.sleep(0.5)", "import pyautogui; pyautogui.click(300, 250); time.sleep(0.3)"]
BUTTONS = "watch = d.observer(mode='button', geometry='400x300+200+150', bg='#00aa00', buttons=[[100, 100], [100, 180]]); time.sleep(0.5)"

EXAMPLES = [
    # ------------------------------------------------------------ part 1: the display and the first moves
    dict(id="pins", name="The packages and the display", title="Which versions run, and does the display answer?", part=1, visual="pins",
         setup=_s(False),
         concepts=["PyAutoGUI", "pyautogui", "pyautogui.size()", "Figure 23-1: the coordinates of a computer screen with 1920x1080 resolution"],
         groups=[
             (["import importlib.metadata as md, platform", "print(platform.python_version())",
               "print([md.version(p) for p in ('pyautogui', 'pyscreeze', 'pillow', 'pymsgbox')])"],
              "The versions are printed, not assumed: pyautogui is still below 1.0.0."),
             (["import pyautogui", "print(pyautogui.size())", "print(pyautogui.position())"],
              "size() is the screen; position() is the pointer, which starts in the middle."),
         ]),
    dict(id="session", name="Without a display, and under Wayland", title="What happens when no screen is there?", part=1, visual="session",
         setup=_s(False),
         concepts=["Setting Up Accessibility Apps on macOS", "Logouts"],
         groups=[
             (["code = 'import pyautogui; print(pyautogui.size())'", "env = dict(d.env); env.pop('DISPLAY')",
               "print(child(code, env=env)[2])"],
              "Without DISPLAY the import fails at once, with an error that names the missing variable."),
             (["env = dict(d.env, XDG_SESSION_TYPE='wayland')", "shot = 'import pyautogui; pyautogui.screenshot()'",
               "print(child(shot, env=env)[2].split(':')[0])", "print(child(code, env=d.env)[1])"],
              "On a Wayland session the screenshot is refused; the same code works on an X display."),
         ]),
    dict(id="xtest", name="How a click reaches a window", title="Does the window know the input is synthetic?", part=1, visual="xtest",
         setup=_s(True, "watch = d.observer()", FAST),
         concepts=["Staying on Track", "pyautogui.click()", "pyautogui.press()"],
         groups=[
             (["import pyautogui", "st = watch.state()", "pyautogui.click(st['rootx'] + 50, st['rooty'] + 10)",
               "print('click      :', btns(watch))"],
              "The click arrives as a real button event; send_event False means it came from the server."),
             (["watch.clear(); pyautogui.press('w')", "print('press w    :', keys(watch))",
               "watch.clear(); sendkey(d, 'observer', 'q')", "print('SendEvent q:', keys(watch))",
               "print('both reached the entry:', repr(watch.entry()))"],
              "A key sent with SendEvent is flagged True; PyAutoGUI's key is not flagged."),
         ]),
    dict(id="pause", layout="left", name="Pauses", title="PAUSE: a wait after most calls", part=2, visual="pause",
         setup=_s(False),
         concepts=["Pauses and Fail-Safes", "pyautogui.PAUSE", "pyautogui.sleep()", "pyautogui.countdown()"],
         groups=[
             (["import time, pyautogui", "print('PAUSE', pyautogui.PAUSE, '| FAILSAFE', pyautogui.FAILSAFE)", "pyautogui.PAUSE = 0.3"],
              "The default pause is 0.1 seconds; here it is raised to 0.3 to make it easy to measure."),
             (["def waits(f, *a):", "    t = time.perf_counter(); f(*a)", "    return time.perf_counter() - t > 0.25",
               "calls = [(pyautogui.moveTo, (50, 60)), (pyautogui.click, ()),",
               "         (pyautogui.press, ('shift',)), (pyautogui.position, ()),", "         (pyautogui.onScreen, (5, 5))]",
               "for f, a in calls:", "    print('%-9s waits after the call:' % f.__name__, waits(f, *a))"],
              "Calls that act wait; calls that only ask do not."),
         ]),
    dict(id="corners", name="The fail-safe corners", title="The four corners stop a runaway script", part=2, layout="left", visual="corners",
         setup=_s(False, "CODE = 'import pyautogui as p; print(tuple(p.size()))'"),
         concepts=["Pauses and Fail-Safes", "pyautogui.FailSafeException", "pyautogui.size()"],
         groups=[
             (["import pyautogui; pyautogui.PAUSE = 0", "print('FAILSAFE_POINTS', sorted(pyautogui.FAILSAFE_POINTS))"],
              "The points are the four corners of the screen."),
             (["def fires(x, y):", "    pyautogui.FAILSAFE = False; pyautogui.moveTo(x, y)", "    pyautogui.FAILSAFE = True",
               "    try: pyautogui.moveTo(500, 500)", "    except pyautogui.FailSafeException: return True", "    return False",
               "for xy in ((0, 0), (1919, 1079), (1, 1)):", "    print(xy, 'raises:', fires(*xy))"],
              "A pointer in a corner makes the next call raise."),
             (["d.sh('xrandr', '--fb', '1280x720'); time.sleep(0.3)", "print('this process:', tuple(pyautogui.size()))",
               "print('a new process:', child(CODE, env=d.env)[1][0])"],
              "A running script keeps its old corners."),
         ]),
    # ------------------------------------------------------------ part 2: the mouse
    dict(id="move", name="Moving the mouse", title="moveTo(): how many steps does a move take?", part=3, visual="move",
         setup=_s(False, FAST, PAINT),
         concepts=["Controlling Mouse Movement", "Moving the Mouse", "Getting the Current Position", "pyautogui.moveTo()", "pyautogui.move()", "pyautogui.position()", "duration"],
         groups=[
             (["import pyautogui", "for dur in (0, 0.1, 0.25, 0.5, 1.0):", "    pyautogui.moveTo(500, 500); time.sleep(0.3); watch.clear()",
               "    pyautogui.moveTo(900, 700, duration=dur)", "    n = sum(e['type'] == 'Motion' for e in watch.events())",
               "    print('moveTo(900, 700, duration=%s): %2d motion events' % (dur, n))"],
              "A longer duration makes more small steps; duration 0 jumps in one."),
             (["for x, y in ((-50, -50), (5000, 5000)):", "    pyautogui.FAILSAFE = False; pyautogui.moveTo(x, y)",
               "    print('moveTo(%s, %s) ->' % (x, y), tuple(pyautogui.position()))"],
              "A target outside the screen is cut to the nearest point of the screen."),
         ]),
    dict(id="click", name="Clicking", title="click(): which button events does each call send?", part=3, visual="click",
         setup=_s(False, FAST, PAINT, "import pyautogui; pyautogui.moveTo(700, 400); time.sleep(0.3)",
                  "def show(label):", "    print('%-30s' % label, presses(watch)); time.sleep(0.7); watch.clear()"),
         concepts=["Controlling Mouse Interaction", "Clicking", "pyautogui.click()", "button='left'"],
         groups=[
             (["import pyautogui", "pyautogui.click(); show('click()')", "pyautogui.click(button='middle'); show(\"click(button='middle')\")",
               "pyautogui.rightClick(); show('rightClick()')"],
              "Buttons are numbered 1 left, 2 middle, 3 right."),
             (["pyautogui.doubleClick(); show('doubleClick()')", "pyautogui.tripleClick(); show('tripleClick()')",
               "pyautogui.click(clicks=2, interval=0.6); show('click(clicks=2, interval=0.6)')"],
              "A double click needs its clicks close together; a long interval makes two single clicks."),
         ]),
    dict(id="drag", layout="left", name="Dragging: the spiral", title="drag(): the book's spiral, drawn on the display", part=3, visual="drag",
         setup=_s(False, FAST, "watch = d.observer(geometry='700x500+0+0', mode='paint', w=700, h=500)", "import pyautogui; pyautogui.moveTo(200, 160); time.sleep(0.3)"),
         concepts=["Dragging", "pyautogui.dragTo()", "pyautogui.drag()", "spiralDraw.py", "Figure 23-2: the results from the pyautogui.drag() example, drawn with MS Paint brushes"],
         groups=[
             (["import pyautogui", "n = 0", "distance, change = 300, 20", "while distance > 0:",
               "    pyautogui.drag(distance, 0, duration=0.05); distance -= change", "    pyautogui.drag(0, distance, duration=0.05)",
               "    pyautogui.drag(-distance, 0, duration=0.05); distance -= change", "    pyautogui.drag(0, -distance, duration=0.05); n += 4"],
              "Each drag() is relative to the pointer: right, down, left, up, each side 20 pixels shorter."),
             (["im = pyautogui.screenshot().crop((0, 0, 700, 500)).convert('L')", "ink = im.point([255] * 128 + [0] * 128)",
               "print('spiral:', n, 'drag calls, ink inside the box', ink.getbbox())", "ev = [e['type'] for e in watch.events()]",
               "print('presses', ev.count('ButtonPress'))", "print('releases', ev.count('ButtonRelease'))", "im.convert('RGB').save('spiral.png'); done('spiral.png')"],
              "The window drew what the drag moved; every press has its release."),
         ]),
    dict(id="scroll", layout="left", name="Scrolling", title="scroll(): how many lines is one click?", part=3, visual="scroll",
         setup=_s(True, FAST, "def top(w): return int(w.state()['top'].split('.')[0])",
                  "def text_window(py): return d.observer(mode='text', focus='text', fill=300, lines=12, py=py)"),
         concepts=["Scrolling", "pyautogui.scroll()"],
         groups=[
             (["import pyautogui", "def lines_moved(py, name):",
               "    watch = text_window(py); st = watch.state(); row = {}",
               "    pyautogui.moveTo(st['rootx'] + 100, st['rooty'] + 150)", "    for n in (-1, -2, -3, -10):",
               "        pyautogui.scroll(60); time.sleep(0.4); before = top(watch)",
               "        pyautogui.scroll(n); watch.settle(); time.sleep(0.4)", "        row[n] = top(watch) - before",
               "    print('lines moved, %s %s:' % (name, st['tk']), row)", "    watch.close()"],
              "Scroll up, note the top line, scroll by n clicks, note again."),
             (["lines_moved(LATEST, 'Tk 9')", "lines_moved(TK86, 'Tk 8.6')"],
              "The same clicks move a different number of lines under Tk 9 and Tk 8.6."),
         ]),
    # ------------------------------------------------------------ part 3: the screen
    dict(id="shot", layout="left", name="Screenshots and pixels", title="screenshot() and pixel(): what the screen shows", part=4, visual="shot",
         setup=_s(False, FAST, "watch = d.observer(mode='button', geometry='400x300+200+150', bg='#b0b0af', buttons=[[100, 100]]); time.sleep(0.5)"),
         concepts=["Taking Screenshots", "pyautogui.screenshot()", "pyautogui.pixel()", "pyautogui.pixelMatchesColor()", "screenshot.png"],
         groups=[
             (["import pyautogui", "im = pyautogui.screenshot(); inside = (210, 160)", "print(type(im).__name__, im.size, im.mode)",
               "print('pixel(210, 160) ->', pyautogui.pixel(*inside))", "print('pixel (5, 5) ->', im.getpixel((5, 5)))"],
              "The screenshot is a Pillow image of the whole screen; pixel() reads one point."),
             (["cases = (((176, 176, 175), 0), ((177, 176, 175), 0),", "         ((177, 176, 175), 1))", "for c, t in cases:",
               "    ok = pyautogui.pixelMatchesColor(*inside, c, tolerance=t)", "    print(c, t, ok)",
               "try: pyautogui.pixel(inside)", "except TypeError as e: print('pixel((210, 160)):', e)",
               "im.resize((480, 270)).save('screen.png'); done('screen.png')"],
              "A tolerance of 1 accepts a color that is one step off; a point must be two numbers."),
         ]),
    dict(id="locate", layout="left", name="Finding a button", title="locateOnScreen(): where is the button?", part=4, visual="locate",
         setup=_s(False, FAST, BUTTONS),
         concepts=["Image Recognition", "pyautogui.locateOnScreen()", "pyautogui.locateAllOnScreen()", "submit.png", "Figure 23-1: the coordinates of a computer screen with 1920x1080 resolution"],
         groups=[
             (["import pyautogui", "shot = pyautogui.screenshot()", "bx, by, bw, bh = watch.state()['buttons'][0]",
               "shot.crop((bx, by, bx + bw, by + bh)).save('submit.png')", "box = pyautogui.locateOnScreen('submit.png')",
               "boxes = list(pyautogui.locateAllOnScreen('submit.png'))", "print('found', ints(box))"],
              "The button is cut out of a screenshot and searched for on the screen."),
             (["print('locateAll', [ints(b) for b in boxes])", "print('center', ints(pyautogui.center(box)))",
               "watch.clear(); pyautogui.click(boxes[1]); time.sleep(0.4)", "print('click(boxes[1]) pressed button', cmds(watch))",
               "mark(shot, box, 'located.png')"],
              "Two identical buttons are found; clicking the second box presses the second button."),
         ]),
    dict(id="match", name="Exact matches and missing images", title="When does locateOnScreen() find nothing?", part=4, layout="left", visual="match",
         setup=_s(False, FAST, "watch = d.observer(mode='button', geometry='400x300+200+150', bg='#00aa00', buttons=[[100, 100]]); time.sleep(0.5)",
                  "ENVS = (('OpenCV', LATEST), ('no OpenCV', NOCV), ('PyScreeze 0.1.28', OLDSCREEZE))",
                  "PROBE = 'import pyautogui as p\\ntry: print(type(p.locateOnScreen(%s)).__name__)\\nexcept Exception as e: print(type(e).__name__)'"),
         concepts=["Image Recognition", "pyautogui.locateOnScreen()", "pyautogui.ImageNotFoundException", "PyAutoGUI", "Selenium"],
         groups=[
             (["import pyautogui", "bx, by, bw, bh = watch.state()['buttons'][0]",
               "btn = pyautogui.screenshot().crop((bx, by, bx + bw, by + bh))", "btn.save('exact.png'); btn.putpixel((5, 5), (0, 0, 0))", "btn.save('off.png')"],
              "Two picture files: the exact button, and one with a single pixel changed."),
             (["calls = [\"'exact.png'\", \"'off.png'\", \"'off.png', confidence=0.9\",", "         \"'off.png', grayscale=True\"]", "for name, py in ENVS:",
               "    r = [child(PROBE % c, py=py, env=d.env)[1][0] for c in calls]", "    print('%-17s' % name, [short(x) for x in r])"],
              "Three environments try the same four searches: exact, off by one pixel, with confidence, in gray."),
         ]),
    # ------------------------------------------------------------ part 4: the keyboard
    dict(id="type", layout="left", name="Typing into the right window", title="write(): typing into a window", part=5, visual="type",
         setup=_s(True, FAST, TEXT, *CLICKTEXT),
         concepts=["Controlling the Keyboard", "Sending Key Press Strings", "Pressing and Releasing the Keyboard", "pyautogui.write()", "pyautogui.keyDown()", "Figure 23-6: using PyAutoGUI to click the file editor window and enter Hello, world!"],
         groups=[
             (["import pyautogui", "pyautogui.write('Hello, world!'); print(repr(watch.text()))",
               "pyautogui.write(['a', 'b', 'left', 'left', 'X', 'Y'])", "print('write([a, b, left, left, X, Y]) ->', repr(watch.text()))"],
              "write() with a str types characters; with a list it also accepts key names such as 'left'."),
             (["pyautogui.keyDown('shift'); pyautogui.press('4')", "pyautogui.keyUp('shift')", "print('shift down, 4, shift up ->', repr(watch.text()[-3:]))",
               "pyautogui.hotkey('ctrl', 'a'); pyautogui.press('delete')", "print('hotkey(ctrl, a), delete ->', repr(watch.text()))",
               "pyautogui.write('Hello, world!')", "pyautogui.click(1000, 800); time.sleep(0.6)", "shotof(watch, 'typed.png', 120)"],
              "keyDown() and keyUp() hold a key; hotkey() presses a combination."),
         ]),
    dict(id="keys", name="Key names: mistakes are silent", title="What happens with a wrong key name?", part=5, visual="keys",
         setup=_s(True, FAST, TEXT, *CLICKTEXT),
         concepts=["Specifying Key Names", "Table 23-1: string values for keyboard keys", "pyautogui.KEYBOARD_KEYS", "pyautogui.press()", "pyautogui.keyDown()"],
         groups=[
             (["import pyautogui", "print('KEYBOARD_KEYS:', len(pyautogui.KEYBOARD_KEYS), 'names')",
               "for call in ('press', 'keyDown'):", "    try: getattr(pyautogui, call)('nokey'); r = 'raised nothing'",
               "    except Exception as e: r = type(e).__name__", "    print('%-8s nokey' % call, r, '| typed', repr(watch.text()))"],
              "A key name that does not exist raises nothing and types nothing."),
             (["pyautogui.write(['a', 'nokey', 'b']); pyautogui.write('café')", "print('a, nokey, b, then café typed', repr(watch.text()))",
               "print('A in the list:', 'A' in pyautogui.KEYBOARD_KEYS)"],
              "The wrong name is skipped without a word; check the text that arrived."),
         ]),
    dict(id="clip", name="Hotkeys and the clipboard", title="hotkey() and the clipboard", part=5, visual="clip",
         setup=_s(True, FAST, TEXT, *CLICKTEXT),
         concepts=["Running Hotkey Combinations", "Practice Program: Reading Text Fields with the Clipboard", "pyautogui.hotkey()", "pyperclip", "PyMsgBox"],
         groups=[
             (["import pyautogui, pyperclip", "pyautogui.write('Hello, world!\\nsecond line')", "watch.clear()",
               "pyautogui.hotkey('ctrl', 'alt', 'shift', 's')", "ks = [k.split('_')[0] for t, k, s in keys(watch)]", "print('down, then up:', *ks)"],
              "hotkey() presses the keys down in order and releases them in reverse order."),
             (["pyautogui.hotkey('ctrl', 'a'); pyautogui.hotkey('ctrl', 'c')", "time.sleep(1); text = pyperclip.paste()", "print('paste():', repr(text))",
               "pyautogui.press('end'); pyautogui.hotkey('ctrl', 'v')", "print('ctrl+v pasted it again:', watch.text() == text * 2)"],
              "Select all, copy, read the clipboard with pyperclip, paste it again."),
         ]),
]

BY_ID = {e["id"]: e for e in EXAMPLES}


def code_lines(ex):
    return [l for g, _ in ex["groups"] for l in g]


def run_text(ex):
    """the hidden setup lines first (they start the display and the watching window), then the shown code"""
    return "\n".join(ex.get("setup", []) + code_lines(ex)) + "\n"


def code_text(ex):
    return "\n".join(code_lines(ex)) + "\n"

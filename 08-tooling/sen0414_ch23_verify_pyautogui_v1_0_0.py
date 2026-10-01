"""Chapter 23 verification against the real PyAutoGUI (version 1.0.0 of this script).
Runs under a Python 3.14.4 virtual environment that has PyAutoGUI 0.9.54, PyScreeze 1.0.1, Pillow and Pyperclip installed
(python -m venv v; v/bin/pip install pyautogui) and a virtual X display:
    xvfb-run -a -s "-screen 0 1920x1080x24" v/bin/python 08-tooling/sen0414_ch23_verify_pyautogui_v1_0_0.py
Part 1 replaces the platform backend by a recorder and compares the events of 21 PyAutoGUI calls with those of the plain-Python model
DESK in the chapter's data module. Part 2 prints the other facts the chapter's document states about the library.
Exit code 1 if any comparison differs. Not a test the course page runs: it needs a display and a third-party package."""
__version__ = "1.0.0"
import os, sys, inspect
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_ch23_rdodi_data_v1_0_0 as D
ns = {}; exec(D.DESK, ns); Desk = ns["Desk"]
import pyautogui as p, pyscreeze
from PIL import Image
M = p.platformModule
raw = []; state = {"pos": (960, 540)}
clamp = lambda x, y: (max(0, min(1919, x)), max(0, min(1079, y)))
M._position = lambda: state["pos"]; M._size = lambda: (1920, 1080)
def mv(x, y): state["pos"] = clamp(x, y); raw.append(("move",) + state["pos"])
M._moveTo = mv
M._mouseDown = lambda x, y, b: (mv(x, y), raw.append(("down", b)))[0]
M._mouseUp = lambda x, y, b: (mv(x, y), raw.append(("up", b)))[0]
M._keyDown = lambda k: raw.append(("keydown", k)); M._keyUp = lambda k: raw.append(("keyup", k))
p.PAUSE = 0
BN = {1: "left", "left": "left", 2: "middle", "middle": "middle", 3: "right", "right": "right"}
def collapse(start):
    out = []; cur = tuple(start)
    for e in raw:
        if e[0] == "move":
            if (e[1], e[2]) != cur: out.append(e); cur = (e[1], e[2])
        elif e[0] in ("down", "up") and e[1] in (4, 5):
            if e[0] == "down": out.append(("wheel", 1 if e[1] == 4 else -1))
        elif e[0] in ("down", "up"): out.append((e[0], BN[e[1]]))
        else: out.append(e)
    return out
C = (960, 540)
S = {
 "click(10, 5)": (lambda d: d.click(10, 5), lambda: p.click(10, 5), C),
 "click(100, 150, button='right')": (lambda d: d.click(100, 150, button="right"), lambda: p.click(100, 150, button="right"), C),
 "click(box)": (lambda d: d.click((643, 745, 70, 29)), lambda: p.click((643, 745, 70, 29)), C),
 "doubleClick()": (lambda d: d.doubleClick(), lambda: p.doubleClick(), C),
 "moveTo, move, move": (lambda d: (d.moveTo(100, 100), d.move(100, 0), d.move(0, 100)), lambda: (p.moveTo(100, 100), p.move(100, 0), p.move(0, 100)), C),
 "move(-300, 0) from (200, 100)": (lambda d: d.move(-300, 0), lambda: p.move(-300, 0), (200, 100)),
 "moveTo(None, 500)": (lambda d: d.moveTo(None, 500), lambda: p.moveTo(None, 500), (100, 200)),
 "drag(30, 0)": (lambda d: d.drag(30, 0), lambda: p.drag(30, 0), (100, 100)),
 "dragTo(200, 150)": (lambda d: d.dragTo(200, 150), lambda: p.dragTo(200, 150), (100, 100)),
 "drag(0, 0)": (lambda d: d.drag(0, 0), lambda: p.drag(0, 0), (100, 100)),
 "scroll(3)": (lambda d: d.scroll(3), lambda: p.scroll(3), C),
 "scroll(-2)": (lambda d: d.scroll(-2), lambda: p.scroll(-2), C),
 "write('Hi!')": (lambda d: d.write("Hi!"), lambda: p.write("Hi!"), C),
 "write(key list)": (lambda d: d.write(["a", "b", "left", "left", "X", "Y"]), lambda: p.write(["a", "b", "left", "left", "X", "Y"]), C),
 "press('ENTER')": (lambda d: d.press("ENTER"), lambda: p.press("ENTER"), C),
 "press('left', presses=2)": (lambda d: d.press("left", presses=2), lambda: p.press("left", presses=2), C),
 "keyDown shift, press 4, keyUp shift": (lambda d: (d.keyDown("shift"), d.press("4"), d.keyUp("shift")), lambda: (p.keyDown("shift"), p.press("4"), p.keyUp("shift")), C),
 "hotkey('ctrl', 'c')": (lambda d: d.hotkey("ctrl", "c"), lambda: p.hotkey("ctrl", "c"), C),
 "hotkey('ctrl', 'alt', 'shift', 's')": (lambda d: d.hotkey("ctrl", "alt", "shift", "s"), lambda: p.hotkey("ctrl", "alt", "shift", "s"), C),
 "press('notakey')": (lambda d: d.press("notakey"), lambda: p.press("notakey"), C),
 "scroll(0) sends nothing": (lambda d: d.scroll(0), lambda: p.scroll(0), C),
}
bad = 0
for name, (model, real, start) in S.items():
    raw.clear(); state["pos"] = start; real(); got = collapse(start)
    d = Desk(pos=start); model(d)
    ok = got == d.log and tuple(d.pos) == state["pos"]; bad += not ok
    print("OK " if ok else "BAD", name, "" if ok else (got, d.log))
# the spiral of the chapter against the recorder
raw.clear(); state["pos"] = (500, 500); calls = []
distance = 300; change = 20
while distance > 0:
    for f in (lambda: (distance, 0), lambda: (0, distance - change), lambda: (-(distance - change), 0), lambda: (0, -(distance - 2 * change))):
        dx, dy = f(); calls.append((dx, dy)); p.drag(dx, dy)
    distance -= 2 * change
print("spiral: calls", len(calls), "zero drags", calls.count((0, 0)), "downs", sum(1 for e in raw if e[0] == "down"), "final", state["pos"], "expected 32 2 30 (660, 660)")
bad += (len(calls), calls.count((0, 0)), sum(1 for e in raw if e[0] == "down"), state["pos"]) != (32, 2, 30, (660, 660))
# fail-safe
for pt in [(0, 0), (1919, 0), (0, 1079), (1919, 1079), (1, 0), (960, 540)]:
    state["pos"] = pt
    try: p.press("a"); r = "ok"
    except p.FailSafeException: r = "raises"
    print("fail-safe at", pt, r)
print("FAILSAFE_POINTS", p.FAILSAFE_POINTS, "PAUSE default in module text: see source; MINIMUM_DURATION", p.MINIMUM_DURATION)
# keys
print("KEYBOARD_KEYS", len(p.KEYBOARD_KEYS), {k: p.isValidKey(k) for k in ("enter", "notakey", "command", "option", "volumemute", "shift")}, M.keyboardMapping["shift"], M.keyboardMapping["shiftleft"])
print("isShiftCharacter", [p.isShiftCharacter(c) for c in "aA!4~"])
# locate on two in-memory images, and pixel with the screen replaced by an image
hay = Image.new("RGB", (12, 6), (0, 0, 0)); nee = Image.new("RGB", (3, 2), (9, 9, 9)); hay.paste((9, 9, 9), (4, 2, 7, 4)); hay.paste((9, 9, 9), (8, 3, 11, 5))
print("locate", p.locate(nee, hay), list(p.locateAll(nee, hay)))
try: p.locate(Image.new("RGB", (3, 2), (1, 1, 1)), hay)
except p.ImageNotFoundException: print("not found raised pyautogui.ImageNotFoundException")
p.useImageNotFoundException(False); print("after useImageNotFoundException(False):", p.locate(Image.new("RGB", (3, 2), (1, 1, 1)), hay)); p.useImageNotFoundException(True)
img = Image.new("RGB", (300, 300), (255, 255, 254)); img.putpixel((50, 200), (130, 135, 144)); pyscreeze.pixel = lambda x, y: img.getpixel((x, y))
print("pixelMatchesColor", pyscreeze.pixelMatchesColor(50, 200, (130, 135, 144)), pyscreeze.pixelMatchesColor(50, 200, (255, 135, 144)), pyscreeze.pixelMatchesColor(1, 1, (255, 255, 255)), pyscreeze.pixelMatchesColor(1, 1, (255, 255, 255), tolerance=1), inspect.signature(pyscreeze.pixelMatchesColor))
try: p.pixel((50, 200))
except TypeError as e: print("pixel((50, 200)): TypeError", e)
# what is not available here
try: p.screenshot()
except Exception as e: print("screenshot():", type(e).__name__, str(e)[:90])
for n in ("getActiveWindow", "getAllTitles", "getWindowsWithTitle"):
    try: getattr(p, n)
    except AttributeError as e: print(n, "-> AttributeError", e)
try:
    import pyperclip; pyperclip.copy("x")
except Exception as e: print("pyperclip.copy:", type(e).__name__, str(e)[:70])
print("alert is", p.alert.__name__, "| has mouseInfo:", hasattr(p, "mouseInfo"), "| pyautogui", p.__version__, "| python", sys.version.split()[0])
print("MISMATCHES", bad); sys.exit(1 if bad else 0)

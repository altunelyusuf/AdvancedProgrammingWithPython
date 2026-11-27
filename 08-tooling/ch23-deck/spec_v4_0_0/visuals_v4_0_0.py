"""Chapter 23 deck visuals, version 4.0.0 (Lineage14): the executed result of every code example drawn as native tables and charts, and the pictures that the run itself made (the files an example saves are read from the folder it worked in).
Every number, string and picture shown is taken from the run of the example's own code (the namespace `ns` and the printed text `out` that the generic builder 08-tooling/chapter_deck_build_v2_10_0.py passes in);
nothing is typed in by hand except plain-language names of boxes and columns. Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants.
An example with layout="left" gets a narrow area (3.25 in wide, 3.9 in high); the others a wide, low one."""
__version__ = "4.0.0"
import ast
import os
import tempfile
from deck_kit_v2_2_0 import C, MONO, arrow, chart, label_shape as _label_shape, picture, rect, table as _table, tb


def table(s, x, y, w, rows, colw, fs=10.5, **kw):
    return _table(s, x, y, w, rows, colw, fs=fs, **kw)


def need(h):
    def deco(f):
        f.need = h
        return f
    return deco


FILL = {"plain": C["card"], "red": C["redLight"], "amber": C["amberLight"], "teal": C["tealLight"], "green": C["greenLight"], "grey": C["grey"]}


def box(s, x, y, w, h, text, kind="plain", fs=10, mono=False):
    return _label_shape(s, x, y, w, h, text, FILL[kind], C["ink"], size=fs, line=C["line"], radius=0.12, font="Consolas" if mono else None)


def note(s, x, y, w, text, h=0.24, fs=9.5):
    return tb(s, x, y, w, h, text, fs, C["muted"], italic=True, name="visual note")


def lines(out):
    return out.rstrip("\n").split("\n")


def lit(text):
    return ast.literal_eval(text)


_KEEP = []


def pic(s, im, x, y, w, h, descr, scale=1):
    """the picture the run made, drawn as it is (an alpha channel is shown over a white ground), inside the box x, y, w, h"""
    from PIL import Image
    im = im.convert("RGBA")
    if scale != 1:
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.NEAREST)
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    fd, path = tempfile.mkstemp(suffix=".png", prefix="ch23_result_")
    os.close(fd)
    bg.convert("RGB").save(path)
    _KEEP.append(path)
    rect(s, x - 0.03, y - 0.03, w + 0.06, h + 0.06, C["line"], name="frame")
    return picture(s, path, x, y, w, h, descr, "result picture")


def caption(s, x, y, w, text, fs=9.5):
    return tb(s, x, y, w, 0.24, text, fs, C["muted"], italic=True, name="caption")



def reading(s, x, y, w, rows, rowh=0.27, fs=10, fills=None):
    """what the run printed, as a native table of two columns"""
    return table(s, x, y, w, [["What the run printed", "Value"]] + rows, [w * 0.38, w * 0.62], rowh=rowh, mono_cols=(1,), cell_fill=fills, fs=fs)



G, A, R = C["greenLight"], C["amberLight"], C["redLight"]


def split2(out, sep):
    """lines of 'left<sep>right' as (left, right)"""
    return [tuple(p.strip() for p in ln.split(sep, 1)) for ln in lines(out) if sep in ln]


@need(1.6)
def v_pins(s, x, y, w, h, ns, out):
    L = lines(out)
    pk = lit(L[1])
    rows = [["Python", L[0]], ["pyautogui", pk[0]], ["its 3 helpers", ", ".join(pk[1:4])], ["size()", L[2].replace("Size", "")], ["position()", L[3].replace("Point", "")]]
    reading(s, x, y, w * 0.62, rows, rowh=0.27, fs=10, fills={(1, 1): G, (2, 1): G})
    note(s, x + w * 0.66, y + 0.1, w * 0.34, "pyautogui is below 1.0.0; the pointer starts in the middle of the display.", h=0.6)


@need(1.5)
def v_session(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["no DISPLAY", L[0]], ["Wayland, screenshot()", L[1]], ["X display, size()", L[2]]]
    reading(s, x, y, w, rows, rowh=0.36, fs=10.5, fills={(1, 1): R, (2, 1): R, (3, 1): G})


@need(1.6)
def v_xtest(s, x, y, w, h, ns, out):
    P = split2(out, ":")
    rows = [[a, b] for a, b in P]
    reading(s, x, y, w, rows, rowh=0.3, fs=10, fills={(1, 1): G, (2, 1): G, (3, 1): A, (4, 1): G})


@need(1.6)
def v_pause(s, x, y, w, h, ns, out):
    rows = [[ln.split(" ")[0], ln.split(": ")[1]] for ln in lines(out)[1:]]
    chart(s, "col", x, y, w * 0.4, 1.5, [r[0] for r in rows], [("waits", [1 if r[1] == "True" else 0 for r in rows])], fs=9, legend=False, gap=60, vmax=1, axis_title="1 = waits after the call")
    table(s, x + w * 0.45, y + 0.1, w * 0.55, [["Call", "Waits PAUSE seconds"]] + rows, [w * 0.25, w * 0.3], rowh=0.3, mono_cols=(0, 1), cell_fill={(i + 1, 1): (G if r[1] == "True" else A) for i, r in enumerate(rows)}, fs=10)


@need(1.7)
def v_corners(s, x, y, w, h, ns, out):
    L = lines(out)
    pts = [ln for ln in L if "raises" in ln]
    rows = [[ln.split(" raises:")[0], ln.split(": ")[1]] for ln in pts]
    table(s, x, y, w * 0.42, [["Pointer at", "FailSafeException"]] + rows, [w * 0.2, w * 0.22], rowh=0.32, mono_cols=(0, 1), cell_fill={(i + 1, 1): (G if r[1] == "True" else A) for i, r in enumerate(rows)}, fs=10.5)
    rows2 = [["FAILSAFE_POINTS", L[0].split(" ", 1)[1]], ["this process after the resize", L[-2].split(": ")[1]], ["a new process", L[-1].split(": ")[1]]]
    table(s, x + w * 0.46, y, w * 0.54, [["The corners", "Value"]] + rows2, [w * 0.2, w * 0.34], rowh=0.34, mono_cols=(1,), cell_fill={(2, 1): A, (3, 1): G}, fs=9.5)


@need(1.7)
def v_move(s, x, y, w, h, ns, out):
    P = [(m.group(1), int(m.group(2))) for m in __import__("re").finditer(r"duration=([0-9.]+\)?)\): +(\d+) motion", out)]
    chart(s, "col", x, y, w * 0.5, 1.6, ["%s s" % k for k, _ in P], [("motion events", [v for _, v in P])], fs=9, legend=False, gap=50, axis_title="motion events")
    rows = [[ln.split(" ->")[0], ln.split("-> ")[1]] for ln in lines(out) if "->" in ln]
    table(s, x + w * 0.54, y + 0.15, w * 0.46, [["Target", "Pointer ends at"]] + rows, [w * 0.24, w * 0.22], rowh=0.34, mono_cols=(0, 1), cell_fill={(1, 1): A, (2, 1): A}, fs=9.5)


@need(1.5)
def v_click(s, x, y, w, h, ns, out):
    rows = [[ln[:30].strip(), ln[30:].strip()] for ln in lines(out)]
    table(s, x, y, w, [["Call", "Button events received"]] + rows, [w * 0.42, w * 0.58], rowh=0.21, mono_cols=(0, 1), cell_fill={(6, 1): A}, fs=8.5)


@need(2.4)
def v_drag(s, x, y, w, h, ns, out):
    from PIL import Image
    im = Image.open("spiral.png").crop((150, 120, 560, 480))
    pic(s, im, x, y, 2.5, 2.2, "the spiral that the drag calls drew on the display", scale=1)
    L = lines(out)
    reading(s, x + 2.8, y + 0.2, w - 2.8, [["drag calls and ink box", L[0].replace("spiral: ", "")], ["button events", L[1]]], rowh=0.34, fs=10, fills={(2, 1): G})
    note(s, x, y + 2.25, 2.5, "The spiral, read from the display", h=0.24, fs=9)


@need(1.6)
def v_scroll(s, x, y, w, h, ns, out):
    rows = []
    for ln in lines(out):
        name, d = ln.split(":", 1)[0], __import__("ast").literal_eval(ln.split(":", 1)[1].strip())
        rows.append((name.replace("lines moved, ", ""), d))
    chart(s, "col", x, y, w * 0.5, 1.6, ["%d" % -k for k in rows[0][1]], [(n.split(" ")[0] + " " + n.split(" ")[1], [abs(v) for v in d.values()]) for n, d in rows], fs=9, legend=True, gap=40, axis_title="lines moved")
    table(s, x + w * 0.54, y + 0.15, w * 0.46, [["Clicks"] + ["%d" % -k for k in rows[0][1]]] + [[n.split(" ")[0] + " " + n.split(" ")[1]] + [str(v) for v in d.values()] for n, d in rows], [w * 0.14] + [w * 0.08] * 4, rowh=0.36, mono_cols=(), cell_fill={(2, i + 1): A for i in range(4)}, fs=9.5)


@need(2.4)
def v_shot(s, x, y, w, h, ns, out):
    from PIL import Image
    pic(s, Image.open("screen.png"), x, y, 2.9, 1.63, "the screenshot, reduced to 480 by 270")
    L = lines(out)
    reading(s, x + 3.2, y, w - 3.2, [["type, size, mode", L[0]], ["pixel(210, 160)", L[1].split("|")[0].split("->")[1].strip()], ["three tolerance tests", L[2]], ["pixel((210, 160))", "TypeError"]], rowh=0.3, fs=9.5, fills={(3, 1): A, (4, 1): R})
    note(s, x, y + 1.7, 2.9, "The display: grey background, one button", h=0.24, fs=9)


@need(2.4)
def v_locate(s, x, y, w, h, ns, out):
    from PIL import Image
    pic(s, Image.open("located.png"), x, y, 2.9, 2.1, "the search area with a red box around the first button")
    L = lines(out)
    reading(s, x + 3.2, y, w - 3.2, [["found (left, top, width, height)", L[0].replace("found ", "")], ["all matches", L[1].split(" | ")[0].replace("locateAll ", "")], ["center of the first", L[1].split("center ")[1]], ["click(boxes[1]) pressed", L[2].split("button ")[1]]], rowh=0.34, fs=9.5, fills={(3, 1): G})
    note(s, x, y + 2.15, 2.9, "Red box: the first match", h=0.24, fs=9)


@need(1.6)
def v_match(s, x, y, w, h, ns, out):
    rows = []
    for ln in lines(out):
        name, r = ln[:17].strip(), __import__("ast").literal_eval(ln[17:].strip())
        rows.append([name] + r)
    fills = {}
    for i, r in enumerate(rows):
        for j, v in enumerate(r[1:]):
            fills[(i + 1, j + 1)] = G if v == "Box" else (R if v in ("ImageNotFound", "NoneType") else A)
    table(s, x, y, w, [["Environment", "exact", "one pixel off", "confidence 0.9", "grayscale"]] + rows, [w * 0.24] + [w * 0.19] * 4, rowh=0.36, mono_cols=(1, 2, 3, 4), cell_fill=fills, fs=10)
    note(s, x, y + 1.6, w, "Green: found. Red: nothing found. Amber: the call is not implemented without OpenCV.", h=0.3, fs=9)


@need(2.2)
def v_type(s, x, y, w, h, ns, out):
    from PIL import Image
    pic(s, Image.open("typed.png"), x, y, 3.2, 0.9, "the window after the typing, as the display showed it")
    P = split2(out.replace(" ->", ":"), ":")
    reading(s, x, y + 1.05, w, [[a, b] for a, b in P[1:]] if P and P[0][0].startswith("'Hello") else [[a, b] for a, b in P], rowh=0.3, fs=9.5, fills={(2, 1): A})


@need(1.9)
def v_keys(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["names in KEYBOARD_KEYS", L[0].split(": ")[1]], ["press('nokey')", L[1].split("nokey")[1].strip()], ["keyDown('nokey')", L[2].split("nokey")[1].strip()],
            ["a, nokey, b, then café", L[3].split("typed ")[1]], ["'A' in the list", L[4].split(": ")[1]]]
    reading(s, x, y, w, rows, rowh=0.32, fs=10, fills={(2, 1): R, (3, 1): R, (4, 1): A, (5, 1): A})


@need(1.7)
def v_clip(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["keys received, in order", L[0].replace("down, then up: ", "")], ["paste() returned", L[1].split(": ", 1)[1]], ["ctrl+v pasted the same text", L[2].split(": ")[1]]]
    reading(s, x, y, w, rows, rowh=0.36, fs=10, fills={(3, 1): G})



# ---- narrow versions (layout="left": an area 3.25 in wide and 3.9 in high) -------------------------------------------------------
@need(3.0)
def v_pause(s, x, y, w, h, ns, out):
    rows = [[ln.split(" ")[0], ln.split(": ")[1]] for ln in lines(out)[1:]]
    chart(s, "col", x, y, w, 1.55, [r[0] for r in rows], [("waits", [1 if r[1] == "True" else 0 for r in rows])], fs=8, legend=False, gap=60, vmax=1, axis_title="1 = waits")
    table(s, x, y + 1.65, w, [["Call", "Waits PAUSE seconds"]] + rows, [w * 0.5, w * 0.5], rowh=0.3, mono_cols=(0, 1), cell_fill={(i + 1, 1): (G if r[1] == "True" else A) for i, r in enumerate(rows)}, fs=9.5)


@need(3.0)
def v_corners(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [[ln.split(" raises:")[0], ln.split(": ")[1]] for ln in L if "raises" in ln]
    table(s, x, y, w, [["Pointer at", "FailSafeException"]] + rows, [w * 0.5, w * 0.5], rowh=0.3, mono_cols=(0, 1), cell_fill={(i + 1, 1): (G if r[1] == "True" else A) for i, r in enumerate(rows)}, fs=9.5)
    table(s, x, y + 1.45, w, [["Screen size", "width, height"], ["before the resize", "(1920, 1080)"], ["this process", L[-2].split(": ")[1]], ["a new process", L[-1].split(": ")[1]]], [w * 0.55, w * 0.45], rowh=0.32, mono_cols=(1,), cell_fill={(2, 1): A, (3, 1): G}, fs=9.5)
    note(s, x, y + 2.85, w, "After the resize to 1280 by 720, only a new process sees the new corners.", h=0.4, fs=9)


@need(3.0)
def v_drag(s, x, y, w, h, ns, out):
    from PIL import Image
    im = Image.open("spiral.png").crop((150, 120, 560, 480))
    pic(s, im, x + 0.55, y, 2.1, 1.85, "the spiral that the drag calls drew on the display")
    L = lines(out)
    reading(s, x, y + 2.05, w, [["drag calls and ink box", L[0].replace("spiral: ", "")], ["presses and releases", L[1].replace("presses ", "") + " and " + L[2].replace("releases ", "")]], rowh=0.42, fs=9, fills={(2, 1): G})


@need(3.0)
def v_scroll(s, x, y, w, h, ns, out):
    rows = []
    for ln in lines(out):
        name, d = ln.split(":", 1)[0], __import__("ast").literal_eval(ln.split(":", 1)[1].strip())
        rows.append((name.replace("lines moved, ", "").split(" ")[0] + " " + name.replace("lines moved, ", "").split(" ")[1], d))
    chart(s, "col", x, y, w, 1.8, ["%d" % -k for k in rows[0][1]], [(n, [abs(v) for v in d.values()]) for n, d in rows], fs=8, legend=True, gap=40, axis_title="lines moved")
    table(s, x, y + 1.95, w, [["Clicks"] + ["%d" % -k for k in rows[0][1]]] + [[n] + [str(v) for v in d.values()] for n, d in rows], [w * 0.28] + [w * 0.18] * 4, rowh=0.34, mono_cols=(), cell_fill={(2, i + 1): A for i in range(4)}, fs=9)


@need(3.0)
def v_shot(s, x, y, w, h, ns, out):
    from PIL import Image
    pic(s, Image.open("screen.png"), x, y, 2.6, 1.46, "the screenshot, reduced to 480 by 270")
    L = lines(out)
    reading(s, x, y + 1.6, w, [["type, size, mode", L[0].replace("PngImageFile ", "")], ["pixel(210, 160)", L[1].split("-> ")[1]], ["tolerance tests", ", ".join(l.split(" ")[-1] for l in L[3:6])], ["pixel((210, 160))", "TypeError"]], rowh=0.36, fs=9, fills={(3, 1): A, (4, 1): R})


@need(3.0)
def v_locate(s, x, y, w, h, ns, out):
    from PIL import Image
    pic(s, Image.open("located.png"), x + 0.3, y, 2.6, 1.9, "the search area with a red box around the first button")
    L = lines(out)
    reading(s, x, y + 2.05, w, [["found (l, t, w, h)", L[0].replace("found ", "")], ["all matches", L[1].replace("locateAll ", "")], ["center of the first", L[2].replace("center ", "")], ["click(boxes[1])", "button " + L[3].split("button ")[1]]], rowh=0.4, fs=9, fills={(3, 1): G})


@need(3.0)
def v_match(s, x, y, w, h, ns, out):
    rows = []
    for ln in lines(out):
        rows.append(__import__("ast").literal_eval(ln[17:].strip()))
    names = ["OpenCV", "no OpenCV", "PyScreeze 0.1.28"]
    tests = ["exact", "one pixel off", "confidence 0.9", "grayscale"]
    body = [[tests[j]] + [rows[i][j] for i in range(3)] for j in range(4)]
    fills = {}
    for j in range(4):
        for i in range(3):
            v = rows[i][j]
            fills[(j + 1, i + 1)] = G if v == "Box" else (R if v in ("ImageNotFound", "NoneType") else A)
    table(s, x, y, w, [["Search"] + ["OpenCV", "no CV", "0.1.28"]] + body, [w * 0.31] + [w * 0.23] * 3, rowh=0.5, mono_cols=(1, 2, 3), cell_fill=fills, fs=8.5)
    note(s, x, y + 2.6, w, "Green: found. Red: nothing found. Amber: not implemented without OpenCV. Environments: " + ", ".join(names) + ".", h=0.7, fs=9)


@need(3.0)
def v_type(s, x, y, w, h, ns, out):
    from PIL import Image
    pic(s, Image.open("typed.png"), x, y, 3.2, 0.9, "the window after the typing, as the display showed it")
    L = lines(out)
    rows = [["write(str)", L[0]], ["write(list)", L[1].split("-> ")[1]], ["shift, 4", L[2].split("-> ")[1]], ["ctrl+a, delete", L[3].split("-> ")[1]]]
    reading(s, x, y + 1.1, w, rows, rowh=0.42, fs=9, fills={(2, 1): A})


VISUALS = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("v_") and callable(v)}

"""Chapter 21 deck visuals, version 4.0.0 (Lineage14): the executed result of every code example drawn as native tables and charts, drawn flows with arrows, and the pictures that the run itself made.
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
    fd, path = tempfile.mkstemp(suffix=".png", prefix="ch21_result_")
    os.close(fd)
    bg.convert("RGB").save(path)
    _KEEP.append(path)
    rect(s, x - 0.03, y - 0.03, w + 0.06, h + 0.06, C["line"], name="frame")
    return picture(s, path, x, y, w, h, descr, "result picture")


def caption(s, x, y, w, text, fs=9.5):
    return tb(s, x, y, w, 0.24, text, fs, C["muted"], italic=True, name="caption")


# ------------------------------------------------------------------ part 1: pixels, colours and boxes
def reading(s, x, y, w, rows, rowh=0.27, fs=10, fills=None):
    """what the run printed, as a native table of two columns"""
    return table(s, x, y, w, [["What the run printed", "Value"]] + rows, [w * 0.42, w * 0.58], rowh=rowh, mono_cols=(1,), cell_fill=fills, fs=fs)


@need(1.3)
def v_colours(s, x, y, w, h, ns, out):
    L = lines(out)
    names = ["red", "lime", "blue", "CornflowerBlue", "#CCDDEE"]
    nums = [lit(L[i].split(" ", 1)[1]) for i in range(len(names))]
    hexes = ["%02X%02X%02X" % tuple(n[:3]) for n in nums]
    rows = [names, ["%d, %d, %d, %d" % n for n in nums]]
    fills = {(0, i): hexes[i] for i in range(len(names))}
    colors = {(0, i): ("FFFFFF" if sum(n[:3]) < 400 else C["ink"]) for i, n in enumerate(nums)}
    table(s, x, y, w, rows, [w / len(names)] * len(names), header=False, rowh=0.4, mono_cols=(), cell_fill=fills, cell_color=colors, fs=10, bold_cols=())
    note(s, x, y + 0.9, w, "Colour, then red, green, blue, alpha. Last line printed: %s" % L[5], h=0.24, fs=9.5)


@need(1.25)
def v_boxtuple(s, x, y, w, h, ns, out):
    L = lines(out)
    im = ns["im"]
    gw, gh = im.size
    cell = min(0.1, (h - 0.2) / gh)
    gx, gy = x + 0.1, y + 0.05
    rect(s, gx, gy, gw * cell, gh * cell, "FFFFFF", line=C["muted"], name="grid")
    rect(s, gx + 3 * cell, gy + 1 * cell, 6 * cell, 5 * cell, C["tealLight"], line=C["teal"], name="box (3, 1, 9, 6)")
    sizes = L[2].replace(") (", ")|(").split("|")
    reading(s, x + gw * cell + 0.3, y, w - gw * cell - 0.4, [["picture size", L[0].split(") ")[0] + ")"],
                                                           ["the box (3, 1, 9, 6)", L[1]], ["crop of the box", sizes[0]], ["picture afterwards", sizes[1]]], rowh=0.27, fs=10)


@need(1.5)
def v_crop(s, x, y, w, h, ns, out):
    L = lines(out)
    cat, face = ns["cat"], ns["face"]
    sizes = L[0].replace(") (", ")|(").split("|")
    rows = [["original", sizes[0]], ["the crop", sizes[1]], ["middle pixels read", L[1]]]
    if w < 5:
        pic(s, cat, x, y + 0.05, 1.9, 1.33, "the picture the example drew: a dark face on a tan field")
        pic(s, face, x + 2.1, y + 0.05, 1.19, 1.19, "the cut-out face")
        reading(s, x, y + 1.7, w, rows, rowh=0.3, fs=9.5)
    else:
        pic(s, cat, x, y + 0.05, 1.7, 1.19, "the picture the example drew: a dark face on a tan field")
        pic(s, face, x + 1.95, y + 0.05, 1.19, 1.19, "the cut-out face")
        reading(s, x + 3.4, y, w - 3.4, rows, rowh=0.27, fs=10)


@need(1.5)
def v_paste(s, x, y, w, h, ns, out):
    L = lines(out)
    sheet = ns["sheet"]
    rows = [["pastes made", L[0].split(" ")[0]], ["last pixel of the sheet", L[1].split(" None")[0]], ["value paste() returned", "None"]]
    if w < 5:
        pic(s, sheet, x, y + 0.05, 3.1, 1.86, "the sheet of 15 orange faces")
        reading(s, x, y + 2.1, w, rows, rowh=0.3, fs=9.5)
    else:
        pic(s, sheet, x, y + 0.05, 1.9, 1.14, "the sheet of 15 orange faces")
        reading(s, x + 2.2, y, w - 2.2, rows, rowh=0.27, fs=10)


# ------------------------------------------------------------------ part 2: changing pictures
@need(1.5)
def v_mask(s, x, y, w, h, ns, out):
    L = lines(out)
    plain, masked = ns["plain"], ns["masked"]
    rows = [["pasted without a mask", L[0]], ["pasted with the square as mask", L[1]]]
    cw = 1.25
    pic(s, plain, x, y + 0.05, cw, cw, "red base with a blue square pasted without a mask")
    pic(s, masked, x + cw + 0.25, y + 0.05, cw, cw, "red base with the blue square pasted with a mask")
    if w >= 5:
        reading(s, x + 2.9, y, w - 2.9, rows, rowh=0.3, fs=10)
    else:
        reading(s, x, y + 1.6, w, rows, rowh=0.36, fs=9)


@need(1.3)
def v_transform(s, x, y, w, h, ns, out):
    L = lines(out)
    a = lit(L[0].replace(") (", "),("))
    sizes = [("resize((60, 40))", a[0]), ("rotate(90)", a[1]), ("rotate(90, expand=True)", a[2])]
    t, e = lit(L[1].replace(") (", "),("))
    sizes += [("rotate(6)", t), ("rotate(6, expand=True)", e)]
    rows = [["Call", "Size (width by height)"]] + [[k, "%d by %d" % v] for k, v in sizes]
    cf = {(3, 1): C["greenLight"], (5, 1): C["greenLight"]}
    if w >= 5:
        chart(s, "col", x, y, w * 0.5, max(h, 1.3), [k for k, _ in sizes], [("width", [v[0] for _, v in sizes]), ("height", [v[1] for _, v in sizes])], fs=8, legend=True, gap=50)
        table(s, x + w * 0.55, y + 0.02, w * 0.45, rows, [2.5, 1.6], rowh=0.2, mono_cols=(0,), cell_fill=cf, fs=9)
    else:
        table(s, x, y + 0.05, w, rows, [1.9, 1.35], rowh=0.34, mono_cols=(0,), cell_fill=cf, fs=9)
        tb(s, x, y + 2.3, w, 0.9, "Green: the canvas grew. The flip kept 120 by 80, and the corner of a turned picture is black.", 10, C["muted"], italic=True, name="visual note")


@need(1.3)
def v_save(s, x, y, w, h, ns, out):
    L = lines(out)
    sizes = {ln.split(" ")[0]: int(ln.split(" ")[1]) for ln in L[:2]}
    rows = [["Format", "Bytes", "Alpha channel"], ["PNG", str(sizes["PNG"]), "kept"], ["JPEG", str(sizes["JPEG"]), "none"], ["RGBA as JPEG", "refused", "OSError"]]
    cf = {(2, 2): C["redLight"], (1, 2): C["greenLight"], (3, 1): C["redLight"]}
    if w >= 5:
        chart(s, "col", x, y, w * 0.4, max(h, 1.3), list(sizes), [("bytes", list(sizes.values()))], fs=10, legend=False, gap=80)
        table(s, x + w * 0.45, y + 0.05, w * 0.55, rows, [1.4, 1.2, 1.5], rowh=0.28, mono_cols=(1,), cell_fill=cf, fs=10)
    else:
        chart(s, "col", x, y, w, 2.1, list(sizes), [("bytes", list(sizes.values()))], fs=10, legend=False, gap=80)
        table(s, x, y + 2.3, w, rows, [1.2, 0.8, 1.25], rowh=0.3, mono_cols=(1,), cell_fill=cf, fs=9)


# ------------------------------------------------------------------ part 3: Project 16 and drawing
@need(1.5)
def v_logo(s, x, y, w, h, ns, out):
    L = lines(out)
    from PIL import Image
    names = [ln.split(" ")[0] for ln in L if not ln.endswith("None")]
    sizes = [lit(ln.split(" ", 1)[1]) for ln in L if not ln.endswith("None")]
    rows = [["File", "Size before", "Result"]]
    before = {f: Image.open(f).size for f in sorted(os.listdir(".")) if f.endswith(".png")}
    for f in sorted(before):
        rows.append([f, "%d by %d" % before[f], ("stamped, %d by %d" % sizes[names.index(f)]) if f in names else "skipped: too small"])
    cf = {(i, 2): (C["greenLight"] if r[2].startswith("stamped") else C["amberLight"]) for i, r in enumerate(rows) if i}
    if w >= 5:
        pic(s, ns["logo"], x, y + 0.05, 0.8, 0.6, "the logo: a red rectangle with some alpha")
        table(s, x + 1.1, y + 0.02, w - 1.1, rows, [1.2, 1.8, 3.8], rowh=0.28, mono_cols=(0,), cell_fill=cf, fs=10)
    else:
        pic(s, ns["logo"], x, y + 0.05, 0.8, 0.6, "the logo: a red rectangle with some alpha")
        table(s, x, y + 0.9, w, rows, [0.8, 1.0, 1.45], rowh=0.42, mono_cols=(0,), cell_fill=cf, fs=8.5)


@need(1.5)
def v_draw(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["blue pixels counted", L[0].split(" ")[0]], ["41 by 31", "1271"], ["40 by 30 would be", "1200"]]
    if w >= 5:
        pic(s, ns["im"], x, y + 0.03, 1.25, 1.25, "the drawing: a point, a line, a rectangle, an ellipse and a polygon")
        reading(s, x + 1.6, y, w - 1.6, rows, rowh=0.3, fs=10)
    else:
        pic(s, ns["im"], x + 0.1, y + 0.05, 2.6, 2.6, "the drawing: a point, a line, a rectangle, an ellipse and a polygon")
        reading(s, x, y + 2.8, w, rows, rowh=0.3, fs=9.5)


@need(1.4)
def v_text(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["box of the text", L[0]], ["width and height", L[1]], ["ink was drawn", L[2]]]
    if w >= 5:
        pic(s, ns["im"], x, y + 0.05, 2.0, 0.6, "the picture with the text Howdy!")
        reading(s, x + 2.4, y, w - 2.4, rows, rowh=0.3, fs=10)
    else:
        pic(s, ns["im"], x, y + 0.05, 3.1, 0.93, "the picture with the text Howdy!")
        reading(s, x, y + 1.2, w, rows, rowh=0.3, fs=9.5)


# ------------------------------------------------------------------ part 4: the clipboard and graphs
@need(1.2)
def v_clipboard(s, x, y, w, h, ns, out):
    L = lines(out)
    got = ns["got"]
    box(s, x, y + 0.2, 2.0, 0.5, "copy(picture)", "teal", 10, True)
    arrow(s, x + 2.05, y + 0.45, x + 2.6, y + 0.45, C["muted"], 1.5)
    box(s, x + 2.65, y + 0.2, 1.8, 0.5, "clipboard holds one", "amber", 10)
    arrow(s, x + 4.5, y + 0.45, x + 5.05, y + 0.45, C["muted"], 1.5)
    box(s, x + 5.1, y + 0.2, 2.0, 0.5, "paste() gives it back", "teal", 10, True)
    pic(s, got, x + 7.4, y + 0.1, 0.9, 0.6, "the picture that paste() returned")
    note(s, x, y + 0.85, w, "The run printed %s: the size and the first pixel of the returned picture." % L[0], h=0.24)


@need(1.3)
def v_line(s, x, y, w, h, ns, out):
    L = lines(out).copy()
    n_lines, kind, title, saved = L[0].split(" ")
    xs = [str(int(v)) for v in ns["lines"][0].get_xdata()]
    ys = [float(v) for v in ns["lines"][0].get_ydata()]
    dots = [float(v) for v in ns["dots"].get_offsets()[:, 1]]
    rows = [["lines returned by plot()", n_lines], ["what scatter() returned", kind], ["title set", title], ["savefig() wrote data", saved]]
    if w >= 5:
        chart(s, "col", x, y, w * 0.5, max(h, 1.3), xs, [("plot(): squares", ys), ("scatter(): dots", dots)], fs=9, legend=True, gap=50)
        reading(s, x + w * 0.55, y, w * 0.45, rows, rowh=0.26, fs=9.5)
    else:
        chart(s, "col", x, y, w, 2.0, xs, [("plot(): squares", ys), ("scatter(): dots", dots)], fs=9, legend=True, gap=50)
        reading(s, x, y + 2.15, w, rows, rowh=0.3, fs=9)


@need(1.3)
def v_barpie(s, x, y, w, h, ns, out):
    L = lines(out)
    heights = lit(L[0])
    names = ns["names"]
    votes = ns["votes"]
    if w >= 5:
        chart(s, "col", x, y, w * 0.45, max(h, 1.3), names, [("votes", heights)], fs=10, legend=False, gap=60)
        rows = [["Wedge", "Share", "Angle (degrees)"]] + [[n_, "%d of %d" % (v, sum(votes)), "%d" % round(360 * v / sum(votes))] for n_, v in zip(names, votes)]
        table(s, x + w * 0.5, y + 0.02, w * 0.5, rows, [1.2, 1.5, 1.9], rowh=0.26, cell_fill={(1, 2): C["greenLight"]}, fs=10)
    else:
        chart(s, "col", x, y, w, 1.8, names, [("votes", heights)], fs=10, legend=False, gap=60)
        rows = [["Wedge", "Share", "Angle"]] + [[n_, "%d of %d" % (v, sum(votes)), "%d" % round(360 * v / sum(votes))] for n_, v in zip(names, votes)]
        table(s, x, y + 1.95, w, rows, [0.8, 1.2, 1.25], rowh=0.28, cell_fill={(1, 2): C["greenLight"]}, fs=10)
        tb(s, x, y + 3.2, w, 0.5, "pie() returned " + L[1].split(" ")[0] + " wedges; the first spans " + L[1].split(" ")[-1] + " degrees", 10, C["ink"], name="reading")


# ------------------------------------------------------------------ part 5: practice programs
@need(1.5)
def v_tile(s, x, y, w, h, ns, out):
    L = lines(out)
    size, p1, p2 = L[0].split(" (", 1)[0], None, None
    parts = L[0].replace(") (", ")|(").split("|")
    rows = [["sheet size", parts[0]], ["pixel at the middle of tile 1", parts[1]], ["pixel at the middle of tile 8", parts[2]]]
    if w >= 5:
        pic(s, ns["sheet"], x, y + 0.05, 1.9, 1.14, "the tile sheet: 4 faces across and 3 down")
        reading(s, x + 2.2, y, w - 2.2, rows, rowh=0.28, fs=10)
    else:
        pic(s, ns["sheet"], x, y + 0.05, 3.1, 1.86, "the tile sheet: 4 faces across and 3 down")
        reading(s, x, y + 2.1, w, rows, rowh=0.3, fs=9)


@need(1.5)
def v_seating(s, x, y, w, h, ns, out):
    L = lines(out)
    cards = ns["cards"]
    n_cards, size = L[0].split(" ", 1)
    rows = [["cards made", n_cards], ["size of a card", size], ["corner pixel, then ink in the middle", L[1]]]
    for i, c_ in enumerate(cards):
        pic(s, c_, x + i * 1.08, y + 0.05, 1.0, 1.25, "seating card for " + ns["guests"][i])
    if w >= 5:
        reading(s, x + 3.4, y, w - 3.4, rows, rowh=0.3, fs=10)
    else:
        reading(s, x, y + 1.5, w, rows, rowh=0.4, fs=9)


VISUALS = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("v_") and callable(v)}

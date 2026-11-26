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
@need(1.3)
def v_colours(s, x, y, w, h, ns, out):
    L = lines(out)
    names = ["red", "lime", "blue", "CornflowerBlue", "#CCDDEE"]
    n = len(names)
    cw = (w - 0.1 * (n - 1)) / n
    for i, nm in enumerate(names):
        r, g, b, a = lit(L[i].split(" ", 1)[1])
        xx = x + i * (cw + 0.1)
        rect(s, xx, y, cw, 0.5, "%02X%02X%02X" % (r, g, b), line=C["line"], name="swatch")
        tb(s, xx, y + 0.52, cw, 0.5, [nm, "%d, %d, %d, %d" % (r, g, b, a)], 9.5, C["ink"], align=None, name="swatch label")
    note(s, x, y + 1.03, w, "Last line printed: %s" % L[5], h=0.24, fs=9.5)


@need(1.25)
def v_boxtuple(s, x, y, w, h, ns, out):
    L = lines(out)
    im = ns["im"]
    gw, gh = im.size
    cell = min(0.1, (h - 0.2) / gh)
    gx, gy = x + 0.1, y + 0.05
    rect(s, gx, gy, gw * cell, gh * cell, "FFFFFF", line=C["muted"], name="grid")
    rect(s, gx + 3 * cell, gy + 1 * cell, 6 * cell, 5 * cell, C["tealLight"], line=C["teal"], name="box (3, 1, 9, 6)")
    tb(s, gx + gw * cell + 0.2, y, w - gw * cell - 0.4, 1.2, ["The picture is %s pixels." % L[0].split(" ", 1)[0].replace("(", "").replace(",", " by").replace(")", ""),
                                                           "The box (3, 1, 9, 6) is %s." % L[1], "crop((3, 1, 9, 6)) gave %s; the picture stays %s." % tuple(L[2].replace(") (", ")|(").split("|"))],
       10.5, C["ink"], name="reading")


@need(1.5)
def v_crop(s, x, y, w, h, ns, out):
    L = lines(out)
    cat, face = ns["cat"], ns["face"]
    narrow = w < 5
    if narrow:
        pic(s, cat, x, y + 0.05, 2.0, 1.4, "the picture the example drew: a dark face on a tan field")
        pic(s, face, x + 0.4, y + 1.7, 1.3, 1.3, "the cut-out face")
        caption(s, x, y + 1.5, w, "the original: %s" % L[0].split(") (")[0] + ")")
        caption(s, x, y + 3.05, w, "the crop: (%s" % L[0].split(") (")[1])
    else:
        pic(s, cat, x, y + 0.05, 1.7, 1.19, "the picture the example drew: a dark face on a tan field")
        pic(s, face, x + 2.6, y + 0.05, 1.19, 1.19, "the cut-out face")
        tb(s, x + 4.2, y, w - 4.2, 1.3, ["original %s" % L[0].split(") (")[0] + ")", "crop %s" % ("(" + L[0].split(") (")[1]), "pixels read: " + L[1]], 10.5, C["ink"], name="reading")


@need(1.5)
def v_paste(s, x, y, w, h, ns, out):
    L = lines(out)
    sheet = ns["sheet"]
    narrow = w < 5
    if narrow:
        pic(s, sheet, x, y + 0.05, 3.1, 1.86, "the sheet of 15 orange faces")
        tb(s, x, y + 2.0, w, 1.2, [L[0], "last pixel %s" % L[1].split(" None")[0], "paste() returned None"], 10.5, C["ink"], name="reading")
    else:
        pic(s, sheet, x, y + 0.05, 1.9, 1.14, "the sheet of 15 orange faces")
        tb(s, x + 2.2, y, w - 2.2, 1.3, ["the run printed: %s" % L[0], "last pixel %s; paste() returned None" % L[1].split(" None")[0]], 10.5, C["ink"], name="reading")


# ------------------------------------------------------------------ part 2: changing pictures
@need(1.5)
def v_mask(s, x, y, w, h, ns, out):
    L = lines(out)
    plain, masked = ns["plain"], ns["masked"]
    cw = 1.25 if w >= 5 else 1.4
    if w >= 5:
        pic(s, plain, x, y + 0.05, cw, cw, "red base with a blue square pasted without a mask")
        pic(s, masked, x + 3.3, y + 0.05, cw, cw, "red base with the blue square pasted with a mask")
        tb(s, x + cw + 0.15, y + 0.1, 1.8, 1.0, ["no mask", L[0]], 10.5, C["ink"], name="reading")
        tb(s, x + 3.3 + cw + 0.15, y + 0.1, 3.6, 1.0, ["the square as the mask", L[1]], 10.5, C["ink"], name="reading")
    else:
        pic(s, plain, x, y + 0.05, cw, cw, "red base with a blue square pasted without a mask")
        pic(s, masked, x + 1.7, y + 0.05, cw, cw, "red base with the blue square pasted with a mask")
        tb(s, x, y + 1.55, w, 1.4, ["no mask (left): " + L[0], "with the mask (right): " + L[1], "The mask blends; no mask replaces."], 10.5, C["ink"], name="reading")


@need(1.3)
def v_transform(s, x, y, w, h, ns, out):
    L = lines(out)
    a, b, c_ = lit(L[0].replace(") (", "),(")), None, None
    sizes = [("resize((60, 40))", a[0]), ("rotate(90)", a[1]), ("rotate(90, expand=True)", a[2])]
    t, e = lit(L[1].replace(") (", "),("))
    sizes += [("rotate(6)", t), ("rotate(6, expand=True)", e)]
    chart(s, "col", x, y, w * 0.5, max(h, 1.3), [k for k, _ in sizes], [("width", [v[0] for _, v in sizes]), ("height", [v[1] for _, v in sizes])], fs=8, legend=True, gap=50)
    rows = [["Call", "Size"]] + [[k, "%d by %d" % v] for k, v in sizes]
    table(s, x + w * 0.55, y + 0.02, w * 0.45, rows, [2.5, 1.6], rowh=0.2, mono_cols=(0,), cell_fill={(3, 1): C["greenLight"], (5, 1): C["greenLight"]}, fs=9)


@need(1.3)
def v_save(s, x, y, w, h, ns, out):
    L = lines(out)
    sizes = {ln.split(" ")[0]: int(ln.split(" ")[1]) for ln in L[:2]}
    chart(s, "col", x, y, w * 0.4, max(h, 1.3), list(sizes), [("bytes", list(sizes.values()))], fs=10, legend=False, gap=80)
    rows = [["Format", "Bytes", "Alpha channel"], ["PNG", str(sizes["PNG"]), "kept"], ["JPEG", str(sizes["JPEG"]), "none"]]
    table(s, x + w * 0.45, y + 0.05, w * 0.55, rows, [1.2, 1.2, 1.7], rowh=0.28, mono_cols=(1,), cell_fill={(2, 2): C["redLight"], (1, 2): C["greenLight"]}, fs=10)
    box(s, x + w * 0.45, y + 1.0, w * 0.55, 0.3, "saving RGBA as JPEG: " + L[2], "red", 9.5, True)


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
    if w >= 5:
        pic(s, ns["im"], x, y + 0.03, 1.25, 1.25, "the drawing: a point, a line, a rectangle, an ellipse and a polygon")
        tb(s, x + 1.5, y, w - 1.5, 1.3, [L[0] + " (the rectangle from (20, 30) to (60, 60))", "41 times 31 is 1271; 40 times 30 would be 1200"], 10.5, C["ink"], name="reading")
    else:
        pic(s, ns["im"], x + 0.1, y + 0.05, 2.6, 2.6, "the drawing: a point, a line, a rectangle, an ellipse and a polygon")
        tb(s, x, y + 2.75, w, 1.0, [L[0], "41 times 31 is 1271; 40 times 30 would be 1200"], 10.5, C["ink"], name="reading")


@need(1.4)
def v_text(s, x, y, w, h, ns, out):
    L = lines(out)
    if w >= 5:
        pic(s, ns["im"], x, y + 0.05, 2.0, 0.6, "the picture with the text Howdy!")
        tb(s, x + 2.3, y, w - 2.3, 1.3, ["box (left, top, right, bottom): " + L[0], L[1], "ink drawn: " + L[2]], 10.5, C["ink"], name="reading")
    else:
        pic(s, ns["im"], x, y + 0.05, 3.1, 0.93, "the picture with the text Howdy!")
        tb(s, x, y + 1.15, w, 1.4, ["box: " + L[0], L[1], "ink drawn: " + L[2]], 10.5, C["ink"], name="reading")


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
    L = lines(out)
    plt = ns["plt"]
    fd, path = tempfile.mkstemp(suffix=".png", prefix="ch21_fig_")
    os.close(fd)
    plt.gcf().savefig(path, dpi=100)
    _KEEP.append(path)
    from PIL import Image
    im = Image.open(path)
    if w >= 5:
        picture(s, path, x, y, 1.7, 1.3, "the graph the example drew: a line, dots, a title, labels and a legend", "result picture")
        xs = [1, 2, 3, 4]
        chart(s, "col", x + 2.0, y, 3.0, max(h, 1.3), [str(v) for v in xs], [("squares", [1, 4, 9, 16]), ("scatter", [2, 3, 5, 8])], fs=9, legend=True, gap=50)
        tb(s, x + 5.2, y, w - 5.2, 1.3, ["lines returned: " + L[0].split(" ")[0], "scatter returned: " + L[0].split(" ")[1], "title: " + L[0].split(" ")[2], "saved: " + L[0].split(" ")[3]], 10, C["ink"], name="reading")
    else:
        picture(s, path, x, y + 0.05, 3.15, 2.36, "the graph the example drew: a line, dots, a title, labels and a legend", "result picture")
        tb(s, x, y + 2.55, w, 1.3, ["lines returned: " + L[0].split(" ")[0], "scatter returned: " + L[0].split(" ")[1], "title: " + L[0].split(" ")[2], "figure saved: " + L[0].split(" ")[3]], 10, C["ink"], name="reading")


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
    if w >= 5:
        pic(s, ns["sheet"], x, y + 0.05, 1.9, 1.14, "the tile sheet: 4 faces across and 3 down")
        tb(s, x + 2.2, y, w - 2.2, 1.3, ["sheet size and two pixels read: " + L[0]], 10.5, C["ink"], name="reading")
    else:
        pic(s, ns["sheet"], x, y + 0.05, 3.1, 1.86, "the tile sheet: 4 faces across and 3 down")
        tb(s, x, y + 2.05, w, 1.4, ["printed: " + L[0], "4 across and 3 down of 50 by 40"], 10.5, C["ink"], name="reading")


@need(1.5)
def v_seating(s, x, y, w, h, ns, out):
    L = lines(out)
    cards = ns["cards"]
    if w >= 5:
        for i, c_ in enumerate(cards):
            pic(s, c_, x + i * 1.15, y + 0.05, 1.0, 1.25, "seating card for " + ns["guests"][i])
        tb(s, x + 3.6, y, w - 3.6, 1.3, ["printed: " + L[0], L[1]], 10.5, C["ink"], name="reading")
    else:
        for i, c_ in enumerate(cards):
            pic(s, c_, x + i * 1.08, y + 0.05, 1.0, 1.25, "seating card for " + ns["guests"][i])
        tb(s, x, y + 1.5, w, 1.4, ["printed: " + L[0], L[1]], 10.5, C["ink"], name="reading")


VISUALS = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("v_") and callable(v)}

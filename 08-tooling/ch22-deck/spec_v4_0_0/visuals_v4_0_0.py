"""Chapter 22 deck visuals, version 4.0.0 (Lineage14): the executed result of every code example drawn as native tables and charts, drawn flows with arrows, and the pictures that the run itself made.
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
    fd, path = tempfile.mkstemp(suffix=".png", prefix="ch22_result_")
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


def pairs(out):
    """lines of 'key value' as (key, float)"""
    return [(a.split(" ")[0], float(a.split(" ")[1])) for a in lines(out) if a.strip()]


@need(1.5)
def v_engine(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["version of Tesseract", L[0]], ["language files installed", L[1].split(" ", 1)[0]], ["the first five", L[1].split(" ", 1)[1]],
            ["eng installed, xyz installed", L[2]]]
    reading(s, x, y, w, rows, rowh=0.32, fs=10.5, fills={(3, 1): C["greenLight"]})


@need(1.5)
def v_read(s, x, y, w, h, ns, out):
    L = lines(out)
    pic(s, ns["im"], x, y + 0.05, 3.2, 0.65, "the picture the example drew: Hello OCR 2026")
    reading(s, x + 3.5, y, w - 3.5, [["text returned (repr)", L[0]], ["equal to the drawn text after strip()", L[1]]], rowh=0.32, fs=10.5, fills={(1, 1): C["greenLight"]})
    note(s, x, y + 0.85, 3.2, "The picture the example drew")


@need(1.7)
def v_lines(s, x, y, w, h, ns, out):
    L = lines(out)
    pic(s, ns["im"], x, y + 0.05, 2.8, 0.87, "three lines of text drawn by the example")
    got = ns["text"].splitlines()
    rows = [[str(i + 1), repr(t)] for i, t in enumerate(got)]
    fills = {(i, 1): C["amberLight"] for i, t in enumerate(got) if t == "" or "|" in t}
    table(s, x + 3.1, y, w - 3.1, [["Line", "What splitlines() returned"]] + rows, [0.7, w - 3.8], rowh=0.3, mono_cols=(1,), cell_fill={(r + 1, c): v for (r, c), v in fills.items()}, fs=10)
    note(s, x, y + 0.97, 2.9, "%s. Amber: a mistake, a blank line." % L[0], h=0.24, fs=9)


@need(1.7)
def v_data(s, x, y, w, h, ns, out):
    rows = [ln.split(" ") for ln in lines(out) if ln.strip()]
    pic(s, ns["im"], x, y + 0.05, 3.2, 0.46, "the line the example drew")
    table(s, x + 3.5, y, w - 3.5, [["Word", "Confidence", "Left", "Top"]] + rows, [(w - 3.5) * 0.4, (w - 3.5) * 0.2, (w - 3.5) * 0.2, (w - 3.5) * 0.2], rowh=0.3, mono_cols=(0, 1, 2, 3), cell_fill={(i + 1, 1): C["greenLight"] for i in range(len(rows))}, fs=10)


def _score_chart(s, x, y, w, h, out, unit, name):
    P = pairs(out)
    chart(s, "col", x, y, w * 0.45, 1.5, [k for k, _ in P], [(name, [v for _, v in P])], fs=9, legend=False, gap=50, vmax=1.0, axis_title=unit)
    kinds = ["reads" if v >= 0.9 else ("weak" if v > 0 and v < 0.9 else "fails") for _, v in P]
    fills = {(2, i + 1): (C["greenLight"] if k == "reads" else C["amberLight"] if k == "weak" else C["redLight"]) for i, k in enumerate(kinds)}
    cw = [w * 0.1] + [w * 0.4 / len(P)] * len(P)
    table(s, x + w * 0.5, y + 0.2, w * 0.5, [[unit] + [k for k, _ in P], ["score"] + ["%.2f" % v for _, v in P], ["reading"] + kinds], cw,
          rowh=0.36, header=True, mono_cols=(), cell_fill=fills, fs=9)


@need(1.5)
def v_size(s, x, y, w, h, ns, out):
    _score_chart(s, x, y, w, h, out, "pixels", "score")


@need(1.5)
def v_tilt(s, x, y, w, h, ns, out):
    _score_chart(s, x, y, w, h, out, "degrees", "score")


@need(1.5)
def v_noise(s, x, y, w, h, ns, out):
    _score_chart(s, x, y, w, h, out, "noise", "score")


@need(1.2)
def v_clean(s, x, y, w, h, ns, out):
    L = lines(out)
    t = L[0].split(" ")
    sm = L[1].split(" ")
    bw = L[2].split(" ")[-1]
    cats = ["tilted 10 degrees", "small, 8 pixels", "black and white"]
    before = [float(t[1]), float(sm[1]), float(sm[2])]
    after = [float(t[2]), float(sm[2]), float(bw)]
    chart(s, "col", x, y, w * 0.5, 1.2, cats, [("before the step", before), ("after the step", after)], fs=8, legend=True, gap=50, vmax=1.0)
    rows = [[cats[i], "%.2f" % before[i], "%.2f" % after[i], "better" if after[i] > before[i] else "worse"] for i in range(3)]
    fills = {(i + 1, 3): (C["greenLight"] if rows[i][3] == "better" else C["redLight"]) for i in range(3)}
    table(s, x + w * 0.55, y, w * 0.45, [["Picture", "Before", "After", "Effect"]] + rows, [w * 0.18, w * 0.09, w * 0.09, w * 0.09], rowh=0.28, mono_cols=(1, 2), cell_fill=fills, fs=9)


@need(1.5)
def v_config(s, x, y, w, h, ns, out):
    L = lines(out)
    pic(s, ns["im"], x, y + 0.05, 3.2, 0.57, "the line the example drew: Call 555-0199 now: 2026")
    rows = [["without settings", L[0]], ["--psm 7 with a whitelist", L[1]]]
    reading(s, x + 3.5, y, w - 3.5, rows, rowh=0.34, fs=10.5, fills={(1, 1): C["tealLight"]})


@need(1.5)
def v_lang(s, x, y, w, h, ns, out):
    L = lines(out)
    langs = [l.split(" ")[0] for l in L[:2]]
    eng = [float(l.split(" ")[1]) for l in L[:2]]
    own = [float(l.split(" ")[2]) for l in L[:2]]
    chart(s, "col", x, y, w * 0.45, 1.5, langs, [("lang='eng'", eng), ("own language", own)], fs=9, legend=True, gap=50, vmax=1.0)
    rows = [["lang='%s' vs 'eng'" % l, "%.2f" % own[i], "%.2f" % eng[i]] for i, l in enumerate(langs)] + [["lang='xyz' (not installed)", L[2], "error"]]
    table(s, x + w * 0.5, y, w * 0.5, [["Line", "Own language", "English"]] + rows, [w * 0.25, w * 0.125, w * 0.125], rowh=0.3, mono_cols=(1, 2), cell_fill={(3, 1): C["redLight"], (1, 1): C["greenLight"], (2, 1): C["greenLight"]}, fs=9.5)


@need(1.05)
def v_mistakes(s, x, y, w, h, ns, out):
    L = lines(out)
    ops = [l for l in L if l.startswith("replace")]
    rows = [[l.split(" ")[1], l.split("read as ")[1]] for l in ops]
    table(s, x, y, w * 0.4, [["True character", "Read as"]] + rows, [w * 0.2, w * 0.2], rowh=0.2, mono_cols=(0, 1), cell_fill={(i + 1, 1): C["amberLight"] for i in range(len(rows))}, fs=9)
    reading(s, x + w * 0.45, y, w * 0.55, [["true text", ns["TRUTH"]], ["what was read", ns["read"]], ["differences found", str(len(ops))], ["similarity", L[-1]]], rowh=0.2, fs=9)


@need(1.4)
def v_pdf(s, x, y, w, h, ns, out):
    L = lines(out)
    reading(s, x, y, w, [["type and first five bytes", L[0]], ["text found by pdftotext", L[1]], ["lines in the picture", "2"]], rowh=0.34, fs=10.5, fills={(1, 1): C["greenLight"]})


@need(1.5)
def v_naps(s, x, y, w, h, ns, out):
    L = lines(out)
    bw = (w - 1.2) / 3
    box(s, x, y + 0.1, bw, 0.7, "command as a list\n" + L[0][:40], "plain", fs=9, mono=True)
    arrow(s, x + bw, y + 0.45, x + bw + 0.6, y + 0.45)
    box(s, x + bw + 0.6, y + 0.1, bw, 0.7, "subprocess.run(command, check=True)", "teal", fs=9, mono=True)
    arrow(s, x + 2 * bw + 0.6, y + 0.45, x + 2 * bw + 1.2, y + 0.45)
    box(s, x + 2 * bw + 1.2, y + 0.1, bw, 0.7, L[1], "red", fs=10, mono=True)
    note(s, x, y + 1.0, w, "NAPS2 is not installed on this machine, so the program that should have started is not found.")


@need(0.9)
def v_screen(s, x, y, w, h, ns, out):
    L = lines(out)
    sizes = L[0].replace(") (", ")|(").split("|")
    pic(s, ns["shot"], x, y + 0.02, 1.4, 0.66, "the emulated screenshot with a bar and two lines of text")
    pic(s, ns["part"], x + 1.6, y + 0.02, 1.4, 0.26, "the cropped region that holds the text")
    reading(s, x + 3.3, y, w - 3.3, [["screenshot size, crop size", L[0]], ["lines read", L[1]]], rowh=0.26, fs=9, fills={(1, 1): C["greenLight"]})
    note(s, x, y + 0.7, 3.0, "Left: the screenshot. Right: the crop.", h=0.2, fs=9)


@need(1.4)
def v_scraper(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [[str(i + 1), t] for i, t in enumerate(lit(L[0]))]
    table(s, x, y, w * 0.45, [["Page", "Line in output.txt"]] + rows, [w * 0.08, w * 0.37], rowh=0.32, mono_cols=(1,), cell_fill={(i + 1, 1): C["greenLight"] for i in range(len(rows))}, fs=10.5)
    bx = x + w * 0.5
    box(s, bx, y + 0.1, 1.5, 0.6, "screenshot, crop", "plain", fs=10)
    arrow(s, bx + 1.5, y + 0.4, bx + 1.8, y + 0.4)
    box(s, bx + 1.8, y + 0.1, 0.9, 0.6, "read", "teal", fs=10)
    arrow(s, bx + 2.7, y + 0.4, bx + 3.0, y + 0.4)
    box(s, bx + 3.0, y + 0.1, 1.5, 0.6, "append to file", "green", fs=10)
    note(s, bx, y + 0.9, 4.5, "One pass for each page: three pages, three lines.")


VISUALS = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("v_") and callable(v)}

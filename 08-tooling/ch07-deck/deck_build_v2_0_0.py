#!/usr/bin/env python3
"""Chapter 7 deck v2.0.0 generator (a NEW tool file; the v1.0.0 builders and the v1.0.0 deck are untouched).

Builds 03-materials/ch07/SEN0414_Ch07_Dictionaries_3e_v2_0_0.pptx with python-pptx 1.0.2, from the chapter research
(03-materials/ch07/rdodi, the newest: sen0414_ch07_research_v1_3_0.ttl) and the assets of the earlier deck, and writes
03-materials/ch07/page/chapter_code_ch07_v1_0_0.json, the ordered chapter-code manifest the page's chapter-code tab lists.

Every result on a code slide is what examples_v2_0_0.py printed when it ran the code under python3.14.

Usage: python3 deck_build_v2_0_0.py"""
__version__ = "2.0.0"
import ast, hashlib, json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck_kit_v2_0_0 import *                      # noqa: F401,F403
from deck_kit_v2_0_0 import _text
import examples_v2_0_0 as X

OUT_DECK = os.path.join(ROOT, "03-materials", "ch07", "SEN0414_Ch07_Dictionaries_3e_v2_0_0.pptx")
OUT_MANIFEST = os.path.join(ROOT, "03-materials", "ch07", "page", "chapter_code_ch07_v1_0_0.json")

bad = X.lint()
if bad:
    raise SystemExit("REFUSED: the examples break their own rules:\n" + "\n".join(bad))
RUNS = X.run_all()
PYV = subprocess.run([X.PY, "-c", "import platform;print(platform.python_version())"], capture_output=True, text=True).stdout.strip()

SLIDE_OF = {}          # example id -> slide number (filled while building)
PART_FIRST = []        # (part title, slide number of its divider)


def lines(ex_id):
    return RUNS[ex_id]["out"].splitlines()


# ---------------------------------------------------------------- code slides
CODEW = 5.25


def code_slide(ex, vis, need=1.25):
    s = new_slide("Code %d: %s" % (len(SLIDE_OF) + 1, ex["name"]), ex["sub"], ex["src"], ex["notes"])
    SLIDE_OF[ex["id"]] = len(SLIDES)
    top, bottom, gap = 1.2, 4.84, 0.06
    chosen = None
    maxlen = max(len(l) for g, _ in ex["groups"] for l in g) + 4
    for cfs, nfs in [(12, 12.5), (11.5, 12), (11, 12), (10.5, 11.5), (10, 11.5), (10, 11), (10, 10.5)]:
        if maxlen * 0.6 * cfs + 14.4 > CODEW * 72 - 2:
            continue
        lh = cfs * 1.22 / 72
        per = 0.9 * (3.92 * 72 - 11.5) / (0.5 * nfs)
        rows = []
        for g, note in ex["groups"]:
            rows.append(max(len(g) * lh + 0.12, math.ceil(len(note) / per) * nfs * 1.22 / 72 + 0.12))
        total = sum(rows) + gap * (len(rows) - 1)
        chosen = (cfs, nfs, rows, total)
        if total + 0.3 + need <= bottom - top:
            break
    cfs, nfs, rows, total = chosen
    if total + 0.3 + need > bottom - top + 0.001:
        print("WARN: %s leaves %.2f in for its result (wanted %.2f)" % (ex["id"], bottom - top - total - 0.3, need))
    y = top
    for (g, note), rh in zip(ex["groups"], rows):
        code_box(s, 0.4, y, CODEW, rh, g, cfs)
        box_text(s, 5.63, y, 3.92, rh, note, nfs, C["ink"], C["card"], name="explanation")
        y += rh + gap
    ry = y + 0.03
    tb(s, 0.4, ry, 5.5, 0.24, "What the run printed (Python %s)" % PYV, 11, C["slate"], bold=True, name="result label")
    h = bottom - (ry + 0.27)
    vis(s, RUNS[ex["id"]], 0.4, ry + 0.27, 9.2, h)
    takeaway(s, ex["take"], 4.92)
    return s


def tbl(s, x, y, w, h, rows, colw, fs=None, mono=(), bold_first=False):
    rowh = min(0.34, h / len(rows))
    fs = 12 if rowh >= 0.3 else (11 if rowh >= 0.25 else 10)
    return table(s, x, y, w, rows, colw, fs, rowh, mono_cols=mono, bold_first=bold_first)


# ---- the visual of each example (all values read from what the example printed)
def v_dict_basics(s, res, x, y, w, h):
    L = res["out"].splitlines()
    d = ast.literal_eval(res["vars"]["my_cat"])
    pairs(s, x, y, 4.5, h, list(d.items()), size=11)
    tbl(s, x + 4.8, y, 4.4, h, [["Expression", "Printed"], ["my_cat['size']", L[0]], ["'My cat has ' + color", L[1]], ["len(my_cat)", L[2]]], [2.2, 2.2], mono=(0,))


def v_dict_vs_list(s, res, x, y, w, h):
    L = res["out"].splitlines()
    tbl(s, x, y, w, h, [["Expression", "Printed", "Why"], ["spam == bacon", L[0], "the same items in a different order"], ["eggs == ham", L[1], "the same pairs, in any order"],
                        ["list(ham)", L[2], "the order of adding is still kept"]], [2, 3, 4], mono=(0, 1))


def v_insertion(s, res, x, y, w, h):
    L = res["out"].splitlines()
    a, b = ast.literal_eval(L[0]), ast.literal_eval(L[2])
    rh = (h - 0.12) / 2
    tb(s, x, y, 2.4, rh, "after the three assignments", 11, C["mute"], italic=True, anchor=MSO_ANCHOR.MIDDLE, name="row label")
    flow(s, x + 2.5, y, 6.4, rh, a, name="visual: order before", size=12, mono=True)
    tb(s, x, y + rh + 0.12, 2.4, rh, "after del and adding again", 11, C["mute"], italic=True, anchor=MSO_ANCHOR.MIDDLE, name="row label")
    flow(s, x + 2.5, y + rh + 0.12, 6.4, rh, b, name="visual: order after", hot=(2,), size=12, mono=True)


def v_hashable(s, res, x, y, w, h):
    L = res["out"].splitlines()
    tbl(s, x, y, w, h, [["Key tried", "Allowed?", "Printed"], ["(1, 2)  a tuple", "yes", L[0]], ["[1, 2]  a list", "no, unhashable", L[1]], ["1, 1.0 and True", "yes, but one key", L[2]]],
        [3, 3, 4.5], mono=(2,))


def v_kvi(s, res, x, y, w, h):
    L = res["out"].splitlines()
    tbl(s, x, y, w, h, [["Method", "Gives", "Printed"], ["spam.keys()", "the labels", L[0]], ["spam.values()", "the contents", L[1]], ["spam.items()", "both, as pairs", L[4]]],
        [2, 2, 5], mono=(0, 2))


def v_exists(s, res, x, y, w, h):
    L = res["out"].splitlines()
    tbl(s, x, y, w, h, [["Question", "Printed"], ["'cups' in picnic", L[0]], ["'eggs' not in picnic", L[1]], ["picnic.get('eggs', 0)", L[2]],
                        ["picnic.get('cups', 0)", L[3]], ["picnic['eggs']", L[4]]], [4, 3], mono=(0,))


def v_setdefault(s, res, x, y, w, h):
    L = res["out"].splitlines()
    d = ast.literal_eval(res["vars"]["picnic"])
    chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, list(d), [("picnic", list(d.values()))], x, y, 4.3, h, name="result", fs=10)
    tbl(s, x + 4.6, y, 4.6, h, [["Call", "Printed", "What happened"], ["first", L[0], "key missing: 12 stored"], ["second", L[1], "key found: 99 unused"]], [1.2, 1.2, 3])


def v_change(s, res, x, y, w, h):
    L = res["out"].splitlines()
    tbl(s, x, y, w, h, [["Line", "Printed"], ["spam.pop('color')", L[0]], ["print(spam)", L[1]], ["spam | {'name': 'Rex', 'legs': 4}", L[2]], ["print(spam) again", L[3]]], [4, 5], mono=(0, 1))


def v_views(s, res, x, y, w, h):
    L = res["out"].splitlines()
    tbl(s, x, y, w, h, [["Name", "What it is", "Shows"], ["ks = stock.keys()", "a live view", L[0]], ["frozen = list(stock)", "a photograph", L[1]],
                        ["sorted(stock)", "a new sorted list", L[2]], ["reversed(stock)", "newest first", L[3]]], [3, 2.4, 4], mono=(0, 2))


def v_birthdays(s, res, x, y, w, h):
    L = res["out"].splitlines()
    d = ast.literal_eval(res["vars"]["birthdays"])
    tbl(s, x, y, w, h, [["Typed", "The program did", "Printed"], ["Alice", "found the key", L[0]], ["Eve, then Dec 5", "stored a new pair", L[1]], ["Eve", "found the new key", L[2]],
                        ["dictionary now", "%d pairs" % len(d), ", ".join(d)]], [2, 2.4, 4.6])


def v_charcount(s, res, x, y, w, h):
    L = res["out"].splitlines()
    top = ast.literal_eval(L[0])
    tot, kinds = [int(t) for t in L[1].split()]
    chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, ["space" if k == " " else k for k, _ in top], [("count", [v for _, v in top])], x, y, 6.0, h, name="result", fs=10)
    tbl(s, x + 6.3, y, 2.9, min(h, 0.9), [["Measure", "Value"], ["characters", tot], ["different ones", kinds]], [2, 1])


def v_counter(s, res, x, y, w, h):
    L = res["out"].splitlines()
    d = ast.literal_eval(L[3])
    chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, list(d), [("count", list(d.values()))], x, y, 4.6, h, name="result", fs=10)
    tbl(s, x + 4.9, y, 4.3, h, [["Expression", "Printed"], ["c.most_common(2)", L[0]], ["c['a'], c['z']", L[1]], ["sum(c.values())", L[2]]], [2.2, 2.4], mono=(0, 1))


def v_grouping(s, res, x, y, w, h):
    L = res["out"].splitlines()
    d = ast.literal_eval(L[0])
    pairs(s, x, y, 5.2, h, [(k, v) for k, v in d.items()], size=11)
    tbl(s, x + 5.5, y, 3.7, min(h, 0.7), [["Is g2 == groups?", "Printed"], ["defaultdict result", L[1]]], [2.2, 1.2])


def v_board_model(s, res, x, y, w, h):
    L = res["out"].splitlines()
    d = ast.literal_eval(res["vars"]["board"])
    pairs(s, x, y, 3.0, h, list(d.items()), size=10)
    tbl(s, x + 3.3, y, 4.4, min(h, 0.9), [["Printed", "Meaning"], [L[0], "c6 occupied, a1 empty"], [L[1], "five keys, sorted"]], [2.6, 1.8], fs=10, mono=(0,))
    picture(s, "book_fig_000103.jpg", x + 7.85, y - 0.05, 1.35, h + 0.02, None, name="Figure 7-2, the chessboard of the model")


def v_board_print(s, res, x, y, w, h):
    L = res["out"].splitlines()
    rows = [["", "a", "b", "c", "d", "e", "f", "g", "h"]]
    for ln in L:
        t = ln.split()
        rows.append([t[0]] + ["" if c == ".." else c for c in t[1:]])
    gf = table(s, x, y, 4.6, rows, [0.6] + [1] * 8, 9.5, h / 9, name="result table", bold_first=True)
    t = gf.table
    for i in range(1, 9):
        for j in range(1, 9):
            c = t.cell(i, j)
            c.fill.solid(); c.fill.fore_color.rgb = rgb("B7A98F" if (j - 1 + (9 - i)) % 2 == 1 else "F0E6D2")
            for p in c.text_frame.paragraphs:
                for r in p.runs:
                    r.font.bold = True; r.font.color.rgb = rgb(C["dark"])
    pcs = sum(1 for r in rows[1:] for c in r[1:] if c)
    tbl(s, x + 4.9, y, 4.3, min(h, 1.2), [["Measure", "Value"], ["keys in the dictionary", pcs], ["squares drawn", 64], ["squares without a key", 64 - pcs]], [3, 1.2])


def v_moves(s, res, x, y, w, h):
    L = res["out"].splitlines()
    b, st = ast.literal_eval(L[1]), ast.literal_eval(L[2])
    flow(s, x, y, w, h * 0.62, ["START\n" + "  ".join(st), "board = copy.copy(START)\n" + "  ".join(st), "e2 moves to e4\nboard: " + "  ".join(b)], hot=(2,), size=12, mono=False)
    tb(s, x, y + h * 0.66, w, h * 0.3, "Printed report: " + L[0] + ".   START still holds " + " ".join(st) + ".", 11, C["slate"], bold=True, name="result note")


def v_validator(s, res, x, y, w, h):
    L = res["out"].splitlines()
    m = re.match(r"(\[.*?\]) (\[.*?\]) (\w+)", L[0])
    bad, kings, ok = ast.literal_eval(m.group(1)), ast.literal_eval(m.group(2)), m.group(3) == "True"
    tbl(s, x, y, w, h, [["Rule of the game", "Looks at", "Found", "Verdict"], ["every key is a real square", "the keys", "bad squares: %s" % bad, "PASS" if not bad else "FAIL"],
                        ["one king of each colour", "the values", "kings: %s" % kings, "PASS" if ok else "FAIL"]], [3.2, 1.4, 3.2, 1.2])


def v_picnic(s, res, x, y, w, h):
    L = res["out"].splitlines()
    g = ast.literal_eval(res["vars"]["guests"])
    items = []
    for d in g.values():
        for k in d:
            if k not in items:
                items.append(k)
    chart(s, XL_CHART_TYPE.COLUMN_STACKED, items, [(n, [d.get(k) for k in items]) for n, d in g.items()], x, y, 5.6, h, name="result", fs=10, legend=True)
    tbl(s, x + 5.9, y, 3.3, h, [["Expression", "Printed"], ["total('apples'), total('cups')", L[0]], ["Alice's pretzels", L[1]]], [2.4, 1], mono=(0,), fs=9.5)


def v_inventory(s, res, x, y, w, h):
    L = res["out"].splitlines()
    d = ast.literal_eval(res["vars"]["stuff"])
    chart(s, XL_CHART_TYPE.BAR_CLUSTERED, list(d), [("how many", list(d.values()))], x, y, 5.2, h, name="result", fs=10)
    tbl(s, x + 5.5, y, 3.7, min(h, 0.8), [["Last line printed"], [L[-1]]], [1])


def v_loot(s, res, x, y, w, h):
    L = res["out"].splitlines()
    after = ast.literal_eval(L[0])
    line = [l for g, _ in X.BY_ID["loot"]["groups"] for l in g if l.startswith("inv = ")][0]
    before = ast.literal_eval(line.split("=", 1)[1].strip())
    cats = list(after)
    chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, cats, [("before", [before.get(k) for k in cats]), ("after", [after[k] for k in cats])], x, y, 6.0, h, name="result", fs=10, legend=True)
    tbl(s, x + 6.3, y, 2.9, min(h, 0.9), [["Measure", "Value"], ["items before", sum(before.values())], ["items after", L[1]]], [2, 1])


def v_copies(s, res, x, y, w, h):
    L = res["out"].splitlines()
    a, sh, dp = L[0].split()
    is_alias, is_shallow = L[1].split()
    inner = L[2] == "True"
    tbl(s, x, y, w, h, [["Name", "New outer dictionary?", "Shares the inner one?", "Apples after the change"],
                        ["alias", "no, same object" if is_alias == "True" else "yes", "yes", a],
                        ["shallow copy", "yes" if is_shallow == "False" else "no", "yes" if inner else "no", sh],
                        ["deep copy", "yes", "no", dp]], [2, 3, 3, 3])


def v_json(s, res, x, y, w, h):
    L = res["out"].splitlines()
    flow(s, x, y, w, h * 0.7, ["dictionary\ncat", "text (JSON)\n" + L[0], "equal again?\njson.loads(text) == cat: " + L[1]], hot=(1,), size=11)
    tb(s, x, y + h * 0.74, w, h * 0.26, "pprint printed: " + L[2].strip() + " " + L[3].strip(), 11, C["slate"], bold=True, name="result note", font=MONO)


def v_typed(s, res, x, y, w, h):
    L = res["out"].splitlines()
    tp, age = L[0].split()
    tbl(s, x, y, w, h, [["Tool", "At run time", "Who enforces it"], ["TypedDict Cat", "type(c).__name__ is '%s', age %s" % (tp, age), "a type checker, not Python"],
                        ["MappingProxyType", "age %s, length %s: read-only" % tuple(L[1].split()), "Python itself: item assignment fails"]], [2.4, 4.2, 3.6])


def v_match(s, res, x, y, w, h):
    L = res["out"].splitlines()
    flow(s, x, y, w, h * 0.75, ["cat\n{'name': 'Zophie', 'age': 8}", "case 1 fits\nname, age and a > 5", L[0]], hot=(2,), size=11)
    tb(s, x, y + h * 0.8, w, h * 0.2, "case 2 is never tried: the first fitting case wins.", 11, C["slate"], bold=True, name="result note")


VIS = {"dict_basics": (v_dict_basics, 1.1), "dict_vs_list": (v_dict_vs_list, 1.0), "insertion_order": (v_insertion, 1.1), "hashable_keys": (v_hashable, 1.0),
       "keys_values_items": (v_kvi, 1.0), "key_exists": (v_exists, 1.2), "setdefault": (v_setdefault, 1.2), "change_pairs": (v_change, 1.2), "views_follow": (v_views, 1.2),
       "birthdays": (v_birthdays, 1.3), "char_count": (v_charcount, 1.1), "counter": (v_counter, 1.2), "grouping": (v_grouping, 0.95), "board_model": (v_board_model, 1.4),
       "board_print": (v_board_print, 1.9), "chess_moves": (v_moves, 1.0), "validator": (v_validator, 0.9), "picnic_nested": (v_picnic, 1.3), "inventory": (v_inventory, 1.1),
       "loot": (v_loot, 1.3), "copies": (v_copies, 0.9), "json_pprint": (v_json, 0.9), "typed_records": (v_typed, 0.9), "match_dict": (v_match, 0.9)}


def code(ex_id):
    fn, need = VIS[ex_id]
    return code_slide(X.BY_ID[ex_id], fn, need)


# ---------------------------------------------------------------- other slide types
def divider(title, sub, items, flow_labels, notes):
    """one divider (no brand chip): each concept as a short name plus one line of meaning, and one native table as the visual"""
    s = new_slide(title, sub, None, notes, chip=False)
    t = s.shapes.title
    t.left, t.width = Inches(0.5), Inches(9.0)
    for sh in s.shapes:
        if sh.name == "subtitle":
            sh.left, sh.width = Inches(0.5), Inches(9.0)
    n = len(items)
    h = min(0.74, 3.5 / n - 0.05)
    y0 = 1.4
    for i, (name, meaning) in enumerate(items):
        assert len(name.split()) <= 4 and len(meaning.split()) >= 5, (name, meaning)
        y = y0 + i * (h + 0.08)
        card(s, 0.5, y, 5.95, h, C["card"], "concept row")
        card(s, 0.5, y, 0.07, h, C["orange"], "concept accent")
        tb(s, 0.65, y, 1.85, h, name, 13.5, C["dark"], bold=True, anchor=MSO_ANCHOR.MIDDLE, name="concept")
        tb(s, 2.5, y, 3.9, h, meaning, 13, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="concept meaning")
    rows = [["How they fit together"]] + [["%d.  %s" % (k + 1, lab)] for k, lab in enumerate(flow_labels)]
    table(s, 6.75, y0, 2.75, rows, [1], 13, min(0.7, 3.5 / len(rows)), name="visual: how the concepts fit")
    return s


def everyday(title, sub, cards_, notes, cols=2, src=None):
    """cards_: (concept label exactly as in the research, the everyday picture). One text box per card: EVERYDAY, the concept, the picture."""
    s = new_slide(title, sub, src, notes)
    n = len(cards_)
    rows = math.ceil(n / cols)
    gapx, gapy = 0.2, 0.12
    x0, y0, W, H = 0.5, 1.28, 9.0, 3.5
    bw = (W - (cols - 1) * gapx) / cols
    bh = min(1.15, (H - (rows - 1) * gapy) / rows)
    for i, (label, pic) in enumerate(cards_):
        assert len(("EVERYDAY " + label + " " + pic).split()) <= 30, label
        r, c = divmod(i, cols)
        cx, cy = x0 + c * (bw + gapx), y0 + r * (bh + gapy)
        sh = card(s, cx, cy, bw, bh, C["card"], "everyday card")
        card_accent = card(s, cx, cy, 0.07, bh, C["orange"], "card accent")
        big = rows <= 3
        _text(sh, [[("EVERYDAY  ", {"size": 10 if big else 9.5, "bold": True, "color": C["orange"]}), (label, {"size": 14 if big else 13, "bold": True, "color": C["dark"], "font": HF})],
                   [(pic, {"size": 13 if big else 12})]], 12, C["ink"], anchor=MSO_ANCHOR.MIDDLE, margin=0.16)
    return s


STORIES = {
    "guido": dict(title="Five words that gave dictionaries an order", photo="photo_guido_van_rossum_2014.jpg", credit="Guido van Rossum - photo: Daniel Stroud, CC BY-SA 4.0",
                  link="https://mail.python.org/pipermail/python-dev/2017-December/151283.html", linkLabel="Guido's ruling on python-dev, 15 December 2017",
                  rows=["Guido van Rossum, Python's creator, answering core developer INADA Naoki.",
                        "He ruled that a dict keeps insertion order: 'Make it so.'",
                        "Friday 15 December 2017, at 10:53 Eastern time.",
                        "The python-dev mailing list, in the thread 'Guarantee ordered dict literals in v3.7?'",
                        "Python 3.6's dict kept order only as an implementation detail; users wanted a promise.",
                        "Python 3.7 made insertion order 'an official part of the Python language spec'."],
                  lesson="One short message turned an implementation detail into a promise.",
                  notes="On 15 December 2017 Guido van Rossum answered a question about ordered dictionaries with the words 'Make it so'. From Python 3.7 the order of adding is part of the language, and the book's 'no first item' is out of date."),
    "orwell": dict(title="The sentence the character counter counts", photo="photo_george_orwell.jpg", credit="George Orwell, press card photo, 1943 - National Union of Journalists, public domain",
                   link="https://en.wikipedia.org/wiki/Nineteen_Eighty-Four", linkLabel="Nineteen Eighty-Four, on Wikipedia",
                   rows=["George Orwell, the pen name of the writer Eric Blair.",
                         "His novel Nineteen Eighty-Four opens with the sentence our program counts.",
                         "8 June 1949.",
                         "London: Secker & Warburg published the novel in the United Kingdom.",
                         "A famous, real sentence is honest test data for counting characters.",
                         "Our loop counts 73 characters, 23 of them different, using setdefault()."],
                   lesson="The lines that count one sentence count a whole novel.",
                   notes="The text in the character counter is the first sentence of Nineteen Eighty-Four, published on 8 June 1949. A real sentence makes the counts meaningful: thirteen spaces, and the same table would count the whole book."),
    "chess": dict(title="The squares a1 to h8 are almost three centuries old", photo="photo_chess_staunton.jpg", credit="A Staunton chess set - photo: Wilfredor, CC0",
                  link="https://en.wikipedia.org/wiki/Algebraic_notation_(chess)", linkLabel="Algebraic notation (chess), on Wikipedia",
                  rows=["Philipp Stamma, Howard Staunton and the chess federation FIDE.",
                        "They named every square a1 to h8 and made that notation the standard.",
                        "1730s: Stamma. 1847: Staunton's handbook. 1981: FIDE.",
                        "In chess books such as Staunton's Chess-Player's Handbook, then in FIDE rules.",
                        "Players needed one short name for each of the 64 squares to write moves down.",
                        "Our keys 'a1' to 'h8' reuse those names, so a position reads like a score sheet."],
                  lesson="The best keys are often a notation people already use.",
                  notes="Philipp Stamma used the modern square names in the 1730s, Howard Staunton described the system in 1847, and FIDE stopped recognising descriptive notation in 1981. The chessboard dictionary borrows those names as its keys."),
    "json": dict(title="The notation that carries dictionaries", photo="photo_douglas_crockford.jpg", credit="Douglas Crockford, 2013 - photo: Robert Claypool, CC0",
                 link="https://www.json.org/json-en.html", linkLabel="Introducing JSON, on json.org",
                 rows=["Douglas Crockford and Chip Morningstar; the standards body IETF later.",
                       "A small text format of name-value pairs and lists, shaped like a Python dict.",
                       "April 2001: first message. December 2005: Yahoo! December 2017: RFC 8259.",
                       "State Software, the company Crockford co-founded, and the website json.org.",
                       "Web pages needed a light way to receive data without plug-ins such as Flash.",
                       "Python's json module writes a dictionary as that text with dumps() and reads it back with loads()."],
                 lesson="JSON is how a dictionary leaves a program and comes back.",
                 notes="Douglas Crockford and Chip Morningstar sent the first JSON message in April 2001. Yahoo began offering web services in JSON in December 2005, and the IETF published it as RFC 8259 in December 2017. Python's json module converts between it and dictionaries."),
}


def story(key):
    st = STORIES[key]
    s = new_slide(st["title"], "A true story, told as who, what, when, where, why and how", None, st["notes"])
    picture(s, st["photo"], 0.5, 1.28, 3.3, 3.2, st["credit"])
    y, rh = 1.22, 0.52
    for lab, txt in zip(["WHO", "WHAT", "WHEN", "WHERE", "WHY", "HOW"], st["rows"]):
        assert len(txt.split()) <= 22, txt
        card(s, 3.95, y, 5.55, rh, C["card"], "5N1K row")
        tb(s, 4.02, y, 0.8, rh, lab, 12, C["orange"], bold=True, anchor=MSO_ANCHOR.MIDDLE, name="5N1K label")
        tb(s, 4.8, y, 4.65, rh, txt, 10.5, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="5N1K text")
        y += rh + 0.035
    host = st["link"].split("//")[1].split("/")[0].replace("www.", "")
    tb(s, 3.95, y + 0.0, 5.55, 0.34, [[("READ  ", {"bold": True, "color": C["orange"]}), (st["linkLabel"], {"link": st["link"], "color": C["slate"], "bold": True}),
                                         ("   " + host, {"color": C["mute"], "size": 10})]], 11, name="live link")
    takeaway(s, st["lesson"], 4.93)
    return s


# ---------------------------------------------------------------- the deck
COURSE = "SEN0414 Advanced Programming · Fall 2026 · Yusuf Altunel, PhD · İstanbul Kültür University"

# 1 title
s = new_slide("Chapter 7: Dictionaries and Structuring Data", None, None,
              "This chapter is about the dictionary: pairs of a key and a value, found by key. We count with it, model a chessboard with it, copy it and write it down as text. Every result you see was run under Python %s." % PYV, chip=False)
t = s.shapes.title
t.left, t.top, t.width, t.height = Inches(0.6), Inches(0.9), Inches(5.2), Inches(1.7)
t.text_frame.paragraphs[0].runs[0].font.size = Pt(30)
card(s, 0.6, 0.55, 0.9, 0.12, C["orange"], "accent")
tb(s, 0.6, 2.75, 5.2, 0.8, "Pairs, counts, models and the text that carries them", 18, C["slate"], italic=True, name="subtitle")
tb(s, 0.6, 3.75, 5.2, 0.75, COURSE, 12, C["mute"], name="course line")
picture(s, "book_fig_000112.jpg", 6.2, 0.9, 3.2, 3.2, "Sweigart (2025), chapter 7 opener illustration")

# 2 route (filled once the slide numbers are known)
ROUTE = new_slide("Today's route", "Five parts; every range is a run of slides you can jump to", None,
                  "Five parts take us from one pair to a chessboard. Each part opens with a divider that names its concepts. The deck follows the sections of the book chapter and adds what current Python offers.")

# 3 questions
s = new_slide("The questions this chapter answers", "The summary comes back to each of them", "Summary",
              "These five questions are the chapter. Keep them in mind: each part of the deck answers one, and the summary answers all five in a line each.")
QS = ["Which operations read, add, replace and remove the pairs of a dictionary?",
      "Which values may be keys, and why must a key be hashable?",
      "How are counting, grouping and nesting solved with dictionaries?",
      "How is a real thing modelled, displayed, copied and written down?",
      "Which terms must a learner look up, and what is each one in everyday life?"]
for i, q in enumerate(QS):
    y = 1.3 + i * 0.68
    box_text(s, 0.5, y, 0.5, 0.56, str(i + 1), 18, C["white"], C["orange"], bold=True, align=PP_ALIGN.CENTER, name="question number", font=HF)
    box_text(s, 1.1, y, 8.4, 0.56, q, 14, C["ink"], C["card"], name="question")
takeaway(s, "Answer these five questions and you have the chapter.", 4.9)

# ---- part 1
PART_FIRST.append(("Part 1: The dictionary and its keys", len(SLIDES) + 1))
divider("Part 1: The dictionary and its keys", "Pairs in braces, found by key",
        [("Dictionary", "A collection of key-value pairs, found by key."), ("Key and value", "The key is the label; the value is what it finds."),
         ("Hashable keys", "A key must never change, so lists cannot be keys."), ("Insertion order", "Keys stay in the order they were added.")],
        ["Pairs sit in braces", "A key finds its value", "Keys must be hashable", "The order of adding is kept"],
        "Part one introduces the dictionary data type. A dictionary holds key-value pairs. A key must be hashable, and since Python 3.7 the keys remember the order in which they were added.")
code("dict_basics"); code("dict_vs_list"); code("insertion_order"); story("guido"); code("hashable_keys")
everyday("Everyday pictures: the dictionary and its keys", "Each term of this part, as something you already know",
         [("The Dictionary Data Type", "A filing cabinet with labelled tabs: you jump to the tab instead of leafing through every page."),
          ("Comparing Dictionaries and Lists", "A queue cares who stands where; a coat rack only cares which labels hang on it."),
          ("dictionary", "A phone book: look up a name and the number is next to it."),
          ("key", "The ticket you hand over at the coat check; it names exactly one coat."),
          ("value", "The coat itself: the thing you get back when you present the ticket."),
          ("key-value pair", "One line of the phone book: a name and its number, written together."),
          ("unhashable type", "Lockers numbered by hair colour: when the colour changes, the locker is lost.")],
         "A dictionary is like a phone book or a coat check. The key is the ticket, the value is the coat, and a key must never change, or the coat is lost.", src="The Dictionary Data Type")

# ---- part 2
PART_FIRST.append(("Part 2: Reading and changing pairs", len(SLIDES) + 1))
divider("Part 2: Reading and changing pairs", "Look at the parts, ask for a key, fill in defaults",
        [("Keys, values, items", "Three views of the parts of a dictionary."), ("in and get()", "Ask whether a key exists without an error."),
         ("setdefault()", "Add a pair only when the key is missing."), ("Change a pair", "Assign, del, pop and merge change the contents.")],
        ["Look at the parts", "Test for a key", "Fill in a default", "Add, remove or merge"],
        "Part two covers the everyday operations. We read keys, values and items, test for a key safely, set defaults, and add, remove and merge pairs.")
code("keys_values_items"); code("key_exists"); code("setdefault"); code("change_pairs"); code("views_follow")
everyday("Everyday pictures: reading the parts", "Keys, values, items and the views that follow them",
         [("Returning Keys and Values", "Reading only the index of a book, only its chapters, or both together."),
          ("keys", "The labels along a shelf edge, without the goods."),
          ("values", "The goods on the shelves, without their labels."),
          ("items", "Each shelf label together with its goods, one pair at a time."),
          ("list()", "A photograph of the shop window: it freezes what the window showed a moment ago.")],
         "keys, values and items are like the labels, the goods and both together on a shop shelf. A view is a window onto the shop, and list() is a photograph of it.", src="Returning Keys and Values")
everyday("Everyday pictures: asking and changing", "Existence tests, defaults and removal",
         [("Checking Whether a Key Exists", "Asking at the desk whether a ticket was ever issued, before you hand it over."),
          ("get", "A polite attendant who answers 'none' instead of shouting when the ticket is unknown."),
          ("Setting Default Values", "An empty form with a pre-printed zero in every box, so counting can start at once."),
          ("setdefault", "Hanging a new coat on a fresh hook only when the hook is free; otherwise the old coat stays."),
          ("del", "Tearing one line out of the phone book: the name and the number go together.")],
         "Asking for a key is like asking the desk about a ticket. get() is the polite attendant, setdefault() hangs a coat only on a free hook, and del tears the line out.", src="Checking Whether a Key Exists")

# ---- part 3
PART_FIRST.append(("Part 3: Programs that count and learn", len(SLIDES) + 1))
divider("Part 3: Programs that count and learn", "A dictionary as the memory of a program",
        [("birthdays.py", "A program that learns a new pair when asked."), ("characterCount.py", "Count every character of a text by key."),
         ("Counter", "One call builds the whole table of counts."), ("Grouping", "Lists as values collect items under one key.")],
        ["Ask and remember", "Count by key", "Let Counter count", "Group items in lists"],
        "Part three uses the dictionary as a program's memory. birthdays.py learns new pairs, characterCount.py counts characters, and Counter and defaultdict shorten counting and grouping.")
code("birthdays"); code("char_count"); story("orwell"); code("counter"); code("grouping")
everyday("Everyday pictures: programs that remember", "Two programs and the two calls that stop them",
         [("birthdays.py", "A pocket diary that learns a new friend's date the first time you ask."),
          ("characterCount.py", "Tally marks on paper: one stroke per sighting, one row per character."),
          ("input()", "A shop assistant who stops and waits at the counter until you answer."),
          ("sys.exit()", "The fire door: you leave the building at once, whatever you were doing.")],
         "birthdays.py is like a pocket diary and characterCount.py like tally marks. input() waits at the counter like an assistant, and sys.exit() is the fire door.", src="birthdays.py")

# ---- part 4
PART_FIRST.append(("Part 4: Structuring data", len(SLIDES) + 1))
divider("Part 4: Structuring data", "Model a real thing with dictionaries and lists",
        [("Data model", "Decide what a real thing must record."), ("Chessboard", "Squares are keys and pieces are values."),
         ("Nested records", "A dictionary inside a dictionary holds records."), ("Inventory and loot", "Counts per item, built from lists.")],
        ["Model the thing", "Print a view of it", "Nest the records", "Total and convert"],
        "Part four is about structuring data. We model a chessboard, validate it, nest dictionaries for a picnic, and turn lists of loot into inventories.")
code("board_model"); story("chess"); code("board_print"); code("chess_moves"); code("validator"); code("picnic_nested"); code("inventory"); code("loot")
everyday("Everyday pictures: models and structures", "A model keeps what matters and leaves the rest out",
         [("data structure", "A shelf layout: where each item is placed decides how quickly you find it."),
          ("data model", "The floor plan drawn before building: it decides which rooms and which details exist at all."),
          ("Model Real-World Things Using Data Structures", "A street map keeps the streets and drops every leaf and parked car."),
          ("Nested Dictionaries and Lists", "Russian dolls: each doll holds a smaller one, and you open them in turn."),
          ("guestpicnic.py", "A picnic checklist that adds up what each guest's basket holds."),
          ("format", "A letter template with blanks, filled in once the names are known.")],
         "A data model is like a floor plan and a street map: it keeps what matters. Nested dictionaries are like Russian dolls, and format is like a letter template.", src="Model Real-World Things Using Data Structures")
everyday("Everyday pictures: the practice projects", "The chessboard, its checker, the inventory and the loot",
         [("Project 1: Interactive Chessboard Simulator", "A pocket chess set that remembers where every piece stands and moves them when told."),
          ("chessboard.py", "A seating chart printed from the guest list: the list is the data, the picture is a view."),
          ("Chess Dictionary Validator", "A match arbiter checking a position is legal: one king each, every piece on a real square."),
          ("Fantasy Game Inventory", "A backpack list that says which items you carry and how many of each."),
          ("List-to-Dictionary Loot Conversion", "Sorting a heap of loot into labelled bins, one tally per bin."),
          ("copy.copy()", "A photocopy of a folder's cover: the new cover still points at the same pages inside.")],
         "The chessboard is like a pocket chess set and the validator like an arbiter. copy.copy() is like photocopying a folder's cover, not its pages.", src="Project 1: Interactive Chessboard Simulator")

# ---- part 5
PART_FIRST.append(("Part 5: Copies and writing data down", len(SLIDES) + 1))
divider("Part 5: Copies and writing data down", "Keep a copy safe, carry data out, check its shape",
        [("Alias and copies", "Shallow copies share what is inside them."), ("JSON and pprint", "Text carries a dictionary out and back."),
         ("TypedDict", "Names the keys of a record for checkers."), ("match patterns", "Test the shape of a dictionary and bind values.")],
        ["Copy with care", "Write it down", "Name the keys", "Match the shape"],
        "Part five finishes the chapter. We copy dictionaries with care, write them as JSON, name their keys with TypedDict, and match their shape with the match statement.")
code("copies"); code("json_pprint"); story("json"); code("typed_records"); code("match_dict")

# python today
s = new_slide("What current Python adds to the chapter", "The book is right about the basics; six things have moved on", "Summary",
              "The chapter's printed outputs still hold. Six things differ or go further: the order promise, the merge operators, live views, the hashing rule, TypedDict and mapping patterns.")
TODAY = [("Insertion order", "Since Python 3.7 the order of adding is a promise, so the book's 'no first item' is out of date."),
         ("Merge operators", "d1 | d2 builds a new dictionary and d1 |= d2 updates one (Python 3.9, PEP 584)."),
         ("Live views", "keys(), values() and items() show later changes, and can be reversed since Python 3.8."),
         ("Hashing rule", "Equal keys must hash alike; a class with __eq__ but no __hash__ cannot be a key."),
         ("TypedDict", "Names the keys of a record for a type checker, but is a plain dict at run time (PEP 589)."),
         ("match patterns", "Mapping patterns test keys and bind values (PEP 634, Python 3.10).")]
for i, (hd, body) in enumerate(TODAY):
    r, c = divmod(i, 2)
    cx, cy = 0.5 + c * 4.6, 1.3 + r * 1.2
    card(s, cx, cy, 4.4, 1.08, C["card"], "card")
    tb(s, cx + 0.12, cy + 0.04, 4.15, 0.3, hd, 13, C["orange"], bold=True, name="card heading", font=HF)
    tb(s, cx + 0.12, cy + 0.36, 4.15, 0.7, body, 11.5, C["ink"], name="card text")
takeaway(s, "Teach the basics from the book and add what Python has learned since.", 4.9)

# practice
s = new_slide("Practice Questions and Practice Programs", "Try these on your own, then compare with the examples of the deck", "Practice Questions",
              "The book ends with questions and programs. Answer the questions from the examples you have seen, then write the three programs yourself: the validator, the inventory and the loot conversion.")
PQ = ["What does the code for an empty dictionary look like?", "What does a dictionary with the key 'foo' and the value 42 look like?",
      "What is the main difference between a dictionary and a list?", "What happens if you try spam['foo'] when spam is {'bar': 100}?",
      "What is the difference between 'cat' in spam and 'cat' in spam.keys()?"]
tb(s, 0.5, 1.25, 4.5, 0.3, "Practice Questions", 14, C["orange"], bold=True, font=HF, name="column heading")
for i, q in enumerate(PQ):
    box_text(s, 0.5, 1.6 + i * 0.64, 4.5, 0.56, q, 11.5, C["ink"], C["card"], name="practice question")
tb(s, 5.2, 1.25, 4.3, 0.3, "Practice Programs", 14, C["orange"], bold=True, font=HF, name="column heading")
for i, (nm, what) in enumerate([("Chess Dictionary Validator", "Check that a board dictionary is a legal position."), ("Fantasy Game Inventory", "Display an inventory and add up its items."),
                                ("List-to-Dictionary Loot Conversion", "Add a list of loot into the inventory.")]):
    box_text(s, 5.2, 1.6 + i * 1.0, 4.3, 0.9, [[(nm, {"bold": True, "size": 12.5, "color": C["dark"], "font": HF})], [(what, {"size": 11.5})]], 11.5, C["ink"], C["card"], name="practice program")
takeaway(s, "Each question is answered by an example in this deck.", 4.9)
everyday("Everyday pictures: closing the chapter", "The last three terms of the chapter",
         [("Summary", "The last line of a recipe card: what you must remember when the cooking is done."),
          ("Practice Questions", "Driving-school mock questions: quick checks that you understood before the real test."),
          ("Practice Programs", "A workshop evening: you build something real with the tools you have just learned.")],
         "A summary is like the last line of a recipe card. Practice questions are like mock driving questions, and practice programs are like a workshop evening.", src="Summary")

# summary
s = new_slide("Summary: the chapter in five lines", "One line for each question the chapter set", "Summary",
              "Here are the five lines that answer the five questions. If one of them feels unproven, go back to the slide that carries its example.")
SUM = ["Assign to add or replace a pair; del and pop remove one; get() helps when a key may be missing.",
       "A key must be hashable: tuples are welcome, lists are not; keys keep their order since Python 3.7.",
       "Counting and grouping use setdefault, Counter or defaultdict; a view follows its dictionary.",
       "A chessboard is a dictionary of occupied squares; a nested dictionary holds a record in a record.",
       "copy.copy() shares the inner dictionaries, deepcopy() does not, and JSON writes the data as text."]
for i, q in enumerate(SUM):
    y = 1.3 + i * 0.68
    box_text(s, 0.5, y, 0.5, 0.56, str(i + 1), 18, C["white"], C["orange"], bold=True, align=PP_ALIGN.CENTER, name="summary number", font=HF)
    box_text(s, 1.1, y, 8.4, 0.56, q, 13, C["ink"], C["card"], name="summary line")
takeaway(s, "If a line feels unproven, its slides hold the example.", 4.9)

# resources
s = new_slide("Resources: where to go from here", "Every link was opened on the day this deck was made", None,
              "These links lead to the textbook, the official documentation, the history behind the stories, a talk on modern dictionaries and a tool to step through your code. The last one is this course's own repository.")
LINKS = [("Read", [("The textbook, chapter 7 (free online)", "https://automatetheboringstuff.com/3e/chapter7.html"),
                   ("Python tutorial: data structures", "https://docs.python.org/3/tutorial/datastructures.html"),
                   ("Built-in types: dict and its views", "https://docs.python.org/3/library/stdtypes.html#mapping-types-dict")]),
         ("Libraries", [("collections: Counter and defaultdict", "https://docs.python.org/3/library/collections.html"),
                        ("copy: shallow and deep copies", "https://docs.python.org/3/library/copy.html"),
                        ("json: the JSON encoder and decoder", "https://docs.python.org/3/library/json.html")]),
         ("History", [("Guido's ruling on dictionary order, 2017", "https://mail.python.org/pipermail/python-dev/2017-December/151283.html"),
                      ("PEP 584: merge operators for dict", "https://peps.python.org/pep-0584/"),
                      ("RFC 8259: the JSON standard", "https://datatracker.ietf.org/doc/html/rfc8259")]),
         ("Try and watch", [("Modern Dictionaries, R. Hettinger (video)", "https://www.youtube.com/watch?v=p33CVV29OG8"),
                            ("Python Tutor: step through your code", "https://pythontutor.com/"),
                            ("pprint: tidy printing of nested data", "https://docs.python.org/3/library/pprint.html"),
                            ("The course repository and corpus", "https://github.com/altunelyusuf/AdvancedProgrammingWithPython")])]
y = 1.22
for head, items in LINKS:
    tb(s, 0.5, y, 1.25, 0.3, head, 12.5, C["orange"], bold=True, font=HF, name="link group")
    for k, (lab, url) in enumerate(items):
        r, c = divmod(k, 2)
        host = url.split("//")[1].split("/")[0].replace("www.", "")
        tb(s, 1.85 + c * 3.95, y + r * 0.32, 3.8, 0.3, [[(lab, {"link": url, "color": C["slate"], "bold": True})]], 11.5, name="link")
    y += 0.32 * math.ceil(len(items) / 2) + 0.14
NLINKS = sum(len(i) for _, i in LINKS)
takeaway(s, "%d links, each opened on the day this deck was built." % NLINKS, 4.93)

# closing
s = new_slide("What you should now be able to say", "Four claims, each carried by a result you saw printed", None,
              "These four claims are what you should leave with. Bring one example you could not predict, and we will run it together.")
CL = ["A dictionary finds values by key, and keys must be hashable.", "Counting and grouping are a few lines with setdefault, or one with Counter.",
      "A real thing becomes a dictionary of the parts that are there.", "A shallow copy shares the inner dictionaries, and JSON writes the data down."]
for i, q in enumerate(CL):
    y = 1.3 + i * 0.7
    box_text(s, 0.5, y, 0.5, 0.58, str(i + 1), 18, C["white"], C["orange"], bold=True, align=PP_ALIGN.CENTER, name="claim number", font=HF)
    box_text(s, 1.1, y, 8.4, 0.58, q, 14, C["ink"], C["card"], name="claim")
takeaway(s, "Questions are welcome; bring one example you could not predict.", 4.9)

# ---------------------------------------------------------------- route, numbering, manifest
N = len(SLIDES)
firsts = [n for _, n in PART_FIRST]
route_rows = [("Opening: questions and the map of the chapter", 1, firsts[0] - 1)]
for k, (title, n) in enumerate(PART_FIRST):
    last = (firsts[k + 1] - 1) if k + 1 < len(firsts) else None
    route_rows.append((title, n, last))
tail_start = next(i for i, sl in enumerate(SLIDES, 1) if sl.shapes.title.text_frame.text.startswith("What current Python adds"))
route_rows[-1] = (route_rows[-1][0], route_rows[-1][1], tail_start - 1)
route_rows.append(("Today's Python, practice, summary and resources", tail_start, N))
for i, (nm, a, b) in enumerate(route_rows):
    y = 1.25 + i * 0.44
    box_text(ROUTE, 0.5, y, 0.4, 0.36, str(i + 1), 12, C["white"], C["orange"], bold=True, align=PP_ALIGN.CENTER, name="route number", font=HF)
    box_text(ROUTE, 1.0, y, 5.6, 0.36, "%s  (slides %d-%d)" % (nm, a, b), 12, C["ink"], C["card"], name="route row")
n_code = len(X.EXAMPLES)
for k, (n, lab) in enumerate([(str(N), "slides, numbered bottom-right"), (str(n_code), "code examples, each with its result"), ("4", "true stories: who, what, when, where, why, how")]):
    card(ROUTE, 6.9, 1.25 + k * 1.03, 2.6, 0.93, C["card"], "stat card")
    tb(ROUTE, 6.95, 1.25 + k * 1.03, 2.5, 0.45, n, 24, C["orange"], bold=True, font=HF, name="stat number", align=PP_ALIGN.CENTER)
    tb(ROUTE, 6.95, 1.68 + k * 1.03, 2.5, 0.48, lab, 10.5, C["ink"], name="stat label", align=PP_ALIGN.CENTER)
tb(ROUTE, 0.5, 4.4, 9.0, 0.45, "Book sections: The Dictionary Data Type, Model Real-World Things Using Data Structures, Nested Dictionaries and Lists, Summary, Practice Questions, Practice Programs.",
   11, C["mute"], italic=True, name="book sections")
takeaway(ROUTE, "Five parts, from one pair to a chessboard, all of it executed.", 4.9)

for i, sl in enumerate(SLIDES, 1):
    tb(sl, 8.3, 5.3, 1.2, 0.22, "%d / %d" % (i, N), 10.5, C["mute"], align=PP_ALIGN.RIGHT, name="slide number")

prs.core_properties.title = "SEN0414 Chapter 7: Dictionaries and Structuring Data (3rd edition), lecture deck v2.0.0"
prs.core_properties.author = "Yusuf Altunel"
prs.core_properties.subject = "SEN0414 Advanced Programming"
os.makedirs(os.path.dirname(OUT_DECK), exist_ok=True)
prs.save(OUT_DECK)
print("written", os.path.relpath(OUT_DECK, ROOT), "-", N, "slides,", n_code, "code examples")

# ---- the chapter-code manifest: the examples in slide order, the code exactly as in the code boxes (the '>>> ' prefix removed, the lines of the boxes joined)
order = sorted(X.EXAMPLES, key=lambda e: SLIDE_OF[e["id"]])
assert [e["id"] for e in order] == [e["id"] for e in X.EXAMPLES], "the examples are not in slide order"
man = {"chapter": 7, "version": "1.0.0", "kind": "chapter-code manifest", "deck": os.path.relpath(OUT_DECK, ROOT),
       "about": "The code examples of the chapter 7 deck, in the order of the code slides (order = slide order). The page's chapter-code tab lists them by NAME in this order; "
                "the code runs in the page with the Python standard library only; every example is self-contained; the expected result is what the run printed.",
       "executed_with": {"python": PYV, "library": None},
       "library": {"file": None, "sha256": None, "data_files": [],
                   "page_requirements": ["the Python standard library: collections (Counter, defaultdict), copy, json, pprint, typing (TypedDict), types (MappingProxyType)",
                                         "the match statement (Python 3.10 or later) and the assignment expression (3.8 or later)",
                                         "no keyboard input: birthdays.py is scripted with an iterator"]},
       "prelude": X.PRELUDE, "examples": []}
for k, ex in enumerate(order, 1):
    man["examples"].append({"order": k, "id": ex["id"], "name": ex["name"], "slide": SLIDE_OF[ex["id"]], "concepts": ex["concepts"],
                            "code": X.code_text(ex), "expected": RUNS[ex["id"]]["out"]})
os.makedirs(os.path.dirname(OUT_MANIFEST), exist_ok=True)
json.dump(man, open(OUT_MANIFEST, "w", encoding="utf-8"), indent=1, ensure_ascii=True)
print("written", os.path.relpath(OUT_MANIFEST, ROOT), "-", len(man["examples"]), "examples")

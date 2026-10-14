"""Builds deck_plan_v1_0_0.json - SEN0414 chapter 25 (the Threads subject: the multithreading material of chapter 17 of the 2nd edition of Automate the Boring Stuff with Python, which
the 3rd edition dropped) on the CME classroom standard.

Same regime as chapters 10 to 23: numbered warm-ivory slides, an agenda with exact slide ranges, a summary before the resources, full-sentence takeaway
strips, stories with fact rows, consoles and programs (whole or honest excerpts, labelled with their line numbers) with their results as Python printed
them. Every console result and program transcript comes from examples_out_v1_0_0.json (made by examples_run_v1_0_0.py under Python 3.14.6 with requests 2.34.2 and
beautifulsoup4 4.15.0); the speaker notes are prose for the reader and carry only what the chapter's RDODI research package (03-materials/ch25/rdodi,
sen0414_ch25_rdodi_data_v1_0_0.py, findings F1 to F25, 64 executed leaves, 74 sources), its records (08-tooling/ch25-page/*.json) or a program of this deck established.

What this chapter adds against chapter 23:
  * EVERY TIMING IS RECORDED, NONE IS MEASURED AGAIN. The box has 2 CPUs and a timing program run beside another build would print other numbers, so no program of the deck prints
    a duration: a program that waits prints a list, a name, an error, or a boolean with a wide margin. The research's timings (seconds for a loop, microseconds to start a thread, the
    lost updates of a race) are read by tables and charts from ch25-page/timing_record_v1_0_0.json (single runs of 2026-10-14, each taken after the load average fell below 1.0)
    and their slides say 'Recorded'. The deck check computes every cell and every bar again from that file.
  * THE LOCAL STAND-IN IS A SERVER. The chapter's XKCD downloader is run against an HTTP server of the program on 127.0.0.1; xkcd.com is never contacted. The two slides that show
    those programs say 'local stand-in' and 'xkcd.com is never contacted' (honesty_check_v1_0_0.py requires the words).
  * THE STORIES HAVE REAL PICTURES. The four photographs and pictures (Therac-25, Dijkstra, the 2003 blackout map, a multithreaded process) are files of Wikimedia Commons fetched on
    2026-10-14 and reduced here; photos_v1_0_0.json records author, licence, source page, the SHA-256 of the file and of the original, and what was changed. Each caption begins with the credit
    ('photo <file>: <credit>') and program_check_v1_0_0.py requires the slide to carry that file. One more picture is saved by a program (skipped.png, 'image skipped.png made by
    fixedCut_v1_0_0.py') and run again by the same check.
What the deck does not run: the free-threaded build of Python 3.13, a C extension that re-enables the GIL, Windows and macOS, more than 2 CPUs, the real xkcd.com, runs under load
(meta.notExecuted names the slides). The seven narrative diagrams of the chapter (sen0414_ch25_diagrams_v1_0_0.py, grounding 0.84 or more) are drawn as native shapes
(diagram_shapes_v1_0_0.py) and checked by diagram_check_v1_0_0.py; four tables and two charts are native PowerPoint objects whose data the deck check computes again. All four stories are
on slides.

Usage: python3 deck_build_v1_0_0.py   (writes deck_plan_v1_0_0.json and links_v1_0_0.json beside itself; needs rdflib)
"""
__version__ = "1.0.0"
import importlib.util
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import diagram_shapes_v1_0_0 as DS


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ST = load("stories25", os.path.join(HERE, "..", "sen0414_ch25_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
DG = load("diagrams25", os.path.join(HERE, "..", "sen0414_ch25_diagrams_v1_0_0.py"))
NODES = DG.nodes_from_ttl(os.path.join(HERE, "..", ".."))
_bad = DG.run_checks(NODES)
if _bad:
    raise SystemExit("REFUSED: the diagrams fail their own checks: %r" % _bad[:3])
DIAG = {d["id"]: d for d in DG.DIAGRAMS}
RD = load("rdodi25", os.path.join(HERE, "..", "sen0414_ch25_rdodi_data_v1_0_0.py"))
EX = json.load(open(os.path.join(HERE, "examples_out_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s; no row reads the clock or the network" % PYV
G = {k: [[s, (o or "")] for s, o in v] for k, v in EX.items() if not k.startswith("_")}
PROGS = EX["_programs"]
IMGDIR = os.path.join(HERE, "images")
PHDIR = os.path.join(HERE, "photos")
PHOTOS = {x["file"]: x for x in json.load(open(os.path.join(HERE, "photos_v1_0_0.json")))["photos"]}
CQ1, CQ2 = RD.CQS
CW = 0.0088  # inches per character per point of Courier New, as the shared fit check measures it

L_NOTEXEC = "NOT EXECUTED"
L_REC = "Recorded"


def lines_of(rows):
    return sum(1 + (1 if out.strip() else 0) for _, out in rows)


ROWS_SHOWN = sum(len(G[k]) for k in ("title", "inc", "locals", "pins"))


def con(group, x, y, w, fs=11, label=None, cap=True, rows=None):
    """A console panel sized from its rows; returns (item, bottom y)."""
    rr = rows if rows is not None else G[group]
    maxlen = max(max(len(st) + 4, len(out)) for st, out in rr)
    fs = min(fs, round((w - 0.4) / (maxlen * CW), 1))
    capt = CAP if w >= 3.9 else "run under Python %s; no clock, no network" % PYV
    if fs < 7:
        raise SystemExit("REFUSED: console %s cannot fit unwrapped in %.1f in (fs %.1f)" % (group, w, fs))
    L = lines_of(rr)
    h = round(L * fs * 1.23 / 72.0 + 0.36 + 0.02 * max(0, L - 1), 2)
    it = {"t": "code", "x": x, "y": y, "w": w, "h": h, "rows": rr, "fs": fs}
    if cap:
        it["cap"] = capt
    if label:
        it["label"] = label
    return it, round(y + h + (0.26 if cap else 0), 2)


def span(pname, first, last=None):
    """1-based line numbers (a, b) of the program lines from the first containing `first` to the first containing `last`."""
    ls = PROGS[pname]["code"].rstrip("\n").split("\n")
    a = next(i for i, l in enumerate(ls, 1) if first in l)
    b = len(ls) if last is None else next(i for i, l in enumerate(ls, 1) if i >= a and last in l)
    return a, b


def body(pname):
    """the first line of a Cut that is shown: line 1 (a Cut of this chapter is shown whole unless a slide names the lines)"""
    return 1


def pw(pname, lines=None, out=True, fs=7.0):
    pr = PROGS[pname]
    L = pr["code"].rstrip("\n").split("\n")
    a, b = (1, len(L)) if lines is None else lines
    ws = [len(l) for l in L[a - 1:b]]
    if out and pr["transcript"]:
        t = pr["transcript"].split("\n")
        ws += [len(t[0]) + 7] + [len(x) for x in t[1:]]
    return round(max(ws) * CW * fs + 0.4, 2)


def bestfs(pname, lines, wmax, hmax, out=True, lo=7.0, hi=9.5):
    pr = PROGS[pname]
    a, b = lines
    n = (b - a + 1) + (pr["transcript"].count("\n") + 1 if out and pr["transcript"] else 0)
    fs = hi
    while fs >= lo:
        if pw(pname, lines, out, fs) <= wmax and n * (fs * 1.22 / 72.0 + 0.02) + 0.30 <= hmax:
            return fs
        fs -= 0.5
    raise SystemExit("REFUSED: %s lines %d-%d (%d lines with the transcript) do not fit %.2f x %.2f in at %.1f pt (width needs %.2f, height needs %.2f)"
                     % (pname, a, b, n, wmax, hmax, lo, pw(pname, lines, out, lo), n * (lo * 1.22 / 72.0 + 0.02) + 0.30))


def prog(pname, x, y, w, fs=7.0, lines=None, show_out=True):
    """A chapter program (or an honest excerpt) with its transcript, sized from its text; returns (item, bottom y)."""
    y = max(y, 1.55)
    pr = PROGS[pname]
    all_lines = pr["code"].rstrip("\n").split("\n")
    a, b = (1, len(all_lines)) if lines is None else lines
    shown = all_lines[a - 1:b]
    out = pr["transcript"] if show_out else ""
    outlines = (out.count("\n") + 1) if out else 0
    need = pw(pname, (a, b), show_out, fs)
    if need > w + 0.005:
        raise SystemExit("REFUSED: program %s lines %d-%d cannot fit unwrapped in %.2f in at %.1f pt (needs %.2f)" % (pname, a, b, w, fs, need))
    L = len(shown) + outlines
    h = round(L * (fs * 1.22 / 72.0 + 0.02) + 0.30, 2)
    label = "program %s, lines %d to %d of %d" % (pname, a, b, len(all_lines))
    if len(label) > (w - 0.1) / 0.0725:
        raise SystemExit("REFUSED: caption %r is too long for a %.2f in panel" % (label, w))
    it = {"t": "prog", "x": x, "y": y, "w": w, "h": h, "lines": shown, "fs": fs, "compact": bool(out),
          "out": out if out else None, "outLabel": "prints", "label": label}
    return it, round(y + h, 2)


def pfit(pname, x, y, wmax, hmax, a=None, b=None, right=False, lo=7.0, hi=9.0):
    """prog() of the lines a to b of a Cut (default: the body after 'd = wd()' to the last line) at the largest size that fits wmax x hmax;
    right=True puts the panel against the right margin. Returns (item, bottom y, a, b, x, w)."""
    a = body(pname) if a is None else a
    b = len(PROGS[pname]["code"].rstrip("\n").split("\n")) if b is None else b
    f = bestfs(pname, (a, b), wmax, hmax, lo=lo, hi=hi)
    w = pw(pname, (a, b), True, f)
    _lab = "program %s, lines %d to %d of %d" % (pname, a, b, len(PROGS[pname]["code"].rstrip("\n").split("\n")))
    w = max(w, round(len(_lab) * 0.0725 + 0.12, 2))
    x = round(9.5 - w, 2) if right else x
    it, bot = prog(pname, x, y, w, fs=f, lines=(a, b), show_out=True)
    return it, bot, a, b, x, w


def factrow(sid, x=0.5, y=4.58, w=9.0):
    st = STORY[sid]
    host = st["link"].split("//")[1].split("/")[0].replace("www.", "")
    return {"t": "factrow", "x": x, "y": y, "w": w, "who": st["who"], "where": st["where"],
            "when": st["when"], "link": st["link"], "linkText": host}


def story_notes(sid):
    st = STORY[sid]
    return st["story"] + " The account rests on these sources. " + st["source"]


def card(head, body_, x, y, w, h, fs=11.5, accent=None):
    if len(head) > (w - 0.4) / 0.112:
        raise SystemExit("REFUSED: card heading %r does not fit one line of a %.2f in card" % (head, w))
    it = {"t": "card", "head": head, "body": body_, "x": x, "y": y, "w": w, "h": h, "fs": fs}
    if accent:
        it["accent"] = accent
    return it


def foot(body_, x, y, w, fs=9.5):
    h = round(DS.need_h(body_, w, fs) + 0.04, 2)
    return {"t": "foot", "x": x, "y": y, "w": w, "h": h, "fs": fs, "body": body_}


def stack(bodies, x, y, w, fs=8.5, gap=0.04):
    out = []
    for b in bodies:
        f = foot(b, x, round(y, 2), w, fs=fs)
        out.append(f)
        y = f["y"] + f["h"] + gap
    return out


def diagram(did, kind, box, **kw):
    """The shapes item of a narrative diagram and its caption (which names the diagram and its measured grounding)."""
    d = DIAG[did]
    fn = {"activity": DS.activity, "sequence": DS.sequence, "lifecycle": DS.lifecycle_col, "usecases": DS.usecases, "mindmap": DS.mindmap}[kind]
    it = fn(d["data"], box, **kw)
    h, n = d["grounding"]
    body_ = "diagram %s - %s pattern, %d of %d words grounded in the chapter's text" % (did, d["pattern"], h, n)
    cap = {"t": "foot", "x": box[0], "y": round(box[1] + box[3] + 0.03, 2), "w": box[2], "h": round(DS.need_h(body_, box[2], 8.5) + 0.04, 2), "fs": 8.5,
           "body": body_}
    it["did"] = did
    return it, cap


def png_size(fn):
    with open(os.path.join(IMGDIR, fn), "rb") as f:
        head = f.read(24)
    return struct.unpack(">II", head[16:24])


def img(fn, x, y, maxw, maxh):
    """A picture a program saved, placed in the largest box of its own shape that fits maxw x maxh inches at (x, y); returns (item, bottom y, right x)."""
    if fn not in EX["_images"]:
        raise SystemExit("REFUSED: %s is not a picture of the recording" % fn)
    pw_, ph_ = png_size(fn)
    k = min(maxw / pw_, maxh / ph_)
    w, h = round(pw_ * k, 2), round(ph_ * k, 2)
    it = {"t": "img", "path": os.path.join(IMGDIR, fn), "x": x, "y": y, "w": w, "h": h}
    return it, round(y + h, 2), round(x + w, 2)


def imgcap(fns, x, y, w, fs=8.5):
    body_ = "; ".join("image %s made by %s" % (fn, EX["_images"][fn]["program"]) for fn in fns)
    return foot(body_, x, y, w, fs=fs)


def tpanel(pname, x, y, w, fs=7.5):
    pr = PROGS[pname]
    t = pr["transcript"].split("\n")
    need = round(max(len(l) for l in t) * CW * fs + 0.4 + 0.5, 2)
    if need > w + 0.005:
        raise SystemExit("REFUSED: the transcript of %s needs %.2f in at %.1f pt, the panel has %.2f" % (pname, need, fs, w))
    h = round(len(t) * (fs * 1.22 / 72.0 + 0.02) + 0.30, 2)
    label = "transcript of program %s" % pname
    return {"t": "prog", "x": x, "y": max(y, 1.55), "w": w, "h": h, "lines": [], "fs": fs, "compact": True, "out": pr["transcript"], "outLabel": "prints", "label": label}, round(max(y, 1.55) + h, 2)


S = []
SHOWN = {}
NOTEXEC = []
RECORDED = []
STANDIN = {}
LATE = []


def content(title, sub, items, notes, take, lede=None, notexec=False, recorded=False):
    if lede and len(lede.split()) > 34:
        raise SystemExit("REFUSED: lede on %r runs past the gate" % title)
    if len(take.split()) > 24 or not take.endswith(".") or len(take) > 84:
        LATE.append("takeaway %r (%d)" % (take, len(take)))
    if len(title) > 44:
        LATE.append("title %r" % title)
    if len(sub) > 86:
        LATE.append("subtitle %r (%d)" % (sub, len(sub)))
    for it in items:
        if it["t"] in ("code", "prog", "shapes", "card", "boxes", "chips", "stat", "beats", "factrow", "numlist", "bullets", "links", "foot", "text", "img", "table", "chart"):
            if it["y"] + it.get("h", 0.4) + (0.26 if it.get("cap") and it["t"] == "code" else 0) > 5.0 or it["x"] + it["w"] > 9.56:
                raise SystemExit("REFUSED: item %s on %r reaches y %.2f / x %.2f (starts %.2f)" % (it["t"], title, it["y"] + it.get("h", 0.4), it["x"] + it["w"], it["y"]))
        if it["t"] == "shapes":
            SHOWN[it["did"]] = len(S) + 1
        if it["t"] == "prog":
            nm = it["label"].replace("transcript of program ", "").replace("program ", "").split(",")[0]
            if PROGS[nm]['kind'] == 'standin':
                STANDIN.setdefault(len(S) + 1, []).append(nm)
    blob = json.dumps(items)
    if notexec:
        NOTEXEC.append(len(S) + 1)
        if L_NOTEXEC not in blob:
            raise SystemExit("REFUSED: slide %r is declared NOT EXECUTED but says nothing of it" % title)
    if recorded:
        RECORDED.append(len(S) + 1)
        if L_REC not in blob:
            raise SystemExit("REFUSED: slide %r is declared Recorded but says nothing of it" % title)
    sl = {"kind": "content", "title": title, "sub": sub, "items": items, "notes": notes, "take": take, "bg": "light"}
    if lede:
        sl["lede"] = lede
    S.append(sl)


def hid(pn, a, b, what_before="imports, helpers, the folder and the download check", what_after=None):
    """The words that say which lines of the program are not on the slide: lines 1 to a-1, and lines b+1 to n."""
    n = len(PROGS[pn]["code"].rstrip("\n").split("\n"))
    out = []
    if a > 1:
        out.append(("Lines 1 to %d (%s) are not shown." % (a - 1, what_before)) if a > 2 else ("Line 1 (%s) is not shown." % what_before))
    if b < n:
        out.append(("Lines %d to %d (%s) are not shown." % (b + 1, n, what_after or "the rest")) if b + 1 < n else ("Line %d (%s) is not shown." % (n, what_after or "the rest")))
    return " ".join(out)



SAY_SI = "Stand-in: the downloader asks a local stand-in, an HTTP server of this program on 127.0.0.1; xkcd.com is never contacted."
REC = "Recorded 14 Oct 2026"
NE = "NOT EXECUTED here"


def rec(t):
    return "Recorded 14 Oct 2026: " + t


def ne(t):
    return "NOT EXECUTED here: " + t


def capfoot(cap, extra, x, y, w, fs=8):
    """the caption of a diagram ('diagram <id> - <pattern> pattern, ...') followed by more text, as one foot placed where there is room"""
    return foot(cap["body"] + ". " + extra, x, y, w, fs=fs)


def cut(pn):
    return PROGS[pn]["code"].rstrip("\n").split("\n")


# ---- photographs of the stories (Wikimedia Commons; credit, licence and what was changed are in photos_v1_0_0.json) -----------------------------
def photo(fn, x, y, maxw, maxh):
    """A photograph of a story, placed in the largest box of its own shape that fits maxw x maxh inches at (x, y); returns (item, bottom y, right x)."""
    info = PHOTOS[fn]
    k = min(maxw / info["width"], maxh / info["height"])
    w, h = round(info["width"] * k, 2), round(info["height"] * k, 2)
    return {"t": "img", "path": os.path.join(PHDIR, fn), "x": x, "y": y, "w": w, "h": h}, round(y + h, 2), round(x + w, 2)


def photocap(fn, x, y, w, fs=8, extra=""):
    info = PHOTOS[fn]
    return foot("photo %s: %s. %s%s" % (fn, info["credit"], extra + " " if extra else "", "Reduced copy: " + info["changes"] + "."), x, y, w, fs=fs)


def imgcap1(fn, x, y, w, fs=8):
    return foot("image %s made by %s" % (fn, EX["_images"][fn]["program"]), x, y, w, fs=fs)


def pq(pname, x, y, wmax, hmax, a, b, right=False, lo=7.0, hi=9.0):
    return pfit(pname, x, y, wmax, hmax, a=a, b=b, right=right, lo=lo, hi=hi)


# ---- 1 title ---------------------------------------------------------------------------------------------------
c1, _ = con("title", 5.0, 0.25, 4.5, fs=8, cap=False)
S.append({"kind": "title", "title": "Ch. 25: Threads",
          "sub": "Threads, locks, pools and the GIL: the multithreading the 3rd edition dropped",
          "items": [c1, foot("Every output on these slides was printed by the Python above when the deck was made, and every picture was either saved by a program that is run again to check it or is a credited file of Wikimedia Commons. "
                             "Windows, macOS, more than 2 CPUs and the real xkcd.com were never used: the downloaders ask a local stand-in, and what could not be run is marked on its slide.",
                             0.6, 3.85, 8.8, fs=11)],
          "notes": "Chapter 25 of this course is the Threads subject. It takes the multithreading material of chapter 17 of the 2nd edition of Automate the Boring Stuff with Python, which the 3rd edition dropped, and teaches it with Python %s, where threads, executors, the global interpreter lock and the free-threaded build have all moved on. "
                   "The number 25 is the slot of this subject in the course and not a chapter number of either edition. "
                   "The 2nd edition chapter was read on 14 October 2026. The research ran every listing that works offline, found three places where the chapter's prose or listing differs from what Python does, and added what the chapter leaves out: locks, events, semaphores, queues, pools, the global interpreter lock, processes and asyncio. "
                   "Every output on the slides was printed by Python %s with requests 2.34.2 and beautifulsoup4 4.15.0, the interpreter the console above reports. "
                   "The programs that wait print only lists, names, errors and booleans and never a duration, because the machine had 2 CPUs and a duration measured again would be another number. "
                   "The timings that the research measured once, on a quiet machine, are on slides marked Recorded. What could not be run is marked NOT EXECUTED on its slide: the free-threaded build of Python 3.13, a C extension that switches the lock back on, Windows and macOS, more than 2 CPUs and the real xkcd.com, which no program here ever contacted." % (PYV, PYV),
          "bg": "light"})

# ---- 2 agenda (filled in at the end) -------------------------------------------------------------------------------
S.append({"kind": "content", "title": "Today's route", "sub": "", "items": [], "notes": "", "take": "", "bg": "light"})

# ---- 3 questions ------------------------------------------------------------------------------------------------
_nb = len(DIAG["ThreadsAtAGlance"]["data"]["branches"])
content("The questions this chapter answers", "The chapter's own competency questions; the summary comes back to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 2.3, "fs": 11, "items": [CQ1, CQ2]},
         {"t": "chips", "x": 0.5, "y": 3.8, "w": 9.0, "h": 0.5, "fs": 10,
          "items": ["%d branches" % _nb, "%d topics" % len(NODES), "%d console rows" % ROWS_SHOWN,
                    "%d programs run" % len(PROGS), "%d diagrams" % len(DIAG), "%d pictures" % (len(EX["_images"]) + len(PHOTOS)), "Python %s" % PYV]}],
        "The first question is the spine of the chapter, and the deck answers it slide by slide. The listings that run offline print what the chapter says: a second thread prints its line last, the arguments of the target arrive through args and kwargs, and join() waits. "
        "Three things differ from the text. The chapter's prose writes the keyword dictionary with one space fewer than its listing and prints Cats& Dogs& Frogs. The downloader as printed never calls start(), so no request is made and join() raises RuntimeError. "
        "And with the missing line added, the downloader requests 125 of the 139 comic numbers its loop covers and never asks for 9, 19, 29 and every tenth number up to 139. "
        "What could only be read is the part that needs another machine: the free-threaded build of Python 3.13, a C extension that switches the global interpreter lock back on, Windows and macOS, more than 2 CPUs and the real xkcd.com. "
        "The second question is about size, and every size comes from a single run. Four threads that each ran counter += 1 one million times lost between 2,500,522 and 2,913,206 of 4,000,000 updates in each of 3 runs on the free-threaded 3.14.6 and none in 12 runs on the builds with the lock. "
        "Four CPU-bound tasks took 0.89 s one after another and 1.003 s on 4 threads on the standard build, and 1.292 s against 0.522 s on the free-threaded build; a pool of 2 processes took 0.667 s where one process took 0.963 s; starting a thread took 112 microseconds and starting a process 5.4 milliseconds. "
        "Each slide says where its figure comes from.",
        "Know what ran, what only failed, and what was only read.")

# ---- 4 what a program can do ---------------------------------------------------------------------------------------
dg, dcap = diagram("WhatAProgramCanDoWithThreads", "usecases", (0.5, 1.4, 4.6, 2.75), fs=8)
c4, bot4 = con("pins", 5.3, 1.45, 4.2, fs=8, cap=True)
content("What a program can do with threads", "Seven uses; the 2nd edition taught threads, the 3rd edition dropped them",
        [dg, dcap, c4,
         foot(rec("the 2nd edition's chapter 17 page (200, 103,558 bytes) holds 9 code paragraphs on multithreading, and the 3rd edition's chapter 19, with the same title, has 0 occurrences of the word thread."), 5.3, round(bot4 + 0.08, 2), 4.2, fs=9),
         foot("The chapter teaches a Thread with a target, start(), args and kwargs, join(), and the XKCD downloader.", 5.3, round(bot4 + 0.98, 2), 4.2, fs=9)],
        "The use-case diagram lists what a program can ask of threads in this chapter: start a thread with a target, pass args and kwargs, wait with join(), guard a counter with a lock, hand items over with a queue, run functions on a pool with map(), and overlap waiting with asyncio.gather(). "
        "They are independent calls to the standard library, which is why the picture is a set of uses and not a sequence. "
        "The console runs under the interpreter of the deck: the global interpreter lock is on in this standard build, the build variable Py_GIL_DISABLED is 0, and the machine reports 2 CPUs, a number that the later slides rely on because every speed figure was taken on 2 CPUs. "
        "The card records what the research found on 14 October 2026 and this deck does not read again: the 2nd edition's chapter 17 page answered 200 with 103,558 bytes and its multithreading section holds 9 code paragraphs, and the page of the 3rd edition's chapter 19, which has the same title, answered 200 with no occurrence of the word thread while it still teaches the subprocess module. "
        "The chapter ends with practice questions 7 and 8 on threads. The number 25 of this deck is the slot of the subject in the course and not a chapter number of either edition.",
        "Threads let one program do several things at once.", recorded=True)

# ---- 5 starting a thread ----------------------------------------------------------------------------------------------
pn = "startCut_v1_0_0.py"
p5, bot5, a5, b5, x5, w5 = pfit(pn, 0.5, 1.55, 5.7, 3.42)
xr = round(x5 + w5 + 0.2, 2)
content("Starting a thread", "The new thread's line comes last, although start() was called before the main line",
        [p5,
         *stack(["start() returns at once: the line Wake up! came after the line End of program, although the thread was started first.",
                 "The main program is itself a thread, MainThread; each start() adds one more.",
                 "While the new thread ran, 2 Thread objects were alive: the main thread and itself.",
                 "The program ended only after the last thread did; join() made the main thread wait."],
                xr, 1.5, round(9.5 - xr, 2), fs=9, gap=0.07)],
        "The program is the chapter's threadDemo.py with the nap shortened to half a second. The main thread prints Start of program., creates a Thread whose target is takeANap, calls start() and prints End of program.; the new thread sleeps and prints Wake up! last, which is the order the transcript shows, and it shows that two flows of control run at once. "
        "The second half of the program asks who is who: the main program runs in a thread named MainThread, a thread created later is named Thread-2 (f), because the number counts every thread made so far and the function name is added in brackets, and while it ran the program had 2 thread objects alive. "
        "A learner should predict the order of the three lines before running it. The research also timed a process of the same shape: it ended with return code 0 and lasted at least the nap of its second thread although the main thread had printed its last line within 0.2 s, so a Python program does not end until its last non-daemon thread has ended. "
        "That is the rule behind the join loop of the chapter's downloader and behind the daemon flag, which later slides take up.",
        "start() returns at once; the new thread runs beside the main one.")

# ---- 6 arguments of the target ---------------------------------------------------------------------------------------------
pn = "argsCut_v1_0_0.py"
p6, bot6, a6, b6, x6, w6 = pfit(pn, 0.5, 1.55, 5.2, 3.0)
xr = round(x6 + w6 + 0.2, 2)
content("The arguments of the target", "args is a list, kwargs a dictionary; the chapter's prose and listing differ",
        [p6,
         *stack(["The list becomes the positional arguments of the target and the dictionary its keyword arguments, as in an ordinary call.",
                 "The chapter's listing has {'sep': ' & '} and prints Cats & Dogs & Frogs; its prose writes {'sep': '& '}, which prints Cats& Dogs& Frogs.",
                 "target=print('Now', 'not later') calls print at once, in the main thread, and hands the thread None: there was nothing for it to run."],
                xr, 1.5, round(9.5 - xr, 2), fs=9, gap=0.08)],
        "Passing arguments to a thread is the same idea as calling a function: args is a list of positional arguments and kwargs a dictionary of keyword arguments, and the program shows both with print as the target. "
        "The first call uses the separator of the chapter's listing, a space, an ampersand and a space, and prints Cats & Dogs & Frogs. The second call uses the separator as the chapter's explanation writes it, an ampersand and a space, and prints Cats& Dogs& Frogs. "
        "The prose and the listing of the chapter differ by one character, which is a small case of why a course should run the text it teaches. "
        "The third call is the mistake the chapter warns about: writing target=print('Now', 'not later') calls print at once and passes its return value, None, as the target. The line appears from the main thread, nothing runs in a second thread, and the thread is not alive afterwards. "
        "The error is silent, since nothing fails, and only the place where the output appears gives it away.",
        "Pass the function itself, with args and kwargs; never its call.")

# ---- 7 the life of a Thread object -------------------------------------------------------------------------------------------
pn = "lifeCut_v1_0_0.py"
dg, dcap = diagram("TheLifeOfAThread", "lifecycle", (0.5, 1.4, 3.0, 2.2), fs=8, sw=1.4, sh=0.36, sfs=8, top=0.3, lab_w=1.5)
p7, bot7, a7, b7, x7, w7 = pfit(pn, 3.7, 1.55, 5.8, 3.3, right=True)
content("The life of a Thread object", "Created, started once, finished; a name follows it and an error stays in it",
        [dg, dcap, p7,
         *stack(["Names count every thread made so far, Thread-1 (f), Thread-2 (f); name= chooses one.",
                 "start() works once: a second call raised RuntimeError."],
                0.5, round(dcap["y"] + dcap["h"] + 0.1, 2), 3.0, fs=8.5, gap=0.05)],
        "The state diagram follows one Thread object: it is created, start() runs the target in a new thread, and it has finished when the target returns. "
        "The program shows what follows from that. The default names are Thread-1 (f) and Thread-2 (f), and a thread given name='copier' keeps its name. A thread object is single use, so the second start() raised RuntimeError: threads can only be started once, which is why the chapter's loop makes a new Thread for each range. "
        "An exception raised in a thread does not reach the main thread. By default it is printed on standard error and the main thread goes on and ends with return code 0, which the research saw; here threading.excepthook is replaced so that the program can print what the hook received, ValueError('boom'), and the main thread printed main continues. "
        "A thread therefore needs its own try and except, or a Future that carries the error, which the pool slides show.",
        "A Thread object starts once; its errors stay in its own thread.")

# ---- 8 join ---------------------------------------------------------------------------------------------------------------------
pn = "joinCut_v1_0_0.py"
dg, dcap = diagram("StartingAndJoiningAThread", "activity", (0.5, 1.4, 3.7, 3.05),
                   grid={"make": (0, 0), "call": (0, 1), "go": (0, 2), "chk": (0, 3), "err": (0, 4), "join": (1, 3)},
                   cols=[(0.05, 1.55), (2.1, 1.55)], rows_n=5, starts=(1, 0), ends={"type": "dot", "col": 1, "row": 4},
                   routes={("start", "make"): "h", ("chk", "join"): "h", ("err", "end"): "h"}, fs=8, nh=0.4, dh=0.52)
p8, bot8, a8, b8, x8, w8 = pfit(pn, 4.4, 1.55, 5.1, 2.5, right=True)
content("join(): waiting for a thread", "join() waits; join(0.1) only asks, and a thread never started cannot be joined",
        [dg, dcap, p8,
         *stack(["join(timeout) always returns None: only is_alive() tells whether the thread has finished.",
                 "join() on a Thread that was never started raises RuntimeError, the error the chapter's printed downloader meets."],
                x8, round(bot8 + 0.1, 2), w8, fs=9, gap=0.07)],
        "The flow chart is the chapter's rule in a picture: create a Thread with a target, call start(), let the main thread go on, and call join() to wait for the thread; if start() was never called before join(), join() raises RuntimeError instead. "
        "The program shows three behaviours. join(0.1) on a thread that sleeps 0.6 s returns after about 0.1 s with the value None and the thread still alive, so the caller must test is_alive() to know whether the thread finished; a join() with no timeout waits for the end, after which the thread is no longer alive; and join() on a thread that was never started raises RuntimeError: cannot join thread before it is started. "
        "The last message is the one the chapter's printed downloader produces, which the next slide shows. A join with a timeout turns the wait into a poll, which the chapter does not mention.",
        "join() waits; with a timeout it only asks, and is_alive() answers.")

# ---- 9 daemon threads --------------------------------------------------------------------------------------------------------------
pn = "daemonCut_v1_0_0.py"
p9, bot9, a9, b9, x9, w9 = pfit(pn, 0.5, 1.55, 5.2, 3.0)
xr = round(x9 + w9 + 0.2, 2)
content("Daemon threads", "A daemon thread does not keep the program alive; the flag is fixed at start()",
        [p9,
         *stack(["With daemon=True the late line was never printed, because the program ended first; with daemon=False it was printed.",
                 "Setting the flag after start() raised RuntimeError: the flag is fixed when the thread starts.",
                 rec("a thread inherited the daemon flag of the thread that created it (True), and an exception in a thread went to standard error while the main thread ended with return code 0.")],
                xr, 1.5, round(9.5 - xr, 2), fs=9, gap=0.08)],
        "A daemon thread is one the program does not wait for. The program runs the same small script twice in a new Python, once with daemon=True and once with daemon=False, and prints what each run printed: the daemon thread's late line never appeared, because the program ended when the main thread did, while the non-daemon thread kept the program alive until it printed. "
        "The threading documentation says that daemon threads are stopped abruptly at shutdown, so a daemon thread must not hold a file or a lock that needs a clean close. "
        "The last lines show that the flag is fixed when the thread starts: setting t.daemon after start() raised RuntimeError: cannot set daemon status of active thread. "
        "The card holds two findings of the research that this deck does not run again: a thread created by a daemon thread inherited the flag, and an exception in a thread went to standard error while the main thread ended with return code 0.",
        "A daemon thread dies with the program; set the flag before start().", recorded=True)

# ---- 10 the downloader as printed -----------------------------------------------------------------------------------------------------
pn = "printedCut_v1_0_0.py"
a10, b10 = span(pn, "downloadThreads = []")[0], span(pn, "print('Done.')")[0]
p10, bot10, a10, b10, x10, w10 = pfit(pn, 0.5, 1.55, 5.3, 3.4, a=a10, b=b10)
xr = round(x10 + w10 + 0.2, 2)
content("The downloader as printed", "The listing never calls start(): no request is made and join() raises",
        [p10,
         *stack([SAY_SI + " " + hid(pn, a10, b10, "imports, the server and the folder", "the run and the report"),
                 "The loop of the chapter's Step 2 appends 14 Thread objects and nothing starts them; the prose says the loop calls start().",
                 "Step 3 then calls join() on a thread that was never started, and the program ends with return code 1."],
                xr, 1.5, round(9.5 - xr, 2), fs=8.5, gap=0.07)],
        "This is the chapter's multithreaded XKCD downloader, Step 2 and Step 3, run exactly as it is printed. The research ran the program against a local stand-in, an HTTP server on 127.0.0.1 that answers a page for every comic number with one image, so xkcd.com was never contacted. "
        "The program of this slide starts that server, writes the printed listing into a Python of its own, runs it in an empty folder and reports what the server saw: no comic page was requested, no file was saved, and the run ended with return code 1 and RuntimeError: cannot join thread before it is started. "
        "The loop of the printed listing creates a Thread for each block of comic numbers and appends it to a list, but nothing calls start(), and the prose of the chapter says that the loop does. The join loop that follows then meets a thread that was never started. "
        "The lines before the listing, the server and the folder, are not shown, nor are the lines that run it and report the result, because they are the machinery of the experiment and not the chapter's code. "
        "The fix is one line, and the next slide shows what it uncovers.",
        "The listing as printed never starts a thread; join() raises.")

# ---- 11 the fixed downloader skips every tenth comic ------------------------------------------------------------------------------------------
pn = "fixedCut_v1_0_0.py"
a11, b11 = span(pn, "downloadThreads = []")[0], span(pn, "print('Done.')")[0]
p11, bot11, a11, b11, x11, w11 = pfit(pn, 0.5, 1.55, 5.3, 3.4, a=a11, b=b11)
xr = round(x11 + w11 + 0.15, 2)
im11, ib11, ir11 = img("skipped.png", xr, 1.5, 1.45, 2.05)
content("The downloader skips every tenth comic", "With start() added it asks for 125 of 139 numbers; 9, 19, 29 on are never asked for",
        [p11, im11, imgcap1("skipped.png", xr, round(ib11 + 0.03, 2), round(9.5 - xr, 2), fs=8),
         *stack([SAY_SI + " " + hid(pn, a11, b11, "imports, the server and the picture writer", "the run and the report"),
                 "Each thread runs range(start, end), and end is the last number of its block, so that number is skipped.",
                 ne("the real xkcd.com, which no program here contacted.")],
                round(ir11 + 0.12, 2), 1.5, round(9.5 - ir11 - 0.12, 2), fs=8, gap=0.06)],
        "With the missing line added under the append, every thread starts and the program finishes, but the stand-in server saw 125 comic pages requested and 125 files saved, and 14 numbers never requested: 9, 19, 29 and so on up to 139. "
        "The cause is in the loop: each thread runs range(start, end) where end is the last number of its block, i + 9, and range stops one short, so every block of ten loses its last number. The first thread covers 1 to 8, because its start is moved from 0 to 1, and the other thirteen cover nine numbers each, which is 8 plus 13 times 9, 125. "
        "The picture is drawn by the program from the list of numbers the server saw: each row is one thread's block of ten numbers, teal marks a number that was requested, orange one that was not, and the grey cell at the top left is the number 0, which is not a comic. The orange column is the finding of the research that the printed listing skips every tenth comic. "
        "The program counts no clock and prints no duration. The research measured the speed of the repaired downloader against one thread doing the same 250 requests and found it at least 5 times faster when each request waits 0.05 s, which is the waiting that threads overlap and which the later slides record as numbers. "
        "The real xkcd.com was never contacted, which is why the card says NOT EXECUTED.",
        "Range stops one short: every tenth comic is never requested.", notexec=True)

# ---- 12 lost updates (Therac) ---------------------------------------------------------------------------------------------------------------------
pn = "lostCut_v1_0_0.py"
p12, bot12, a12, b12, x12, w12 = pfit(pn, 0.5, 1.55, 4.5, 2.35)
ph12, pb12, pr12 = photo("therac.png", 5.2, 1.48, 1.05, 1.4)
c12, cb12 = con("inc", 5.2, 3.0, 4.3, fs=8, cap=False, label=None)
content("Lost updates", "Two threads read 0 and both write 1; a counter += 1 is five steps, not one",
        [p12, ph12, photocap("therac.png", round(pr12 + 0.12, 2), 1.48, round(9.5 - pr12 - 0.12, 2), fs=7.5, extra="A Therac-25 machine as it stood in use."),
         c12,
         foot("In all 3 runs the counter ended at 1 without a lock and at 2 with one, because both threads read 0 before either wrote.", 0.5, round(bot12 + 0.08, 2), 4.5, fs=9),
         factrow("Therac1985", y=4.58)],
        story_notes("Therac1985") + " The program forces the race: each thread reads the counter, waits 0.05 s and writes back the value plus one, so both read 0 before either writes and the counter ends at 1 in all 3 runs; with a lock around the read and the write it ends at 2. "
        "The console shows why a race needs no pause to exist: counter += 1 in a function compiled to 5 steps on Python 3.14.6, a load of the global, a load of the small integer 1, the addition, the store of the global and, as the fifth, the load of None that the function returns, so a thread can be stopped between the read and the write. "
        "On the standard build the interpreter considers switching threads every 0.005 s by default, which is why such a race is rare there and why the research forced it with a pause. The photograph is a Therac-25 as it stood in use, a public domain file of Wikimedia Commons whose author is unknown.",
        "Two threads, one counter, no lock: an update disappears.")

# ---- 13 locks ---------------------------------------------------------------------------------------------------------------------------------------
pn = "lockCut_v1_0_0.py"
dg, dcap = diagram("TwoThreadsAndALock", "sequence", (5.1, 1.4, 4.4, 2.55), fs=8, head_w=0.95, gap0=0.1)
p13, bot13, a13, b13, x13, w13 = pfit(pn, 0.5, 1.55, 4.5, 3.4)
content("Locks", "A lock makes the read and the write one step; the with statement always releases it",
        [p13, dg,
         capfoot(dcap, "A plain Lock cannot be taken twice by the same thread; an RLock can.", 5.1, round(1.4 + 2.55 + 0.03, 2), 4.4, fs=8),
         *stack(["Four threads with a lock reached the exact 400000; the lock was free again after an error in the with block."],
                5.1, 4.55, 4.4, fs=9, gap=0.05)],
        "The sequence diagram is the lock protecting the counter: thread A acquires the lock, reads, adds one and writes the counter, thread B waits for the lock, A releases it, and the lock lets B read the value. "
        "The program shows four threads that each add 1 to a shared counter 100,000 times inside a with-lock block and end at exactly 400000, the total that a loop without a lock cannot promise. "
        "The with statement releases the lock even when the block raises, which the second line shows: after a ValueError inside the block the lock was free again. "
        "The last two lines show the difference between a plain Lock and an RLock: a thread that already holds a Lock and asks for it again with a 0.2 s timeout gets False, and without the timeout it would wait forever, while the same request on an RLock gets True. A function that takes a lock and calls another that takes the same lock needs an RLock or a redesign.",
        "A lock makes read and write one step for every thread that uses it.")

# ---- 14 deadlock and events ------------------------------------------------------------------------------------------------------------------------------
pn = "deadCut_v1_0_0.py"
p14, bot14, a14, b14, x14, w14 = pfit(pn, 0.5, 1.55, 4.4, 3.4)
xr = round(x14 + w14 + 0.25, 2)
content("Deadlock and events", "Two locks taken in opposite orders leave both threads waiting; an Event says go",
        [p14,
         *stack(["Each thread took one lock, paused 0.1 s and asked for the other: after join(0.5) both were still alive, a deadlock.",
                 "The usual remedy is one agreed order for taking locks.",
                 "A thread waiting on an Event stayed blocked until set() was called and then went on: the list was empty before and held 'woke' after."],
                xr, 1.5, round(9.5 - xr, 2), fs=10, gap=0.12)],
        "The two daemon threads of the program take the same two locks in opposite orders with a pause between the two acquisitions, so each holds one lock and waits for the other. "
        "After join(0.5) on both, both were still alive, which is the deadlock that Wikipedia describes as each member of a group waiting for another to release a resource, and the dining philosophers problem is its classic example. The threads are daemons so that the program can end, and a real program in this state would hang. The usual remedy is one global order for taking locks. "
        "The second half of the program is the simplest way for one thread to tell another that it may go on. An Event is a flag: the worker waits on it, the list of results is empty before set() is called, and it holds the worker's word right after, with nothing timed. "
        "A thread waiting without a timeout blocks until the flag is set, which is why the Event is the tool for wait until another thread says go.",
        "Locks taken in opposite orders deadlock; an Event says go.")

# ---- 15 semaphores (Dijkstra) ----------------------------------------------------------------------------------------------------------------------------------
pn = "semCut_v1_0_0.py"
p15, bot15, a15, b15, x15, w15 = pfit(pn, 0.5, 1.55, 4.6, 2.9)
ph15, pb15, pr15 = photo("dijkstra.jpg", 5.5, 1.48, 1.2, 1.6)
content("Semaphores", "A Semaphore of 2 let at most 2 of 6 threads into the block at once",
        [p15, ph15, photocap("dijkstra.jpg", round(pr15 + 0.12, 2), 1.48, round(9.5 - pr15 - 0.12, 2), fs=7.5, extra="Edsger Dijkstra."),
         *stack(["Six threads each held the block for 0.1 s: at most 2 were inside with Semaphore(2), and all 6 with Semaphore(6).",
                 "A semaphore limits how many threads work at once, for example how many connections a downloader opens."],
                5.5, round(pb15 + 0.1, 2), 4.0, fs=9, gap=0.06),
         factrow("Semaphore1962", y=4.58)],
        story_notes("Semaphore1962") + " The program counts how many of six threads are inside a guarded block at the same moment, and prints the largest number it saw: with a BoundedSemaphore of 2 it was 2, and with one of 6, which lets all of them in, it was 6. "
        "The counter that records the number inside is itself protected by a lock, because the demonstration must not suffer the race the previous slides show. "
        "A semaphore is a counter that lets a fixed number of threads pass at once, and a lock is the semaphore of 1. The research measured the same thing against no semaphore at all and found 6 inside. "
        "The photograph is a portrait of Edsger Dijkstra by Hamilton Richards, licensed CC BY-SA 3.0 on Wikimedia Commons and reduced for this slide.",
        "A semaphore limits how many threads work at once.")

# ---- 16 queues and local data ------------------------------------------------------------------------------------------------------------------------------------
pn = "queueCut_v1_0_0.py"
dg, dcap = diagram("TheProducerAndTheConsumer", "sequence", (0.5, 1.4, 4.5, 2.7), fs=8, head_w=1.1, gap0=0.1)
p16, bot16, a16, b16, x16, w16 = pfit(pn, 5.2, 1.55, 4.3, 1.9)
c16, cb16 = con("locals", 5.2, round(bot16 + 0.1, 2), 4.3, fs=8, cap=False)
content("Queues and thread-local data", "A queue hands items over in order; a threading.local value stays in its thread",
        [dg, dcap, p16, c16,
         foot("The consumer received [0, 1, 2, 3, 4] in order and stopped at the marker None: items are handed over, not shared.", 0.5, 4.55, 4.5, fs=9)],
        "The sequence diagram is the producer-consumer pattern: the producer puts the numbers into the queue and then the marker None, the consumer takes the items in order, the queue hands over each item, and the consumer calls task_done() for each. "
        "The program's producer is the main thread and the consumer a thread of its own: the consumer received [0, 1, 2, 3, 4], in order, and stopped at the marker; the queue does its own locking, so no lock is written, and join() returns after 6 task_done() calls, 5 items and the marker. "
        "The queue removes the shared variable that the chapter warns about, because items are handed over and not shared. The chapter's own advice is to use only local variables in the target function. "
        "The console shows the other half of that advice: a value set on a threading.local() in one thread is absent in the main thread. The research also ran four threads that each summed their own list into a local variable and got the four expected totals, 0, 45, 190 and 435.",
        "A queue hands items over, so nothing is shared.")

# ---- 17 pools -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
pa, pb_ = "poolCut_v1_0_0.py", "poolerrCut_v1_0_0.py"
p17a, bot17a, _, _, x17a, w17a = pfit(pa, 0.5, 1.55, 4.4, 3.1)
p17b, bot17b, _, _, x17b, w17b = pfit(pb_, 5.0, 1.55, 4.5, 3.25, right=True)
content("Pools: results, errors, cancelling", "map keeps the order of the inputs; a Future carries its error to result()",
        [p17a, p17b,
         *stack(["map kept the input order; as_completed yielded [2, 1, 0]."],
                0.5, round(bot17a + 0.04, 2), 4.4, fs=8, gap=0.05),
         *stack(["cancel_futures=True cancelled 4 of 5 queued tasks."],
                5.0, round(bot17b + 0.04, 2), 4.5, fs=8, gap=0.05)],
        "A pool starts a fixed number of worker threads and runs submitted functions on them, returning Future objects. The left program runs three tasks that finish in the reverse order of their inputs: map returned [0, 1, 2], the order of the inputs, while as_completed yielded the results as they finished, [2, 1, 0]. "
        "A pool created with thread_name_prefix='dl' named its workers dl_0 and dl_1, which makes a log readable, and a pool created without max_workers had 6 workers on this machine of 2 CPUs; the documented rule since Python 3.13 is the smaller of 32 and the number of CPUs plus 4, and the program reads the private attribute _max_workers to print it. "
        "The right program shows how errors and waiting are carried by the Future: an exception raised in a task stays in its Future until result() is called, result(timeout=0.1) raised TimeoutError while the task was still not done, and shutdown(cancel_futures=True) cancelled the 4 queued tasks that had not started and let the one running finish, since a task that started cannot be cancelled. "
        "The with block of an executor waits for every task before it ends, which the research also confirmed.",
        "map keeps input order; a Future carries its error to result().")

# ---- 18 the GIL on and off (PEP 703) -------------------------------------------------------------------------------------------------------------------------
pn = "gilCut_v1_0_0.py"
p18, bot18, a18, b18, x18, w18 = pfit(pn, 0.5, 1.55, 4.8, 3.0, a=3)
ph18, pb18, pr18 = photo("threads.png", round(x18 + w18 + 0.2, 2), 1.48, 1.3, 1.25)
xr = round(x18 + w18 + 0.2, 2)
content("The GIL on, and off", "The standard build has the lock; the free-threaded build can switch it off",
        [p18, ph18, photocap("threads.png", round(pr18 + 0.1, 2), 1.48, round(9.5 - pr18 - 0.1, 2), fs=7.5, extra="A process with two threads."),
         *stack([hid(pn, a18, b18, "imports and the path of the free-threaded interpreter"),
                 rec("the free-threading guide says a package with an extension module that does not declare support re-enables the lock."),
                 ne("the free-threaded build of Python 3.13, and a C extension that re-enables the lock: the second is only what the documentation says.")],
                xr, round(pb18 + 0.08, 2), round(9.5 - xr, 2), fs=8.5, gap=0.06),
         factrow("Gil2023", y=4.58)],
        story_notes("Gil2023") + " The program asks the standard build and the free-threaded build the same question, sys._is_gil_enabled() and the build variable Py_GIL_DISABLED. The standard Python 3.14.6 answered True and 0, the free-threaded 3.14.6 installed with uv answered False and 1, and the environment variable PYTHON_GIL=1 and the option -X gil=1 both turned the lock on again, so one build can be run either way. "
        "The free-threaded build of Python 3.13, the first and experimental one, was not installed and was not run, and the study states its behaviour only from the documentation; the 3.13 build with the lock answered True. A C extension that does not declare support for free-threading makes the free-threaded build switch the lock back on, according to the free-threading guide; no such extension was built, so that behaviour is only read, and the card says both. "
        "The picture is a multithreaded process by Cburnett, licensed CC BY-SA 3.0 on Wikimedia Commons: two threads inside one process, sharing it.",
        "The lock is on by default; the free-threaded build turns it off.", notexec=True, recorded=True)

# ---- 19 the race on and off the GIL (blackout) ---------------------------------------------------------------------------------------------------------------------
tr19 = EX["_tables"]["raceRecord"]["rows"]
tbl19 = {"t": "table", "x": 0.5, "y": 1.45, "w": 5.0, "colW": [1.7, 1.1, 1.1, 1.1], "fs": 9, "rowH": 0.3, "rows": tr19}
ph19, pb19, pr19 = photo("blackout.png", 6.2, 1.48, 1.3, 1.5)
content("The race with and without the lock", "Updates lost out of 4,000,000, three runs per build; none was lost with the GIL",
        [tbl19, ph19, photocap("blackout.png", round(pr19 + 0.1, 2), 1.48, round(9.5 - pr19 - 0.1, 2), fs=7.5, extra="The region of the 2003 blackout in red."),
         *stack([rec("four threads each ran counter += 1 one million times; the table counts the updates lost in each of 3 runs, one run each on 2 CPUs, a load average of 0.75."),
                 "None was lost in 12 runs on the four builds with the lock; 2,500,522 to 2,913,206 were lost in 3 runs on the free-threaded build.",
                 "A run without a loss proves nothing: the lock only makes the race rare."],
                0.5, 3.3, 5.4, fs=8.5, gap=0.05),
         factrow("Blackout2003", y=4.58)],
        story_notes("Blackout2003") + " The table is the research's record of a race that needs no pause. Four threads each ran counter += 1 one million times, so 4,000,000 was the expected total, and the table gives the updates lost in each of 3 runs: none on Python 3.14.6 with the lock, 3.13.14, 3.12.13 and 3.11.15, and 2,844,845, 2,500,522 and 2,913,206 on the free-threaded 3.14.6. "
        "The deck check computes every cell again from the record, and every figure is a single run on the machine of 2 CPUs on 14 October 2026, with the load average at 0.75. The lesson is the one of the story: a race that never shows can still be there, and a program that passes its tests on the builds with the lock can lose updates on the free-threaded build. "
        "The program is not run again on this slide, because a race of this kind depends on timing and the machine had another job running beside the deck. The map is the region of the 2003 blackout by Lokal_Profil, licensed CC BY-SA 2.5 on Wikimedia Commons.",
        "No lost update in a run proves nothing; lock anyway.", recorded=True)

# ---- 20 CPU-bound work -----------------------------------------------------------------------------------------------------------------------------------------------------------
ch20 = EX["_charts"]["cpuRatio"]
chart20 = {"t": "chart", "ctype": "bar", "x": 0.5, "y": 1.4, "w": 4.4, "h": 2.7, "labels": ch20["labels"], "title": "4 threads as a multiple of the serial time",
           "series": [{"name": "ratio", "data": ch20["values"]}], "dataLabels": True, "dlFs": 9}
tbl20 = {"t": "table", "x": 5.1, "y": 1.45, "w": 4.4, "colW": [1.6, 0.9, 0.95, 0.95], "fs": 8.5, "rowH": 0.3, "rows": EX["_tables"]["cpuRecord"]["rows"]}
content("CPU-bound work on threads", "Only the free-threaded build was faster on 4 threads; below 1 means faster than serial",
        [chart20, tbl20,
         *stack([rec("four CPU-bound tasks, one after another and on 2 and 4 threads, in seconds; one run each, 2 CPUs, a load average below 1.0 when it started."),
                 "On the standard 3.14.6 and on 3.13, 3.12 and 3.11 the 4 threads took at least 0.8 of the serial time, 0.94 to 1.19; the free-threaded 3.14.6 took 0.40.",
                 "The free-threaded serial run (1.292 s) was slower than the standard one (0.89 s): the single-thread cost of the build."],
                5.1, 3.35, 4.4, fs=8.5, gap=0.06),
         *stack([ne("more than 2 CPUs and a run under load; the speed-up of the free-threaded build was measured on 2 CPUs only.")], 0.5, 4.2, 4.4, fs=8.5)],
        "The chart divides the time of 4 threads by the time of the same 4 tasks run one after another, for each interpreter of the research, and the table beside it gives the seconds. On the standard Python 3.14.6 the serial run took 0.89 s and 4 threads took 1.003 s, a ratio of 1.13, because the global interpreter lock lets one thread run Python code at a time and the threads only add the cost of switching; "
        "on 3.13.14, 3.12.13 and 3.11.15 the 4 threads took at least 0.8 of the serial time, a ratio from 0.94 to 1.19, the same picture. On the free-threaded 3.14.6 the serial run took 1.292 s and 2 threads 0.553 s and 4 threads 0.522 s, a ratio of 0.40, so the work ran in parallel on the 2 CPUs. "
        "The free-threaded serial run was slower than the standard one, 1.292 s against 0.89 s, which is the single-thread cost of the build. Every figure is one run taken after the research waited for the one-minute load average to fall below 1.0, and the deck does not time the loop again. "
        "More than 2 CPUs and a run under load were not executed, so the slide makes no claim about how the speed-up grows with more cores.",
        "Only the free-threaded build sped up four CPU-bound tasks on 2 CPUs.", notexec=True, recorded=True)

# ---- 21 processes and waiting ------------------------------------------------------------------------------------------------------------------------------------------------------
pn = "procCut_v1_0_0.py"
p21, bot21, a21, b21, x21, w21 = pfit(pn, 0.5, 1.55, 4.6, 3.4, a=3)
xr = round(x21 + w21 + 0.2, 2)
ch21 = EX["_charts"]["waitingRecord"]
chart21 = {"t": "chart", "ctype": "bar", "x": xr, "y": 1.35, "w": round(9.5 - xr, 2), "h": 1.5, "labels": ch21["labels"], "title": "8 sleeps of 0.5 s, seconds",
           "series": [{"name": "seconds", "data": ch21["values"]}], "dataLabels": True, "dlFs": 9}
tbl21 = {"t": "table", "x": xr, "y": 2.95, "w": round(9.5 - xr, 2), "colW": [1.9, 1.0, round(9.5 - xr - 2.9, 2)], "fs": 8, "rowH": 0.26, "cellMargin": [0.02, 0.04, 0.02, 0.04],
         "rows": EX["_tables"]["processRecord"]["rows"]}
content("Waiting, processes and starting cost", "Threads overlap waiting; a process does not share variables and costs more to start",
        [p21, chart21, tbl21,
         foot(hid(pn, a21, b21, "imports and the main guard") + " " + rec("single runs of 2026-10-14 on 2 CPUs; the chart is the standard 3.14.6, whose waiting threads, pool and asyncio all took about 0.5 s."), xr, 4.33, round(9.5 - xr, 2), fs=8)],
        "The program shows what a process does not share. A child process that updated its copy of a dictionary left the parent's dictionary at {'n': 0}, while a thread that updated the same dictionary changed it to {'n': 99}; the research saw the same with a module variable. The default start method of multiprocessing on Linux was forkserver on Python 3.14.6, which the documentation says replaced fork in 3.14, "
        "and subprocess.Popen came back at once, before the child that slept a second had ended, with poll() still None, and wait() then returned the return code 0. "
        "The chart and the table are the research's record and are not measured again. Eight sleeps of 0.5 s took 4.001 s one after another and 0.502 s on 8 threads, 0.502 s in a pool and 0.503 s with asyncio on the standard build, and 0.503 s on 8 threads on the free-threaded build, so waiting overlaps on either build. "
        "Four CPU-bound tasks took 0.963 s one after another and 0.667 s on a pool of 2 processes, and starting a thread cost 112 microseconds against 5.4 milliseconds for a process on the standard build, and 382 microseconds against 8.6 milliseconds on the free-threaded build. "
        "A process therefore escapes the lock, at the price of memory that is not shared and a start that costs about 50 times more.",
        "Waiting overlaps in threads; a process costs far more to start.", recorded=True)

# ---- 22 asyncio and the choice -------------------------------------------------------------------------------------------------------------------------------------------------------
pn = "asyncCut_v1_0_0.py"
dg, dcap = diagram("ChoosingBetweenTheTools", "activity", (5.1, 1.4, 4.4, 2.85),
                   grid={"kind": (0, 1), "wait": (2, 1), "build": (0, 2), "proc": (1, 2), "thr": (0, 3)},
                   cols=[(0.0, 1.45), (1.8, 1.3), (3.2, 1.2)], rows_n=4, starts=(0, 0), ends={"type": "dot", "col": 2, "row": 3},
                   routes={}, fs=8, nh=0.56, dh=0.6)
p22, bot22, a22, b22, x22, w22 = pfit(pn, 0.5, 1.55, 4.55, 3.3)
content("asyncio, and choosing a tool", "asyncio overlaps waiting on one thread; a blocking call stalls every task on it",
        [p22, dg, dcap,
         foot("A blocking time.sleep in a coroutine stops the whole loop; asyncio.to_thread runs it in a worker.", 5.1, 4.62, 4.4, fs=8)],
        "asyncio overlaps waiting on one thread by switching at every await. The program shows three things with times that are printed only as booleans: ten coroutines that each awaited asyncio.sleep(0.3) finished together in under 0.6 s on one thread; five coroutines that each called the blocking time.sleep(0.2) took at least 1 s, because one blocking call stops every other task on the loop; "
        "and asyncio.to_thread ran five such blocking calls in worker threads in under 0.6 s, with workers whose names begin asyncio while the loop itself stayed in MainThread. "
        "The flow chart is the choice that the whole chapter prepares: if the work waits, threads, a pool or asyncio overlap the waiting, and the timer could not tell them apart; if it computes, the free-threaded build runs threads in parallel and otherwise a pool of processes computes in parallel. "
        "The chart of the earlier slides recorded the times behind that choice, and the research also read the Rust and Go documents that frame the same choice in other languages.",
        "asyncio overlaps waiting on one thread; a blocking call stalls it.")
# ---- 23 five interpreters and what did not run ---------------------------------------------------------------------------------------------------------------------
tbl23 = {"t": "table", "x": 0.5, "y": 1.45, "w": 9.0, "colW": [1.8, 1.3, 1.3, 1.3, 1.3, 2.0], "fs": 8, "rowH": 0.26, "rows": EX["_tables"]["environments"]["rows"]}
content("Five interpreters, and what did not run", "Recorded: one probe under five interpreters; below it, what was not run",
        [tbl23,
         card("Recorded 14 Oct 2026", "The research package holds %d sources, %d findings, 64 executed leaves, %d stories and %d diagrams. Every figure of a timing is one run on 2 CPUs; the probe above ran the same program under five interpreters." % (len(RD.PUBS), len(RD.FINDINGS), len(ST.STORIES), len(DIAG)),
              0.5, 3.7, 4.4, 1.25, fs=8.5, accent="slate"),
         card("NOT EXECUTED here", "The free-threaded build of Python 3.13, a C extension that re-enables the lock, Windows and macOS, more than 2 CPUs, runs under load and the real xkcd.com (a local stand-in server was used).",
              5.1, 3.7, 4.4, 1.25, fs=8.5, accent="orange")],
        "The table is the same probe run under five interpreters of the research, and the deck check runs it again and compares every cell. The GIL answer is True on 3.13.14 and 3.14.6 and False on the free-threaded 3.14.6, and the older 3.11.15 and 3.12.13 have no sys._is_gil_enabled() at all. "
        "Py_GIL_DISABLED is 1 only on the free-threaded build. The thread name is Thread-1 (f) on all five, a pool's map returns [1, 2] on all five, InterpreterPool exists from 3.14, and the default start method of multiprocessing is fork up to 3.13.14 and forkserver from 3.14. "
        "The card on the left counts the research: %d sources, %d findings, 64 executed leaves, %d stories and %d diagrams. The card on the right lists what was not run. "
        "The free-threaded build of Python 3.13 was not installed, only the free-threaded 3.14.6 was, so what the study says of 3.13 comes from the documentation. A C extension that re-enables the lock was not built, Windows and macOS were not available, the machine has 2 CPUs, no run was made under load, and the real xkcd.com was never contacted: a local stand-in server answered the downloader. "
        "Every timing of the deck is one run and not a benchmark." % (len(RD.PUBS), len(RD.FINDINGS), len(ST.STORIES), len(DIAG)),
        "Five interpreters agree on most rows; the rest was not run.", notexec=True, recorded=True)

# ---- 24 summary: the mind map ----------------------------------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("ThreadsAtAGlance", "mindmap", (0.5, 1.4, 9.0, 3.2), fs=9, root_w=2.0)
content("The chapter in one map", "Seven branches; the slides of each branch hold the examples",
        [dg, dcap],
        "These seven branches are the route of the deck. Thread basics: start() runs the target in a new thread, args and kwargs pass the arguments, and the printed listing of the downloader never starts its threads. "
        "Join and daemon: join() waits for a thread, a daemon thread dies with the program, and the downloader with start() added skips every tenth comic. Shared data and locks: a lost update happens without a lock, a lock makes the update one step, and a queue hands items over. "
        "Executors and pools: map() keeps the order of the inputs, an exception waits in the Future until result() is called, and the default number of workers depends on the CPUs. GIL and free threading: the standard build keeps the lock on, waiting threads overlap on both builds, and the free-threaded build scaled with the cores in the one measurement on 2 CPUs. "
        "Threads versus other tools: a process does not share variables, asyncio overlaps waiting on one thread, and the default start method of multiprocessing is forkserver on Python 3.14.6. Environment and evidence: the study ran Python 3.14.6, every timing is a single run, and Windows and macOS were not executed. "
        "Together they answer the two questions of the chapter, what the threads of a program do and how much they cost, and the slides that say where the printed chapter differs from what ran answer the rest. The map is drawn from the same specification as the interactive page.",
        "If a branch feels unproven, its slides hold the example.")

# ---- 25 resources ------------------------------------------------------------------------------------------------------------------------------------------------------------------
PUB = {p[0]: p for p in RD.PUBS}
_read = [["The textbook, 2nd edition, chapter 17 - free online", PUB["P01"][2]],
         ["The 3rd edition: table of contents", PUB["P02"][2]],
         ["Appendix A: installing third-party modules", PUB["P04"][2]]]
_ref = [["threading (Python 3.14 documentation)", PUB["P07"][2]],
        ["concurrent.futures (Python 3.14 documentation)", PUB["P08"][2]],
        ["asyncio (Python 3.14 documentation)", PUB["P10"][2]],
        ["Python support for free threading (HOWTO)", PUB["P17"][2]],
        ["Python Free-Threading Guide", PUB["P36"][2]],
        ["Edsger W. Dijkstra (Wikipedia)", PUB["P52"][2]]]
_hist = [["Therac-25 (Wikipedia)", STORY["Therac1985"]["link"]],
         ["Semaphore (programming) (Wikipedia)", STORY["Semaphore1962"]["link"]],
         ["Northeast blackout of 2003 (Wikipedia)", STORY["Blackout2003"]["link"]],
         ["PEP 703: making the GIL optional", STORY["Gil2023"]["link"]]]
LINKS = [r[1] for r in _read + _ref + _hist]
json.dump({"_version": __version__, "links": LINKS}, open(os.path.join(HERE, "links_v1_0_0.json"), "w"), indent=1)
content("Where to go from here", "Every link was opened on the day this deck was made",
        [{"t": "links", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.55, "fs": 9, "groups": [
            {"head": "Stories", "rows": _hist}, {"head": "Read", "rows": _read}, {"head": "Reference", "rows": _ref}]}],
        "Every link on this slide was opened on the day the deck was made, and the build records the status each answered. The textbook chapter is free to read online and holds every listing of this deck; the 3rd edition no longer has the chapter, and Appendix A is where the book installs third-party modules. "
        "The reference links are the documentation of threading, concurrent.futures and asyncio, the Python HOWTO on free threading and the community guide to free-threading. "
        "The four stories of the chapter are on slides with their own link, and their pages are the first group together with Dijkstra's page. "
        "The research package holds %d sources in all. No photograph of a living person is used in the deck, and the four pictures of the stories are files of Wikimedia Commons with their credit under them." % len(RD.PUBS),
        "Textbook, documentation, and history, all opened today.")

# ---- 26 closing ------------------------------------------------------------------------------------------------------------------------------------------------------------------
content("What you should now be able to say", "Four claims, each carried by a result you saw printed",
        [{"t": "bullets", "x": 0.6, "y": 1.5, "w": 8.8, "h": 2.4, "fs": 15, "items": [
            "A thread runs only after start(), and join() waits for it; the printed downloader never calls start().",
            "A shared counter needs a lock; with the GIL a race is rare, not impossible.",
            "Threads overlap waiting; only the free-threaded build sped up CPU-bound work.",
            "Every timing here is one run on 2 CPUs; Windows and macOS did not run."]},
         {"t": "chips", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.6, "fs": 10, "big": False,
          "items": ["%d console rows" % ROWS_SHOWN, "%d programs run" % len(PROGS), "%d diagrams" % len(DIAG), "%d pictures" % (len(EX["_images"]) + len(PHOTOS))]}],
        "Four claims, each carried by a result you saw printed. If you can say them in your own words and run the examples yourself, you have the chapter. The programs of the deck need only Python and its standard library, and the downloader runs against an HTTP server of the program on 127.0.0.1. "
        "The rows were run again under Python %s each time the deck was built, and the programs, and with them the picture they save, were run again by the check that compares the slides with the recording. "
        "What was not run is marked on its slide: the free-threaded build of Python 3.13, a C extension that re-enables the lock, Windows and macOS, more than 2 CPUs, runs under load and the real xkcd.com. "
        "The timings are Recorded, single runs of 14 October 2026 on a machine of 2 CPUs, and not benchmarks. What this chapter taught about checking what a program really does, rather than what its listing says, carries over to the rest of the course." % PYV,
        "Questions are welcome; bring a thread to try.")

# ---- agenda ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
_t = {s["title"]: i + 1 for i, s in enumerate(S)}
_parts = [("Starting and joining threads", "What a program can do with threads", "Daemon threads"),
          ("The XKCD downloader", "The downloader as printed", "The downloader skips every tenth comic"),
          ("Shared data, locks and queues", "Lost updates", "Queues and thread-local data"),
          ("Pools, the GIL and the race", "Pools: results, errors, cancelling", "The race with and without the lock"),
          ("Speed, processes and asyncio", "CPU-bound work on threads", "Five interpreters, and what did not run"),
          ("Summary and resources", "The chapter in one map", "Where to go from here")]
_rows = ["%s (slides %d-%d)" % (name, _t[a], _t[b]) for name, a, b in _parts]
_ends = [_t[b] for _, _, b in _parts]
_starts = [_t[a] for _, a, _ in _parts]
if _starts[0] != 4 or any(_starts[i + 1] != _ends[i] + 1 for i in range(len(_parts) - 1)) or _ends[-1] != len(S) - 1:
    raise SystemExit("REFUSED: agenda ranges are not contiguous: %r %r (len S=%d)" % (_starts, _ends, len(S)))
_nstory = sum(1 for s in S for i in s["items"] if i.get("t") == "factrow")
_npic = sum(1 for s in S for i in s["items"] if i.get("t") == "img")
_nph = sum(1 for s in S for i in s["items"] if i.get("t") == "img" and "photos" in i["path"])
S[1]["items"] = [
    {"t": "numlist", "x": 0.5, "y": 1.4, "w": 6.3, "h": 3.55, "fs": 11.5, "items": _rows},
    {"t": "stat", "x": 7.05, "y": 1.5, "w": 2.45, "h": 3.4, "vert": True, "items": [
        {"n": str(len(S)), "label": "slides, numbered bottom-right"},
        {"n": "%d + %d" % (_nstory, len(ST.STORIES) - _nstory), "label": "true stories: %d on slides, %d in the notes" % (_nstory, len(ST.STORIES) - _nstory)},
        {"n": str(_npic), "label": "pictures: %d credited photos, %d saved by a program" % (_nph, _npic - _nph)}]}]
S[1]["sub"] = "Six parts; every range is a run of slides you can jump to"
S[1]["take"] = "Six parts, from starting a thread to a map."
S[1]["notes"] = ("The route has six parts. It starts with starting and joining threads: the seven uses of threads, starting a thread, the arguments of the target, the life of a Thread object, join and daemon threads. "
                 "Then the XKCD downloader: the listing as printed, which never calls start(), and the listing with the line added, which skips every tenth comic. The third part is shared data, locks and queues: the lost update, locks, deadlock and events, semaphores, queues and thread-local data. "
                 "The fourth is pools, the GIL and the race: results, errors and cancelling in an executor, the lock on and off, and the race with and without it. "
                 "The fifth is speed, processes and asyncio: CPU-bound work on threads, waiting and starting a process, asyncio and the choice of a tool, and five interpreters with what did not run. "
                 "The last part is a one-map summary and the resources. The ranges name the exact slides, so you can return to the part you need. All four stories are on slides, each with a link; the seven narrative diagrams of the chapter are drawn from the same specifications as the interactive page. "
                 "Every output was printed by Python %s, the downloader ran against a local stand-in server, and what could not be run is marked on its slide." % PYV)

for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])
    for i in s["items"]:
        if i.get("t") == "bullets" and len(i["items"]) > 5:
            raise SystemExit("REFUSED: too many bullets on %r" % s["title"])
if len(S) != 26:
    raise SystemExit("REFUSED: %d slides, the plan is 26" % len(S))
if set(SHOWN) != set(DIAG):
    raise SystemExit("REFUSED: diagrams not on a slide: %r" % (set(DIAG) - set(SHOWN)))
_pics = sorted(i["path"].split("/")[-1] for s in S for i in s["items"] if i.get("t") == "img")
if _pics != sorted(list(EX["_images"]) + list(PHOTOS)):
    raise SystemExit("REFUSED: pictures on slides %r differ from the recording and the photographs" % (_pics,))
plan = {"meta": {"title": "Ch. 25: Threads", "sub": "SEN0414, second-edition chapter 17 material",
                 "version": __version__, "python": PYV, "total": len(S), "diagrams": SHOWN, "notExecuted": NOTEXEC, "recorded": RECORDED,
                 "standin": {str(k): v for k, v in STANDIN.items()}}, "slides": S}
if LATE:
    raise SystemExit("REFUSED:\n" + "\n".join(LATE))
out = os.path.join(HERE, "deck_plan_v1_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides; diagrams on slides", dict(sorted(SHOWN.items(), key=lambda kv: kv[1])), "; NOT EXECUTED on slides", NOTEXEC, "; Recorded on slides", RECORDED)

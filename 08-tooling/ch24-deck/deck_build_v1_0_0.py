#!/usr/bin/env python3
"""Builds deck_plan_v1_0_0.json - SEN0414 chapter 24 (Text-to-Speech and Speech Recognition Engines) on the CME classroom standard.

Same regime as chapters 10 to 23: numbered warm-ivory slides, an agenda with exact slide ranges, a summary before the resources, full-sentence takeaway
strips, stories with fact rows, consoles and programs (whole or honest excerpts, labelled with their line numbers) with their results as Python printed
them. Every console result and program transcript comes from examples_out_v1_0_0.json (made by examples_run_v1_0_0.py under Python 3.14.6 with pyttsx3 2.99,
openai-whisper 20250625, yt-dlp 2026.8.19, torch 2.14.1+cpu and NumPy 2.5.4, eSpeak NG 1.51 and ffmpeg 6.1.1); the speaker notes are prose for the reader and carry only what
the chapter's RDODI research package (03-materials/ch24/rdodi, sen0414_ch24_rdodi_data_v1_0_2.py, findings F1 to F27), its records (08-tooling/ch24-page/*.json) or a program of this
deck established.

What this chapter adds against chapter 23: NOTHING IS HEARD. The machine has no sound card, no microphone and no GPU, so pyttsx3 writes WAV files and no program plays a sound; every
slide that shows such a program says 'No sound card' and 'local stand-in' (honesty_check_v1_0_0.py requires the words). The programs that need real audio read public-domain LibriVox
readings from archive.org, which STANDS IN FOR YouTube (nothing is downloaded from YouTube; the slide says so). Seventeen programs written for the deck (the Cuts) were run, each twice, and the
runner refuses a program whose transcript or picture differs between the two runs. The 15 programs of the research corpus were run by the research on 14 October 2026 and are recorded in
ch24-page/corpus_run_v1_0_0.json; this deck does not run them again and marks what it takes from them Recorded. Five pictures that programs saved are placed on the slides as images; each caption
names the program ('image <file> made by <program>') and program_check_v1_0_0.py runs that program again and requires the slide to carry a picture byte-identical (or pixel-identical) to what the
program saves now. What could not be run is marked NOT EXECUTED on its slide (meta.notExecuted): SAPI5 and NSSpeechSynthesizer, a microphone, a GPU, the cloud services, a YouTube download,
and Whisper medium, turbo and large-v3 (the first two were killed at about 6 GB of memory, the third does not load: findings, not successes). The seven narrative diagrams of the chapter
(sen0414_ch24_diagrams_v1_0_0.py, grounding 0.84 or more) are drawn as native shapes (diagram_shapes_v1_0_0.py) and checked by diagram_check_v1_0_0.py; four tables (the same probe in four
environments at check time, the releases, Table 24-1 against this machine, and the replay of the chapter) and two charts are native PowerPoint objects whose data the deck check computes again.
Four of the six stories stand on slides with a fact row, all six are told in the notes; no photograph is used (the requests to Wikimedia answered 429).

Usage: python3 deck_build_v1_0_0.py   (run it with the system python3, which has rdflib; writes deck_plan_v1_0_0.json and links_v1_0_0.json beside itself; needs rdflib)
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


ST = load("stories24", os.path.join(HERE, "..", "sen0414_ch24_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
DG = load("diagrams24", os.path.join(HERE, "..", "sen0414_ch24_diagrams_v1_0_0.py"))
NODES = DG.nodes_from_ttl(os.path.join(HERE, "..", ".."))
_bad = DG.run_checks(NODES)
if _bad:
    raise SystemExit("REFUSED: the diagrams fail their own checks: %r" % _bad[:3])
DIAG = {d["id"]: d for d in DG.DIAGRAMS}
RD = load("rdodi24", os.path.join(HERE, "..", "sen0414_ch24_rdodi_data_v1_0_2.py"))
EX = json.load(open(os.path.join(HERE, "examples_out_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s; no row reads the clock or the network" % PYV
G = {k: [[s, (o or "")] for s, o in v] for k, v in EX.items() if not k.startswith("_")}
PROGS = EX["_programs"]
IMGDIR = os.path.join(HERE, "images")
CQ1, CQ2 = RD.CQS
CW = 0.0088  # inches per character per point of Courier New, as the shared fit check measures it

L_NOTEXEC = "NOT EXECUTED"
L_REC = "Recorded"


def lines_of(rows):
    return sum(1 + (1 if out.strip() else 0) for _, out in rows)


ROWS_SHOWN = len(G["title"]) + len(G["tools"])


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
    """the first line of a Cut that is shown: the line after the marker '# ---- shown from here ----' that ends the hidden head"""
    return span(pname, "# ---- shown from here ----")[0] + 1


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


def pfit(pname, x, y, wmax, hmax, a=None, b=None, right=False, lo=7.0, hi=8.0):
    """prog() of the lines a to b of a Cut (default: the body after the hidden head to the last line) at the largest size that fits wmax x hmax;
    right=True puts the panel against the right margin. Returns (item, bottom y, a, b, x, w)."""
    a = body(pname) if a is None else a
    b = len(PROGS[pname]["code"].rstrip("\n").split("\n")) if b is None else b
    f = bestfs(pname, (a, b), wmax, hmax, lo=lo, hi=hi)
    w = pw(pname, (a, b), True, f)
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


def sbs(pname, x, y, wcode_max=None, a=None, b=None, hmax=3.45, hi=8.5, lo=7.0):
    """A Cut as two panels side by side: its lines a to b (default: the body) in a panel without the transcript, and the transcript in a
    'transcript of program' panel to the right of it, against the right margin, both at the largest font (hi down to lo) at which the two panels fit the slide's
    width and the height hmax. Returns (code item, transcript item, bottom y of both, x of the right panel, its width, a, b)."""
    a = body(pname) if a is None else a
    b = len(PROGS[pname]["code"].rstrip("\n").split("\n")) if b is None else b
    tr = PROGS[pname]["transcript"].split("\n")
    nl = max(b - a + 1, len(tr))
    fs = hi
    while fs >= lo - 1e-9:
        w = pw(pname, (a, b), False, fs)
        need = round(max(len(l) for l in tr) * CW * fs + 0.9, 2)
        if (wcode_max is None or w <= wcode_max + 0.005) and x + w + 0.2 + need <= 9.5 + 0.005 and nl * (fs * 1.22 / 72.0 + 0.02) + 0.30 <= hmax:
            break
        fs -= 0.5
    else:
        raise SystemExit("REFUSED: %s lines %d-%d and its transcript do not fit side by side in %.2f x %.2f in even at %.1f pt" % (pname, a, b, 9.5 - x, hmax, lo))
    it, bot = prog(pname, x, y, w, fs=fs, lines=(a, b), show_out=False)
    xr = round(x + w + 0.2, 2)
    tp, bt = tpanel(pname, xr, y, round(9.5 - xr, 2), fs=fs)
    return it, tp, max(bot, bt), xr, round(9.5 - xr, 2), a, b


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
                LATE.append("item %s on slide %d %r reaches y %.2f / x %.2f (starts %.2f)" % (it["t"], len(S) + 1, title, it["y"] + it.get("h", 0.4), it["x"] + it["w"], it["y"]))
        if it["t"] == "shapes":
            SHOWN[it["did"]] = len(S) + 1
        if it["t"] == "prog":
            nm = it["label"].replace("transcript of program ", "").replace("program ", "").split(",")[0]
            if PROGS[nm]['kind'] in ('standin', 'standin_remote'):
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


def hid(pn, a, b, what_before="imports, helpers and the work folder", what_after=None):
    """The words that say which lines of the program are not on the slide: lines 1 to a-1, and lines b+1 to n."""
    n = len(PROGS[pn]["code"].rstrip("\n").split("\n"))
    out = []
    if a > 1:
        out.append(("Lines 1 to %d (%s) are not shown." % (a - 1, what_before)) if a > 2 else ("Line 1 (%s) is not shown." % what_before))
    if b < n:
        out.append(("Lines %d to %d (%s) are not shown." % (b + 1, n, what_after or "the rest")) if b + 1 < n else ("Line %d (%s) is not shown." % (n, what_after or "the rest")))
    return " ".join(out)



SAY_NS = "No sound card: nothing is heard, the speech goes to WAV files - a local stand-in for a loudspeaker."
SAY_AI = "archive.org public-domain audio stands in for YouTube, which this deck never used."
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


# ---- 1 title ---------------------------------------------------------------------------------------------------
c1, _ = con("title", 5.0, 0.25, 4.5, fs=8, cap=False)
S.append({"kind": "title", "title": "Ch. 24: Speech Engines",
          "sub": "Speech synthesis with pyttsx3, recognition with Whisper, subtitles and downloads with yt-dlp",
          "items": [c1, foot("Every output on these slides was printed by the Python above when the deck was made, and every picture was saved by a program that is run again to check it. "
                             "Nothing is heard: the machine has no sound card, so the speech goes to WAV files. "
                             "Windows, macOS, a microphone, a GPU, a cloud key and YouTube were never used; what could not be run is marked on its slide.",
                             0.6, 3.75, 8.8, fs=10.5)],
          "notes": "Chapter 23 taught a program to act on the screen. Chapter 24 teaches a program to speak and to listen: pyttsx3 turns text into speech, Whisper turns speech into text, the writers of whisper.utils turn the text into subtitle files, and yt-dlp downloads the audio of a video. "
                   "The chapter has %d listings and %d table, and ends with 7 practice questions and 3 practice programs. "
                   "This deck follows the chapter in its own order: the engine and its settings, saving speech as a WAV file, the Whisper models and what they hear, the subtitle files, the downloader, and the three practice programs, and it adds what the research found when the chapter's %d printed statements were replayed. "
                   "Nothing in the deck is heard. The machine has no sound card, so the console above shows that /dev/snd does not exist, and every program writes its speech to a WAV file that it deletes afterwards. "
                   "Every output on the slides was printed by Python %s with pyttsx3 2.99, openai-whisper 20250625, yt-dlp 2026.8.19 and NumPy 2.5.4, the versions the console above prints, with eSpeak NG 1.51 and ffmpeg 6.1.1 on the path. "
                   "Windows, macOS, a microphone, a GPU, a cloud key and any download from YouTube were never used. What could not be run is marked NOT EXECUTED on its slide, and what the research measured and this deck does not run again is marked Recorded. "
                   "Every count and time from one run is a single run on a machine with two cores, and not a benchmark." % (17, 1, 46, PYV),
          "bg": "light"})

# ---- 2 agenda (filled in at the end) -------------------------------------------------------------------------------
S.append({"kind": "content", "title": "Today's route", "sub": "", "items": [], "notes": "", "take": "", "bg": "light"})

# ---- 3 questions ------------------------------------------------------------------------------------------------
_nb = len(DIAG["TextToSpeechAndSpeechRecognitionAtAGlance"]["data"]["branches"])
content("The questions this chapter answers", "The research's two competency questions; the summary comes back to each",
        [{"t": "numlist", "x": 0.5, "y": 1.35, "w": 9.0, "h": 2.5, "fs": 10, "items": [CQ1, CQ2]},
         {"t": "chips", "x": 0.5, "y": 3.95, "w": 9.0, "h": 0.5, "fs": 10,
          "items": ["%d branches" % _nb, "%d topics" % len(NODES), "%d console rows" % ROWS_SHOWN,
                    "%d programs run" % len(PROGS), "%d diagrams" % len(DIAG), "%d pictures" % len(EX["_images"]), "Python %s" % PYV]}],
        "The first question is the spine of the chapter, and the deck answers it slide by slide. On a machine with no sound card, no microphone and no GPU, a program can still list the voices of the engine, change the rate and the volume, save speech as a WAV file, transcribe that file with Whisper, write subtitle files and ask yt-dlp for the metadata of a video, and every one of those can be checked because the result is a file or a number. "
        "What cannot be shown to work is the part that needs a person or a service: the sound itself, a microphone, a GPU, Windows and macOS, the cloud services, and any download from YouTube, whose Terms of Service do not allow it. "
        "The second question is the watch-out. The chapter's 17 listings hold 45 statements, 46 with the one that was substituted, and the research replayed them as printed. "
        "With Python 3.14.6 and the newest packages 34 of the 46 matched the book's output, 42 ran without an exception, 1 raised and 3 were not executed; the pinned set gave 35, 42, 1 and 3, the empty environment 8, 8, 35 and 3, and the set without ffmpeg 32, 38, 5 and 3. "
        "The statements that differ are the Voice objects and names, the line Audio saved to that the driver prints, the transcription of hello.wav, the TSV listing and the call of speak(), which no listing defines. Each slide says where a printed line differs and on what evidence. "
        "The spread between releases is large too: of the 22 releases of pyttsx3, 8 ran and 9 crashed with a segmentation fault, and Appendix A pins a pyttsx3 that saves a truncated file.",
        "Know what can be shown to work and what can only be shown to fail.")

# ---- 4 what a script can do ---------------------------------------------------------------------------------------
dg, dcap = diagram("WhatYouCanDoWithTheEngines", "usecases", (0.5, 1.4, 4.6, 2.75), fs=8)
c4, bot4 = con("tools", 5.3, 1.45, 4.2, fs=8, cap=True)
content("What a script can do with the engines", "Seven uses of the engines; the console shows the tools of this machine",
        [dg, dcap, c4,
         foot("os.path.exists('/dev/snd') is False: no sound card, no microphone and no GPU, so nothing in this deck is heard.", 5.3, round(bot4 + 0.04, 2), 4.2, fs=8),
         foot(rec("the chapter page (200, 44,667 bytes) holds 17 listings and 1 table; the online materials (91 files) hold hello_tts.py as the only file of the chapter."), 5.3, round(bot4 + 0.36, 2), 4.2, fs=8),
         factrow("Voder1939", y=4.58)],
        story_notes("Voder1939") + " The use-case diagram lists what a script can do with the engines of the chapter: list the voices of the engine, change the rate of the speech, save speech as a WAV file, transcribe audio with transcribe(), write a subtitle file, read the metadata of a video and download audio with download(). "
        "They are independent calls into three libraries, which is why the picture is a set of uses and not a sequence. "
        "The console runs under the interpreter of the deck. ffmpeg and espeak-ng are on the path, /dev/snd does not exist, audioop is gone from this Python and wave is not: PEP 594 removed audioop, aifc, sunau, chunk and sndhdr in Python 3.13, and the wave module that pyttsx3 uses stayed. "
        "The card records what the research found on 14 October 2026 and this deck does not run again: the chapter page returned 200 with 44,667 bytes and its sha256 equals the digest in the book's own chapter ontology; the online materials are a zip of 91 files, 72 of them Python, and none of them imports whisper or yt_dlp or holds hello.wav, audio.srt or metadata.json. "
        "The publisher's book page names the chapter once and Whisper, pyttsx3 and yt-dlp not at all.",
        "A script can speak, listen and write subtitles with a few calls.", recorded=True)

# ---- 5 packages, tools and what is missing ------------------------------------------------------------------------------
tbe = EX["_tables"]["environments"]["rows"]
tbl5 = {"t": "table", "x": 0.5, "y": 1.45, "w": 4.3, "colW": [0.95, 0.75, 0.8, 0.8, 1.0], "fs": 8, "rowH": 0.26, "cellMargin": [0.02, 0.04, 0.02, 0.04], "rows": tbe}
content("Packages and the tools they need", "pyttsx3 needs eSpeak NG and Whisper needs ffmpeg, which the chapter never installs",
        [tbl5,
         foot("One probe, four interpreters, run when the deck is checked: it imports the packages, looks for ffmpeg and calls pyttsx3.init().", 0.5, 3.9, 4.3, fs=8.5),
         *stack([rec("Appendix A pins pyttsx3==2.98 and openai-whisper==20231117, advises numpy below 2 and names neither ffmpeg nor espeak; PyPI lists 22 releases of pyttsx3 (2.99 the newest), 13 of openai-whisper (20250625) and 641 of yt-dlp (2026.8.19)."),
                 rec("the chapter's command sudo apt install espeak: with neither package pyttsx3 2.99 raised RuntimeError, with only espeak 1.48.15 it raised ValueError (SetVoiceByName failed for gmw/en) and with espeak-ng 1.51 it worked."),
                 ne("SAPI5 on Windows, NSSpeechSynthesizer and AVSpeech on macOS, a microphone, a GPU and the cloud services of OpenAI, Google and Microsoft; only the eSpeak NG driver on Linux ran.")],
                5.0, 1.45, 4.5, fs=8.5, gap=0.07),
         factrow("ESpeak1995", y=4.58)],
        story_notes("ESpeak1995") + " The table runs one probe in four interpreters while the deck is checked: Python 3.14.6 with the newest packages, Python 3.12.3 with the pinned pyttsx3 2.98 and openai-whisper 20231117 and NumPy 1.26.4, Python 3.14.6 with ffmpeg taken off the path, and an empty Python 3.14.6. "
        "The probe imports the packages, looks for ffmpeg and calls pyttsx3.init(); every row with the packages starts an Engine, the empty Python raises ModuleNotFoundError, and the row without ffmpeg shows the only difference that the probe can see. "
        "The chapter's Linux command installs espeak, the old package, and pyttsx3 2.99 needs espeak-ng: the research tried the four combinations on Ubuntu 24.04 and only the two that include espeak-ng started, with 131 voices, a saved WAV file and the library libespeak-ng.so.1. "
        "Appendix A pins the 2.98 release of pyttsx3, advises numpy below 2 and the CUDA 11.8 wheels of PyTorch, and says that the automateboringstuff3 package always installs the newest yt-dlp. It names neither ffmpeg nor espeak, and the next slides show what each one is needed for. "
        "SAPI5, NSSpeechSynthesizer, AVSpeech, the microphone, the GPU and the cloud services were read from their documentation and never run.",
        "Install eSpeak NG and ffmpeg first; the Python packages are not enough.", notexec=True, recorded=True)

# ---- 6 the pinned release and the newest --------------------------------------------------------------------------------
pn = "pinCut_v1_0_0.py"
dg, dcap = diagram("ThePinnedReleaseAndTheNewest", "sequence", (0.5, 1.4, 4.1, 2.05), fs=8, head_w=0.9, gap0=0.3)
rel = EX["_tables"]["releases"]["rows"]
tbl6 = {"t": "table", "x": 0.5, "y": 3.95, "w": 4.1, "colW": [1.0, 0.45, 0.6, 0.35, 1.7], "fs": 7, "rowH": 0.2, "cellMargin": [0.02, 0.04, 0.02, 0.04], "rows": rel}
p6, bot6, a6, b6, x6, w6 = pfit(pn, 4.8, 1.55, 4.7, 2.85, right=True)
content("The pinned release and the newest", "Appendix A pins pyttsx3 2.98, which saves 0.6 s of audio where 2.99 saves 1.54 s",
        [dg, dcap, tbl6, p6,
         foot(SAY_NS + " " + hid(pn, a6, b6, "imports and helpers"), x6, round(bot6 + 0.04, 2), w6, fs=7.5),
         foot(rec("the table counts the releases tried on one machine."), 0.5, 4.8, 4.1, fs=7.5)],
        "The sequence diagram is the story of the pin: the reader installs the pinned release of pyttsx3 from PyPI, PyPI delivers pyttsx3 2.98, the reader saves the sentence Hello. How are you doing?, and the engine truncates the file; with pyttsx3 2.99 the same sentence is saved whole. "
        "The program runs the same few lines in two interpreters, Python 3.12.3 with pyttsx3 2.98 and Python 3.14.6 with 2.99, and prints the length of the file each wrote: 0.6 and 0.51 seconds for the pinned release, 1.54 and 1.55 for the newest. The sentences are Hello. How are you doing? and One. Two. Three. "
        "The research found the cause in the driver: 2.98 writes the file at the first end-of-sentence event, before it adds the samples of that event, and it hands the file to ffmpeg, so a name ending in .mp3 gave a real MP3 file, .ogg a real Ogg file, and with no ffmpeg on the path no file at all, while 2.99 writes a WAV file through the wave module whatever the extension says. "
        "The table is the research's record of the releases it tried: of 22 releases of pyttsx3, 8 ran on Python 3.14.6, 9 (2.71 to 2.95) crashed with a segmentation fault and 5 needed macOS; of 13 releases of openai-whisper, 6 ran on Python 3.12.3, 1 had an import error and 6, 20230307 to 20231106, could not be installed there because they require triton 2.0.0; of the 6 last stable yt-dlp releases of 2021 to 2026, 5 ran and 2021.12.27 stopped on the missing imghdr module that Python 3.13 removed. "
        "Pinning is not safe by itself: the pinned openai-whisper also needed setuptools below 81 and no build isolation before it would install.",
        "A pinned release can be older than the book's own output.", recorded=True)

# ---- 7 say() only queues the text ----------------------------------------------------------------------------------------
pn = "sayCut_v1_0_0.py"
dg, dcap = diagram("TheLifeOfAnUtterance", "lifecycle", (0.5, 1.4, 3.5, 2.1), fs=8, sw=1.5, sh=0.36, sfs=8, top=0.3, lab_w=1.6)
p7, bot7, a7, b7, x7, w7 = pfit(pn, 4.2, 1.55, 5.3, 3.0, right=True)
content("say() only queues the text", "Nothing is spoken until runAndWait(); a property set before it is not applied yet",
        [dg, dcap, p7,
         *stack([SAY_NS, hid(pn, a7, b7, "imports, helpers and the work folder")], 0.5, round(dcap["y"] + dcap["h"] + 0.1, 2), 3.5, fs=8, gap=0.04),
         foot(rec("with no sound card runAndWait() returned with exit code 0 although aplay printed an audio open error; save_to_file('') raised AssertionError."), x7, round(bot7 + 0.06, 2), w7, fs=8.5)],
        "The life of an utterance has three states. The text is in the queue after say(); the utterance has started when runAndWait() fires started-utterance; and it has finished when the engine fires finished-utterance. "
        "The program connects both events to a list and shows the three moments. say() returns None at once, no event has fired and isBusy() already reports True, because the text is only in the queue. "
        "After setProperty('rate', 300) the rate still reads 200, since a property is applied when runAndWait() processes the queue, and it reads 300 after the call. The events list ends with started-utterance and finished-utterance, in that order. "
        "say('') does not raise an error: it returns the text Argument value can't be None or empty. The research also saw that save_to_file('') raised AssertionError, and that with no sound card, which is the case here, runAndWait() returned with exit code 0 although aplay printed an audio open error, so a program that speaks to nobody does not fail. "
        "The program of the slide never plays a sound: the engine is asked to speak, the audio device is absent and nothing is heard, which is the local stand-in the slide names.",
        "A call that speaks does nothing until runAndWait() runs.", recorded=True)

# ---- 8 the voices of the engine -----------------------------------------------------------------------------------------
pn = "voicesCut_v1_0_0.py"
p8, bot8, a8, b8, x8, w8 = pfit(pn, 0.5, 1.55, 5.5, 3.42)
xr = round(x8 + w8 + 0.2, 2)
content("The voices of the engine", "131 voices, 8 of them English; the engine starts with gmw/en and voices[1] is Amharic",
        [p8,
         *stack([SAY_NS, hid(pn, a8, b8, "imports, helpers and the work folder"),
                 rec("the research's hello.wav with voices[1] lasted 0.89 s where this deck's run prints 1.48 s; both are single runs, and the default voice gives 1.54 s."),
                 ne("SAPI5 on Windows and NSSpeechSynthesizer on macOS: the Voice names David and Zira that the chapter prints could not be listed here, and no name of the 131 contains them.")],
                xr, 1.5, round(9.5 - xr, 2), fs=8, gap=0.06)],
        "The program lists the voices of eSpeak NG through pyttsx3 2.99: 131 Voice objects, the first of them Afrikaans with the gender Male, the age None and the languages ['af']. All 131 say Male, none has an age, and 8 are English. The voice the engine starts with is gmw/en. "
        "The chapter's listing 4 prints the names of Windows voices, David and Zira; no voice here has those names, and the research confirmed that none of the 131 names contains them. The chapter then sets the voice to voices[1].id, which on this engine is sem/am, Amharic, so the program speaks the same sentence with it and saves hello.wav. "
        "The research measured 0.89 seconds for that file and 1.54 seconds for the default voice; this deck's own run of the program prints 1.48 seconds for voices[1], and the difference is one more reason to treat a time as a single run. "
        "A Voice object is not a string: printing a list of voices shows addresses, one of the statements of the chapter that cannot match its book. "
        "SAPI5 and NSSpeechSynthesizer, the drivers of Windows and macOS, were read from their sources and documentation, and were not executed.",
        "The voices depend on the engine and the operating system.", notexec=True, recorded=True)

# ---- 9 rate and volume ----------------------------------------------------------------------------------------------------
pn = "rateCut_v1_0_0.py"
p9, bot9, a9, b9, x9, w9 = pfit(pn, 0.5, 1.55, 4.7, 3.42)
xr = round(x9 + w9 + 0.2, 2)
ch9 = EX["_charts"]["rateSeconds"]
chart9 = {"t": "chart", "ctype": "bar", "x": xr, "y": 1.4, "w": round(9.5 - xr, 2), "h": 1.6, "labels": ch9["labels"],
          "title": "Seconds of audio by rate", "series": [{"name": "seconds", "data": ch9["values"]}], "dataLabels": True, "dlFs": 8}
im9, ib9, _ = img("waves.png", xr, 3.05, round(9.5 - xr, 2), 0.8)
content("Rate and volume", "Seven rates turn 6.46 s of speech into 1.26 s; volume 5 clips at 32768",
        [p9, chart9, im9, imgcap(["waves.png"], xr, round(ib9 + 0.02, 2), round(9.5 - xr, 2), fs=8),
         *stack([SAY_NS, hid(pn, a9, b9, "imports, helpers and the work folder", "the picture")], xr, round(ib9 + 0.3, 2), round(9.5 - xr, 2), fs=8, gap=0.03)],
        "The chart is the length in seconds of the same ten-word sentence, The quick brown fox jumps over the yellow lazy dog, at seven rates, each set in a fresh process: 6.46 seconds at rate 50, 5.44 at 100, 3.62 at 150, 2.70 at 200, which is the default, 2.16 at 250, 1.76 at 300 and 1.26 at 400. "
        "The rate is the speed in words per minute that the engine is asked for, and the measured speed at the default is about 222 words per minute. "
        "The volume is a number from 0 to 1 that scales the samples: the largest sample is 26394 at volume 1.0, 19622 at 0.75, 13024 at 0.5, 2222 at 0.1 and 0 at 0.0, and volume 5 gives 32768, the end of what 16 bits hold, so the sound is clipped and the chapter's advice to keep the volume at or below 1 is not a matter of taste. "
        "The picture shows the two files at a common time scale: the slow one, rate 100, is longer than the fast one, rate 300. "
        "Each value comes from a separate process because the rate set with setProperty() is only applied when runAndWait() runs, as the previous slide showed. The research set the rate before each of seven files in one process and got the same seven lengths in its run. "
        "All of these are single runs.",
        "The rate sets the speed, and a volume above 1 only clips.")

# ---- 10 the WAV file ------------------------------------------------------------------------------------------------------
pn = "wavCut_v1_0_0.py"
p10, bot10, a10, b10, x10, w10 = pfit(pn, 0.5, 1.55, 5.2, 3.42)
xr = round(x10 + w10 + 0.2, 2)
im10, ib10, _ = img("hello.png", xr, 1.5, round(9.5 - xr, 2), 0.7)
content("Saving speech as a WAV file", "save_to_file() writes 22,050 Hz mono samples, whatever the extension says",
        [p10, im10, imgcap(["hello.png"], xr, round(ib10 + 0.02, 2), round(9.5 - xr, 2), fs=8),
         *stack([SAY_NS, hid(pn, a10, b10, "imports, helpers and the work folder")], xr, round(ib10 + 0.35, 2), round(9.5 - xr, 2), fs=8, gap=0.04)],
        "save_to_file() does not write anything when it is called: the program prints that hello.wav does not exist before runAndWait(), and the file appears when the queue is processed. "
        "The file for Hello. How are you doing? has 1 channel, 2 bytes per sample, a rate of 22,050 Hz and 33,948 frames, which is 1.54 seconds and 67,940 bytes, and it is written with the wave module. "
        "The chapter says the file can have another extension; pyttsx3 2.99 writes a WAV whatever the name says, so the file hello.mp3 begins with RIFF and WAVE, and the research found that ffprobe called it a wav file. The pinned 2.98, by contrast, handed the file to ffmpeg. "
        "The picture is the waveform of hello.wav, saved by the same program: the greater the amplitude the taller the strip, and the pauses between the words are the flat parts. "
        "Because the file can be incomplete when runAndWait() returns, the program calls a small helper that waits until the size of the file has not changed for a moment; the next slide shows why. "
        "In the research 1,800 words of Alice's Adventures in Wonderland became 450.2 seconds, 7.5 minutes, of audio in about 3 seconds of work, where the chapter says 10 minutes in about 2 seconds; that is one run on this machine.",
        "The file is a WAV, and it exists only after runAndWait().")

# ---- 11 a call that never returns ------------------------------------------------------------------------------------------
pn = "raceCut_v1_0_0.py"
dg, dcap = diagram("SpeakingAndSavingASentence", "activity", (0.5, 1.4, 4.2, 2.55),
                   grid={"init": (0, 0), "say": (0, 1), "run": (0, 2), "done": (0, 3), "wait": (0, 4), "open": (1, 3)},
                   cols=[(0.3, 1.7), (2.5, 1.6)], rows_n=5, starts=(1, 0), ends={"type": "dot", "col": 1, "row": 4},
                   routes={("start", "init"): "h", ("done", "wait"): "v", ("wait", "done"): "loopL", ("done", "open"): "h", ("open", "end"): "v"}, fs=8, nh=0.46, dh=0.46)
p11, bot11, a11, b11, x11, w11 = pfit(pn, 4.9, 1.55, 4.6, 3.1, right=True)
content("A call that never returns", "runAndWait() hangs on a second call and on a missing folder; wait for the file",
        [dg, dcap, p11,
         foot(SAY_NS + " " + hid(pn, a11, b11, "imports and helpers"), x11, round(bot11 + 0.04, 2), w11, fs=7.5),
         foot(rec("in 12 fresh processes a 33-word text was not yet a complete file when the first runAndWait() returned in 8, and a 5-word text in none."), 0.5, round(dcap["y"] + dcap["h"] + 0.05, 2), 4.2, fs=8)],
        "The activity diagram is the safe way to save a sentence: initialise the engine, call save_to_file() with the text and the file name, call runAndWait() to process the queue, and then ask whether the file is complete; if it is, open it with the wave module, and if not, wait until the size of the file is stable and ask again. "
        "The program shows the two ways a call does not come back, each in a child process that is given 5 seconds. A runAndWait() with nothing to say, after a property was changed, returns the first time and does not return the second time; and a save_to_file() into a folder that does not exist returns as the first call of a process and does not return after an utterance. "
        "The research killed both after 15 seconds. It also found that the file is not always complete when the first runAndWait() returns: in 12 fresh processes that was so in 8 for a text of 33 words and in none for a text of 5 words. "
        "A program that opens the file straight away may read half of it, which is why the helper waits for the size to settle. The hanging calls are written here as a warning, and the safest habit is one runAndWait() after all the calls, and a folder that exists.",
        "Wait for the file, and never call runAndWait() twice with nothing queued.", recorded=True)

# ---- 12 the Whisper models --------------------------------------------------------------------------------------------------
pn = "modelsCut_v1_0_0.py"
tbl12 = {"t": "table", "x": 0.5, "y": 1.45, "w": 5.9, "colW": [0.7, 0.9, 1.15, 0.9, 1.15, 1.1], "fs": 7.5, "rowH": 0.24, "cellMargin": [0.02, 0.04, 0.02, 0.04],
         "rows": EX["_tables"]["models"]["rows"]}
c12, t12, bot12, xr12, wr12, a12, b12 = sbs(pn, 0.5, 3.15, 5.0, hmax=1.85, hi=7.5)
content("The Whisper models", "Table 24-1 against this machine: medium and turbo were killed, large-v3 does not load",
        [tbl12, c12, t12,
         foot(hid(pn, a12, b12, "imports, helpers and the work folder"), xr12, round(t12["y"] + t12["h"] + 0.05, 2), wr12, fs=8),
         *stack([rec("the columns 'here' are the research's runs on two CPU cores (single runs): 10 words took 1.0, 1.6 and 5.1 s, and 1,800 words (13 minutes) took 40.0, 98.9 and 197.5 s."),
                 ne("transcription with medium and turbo (killed at about 6 GB of memory), with large-v3 (3,087,371,615 bytes, does not load) and on a GPU: findings, not successes.")],
                6.6, 1.45, 2.9, fs=8, gap=0.06)],
        "Table 24-1 of the chapter lists five models with a file size, the time to transcribe 10 words and the time for 15 minutes: tiny 74MB, 1.9 s and 1m 20s; base 142MB, 3.0 s and 2m 34s; small 472MB, 9.6 s and 6m 37s; medium 1.5GB, 28.6 s and 20m 17s; large-v3 3GB, 51.9 s and 32m 58s. "
        "The table of the slide sets the book beside this machine. The files have 75,572,083 bytes for tiny, 145,262,807 for base, 483,617,219 for small and 3,087,371,615 for large-v3, so the book's sizes are rounded down; the program counts the parameters of the three models that load, 37.2, 71.8 and 240.6 million, and reads the sizes of their files. "
        "On two CPU cores the research measured 1.0, 1.6 and 5.1 seconds for the ten words where the table says 1.9, 3.0 and 9.6, and the memory of the process peaked at 972, 1,082 and 2,645 MiB. These are single runs on one machine, not the author's laptop. "
        "Loading medium and turbo ended with the kernel's out-of-memory killer, return code -9, on a machine with 8,029 MiB of memory; the README of Whisper lists about 6 GB for turbo and about 10 GB for large. large-v3 could not be loaded under a 6.5 GB address-space limit. These are findings, not successes. "
        "The package knows 14 model names, turbo among them. The program asks for device='cuda' and gets RuntimeError, because torch.cuda.is_available() is False; no GPU was used for anything in this deck.",
        "Pick the model that fits the memory you have, not the one the table praises.", notexec=True, recorded=True)

# ---- 13 transcribing a sentence ---------------------------------------------------------------------------------------------
pn = "transcribeCut_v1_0_0.py"
p13, bot13, a13, b13, x13, w13 = pfit(pn, 0.5, 1.55, 5.2, 2.9)
xr = round(x13 + w13 + 0.2, 2)
ch13 = EX["_charts"]["werByModel"]
chart13 = {"t": "chart", "ctype": "bar", "x": xr, "y": 1.4, "w": round(9.5 - xr, 2), "h": 1.9, "labels": ch13["labels"],
           "title": "Word error rate, ten words", "series": [{"name": "word error rate", "data": ch13["values"]}], "dataLabels": True, "dlFs": 9}
content("Transcribing a sentence", "tiny, base and small make word error rates of 0.3, 0.2 and 0.1 on ten words",
        [p13, chart13,
         *stack([SAY_NS, hid(pn, a13, b13, "imports, helpers and the work folder")], xr, 3.4, round(9.5 - xr, 2), fs=8, gap=0.04),
         factrow("Whisper2022", y=4.58)],
        story_notes("Whisper2022") + " The program speaks the ten-word sentence of the chapter, The quick brown fox jumps over the yellow lazy dog, into fox.wav and transcribes the file with the three models. "
        "tiny hears the quick brown fog stump over the yellow laser dog, base the quick round fox dumps over the yellow lazy dog, and small the quick brown fox dumps over the yellow lazy dog. The word error rate, the number of words to change divided by the number of words said, is 0.3, 0.2 and 0.1, which the chart draws. "
        "The result is a dictionary with the keys text, segments and language, and each segment has the keys id, seek, start, end, text and tokens. The default of transcribe() may retry with a random temperature, which is why the programs of this deck pass temperature=0.0 wherever the text is printed: the same file gives the same text twice. "
        "A word error rate of one sentence is only a count. The research measured 0.1919, 0.1079 and 0.0345 on the 1,800 words read by eSpeak NG, between 0.1636 and 0.3123 for tiny, 0.1524 and 0.2565 for base and 0.0186 and 0.2416 for small on four LibriVox readings of the Gettysburg Address, and it saw tiny transcribe ten seconds of digital silence as the word You. "
        "Speech made by a synthesiser is easy and a human voice is not; a transcript is the text of a model and not a copy of what was said.",
        "Larger models make fewer mistakes, and every transcript is a model's guess.")

# ---- 14 Whisper needs ffmpeg ------------------------------------------------------------------------------------------------
pn = "ffmpegCut_v1_0_0.py"
dg, dcap = diagram("FromAudioToSubtitles", "activity", (0.5, 1.4, 3.6, 2.2),
                   grid={"load": (0, 0), "ff": (0, 1), "tr": (0, 2), "wr": (0, 3), "err": (1, 1)},
                   cols=[(0.05, 1.7), (2.05, 1.5)], rows_n=4, starts=(1, 0), ends={"type": "dot", "col": 1, "row": 3},
                   routes={("start", "load"): "h", ("ff", "err"): "h", ("wr", "end"): "h", ("err", "end"): "v"}, fs=8, nh=0.46, dh=0.5)
p14, bot14, a14, b14, x14, w14 = pfit(pn, 4.3, 1.55, 5.2, 2.95, right=True)
im14, ib14, _ = img("audio16k.png", 0.5, 4.0, 3.6, 0.5)
content("Whisper needs ffmpeg", "load_audio() starts ffmpeg for every file; without it the call raises an error",
        [dg, dcap, im14, imgcap(["audio16k.png"], 0.5, round(ib14 + 0.02, 2), 3.6, fs=8), p14,
         foot(SAY_NS + " " + hid(pn, a14, b14, "imports and helpers", "the picture"), x14, round(bot14 + 0.04, 2), w14, fs=7.5)],
        "The flow chart is the first half of every transcription: load a model, ask whether ffmpeg is on the path, and, if it is, call transcribe() and then get_writer() to write the subtitle file; if it is not, the call raises FileNotFoundError and the chain ends. "
        "The chapter names ffmpeg only inside a comment of the yt-dlp listing, and Appendix A never names it, yet whisper.load_audio() starts ffmpeg for every file. With it on the path a WAV file becomes a float32 array of 43,129 samples at 16,000 Hz, the rate Whisper wants whatever the rate of the file was. "
        "The program empties the path for two calls and both raise FileNotFoundError: load_audio() itself and transcribe(), which calls it. The picture is the signal after the conversion, the same speech at 16 kHz. "
        "The research found the same for yt-dlp: without ffmpeg, extracting audio raised DownloadError, ffprobe and ffmpeg not found, and left downloaded_content.mp3 instead of the m4a that listing 13 looks for, so a missing tool shows up far from where it is needed. "
        "The package manager of the system, not pip, installs ffmpeg, which is why the probe of slide 5 looks for it.",
        "Install ffmpeg before you install Whisper.")

# ---- 15 languages and what Whisper hears ------------------------------------------------------------------------------------------
pn = "langCut_v1_0_0.py"
c15, t15, bot15, xr15, wr15, a15, b15 = sbs(pn, 0.5, 1.55, 5.0, hmax=3.4)
content("Languages and what Whisper hears", "tiny named 3 of 6 languages and base 4; Turkish was heard as Thai; klingon raises",
        [c15, t15,
         *stack([SAY_NS, hid(pn, a15, b15, "imports, helpers and the work folder"),
                 rec("tiny and base wrote 'Hello, how are you doing?' for the sentence the book prints as 'Hello. How are you doing?'; the word error rate on 1,800 words read by eSpeak NG was 0.1919, 0.1079 and 0.0345.")],
                xr15, round(t15["y"] + t15["h"] + 0.08, 2), wr15, fs=8, gap=0.05)],
        story_notes("Audrey1952") + " The program speaks one sentence in each of six languages with the voices of eSpeak NG, Turkish, German, French, Spanish, Italian and English, and asks tiny and base which language they hear. "
        "tiny named the language right for 3 of the 6 and base for 4: the Turkish sentence was heard as Thai by both, German as Danish by tiny, and Italian as Korean by tiny and as Spanish by base; the research, which used a Chinese sentence where this deck uses Italian, got the same totals, 3 and 4. "
        "Whisper 20250625 knows 100 languages, and asking for a language it does not know, here klingon, raises ValueError, Unsupported language. "
        "A transcript is a model's text: tiny and base wrote Hello, how are you doing for the sentence the book prints as Hello. How are you doing?, so a program that compares a transcript with the text it spoke has to normalise case and punctuation first, as the word error rate of the previous slide does. "
        "The synthesised speech is clean and unnatural, and the numbers say nothing about a human voice, an accent or noise.",
        "Name the language yourself; do not let a small model guess.", recorded=True)

# ---- 16 subtitle files --------------------------------------------------------------------------------------------------------
pn = "cuesCut_v1_0_0.py"
c16, t16, bot16, xr16, wr16, a16, b16 = sbs(pn, 0.5, 1.55, 5.1, hmax=2.4, hi=7.5)
im16, ib16, _ = img("cues.png", 0.5, 3.98, 4.0, 0.5)
content("Subtitle files: SRT, VTT and TSV", "SRT, VTT and TSV: 223, 215 and 190 bytes for the book's two segments",
        [c16, t16, im16,
         *stack([imgcap(["cues.png"], xr16, round(t16["y"] + t16["h"] + 0.05, 2), wr16, fs=8)["body"], hid(pn, a16, b16, "imports, helpers and the work folder, where A and B are the two sentences of the book's listing")],
                xr16, round(t16["y"] + t16["h"] + 0.05, 2), wr16, fs=8, gap=0.04),
         factrow("SubRip2000", y=4.58)],
        story_notes("SubRip2000") + " The program gives the writers of whisper.utils the two segments the chapter prints, a first cue from 0.0 to 5.64 seconds and a second from 5.64 to 14.96, and writes them in three formats. "
        "The SRT file has 223 bytes, the WebVTT file 215 and the TSV file 190, and the SRT and VTT files equal the chapter's listings 7 and 8, the research found them equal under the pinned release too. "
        "They differ in the shape of the time: SRT counts hours, minutes, seconds and milliseconds with a comma, 00:00:05,640, WebVTT drops the hours and uses a point, 00:05.640, and the TSV file has the columns start, end and text, separated by tabs and counted in milliseconds, where the chapter's listing 9 shows spaces. "
        "get_writer() accepts srt, vtt, tsv, txt and json; asking for docx raises KeyError. The picture draws the two cues on a time axis, one bar for each. "
        "The W3C specification of WebVTT and the SubRip format are in the resources.",
        "One result, three file formats; the writer decides the clock.")

# ---- 17 options and the time grid ----------------------------------------------------------------------------------------------
pn = "optionsCut_v1_0_0.py"
c17, t17, bot17, xr17, wr17, a17, b17 = sbs(pn, 0.5, 1.55, 5.1)
content("Writer options and the time grid", "Options turn 26 subtitle blocks into 31; every time is a multiple of 0.02 s",
        [c17, t17,
         *stack([SAY_AI, hid(pn, a17, b17, "imports, helpers and the work folder")], xr17, round(t17["y"] + t17["h"] + 0.08, 2), wr17, fs=8, gap=0.04)],
        "The program transcribes the Gettysburg Address, a public-domain LibriVox reading hosted by the Internet Archive, with tiny: 26 segments, written as 26 SRT blocks, and 52 times, a start and an end for each segment. "
        "Of the 52, all 52 are multiples of 0.02 seconds, which is the resolution of Whisper's timestamps and the reason a subtitle time never shows a finer step. "
        "With word_timestamps=True the first segment holds 14 words with a time each, and with the writer options max_line_width=30 and max_line_count=2 the same text is cut into 31 blocks with lines of at most 30 characters; the first block shows how a long cue is wrapped. "
        "The options are keyword arguments of the writer, not of transcribe(), and the word-level times are only produced when transcribe() was asked for them. "
        "The archive.org file stands in for YouTube: the deck never used YouTube, and the file is checked against its SHA-256 before use.",
        "Ask for word times, then let the writer cut the lines.")

# ---- 18 yt-dlp: the metadata of a video ---------------------------------------------------------------------------------------
pn = "ytMetaCut_v1_0_0.py"
p18, bot18, a18, b18, x18, w18 = pfit(pn, 0.5, 1.55, 6.0, 3.42)
xr = round(x18 + w18 + 0.2, 2)
content("yt-dlp: the metadata of a video", "extract_info() returns a dictionary; here 7 of the book's 13 keys, for this site",
        [p18,
         *stack([SAY_AI, hid(pn, a18, b18, "imports, helpers and the work folder"),
                 rec("for the chapter's YouTube video yt-dlp 2026.8.19 returned 76 keys (16 formats, 565 s) with all 13 keys of the book in its order; one request failed with 'Sign in to confirm you're not a bot' and a later one succeeded.")],
                xr, 1.5, round(9.5 - xr, 2), fs=8, gap=0.06)],
        "extract_info(url, download=False) returns a dictionary and downloads nothing. The program asks for the metadata of the Gettysburg reading on archive.org, which stands in for YouTube: 53 keys, 3 formats, the extractor archive.org and the title The Gettysburg Address. "
        "Of the 13 keys the chapter prints, id, title, formats, thumbnails, description, duration and webpage_url are here and 6 are missing: thumbnail, channel_id, channel_url, view_count, average_rating and age_limit belong to a video site. "
        "The prose of the chapter says that YoutubeDL has a sanitize() method; it has sanitize_info() and no sanitize, and the program shows both attributes. sanitize_info() makes the dictionary JSON-serializable, as the yt-dlp README says, and writing the result gives a metadata.json of 55 keys. "
        "For the chapter's own video, Beyond the Basic Stuff with Python by Al Sweigart, the research recorded 76 keys, 16 formats and 565 seconds; on the same day one request failed with a request to sign in to confirm you're not a bot and a later one succeeded, so a result from YouTube is not repeatable.",
        "Ask for the metadata first; the keys depend on the site.", recorded=True)

# ---- 19 downloading audio ---------------------------------------------------------------------------------------------------------
pn = "ytDownCut_v1_0_0.py"
p19, bot19, a19, b19, x19, w19 = pfit(pn, 0.5, 1.55, 5.6, 3.42)
xr = round(x19 + w19 + 0.2, 2)
content("Downloading audio", "download() takes a list; the audio is converted to m4a with ffmpeg",
        [p19,
         *stack([SAY_AI, hid(pn, a19, b19, "imports, helpers and the work folder"),
                 ne("a download from YouTube, whose Terms of Service do not allow downloading any part of the Service or its Content except as expressly authorized."),
                 rec("yt-dlp without ffmpeg raised DownloadError (ffprobe and ffmpeg not found) and left downloaded_content.mp3 instead of the m4a that listing 13 looks for.")],
                xr, 1.5, round(9.5 - xr, 2), fs=8, gap=0.06)],
        "The chapter downloads the audio of a YouTube video. This deck cannot do that for a reason that is not technical: the Terms of Service of YouTube do not allow downloading any part of the service or its content except as expressly authorized, so the study downloaded a public-domain LibriVox reading from the Internet Archive instead, and this deck does the same. "
        "download() returned 0 and left downloaded_content.m4a, an AAC stream of 100.3 seconds, converted by ffmpeg from a 64 kbit/s mp3 of 100.4 seconds. "
        "A string in place of a list was accepted, as the research found, which is a leniency and not a promise; an address that is nowhere raised DownloadError with HTTP Error 404. "
        "The options dictionary names the output template, the format and a postprocessor that extracts the audio as m4a, so the conversion needs ffmpeg, the tool of slide 14. "
        "The YouTube download itself, and every other site the supported-sites list names, was NOT EXECUTED, and the research recorded what happens without ffmpeg.",
        "Download only what you are allowed to, and keep ffmpeg installed.", notexec=True, recorded=True)

# ---- 20 a guessing game that speaks --------------------------------------------------------------------------------------------
pn = "guessCut_v1_0_0.py"
c20, t20, bot20, xr20, wr20, a20, b20 = sbs(pn, 0.5, 1.55, 5.0, hmax=3.4)
content("A guessing game that speaks", "The engine is passed in, so a test can use a recorder and the game can write WAV files",
        [c20, t20,
         *stack([SAY_NS, hid(pn, a20, b20, "imports, helpers and the work folder"),
                 rec("listing 16 of the chapter calls speak(), which no listing defines, and raised NameError in every row; a guessing game with its own speak() said 4 lines in 3 guesses.")],
                xr20, round(t20["y"] + t20["h"] + 0.08, 2), wr20, fs=8, gap=0.05)],
        "The first practice program of the chapter asks for a guessing game that speaks. The chapter's listing 16 calls speak(), which no listing defines, and it raised NameError in every environment the research tried, so the program of the slide defines its own. "
        "The idea is to pass the engine into the game. make_speak() builds a speak() that prints the text and then says it, and game() takes speak as a parameter, so a test can pass a Recorder, a stand-in engine that only keeps the lines, and the real game can pass a Writer, an engine whose say() saves each line to a WAV file. "
        "With the Recorder the game said 4 lines in 3 guesses and the second line was 10 is too low; with the Writer the same 4 lines were written to line1.wav to line4.wav. "
        "The lengths of the four files depend on the text: with the longer sentences of the research they were 2.56, 1.94, 1.95 and 2.5 seconds, and the shorter sentences of this program give the lengths the transcript prints. "
        "Nothing is spoken aloud, and the point of the exercise is that a program which takes its engine as an argument can be tested without a loudspeaker.",
        "Pass the engine in; a test needs no loudspeaker.", recorded=True)

# ---- 21 99 bottles of beer ----------------------------------------------------------------------------------------------------
pn = "songCut_v1_0_0.py"
n21 = len(cut(pn))
c21, t21, bot21, xr21, wr21, a21, b21 = sbs(pn, 0.5, 1.55, 5.0, b=n21 - 1, hmax=3.45, hi=7.5)
im21, ib21, _ = img("song.png", xr21, round(t21["y"] + t21["h"] + 0.05, 2), wr21, 0.45)
content("99 bottles of beer", "99 verses make 396 lines, 2,377 words and 11.7 minutes of audio (30.8 MB)",
        [c21, t21, im21, imgcap(["song.png"], xr21, round(ib21 + 0.02, 2), wr21, fs=8),
         foot(SAY_NS + " " + hid(pn, a21, b21, "imports, helpers and the work folder", "the picture"), xr21, round(ib21 + 0.26, 2), wr21, fs=8)],
        story_notes("DaisyBell1961") + " The second practice program asks for the song of 99 bottles of beer, sung by the engine. "
        "bottles() and verse() write the verse for a number, with 1 bottle in the singular and No more bottles at the end, and the program prints the verses for 2 and for 1. "
        "The whole song is 99 verses, 396 lines, 2,377 words and 11,457 characters. The engine writes the first 3 verses as 18.3 seconds of audio and the 99 verses as 699.3 seconds, 11.7 minutes, and 30.8 MB of WAV; in the research the same 99 verses took 7.5 seconds of work. "
        "The picture is the waveform of the 3-verse file. The research also asked tiny to transcribe the 3 verses and got a word error rate of 0.9589, nearly every word wrong. "
        "The sentence of the chapter, that the program takes a long time, is true of the audio and not of the work: the audio is 11.7 minutes long and it is made in seconds. All of these are single runs.",
        "A song is just text; the engine turns 99 verses into 11.7 minutes.")

# ---- 22 the transcriber loop ----------------------------------------------------------------------------------------------------
pn = "loopCut_v1_0_0.py"
p22, bot22, a22, b22, x22, w22 = pfit(pn, 0.5, 1.55, 5.5, 3.42)
xr = round(x22 + w22 + 0.2, 2)
dg, dcap = diagram("TheLoopOfTheTranscriber", "sequence", (xr, 1.4, round(9.5 - xr, 2), 2.5), fs=8, head_w=0.85, gap0=0.3, hfs=8)
content("The transcriber loop", "One function downloads, transcribes and writes subtitles; a bad address stops the list",
        [p22, dg, dcap,
         foot(SAY_AI + " " + hid(pn, a22, b22, "imports and helpers, among them audio_opts, the options of slide 19"), xr, round(dcap["y"] + dcap["h"] + 0.06, 2), round(9.5 - xr, 2), fs=7.5)],
        "The third practice program asks for a function that takes a list of addresses, downloads the audio of each, transcribes it and writes subtitle files. The sequence diagram is that loop: the script calls download() with the address, yt-dlp returns the audio file, the script calls transcribe() on it, Whisper returns the result, and the writers write an SRT, a VTT and a TXT file. "
        "The program runs it on two public-domain LibriVox readings of the Gettysburg Address on archive.org, which stand in for YouTube: the first gave 26 segments and 312 words, the second 17 segments and 304 words, and each left an m4a, an SRT, a VTT and a TXT file. "
        "The research timed the loop at 47.8 seconds for the two readings. The last lines pass an address that is nowhere: the function raises DownloadError, and since nothing in the loop catches it, one bad address stops the whole list. A version that caught the error and went on to the next address is the obvious improvement. "
        "The options dictionary of slide 19 is held in a helper here so that the function fits the slide, and the hidden lines say so.",
        "One bad address stops the loop unless the loop catches it.")

# ---- 23 the chapter replayed ----------------------------------------------------------------------------------------------------
tbl23 = {"t": "table", "x": 0.5, "y": 1.45, "w": 9.0, "colW": [1.2, 0.9, 0.9, 1.4, 0.8, 2.2, 1.6], "fs": 8, "rowH": 0.26, "rows": EX["_tables"]["configurations"]["rows"]}
content("The chapter replayed in four environments", "Recorded: how many of the 46 printed statements match the book, by environment",
        [tbl23,
         foot("Each cell counts the 46 statements of the chapter's 17 listings; the 3 statements that were not executed (the two downloads from YouTube and the lyrics) are in neither count.", 0.5, 2.9, 9.0, fs=8.5),
         card("Recorded 14 Oct 2026", "The 17 listings were parsed into 45 statements, 46 with the one that was substituted, and replayed as printed. What differs is the Voice objects and names, the Audio saved to line, the transcription of hello.wav, the TSV listing and the call of speak. One program ran under 11 interpreters, 3.11 to 3.15.0b4, and compared 14 items: only 2 differed, the modules PEP 594 removed.",
              0.5, 3.3, 4.4, 1.65, fs=8.5, accent="slate"),
         card("NOT EXECUTED here", "SAPI5, NSSpeechSynthesizer and AVSpeech; a microphone; a GPU; the OpenAI, Google Cloud and Azure speech services; faster-whisper, whisper.cpp, SpeechRecognition, gTTS and Vosk (their pages were read); Whisper medium, turbo and large-v3; and any download from YouTube.",
              5.1, 3.3, 4.4, 1.65, fs=8.5, accent="orange")],
        "The table is the research's record of the chapter's statements replayed as printed, and the deck check computes every cell again from the record. With Python 3.14.6 and the newest packages 34 of the 46 matched the book and 42 ran without an exception; the pinned set, Python 3.12.3 with pyttsx3 2.98 and openai-whisper 20231117, gave 35 and 42; in the empty environment 8 matched and 8 ran; without ffmpeg 32 matched and 38 ran. "
        "The statements that differ are the Voice objects and names, the line Audio saved to that the driver prints, the transcription of hello.wav, the TSV listing and the call of speak. "
        "One program that saves speech, lists voices and asks yt-dlp questions ran under 11 interpreters, 3.11, 3.12, 3.13, 3.14.0 to 3.14.6 and 3.15.0b4, and compared 14 items. Only 2 differed, both about aifc, audioop, sunau, chunk and sndhdr, which import under 3.11 and 3.12 and fail from 3.13, while wave, which pyttsx3 uses, stayed; the Whisper version compared 16 items and 2 differed, only in the printed form of a type. "
        "Appendix B of the book gives 7 answers for the chapter. The research confirmed that pyttsx3 and Whisper need no internet once the tiny model is on disk, and found that answer 5 is wrong about the default model: load_model has no default for the name, and the whisper command defaults to turbo in 20250625 and to small in 20231117. "
        "The photograph of the stories was not fetched, because the request to Wikimedia answered 429.",
        "The same book gives 8 to 35 matching statements, by environment.", notexec=True, recorded=True)

# ---- 24 summary: the mind map ----------------------------------------------------------------------------------------------------
dg, dcap = diagram("TextToSpeechAndSpeechRecognitionAtAGlance", "mindmap", (0.5, 1.4, 9.0, 3.2), fs=9, root_w=2.0)
content("The chapter in one map", "Six branches; the slides of each branch hold the examples",
        [dg, dcap],
        "These six branches are the route of the deck. The text-to-speech engine: pyttsx3 queues text with say(), runAndWait() processes the queue, and the rate and the volume are properties; on slide 7 the rate still read 200 after it was set to 300 until runAndWait() had run. "
        "Saved speech and recognition: save_to_file() writes a WAV file, Whisper needs ffmpeg, and the models differ in size and time; slide 12 sets the book's table beside this machine. "
        "Subtitle files: the writers make SRT, VTT and TSV files, the times are on a grid of 0.02 seconds, and the word error rate measures accuracy. Downloading videos: yt-dlp downloads audio, the terms of the site limit downloading, and downloaders change with the releases, so 5 of 6 recent yt-dlp releases ran. "
        "Practice programs: the guessing game speaks, the song has 99 verses, and the transcriber loop stops at a bad address. Environment and evidence: the study ran Python 3.14.6, Windows and macOS were not executed, and every number is from a single run. "
        "Together they answer the first question of the chapter, what can be shown to work without a sound card, a microphone or a GPU and what can only be shown to fail, and the slides that say where a printed line differs answer the second. The map is drawn from the same specification as the interactive page.",
        "If a branch feels unproven, its slides hold the example.")

# ---- 25 resources ------------------------------------------------------------------------------------------------------------------------------------------------------------------
PUB = {p[0]: p for p in RD.PUBS}
_read = [["The textbook, chapter 24 - free online", PUB["P01"][2]],
         ["Appendix A: installing third-party modules", PUB["P05"][2]],
         ["Online materials of the 3rd edition (zip)", PUB["P02"][2]]]
_ref = [["pyttsx3 on PyPI", "https://pypi.org/project/pyttsx3/"],
        ["Whisper README (OpenAI)", PUB["P29"][2]],
        ["yt-dlp: README, with embedding in Python", PUB["P41"][2]],
        ["WebVTT: the Web Video Text Tracks Format (W3C)", PUB["P46"][2]],
        ["wave: the WAV module, Python 3.14 documentation", PUB["P08"][2]]]
_hist = [["Speech synthesis (Wikipedia)", STORY["Voder1939"]["link"]],
         ["Speech recognition (Wikipedia)", STORY["Audrey1952"]["link"]],
         ["Daisy Bell (Wikipedia)", STORY["DaisyBell1961"]["link"]],
         ["eSpeak (Wikipedia)", STORY["ESpeak1995"]["link"]],
         ["SubRip (Wikipedia)", STORY["SubRip2000"]["link"]],
         ["Whisper, the speech recognition system (Wikipedia)", STORY["Whisper2022"]["link"]]]
LINKS = [r[1] for r in _read + _ref + _hist]
json.dump({"_version": __version__, "links": LINKS}, open(os.path.join(HERE, "links_v1_0_0.json"), "w"), indent=1)
content("Where to go from here", "Every link was opened on the day this deck was made",
        [{"t": "links", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.55, "fs": 9, "groups": [
            {"head": "Stories", "rows": _hist}, {"head": "Read", "rows": _read}, {"head": "Reference", "rows": _ref}]}],
        "Every link on this slide was opened on the day the deck was made, and the build records the status each answered. The textbook chapter is free to read online and holds every listing of the chapter; the online materials are the zip of 91 files, and Appendix A is where the book installs third-party packages. "
        "The reference links are the PyPI page of pyttsx3, the README of Whisper, the README of yt-dlp with its section on embedding the downloader in Python, the specification of WebVTT and the documentation of the wave module. "
        "The six stories of the chapter have their own link, and their pages are the first group. "
        "The research package holds %d sources in all, among them the source of the eSpeak driver of pyttsx3, the PyPI metadata of the three packages, the paper Robust Speech Recognition via Large-Scale Weak Supervision, the supported-sites list of yt-dlp and the Terms of Service of YouTube. "
        "The book recommends Make Python Talk by Liu for more on speech. No photograph of a person is used in the deck." % len(RD.PUBS),
        "Textbook, documentation, and history, all opened today.")

# ---- 26 closing ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
content("What you should now be able to say", "Four claims, each carried by a result you saw printed",
        [{"t": "bullets", "x": 0.6, "y": 1.5, "w": 8.8, "h": 2.4, "fs": 15, "items": [
            "say() only queues; runAndWait() speaks, and the file is complete only after you wait for it.",
            "Appendix A's pinned pyttsx3 saves 0.6 s where the newest saves 1.54 s; test the pin.",
            "Whisper needs ffmpeg, and its models above small did not run here.",
            "A download from YouTube is not allowed, so a public-domain reading stood in for it."]},
         {"t": "chips", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.6, "fs": 10, "big": False,
          "items": ["%d console rows" % ROWS_SHOWN, "%d programs run" % len(PROGS), "%d diagrams" % len(DIAG), "%d pictures" % len(EX["_images"])]}],
        "Four claims, each carried by a result you saw printed. If you can say them in your own words and run the examples yourself, you have the chapter. The programs need pyttsx3, openai-whisper and yt-dlp, with eSpeak NG and ffmpeg installed by the package manager of the system, and a work folder they can fill with WAV files. "
        "The rows were run again under Python 3.14.6 each time the deck was built, and the programs, and with them the pictures, were run again by the check that compares the slides with the recording. "
        "What was not run is marked on its slide: SAPI5, NSSpeechSynthesizer and AVSpeech, a microphone, a GPU, the cloud services, a download from YouTube, and the Whisper models medium, turbo and large-v3. "
        "Nothing was ever heard. Every count and time in this deck from a single run is a single run, and not a benchmark. The next chapter of the book moves on, and what this chapter taught about checking what a program writes carries over.",
        "Questions are welcome; bring a script to try.")

# ---- agenda ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
_t = {s["title"]: i + 1 for i, s in enumerate(S)}
_parts = [("What a script can do", "What a script can do with the engines", "The pinned release and the newest"),
          ("Speaking text", "say() only queues the text", "A call that never returns"),
          ("Recognising speech", "The Whisper models", "Languages and what Whisper hears"),
          ("Subtitles and downloading", "Subtitle files: SRT, VTT and TSV", "Downloading audio"),
          ("Practice and the replay", "A guessing game that speaks", "The chapter replayed in four environments"),
          ("Summary and resources", "The chapter in one map", "Where to go from here")]
_rows = ["%s (slides %d-%d)" % (name, _t[a], _t[b]) for name, a, b in _parts]
_ends = [_t[b] for _, _, b in _parts]
_starts = [_t[a] for _, a, _ in _parts]
if _starts[0] != 4 or any(_starts[i + 1] != _ends[i] + 1 for i in range(len(_parts) - 1)) or _ends[-1] != len(S) - 1:
    raise SystemExit("REFUSED: agenda ranges are not contiguous: %r %r (len S=%d)" % (_starts, _ends, len(S)))
_nstory = sum(1 for s in S for i in s["items"] if i.get("t") == "factrow")
_npic = sum(1 for s in S for i in s["items"] if i.get("t") == "img")
S[1]["items"] = [
    {"t": "numlist", "x": 0.5, "y": 1.4, "w": 6.3, "h": 3.55, "fs": 11.5, "items": _rows},
    {"t": "stat", "x": 7.05, "y": 1.5, "w": 2.45, "h": 3.4, "vert": True, "items": [
        {"n": str(len(S)), "label": "slides, numbered bottom-right"},
        {"n": "%d + %d" % (_nstory, len(ST.STORIES) - _nstory), "label": "true stories: %d on slides, %d in the notes" % (_nstory, len(ST.STORIES) - _nstory)},
        {"n": str(_npic), "label": "pictures, each saved by a program that is run again"}]}]
S[1]["sub"] = "Six parts; every range is a run of slides you can jump to"
S[1]["take"] = "Six parts, from what a script can do to a map."
S[1]["notes"] = ("The route has six parts. It starts with what a script can do: the seven uses of the engines, the packages and tools they need, and the pinned release of pyttsx3 against the newest. "
                 "Then speaking text: say() only queues, the voices, the rate and the volume, the WAV file, and the calls that never return. The third part is recognising speech: the Whisper models and Table 24-1, transcribing a sentence, ffmpeg, and the languages Whisper hears. "
                 "The fourth is subtitles and downloading: the SRT, VTT and TSV files, the writer options and the time grid, the metadata of a video and the download of its audio. "
                 "The fifth is practice and the replay: the guessing game that speaks, the 99 bottles of beer, the transcriber loop, and the chapter replayed in four environments. "
                 "The last part is a one-map summary and the resources. The ranges name the exact slides, so you can return to the part you need. Four of the six stories are on slides and two are told in the notes, each with a link; the seven narrative diagrams of the chapter are drawn from the same specifications as the interactive page. "
                 "Every output was printed by Python %s with pyttsx3 2.99, openai-whisper 20250625 and yt-dlp 2026.8.19, nothing is heard, and what could not be run is marked on its slide." % PYV)

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
_pics = [i["path"].split("/")[-1] for s in S for i in s["items"] if i.get("t") == "img"]
if sorted(_pics) != sorted(EX["_images"]):
    raise SystemExit("REFUSED: pictures on slides %r differ from the recording %r" % (sorted(_pics), sorted(EX["_images"])))
plan = {"meta": {"title": "Ch. 24: Speech Engines", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": len(S), "diagrams": SHOWN, "notExecuted": NOTEXEC, "recorded": RECORDED,
                 "standin": {str(k): v for k, v in STANDIN.items()}}, "slides": S}
if LATE:
    raise SystemExit("REFUSED:\n" + "\n".join(LATE))
out = os.path.join(HERE, "deck_plan_v1_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides; diagrams on slides", dict(sorted(SHOWN.items(), key=lambda kv: kv[1])), "; NOT EXECUTED on slides", NOTEXEC, "; Recorded on slides", RECORDED)

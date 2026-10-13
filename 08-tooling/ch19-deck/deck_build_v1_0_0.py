#!/usr/bin/env python3
"""Builds deck_plan_v1_0_0.json - SEN0414 chapter 19 (Keeping Time, Scheduling Tasks, and Launching Programs) on the CME classroom standard.

Same regime as chapters 10 to 18: numbered warm-ivory slides, an agenda with exact slide ranges, a summary before the resources,
full-sentence takeaway strips, stories with fact rows, consoles and whole programs (or honest excerpts of them, labelled with their
line numbers) with their results as Python printed them. Every console result and program transcript comes from
examples_out_v1_0_0.json (made by examples_run_v1_0_0.py under Python 3.14.6 with tzdata 2026.5 and schedule 1.2.2; time, datetime,
zoneinfo, subprocess, signal, threading, sched, asyncio and calendar are the standard library); the speaker notes are prose for the
reader and carry only what the chapter's RDODI research package (03-materials/ch19/rdodi, sen0414_ch19_rdodi_data_v1_0_5.py, findings
F1 to F18), its records (08-tooling/ch19-page/*.json) or a program of this deck established.

What this chapter adds against chapter 18: the subject is the clock, so NOTHING ON A SLIDE READS IT. A console row never calls now(): every
moment is built from numbers and every zone is named, so the deck check can run every row and program again on any day and compare text. The
two places where a program needs a clock or a person (the stopwatch, the countdown) and the one that needs a scheduler's clock (sched) run on a
clock the program moves, and the slide says EMULATED, as honesty_check_v1_0_0.py requires. What the research recorded on a day (the real
cron runs, the public pages) is on a slide as 'recorded 13 Oct 2026' and is not re-run. What could not be run is marked NOT EXECUTED on its
slide: Python 3.15.0 final and 3.14.7 or later (slide 13), Windows, macOS and a desktop (slide 19), Task Scheduler, launchd and a systemd
timer (slide 21), and the sound (slide 22). The measured numbers of the research (slide 9) say 'single run'. The eight narrative diagrams
of the chapter (sen0414_ch19_diagrams_v1_0_0.py, grounding 0.84 or more) are drawn as native shapes (diagram_shapes_v1_0_0.py, with a
branching state diagram added for the launched process) and checked by diagram_check_v1_0_0.py; two tables (Table 19-1, the two-digit
year) and one chart (the 13th by weekday over 400 years) are native PowerPoint objects whose data the deck check computes again; no
photograph is used (the research used none for this chapter); two of the six stories are slides (the epoch, the Gregorian calendar) and
four are told in the notes.

Usage: python3 deck_build_v1_0_0.py   (writes deck_plan_v1_0_0.json and links_v1_0_0.json beside itself; needs rdflib)
"""
__version__ = "1.0.0"
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import diagram_shapes_v1_0_0 as DS


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ST = load("stories19", os.path.join(HERE, "..", "sen0414_ch19_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
DG = load("diagrams19", os.path.join(HERE, "..", "sen0414_ch19_diagrams_v1_0_0.py"))
NODES = DG.nodes_from_ttl(os.path.join(HERE, "..", ".."))
_bad = DG.run_checks(NODES)
if _bad:
    raise SystemExit("REFUSED: the diagrams fail their own checks: %r" % _bad[:3])
DIAG = {d["id"]: d for d in DG.DIAGRAMS}
RD = load("rdodi19", os.path.join(HERE, "..", "sen0414_ch19_rdodi_data_v1_0_5.py"))
EX = json.load(open(os.path.join(HERE, "examples_out_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s, tzdata %s; no row reads the clock" % (PYV, EX["_packages"].split(" | ")[1].split()[1])
G = {k: [[s, (o or "")] for s, o in v] for k, v in EX.items() if not k.startswith("_")}
PROGS = EX["_programs"]
CQ1, CQ2 = RD.CQS
CW = 0.0088  # inches per character per point of Courier New, as the shared fit check measures it

# the honesty lines (honesty_check_v1_0_0.py requires 'EMULATED' on every slide that shows an emulation, 'single run' on every slide that
# shows a measured time and 'NOT EXECUTED' on every slide the plan lists, and on no other)
L_NOTEXEC = "NOT EXECUTED"
L_ONCE = "single run"
L_EMU = "EMULATED"


def lines_of(rows):
    return sum(1 + (1 if out.strip() else 0) for _, out in rows)


def con(group, x, y, w, fs=11, label=None, cap=True, rows=None):
    """A console panel sized from its rows; returns (item, bottom y)."""
    rr = rows if rows is not None else G[group]
    maxlen = max(max(len(st) + 4, len(out)) for st, out in rr)
    fs = min(fs, round((w - 0.4) / (maxlen * CW), 1))
    if fs < 7:
        raise SystemExit("REFUSED: console %s cannot fit unwrapped in %.1f in (fs %.1f)" % (group, w, fs))
    L = lines_of(rr)
    h = round(L * fs * 1.23 / 72.0 + 0.36 + 0.02 * max(0, L - 1), 2)
    it = {"t": "code", "x": x, "y": y, "w": w, "h": h, "rows": rr, "fs": fs}
    if cap:
        it["cap"] = CAP
    if label:
        if len(label) > (w - 0.1) / 0.0725:
            raise SystemExit("REFUSED: label %r is too long for a %.1f in panel" % (label, w))
        it["label"] = label
    return it, round(y + h + (0.26 if cap else 0), 2)


def span(pname, first, last=None, after=None):
    """1-based line numbers (a, b) of the program lines from the first containing `first` to the first containing `last`."""
    ls = PROGS[pname]["code"].rstrip("\n").split("\n")
    a = next(i for i, l in enumerate(ls, 1) if first in l)
    b = len(ls) if last is None else next(i for i, l in enumerate(ls, 1) if i >= a and last in l)
    return a, b


def pw(pname, lines=None, out=True, fs=7.0):
    """The panel width a program excerpt (and, when asked, its transcript inside the panel) needs at fs points."""
    pr = PROGS[pname]
    L = pr["code"].rstrip("\n").split("\n")
    a, b = (1, len(L)) if lines is None else lines
    ws = [len(l) for l in L[a - 1:b]]
    if out and pr["transcript"]:
        t = pr["transcript"].split("\n")
        ws += [len(t[0]) + 7] + [len(x) for x in t[1:]]
    return round(max(ws) * CW * fs + 0.4, 2)


def bestfs(pname, lines, wmax, hmax, out=True, lo=7.0, hi=9.5):
    """The largest font size (a multiple of 0.5 between lo and hi) at which an excerpt and its transcript fit unwrapped in wmax inches
    and hmax inches; the slide then uses it, so that a program is as large as its slide allows."""
    pr = PROGS[pname]
    L = pr["code"].rstrip("\n").split("\n")
    a, b = lines
    n = (b - a + 1) + (pr["transcript"].count("\n") + 1 if out and pr["transcript"] else 0)
    fs = hi
    while fs >= lo:
        if pw(pname, lines, out, fs) <= wmax and n * (fs * 1.22 / 72.0 + 0.02) + 0.30 <= hmax:
            return fs
        fs -= 0.5
    raise SystemExit("REFUSED: %s lines %d-%d do not fit %.2f x %.2f in at %.1f pt" % (pname, a, b, wmax, hmax, lo))


def prog(pname, x, y, w, fs=7.0, lines=None, show_out=True):
    """A chapter program (or an honest excerpt) with its transcript, sized from its text; returns (item, bottom y).
    The excerpt is a verbatim slice and the label above the panel names it ('program <name>, lines a to b of n'), as
    program_check_v1_0_0.py verifies. The transcript, when shown, sits in the same panel."""
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


def transcript(pname, x, y, w, fs=7.0, label=None, aligned=False):
    """The transcript of a program in a panel of its own. With a label of the form 'transcript of program <name>' the panel is
    re-run by program_check and must equal the recording."""
    label = label or "transcript of program %s" % pname
    out = PROGS[pname]["transcript"]
    t = out.split("\n")
    need = round(max([len(t[0]) + 7] + [len(z) for z in t[1:]]) * CW * fs + 0.4, 2)
    if need > w + 0.005:
        raise SystemExit("REFUSED: transcript of %s cannot fit unwrapped in %.2f in at %.1f pt (needs %.2f)" % (pname, w, fs, need))
    if len(label) > (w - 0.1) / 0.0725:
        raise SystemExit("REFUSED: label %r is too long for a %.2f in panel" % (label, w))
    L = len(t) + (1 if aligned else 0)
    h = round(L * (fs * 1.22 / 72.0 + 0.02) + 0.30, 2)
    # aligned: the word 'prints' stands on a line of its own, so that the columns of the transcript line up from its first line on
    return {"t": "prog", "x": x, "y": y, "w": w, "h": h, "lines": [], "fs": fs, "compact": True, "out": ("\n" + out) if aligned else out,
            "outLabel": "prints", "label": label}


def factrow(sid, x=0.5, y=4.42, w=9.0):
    st = STORY[sid]
    host = st["link"].split("//")[1].split("/")[0].replace("www.", "")
    return {"t": "factrow", "x": x, "y": y, "w": w, "who": st["who"], "where": st["where"],
            "when": st["when"], "link": st["link"], "linkText": host}


def story_notes(sid):
    st = STORY[sid]
    return st["story"] + " The account rests on these sources. " + st["source"]


def card(head, body, x, y, w, h, fs=11.5, accent=None):
    if len(head) > (w - 0.4) / 0.112:
        raise SystemExit("REFUSED: card heading %r does not fit one line of a %.2f in card" % (head, w))
    it = {"t": "card", "head": head, "body": body, "x": x, "y": y, "w": w, "h": h, "fs": fs}
    if accent:
        it["accent"] = accent
    return it


def foot(body, x, y, w, fs=9.5):
    h = round(DS.need_h(body, w, fs) + 0.04, 2)
    return {"t": "foot", "x": x, "y": y, "w": w, "h": h, "fs": fs, "body": body}


def diagram(did, kind, box, **kw):
    """The shapes item of a narrative diagram and its caption (which names the diagram and its measured grounding)."""
    d = DIAG[did]
    fn = {"activity": DS.activity, "sequence": DS.sequence, "states": DS.states5, "lifecycle": DS.lifecycle_col, "lifecycle_skip": DS.lifecycle_skip, "lifecycle_branch": DS.lifecycle_branch, "usecases": DS.usecases, "mindmap": DS.mindmap}[kind]
    it = fn(d["data"], box, **kw)
    h, n = d["grounding"]
    body = "diagram %s - %s pattern, %d of %d words grounded in the chapter's text" % (did, d["pattern"], h, n)
    cap = {"t": "foot", "x": box[0], "y": round(box[1] + box[3] + 0.03, 2), "w": box[2], "h": round(DS.need_h(body, box[2], 8.5) + 0.04, 2), "fs": 8.5,
           "body": body}
    it["did"] = did
    return it, cap





def pair(pname, lines, x, y, wtot, hmax, gap=0.2, lo=7.0, hi=9.0, label=None):
    """A program excerpt (no transcript inside) with its transcript in a panel beside it, at the largest font size at which both fit
    unwrapped in wtot inches and hmax inches; returns (code item, transcript item, bottom y)."""
    pr = PROGS[pname]
    a, b = lines
    t = pr["transcript"].split("\n")
    fs = hi
    while fs >= lo:
        wc = pw(pname, lines, False, fs)
        wc = max(wc, round(len('program %s, lines %d to %d of %d' % (pname, a, b, len(pr['code'].rstrip().split('\n')))) * 0.0725 + 0.12, 2))
        wt = round(max([len(t[0]) + 7] + [len(z) for z in t[1:]]) * CW * fs + 0.4, 2)
        hc = (b - a + 1) * (fs * 1.22 / 72.0 + 0.02) + 0.30
        ht = len(t) * (fs * 1.22 / 72.0 + 0.02) + 0.30
        if wc + gap + wt <= wtot and max(hc, ht) <= hmax:
            c, bot = prog(pname, x, y, wc, fs=fs, lines=lines, show_out=False)
            tr = transcript(pname, round(x + wc + gap, 2), y, wt, fs=fs)
            return c, tr, max(bot, round(y + tr["h"], 2))
        fs -= 0.5
    raise SystemExit("REFUSED: %s lines %d-%d and their transcript do not fit %.2f x %.2f in side by side at %.1f pt" % (pname, a, b, wtot, hmax, lo))

S = []
SHOWN = {}  # diagram id -> slide number
NOTEXEC = []  # slide numbers that carry the words NOT EXECUTED
MEASURED = []  # slide numbers that show a measured time (and say 'single run')
EMULATED = []  # slide numbers that show an emulation (a Python object standing in for Windows) and say EMULATED


def content(title, sub, items, notes, take, lede=None, notexec=False, measured=False, emulated=False):
    if lede and len(lede.split()) > 34:
        raise SystemExit("REFUSED: lede on %r runs past the gate" % title)
    if len(take.split()) > 24 or not take.endswith("."):
        raise SystemExit("REFUSED: takeaway %r is not a short full sentence" % take)
    if len(title) > 44:
        raise SystemExit("REFUSED: title %r is longer than the 44 characters one line of it holds" % title)
    if len(sub) > 86:
        raise SystemExit("REFUSED: subtitle %r is longer than the 86 characters one line of it holds" % sub)
    for it in items:
        if it["t"] in ("code", "prog", "shapes", "card", "boxes", "chips", "stat", "beats", "factrow", "numlist", "bullets", "links", "foot", "text", "img", "table", "chart"):
            if it["y"] + it.get("h", 0.4) + (0.26 if it.get("cap") and it["t"] == "code" else 0) > 5.0 or it["x"] + it["w"] > 9.56:
                raise SystemExit("REFUSED: item %s on %r reaches y %.2f / x %.2f" % (it["t"], title, it["y"] + it.get("h", 0.4), it["x"] + it["w"]))
        if it["t"] == "shapes":
            SHOWN[it["did"]] = len(S) + 1
    blob = json.dumps(items)
    if notexec:
        NOTEXEC.append(len(S) + 1)
        if L_NOTEXEC not in blob:
            raise SystemExit("REFUSED: slide %r is declared NOT EXECUTED but says nothing of it" % title)
    if emulated:
        EMULATED.append(len(S) + 1)
        if L_EMU not in blob:
            raise SystemExit("REFUSED: slide %r is declared EMULATED but says nothing of it" % title)
    if measured:
        MEASURED.append(len(S) + 1)
        if L_ONCE not in blob.lower():
            raise SystemExit("REFUSED: slide %r shows a measured time but does not say 'single run'" % title)
    sl = {"kind": "content", "title": title, "sub": sub, "items": items, "notes": notes, "take": take, "bg": "light"}
    if lede:
        sl["lede"] = lede
    S.append(sl)


def hidden(pname, a):
    """The words that say where the lines before the excerpt are: lines 1 to a-1 of the program, the corpus HEAD and a comment."""
    return "Lines 1 to %d (imports, a temporary folder and a comment) are not shown." % (a - 1)

# ---- 1 title ---------------------------------------------------------------------------------------------------
c1, _ = con("title", 5.0, 0.4, 4.5, fs=10, cap=False)
S.append({"kind": "title", "title": "Ch. 19: Time, Tasks, and Programs",
          "sub": "Keeping time, scheduling tasks, and launching programs: time, datetime, zoneinfo, subprocess, and cron",
          "items": [c1, foot("Every output on these slides was printed by the Python above when the deck was made. No slide reads the clock: moments are built from numbers and zones are named. What could not be run is marked on its slide.", 0.6, 3.85, 8.8, fs=11)],
          "notes": "Chapter 18 worked with files that programs read and write. Chapter 19 turns to time and to other programs: how a program reads a clock, waits, writes and reads dates, and how it starts, "
                   "stops and schedules another program. This deck follows the chapter in its own order: the time module with the epoch timestamp and sleep and Project 14, the Super Stopwatch; the "
                   "datetime module with moments, durations, strftime() and strptime(); launching programs with subprocess.run() and subprocess.Popen(), the start and open commands and the scheduler "
                   "paragraph; and Project 15, the Simple Countdown, with the two practice programs. It adds what the chapter leaves out and what the research found when every printed output was run again: "
                   "four en dashes that make listings a SyntaxError, a profiling listing that does not match the file the book ships, a time zone named Pacific Standard Time on a day when it was Pacific Daylight Time, "
                   "a two-digit year that maps 69 to 1969, thirty years that are seven days short, time zones and daylight saving, the utcnow() deprecation, the commands of Windows and macOS that Linux lacks, "
                   "and what real cron did on a real machine. Everything printed on these slides was produced by Python 3.14.6, installed with uv, with tzdata 2026.5 and schedule 1.2.2; time, datetime, zoneinfo and "
                   "subprocess are the standard library. Nothing on a slide depends on the time of day: every moment is built from numbers, every zone is named, and the stopwatch and countdown run on a clock the program moves. "
                   "What could not be run, a Windows computer, a Mac, a systemd timer, a sound card and the final release of Python 3.15, is marked NOT EXECUTED on its slide.",
          "bg": "light"})

# ---- 2 agenda (filled in at the end) -------------------------------------------------------------------------------
S.append({"kind": "content", "title": "Today's route", "sub": "", "items": [], "notes": "", "take": "", "bg": "light"})

# ---- 3 questions ------------------------------------------------------------------------------------------------
content("The questions this chapter answers", "The chapter's own competency questions; the summary comes back to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 2.2, "fs": 13, "items": [CQ1, CQ2]},
         {"t": "chips", "x": 0.5, "y": 3.8, "w": 9.0, "h": 0.5, "fs": 10,
          "items": ["6 branches", "%d topics" % len(NODES), "%d console rows" % sum(len(v) for v in G.values()),
                    "%d programs run" % len(PROGS), "8 diagrams", "Python %s" % PYV, "tzdata 2026.5", "schedule 1.2.2"]}],
        "The first question is the spine of the chapter. A program can read several clocks, and they answer different questions: time.time() answers what moment is it, time.monotonic() answers how long did this take. "
        "A datetime holds a moment and a timedelta a duration, and both refuse or misread things: a timedelta has no months, a two-digit year maps 69 to 1969, a value with no zone cannot be compared with one that has a zone, "
        "and a day added across a daylight saving change is 23 hours long. A program launches another program with a list of arguments through subprocess.run(), which waits, or subprocess.Popen(), which does not, and it "
        "schedules a program either inside a process that stays alive or with the operating system, where the commands of the book, start and open, may not exist. The second question is the watch-out of the deck. "
        "The chapter page of 13 October 2026 has 29 listings, 20 of them interactive sessions of 75 statements, one figure and one table. All 75 statements were replayed in order under Python 3.14.6 with the zone of the author, "
        "America/Los_Angeles: 54 printed what the book prints and 21 did not, of which 7 depend on the clock, 1 is the en dash and 13 launch Windows or macOS programs or call a program that Linux lacks; with the dash repaired 55 matched. "
        "The online materials of the book, 91 files, hold three files of this chapter, calcProd.py, stopwatch.py and simplecountdown.py, and none of the alarm.wav, the hello.txt or the practice programs. Each slide says where a printed line differs and on what evidence.",
        "Know which clock, which moment and which launcher answers each question.")

# ---- 4 the epoch timestamp ---------------------------------------------------------------------------------------
pn = "epochCut_v1_0_0.py"
a4, b4 = span(pn, "t = calendar.timegm")
f4 = bestfs(pn, (a4, b4), 4.95, 3.0)
w4 = pw(pn, (a4, b4), True, f4)
p4, bot4 = prog(pn, 0.5, 1.55, w4, fs=f4, lines=(a4, b4), show_out=True)
x4 = round(0.5 + w4 + 0.25, 2)
content("The epoch timestamp", "Seconds since 1 January 1970 UTC; a leap second has no number; 32 bits end in 2038",
        [p4,
         card("What the number counts", "Seconds since 00:00:00 UTC on 1 January 1970, by a formula that gives every day 86,400 seconds, so a leap second has no number of its own.",
              x4, 1.5, round(9.5 - x4, 2), 1.75, fs=9.5, accent="slate"),
         card("Where it stops", "A signed 32-bit count ends at 03:14:07 UTC on 19 January 2038; Python's datetime reaches the year 9999.",
              x4, 3.35, round(9.5 - x4, 2), 1.45, fs=9.5, accent="orange"),
         foot(hidden(pn, a4), 0.5, round(bot4 + 0.08, 2), w4, fs=8.5)],
        "The chapter says the epoch timestamp is the number of seconds since the epoch, a reference moment that many date and time programs use, and that the moment is January 1, 1970, UTC. The program shows what that "
        "definition leaves out. calendar.timegm() turns a moment in UTC into its timestamp, so the moment 06:04:35 on 18 March 2026 is 1773813875, the whole-second part of the chapter's example; timestamp 0 is the first moment of 1970. "
        "The POSIX formula that defines the number gives every day exactly 86,400 seconds, so the leap second of 31 December 2016 has no number: the two seconds on either side of it are one second apart in epoch time, and datetime refuses a "
        "60th second. A float has limited precision: near the chapter's timestamp neighbouring floats are about 2.4e-07 apart, a quarter of a microsecond. The last lines show the year 2038 problem: a signed 32-bit count of seconds "
        "reaches 2**31 - 1 at 03:14:07 UTC on 19 January 2038, and the next second, packed into 32 bits and read back as signed, is -2147483648, which is 20:45:52 UTC on 13 December 1901. Python on a 64-bit machine is not affected, "
        "but file formats and old C programs may be. The chapter does not mention leap seconds or 2038; Appendix B's answer to question 1 names the same moment, January 1, 1970, UTC.",
        "A timestamp counts seconds since 1970 UTC; leap seconds have no number.")

# ---- 5 story: the epoch -------------------------------------------------------------------------------------------
c5, bot5 = con("epoch", 0.5, 2.7, 4.5, fs=7.5, cap=True)
content("An epoch chosen by engineers", STORY["UnixEpoch1971"]["when"],
        [card("Before 1970", "The first Unix manual counted sixtieths of a second from 1 January 1971; the third said 32 bits \"guarantees a crisis every 2.26 years\".",
              0.5, 1.45, 4.5, 1.2, fs=9),
         c5,
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "Nov 1971: counts from 1 Jan 1971",
             "Mar 1972: counts from 1 Jan 1972",
             "Then: 1 Jan 1970, chosen arbitrarily",
             "Jan 2038: a signed 32-bit count wraps"]},
         factrow("UnixEpoch1971", y=4.6)],
        story_notes("UnixEpoch1971") + " The console on the slide runs the arithmetic of the story: time.gmtime(0) is the first moment of 1970 and calendar.timegm of it is 0, the largest signed 32-bit count is 03:14:07 UTC "
        "on 19 January 2038, and 2**32 sixtieths of a second last 2.27 years by this deck's arithmetic, close to the 2.26 the manual states.",
        "An epoch is a choice engineers made, not a fact of nature.")

# ---- 6 which clock -----------------------------------------------------------------------------------------------------
pn = "clocksCut_v1_0_0.py"
a6, b6 = span(pn, "for n in")
f6 = bestfs(pn, (a6, b6), 5.0, 2.9)
w6 = pw(pn, (a6, b6), True, f6)
p6, bot6 = prog(pn, 0.5, 1.55, w6, fs=f6, lines=(a6, b6), show_out=True)
x6 = round(0.5 + w6 + 0.25, 2)
content("Which clock answers which question", "time() can be set back; monotonic() cannot; the chapter subtracts two time() readings",
        [p6,
         card("A moment or an interval", "time.time() answers what moment it is. monotonic() and perf_counter() answer how long something took and never go back; process_time() counts this process's CPU.",
              x6, 1.5, round(9.5 - x6, 2), 1.9, fs=9.5, accent="slate"),
         card("EMULATED, not a changed clock", "Nothing set a clock back: two numbers stand in for a wall clock set back by 10 sec and for the monotonic clock beside it.",
              x6, 3.5, round(9.5 - x6, 2), 1.4, fs=9.5, accent="orange"),
         foot(hidden(pn, a6), 0.5, round(bot6 + 0.08, 2), w6, fs=8.5)],
        "The chapter times code by subtracting two readings of time.time(), and Project 14 does the same for laps. get_clock_info() says what each clock is. time.time() reads CLOCK_REALTIME, which is the system "
        "clock: monotonic False, adjustable True, so an administrator or a time service can set it, and then a difference can be negative. monotonic() and perf_counter() read CLOCK_MONOTONIC, which cannot go "
        "backwards and cannot be adjusted; the Python documentation and PEP 418 name them for intervals. process_time() reads the CPU time of this process, so it does not run while the program sleeps. The program "
        "cannot set the real clock back, so it says EMULATED: two numbers stand in, the wall clock 1000.0 then 990.0 and the monotonic clock 50.0 then 60.0, and the difference is -10.0 on the first and +10.0 on the second. "
        "The last line measures a sleep on the monotonic clock and compares it with a bound, so the line prints the same on every run. For an exact interval the course therefore uses monotonic() or perf_counter(), and keeps time() for a "
        "moment on a calendar.",
        "Use monotonic() for an interval and time() for a moment.", emulated=True)

# ---- 7 pausing -----------------------------------------------------------------------------------------------------------
dg, dcap = diagram("WaitingUntilADate", "activity", (0.5, 1.4, 4.3, 3.1),
                   grid={"make": (0, 0), "now": (0, 1), "later": (0, 2), "go": (0, 3), "sleep": (1, 2)},
                   cols=[(0.0, 2.3), (2.65, 1.65)], rows_n=5, starts=(1, 0), ends={"type": "dot", "col": 0, "row": 4},
                   routes={("start", "make"): "h", ("later", "sleep"): "h", ("sleep", "now"): "vh"}, fs=8, nh=0.5, dh=0.6)
pn = "sleepCut_v1_0_0.py"
a7, b7 = span(pn, "t = time.monotonic(); r")
f7 = bestfs(pn, (a7, b7), 4.65, 3.1)
p7, bot7 = prog(pn, 4.85, 1.55, pw(pn, (a7, b7), True, f7), fs=f7, lines=(a7, b7), show_out=True)
content("Pausing: sleep, polling and drift", "sleep() waits at least what you ask; a loop that sleeps after its work starts late",
        [dg, dcap, p7, foot(hidden(pn, a7), 4.85, round(bot7 + 0.08, 2), 4.65, fs=8.5)],
        "The activity diagram is the chapter's way of pausing a program until a date: make a datetime for the date, read the current moment, and while the moment is earlier than the date pause with time.sleep(1) and read it again, then "
        "continue. The one-second sleep is what keeps the loop from using the processor all the time; the research measured it once: the loop with the sleep used under 0.05 of processor time in 1.2 of elapsed time, and the loop without it over 0.1 in 0.3. The program shows "
        "four things the chapter does not say. time.sleep() returns None and lasts at least the time asked, measured on the monotonic clock. Since Python 3.5 a signal handler that returns does not shorten the sleep, which is retried for "
        "the time that remains, as PEP 475 says: the handler ran and the sleep still lasted at least 0.3. A loop that sleeps one second after its work drifts: with 0.02 of work in each round, the 3600th round starts at 3670.98, "
        "which is 71.98 late, while a loop anchored to the tick starts it at 3599.0 as it should. And round() goes to the even neighbour on a tie, so round(2.5) is 2 and round(3.5) is 4, and it returns an int without a digits argument; "
        "round(2.675, 2) is 2.67 because the float is a little below 2.675. Appendix B answers question 5 with the closest integer, which is incomplete for exactly this reason.",
        "sleep() waits at least what you ask; a sleep after the work drifts.")

# ---- 8 Project 14 --------------------------------------------------------------------------------------------------------
dg, dcap = diagram("TimingALapOfTheStopwatch", "activity", (0.5, 1.4, 4.2, 3.2),
                   grid={"t0": (0, 0), "wait": (0, 1), "lap": (0, 2), "round": (0, 3), "print": (0, 4), "quit": (0, 5)},
                   cols=[(0.0, 3.3), (3.7, 0.5)], rows_n=7, starts=(1, 0), ends={"type": "dot", "col": 0, "row": 6},
                   routes={("start", "t0"): "h", ("quit", "wait"): "loopR"}, fs=8, nh=0.34, dh=0.44)
pn = "stopwatchCut_v1_0_0.py"
a8, b8 = span(pn, "now = [1000.0]")
f8 = bestfs(pn, (a8, b8), 4.65, 3.0)
p8, bot8 = prog(pn, 4.85, 1.55, pw(pn, (a8, b8), True, f8), fs=f8, lines=(a8, b8), show_out=True)
content("Project 14: the Super Stopwatch", "Subtract the last reading, round both times, print the lap; Ctrl-C ends the loop",
        [dg, dcap, p8,
         foot("EMULATED: the key presses are numbers added to a fake clock, so the laps are known. " + hidden(pn, a8), 4.85, round(bot8 + 0.08, 2), 4.65, fs=8.5)],
        "The activity diagram is the chapter's program, step by step: note the start time with time.time(), wait for ENTER, subtract the last time to get the lap time, round the lap time and the total time to two digits, print the "
        "lap number, the total time and the lap time, and ask whether the user pressed Ctrl-C. The real program needs a terminal, because it calls input(); run without one it raises EOFError at the first call. So the program on the slide "
        "says EMULATED: it adds the gaps 3.56, 5.07, 9.05 and 1.43 to a fake clock instead of waiting for a person, and prints the laps the chapter prints, 3.56 and 3.56, 8.63 and 5.07, 17.68 and 9.05, 19.11 and 1.43. "
        "The last line shows a trap of the shipped file: stopwatch.py in the online materials has no f prefix on its print, so it prints the braces, Lap #{lap_number}: {total_time}({lap_time}), where the chapter's listing has the prefix; "
        "the shipped file also has two en dashes, which the next slide explains. The chapter prints the total time and the lap time without a space between them, while the Prettified Stopwatch practice program, on a later slide, "
        "pads them into columns with rjust().",
        "Subtract the last reading from this one; print the laps.", emulated=True)

# ---- 9 repairs ----------------------------------------------------------------------------------------------------------------
c9, bot9 = con("repairs", 0.5, 1.45, 9.0, fs=10, cap=True)
y9 = round(bot9 + 0.1, 2)
content("What the listings need before they run", "Four en dashes, a digit limit, and the Pacific time that was not standard",
        [c9,
         foot("Listings 2, 6 (twice) and 12 write the en dash U+2013 for a minus sign; Python refuses each. The shipped stopwatch.py has two of them, CRLF line ends and no f prefix.",
              0.5, y9, 9.0, fs=10),
         foot("Single run, research: the shipped calcProd.py needs sys.set_int_max_str_digits(); the chapter's product took 2.3 to 2.6 s, math.factorial(100000) 0.136 s.",
              0.5, round(y9 + 0.42, 2), 9.0, fs=10)],
        "The chapter's listings, as served on its web page, need repairs before they run. Four places in three listings, listings 2, 6 and 12, write the en dash U+2013 instead of the minus sign, in end_time – start_time, "
        "time.time() – last_time and oct_21st – about_thirty_years. The first console rows show the refusal, SyntaxError: invalid character '–' (U+2013), and the same expression with a minus sign. A reader who copies the listing gets a program that "
        "does not start. The shipped files are another matter: calcProd.py in the online materials is not the program the chapter prints. It loops over range(1, 100000), prints len(str(result)) and has an en dash; repaired, it raises "
        "ValueError because Python refuses to convert an integer of more than 4300 digits to a string by default, which the console shows with str(math.factorial(100000)). The number of digits of 100000! is 456574, computed here without converting it. "
        "The timings are single runs of the research on one machine: the product took about 2.3 to 2.6 seconds and math.factorial(100000), which gives the same integer, 0.136 seconds, and they vary with the machine. The chapter prints 2.844162940979004 "
        "seconds for its own run. The shipped stopwatch.py also has CRLF line ends, two en dashes and no f prefix on its print, which the previous slide showed.",
        "Copy the dashes out of a listing before you run it; Python refuses them.", measured=True)

# ---- 10 what a program can do with datetime --------------------------------------------------------------------------------------
dg, dcap = diagram("WhatAProgramCanDoWithDatetime", "usecases", (0.5, 1.45, 3.9, 3.15), fs=8)
c10, bot10 = con("dtbasics", 4.6, 1.5, 4.9, fs=9.5, cap=True)
content("What a program can do with datetime", "Seven things through one module; the chapter shows six and no time zone",
        [dg, dcap, c10,
         foot("No now() on these slides: datetime.now() is the time of the day it runs. Every moment here is built from numbers, so every row prints the same on any day.",
              4.6, round(bot10 + 0.3, 2), 4.9, fs=8.5)],
        "The use-case diagram lists what the chapter does with moments and durations through one module: make a moment from a year, month and day, read the current moment, compare two moments, add a duration to a moment, turn a moment into "
        "text with strftime() and read text into a moment with strptime(). They are independent uses of the same module and not a sequence, which is why the picture is a set of uses. The seventh, attaching a time zone with ZoneInfo, is not in "
        "the chapter. The console builds the moments from numbers: Halloween 2026 is earlier than 1 January 2027, their difference is the timedelta of 62 days, 31 October 2026 is a weekday numbered 5, a Saturday, and a day that does not exist, "
        "30 February, raises ValueError. The last row is Appendix B's answer to question 7: the weekday() of 7 January 2019 is 0, Monday. datetime.now() would print the moment the slide was run, so no row calls it; the research recorded the "
        "chapter's own statements of that kind, and they differ from the book's because they come from four different days in the book (11:05 on 17 March 2026, 27 February 2026, 21 October 2026 and 2 December 2026). Python 3.12 deprecated utcnow() "
        "for now(datetime.UTC), which a later slide shows.",
        "A datetime is a moment: compare and subtract moments, not months.")

# ---- 11 timedelta ------------------------------------------------------------------------------------------------------------------
pn = "durationsCut_v1_0_0.py"
a11, b11 = span(pn, "d = TD(")
f11 = bestfs(pn, (a11, b11), 6.1, 3.1)
w11 = pw(pn, (a11, b11), True, f11)
p11, bot11 = prog(pn, 0.5, 1.55, w11, fs=f11, lines=(a11, b11), show_out=True)
x11 = round(0.5 + w11 + 0.25, 2)
content("Durations: timedelta", "Days, seconds and microseconds only; thirty years of 365 days are 7 days short",
        [p11,
         card("No months or years", "TypeError for months= and years=. A month has 28 to 31 days, so 31 Jan + 30 days is 2 March and + 31 days is 3 March.",
              x11, 1.5, round(9.5 - x11, 2), 1.55, fs=9.5, accent="slate"),
         card("Thirty years off", "365 * 30 days back from 21 Oct 2026 is 28 Oct 1996: 7 days off, the 7 leap days.",
              x11, 3.15, round(9.5 - x11, 2), 1.75, fs=9.5, accent="orange"),
         foot(hidden(pn, a11), 0.5, round(bot11 + 0.08, 2), w11, fs=8.5)],
        "A timedelta stores a duration as days, seconds and microseconds. The chapter's example, 11 days, 10 hours, 9 minutes and 8 seconds, has days 11, seconds 36548 and total_seconds() 986948.0, and prints as 11 days, 10:09:08. "
        "It has no months or years, because they are not fixed lengths: months=1 raised TypeError, with the message of Python 3.14, which differs in 3.11, 3.12 and 3.15, as the research found by running eleven interpreters. Adding 30 days "
        "to 31 January gives 2 March and adding 31 gives 3 March, so there is no single addition that means a month. The chapter's about_thirty_years is 365 * 30 days and the chapter says it ignores leap years, but it prints 28 October 1996 "
        "for 30 years before 21 October 2026, which is 7 days off because the span holds 7 leap days; twice the span prints 5 November 1966, 15 days off. The text before the example calls the function datetime.delta(), "
        "which raises AttributeError: module 'datetime' has no attribute 'delta'; the function is datetime.timedelta(). For a real calendar span use replace(year=...), as the program does, or a library.",
        "A timedelta has days and seconds only; 30 times 365 days is not 30 years.")

# ---- 12 strftime ---------------------------------------------------------------------------------------------------------------------------
tq = EX["_tables"]["directives"]["rows"]
tbl = {"t": "table", "x": 0.5, "y": 1.45, "w": 4.5, "colW": [0.7, 1.95, 1.85], "fs": 9, "rowH": 0.27, "rows": tq}
pn = "strftimeCut_v1_0_0.py"
a12, b12 = span(pn, "dt = DT(")
f12 = bestfs(pn, (a12, b12), 4.3, 3.0)
p12, bot12 = prog(pn, 5.2, 1.55, pw(pn, (a12, b12), True, f12), fs=f12, lines=(a12, b12), show_out=True)
content("strftime: a moment to text", "Table 19-1, computed; isoformat() and fromisoformat() are the way to store a moment",
        [tbl, p12, foot(hidden(pn, a12), 5.2, round(bot12 + 0.08, 2), 4.3, fs=8.5)],
        "Table 19-1 of the chapter lists the directives of strftime(). The table on the slide is computed, not typed: for each directive it calls strftime() on the moment 16:29:07 on 3 November 2026, a Tuesday, so %w, "
        "the weekday with Sunday as 0, prints 2 and %j, the day of the year, prints 307. The names of days and months come from the C locale. The chapter sends the reader to strftime.org for the directives; that address now redirects with "
        "HTTP 301 to a cheatsheet of another company, which the links check of this deck does not count on. The program writes the chapter's year/month/day format, a 12-hour clock with %p, the weekday and month names, and a literal percent "
        "sign written as %%. It then shows the form the course recommends for storing a moment, ISO 8601: isoformat() writes 2026-11-03T16:29:07, timespec='minutes' shortens it, an aware value ends in +00:00, and fromisoformat() reads it back, "
        "since Python 3.11 including the letter Z and the week form 2026-W43-3, a Wednesday. The chapter mentions neither isoformat() nor ISO 8601, and the internet standard for timestamps is RFC 3339.",
        "strftime() writes text; isoformat() is the format to store.")

# ---- 13 strptime ----------------------------------------------------------------------------------------------------------------------------------------
pn = "strptimeCut_v1_0_0.py"
a13, b13 = span(pn, "print(DT.strptime('October")
f13 = bestfs(pn, (a13, b13), 5.6, 3.0)
w13 = pw(pn, (a13, b13), True, f13)
p13, bot13 = prog(pn, 0.5, 1.55, w13, fs=f13, lines=(a13, b13), show_out=True)
x13 = round(0.5 + w13 + 0.2, 2)
ty = EX["_tables"]["twoDigitYear"]["rows"]
wt13 = round(9.5 - x13, 2)
content("strptime: text to a moment", "The format must match the text; %y maps 69 to 99 to 1969 to 1999",
        [p13,
         {"t": "table", "x": x13, "y": 1.5, "w": wt13, "colW": [round(wt13 * 0.45, 2), round(wt13 * 0.55, 2)], "fs": 9.5, "rowH": 0.3, "rows": ty},
         card("NOT EXECUTED here", "Python 3.15.0 final and 3.14.7 or later were not run; only 3.15.0b4 was: it raises ValueError for %d without a year.",
              x13, 3.5, wt13, 1.4, fs=9, accent="orange"),
         foot(hidden(pn, a13), 0.5, round(bot13 + 0.08, 2), w13, fs=8.5)],
        "strptime() is the inverse of strftime(): the format must describe the text exactly. October 21, 2026 with %B %d, %Y is a moment at midnight. The chapter's example uses November of '63 and '73, and the table of this slide computes the "
        "rule for %y: Table 19-1 says 00 to 99 means 1970 to 2069, but Python and POSIX map 69 to 99 to 1969 to 1999 and 00 to 68 to 2000 to 2068, so '68' is 2068 and '69' is 1969; the book's two examples, 63 as 2063 and 73 as 1973, are right either way. "
        "A text that does not match raises ValueError and names the text and the format, as the second part of the transcript shows; %B wants the full month name and refuses Oct. A date with no year gets the year 1900, which draws a DeprecationWarning "
        "since Python 3.13 for 29 February, since 1900 was not a leap year. Python 3.15.0b4, the only 3.15 the research could install, raises ValueError for %d without a year; Python 3.15.0 final, released on 9 October 2026 by python.org's list, and "
        "Python 3.14.7 and later were NOT EXECUTED, because uv offered only 3.14.6 and 3.15.0b4 on the day. Python 3.14 added date.strptime() and time.strptime(), which the last line uses.",
        "strptime() needs the exact format; 69 to 99 mean 1969 to 1999.", notexec=True)

# ---- 14 zones ------------------------------------------------------------------------------------------------------------------------------------------------
pn = "zonesCut_v1_0_0.py"
a14, b14 = span(pn, "n = DT(")
f14 = bestfs(pn, (a14, b14), 5.75, 3.1)
w14 = pw(pn, (a14, b14), True, f14)
p14, bot14 = prog(pn, 0.5, 1.55, w14, fs=f14, lines=(a14, b14), show_out=True)
x14 = round(0.5 + w14 + 0.2, 2)
bare = EX["_bare"]["transcript"].split("\n")
content("Time zones: naive and aware", "A value with no zone cannot be compared with one that has one; zoneinfo names the zone",
        [p14,
         card("Pacific Standard Time?", "On 17 March 2026 the zone was Pacific Daylight Time: daylight saving began on 8 March 2026. The chapter says Standard.",
              x14, 1.5, round(9.5 - x14, 2), 1.7, fs=9.5, accent="orange"),
         card("Zones are data", "zoneinfo reads the tz database: tzdata 2026.5 here. A Python with no tzdata package: %s; zoneinfo imported." % bare[1].replace(" - ", ": "),
              x14, 3.3, round(9.5 - x14, 2), 1.6, fs=9, accent="slate"),
         foot(hidden(pn, a14), 0.5, round(bot14 + 0.08, 2), w14, fs=8.5)],
        "A naive datetime has no zone and an aware one has; comparing them for equality gives False and subtracting them raises TypeError. The chapter has no time zone object, so the program uses zoneinfo, in the standard library since "
        "Python 3.9 (PEP 615): 16:29 UTC is equal to 19:29 in Istanbul. The chapter's moment, 1773813875.35, is 23:04:35 on 17 March 2026 in Los Angeles, and the zone name is PDT: the chapter says Pacific Standard Time, but daylight saving time began "
        "in the United States on 8 March 2026, so the zone was Pacific Daylight Time at -07:00, and the printed ctime of 11:05:38 reads 23:05 on a 24-hour clock. The same second, 1,000,000, is 05:46:40 in Los Angeles, 13:46:40 in UTC and 15:46:40 in Istanbul, "
        "so the chapter's fromtimestamp(1000000) is right only in the author's zone; Istanbul was UTC+02:00 in January 1970 and UTC+03:00 in July 2026, as the last line prints, so the offset of a zone depends on the date. zoneinfo reads the operating system's tz database "
        "or the tzdata package and raises ZoneInfoNotFoundError with neither; in the bare environment of the research, with no tzdata package, zoneinfo still worked from the system's data. The story of the database, a lawsuit that shut down its mailing "
        "list for a week in October 2011 until ICANN took it over, is in the notes of the resources slide. This is a record of 13 October 2026 on an Ubuntu 24.04 machine whose system tz database is 2026c.",
        "A naive moment has no zone; name the zone with ZoneInfo.")

# ---- 15 daylight saving ------------------------------------------------------------------------------------------------------------------------------------------
pn = "dstCut_v1_0_0.py"
a15, b15 = span(pn, "import warnings")
c15, t15, bot = pair(pn, (a15, b15), 0.5, 1.55, 9.0, 3.3)
content("Daylight saving: 23 hours, a gap, a fold", "A day added across the change; 02:30 does not exist; 01:30 happens twice; utcnow()",
        [c15, t15, foot(hidden(pn, a15), 0.5, round(bot + 0.06, 2), 9.0, fs=8.5),
         foot("Adding a timedelta to an aware moment moves the wall clock; astimezone(UTC) first if you want the span. utcnow() returns a naive value and warns; use now(UTC).",
              0.5, round(bot + 0.4, 2), 9.0, fs=10)],
        "Noon on 7 March 2026 in New York plus one day is noon on 8 March, and between them the clocks went forward: the difference in UTC is 23 hours while the wall-clock difference is 1 day, because a timedelta added to an aware datetime "
        "moves the wall clock. The hour from 02:00 to 03:00 on 8 March does not exist: asking for 02:30 there and converting to UTC and back gives 03:30. The hour from 01:00 to 02:00 on 1 November happens twice, and the attribute fold, "
        "added by PEP 495, tells the two apart: 01:30 with fold 0 is 05:30 UTC and with fold 1 is 06:30 UTC, although the two values compare equal. The chapter has none of this. The last two lines are about a deprecation: Python 3.12 deprecated "
        "datetime.utcnow() and utcfromtimestamp(), which return naive values in UTC, in favour of now(datetime.UTC), which returns an aware value; the program catches the DeprecationWarning and prints its category. "
        "The Python documentation lists datetime.UTC, added in Python 3.11, as an alias of timezone.utc. The research ran the same lines under eleven interpreters, 3.11, 3.12, 3.13, the seven 3.14 releases and 3.15.0b4: 11 of 48 compared items differ between releases, among them this deprecation, "
        "the error text of sleep('1'), and the text of the error for timedelta(months=1).",
        "Add a day to an aware moment and the wall clock moves, not 24 hours.")

# ---- 16 run and Popen ---------------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("ChoosingHowToLaunchAProgram", "activity", (0.5, 1.4, 4.4, 3.2),
                   grid={"list": (0, 0), "wait": (0, 1), "run": (0, 2), "capture": (0, 3), "check": (0, 4), "popen": (1, 2), "poll": (1, 3)},
                   cols=[(0.0, 2.1), (2.3, 2.1)], rows_n=6, starts=(1, 0), ends={"type": "dot", "col": 0, "row": 5},
                   routes={("start", "list"): "h", ("wait", "popen"): "hv", ("poll", "end"): "vh"}, fs=8, nh=0.42, dh=0.5)
pn = "runCut_v1_0_0.py"
a16, b16 = span(pn, "r = subprocess.run(['sleep'")
f16 = bestfs(pn, (a16, b16), 4.4, 3.2)
p16, bot16 = prog(pn, 5.1, 1.55, pw(pn, (a16, b16), True, f16), fs=f16, lines=(a16, b16), show_out=True)
content("Launching a program: run() or Popen()", "A list of strings starts the program; run() waits for it and Popen() does not",
        [dg, dcap, p16, foot(hidden(pn, a16), 5.1, round(bot16 + 0.08, 2), 4.4, fs=8.5)],
        "The flow chart is the choice the chapter walks through: put the program and its arguments in a list of strings, then decide whether the program should wait for the process to end. If it should, call subprocess.run() with the list, "
        "pass capture_output=True and text=True to get the output, and check=True and a timeout to raise on a failure; if it should not, call subprocess.Popen() and use poll(), which returns None while the process runs. "
        "The program runs both on this machine. run(['sleep', '0.3']) returned a CompletedProcess with returncode 0 after the child ended. With capture_output=True the output is bytes, b'out\\n' and b'err\\n', and the child's standard error is "
        "captured separately; with text=True the same output is a str. Popen returned at once: poll() gave None while the child slept, then wait() blocked and returned 0, and poll() gave 0. The chapter opens the calculator six times with "
        "Popen on Windows, and Figure 19-1 is a screenshot of the six windows; calc.exe, notepad and mspaint were NOT EXECUTED, because the machine is Linux, and the picture is not reproduced here. The alt text of the opening picture of the chapter is empty "
        "and the alt text of Figure 19-1 describes a Windows desktop with six overlapping calculator programs.",
        "run() waits for the program; Popen() returns at once.")

# ---- 17 Popen, poll, wait -----------------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("ARunningAChildProcess", "sequence", (0.5, 1.45, 3.9, 3.15), fs=8, head_w=1.05)
pn = "popenCut_v1_0_0.py"
a17, b17 = span(pn, "for call in")
f17 = bestfs(pn, (a17, b17), 5.0, 3.2)
p17, bot17 = prog(pn, 4.5, 1.55, pw(pn, (a17, b17), True, f17), fs=f17, lines=(a17, b17), show_out=True)
content("Popen: poll, wait, check, timeout", "A failing program raises, a hung one times out, a list passes arguments untouched",
        [dg, dcap, p17, foot(hidden(pn, a17), 4.5, round(bot17 + 0.08, 2), 5.0, fs=8.5)],
        "The sequence diagram follows the exchange between the program, the Popen object and the process: the program calls Popen() with a list, the object starts the process and returns at once, poll() returns None while the process runs, "
        "wait() blocks until the process ends with an exit code, and the object returns the code. The program on the slide shows what the chapter does not. check=True turns a non-zero exit status into CalledProcessError: false exits 1, and the "
        "message says so. A timeout turns a program that hangs into TimeoutExpired, and run() kills the child before it raises; the message names the command and the time, and its wording of the time depends on the release, which the research "
        "found by running eleven interpreters. A program that does not exist raises FileNotFoundError, not a non-zero exit code. The last lines show that a list passes the arguments untouched: 'my file.txt' stays one argument, and '*.txt' is not "
        "expanded, because no shell is involved. That is the reason to prefer a list over a string for a program you know. The chapter's example passes the name of a file to notepad on Windows as the second item of the list; that program was NOT EXECUTED here.",
        "Check the exit status, give a timeout, and pass a list, not a string.")

# ---- 18 exit codes, signals, life of a process ---------------------------------------------------------------------------------------------------------
dg, dcap = diagram("ALaunchedProcessFromStartToExit", "lifecycle_branch", (0.5, 1.4, 9.0, 2.0), fs=8)
pn = "exitsCut_v1_0_0.py"
a18, b18 = span(pn, "run = lambda")
f18 = bestfs(pn, (a18, b18), 9.0, 1.05, hi=7.5)
w18 = pw(pn, (a18, b18), True, f18)
y18 = 3.9
p18, bot18 = prog(pn, 0.5, y18, w18, fs=f18, lines=(a18, b18), show_out=True)
content("A process from start to exit", "Exit code 0 is success; a negative code is the signal that ended the child",
        [dg, dcap, p18,
         foot(hidden(pn, a18), round(0.5 + w18 + 0.15, 2), y18, round(9.5 - 0.5 - w18 - 0.15, 2), fs=8.5)],
        "The state diagram follows a launched process: Popen starts it, it runs while poll() gives None, and it ends either with an exit code or by a signal. The program runs five children and prints their return codes: a program that does "
        "nothing returns 0, sys.exit(3) returns 3, an uncaught exception returns 1, and a child that was killed by SIGKILL has the return code -9 and one ended by SIGTERM -15, the negative of the signal number. The corpus program of the research "
        "ran the rest: sys.exit('msg') also returns 1, os._exit(256 + 7) returns 7 because an exit status holds eight bits, terminate() on a child with a SIGTERM handler printed asked to stop, saving work and returned 0, kill() returned -9 and "
        "printed nothing, and trying to handle SIGKILL raised OSError with errno 22. The chapter mentions none of this; it has no exit codes, no terminate() and no kill(). A timeout in run() kills the child with SIGKILL, which is the last transition "
        "of the diagram. On Windows the same words exist, terminate() and kill() both call TerminateProcess, but Windows was NOT EXECUTED, so the slide claims nothing about it.",
        "A process ends with a return code; a negative one is a signal.")

# ---- 19 shell, arguments, opening files -----------------------------------------------------------------------------------------------------------------------
pn = "shellCut_v1_0_0.py"
a19, b19 = span(pn, "import shutil")
f19 = bestfs(pn, (a19, b19), 5.9, 3.1)
w19 = pw(pn, (a19, b19), True, f19)
p19, bot19 = prog(pn, 0.5, 1.55, w19, fs=f19, lines=(a19, b19), show_out=True)
x19 = round(0.5 + w19 + 0.2, 2)
content("The shell, and opening files", "shell=True with a list runs only the first item; start and open are not on Linux",
        [p19,
         card("NOT EXECUTED here", "start, notepad and calc.exe (Windows), open for an application (macOS) and a desktop that xdg-open could use were not run.",
              x19, 1.5, round(9.5 - x19, 2), 1.9, fs=9.5, accent="orange"),
         card("What Linux does", "open exists only because xdg-utils registers it as an alternative of xdg-open; start does not exist.",
              x19, 3.5, round(9.5 - x19, 2), 1.4, fs=9.5, accent="slate"),
         foot(hidden(pn, a19), 0.5, round(bot19 + 0.08, 2), w19, fs=8.5)],
        "The chapter opens a file with the default application by running start on Windows and open on macOS and Linux. The program asks what a Linux machine does. A list with shell=True runs only its first item: echo ran with no arguments and "
        "printed an empty line, and the second item became the zero argument of the shell, which is why the failing start printed hello.txt: 1: start: not found and returned 127. A string with shell=True works. A command built from a file name is "
        "the danger: the file name x; echo INJECTED ran a second command, shlex.quote() prevented it, and so did a list with no shell. open exists here as /usr/bin/open only because the xdg-utils package registers it as an alternative of xdg-open; "
        "start does not exist, and os.startfile, the Windows way, is absent. webbrowser.open() returned False with no browser to open, and pyperclip, which the chapter introduces in Chapter 8, raised an error with no clipboard program. All of the "
        "following were NOT EXECUTED: the commands of Windows and macOS, and any program that needs a desktop. The research ran xdg-open on a file that did not exist, which exited 2 and said so, and that is all it can say about it here.",
        "Never build a shell string from a file name; pass a list.", notexec=True)

# ---- 20 schedulers inside a process ---------------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("WhatAProgramCanDoToRunALaterJob", "usecases", (0.5, 1.45, 3.6, 3.15), fs=8)
pn = "schedCut_v1_0_0.py"
a20, b20 = span(pn, "now, log")
f20 = bestfs(pn, (a20, b20), 5.2, 3.05)
w20 = pw(pn, (a20, b20), True, f20)
p20, bot20 = prog(pn, 4.3, 1.55, w20, fs=f20, lines=(a20, b20), show_out=True)
barepk = EX["_bare"]["transcript"].split("\n")[0]
content("Running a job later", "Timer, sched and call_later run inside a live process; cron and launchd outside it",
        [dg, dcap, p20,
         foot("EMULATED: sched runs on a clock the program moves. " + hidden(pn, a20),
              4.3, round(bot20 + 0.08, 2), w20, fs=8.5)],
        "The use-case diagram lists what a program can do to run a job later: write a cron entry with five time fields, call a function once after a delay with Timer, order events by time and priority with sched, call a function later with "
        "asyncio's call_later, run jobs every day with the schedule package, describe a job in a launchd property list, and normalise a systemd calendar expression. The chapter gives the operating system schedulers one paragraph, Task Scheduler, launchd "
        "and cron, and its Summary points to the book's page at No Starch Press for instructions that the page does not hold. The program runs the three that live inside a process. sched ran its events in order of time and then priority on a "
        "clock the program moves, so it says EMULATED: now at 0, two at 2, five first at 5 with priority 0 and five at 5 with priority 1, and the clock ended at 5.0. threading.Timer returns at once, so the list was still empty after start() and held "
        "fired after join(). call_later ran soon first, then the 0.1 callback, then the 0.2 one. The schedule package, version 1.2.2, the newest release on 13 October 2026, uploaded on 25 May 2024, computed its first run at 10:30 for a job set "
        "every day at that time; in a Python with only the standard library, importing it raised ModuleNotFoundError. All four need a process that stays alive; if the machine restarts, they are gone, which is the reason for an operating system scheduler.",
        "Timer, sched and call_later run inside a process that stays alive.", emulated=True)

# ---- 21 cron -----------------------------------------------------------------------------------------------------------------------------------------------------------
pn = "cronCut_v1_0_0.py"
a21, b21 = span(pn, "def nxt")
c21, t21, bot = pair(pn, (a21, b21), 0.5, 1.55, 9.0, 2.6, gap=0.2)
xr = t21["x"]
wr = round(9.5 - xr, 2)
ytr = round(t21["y"] + t21["h"] + 0.1, 2)
content("Cron: five fields and a small world", "Both day fields restricted means either matches; the job runs in cron's environment",
        [c21, t21,
         foot("Lines 1 to 12 (imports, a comment and field(), which turns one time field into its set of numbers) are not shown.", 0.5, round(bot + 0.06, 2), 4.7, fs=8.5),
         card("Real cron, recorded 13 Oct 2026", "Ubuntu 24.04, cron 3.0pl1. The job saw PATH=/usr/bin:/bin, /root, no terminal, parent sh. A TZ line reached it; CRON_TZ did not move the schedule.",
              xr, ytr, wr, 1.3, fs=8.5, accent="slate"),
         card("NOT EXECUTED here", "Task Scheduler (schtasks) and launchd (the plist only written and read back) and a systemd timer (OnCalendar only normalised).",
              xr, round(ytr + 1.35, 2), wr, round(4.97 - ytr - 1.35, 2), fs=8.5, accent="orange")],
        "A crontab line has five time fields, minute, hour, day of the month, month and day of the week, and then the command. The matcher on the slide is the study's own function, written to the rule of the Debian manual page. "
        "The manual page says that when both day fields are restricted a command runs when either matches, so 0 0 13 * 5 is not Friday the 13th: it fires on every 13th and on every Friday, and the next run after 9:30 on Tuesday 13 October 2026 "
        "is the Friday 16 October. The other lines show 9:30 on weekdays, every 15 minutes, and 29 February, which waits until 2028. The research then ran cron for real on this machine, cron 3.0pl1-184 on Ubuntu 24.04, and these are records of 13 October 2026, "
        "not results the deck recomputes. A Python job started by cron two seconds after the turn of the minute saw PATH=/usr/bin:/bin, the working directory /root, no terminal and sh as its parent, and its local clock read 22:36:01 UTC while the shell "
        "showed 01:36:01 +03. A TZ=Asia/Kolkata line in the crontab reached the job and set its clock to IST; a minute of 61 was refused by crontab with exit code 1 and the message bad minute. The schedule follows the zone of the cron daemon: started from a "
        "shell whose TZ was Europe/Istanbul, an entry written on the Istanbul clock fired at the target moment and the entry for the same moment on the UTC clock did not, while a CRON_TZ=Asia/Kolkata line was passed to the job as a variable but did not move the "
        "schedule, and the Debian manual page does not mention CRON_TZ. Task Scheduler, launchd and a systemd timer were NOT EXECUTED: a launchd property list for 04:00 daily was written and read back with plistlib, 501 bytes and equal, and systemd-analyze "
        "only normalised Mon..Fri 09:00 to Mon..Fri *-*-* 09:00:00. " + story_notes("CronPurdue1977"),
        "Cron runs the job in its own small world, in the zone of its daemon.", notexec=True)

# ---- 22 Project 15 and the Prettified Stopwatch ---------------------------------------------------------------------------------------------------------------------
pn1, pn2 = "countdownCut_v1_0_0.py", "prettyCut_v1_0_0.py"
a22, b22 = span(pn1, "now = [0.0]")
a22b, b22b = span(pn2, "rows = ")
f22 = bestfs(pn1, (a22, b22), 5.9, 1.6)
p22, bot22 = prog(pn1, 0.5, 1.55, pw(pn1, (a22, b22), True, f22), fs=f22, lines=(a22, b22), show_out=True)
f22b = bestfs(pn2, (a22b, b22b), 5.9, 1.6)
p22b, bot22b = prog(pn2, 0.5, round(bot22 + 0.3, 2), pw(pn2, (a22b, b22b), True, f22b), fs=f22b, lines=(a22b, b22b), show_out=True)
x22 = round(0.5 + max(p22["w"], p22b["w"]) + 0.2, 2)
pins = EX["_pins"]["transcript"].split("\n")
content("Project 15 and the Prettified Stopwatch", "A countdown is a loop that sleeps; rjust() lines the laps up in columns",
        [p22, p22b,
         card("NOT EXECUTED here", "No sound was played: the machine has no sound card. alarm.wav is not in the online materials; autbor.com/alarm.wav redirects (HTTP 302) to a 582,952-byte file.",
              x22, 1.5, round(9.5 - x22, 2), 1.55, fs=9, accent="orange"),
         card("Pinned and newest", "Appendix A pins playsound3 2.4.0. Recorded in the pins environment: %s." % pins[0].replace(" | ", ", "),
              x22, 3.1, round(9.5 - x22, 2), 1.2, fs=9, accent="slate"),
         foot("EMULATED: a number stands in for the clock time.sleep(1) would move; the chapter counts from 60. " + hidden(pn1, a22),
              x22, 4.28, round(9.5 - x22, 2), fs=8)],
        "Project 15, the Simple Countdown, counts down from 60 with time.sleep(1) between the numbers and then plays a sound file with playsound3. The loop on the slide is the same loop with 5 in place of 60, and it says EMULATED: a number "
        "that the loop increases stands in for the clock that time.sleep(1) would move, so it prints 5 4 3 2 1 and counts 5.0 seconds of fake time without waiting. The sound was NOT EXECUTED: the machine has no sound card, the online materials do not "
        "hold alarm.wav, and autbor.com/alarm.wav redirects with HTTP 302 to a file of 582,952 bytes and 3.30 seconds on the book's own site. The shipped simplecountdown.py matches the printed listing apart from spacing, but the copy served at autbor.com differs: "
        "it sets timeLeft to 2, uses camel case and has the Windows start line uncommented. Appendix A pins playsound3 2.4.0; the newest release on 13 October 2026 is 3.3.2, uploaded on 18 July 2026, and the pins environment of the research holds 2.4.0. "
        "The second program is the first practice program, the Prettified Stopwatch: rjust() pads the lap number to 2, and the times to 6, so the columns line up, where the chapter's Project 14 printed them without padding. The numbers come from the "
        "laps of the stopwatch slide.",
        "A countdown is a loop that sleeps; rjust() lines columns up.", emulated=True, notexec=True)

# ---- 23 Friday the 13th ---------------------------------------------------------------------------------------------------------------------------------------------------
pn = "fridayCut_v1_0_0.py"
a23, b23 = span(pn, "import collections")
c23, t23, bot = pair(pn, (a23, b23), 0.5, 1.55, 9.0, 2.85, gap=0.2)
xr = t23["x"]
ch = EX["_charts"]["thirteenths"]
ych = round(t23["y"] + t23["h"] + 0.05, 2)
chart = {"t": "chart", "ctype": "bar", "x": xr, "y": ych, "w": round(9.5 - xr, 2), "h": round(4.38 - ych, 2), "labels": ch["labels"],
         "title": "13ths by weekday, 400 years", "series": [{"name": "13ths", "data": ch["values"]}], "dataLabels": True, "dlFs": 9}
content("Friday the 13th, forward and backward", "Python's dates run back to the year 1; the 13th is a Friday 688 times in 400 years",
        [c23, t23, chart, factrow("Gregorian1582")],
        story_notes("Gregorian1582") + " The second practice program of the chapter finds the next ten Friday the 13ths from a date. From a fixed day, 13 October 2026, the first is 13 November 2026 and the tenth 13 August 2032. "
        "The research also walked backward day by day until Python stopped it: 3,485 such dates down to 13 April of the year 1, and then OverflowError: date value out of range at 1 January of the year 1. The chart is computed: over 400 years from 2000, "
        "the 13th falls on a Friday 688 times, the most of any weekday, and on a Thursday 684 times, because the Gregorian calendar repeats every 146,097 days, which is exactly 20,871 weeks. Every year from 1 to 9999 has at least one Friday the 13th, "
        "which the corpus program of the research checked. The chapter's two practice programs are not in the online materials: the zip holds no prettifiedStopwatch.py and no fridayThirteenth.py, so this deck's programs are written from the chapter's description.",
        "The 13th is a Friday 688 times in 400 years; Python dates reach year 1.")

# ---- 24 summary: the mind map --------------------------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("KeepingTimeAtAGlance", "mindmap", (0.5, 1.4, 9.0, 3.2), fs=9, root_w=2.0)
content("The chapter in one map", "Six branches; the slides of each branch hold the examples",
        [dg, dcap],
        "These six branches are the route of the deck. The epoch and the clock: the epoch is 1970 in UTC, a monotonic clock gives the true difference, and sleep waits at least the time asked. The datetime module: a timedelta has no months, "
        "a two-digit year maps 69 to 1969, and a date with no year uses 1900. Time zones: a naive value has no zone, a day across the change is 23 hours, and a signed 32-bit count ends in 2038. Launching programs: run() waits and Popen does not, a list "
        "of arguments passes through no shell, and start and open are not on Linux. Scheduling: cron has five time fields, a cron job does not run in your shell, and sched and Timer run inside a Python process. The last branch is the book and its "
        "practice: four places write an en dash, the stopwatch prints the laps, and the 13th is a Friday 688 times in 400 years. Together they answer the first question of the chapter, which clock, which moment and which launcher answers each "
        "question, and the slides that say where a printed line differs answer the second. The map is drawn from the same specification as the interactive page.",
        "If a branch feels unproven, its slides hold the example.")

# ---- 25 resources ----------------------------------------------------------------------------------------------------------------------------------------------------------
PUB = {p[0]: p for p in RD.PUBS}
_read = [["The textbook, chapter 19 - free online", PUB["P01"][2]],
         ["time module documentation", PUB["P10"][2]],
         ["datetime module documentation", PUB["P11"][2]]]
_ref = [["zoneinfo documentation", PUB["P12"][2]],
        ["subprocess documentation", PUB["P13"][2]],
        ["POSIX: seconds since the epoch", PUB["P34"][2]],
        ["crontab(5), the Debian manual page", PUB["P40"][2]]]
_hist = [["Unix time (Wikipedia)", STORY["UnixEpoch1971"]["link"]],
         ["The year 2038 problem (Wikipedia)", STORY["Year2038Wrap"]["link"]],
         ["Cron and Purdue (Wikipedia)", STORY["CronPurdue1977"]["link"]],
         ["The tz database (Wikipedia)", STORY["TzLawsuit2011"]["link"]]]
_pkg = [["schedule on PyPI", PUB["P51"][2]],
        ["tzdata on PyPI", PUB["P50"][2]]]
LINKS = [r[1] for r in _read + _ref + _hist + _pkg]
json.dump({"_version": __version__, "links": LINKS}, open(os.path.join(HERE, "links_v1_0_0.json"), "w"), indent=1)
content("Where to go from here", "Every link was opened on the day this deck was made",
        [{"t": "links", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.55, "fs": 9.5, "groups": [
            {"head": "Read", "rows": _read}, {"head": "Reference", "rows": _ref}, {"head": "History and standards", "rows": _hist},
            {"head": "The two packages", "rows": _pkg}]}],
        "Every link on this slide was opened on the day the deck was made, and the build records the status each answered. The textbook chapter is free to read online and holds every listing of the chapter; the documentation of the time, "
        "datetime, zoneinfo, subprocess and sched modules describes them. The reference links are the pages for the topics where the deck corrected or extended the chapter: the POSIX definition of seconds since the epoch, and the manual page of "
        "crontab that states the rule for the two day fields. The history links are the sources behind the six stories of the chapter. Two of them are slides, the epoch chosen by Unix engineers and the Gregorian calendar; the other four are told in the notes: "
        "the leap second and the year 2038 on the slide of the epoch timestamp, the lawsuit that shut down the time zone database's mailing list on the slide of time zones, and cron at Purdue on the slide of cron. The tzdata and schedule packages are the "
        "two third-party packages whose versions the deck records. The rest of the sixty-odd sources of the research, among them the PEPs, the RFCs and the manual pages of launchd and systemd, are in the research package.",
        "Textbook, documentation and history, opened the day this deck was built.")

# ---- 26 closing ---------------------------------------------------------------------------------------------------------------------------------------------------------------
content("What you should now be able to say", "Four claims, each carried by a result you saw printed",
        [{"t": "bullets", "x": 0.6, "y": 1.5, "w": 8.8, "h": 2.4, "fs": 15, "items": [
            "Use monotonic() for an interval; time() and datetime name a moment, with a zone.",
            "A timedelta has no months, %y maps 69 to 1969, and a day across daylight saving is 23 hours.",
            "Launch with a list of arguments, check the exit code, and give a timeout.",
            "Cron runs the job in its own small world; Timer and sched need a live process."]},
         {"t": "chips", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.6, "fs": 13, "big": True,
          "items": ["%d rows run" % sum(len(v) for v in G.values()), "%d programs run" % len(PROGS), "8 diagrams"]}],
        "Four claims, each carried by a result you saw printed. If you can say them in your own words and run the examples yourself, you have the chapter. The console rows use only numbers and named zones, so they can be typed into any "
        "Python and give the same text on any day; time, datetime, calendar, zoneinfo and subprocess are the standard library, and the programs build their own files in a temporary folder and use no network. The rows were run again under Python 3.14.6 "
        "with tzdata 2026.5 each time the deck was built, and the programs were run again by the check that compares the slides with the recording. What was not run is marked on its slide: a Windows computer, a Mac, a systemd timer, a sound card, "
        "and the final release of Python 3.15 with Python 3.14.7 and later. The next chapter of the book sends email, texts and push notifications, and what this chapter taught about launching and scheduling programs, and about the difference between "
        "a moment and an interval, carries over.",
        "Questions are welcome; bring a time problem to run.")

# ---- agenda ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
_t = {s["title"]: i + 1 for i, s in enumerate(S)}
_parts = [("Clocks, sleeping and the stopwatch", "The epoch timestamp", "What the listings need before they run"),
          ("Dates, durations and text", "What a program can do with datetime", "strptime: text to a moment"),
          ("Time zones", "Time zones: naive and aware", "Daylight saving: 23 hours, a gap, a fold"),
          ("Launching programs", "Launching a program: run() or Popen()", "The shell, and opening files"),
          ("Scheduling and the practice programs", "Running a job later", "Friday the 13th, forward and backward"),
          ("Summary and resources", "The chapter in one map", "Where to go from here")]
_rows = ["%s (slides %d-%d)" % (name, _t[a], _t[b]) for name, a, b in _parts]
_ends = [_t[b] for _, _, b in _parts]
_starts = [_t[a] for _, a, _ in _parts]
if _starts[0] != 4 or any(_starts[i + 1] != _ends[i] + 1 for i in range(len(_parts) - 1)) or _ends[-1] != len(S) - 1:
    raise SystemExit("REFUSED: agenda ranges are not contiguous: %r %r (len S=%d)" % (_starts, _ends, len(S)))
_nconsole = sum(1 for s in S for i in s["items"] if i.get("t") in ("code", "prog"))
_nstory = sum(1 for s in S for i in s["items"] if i.get("t") == "factrow")
S[1]["items"] = [
    {"t": "numlist", "x": 0.5, "y": 1.4, "w": 6.3, "h": 3.55, "fs": 11.5, "items": _rows},
    {"t": "stat", "x": 7.05, "y": 1.5, "w": 2.45, "h": 3.4, "vert": True, "items": [
        {"n": str(len(S)), "label": "slides, numbered bottom-right"},
        {"n": "%d + %d" % (_nstory, 6 - _nstory), "label": "true stories: %d on slides, %d in the notes" % (_nstory, 6 - _nstory)},
        {"n": str(_nconsole), "label": "consoles and programs, all run before they were shown"}]}]
S[1]["sub"] = "Six parts; every range is a run of slides you can jump to"
S[1]["take"] = "Six parts, from the epoch to a cron job in its small world."
S[1]["notes"] = ("The route has six parts. It starts with clocks: the epoch timestamp and the choice of an engineer in the story of the epoch, the clock that answers each question, sleeping and the drift of a loop, "
                 "Project 14, the Super Stopwatch, and the repairs the listings need before they run. Then dates and text: what a program can do with datetime, durations in a timedelta, strftime() with Table 19-1 and strptime() with its "
                 "two-digit year. Then time zones: naive and aware values, the zone of the chapter's example, and the 23-hour day, the gap and the fold of daylight saving. Then launching programs: run() and Popen(), poll, wait, the check "
                 "and the timeout, exit codes and signals, and the shell with the commands start and open that Linux lacks. The fifth part is scheduling and the practice programs: Timer, sched and call_later inside a process, cron fields "
                 "and what real cron did, Project 15 with the Prettified Stopwatch, and the Friday the 13th finder. The last part is a one-map summary and the resources. The ranges name the exact slides, so you can return to the part you need. "
                 "Two of the slides are true stories and four more are told in the notes; the eight narrative diagrams of the chapter are drawn from the same specifications as the interactive page. Every output was printed by "
                 "Python 3.14.6 with tzdata 2026.5 and schedule 1.2.2, and what could not be run is marked on its slide.")

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
plan = {"meta": {"title": "Ch. 19: Time, Tasks, and Programs", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": len(S), "diagrams": SHOWN, "notExecuted": NOTEXEC, "measured": MEASURED, "emulated": EMULATED}, "slides": S}
out = os.path.join(HERE, "deck_plan_v1_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides; diagrams on slides", dict(sorted(SHOWN.items(), key=lambda kv: kv[1])), "; NOT EXECUTED on slides", NOTEXEC, "; measured", MEASURED, "; emulated", EMULATED)

#!/usr/bin/env python3
"""Builds deck_plan_v1_0_0.json - SEN0414 chapter 20 (Sending Email, Texts, and Push Notifications) on the CME classroom standard.

Same regime as chapters 10 to 19: numbered warm-ivory slides, an agenda with exact slide ranges, a summary before the resources,
full-sentence takeaway strips, stories with fact rows, consoles and whole programs (or honest excerpts of them, labelled with their
line numbers) with their results as Python printed them. Every console result and program transcript comes from
examples_out_v1_0_0.json (made by examples_run_v1_0_0.py under Python 3.14.6 with ezgmail 2026.4.28, requests 2.34.2 and aiosmtpd 1.4.6;
email, smtplib, imaplib, ssl, json, hmac, subprocess and html.parser are the standard library); the speaker notes are prose for the
reader and carry only what the chapter's RDODI research package (03-materials/ch20/rdodi, sen0414_ch20_rdodi_data_v1_0_1.py, findings
F1 to F15), its records (08-tooling/ch20-page/*.json) or a program of this deck established.

What this chapter adds against chapter 19: NOTHING REACHED A REAL SERVICE. No Gmail account, Gmail server, phone number, carrier, Twilio
account or ntfy server was used, and nothing was sent to anyone. Twelve corpus programs and nineteen programs written for the deck were run
for real; fourteen of those that show output on a slide ran against a LOCAL STAND-IN on this machine: aiosmtpd with a self-signed certificate
(SMTP), the real ezgmail library on a replacement of the HTTP layer of Google's client library whose replies were written by the research (Gmail),
a recorder in place of ntfy, a list in memory in place of a mailbox, a recorder in place of the browser, and sample forecast periods in the shape of
api.weather.gov. Every slide that shows output of a stand-in says so, with the words honesty_check_v1_0_0.py requires ('Stand-in for Gmail',
'Stand-in for an SMTP server', 'Stand-in for ntfy', ...). What the research recorded on 13 October 2026 and the deck does not re-run (the
dovecot session, the public pages, the DNS queries, the pinned Requests) is on a slide as 'Recorded'. What could not be run is marked NOT EXECUTED on its
slide: a Google account and the OAuth steps (slide 5), Gmail's acceptance of .exe and .zip attachments (slide 6), Gmail's threading of a reply (slide 8),
the Gmail servers (slide 14), Python 3.14.7 and later and the final 3.15.0 (slide 15), a text through a gateway or Twilio (slide 16), the 153 and 67
character parts of a long text (slide 17), publishing to ntfy (slide 18), receiving from ntfy (slide 20) and Windows and macOS (slide 23). The eight narrative
diagrams of the chapter (sen0414_ch20_diagrams_v1_0_0.py, grounding 0.84 or more) are drawn as native shapes (diagram_shapes_v1_0_0.py) and checked by
diagram_check_v1_0_0.py; one table (the same probe run under five interpreters, run again by the deck check every time) and one chart (the bits in a
topic name) are native PowerPoint objects whose data the deck check computes again; no photograph is used (the research used none: Wikimedia
Commons answered 429); two of the six stories are slides (Tomlinson, AT&T) and four are told in the notes.

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


ST = load("stories20", os.path.join(HERE, "..", "sen0414_ch20_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
DG = load("diagrams20", os.path.join(HERE, "..", "sen0414_ch20_diagrams_v1_0_0.py"))
NODES = DG.nodes_from_ttl(os.path.join(HERE, "..", ".."))
_bad = DG.run_checks(NODES)
if _bad:
    raise SystemExit("REFUSED: the diagrams fail their own checks: %r" % _bad[:3])
DIAG = {d["id"]: d for d in DG.DIAGRAMS}
RD = load("rdodi20", os.path.join(HERE, "..", "sen0414_ch20_rdodi_data_v1_0_1.py"))
EX = json.load(open(os.path.join(HERE, "examples_out_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s; no row reads the clock or the network" % PYV
G = {k: [[s, (o or "")] for s, o in v] for k, v in EX.items() if not k.startswith("_")}
PROGS = EX["_programs"]
CQ1, CQ2 = RD.CQS
CW = 0.0088  # inches per character per point of Courier New, as the shared fit check measures it

# the honesty lines (honesty_check_v1_0_0.py requires 'NOT EXECUTED' on every slide the plan lists and on no other, 'Recorded' likewise,
# and on every slide that shows a stand-in program the words the recording holds for that program, besides 'local stand-in')
L_NOTEXEC = "NOT EXECUTED"
L_REC = "Recorded"


def lines_of(rows):
    return sum(1 + (1 if out.strip() else 0) for _, out in rows)


USED = set()
ROWS_SHOWN = sum(len(G[g]) for g in ("title", "address", "imap", "shell"))
SHOWN_PROGS = sum(1 for k in PROGS if "Cut_" in k)


def con(group, x, y, w, fs=11, label=None, cap=True, rows=None):
    USED.add(group)
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
    """A chapter program (or an honest excerpt) with its transcript, sized from its text; returns (item, bottom y).
    The excerpt is a verbatim slice and the label above the panel names it ('program <name>, lines a to b of n'), as
    program_check_v1_0_0.py verifies. The transcript, when shown, sits in the same panel."""
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


def stack(bodies, x, y, w, fs=8.5, gap=0.04):
    """Foot items one under another, each at the bottom of the one before."""
    out = []
    for b in bodies:
        f = foot(b, x, round(y, 2), w, fs=fs)
        out.append(f)
        y = f["y"] + f["h"] + gap
    return out


def diagram(did, kind, box, **kw):
    """The shapes item of a narrative diagram and its caption (which names the diagram and its measured grounding)."""
    d = DIAG[did]
    fn = {"activity": DS.activity, "sequence": DS.sequence, "lifecycle_skip": DS.lifecycle_skip, "usecases": DS.usecases, "mindmap": DS.mindmap}[kind]
    it = fn(d["data"], box, **kw)
    h, n = d["grounding"]
    body = "diagram %s - %s pattern, %d of %d words grounded in the chapter's text" % (did, d["pattern"], h, n)
    cap = {"t": "foot", "x": box[0], "y": round(box[1] + box[3] + 0.03, 2), "w": box[2], "h": round(DS.need_h(body, box[2], 8.5) + 0.04, 2), "fs": 8.5,
           "body": body}
    it["did"] = did
    return it, cap


S = []
SHOWN = {}  # diagram id -> slide number
NOTEXEC = []  # slide numbers that carry the words NOT EXECUTED
RECORDED = []  # slide numbers that carry the word Recorded (a record of 13 Oct 2026 that the deck does not run again)
STANDIN = {}  # slide number -> the stand-in programs it shows


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


def hidden(pn, a, what="imports and a comment"):
    """The words that say where the lines before the excerpt are: lines 1 to a-1 of the program."""
    return "Lines 1 to %d (%s) are not shown." % (a - 1, what)


W_GM = "imports, the Gmail stand-in and a comment"
W_SMTP = "imports, a message helper, the stand-in SMTP server and a comment"
W_SMTP2 = "imports, helpers, the stand-in server and a comment"
W_NTFY = "imports, the recorder and a comment"
W_PLAIN = "imports and a comment"

SAY_GM = "Stand-in for Gmail: the real ezgmail on a local stand-in for Google's server, replies written by this study; Gmail was never reached."
SAY_SMTP = "Stand-in for an SMTP server: aiosmtpd on 127.0.0.1, a local stand-in; Gmail's servers were never reached."
SAY_NTFY = "Stand-in for ntfy: a recorder on 127.0.0.1, a local stand-in; it is not ntfy and says nothing about ntfy.sh."
SAY_BOX = "Stand-in mailbox: a list in memory, a local stand-in for IMAP; no mail account was read."
SAY_BROWSER = "Stand-in for the browser: webbrowser.open is replaced by a local stand-in that records the address; no page was opened."
SAY_FORECAST = "Sample forecast data: two periods written for this study in the shape of api.weather.gov, a local stand-in; no network."

# ---- 1 title ---------------------------------------------------------------------------------------------------
c1, _ = con("title", 5.0, 0.4, 4.5, fs=10, cap=False)
S.append({"kind": "title", "title": "Ch. 20: Email, Texts, and Push",
          "sub": "Sending email, texts, and push notifications: EZGmail, smtplib, SMS gateways, and ntfy",
          "items": [c1, foot("Every output on these slides was printed by the Python above when the deck was made. Gmail, a phone and ntfy were never reached, and nothing was sent to anyone: "
                             "where a program needed a server it ran against a local stand-in on this machine, and its slide says so. What could not be run is marked on its slide.",
                             0.6, 3.85, 8.8, fs=11)],
          "notes": "Chapter 19 taught a program to start and schedule other programs. Chapter 20 teaches a program to reach a person: by email through the Gmail API and the EZGmail module, by text through the SMS email gateways of a table, and by push notification through ntfy and the Requests library. "
                   "It ends with five practice questions and three practice programs, Umbrella Reminder, Auto Unsubscriber and Email-Based Computer Control. This deck follows the chapter in its own order: setting up, sending, reading, searching and downloading with EZGmail; the gateway table and the length of a text; "
                   "sending and receiving with ntfy; and the practice programs. It adds what the chapter leaves out and what the research found when every printed output was run again: the standard library's email, smtplib and imaplib modules, which the chapter names only to say EZGmail is better; "
                   "STARTTLS and certificate checks; the difference between the envelope and the header; two gateways that are gone or going; the byte limit of ntfy; and what changed between Python 3.11 and 3.15. "
                   "Nothing here reached a real service. No Gmail account, no Gmail server, no phone number, no carrier, no Twilio account and no ntfy server was used, and nothing was sent to a person. Every output on these slides was printed by Python 3.14.6, installed with uv, with ezgmail 2026.4.28, requests 2.34.2 and aiosmtpd 1.4.6. "
                   "A program that needed a server ran against a local stand-in on this machine: aiosmtpd with a self-signed certificate for SMTP, the real ezgmail library on a replacement of the HTTP layer of Google's client library whose replies were written by the research for Gmail, and a recorder for ntfy. Each slide that shows such output says so. "
                   "What could not be run, a Google account and its OAuth steps, Gmail's servers, a text through a carrier or Twilio, publishing to ntfy, Windows and macOS, and Python 3.14.7 and later with the final 3.15.0, is marked NOT EXECUTED on its slide.",
          "bg": "light"})

# ---- 2 agenda (filled in at the end) -------------------------------------------------------------------------------
S.append({"kind": "content", "title": "Today's route", "sub": "", "items": [], "notes": "", "take": "", "bg": "light"})

# ---- 3 questions ------------------------------------------------------------------------------------------------
content("The questions this chapter answers", "The chapter's own competency questions; the summary comes back to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 2.2, "fs": 13, "items": [CQ1, CQ2]},
         {"t": "chips", "x": 0.5, "y": 3.8, "w": 9.0, "h": 0.5, "fs": 10,
          "items": ["6 branches", "%d topics" % len(NODES), "%d console rows" % ROWS_SHOWN,
                    "%d programs run" % len(PROGS), "8 diagrams", "Python %s" % PYV]}],
        "The first question is the spine of the chapter, and the deck answers it slide by slide. On a machine with no Gmail account, no phone number and no push service, a program that builds a message, parses an address, speaks SMTP to a server, reads a poll answer or checks a password can be shown to work, "
        "provided the server is a stand-in on the same machine. A program that logs in to Google, delivers a text or reaches ntfy.sh can only be shown to fail, with the error a reader sees before the setup is done, and the deck says NOT EXECUTED wherever a success would have to be claimed. "
        "The second question is the watch-out of the deck. The chapter has 15 listings with 48 statements. They were replayed as printed in three environments. With ezgmail installed and no credentials, which is where a reader stands before the Google Cloud steps, 19 of the 48 matched the book; with no packages at all, 3 matched. "
        "On a stand-in for Google's server, 42 of 46 matched in the zone America/Los_Angeles and 38 of 46 in Europe/Istanbul, because dates and a timestamp depend on the zone of the computer. Four never match: two statements whose quoted strings the web page breaks across lines, the printed text of a thread, and a Windows path that Linux cannot start. "
        "The online materials of the book, 91 files, hold no file for this chapter. Each slide says where a printed line differs and on what evidence.",
        "Know what can be shown to work and what can only be shown to fail.")

# ---- 4 what a program can do with Gmail ---------------------------------------------------------------------------
dg, dcap = diagram("WhatAProgramCanDoWithEzgmail", "usecases", (0.5, 1.45, 4.0, 3.15), fs=8)
x4 = 4.75
content("What a program can do with Gmail", "Seven things through one module; the chapter replaced smtplib with the Gmail API",
        [dg, dcap,
         card("Three ways to reach a person", "The Gmail API through EZGmail for email, SMS email gateways for texts, and ntfy for push notifications; Twilio is named as the reliable way to text.",
              x4, 1.5, round(9.5 - x4, 2), 1.55, fs=9.5, accent="slate"),
         card("Recorded 13 Oct 2026", "The book's page has 15 listings. The online materials hold 91 files and none for this chapter, and the book page it names for an example implementation holds none.",
              x4, 3.15, round(9.5 - x4, 2), 1.75, fs=9.5, accent="orange")],
        "The use-case diagram lists what the chapter does with one Gmail account through one module: send an email, attach files, list unread email, search with the operators of the Gmail search box, read the messages of a thread, download attachments, and reply to a message in its thread. They are independent uses of the same module and not a sequence, which is why the picture is a set of uses. "
        "The chapter teaches three ways for a program to reach a person: the Gmail API through the EZGmail module, with a credentials file and a token file; texts through the SMS email gateways of Table 20-1, with Twilio named as the reliable alternative; and push notifications through ntfy, with a POST to a topic and a poll with /json?poll=1. "
        "It ends with five practice questions and three practice programs. The second edition of the book taught smtplib and imapclient in its chapter 18, mentioning smtplib 21 times and Twilio 31; the third edition's chapter names smtplib and imaplib only to say that EZGmail is better. "
        "The card records what the research found on 13 October 2026 and this deck does not run again: the chapter's page returned 200 with 53,147 bytes, the online materials of the third edition, a zip of 91 files of which 72 are Python, hold no program that names ezgmail, ntfy, smtplib, imaplib, Twilio or weather.gov, "
        "and the book page at No Starch Press that the chapter's last sentence names for an example implementation of the last practice program has none. The practice programs of this deck are therefore written from the chapter's own text.",
        "One account, seven things a program can do with it.", recorded=True)

# ---- 5 setup -----------------------------------------------------------------------------------------------------
dg, dcap = diagram("SendingAMailWithEzgmail", "activity", (0.5, 1.4, 4.35, 2.9),
                   grid={"files": (0, 0), "init": (0, 1), "err": (0, 2), "send": (0, 3), "att": (0, 4), "cc": (0, 5), "redo": (1, 1)},
                   cols=[(0.0, 2.4), (2.55, 1.8)], rows_n=6, starts=(1, 0), ends={"type": "dot", "col": 1, "row": 5},
                   routes={("start", "files"): "h", ("err", "redo"): "hv", ("redo", "init"): "h", ("cc", "end"): "h"}, fs=8, nh=0.42, dh=0.44)
pn = "setupCut_v1_0_0.py"
a5, b5 = span(pn, "d = wd()")
f5 = bestfs(pn, (a5, b5), 4.7, 2.8)
w5 = pw(pn, (a5, b5), True, f5)
p5, bot5 = prog(pn, 4.85, 1.4, w5, fs=f5, lines=(a5, b5), show_out=True)
content("Setup: credentials, token and init()", "A missing credentials.json fails at the first call; token.json is a password",
        [dg, dcap, p5,
         foot("Made-up values. " + hidden(pn, a5, W_GM), 4.85, round(bot5 + 0.04, 2), 4.65, fs=8),
         foot("NOT EXECUTED: Google Cloud console steps, consent screen, token refresh.", 0.5, round(dcap["y"] + dcap["h"] + 0.04, 2), 4.3, fs=8.5)],
        "The activity diagram is the chapter's setup: keep the credentials file and the token file in the working directory, call ezgmail.init(), and if it raises no error go on to send(); if it does, do the steps of the Google Cloud console again. "
        "The program shows what a reader sees before those steps are done. The last line of the ezgmail module calls init(_raiseException=False), so a failed login is hidden when the module is imported and the first call to init() raises EZGmailException with the message Can't find credentials file, and ezgmail.LOGGED_IN stays False. "
        "The library asks for the scope https://mail.google.com/, which is the whole mailbox. The chapter never writes the file name credentials.json, although Appendix B does, and it never uses the word refresh. "
        "The second half of the program makes a token.json with the oauth2client package that ezgmail uses, from made-up values: it is plain JSON of 16 keys, written with the file mode 0o600, and it holds the client secret and the refresh token, so the chapter's advice to treat it like a password is right. "
        "ezgmail 2026.4.28 requires google-api-python-client and oauth2client; oauth2client 4.1.3 was uploaded on 7 September 2018 and PyPI classifies it as inactive, so the login of the chapter's library stands on a package that has not changed in eight years. "
        "Google's OAuth page says that a project whose consent screen is external and in the status Testing is issued a refresh token that expires in 7 days; that was read and not run, because it needs a Google account and a week. "
        + story_notes("Gmail2004"),
        "init() fails without credentials; token.json is a password.", notexec=True)

# ---- 6 sending ---------------------------------------------------------------------------------------------------
pn = "sendCut_v1_0_0.py"
a6, b6 = span(pn, "d = wd()")
f6 = bestfs(pn, (a6, b6), 5.9, 3.0)
w6 = pw(pn, (a6, b6), True, f6)
p6, bot6 = prog(pn, 0.5, 1.55, w6, fs=f6, lines=(a6, b6), show_out=True)
x6 = round(0.5 + w6 + 0.25, 2)
content("Sending: attachments, cc and bcc", "One POST of a base64 message; the library does not look at what it attaches",
        [p6,
         card("Bcc is in the text", "ezgmail writes the bcc argument into the message as a Bcc header, because the API takes the whole message.",
              x6, 1.5, round(9.5 - x6, 2), 1.85, fs=9.5, accent="slate"),
         card("NOT EXECUTED here", "Whether Gmail accepts setup.exe or a .zip, and what it does with that Bcc header, were not run: no Gmail account was used.",
              x6, 3.45, round(9.5 - x6, 2), 1.5, fs=9.5, accent="orange"),
         foot(SAY_GM + " " + hidden(pn, a6, W_GM), 0.5, round(bot6 + 0.06, 2), w6, fs=8.5)],
        "ezgmail.send() makes one POST to users/me/messages/send whose JSON body has a single key, raw, the whole message in base64. The program shows what the library puts in it. With three arguments the message has the headers to, from and subject. With a list of file names it builds a multipart/mixed message with one part for each file; "
        "the library did not refuse setup.exe, although Gmail's help page, which the research read and did not test, names the types Gmail blocks. The cc and bcc arguments become the Cc and Bcc headers of the message, and the Bcc address is written into the text that is posted; whether Gmail removes that header from the copies it delivers was not run, "
        "so the slide says NOT EXECUTED. In a longer run of the same stand-in, program ezgmailSendWithStandIn, which is not on the slide, a Turkish body was sent as charset utf-8 and a Turkish subject as an encoded word, and both came back unchanged; the research read the RFCs for both. A subject with a line break raised HeaderParseError, because ezgmail builds the message with the legacy MIMEText class, and the research found that no request was made. "
        "Everything on the slide came from the real ezgmail library running against a stand-in for Google's server: the Google client library's HTTP layer was replaced by an object that records each request and answers with a reply written by the research. "
        "The chapter says that Gmail has security and anti-spam measures that might not send repeated emails with the exact same text. " + story_notes("Thuerk1978"),
        "send() takes a list of files; the library does not vet them.", notexec=True)

# ---- 7 reading ---------------------------------------------------------------------------------------------------
pn = "readCut_v1_0_0.py"
a7, b7 = span(pn, "th = ezgmail.GmailThread")
f7 = bestfs(pn, (a7, b7), 5.8, 3.0)
w7 = pw(pn, (a7, b7), True, f7)
p7, bot7 = prog(pn, 0.5, 1.55, w7, fs=f7, lines=(a7, b7), show_out=True)
x7 = round(0.5 + w7 + 0.25, 2)
content("Reading: threads, messages and the zone", "Printing a thread fetches its messages; a timestamp is read in the computer's zone",
        [p7,
         card("The book prints another", "The chapter shows a GmailThread with len=2 and a snippet with no opening quote; ezgmail 2026.4.28 prints numMessages=2 and quotes the snippet.",
              x7, 1.4, round(9.5 - x7, 2), 1.6, fs=9, accent="orange"),
         card("A timestamp has no zone", "ezgmail builds it as a naive datetime from internalDate, so the same message reads three ways. The book's 2026-12-20 21:28:32 holds only at UTC-6.",
              x7, 3.05, round(9.5 - x7, 2), 1.3, fs=9, accent="slate"),
         foot(SAY_GM + " " + hidden(pn, a7, W_GM), 0.5, round(max(bot7, 4.4) + 0.06, 2), 9.0, fs=8.5)],
        "A GmailThread holds an id, a snippet and a history id, and it fetches its GmailMessage objects the first time messages is read; printing the thread reads messages, so the program shows one request to the API made by str(thread), which the chapter does not say. "
        "The chapter prints the text <GmailThread len=2 snippet= Do you want to watch RoboCop this weekend?'> with no opening quote; ezgmail 2026.4.28 prints <GmailThread numMessages=2 snippet='...'>. The timestamp of a message is built from the internalDate that the API returns, in milliseconds, as a naive datetime in the zone of the computer that runs the program: "
        "the program sets the zone of its own process three times and the same message, 1797000528 seconds since the epoch, reads 14:48:48 in UTC, 08:48:48 in America/Chicago and 17:48:48 in Europe/Istanbul. The chapter never says that its reading depends on the zone; its example fromtimestamp(1797823712), printed as 2026-12-20 21:28:32, is right only in a zone at UTC-6, "
        "and in UTC it is 2026-12-21 03:28:32, a Monday, as the slide on receiving shows. A message with no Subject header raised AttributeError, both on .subject and on printing it. All of this came from the real library against a stand-in for Google's server whose replies were written by the research.",
        "Reading a thread costs a request; a timestamp depends on the zone.")

# ---- 8 reply, search, quoted text, downloads ------------------------------------------------------------------------
pn1, pn2 = "replyCut_v1_0_0.py", "downloadCut_v1_0_0.py"
a8, b8 = span(pn1, "src = ezgmail")
a8b, b8b = span(pn2, "d = wd()")
f8 = bestfs(pn1, (a8, b8), 4.55, 2.95)
p8, bot8 = prog(pn1, 0.5, 1.4, pw(pn1, (a8, b8), True, f8), fs=f8, lines=(a8, b8), show_out=True)
f8b = bestfs(pn2, (a8b, b8b), 4.55, 2.95)
p8b, bot8b = prog(pn2, 5.05, 1.4, pw(pn2, (a8b, b8b), True, f8b), fs=f8b, lines=(a8b, b8b), show_out=True)
content("Replies, search, quoted text, downloads", "A reply keeps the thread id only; one quoting form is cut; a file name can be a path",
        [p8, p8b,
         foot(SAY_GM + " " + hidden(pn1, a8, W_GM) + " NOT EXECUTED: Gmail threading the reply; any real download.",
              0.5, round(max(bot8, bot8b) + 0.04, 2), 9.0, fs=8)],
        "reply() posted a message with the threadId of the original and the original sender as the recipient, but with the subject unchanged, RoboCop and not Re: RoboCop, and without In-Reply-To or References. Google's sending guide names a matching Subject and those headers, with the threadId, as what makes a message join a thread, "
        "so whether Gmail threads these replies was not run and the slide says NOT EXECUTED. replyAll() made no API call and returned None. The queries of the three listing functions are visible in the requests: unread() asks for the label UNREAD, recent() for INBOX and search('has:attachment') passes the text to the API, which is Appendix B's answer to its third question, "
        "with 25 results by default. removeQuotedParts() cut only the English form On Sun, Jan 1, 2018 at 12:00 PM ... wrote: and left the replies of the form On Sun, 1 Jan 2018 at 12:00, a Turkish line and the English line with U+202F before PM. "
        "On the right, downloadAllAttachments() with an attachment named ../evil.txt wrote the file one level above the download folder, so a name that comes from a stranger's email is a path; the chapter says that downloadAttachment() overwrites an existing file, and it did: MINE became AAAA. A name that is not in the message raised AttributeError. "
        "Both programs ran the real library against a stand-in for Google's server.",
        "A reply keeps the thread id; a name with a path escapes the folder.", notexec=True)

# ---- 9 story: Tomlinson --------------------------------------------------------------------------------------------
c9, bot9 = con("address", 0.5, 1.95, 4.7, fs=9.5, cap=True)
content("An @ between the user and the machine", STORY["Tomlinson1971"]["when"],
        [{"t": "text", "x": 0.5, "y": 1.4, "w": 4.7, "h": 0.5, "fs": 11, "body": "Before 1971, mail reached only users of the same computer."},
         c9,
         {"t": "beats", "x": 5.5, "y": 1.5, "w": 4.0, "h": 2.6, "fs": 12, "items": [
             "1971: SNDMSG adapted for TENEX",
             "The @ separates user and machine",
             "Chosen: it was in no user name",
             "Today: parseaddr splits at it"]},
         factrow("Tomlinson1971", y=4.5)],
        story_notes("Tomlinson1971") + " The console on the slide uses only the email package of the standard library, so each row can be typed into any Python: parseaddr() splits the sender of the chapter's example into a name and an address, partition('@') splits the address at Tomlinson's sign, "
        "and formataddr() puts a name and an address back together. The last two rows show a trap that the research found in every interpreter it ran: parseaddr() given two addresses in one string returns two empty strings, the answer of a parser that rejects malformed input, "
        "and strict=False returns the first address. The strict argument is documented as new in Python 3.13, yet it was accepted by the 3.11.17 and 3.12.3 packages of the machine, which carry the security fix; the table on a later slide shows it.",
        STORY["Tomlinson1971"]["lesson"] + ".")

# ---- 10 building a message ------------------------------------------------------------------------------------------
pn = "buildCut_v1_0_0.py"
a10, b10 = span(pn, "m = mk()")
f10 = bestfs(pn, (a10, b10), 5.6, 3.3)
w10 = pw(pn, (a10, b10), True, f10)
p10, bot10 = prog(pn, 0.5, 1.4, w10, fs=f10, lines=(a10, b10), show_out=True)
x10 = round(0.5 + w10 + 0.25, 2)
content("Building a message: EmailMessage", "Headers, a body, a MIME tree and the bytes that are sent; CRLF only with policy.SMTP",
        [p10,
         card("What EZGmail hides", "ezgmail builds a MIME message and posts it in base64. The chapter shows neither the message nor the standard library that can build one.",
              x10, 1.4, round(9.5 - x10, 2), 1.5, fs=9, accent="slate"),
         card("Line ends", "as_bytes() ends lines with LF; policy.SMTP ends them with CRLF as the protocol wants: 0 against 10 here.",
              x10, 2.95, round(9.5 - x10, 2), 1.3, fs=9, accent="orange"),
         foot(hidden(pn, a10, "imports, a helper that builds the message and a comment") + " The date and Message-ID are fixed so the text is the same on every run.",
              x10, 4.3, round(9.5 - x10, 2), fs=8)],
        "The standard library builds a message with EmailMessage, which the chapter does not use; EZGmail does the equivalent for the reader. The program makes a plain message with set_content() and counts its headers, eight once the body is set, with Content-Type text/plain, charset utf-8, and a transfer encoding of 7bit. "
        "Lines end with a line feed in as_bytes() and with a carriage return and a line feed under policy.SMTP, which counted 0 and 10, because the protocol of RFC 5321 ends lines with CRLF. add_alternative() turns the message into multipart/alternative with a text part and an html part, and add_attachment() wraps it in multipart/mixed with the attachment, "
        "so walk() lists the tree: multipart/mixed, multipart/alternative, text/plain, text/html and application/octet-stream. iter_attachments() lists the file name, and get_body() with the preference html, plain returns the html part. The date is set with formatdate() from a number and the Message-ID is fixed, so that the printed text is the same on every run. "
        "The program imports only the email package and its policy module and opens no connection; whether it runs in a Python in a browser was not tested.",
        "EmailMessage builds the message; policy.SMTP gives the CRLF line ends.")

# ---- 11 headers, addresses, line breaks --------------------------------------------------------------------------------
pn = "headersCut_v1_0_0.py"
a11, b11 = span(pn, "m = EmailMessage()")
f11 = bestfs(pn, (a11, b11), 6.2, 3.25)
w11 = pw(pn, (a11, b11), True, f11)
p11, bot11 = prog(pn, 0.5, 1.4, w11, fs=f11, lines=(a11, b11), show_out=True)
x11 = round(0.5 + w11 + 0.2, 2)
content("Headers, addresses and line breaks", "A Turkish subject is an encoded word; two addresses in one string parse to nothing",
        [p11,
         card("Header injection", "A line break in a header would let text add a Bcc header. EmailMessage refuses it at once; MIMEText, which EZGmail uses, refuses it when the message is written.",
              x11, 1.4, round(9.5 - x11, 2), 1.7, fs=9, accent="orange"),
         card("Quote the name", "A comma in a name needs quotes, or one person becomes two.",
              x11, 3.2, round(9.5 - x11, 2), 1.0, fs=9, accent="slate"),
         foot(hidden(pn, a11, "imports, a helper and a comment"), x11, 4.25, round(9.5 - x11, 2), fs=8)],
        "A header may hold only ASCII, so a subject with Turkish letters is written as an encoded word, =?utf-8?b?...?=, and decoded back by decode_header() and make_header(); the printed Subject line shows the encoded part and the next line the decoded text. "
        "An address list is split by getaddresses(): with the quotes around Doe, Jon the name stays one name, and without them the comma splits one person into two entries, the first with no address. parseaddr() given two addresses in one string returns two empty strings, and with strict=False it returns the first address; the research saw the empty answer in all eleven interpreters it ran. "
        "The last lines are the defence against header injection. EmailMessage raises ValueError at once for a value with a line break, and the legacy MIMEText accepts it and raises HeaderParseError when the message is written; ezgmail uses MIMEText, "
        "which is why a subject with a line break raised before any request was made. Without the check, text after the line break would be read as a new header, such as a Bcc to a stranger. This program uses only the standard library.",
        "Encode the header, quote the name, and refuse the line break.")

# ---- 12 SMTP with STARTTLS ---------------------------------------------------------------------------------------------
dg, dcap = diagram("ASmtpSessionWithStarttls", "sequence", (0.5, 1.45, 4.1, 3.15), fs=8, head_w=1.1)
pn = "starttlsCut_v1_0_0.py"
a12, b12 = span(pn, "s = conn(); print('before:'")
f12 = bestfs(pn, (a12, b12), 4.7, 2.6)
w12 = pw(pn, (a12, b12), True, f12)
p12, bot12 = prog(pn, 4.8, 1.4, w12, fs=f12, lines=(a12, b12), show_out=True)
content("SMTP with STARTTLS", "Upgrade the connection, verify the certificate, and only then log in",
        [dg, dcap, p12,
         foot(SAY_SMTP + " " + hidden(pn, a12, W_SMTP2), 4.8, round(bot12 + 0.04, 2), 4.7, fs=8)],
        "The sequence diagram is the order of an SMTP session with STARTTLS: the client connects and calls ehlo(), the server advertises STARTTLS, the client calls starttls() with a context, the server answers 220 and the session uses TLS, the client logs in and sends the message, and the server answers 250. "
        "The chapter does not use smtplib, and its page never writes the words STARTTLS, TLS or SSL. The program ran the real smtplib against a local stand-in for an SMTP server, aiosmtpd on 127.0.0.1 with a self-signed certificate, so no Gmail server was reached; imap.gmail.com and smtp.gmail.com timed out from this machine. "
        "Before STARTTLS the server advertised STARTTLS and no AUTH; after it, AUTH LOGIN PLAIN, and the server saw TLS. With the default context the self-signed certificate was refused with SSLCertVerificationError; starttls() with no context at all returned 220, an encrypted connection that is not authenticated, because no certificate was checked. "
        "In a longer run of the same local stand-in, program smtpLocalStarttls, which is not on the slide, login() before STARTTLS raised SMTPNotSupportedError, because the server offers AUTH only after TLS; on the slide, after STARTTLS with a context that trusts the certificate, the login returned 235. " + story_notes("Postel1982"),
        "Upgrade with STARTTLS, verify the certificate, then log in.")

# ---- 13 refusals and the envelope --------------------------------------------------------------------------------------------
pn1, pn2 = "refusalsCut_v1_0_0.py", "envelopeCut_v1_0_0.py"
a13, b13 = span(pn1, "s = conn()")
a13b, b13b = span(pn2, "s.send_message")
f13 = min(bestfs(pn1, (a13, b13), 4.5, 3.15), bestfs(pn2, (a13b, b13b), 4.5, 3.15))
p13, bot13 = prog(pn1, 0.5, 1.4, pw(pn1, (a13, b13), True, f13), fs=f13, lines=(a13, b13), show_out=True)
p13b, bot13b = prog(pn2, 5.05, 1.4, pw(pn2, (a13b, b13b), True, f13), fs=f13, lines=(a13b, b13b), show_out=True)
content("Refused recipients and the envelope", "A Bcc recipient is in the envelope, not in the text; the From header can say anything",
        [p13, p13b,
         foot(SAY_SMTP + " " + hidden(pn1, a13, W_SMTP2), 0.5, round(max(bot13, bot13b) + 0.03, 2), 9.0, fs=8)],
        "On the left, one of two recipients is refused with 550. send_message() does not raise: it returns a dict of the refused address and the answer, and the message was still stored for the other, so a program that ignores the return value loses a recipient without a sound. When every recipient is refused it raises SMTPRecipientsRefused. "
        "A wrong password raised SMTPAuthenticationError with the code 535, and a closed port raised ConnectionRefusedError, an OSError. On the right, the envelope is separate from the header. send_message() sent RCPT TO for the To, the Bcc and the Cc addresses, and the Bcc header was not in the text, as the documentation of send_message says; the address of the Bcc recipient appears nowhere in the message. "
        "sendmail() was given an envelope sender, bounces@mallory.example, that matches neither the From header, CEO <ceo@bank.example>, nor any login, and the server accepted it without asking for a login. The chapter says it is fairly trivial for hackers to fake a from address; this is the demonstration, and it is why a program should not trust a From line. "
        "The chapter never uses the words SPF, DKIM or DMARC, the standards that let a receiving server check the sender. The research recorded that gmail.com publishes the SPF record v=spf1 redirect=_spf.google.com and the DMARC record v=DMARC1; p=none; sp=quarantine, and that Google's guidelines require authentication from senders of more than 5,000 messages a day. "
        "Both programs ran the real smtplib against the local stand-in server.",
        "The envelope decides who gets the mail; the From header decides nothing.")

# ---- 14 IMAP -----------------------------------------------------------------------------------------------------------
dg, dcap = diagram("AMessageInAnImapMailbox", "lifecycle_skip", (0.5, 1.4, 4.85, 2.85), fs=8, sw=1.5, sh=0.4, sfs=8.5, top=0.3, lab_w=1.75, margin=1.3)
c14, bot14 = con("imap", 5.5, 1.4, 4.0, fs=7.5, cap=True)
content("Reading mail with IMAP", "A message is unseen, seen, marked Deleted, then expunged; Python 3.14 adds IDLE",
        [dg, dcap, c14,
         foot("Recorded 13 Oct 2026, not run again here: dovecot 2.3.21 on 127.0.0.1, a local stand-in for imap.gmail.com. SEARCH UNSEEN found the message, BODY.PEEK kept it unseen, "
              "RFC822 set Seen, STORE and EXPUNGE emptied the INBOX, and idle() saw EXISTS.", 5.5, round(bot14 + 0.06, 2), 4.0, fs=8.5),
         foot("NOT EXECUTED: any connection to imap.gmail.com or smtp.gmail.com; a TCP connect to each timed out from this machine and nothing was sent.",
              0.5, round(dcap["y"] + dcap["h"] + 0.04, 2), 4.85, fs=8.5)],
        "The state diagram follows one message through the INBOX of an IMAP server: it arrives unseen; a fetch with BODY.PEEK leaves it unseen, a fetch of RFC822 sets the Seen flag, STORE adds the Deleted flag from either state, and EXPUNGE removes it. This is the delete step of the Email-Based Computer Control program. "
        "The chapter does not use imaplib, which the standard library has and which the chapter names only to say EZGmail is better. The console on the right uses only the standard library: the ports 25, 465, 143 and 993; the fact that imaplib.IMAP4.idle exists in Python 3.14, where the IDLE command of RFC 2177 was added; "
        "and the parsers ParseFlags() and Time2Internaldate(). The session itself is a record of 13 October 2026 and this deck does not run it again: the research ran dovecot 2.3.21 on 127.0.0.1, with a self-signed certificate and one user, as a local stand-in for Gmail's IMAP server, and read it with imaplib over STARTTLS. "
        "SEARCH UNSEEN found the message; a FETCH with BODY.PEEK left the flags alone; a FETCH of RFC822 set Seen; STORE with the Deleted flag and EXPUNGE left the INBOX empty; and idle() in Python 3.14.6 reported EXISTS when a message arrived a second later. A wrong password raised error AUTHENTICATIONFAILED. "
        "imapclient 4.1.0, the library the second edition used, did the same against dovecot. Gmail's own servers were NOT EXECUTED: a TCP connection to imap.gmail.com on 993 and to smtp.gmail.com on 587 and 465 timed out after ten seconds, with nothing sent.",
        "A message is unseen, seen, marked, then expunged.", notexec=True, recorded=True)

# ---- 15 what changed in Python -----------------------------------------------------------------------------------------------
tq = EX["_tables"]["interpreters"]["rows"]
tbl = {"t": "table", "x": 0.5, "y": 1.4, "w": 9.0, "colW": [3.3, 1.14, 1.14, 1.14, 1.14, 1.14], "fs": 8.5, "rowH": 0.255, "rows": tq}
ybot15 = round(1.4 + 0.255 * len(tq) + 0.12, 2)
content("What changed in Python's mail modules", "The same probe under five interpreters; every cell is run again by the check",
        [tbl,
         foot("Correction to the research text (finding F13): it puts a minimum of TLS 1.2 in create_default_context() from 3.13. Run here, 3.11.17 already shows TLS 1.2, and the documentation dates it to 3.10; "
              "what 3.13 added is the two verify flags. The 3.12.3 package shows the lowest version, a setting of that build.", 0.5, ybot15, 9.0, fs=9),
         foot("NOT EXECUTED: Python 3.14.7 and later and the final 3.15.0; 3.15.0b4 is a beta. 3.11, 3.12 and 3.13 are the Ubuntu packages of this machine, 3.14.6 and 3.15.0b4 come from uv.",
              0.5, round(ybot15 + 0.52, 2), 9.0, fs=9)],
        "The table is the same probe run under five interpreters, and the deck check runs all five again every time it checks the deck. IMAP4.idle() exists from Python 3.14. The keyfile and certfile arguments of starttls() and of the SSL classes of smtplib and imaplib are gone from 3.12; the documentation of 3.14 says so, "
        "although the body text of starttls() still describes them. smtpd, asyncore and asynchat were removed in 3.12, and cgi, imghdr, sndhdr, nntplib and telnetlib in 3.13; PEP 594 is the list. ssl.create_default_context() adds the verify flags VERIFY_X509_STRICT and VERIFY_X509_PARTIAL_CHAIN from 3.13, as the documentation says, "
        "so a certificate that an older context accepted, one that does not follow RFC 5280, may now be refused. smtplib writes its commands in lower case from 3.13, mail from: and rcpt to:, where 3.12 wrote mail FROM:; this was seen on the wire and is not in the documentation. email.utils.localtime() lost its isdst argument in 3.14, after a deprecation in 3.12. "
        "The research text, finding F13, says the minimum TLS version of create_default_context() became 1.2 in 3.13. Run here it is TLS 1.2 already in 3.11.17, the documentation puts it in 3.10, and the 3.12.3 package of Ubuntu reports the lowest supported version, which is a setting of that build; so that clause of F13 is wrong, and the table shows the evidence. "
        "The same finding says that parseaddr()'s strict argument came in 3.13; the documentation says so, but the 3.11.17 and 3.12.3 packages accept it, because the security fix was backported. The research ran eleven interpreters, 3.11 to 3.15.0b4, and found 19 of 48 compared items different between releases; five are here. "
        "Python 3.14.7 and later and the final 3.15.0 were NOT EXECUTED, because uv offered only 3.14.6 and 3.15.0b4 on the day.",
        "Mail modules changed between 3.11 and 3.15; check the release.", notexec=True)

# ---- 16 SMS gateways: AT&T story --------------------------------------------------------------------------------------------
pn = "gatewayCut_v1_0_0.py"
a16, b16 = span(pn, "print(len(T)")
f16 = bestfs(pn, (a16, b16), 5.1, 2.7)
w16 = pw(pn, (a16, b16), True, f16)
p16, bot16 = prog(pn, 0.5, 1.55, w16, fs=f16, lines=(a16, b16), show_out=True)
x16 = round(0.5 + w16 + 0.25, 2)
content("SMS email gateways, and the end of one", STORY["Att2025"]["when"],
        [p16,
         card("Recorded 13 Oct 2026", "A DNS query for the mail exchangers of the 18 gateway domains found none for txt.att.net and mms.att.net and NXDOMAIN for both of Sprint's; 13 of 18 had one. A missing record is a symptom, not proof.",
              x16, 1.4, round(9.5 - x16, 2), 1.7, fs=9, accent="slate"),
         card("NOT EXECUTED here", "No text was sent or delivered through a gateway or Twilio. Twilio's API answered a request without credentials with HTTP 401, and nothing more.",
              x16, 3.15, round(9.5 - x16, 2), 1.3, fs=9, accent="orange"),
         foot(hidden(pn, a16, "imports and the 12 rows of Table 20-1, typed from the chapter") + " Pure arithmetic; no message is sent.", 0.5, round(bot16 + 0.06, 2), w16, fs=8.5),
         factrow("Att2025", y=4.55)],
        story_notes("Att2025") + " Table 20-1 of the chapter lists 12 providers, each with an SMS domain and some with a different MMS domain. An address is the number, an @ and the domain: 2125551234@vtext.com is the chapter's own example, and 2125551234@vzwpix.com is its MMS address. "
        "Verizon and Xfinity Mobile share the SMS domain vtext.com, so the 12 rows hold 11 distinct SMS domains. The program counts the days from the notices to the date of this study: 483 days after AT&T's shutdown on a Tuesday, and 169 days before the end that Verizon expects by 31 March 2027, a Wednesday, with some senders losing access earlier. "
        "The DNS queries went over HTTPS to dns.google on 13 October 2026; of the 18 gateway domains 13 had mail exchangers; txt.att.net and mms.att.net had none, the two Sprint domains answered NXDOMAIN and sms.myboostmobile.com answered SERVFAIL. The story text in the repository says 12 of the other 16 had them; the recorded answers count 13, and this deck uses the recorded count. The chapter's own list of disadvantages is that a gateway is not guaranteed to work, does not say whether the message was delivered, "
        "and may stop working; the notices are the proof. Delivery through any gateway and anything about Twilio beyond one unauthenticated request were NOT EXECUTED.",
        STORY["Att2025"]["lesson"] + ".", notexec=True, recorded=True)

# ---- 17 how long a text can be -------------------------------------------------------------------------------------------------
pn = "segmentsCut_v1_0_0.py"
a17, b17 = span(pn, "print('140 * 8")
f17 = bestfs(pn, (a17, b17), 5.3, 3.2)
w17 = pw(pn, (a17, b17), True, f17)
p17, bot17 = prog(pn, 0.5, 1.55, w17, fs=f17, lines=(a17, b17), show_out=True)
x17 = round(0.5 + w17 + 0.25, 2)
content("How long a text can be", "160 characters in GSM-7, 70 in UCS-2; one stray character changes the count",
        [p17,
         card("The phone's coding", "140 bytes of 8 bits hold 160 characters of 7 bits; { costs two. One dotless i makes the text UCS-2 at 16 bits, so 70 fit.",
              x17, 1.5, round(9.5 - x17, 2), 1.95, fs=9.5, accent="slate"),
         card("NOT EXECUTED here", "The 153 and 67 characters of each part of a longer text come from a 6-byte header, (140 - 6) * 8 // 7 and (140 - 6) // 2; no page opened by this study confirms them.",
              x17, 3.55, round(9.5 - x17, 2), 1.4, fs=9, accent="orange"),
         foot(hidden(pn, a17, "imports and the GSM-7 table written for this study") + " No message is sent and no carrier is asked.", 0.5, round(bot17 + 0.06, 2), w17, fs=8.5)],
        "The chapter says an SMS gateway limits a message to 160 characters. Twilio's page explains the arithmetic: a message carries 140 bytes of 8 bits, which hold 160 characters of 7 bits, and a character such as { needs an escape and counts as two. The program counts with a GSM-7 table written for this study: 160 characters of the basic set fit one message and 161 need two, and {x} costs 5. "
        "One character outside the table, the dotless i of Yedekleme tamamlandı, turns the whole text into UCS-2 at 16 bits a character, so 70 characters fit one message and 71 need two; the same text written without the dotless i is GSM-7 and counts 20. "
        "The segment sizes for longer texts, 153 and 67 characters, follow from a six-byte header on each part; they are arithmetic and were not found on a page opened by this study, so the slide says NOT EXECUTED and does not print a row that depends on them. The segments of the program use them only for texts longer than 160 or 70, which no row of the slide has. "
        + story_notes("Papworth1992"),
        "Count the characters in the coding the phone uses, not in Python.", notexec=True)

# ---- 18 publishing -------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("PostingAPushNotification", "sequence", (0.5, 1.4, 4.4, 3.2), fs=8, head_w=1.1)
pn = "ntfyPubCut_v1_0_0.py"
a18, b18 = span(pn, "srv, log, base")
f18 = bestfs(pn, (a18, b18), 4.55, 2.7)
w18 = pw(pn, (a18, b18), True, f18)
p18, bot18 = prog(pn, 5.0, 1.4, w18, fs=f18, lines=(a18, b18), show_out=True)
content("Publishing a push notification", "A post is an HTTP request: the body is the message, the headers add title and priority",
        [dg, dcap, p18,
         foot(SAY_NTFY + " " + hidden(pn, a18, W_NTFY), 5.0, round(bot18 + 0.04, 2), 4.5, fs=8),
         foot("NOT EXECUTED: nothing was published to ntfy.sh, the ntfy app or any subscriber.", 5.0, round(bot18 + 0.04 + 0.5, 2), 4.5, fs=8)],
        "The sequence diagram is the exchange of the chapter: the program calls requests.post() with the topic URL and the text, the service answers with a Response with status 200, a subscriber checks the topic and receives the message, and the program can poll the same topic with requests.get(). "
        "The program ran requests against a recorder on 127.0.0.1 that logs what it receives; it is not ntfy and says nothing about what ntfy.sh does. The post arrived as POST /AlSweigartZPgxBQ42 with the body b'Hello, world!', a Content-Length of 13 and no Content-Type. "
        "The headers Title, Tags and Priority of the chapter's second example arrived unchanged, each as a header of the request. The research asked ntfy.sh only twice, with GET: its health endpoint answered 200 with healthy true, and a poll of a random unused topic answered 200 with an empty body, so nothing was published. "
        "The real ntfy server could not be downloaded, because github.com answered 403, and the app, the delivery to a phone and a subscriber were NOT EXECUTED. " + "The service is documented to allow 250 messages a day on ntfy.sh without an account, and the chapter says so.",
        "A post is a request; the headers carry the title, tags and priority.", notexec=True)

# ---- 19 headers and bytes ---------------------------------------------------------------------------------------------------------
pn = "ntfyHdrCut_v1_0_0.py"
a19, b19 = span(pn, "srv, log, base")
f19 = bestfs(pn, (a19, b19), 5.9, 3.15)
w19 = pw(pn, (a19, b19), True, f19)
p19, bot19 = prog(pn, 0.5, 1.4, w19, fs=f19, lines=(a19, b19), show_out=True)
x19 = round(0.5 + w19 + 0.25, 2)
pins = EX["_pins"]["transcript"].split("\n")
content("Headers, bytes and a refused post", "A Turkish word in a header fails; a body is UTF-8; a 429 does not raise",
        [p19,
         card("A header is latin-1", "Requests encodes header values as latin-1, so a Title with the dotless i fails with UnicodeEncodeError, and the integer 5 for Priority with InvalidHeader.",
              x19, 1.5, round(9.5 - x19, 2), 1.7, fs=9.5, accent="orange"),
         card("Recorded, pinned", "Appendix A pins requests 2.32.3. In that environment: %s; %s." % (pins[0].replace(" | ", ", "), pins[2].replace("Priority 5 -> ", "Priority 5 gives ")),
              x19, 3.3, round(9.5 - x19, 2), 1.6, fs=9, accent="slate"),
         foot(SAY_NTFY + " " + hidden(pn, a19, W_NTFY), 0.5, round(bot19 + 0.06, 2), w19, fs=8.5)],
        "A header value must be latin-1 and a string. The program shows two ways it fails: Priority given as the integer 5 raised InvalidHeader, and a Title with the dotless i of Yedekleme tamamlandı raised UnicodeEncodeError before any request was sent, so a Title in Turkish fails while the book's English Title and its Priority written as a string work. "
        "A body given as a string is sent as UTF-8: the 20 characters of Yedekleme tamamlandı were 21 bytes on the wire, b'Yedekleme tamamland\\xc4\\xb1', with a Content-Length of 21; the body of 13 characters on the previous slide went with no Content-Type, and the pinned Requests of the card sent none either, so the receiver has to assume the charset. "
        "The limit of ntfy is 4,096 bytes, not characters, as a later slide shows, and the documentation says a longer message is treated as an attachment, which the chapter does not say. The second half of the program has the recorder answer 429 with the JSON body of a limit reached: post() returned a Response whose ok was False and raised nothing, "
        "so a program that notifies about a long job fails silently when a limit is reached; only raise_for_status() raised HTTPError.. The card records what the research found with the Requests 2.32.3 that Appendix A of the book pins, in an environment of its own: the same prepared body and the same InvalidHeader as the newest requests, 2.34.2.",
        "Send bytes you can name: a UTF-8 body and latin-1 headers.", recorded=True)

# ---- 20 receiving --------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("ReadingMessagesFromANtfyTopic", "activity", (0.5, 1.4, 4.1, 3.2),
                   grid={"get": (0, 0), "since": (0, 1), "split": (0, 2), "parse": (0, 3), "ev": (0, 4), "wait": (0, 5), "read": (1, 4)},
                   cols=[(0.0, 2.2), (2.55, 1.55)], rows_n=6, starts=(1, 0), ends={"type": "dot", "col": 1, "row": 5},
                   routes={("start", "get"): "h", ("ev", "read"): "h", ("read", "wait"): "vh", ("wait", "get"): "loopL", ("wait", "end"): "h"}, fs=8, nh=0.5, dh=0.5)
pn = "ntfyPollCut_v1_0_0.py"
a20, b20 = span(pn, "srv, log, base")
f20 = bestfs(pn, (a20, b20), 4.75, 2.7)
w20 = pw(pn, (a20, b20), True, f20)
p20, bot20 = prog(pn, 4.75, 1.4, w20, fs=f20, lines=(a20, b20), show_out=True)
content("Receiving: poll, lines and JSON", "A poll answer is one JSON object on each line; json.loads of the whole text fails",
        [dg, dcap, p20,
         *stack([SAY_NTFY + " " + hidden(pn, a20, W_NTFY),
                 "Recorded 13 Oct 2026: ntfy.sh/v1/health answered 200. NOT EXECUTED: any message sent to or received from ntfy.sh."],
                4.75, round(bot20 + 0.04, 2), 4.75, fs=8)],
        "The flow chart is the polling loop of the chapter: call requests.get() with the topic URL that ends in /json?poll=1, add since to get the messages of the last minutes, split the text of the answer into lines, parse each line with json.loads(), and ask whether the event is a message; if it is, read the message, the title, the priority and the tags, and in either case wait before the next poll. "
        "The chapter says to poll once a minute or every few minutes. The recorder answered with the two lines the book prints, and the program shows what the book does not: json.loads() of the whole text raised JSONDecodeError, Extra data, because it is not one JSON document; splitlines() and json.loads() on each line worked; the second object has the keys priority, tags and title that the first lacks, so a program must allow for keys that are absent; "
        "and, in the longer run of the recorder, program ntfyPollParse, expires minus time is 43,200 seconds, twelve hours. In that longer run the documentation listed event types that the book does not, message_delete and message_clear. The timestamp 1797823712 is 21:28:32 in America/Chicago and 03:28:32 on the next day in UTC, which is why the book's printed date holds only at UTC-6. "
        "In a longer run of the same recorder, program ntfyPollParse, which is not on the slide, a blank line, which a stream sends as a keepalive and which a trailing newline also makes, raised JSONDecodeError again, so a program that splits lines should skip empty ones. "
        "The research asked ntfy.sh only with GET; the health endpoint answered 200 and a poll of an unused topic answered 200 with an empty body, and no message was published or received, which the slide marks NOT EXECUTED.",
        "A poll answer is one JSON object on each line.", notexec=True, recorded=True)

# ---- 21 secrecy ------------------------------------------------------------------------------------------------------------------------
pn = "secrecyCut_v1_0_0.py"
a21, b21 = span(pn, "book = ")
f21 = bestfs(pn, (a21, b21), 5.2, 2.6)
w21 = pw(pn, (a21, b21), True, f21)
p21, bot21 = prog(pn, 0.5, 1.55, w21, fs=f21, lines=(a21, b21), show_out=True)
x21 = round(0.5 + w21 + 0.25, 2)
ch = EX["_charts"]["topicBits"]
chart = {"t": "chart", "ctype": "bar", "x": x21, "y": 1.45, "w": round(9.5 - x21, 2), "h": 2.55, "labels": ch["labels"],
         "title": "Bits in a topic name", "series": [{"name": "bits", "data": ch["values"]}], "dataLabels": True, "dlFs": 10}
content("The topic name is the password", "Anyone who knows the name can read and post; the limit is 4,096 bytes, not characters",
        [p21, chart,
         foot(hidden(pn, a21, "imports and a comment") + " Arithmetic only; nothing is published.", 0.5, round(bot21 + 0.06, 2), w21, fs=8.5),
         foot("ntfy's FAQ says that without access control the topic name is the password, and the chapter says to treat it like one. The name of the book's example is half the author's name and half 8 random characters.",
              x21, 4.1, round(9.5 - x21, 2), fs=9.5)],
        "The topic name is part of the URL, https://ntfy.sh/ and the name, so it appears in logs, proxies and browser history, and ntfy's FAQ says that without access control the topic name is the password. The random part of the book's example, ZPgxBQ42, is 8 characters of 62, which is 47.6 bits; the other half of the name is the author's name, which is guessable. "
        "secrets.token_urlsafe(16) gives 22 characters and 128 bits, and token_urlsafe(32) 256, as the chart shows; the bars are computed from 8 times log2(62) and from the byte counts, and the deck check computes them again. The chapter says that anyone can post to a topic and that there is no way to know who posted a message, so the sender has to be written inside the text. "
        "The limit of 4,096 bytes is bytes: 4096 ASCII characters are 4096 bytes, and 2049 dotless i characters are 4098 bytes, over the limit. At 250 messages of 4096 bytes a day, a program that notifies about a long job stays inside the limits of the service; the service allows 250 messages a day, one every 345.6 seconds on average. "
        "None of this published anything to ntfy.sh. The program is arithmetic and uses only the standard library.",
        "The topic name is the only secret, so make it random.")

# ---- 22 umbrella and unsubscriber -------------------------------------------------------------------------------------------------
pn1, pn2 = "unsubCut_v1_0_0.py", "umbrellaCut_v1_0_0.py"
a22, b22 = span(pn1, "p = P()")
a22b, b22b = span(pn2, "print('text has rain")
f22 = bestfs(pn1, (a22, b22), 5.0, 3.1)
w22 = pw(pn1, (a22, b22), True, f22)
p22, bot22 = prog(pn1, 0.5, 1.4, w22, fs=f22, lines=(a22, b22), show_out=True)
x22 = round(0.5 + w22 + 0.2, 2)
f22b = bestfs(pn2, (a22b, b22b), round(9.5 - x22, 2), 1.3)
p22b, bot22b = prog(pn2, x22, 1.4, pw(pn2, (a22b, b22b), True, f22b), fs=f22b, lines=(a22b, b22b), show_out=True)
content("Umbrella Reminder and Auto Unsubscriber", "Compare a number, not a word; read the header, not the HTML",
        [p22, p22b,
         foot(SAY_BROWSER + " " + hidden(pn1, a22, "imports, the parser class and the sample HTML"), 0.5, round(bot22 + 0.03, 2), w22, fs=8),
         *stack([SAY_FORECAST + " " + hidden(pn2, a22b, "imports, the two sample periods and two helpers"),
                 "Recorded 13 Oct 2026: api.weather.gov answered the point lookup for Chicago and its forecast with 14 periods, each with a probabilityOfPrecipitation; this deck does not run that again."],
                x22, round(bot22b + 0.06, 2), round(9.5 - x22, 2), fs=8.5)],
        "Two of the chapter's practice programs, with the weakness each has. Umbrella Reminder scrapes the text of a forecast for the word rain. Searching the text of two sample periods found it in neither, so it missed the period with a chance of precipitation of 60 that a comparison of the number with a limit of 40 flagged; "
        "the periods on the slide are sample data written in the shape of the answer of api.weather.gov, not forecasts. The research asked api.weather.gov for a point in Chicago on 13 October 2026 and its forecast came back with 14 periods, each with a probabilityOfPrecipitation number, a number to compare where the chapter's scraping gives text; that record is not run again. "
        "Auto Unsubscriber finds links whose text says unsubscribe. The parser found 1 of 4 links, because an image link and the text opt out are missed. The List-Unsubscribe header of RFC 2369, with List-Unsubscribe-Post of RFC 8058, gives a mailto: and an https: address without parsing any HTML. "
        "The browser is a stand-in: webbrowser.open was replaced by a recorder, because opening a link from an unknown sender with a browser confirms to the sender that the address is read. The book suggests Beautiful Soup, which Appendix A pins at 4.12.3; this program uses html.parser from the standard library. The chapter's two programs are not in the online materials. "
        + story_notes("Thuerk1978"),
        "Compare a number, not a word; read the header, not the HTML.", recorded=True)

# ---- 23 control by email -------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("ControllingAComputerByEmail", "activity", (0.5, 1.4, 3.7, 2.8),
                   grid={"check": (0, 0), "pw": (0, 1), "allow": (0, 2), "run": (0, 3), "wait": (0, 4), "del": (0, 5), "sleep": (0, 6)},
                   cols=[(0.25, 2.75), (3.2, 0.5)], rows_n=8, starts=(1, 0), ends={"type": "dot", "col": 0, "row": 7},
                   routes={("start", "check"): "h", ("pw", "del"): "loopR", ("allow", "del"): "loopR", ("sleep", "check"): "loopL"}, fs=8, nh=0.28, dh=0.33)
pn = "controlCut_v1_0_0.py"
a23, b23 = span(pn, "SECRET = ")
f23 = bestfs(pn, (a23, b23), 5.2, 2.2)
w23 = pw(pn, (a23, b23), True, f23)
p23, bot23 = prog(pn, 4.3, 1.4, w23, fs=f23, lines=(a23, b23), show_out=True)
c23, bot23c = con("shell", 4.3, round(bot23 + 0.05, 2), 5.2, fs=7.5, cap=False)
assert "FileNotFoundError" in PROGS["emailControlLoop_v1_0_0.py"]["transcript"] and "TypeError" in PROGS["emailControlLoop_v1_0_0.py"]["transcript"]
content("Email-Based Computer Control", "Check the password, run only an allow-list, never pass the subject to a shell",
        [dg, dcap, p23, c23,
         foot("Stand-in mailbox: a list, a local stand-in. " + hidden(pn, a23, "imports, mailbox"), 4.3, round(bot23c, 2), 5.2, fs=8),
         foot("NOT EXECUTED: the Popen of qBittorrent on Windows or macOS; Linux raised FileNotFoundError.", 0.5, round(dcap["y"] + dcap["h"] + 0.04, 2), 3.7, fs=8)],
        "The flow chart is one pass of the loop of the chapter's last practice program: check the mail for instructions, ask whether the password is in the message, run the program with Popen, wait for it with wait(), delete the emails the loop handled, and wait fifteen minutes. The diagram adds the test the chapter lacks, whether the command is on an allow-list. "
        "The program takes the mailbox as a list in memory, a stand-in for IMAP; the IMAP version, with three messages arriving by SMTP and read, deleted and expunged against dovecot, is a record of the research and is not run again. The password is compared with hmac.compare_digest(), which refuses a str that is not ASCII with TypeError, so the program compares bytes. "
        "A wrong password answered bad password, a command not on the allow-list, rm, was refused, and an allowed one ran and returned its exit code. The console below the program shows why the command must never be built from the text of an email: run through a shell, the subject status; echo PWNED ran two commands, and as a list the same text was one argument. "
        "The chapter's own example starts qBittorrent with a Windows path, which raised FileNotFoundError on Linux; Windows and macOS were NOT EXECUTED. The chapter also asks for a password in the email; a password in an email travels in clear text through every server unless every hop uses TLS, which is the reason for the STARTTLS slide. "
        "The chapter's last sentence sends a stuck reader to the book page for an example implementation, and that page holds none.",
        "Run only an allow-list, check the password, never use a shell.", notexec=True)

# ---- 24 summary: the mind map --------------------------------------------------------------------------------------------------------
dg, dcap = diagram("SendingEmailTextsAndPushesAtAGlance", "mindmap", (0.5, 1.4, 9.0, 3.2), fs=9, root_w=2.0)
content("The chapter in one map", "Six branches; the slides of each branch hold the examples",
        [dg, dcap],
        "These six branches are the route of the deck. The Gmail API: the token file is a password, a reply keeps the thread id only, and a file name with a path is written outside the folder. The standard library: STARTTLS comes before the login, a Bcc recipient is in the envelope, and IDLE is new in Python 3.14. "
        "SMS email gateways: AT&T ended its gateway in 2025, Verizon ends its gateway in 2027, and a text holds 160 characters in GSM-7 and 70 in UCS-2. ntfy: the topic name is the password, the limit is 4,096 bytes, and the answer to a poll is one JSON object on each line. Trust in an email: the envelope and the From header differ, a line break in a header is refused, "
        "and a command in a subject needs an allow-list. The book and its practice: the online materials hold no file for the chapter, the second edition taught smtplib, and the forecast has a chance of precipitation that the chapter's search for the word rain misses. "
        "Together they answer the first question of the chapter, which parts of a program that reaches a person can be shown to work and which can only be shown to fail, and the slides that say where a printed line differs answer the second. The map is drawn from the same specification as the interactive page.",
        "If a branch feels unproven, its slides hold the example.")

# ---- 25 resources ----------------------------------------------------------------------------------------------------------------------------
PUB = {p[0]: p for p in RD.PUBS}
_read = [["The textbook, chapter 20 - free online", PUB["P01"][2]],
         ["email.message documentation", PUB["P22"][2]],
         ["smtplib documentation", PUB["P20"][2]]]
_ref = [["Gmail API: sending email", PUB["P49"][2]],
        ["ntfy: publishing", PUB["P15"][2]],
        ["ntfy: subscribe through the API", PUB["P16"][2]]]
_hist = [["Ray Tomlinson (Wikipedia)", STORY["Tomlinson1971"]["link"]],
         ["Email spam (Wikipedia)", STORY["Thuerk1978"]["link"]],
         ["SMS (Wikipedia)", STORY["Papworth1992"]["link"]],
         ["AT&T ends email-to-text", STORY["Att2025"]["link"]]]
_pkg = [["ezgmail on PyPI", PUB["P09"][2]],
        ["requests on PyPI", PUB["P10"][2]]]
LINKS = [r[1] for r in _read + _ref + _hist + _pkg]
json.dump({"_version": __version__, "links": LINKS}, open(os.path.join(HERE, "links_v1_0_0.json"), "w"), indent=1)
content("Where to go from here", "Every link was opened on the day this deck was made",
        [{"t": "links", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.55, "fs": 9.5, "groups": [
            {"head": "Read", "rows": _read}, {"head": "Reference", "rows": _ref}, {"head": "History and standards", "rows": _hist},
            {"head": "The two packages", "rows": _pkg}]}],
        "Every link on this slide was opened on the day the deck was made, and the build records the status each answered. The textbook chapter is free to read online and holds every listing of the chapter; the documentation of email.message and smtplib describes the standard library that the chapter names only to say EZGmail is better, and imaplib has its own page that is not linked here. "
        "The reference links are the Gmail API's guide to sending and the two pages of the ntfy documentation that the chapter relies on; the RFC that defines SMTP is told in the notes of the slide about SMTP. The history links are the sources behind four of the six stories of the chapter: Ray Tomlinson and the @ sign, the first spam, the first text message, and AT&T switching off email-to-text. "
        "The other two, the launch of Gmail and RFC 821, are told in the notes of the slide of the setup and of the slide of SMTP without a link here. The two packages whose versions the deck records are ezgmail and requests. "
        "The rest of the seventy-odd sources of the research, among them the RFCs, the pages of the Gmail API, the notices of the carriers and the manual pages of the Python modules, are in the research package.",
        "Textbook, documentation, notices and history, all opened today.")

# ---- 26 closing ---------------------------------------------------------------------------------------------------------------------------------
content("What you should now be able to say", "Four claims, each carried by a result you saw printed",
        [{"t": "bullets", "x": 0.6, "y": 1.5, "w": 8.8, "h": 2.4, "fs": 15, "items": [
            "EZGmail needs credentials and a token; the token is a password, and a reply keeps only the thread id.",
            "Use STARTTLS and a verified context; the envelope decides who gets the mail, not the From line.",
            "A gateway can be switched off; count a text in the phone's coding, and a topic name is a password.",
            "Check the password, run an allow-list, and never pass the text of an email to a shell."]},
         {"t": "chips", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.6, "fs": 13, "big": True,
          "items": ["%d console rows" % ROWS_SHOWN, "%d programs run" % len(PROGS), "8 diagrams"]}],
        "Four claims, each carried by a result you saw printed. If you can say them in your own words and run the examples yourself, you have the chapter. The console rows use only the standard library and no clock, so they can be typed into any Python and give the same text on any day; the email package, json, hmac, html.parser and secrets also run in a Python in a browser, "
        "while the programs that need a server, smtplib against aiosmtpd, ezgmail, requests against a recorder and subprocess, need a computer. The rows were run again under Python 3.14.6 each time the deck was built, and the programs were run again by the check that compares the slides with the recording. "
        "What was not run is marked on its slide: a Google account, Gmail's servers, a text through a carrier or Twilio, ntfy.sh, Windows and macOS, and Python 3.14.7 and later with the final 3.15.0. Nothing was ever sent to a person. The next chapter of the book makes graphs and manipulates images, and what this chapter taught about checking what a program sends and trusting what it receives carries over.",
        "Questions are welcome; bring an email problem to run.")

# ---- agenda ---------------------------------------------------------------------------------------------------------------------------------------
_t = {s["title"]: i + 1 for i, s in enumerate(S)}
_parts = [("The Gmail API through EZGmail", "What a program can do with Gmail", "Replies, search, quoted text, downloads"),
          ("The standard library: messages, SMTP, IMAP", "An @ between the user and the machine", "What changed in Python's mail modules"),
          ("Texts through SMS email gateways", "SMS email gateways, and the end of one", "How long a text can be"),
          ("Push notifications with ntfy", "Publishing a push notification", "The topic name is the password"),
          ("Trust and the practice programs", "Umbrella Reminder and Auto Unsubscriber", "Email-Based Computer Control"),
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
S[1]["take"] = "Six parts, from an account to a command sent by email."
S[1]["notes"] = ("The route has six parts. It starts with the Gmail API through EZGmail: what a program can do with one account, the setup with a credentials file and a token file, sending with attachments, cc and bcc, reading threads and messages, "
                 "and replies, search, quoted text and downloads. Then the standard library, which the chapter names only to say EZGmail is better: the story of the @ sign, building a message, headers and addresses, SMTP with STARTTLS, "
                 "refused recipients and the envelope, reading mail with IMAP, and what changed in Python's mail modules between 3.11 and 3.15. The third part is texts: the gateway table and the end of one gateway, and how long a text can be. "
                 "The fourth is push notifications with ntfy: publishing, headers and bytes, receiving by polling, and the topic name that is the password. The fifth is trust and the practice programs: Umbrella Reminder, Auto Unsubscriber and Email-Based Computer Control. "
                 "The last part is a one-map summary and the resources. The ranges name the exact slides, so you can return to the part you need. Two of the slides are true stories and four more are told in the notes; the eight narrative diagrams of the chapter are drawn from the same specifications as the interactive page. "
                 "Every output was printed by Python 3.14.6 with ezgmail 2026.4.28, requests 2.34.2 and aiosmtpd 1.4.6, a server was always a local stand-in, and what could not be run is marked on its slide.")

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
plan = {"meta": {"title": "Ch. 20: Email, Texts, and Push", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": len(S), "diagrams": SHOWN, "notExecuted": NOTEXEC, "recorded": RECORDED,
                 "standin": {str(k): v for k, v in STANDIN.items()}}, "slides": S}
if LATE:
    raise SystemExit("REFUSED:\n" + "\n".join(LATE))
out = os.path.join(HERE, "deck_plan_v1_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides; diagrams on slides", dict(sorted(SHOWN.items(), key=lambda kv: kv[1])), "; NOT EXECUTED on slides", NOTEXEC, "; Recorded on slides", RECORDED)

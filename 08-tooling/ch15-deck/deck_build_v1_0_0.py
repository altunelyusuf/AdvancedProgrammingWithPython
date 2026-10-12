#!/usr/bin/env python3
"""Builds deck_plan_v1_0_0.json - SEN0414 chapter 15 (Google Sheets) on the CME classroom standard.

Same regime as chapters 10 to 14: numbered warm-ivory slides, an agenda with exact slide ranges, a summary before the
resources, full-sentence takeaway strips, stories with fact rows, consoles and whole programs (or honest excerpts of them,
labelled with their line numbers) with their results as Python printed them. Every console result and program transcript comes
from examples_out_v1_0_0.json (made by examples_run_v1_0_0.py under Python 3.14.6 with ezsheets 2026.4.28); the speaker notes are
prose for the reader and carry only what the chapter's RDODI research package (03-materials/ch15/rdodi,
sen0414_ch15_rdodi_data_v1_0_1.py, findings F1 to F14), its records (08-tooling/ch15-page/*.json) or a program of this deck
established.

What this chapter adds against chapter 14, and why it is the honesty chapter: Google itself was never reached, because no Google
account, OAuth consent or live API call was available. Every spreadsheet output on a slide is the real EZSheets library (with the
real google-api-python-client) talking to a stand-in for Google's HTTP answers that the research step wrote (class G, the first
lines of each program), or a CSV export of a real public sheet read through that stand-in (the recorded fixtures). Each slide that
shows such output says so in a visible line, and honesty_check_v1_0_0.py refuses a deck in which it does not. What needs a Google
account (the console steps, a real sign-in, Google's parsing of USER_ENTERED values, Google's quota answers, the limits of a sheet) is
marked NOT EXECUTED on the slide or told as read from Google's pages in the notes, and never shown as a result.
The eight narrative diagrams of the chapter (sen0414_ch15_diagrams_v1_0_0.py, grounding 0.84 or more) are drawn as native shapes
(diagram_shapes_v1_0_0.py: the chapter 14 drawer plus a four-state diagram) and checked by diagram_check_v1_0_0.py; one table (the
Boringcoin balances) and one chart (the pauses of the library's retry) are native PowerPoint objects whose data the deck check
computes again; no photograph is used, because the research found none it could fetch and licence; two of the six stories are
slides (Google Sheets from XL2Web, Nakamoto's message) and four are told in the notes.

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


ST = load("stories4151", os.path.join(HERE, "..", "sen0414_ch15_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
DG = load("diagrams4151", os.path.join(HERE, "..", "sen0414_ch15_diagrams_v1_0_0.py"))
NODES = DG.nodes_from_ttl(os.path.join(HERE, "..", ".."))
_bad = DG.run_checks(NODES)
if _bad:
    raise SystemExit("REFUSED: the diagrams fail their own checks: %r" % _bad[:3])
DIAG = {d["id"]: d for d in DG.DIAGRAMS}
RD = load("rdodi4151", os.path.join(HERE, "..", "sen0414_ch15_rdodi_data_v1_0_1.py"))
EX = json.load(open(os.path.join(HERE, "examples_out_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s" % PYV
G = {k: [[s, (o or "")] for s, o in v] for k, v in EX.items() if not k.startswith("_")}
PROGS = EX["_programs"]
CQ1, CQ2 = RD.CQS
CW = 0.0088  # inches per character per point of Courier New, as the shared fit check measures it

# the honesty lines (honesty_check_v1_0_0.py requires the phrase of a program's kind on every slide that shows that program)
L_STANDIN = "Stand-in for Google: this output comes from the real EZSheets library talking to a stand-in written for this study, not from Google."
L_FIXTURE = "Stand-in for Google, recorded fixture: rows from the CSV export of the public sheet; the requests went to a stand-in, not to Google."
L_NOTEXEC = "NOT EXECUTED"


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


def span(pname, first, last=None):
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


def tw(pname, fs=7.0):
    """The panel width the transcript of a program needs on its own at fs points."""
    t = PROGS[pname]["transcript"].split("\n")
    return round(max([len(t[0]) + 7] + [len(z) for z in t[1:]]) * CW * fs + 0.4, 2)


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


def transcript(pname, x, y, w, fs=7.0, label=None):
    """The transcript of a program in a panel of its own. With a label of the form 'transcript of program <name>' the panel is
    re-run by program_check and must equal the recording; with another label it is the transcript of a program whose
    excerpt is on the slide, which the program check also requires to be on that slide."""
    label = label or "transcript of program %s" % pname
    out = PROGS[pname]["transcript"]
    t = out.split("\n")
    need = round(max([len(t[0]) + 7] + [len(z) for z in t[1:]]) * CW * fs + 0.4, 2)
    if need > w + 0.005:
        raise SystemExit("REFUSED: transcript of %s cannot fit unwrapped in %.2f in at %.1f pt (needs %.2f)" % (pname, w, fs, need))
    if len(label) > (w - 0.1) / 0.0725:
        raise SystemExit("REFUSED: label %r is too long for a %.2f in panel" % (label, w))
    L = len(t)
    h = round(L * (fs * 1.22 / 72.0 + 0.02) + 0.30, 2)
    return {"t": "prog", "x": x, "y": y, "w": w, "h": h, "lines": [], "fs": fs, "compact": True, "out": out,
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
    fn = {"activity": DS.activity, "sequence": DS.sequence, "states": DS.states4, "usecases": DS.usecases, "mindmap": DS.mindmap}[kind]
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


def content(title, sub, items, notes, take, lede=None, notexec=False):
    if lede and len(lede.split()) > 34:
        raise SystemExit("REFUSED: lede on %r runs past the gate" % title)
    if len(take.split()) > 24 or not take.endswith("."):
        raise SystemExit("REFUSED: takeaway %r is not a short full sentence" % take)
    if len(title) > 53:
        raise SystemExit("REFUSED: title %r is longer than 53 characters" % title)
    if len(sub) > 92:
        raise SystemExit("REFUSED: subtitle %r is longer than the line it is set on" % sub)
    for it in items:
        if it["t"] in ("code", "prog", "shapes", "card", "boxes", "chips", "stat", "beats", "factrow", "numlist", "bullets", "links", "foot", "text", "img", "table", "chart"):
            if it["y"] + it.get("h", 0.4) + (0.26 if it.get("cap") and it["t"] == "code" else 0) > 5.0 or it["x"] + it["w"] > 9.56:
                raise SystemExit("REFUSED: item %s on %r reaches y %.2f / x %.2f" % (it["t"], title, it["y"] + it.get("h", 0.4), it["x"] + it["w"]))
        if it["t"] == "shapes":
            SHOWN[it["did"]] = len(S) + 1
    if notexec:
        NOTEXEC.append(len(S) + 1)
        if not any(L_NOTEXEC in json.dumps(it) for it in items):
            raise SystemExit("REFUSED: slide %r is declared NOT EXECUTED but says nothing of it" % title)
    sl = {"kind": "content", "title": title, "sub": sub, "items": items, "notes": notes, "take": take, "bg": "light"}
    if lede:
        sl["lede"] = lede
    S.append(sl)


# ---- 1 title ---------------------------------------------------------------------------------------------------
c1, _ = con("title", 5.0, 0.85, 4.5, fs=10.5)
S.append({"kind": "title", "title": "Chapter 15: Google Sheets",
          "sub": "How a program reads and writes a Google spreadsheet: EZSheets, sign-in, sheets and cells, quotas and Project 11",
          "items": [c1, foot("Google was never reached for this deck: every output is from a stand-in for Google or from a recorded fixture, and each slide says which.", 0.6, 3.85, 8.8, fs=11)],
          "notes": "Chapter 14 worked on files that a program opens from its own disk. Chapter 15 reaches a spreadsheet that lives on Google's "
                   "servers, so every read and every write becomes a request sent over the web, and before the first request the program must "
                   "be allowed in by an account. This deck follows the chapter in its own order: the access to a Google account by a cloud "
                   "project, a credentials file and token files; spreadsheet objects and sheet objects; rows, columns and cells; the quotas; and "
                   "Project 11, a spreadsheet that pretends to be a blockchain. It adds what the chapter leaves out and what the research found "
                   "when each printed output was run again: the token files are Python pickles and so can run code, a token of an app in "
                   "Testing status stops working after seven days, Spreadsheet.Sheet() returns nothing, and two writers can lose a row. One "
                   "thing must be said first. Google itself was never reached, because no Google account, no consent in a browser and no cloud "
                   "project were available. Every spreadsheet output on these slides was made by the real EZSheets library, release 2026.4.28, "
                   "together with the real Google client library, under Python 3.14.6, talking to a stand-in for Google's answers that was "
                   "written for the study; or the rows are the CSV export of a real public sheet, read through that same stand-in. Each such "
                   "slide says so, and what needs a Google account is marked as not executed.",
          "bg": "light"})

# ---- 2 agenda (filled in at the end) -------------------------------------------------------------------------------
S.append({"kind": "content", "title": "Today's route", "sub": "", "items": [], "notes": "", "take": "", "bg": "light"})

# ---- 3 questions ------------------------------------------------------------------------------------------------
content("The questions this chapter answers", "The chapter's own competency questions; the summary comes back to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 2.2, "fs": 13, "items": [CQ1, CQ2]},
         {"t": "chips", "x": 0.5, "y": 3.8, "w": 9.0, "h": 0.5, "fs": 11.5,
          "items": ["6 branches", "%d topics" % len(NODES), "%d console rows" % sum(len(v) for v in G.values()),
                    "%d programs run" % len(PROGS), "8 diagrams", "Python %s" % PYV, "Google never reached"]}],
        "The first question is the chapter's spine. A Google account, a spreadsheet, a sheet, a row or column and a cell are five different "
        "things, and EZSheets gives each its own object or its own call: a credentials file and two token files for the account, a "
        "Spreadsheet for a file in Google Sheets, a Sheet for one tab, lists for a row or a column, and a bracket for a cell. What the "
        "question adds is that every one of these calls is a request to Google, and the deck shows which request each one sends, read from "
        "the requests the library built. The second question is the watch-out of the deck. The chapter's examples are sound in outline, "
        "but several printed results do not hold for the library or the services of today: Sheet() returns nothing, the quota figures "
        "and the cell limit differ from Google's pages, the one-time setup is weekly for an app in Testing status, and the token files "
        "run code when they are loaded. Each slide says where a printed line differs and on what evidence. The chips give the size of "
        "the chapter as this deck covers it: six branches, the topics beneath them, the console rows and the programs that were run, "
        "the eight diagrams, the Python release, and the reminder that Google itself was never reached.",
        "Know which request each call sends; then check what the book printed.")

# ---- 4 EZSheets and what it can do + use cases ------------------------------------------------------------------------
dg, dcap = diagram("WhatAProgramCanDoWithEzsheets", "usecases", (5.65, 1.45, 3.9, 3.15), fs=8)
content("EZSheets and what a program can do with it", "A one-author library that turns each call into a request to Google's services",
        [dg, dcap,
         card("One author, 18 releases", "First uploaded to PyPI on 8 February 2019, newest release 2026.4.28, GPLv3 or later. Its documentation page "
              "is dated November 2019 and names ten of its 35 public names.", 0.5, 1.5, 5.0, 1.55, fs=10.5),
         card("Under it, Google's clients", "It builds on google-api-python-client for the Sheets API v4 and the Drive API v3, and on "
              "google-auth-oauthlib for the sign-in. Every call below is one or more HTTPS requests.", 0.5, 3.2, 5.0, 1.55, fs=10.5, accent="slate")],
        "EZSheets is the work of one author, Al Sweigart. It was first uploaded to the Python Package Index on 8 February 2019, there are 18 "
        "releases, the newest is 2026.4.28, and the licence is GPLv3 or later. Its documentation on Read the Docs is dated November 2019 and "
        "names ten of the 35 public names of the installed library; it does not name getRow, the download methods, listSpreadsheets or "
        "delete, and the last release differs from the one before it only in its version string, so the research read the library's source "
        "and ran it. EZSheets does not speak to Google itself. It depends on google-api-python-client, which builds each request from "
        "Google's discovery document, and on google-auth-oauthlib, which runs the consent; the two base addresses it uses were read from "
        "the clients it builds, sheets.googleapis.com for version 4 of the Sheets API and www.googleapis.com/drive/v3 for the Drive API, "
        "without a network. The use-case diagram lists what a program can do with one Google account: create or upload spreadsheets, list "
        "and delete them, download them in six formats, read and write cells, rows and columns, create, move and delete sheets, and copy a "
        "sheet into another spreadsheet. A second library, gspread, does the same work and has its own documentation; it was not run. "
        "The library's story is short: it reached PyPI in February 2019, and the third edition of the book, published in April 2025 with "
        "672 pages, puts it in chapter 15. Its code is the same under every release of Python 3.14, from 3.14.0 to 3.14.6, and under 3.13 "
        "and 3.12, apart from the pickle protocol number of the token files, which is 5 from Python 3.14 and 4 before.",
        "EZSheets turns each call into a request to Google.")

# ---- 5 story: XL2Web ------------------------------------------------------------------------------------------------
content("Google Sheets began as XL2Web, in 2006", STORY["GoogleSheetsXL2Web2006"]["when"],
        [card("A small company's web spreadsheet", "XL2Web, made by 2Web Technologies, was bought by Google in 2006 and became Google Labs "
              "Spreadsheets, opened to a limited number of users on 6 June 2006.", 0.5, 1.5, 4.5, 2.8, fs=12.5),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "2Web Technologies: Jonathan Rochelle and Farzad Khosrowshahi",
             "2006: Google acquires XL2Web",
             "6 Jun 2006: limited test, first come, first served",
             "Later: a beta for every Google Account holder"]},
         factrow("GoogleSheetsXL2Web2006")],
        story_notes("GoogleSheetsXL2Web2006"),
        "A browser spreadsheet is a service your program calls, not a file it opens.")

# ---- 6 setup: credentials to signed in -------------------------------------------------------------------------------
dg, dcap = diagram("FromCredentialsToSignedIn", "activity", (0.5, 1.45, 5.15, 3.15),
                   grid={"project": (0, 0), "apis": (0, 1), "consent": (0, 2), "creds": (0, 3), "tokens": (1, 3), "ready": (2, 3),
                         "browser": (1, 4), "write": (2, 4)},
                   cols=[(0.0, 1.8), (2.35, 1.45), (4.15, 1.0)], rows_n=5, starts=(1, 0), ends={"type": "dot", "col": 2, "row": 2},
                   routes={("start", "project"): "h"}, fs=8, nh=0.46, dh=0.56)
c, bot = con("pkce", 5.7, 3.5, 3.8, fs=8, label="S256 challenge, on the RFC 7636 example", cap=True)
content("Credentials, tokens and the first sign-in", "Five set-up steps and one test: do valid token files exist?",
        [dg, dcap, c,
         card("NOT EXECUTED here", "The console steps need a Google account: the project, the two APIs, the consent screen, the credentials "
              "download and a real sign-in. Google was never reached; see the notes.", 5.7, 1.45, 3.8, 1.6, fs=10, accent="orange")],
        "This is the chapter's own sequence of steps, drawn as a workflow. The reader creates a Google Cloud project, which has a name that "
        "can be changed and a project ID that cannot; switches on the Sheets API and the Drive API, because EZSheets uses both; sets up the "
        "consent screen and its scopes; and downloads the credentials file into the folder of the script. At the first call the library "
        "looks for valid token files, and when there are none it opens the browser on Google's consent page, waits for the redirect, and "
        "writes the token files. None of the console steps was executed for this deck, because the console needs a Google account, and "
        "that is said here rather than hidden. What could be run without an account was run: the two API clients and their addresses, the "
        "scopes the library asks for, which are the whole spreadsheets scope and the whole drive scope, and the authorization address the "
        "library builds, which has response_type=code, a PKCE code challenge with the method S256, access_type=offline and the redirect "
        "http://localhost:8080/. The console on the right computes the S256 challenge with the standard library from the example verifier "
        "of RFC 7636 and gives the challenge the RFC prints, which is what the library's PKCE step does with a random verifier. The "
        "console has also changed since the book: the consent-screen wizard of the chapter is now three pages of the Google Auth "
        "platform, Branding, Audience and Data Access, so a student has to map each step to the new page, and that mapping was not "
        "executed either. A story sits behind the sign-in. OAuth began around November 2006, when Blaine Cook, who was working on the "
        "Twitter OpenID implementation, met Chris Messina, David Recordon and Larry Halff at a CitizenSpace OpenID meeting and they "
        "concluded that there was no open standard for API access delegation; a Google group followed in April 2007, and the IETF "
        "published RFC 6749 in October 2012. Its authorization code and refresh token are what the token files hold, and the idea is that "
        "a script never learns your password. This account rests on oauth.net and on the RFC. Sheets API version 3 was turned down on "
        "2 August 2021, so the library can only be using version 4.",
        "Set-up is console steps plus one test of the token files.", notexec=True)

# ---- 7 token life cycle ----------------------------------------------------------------------------------------------
dg, dcap = diagram("ATokenFile", "states", (0.5, 1.4, 9.0, 2.45), fs=8.5)
content("A token file: from sign-in to a refused refresh", "Four states; the last is the one the chapter's one-time setup does not mention",
        [dg, dcap,
         foot("NOT EXECUTED against Google: the seven days are Google's rule for an app in Testing status with External users (its identity page "
              "and its audience help add a limit of 100 test users). The refusal was played against a local server that answered invalid_grant; "
              "the library then raised RefreshError and left the stale token-sheets.pickle in place.", 0.5, 4.2, 9.0, fs=10)],
        "The chapter calls the token files a one-time setup that will not happen again. Google's identity page says otherwise for an app "
        "whose publishing status is Testing and whose user type is External: the refresh token expires in seven days, and the help on the "
        "app audience adds a limit of 100 test users and the same seven days. So the diagram follows one token file through four states: no "
        "file, a valid file written by the sign-in in the browser, an expired access token that a refresh token renews, and a stale file "
        "when Google refuses the refresh after seven days. The research could not make Google refuse a refresh, so that event was not "
        "executed against Google. It was played instead against a local server that answered invalid_grant, which is the error RFC 6749 "
        "names for a refresh token that is invalid, expired or revoked. The library then raised google.auth.exceptions.RefreshError with "
        "the text Token has been expired or revoked, which the import swallows with a bare except and the first Spreadsheet() raises "
        "again, and the stale token-sheets.pickle stayed in place. The remedy, deleting the token files and signing in again, follows "
        "from the library's code and was not run. Where there is no browser, as on a server, the library raises webbrowser.Error, swallows "
        "it at import and raises it again at the first Spreadsheet() without printing an address; with the environment variable BROWSER "
        "set to true it printed the authorization address and listened on port 8080. Google's own Python quickstart stores a token.json "
        "file and not a pickle.",
        "Plan for the token to expire: in Testing status the sign-in is weekly.", notexec=True)

# ---- 8 pickle ----------------------------------------------------------------------------------------------------------
pn = "tokenPickleRunsCode_v1_0_0.py"
a8, b8 = 1, len(PROGS[pn]["code"].rstrip("\n").split("\n"))
w8 = pw(pn, (a8, b8), True)
p1, bot = prog(pn, 0.5, 1.55, w8, fs=7.0, lines=(a8, b8), show_out=True)
c, cb = con("pickle", 0.5, round(bot + 0.55, 2), 5.0, fs=9, label="the standard library does the same, harmlessly")
content("The token files are pickles, and a pickle runs code", "Importing ezsheets loads the token file; a tampered file ran a statement before any call",
        [p1, c,
         card("A token file is a program", "The chapter warns that shared files let others read your spreadsheets. It does not say that a token "
              "file you receive from someone else runs code when you import ezsheets. Python's documentation calls pickle not secure.",
              5.7, round(bot + 0.2, 2), 3.8, round(4.9 - bot - 0.2, 2), fs=10, accent="slate")],
        "The library writes two token files, token-drive.pickle and token-sheets.pickle, beside the credentials file, and loads them with "
        "pickle.load when ezsheets is imported. The chapter's own page has a stray space in one of the names and speaks of two token JSON "
        "files although both are pickles. A pickle runs code when it is loaded, because it may name any callable to be called. The program "
        "on the left makes a token file whose pickle calls exec on a statement that writes a file called PWNED.txt, then imports ezsheets "
        "and looks for the marker: it is there, written during the import, before any call of the library. The marker is harmless on "
        "purpose and stands for hostile code. The console on the lower left shows the same idea with the standard library alone: a class "
        "whose __reduce__ names eval makes pickle.loads evaluate the expression 6 * 7 and return 42. Python's documentation says the pickle "
        "module is not secure and that only data one trusts should be unpickled, and OWASP and MITRE list deserialization of untrusted "
        "data as a weakness, CWE-502. The default protocol of the files is the interpreter's, which is 5 from Python 3.14 and 4 before. "
        "The practical rule is that a token file from someone else is a program and not data, which is a reason to keep one account for "
        "the scripts, as the chapter advises, and never to share the folder. This program does not use Google or the stand-in.",
        "Treat a token file as code; never import ezsheets beside a stranger's.")

# ---- 9 spreadsheet objects: the attributes program ---------------------------------------------------------------------------
pn = "spreadsheetAttributes_v1_0_0.py"
t1 = transcript(pn, 0.5, 1.5, 4.95, fs=7.0)
content("Spreadsheet objects: title, sheets, and Sheet()", "Opening and making a spreadsheet; what is read-only; what the printed Sheet objects hide",
        [t1,
         card("Sheet() answers None", "Spreadsheet.Sheet() was added in release 2024.8.8 as a wrapper that returns nothing, so the Sheet objects "
              "the chapter prints do not come from it. createSheet() returns the Sheet.", 5.6, 1.5, 3.9, 1.5, fs=10, accent="slate"),
         card("Three read-only names", "id, url and sheetTitles have no setter: assigning raises AttributeError. sheets is a plain "
              "attribute, so assigning to it replaces the tuple.", 5.6, 3.1, 3.9, 1.3, fs=9.5, accent="orange"),
         foot(L_STANDIN, 5.6, 4.44, 3.9, fs=9)],
        "A Spreadsheet object stands for one file in Google Sheets. The chapter opens it from a URL, an id or a title, makes a new one with "
        "ezsheets.Spreadsheet(), reads its title, id, url, sheetTitles and sheets, and says some of them are read-only. Run against a "
        "stand-in for Google, the library's own code did what the chapter says in most places and differed in the places named here. "
        "Assigning to the title sent one request, a POST of a batchUpdate. The three names id, url and sheetTitles are properties with no "
        "setter, so assigning raises AttributeError with the text property 'id' of 'Spreadsheet' object has no setter in Python 3.14, while "
        "sheets is a plain attribute and assigning to it silently replaces the tuple, as the last lines of the transcript show. The sheets "
        "are a tuple, so item assignment raises TypeError. The surprise is on the line that prints None. In the library's source "
        "Spreadsheet.Sheet() was added in release 2024.8.8 as a wrapper that calls createSheet and returns nothing, so the printed Sheet "
        "objects of the chapter cannot come from it in this release; only createSheet() returns the Sheet. The program has 87 lines: the first 72 "
        "are the lines every program of this chapter begins with, which define the stand-in for Google, lines 73 to 79 load a "
        "one-sheet example spreadsheet into it, copy its sheet into a new spreadsheet, rename that and print the first results, and the "
        "last lines try the three setters; the transcript shows every expression that the program printed beside its answer. A story sits near this slide. Google Forms, introduced in 2008 as "
        "part of the Google Docs suite, saves its answers into a spreadsheet when the owner chooses a destination for the responses, and "
        "that spreadsheet is what the first practice program of the chapter opens with EZSheets; the account rests on Wikipedia and on "
        "Google's help page on where form responses are saved.",
        "Sheet() returns None; createSheet() returns the Sheet.")

# ---- 10 addresses and column letters ------------------------------------------------------------------------------------------
c, bot = con("letters", 0.5, 1.5, 4.5, fs=8, label="column letters in base 26; standard library only")
t2 = transcript("addressesAndLetters_v1_0_0.py", 5.2, 1.5, 4.3, fs=7.0)
content("Addresses and column letters", "A1 notation is a column in base 26 and a row; the library converts both ways",
        [c, t2,
         foot("ZZZ is the last three-letter column, number 18,278; the library agreed with this arithmetic for every number from 1 to 200,000.", 0.5, round(bot + 0.12, 2), 4.5, fs=9)],
        "Google writes a range in A1 notation, a column letter and a row number, and EZSheets converts between that and the numbers its "
        "own calls take. The chapter converts getColumnLetterOf(999) to ALK and getColumnNumberOf('ZZZ') to 18278, and a string address to "
        "a tuple and back. The transcript on the right is the library's own pure functions with no spreadsheet and no stand-in: they "
        "printed the chapter's answers, a lower-case address worked, convertAddress took a tuple, and a column of 0 or a letter where a "
        "number was wanted raised ValueError or TypeError. The console on the left does the same job with the standard library alone, so it "
        "can be typed into any Python: the letters of a column are counted in base 26, but with no zero, which is why the lambda subtracts "
        "one before it divides and why AA follows Z. The three-letter columns end at ZZZ, which is 26 plus 676 plus 17,576, that is 18,278, "
        "the number the library prints. The research checked that the library's two conversions and this arithmetic agree for every number "
        "from 1 to 200,000. One more fact belongs with ranges: the library builds each range for a request, Sheet1!B2:B2 for a cell and "
        "Sheet1!A3:Z3 for a row, and leaves a sheet title unquoted even when it holds a space, while Google's page says single quotes are "
        "required for such a title. Whether Google accepts the unquoted form was not executed.",
        "Column letters are base 26 with no zero; the library refuses the rest.")

# ---- 11 ids, upload, download ---------------------------------------------------------------------------------------------------
pn = "getIdFromUrl_v1_0_0.py"
a11, b11 = span(pn, "ID = '1Tz")
p1, bot = prog(pn, 0.5, 1.55, pw(pn, (a11, b11), True), fs=7.0, lines=(a11, b11), show_out=True)
pn2 = "downloadName_v1_0_0.py"
a12, b12 = span(pn2, "ss = ezsheets.Spreadsheet(g.load('X'")
p2, bot2 = prog(pn2, 0.5, round(bot + 0.25, 2), pw(pn2, (a12, b12), True), fs=7.0, lines=(a12, b12), show_out=True)
content("Opening by URL, and the name of a download", "An id is cut out of a URL by position; a download's file name is made from the title",
        [p1, p2,
         card("URL ending at the id", "getIdFromUrl takes the characters after /spreadsheets/d/ up to the next slash. A URL that "
              "ends right after the id loses its last character; the /u/3/ form raises ValueError.", 6.25, 1.5, 3.25, 1.95, fs=9.5, accent="slate"),
         card("A file name from a title", "Anything but letters, digits, _ and . becomes an underscore, so "
              "the chapter's Sweigart_Books.xlsx is not what the release saves.", 6.25, 3.5, 3.25, 1.25, fs=8.5, accent="orange"),
         foot(L_STANDIN, 0.5, 4.8, 9.0, fs=9)],
        "The chapter opens the same spreadsheet by a short link, by its long URL and by its bare id, and shows that the three give objects "
        "that compare equal. The library adds a fourth way, a title, which it looks up among all the spreadsheets of the account and which "
        "raises an error when two share the title or none does. The id is the part of the address after /spreadsheets/d/ up to the next "
        "slash, and getIdFromUrl cuts it by position. The program on the top left calls that function, which needs no account and no "
        "stand-in, on the public Sweigart Books sheet's address: the /edit#gid=0 form and the form with a closing slash give the whole id, "
        "a URL that ends after the id gives it without its last character, and the /spreadsheets/u/3/d/ form raises ValueError with the text "
        "url argument must be an alphanumeric id or a full URL. The short links of the chapter, autbor.com/boringcoin and "
        "autbor.com/examplegs, depend on something else: for any address that does not start with https://docs.google.com the library "
        "follows redirects itself with http.client over port 80 and sends no User-Agent, and on 12 October 2026 the short-link server "
        "answered such requests 302 or 403 by turns, which left the address None and stopped the library with an AttributeError before any "
        "Google call. The program below it downloads a spreadsheet titled Sweigart Books (DO NOT DELETE) as an Excel file against the "
        "stand-in and prints the name the library chose; the chapter prints Sweigart_Books.xlsx. The six download methods ask Drive for "
        "the MIME types of xlsx, ods, csv, tsv, pdf and zip, and none of them closes the file it opens. What Google sends back, so "
        "whether a CSV holds only the first sheet, was not observed.",
        "Names and ids are derived by rule: check the rule before you trust the result.")

# ---- 12 rows and columns -----------------------------------------------------------------------------------------------------------
pn = "rowsAndColumns_v1_0_0.py"
t1 = transcript(pn, 0.5, 1.5, 4.05, fs=7.0)
a13, b13 = span(pn, "columnOne = sheet.getColumn(1)", "columnOne[i] = value.upper()")
p1, bot = prog(pn, 4.7, 1.55, 4.8, fs=7.0, lines=(a13, b13), show_out=False)
content("Rows and columns as lists", "One call reads a whole row or column; one call writes it back",
        [t1, p1,
         card("One request for a whole list", "updateColumn sent one request with majorDimension COLUMNS, however long the list. "
              "updateRow and updateColumn also pad the list you give them with empty strings, in place.", 4.7, round(bot + 0.15, 2), 4.8, 1.55, fs=10.5, accent="slate"),
         foot(L_STANDIN, 4.7, 4.45, 4.8, fs=9)],
        "The chapter reads a row or a column as a list, changes the list and writes it back, and does the same for all rows at once with "
        "getRows and updateRows. The transcript on the left is the whole run on a ten-row stand-in of produceSales3.xlsx that has the same "
        "columns as the book's file: getRow(1) and getRow(2) are the header and the first record, getColumn('A') equals getColumn(1), "
        "updateRow(3, vals) replaces a record, and the loop that upper-cases a column and writes it back with updateColumn is the excerpt on "
        "the right. The number printed before the word COLUMNS is the number of requests that write made, one, and COLUMNS is the "
        "majorDimension of that request. Two behaviours are not in the chapter. The update calls pad the list they are given with empty "
        "strings in place, and updateRows also extends the caller's list of rows to the size of the sheet, so the caller's list is changed. "
        "And the lists are as wide and as tall as the grid of the sheet, which for the real produce sheet is 23,758 rows by 6 columns, "
        "142,548 cells; clear() on such a sheet sent 617,746 bytes. The real produceSales3.xlsx has four columns, where the "
        "chapter prints rows of six after the upload to Google, and that upload was not executed, so the six cannot be checked. Indexes "
        "start at 1, and a row or column of 0 raises IndexError.",
        "One call writes a row or a column; the list you pass is changed.")

# ---- 13 sheets: create, move, delete -----------------------------------------------------------------------------------------------
pn = "movingSheets_v1_0_0.py"
t1 = transcript(pn, 0.5, 1.5, 4.0, fs=7.0)
a14, b14 = span(pn, "for v in (9, -9, 'x'):")
p1, bot = prog(pn, 4.7, 1.55, 4.8, fs=7.0, lines=(a14, b14), show_out=False)
content("Sheets: create, move and delete", "A sheet's index is its place among the tabs; the library refuses what is out of range",
        [t1, p1,
         card("Index counts from 0 or from -1", "Setting index moves the tab and renumbers the rest. 9 and -9 raise IndexError, 'x' raises TypeError; "
              "a negative index counts from the right.", 4.7, round(bot + 0.15, 2), 4.8, 1.45, fs=10.5, accent="slate"),
         foot(L_STANDIN, 4.7, 4.45, 4.8, fs=9)],
        "The chapter makes sheets, prints a Sheet object for each, moves them with index, deletes them and clears one, then copies a sheet "
        "into another spreadsheet and sees the copy named Copy of the title. On the stand-in the tab order after each change was the "
        "chapter's: a sheet made at index 0 comes first, moving index 0 to index 2 puts it third, and moving it back restores the order. The "
        "excerpt on the right is the part the chapter does not show: an index of 9 or -9 raises IndexError with the allowed range in the "
        "message, a string raises TypeError, and index = -1 moves the sheet to the end. The research also ran the deletions: deleting by "
        "index or by title works, a spreadsheet's last sheet cannot be deleted and the library raises ValueError with the text Cannot delete "
        "all sheets, spreadsheets must have at least one sheet, clear() keeps the sheet and writes an empty string to every cell, and "
        "copyTo names the copy Copy of the title and returns nothing. These were run in the research study against the same kind of "
        "stand-in and are told here from its record. Two sheets compare equal when their sheetId is equal, which is 0 for the first sheet "
        "of every new spreadsheet, so two different spreadsheets' first sheets are equal; and the in operator searches the text of the "
        "coordinates, so 'Alice' in sheet is False.",
        "A sheet's index is its tab position; the library checks it first.")

# ---- 14 write and read: the sequence ---------------------------------------------------------------------------------------------------
dg, dcap = diagram("AWriteAndARead", "sequence", (0.5, 1.4, 5.9, 3.35), fs=8.5, head_w=1.7)
content("A cell written, and a cell read back", "The write goes to Google; the read comes from the library's own copy until refresh()",
        [dg, dcap,
         card("30 or '30'?", "After sheet['B2'] = 30 the chapter prints '30'. Release 2024.8.9 did; releases 2025.11.11 and 2026.4.28 return "
              "the integer 30 until refresh(), which gives '30'.", 6.6, 1.45, 2.9, 1.75, fs=9.5, accent="slate"),
         card("NOT EXECUTED here", "Every write asks Google to parse the value as typed (USER_ENTERED). Whether text becomes a number, "
              "date or formula was never observed.", 6.6, 3.3, 2.9, 1.45, fs=9.5, accent="orange")],
        "The sequence diagram is the chapter's account of one cell. Assigning to sheet['B2'] makes the Sheet object send one write request "
        "to Google; reading the cell afterwards returns what the library holds locally, with no request; and refresh() reads the "
        "spreadsheet again. Two things differ from the chapter and one cannot be checked. The chapter prints the string '30' after the "
        "write. The library's local copy has changed between releases: under 2024.8.9 the same session printed '30', and under 2025.11.11 and "
        "2026.4.28 it printed the integer 30 until the sheet was refreshed, when it became the string '30'; that comparison is the "
        "research's own record of one cell session under three releases of ezsheets on Python 3.14.6, and the next slide shows the "
        "newest release again. The request itself carries valueInputOption USER_ENTERED, which Google documents as parsing the value as "
        "if a person had typed it into the cell, while RAW would store it as given, and a read returns the formatted value unless told "
        "otherwise. So text written by a program may become a number, a date or a formula in Google. The stand-in keeps text and does not "
        "parse a value, so that effect was not executed; what was executed is the request the library sends and the request that RAW would "
        "send through the library's client. The chapter's own Figure 15-2 has the cell A1 as AI in its alt text, a typo of the book and not "
        "of the library.",
        "Writes go to Google; reads come from a local copy until you refresh.", notexec=True)

# ---- 15 what a call sends and costs --------------------------------------------------------------------------------------------------
pn = "writeThenRead_v1_0_0.py"
a15, b15 = span(pn, "sheet = produce()")
p1, bot = prog(pn, 0.5, 1.55, pw(pn, (a15, b15), True), fs=7.0, lines=(a15, b15), show_out=True)
t1 = transcript("requestCounts_v1_0_0.py", 0.5, round(bot + 0.3, 2), 3.55, fs=7.0)
content("What a call sends, and what it costs", "A write is a request; a read of a loaded sheet is none; a size change is three",
        [p1, t1,
         {"t": "stat", "x": 7.3, "y": 1.5, "w": 2.2, "h": 3.2, "vert": True, "items": [
             {"n": "1", "label": "request per write, of a cell or of a list"},
             {"n": "0", "label": "requests to read from a loaded sheet"},
             {"n": "3", "label": "requests to change a size: 2 reads, 1 write"}]},
         card("Step 2 costs six", "A new Boringcoin row is rowCount += 1 (three requests) and three "
              "cell writes: six.", 4.3, round(bot + 0.2, 2), 2.85, round(4.65 - bot - 0.2, 2), fs=9.5, accent="slate"),
         foot(L_STANDIN, 0.5, 4.74, 9.0, fs=9)],
        "Because every call goes over the web, the number of requests is the cost of a program. The program on top writes the integer 30 to "
        "B2 of the stand-in's produce sheet and prints what the library holds, which is the integer 30; then it prints the request the "
        "library sent, a PUT to the range Sheet1!B2:B2 with valueInputOption=USER_ENTERED and a body whose majorDimension is ROWS and whose "
        "values are [[30]]; then it refreshes the sheet and prints the string '30'. The transcript below it is the library counting its "
        "own requests: a hundred cell writes were a hundred PUT requests, a hundred reads of a cell and a hundred of a row made none, "
        "because they are served from the local copy, changing rowCount made three requests, a read of the properties, a read of the "
        "values and a batchUpdate, a title change made one, a refresh of a one-sheet spreadsheet made two reads, and updateColumn for a "
        "hundred cells made one PUT. The consequence is Project 11, Step 2: one new row costs six requests, three for the size change "
        "and three for the three cells, where Google's values guide describes an append call that the library does not use. Google counts "
        "every request, a batch as one, and recommends batching and a payload of at most 2 MB, so updateRows or updateColumn is the way to "
        "write many cells, and writing them one at a time is the way to meet the quota of the next slides.",
        "Count requests, not lines of code: write lists, not cells.")

# ---- 16 the quota: the workflow -------------------------------------------------------------------------------------------------------
dg, dcap = diagram("AQuotaRetry", "activity", (0.5, 1.45, 5.0, 3.1),
                   grid={"throttle": (0, 0), "send": (0, 1), "refused": (0, 2), "done": (1, 2), "left": (0, 3), "raise": (1, 3), "pause": (0, 4)},
                   cols=[(0.0, 2.55), (3.0, 1.95)], rows_n=5, starts=(1, 0), ends={"type": "dot", "col": 1, "row": 4},
                   routes={("start", "throttle"): "h", ("pause", "send"): "loopL", ("done", "end"): "loopR"}, fs=8, nh=0.44, dh=0.46)
t1 = transcript("quotaRetry_v1_0_0.py", 5.6, 1.5, 3.95, fs=7.0)
content("A request that meets the quota", "It throttles itself, retries on RESOURCE_EXHAUSTED and gives up after nine tries",
        [dg, dcap, t1,
         card("Not 'a minute or two'", "The retry pauses 10, 15, ... 45 seconds: 220 in all. IGNORE_QUOTA switches off only the library's own "
              "throttle, so the retry is the same with the flag set. Another error is raised at once.", 5.6, round(1.5 + t1["h"] + 0.15, 2), 3.9, round(4.4 - (1.5 + t1["h"] + 0.15), 2), fs=9.5, accent="slate"),
         foot(L_STANDIN, 5.6, 4.45, 3.9, fs=8.5)],
        "The chapter ends on quotas. It says the library catches the quota exception and retries, so calls may take several seconds, and "
        "that the flag ezsheets.IGNORE_QUOTA exists. The workflow is what the library's code does with one request: it sleeps while too "
        "many writes are in a burst, sends the request, and if Google answers RESOURCE_EXHAUSTED asks whether its tries are used up; if "
        "they are not it pauses and sends again, and if they are it raises the exception to the program. The program on the right makes the "
        "stand-in answer 429 RESOURCE_EXHAUSTED twenty times, with the clock faked so that nothing really waits, and prints, for each of "
        "the flag set to False and True, the kind of exception, the number of requests made and the pauses: HttpError, nine requests and "
        "pauses of 10, 15, 20, 25, 30, 35, 40 and 45 seconds, the same with the flag on. That is 220 seconds in all and not the minute "
        "or two of the chapter. The third line shows another error, a 403 PERMISSION_DENIED, raised at once after one request with no "
        "pause. The flag IGNORE_QUOTA switches off only the library's own throttle of 90 writes or reads in 101 seconds, and the comment in "
        "the library that speaks of 50 requests per 100 seconds is out of date. Google's own answer to an exceeded quota was not observed.",
        "The retry takes 220 seconds in all; IGNORE_QUOTA does not stop it.")

# ---- 17 the quota numbers: a native chart ---------------------------------------------------------------------------------------------
ch = EX["_charts"]["pauses"]
assert "[10, 15, 20, 25, 30, 35, 40, 45]" in PROGS["quotaRetry_v1_0_0.py"]["transcript"]
assert [float(x) for x in eval(G["backoff"][1][1])] == ch["values"]
chart = {"t": "chart", "ctype": "bar", "x": 0.5, "y": 1.45, "w": 4.4, "h": 2.15, "labels": ch["labels"],
         "title": "Pause after failed try 1 to 8, seconds (stand-in run)", "series": [{"name": "Pause", "data": ch["values"]}], "dataLabels": True, "dlFs": 8}
c, bot = con("backoff", 5.1, 1.85, 4.4, fs=9, label="the retry's pauses and their sum; standard library only")
content("Quota numbers: the library's and Google's", "The retry waits 220 seconds in all; the chapter's figures differ from Google's pages",
        [chart, c,
         card("NOT EXECUTED: Google's numbers", "Google's limits page (2026-09-03): 300 reads and 300 writes a minute per project, "
              "60 each per user; 429 on excess. The chapter's 250 a day is not on it.", 0.5, 3.75, 4.4, 1.2, fs=9.5, accent="orange"),
         card("Cell limit: 10 million or 20?", "The chapter says 10 million cells; Google's Drive Help says 20 million or 100 MB. "
              "The produce sheet is 142,548 cells. Filling a sheet to the limit was NOT EXECUTED.", 5.1, 3.75, 4.4, 1.2, fs=9.5, accent="orange")],
        "The chapter says a user may create 250 new spreadsheets a day, that free accounts can make a few hundred requests a minute, and "
        "that a spreadsheet can have up to 10 million cells. Google's pages, read on 12 October 2026, say something different. The Sheets "
        "usage-limits page, updated on 3 September 2026, gives 300 read and 300 write requests a minute per project and 60 of each per user "
        "per project, has no daily limit beside the per-minute quotas and no figure for new spreadsheets, answers excess with 429, advises "
        "truncated exponential backoff, recommends a payload of at most 2 MB, and says that exceeding the quotas is planned to incur charges "
        "later in 2026. The Drive limits changed on 1 May 2026 to a system of quota units. Google's Drive Help gives the limit of a Google "
        "Sheets spreadsheet as up to 20 million cells or 100 MB, where the chapter says 10 million. These figures were read from the pages and "
        "none of them was executed: Google's answer to an exceeded quota was never observed, and filling a sheet to the limit was not tried. "
        "What was executed is the library's side, drawn as the chart: the library pauses 10 seconds after the first failed try and 5 seconds "
        "longer after each one up to 45, which the console sums to 220 seconds over nine tries. The chart's values are the pauses the "
        "stand-in run printed on the previous slide, and the deck check computes the same list again.",
        "Read Google's quota page, not the chapter's numbers.", notexec=True)

# ---- 18 story: Nakamoto and Boringcoin ----------------------------------------------------------------------------------------------------
content("Boringcoin: a spreadsheet as a blockchain", STORY["NakamotoPaper2008"]["when"],
        [card("The message Boringcoin makes fun of", "On 31 October 2008 at 14:10 Eastern time Satoshi Nakamoto wrote to a cryptography mailing "
              "list about an electronic cash system that was fully peer-to-peer, with no trusted third party.", 0.5, 1.5, 4.5, 2.8, fs=12),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "The paper: bitcoin.pdf, announced on the list",
             "Double-spending prevented by a peer-to-peer network",
             "No mint: new coins from proof-of-work",
             "Boringcoin: one sheet, 1,001 rows, a PRE-MINE sender"]},
         factrow("NakamotoPaper2008")],
        story_notes("NakamotoPaper2008") + " The public Boringcoin sheet that Project 11 reads is the author's; its CSV export of 12 October 2026 "
        "had 1,001 rows and was byte-identical to the export committed on 1 October 2026 in the course repository, which is the recorded "
        "fixture of the next slides.",
        "A ledger of rows is easy to audit and just as easy to forge.")

# ---- 19 Step 1: the workflow ---------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("ProjectElevenAudit", "activity", (0.5, 1.4, 9.0, 3.2),
                   grid={"open": (0, 0), "row": (0, 1), "pre": (0, 2), "mint": (1, 2), "move": (0, 3), "more": (1, 3), "print": (2, 3), "total": (2, 4)},
                   cols=[(0.0, 2.9), (3.3, 2.6), (6.3, 2.6)], rows_n=5, starts=(1, 0), ends={"type": "dot", "col": 1, "row": 4},
                   routes={("start", "open"): "h", ("more", "row"): "loopR", ("total", "end"): "h"}, fs=8, nh=0.46, dh=0.56)
content("Project 11, Step 1: audit the ledger", "One pass over every row; the sender PRE-MINE invents money, everyone else moves it",
        [dg, dcap,
         card("Blank row stops it", "getRows returns every row of the grid, so a trailing empty row makes int('') raise ValueError. "
              "The chapter's audit assumes the grid is exactly as long as the data.", 6.9, 1.45, 2.6, 1.9, fs=9.5, accent="slate")],
        "Project 11 uses a public Google Sheet as a fake blockchain of a made-up currency, Boringcoin. Step 1 audits the ledger: the program "
        "opens the sheet and gets all its rows, then loops, reading the sender, the recipient and the amount of each row. When the sender is "
        "PRE-MINE the amount is added to the recipient from nothing, and otherwise it is taken from the sender and added to the recipient. "
        "When no rows are left the program prints the dictionary of balances and adds up their total, which must equal the pre-mined "
        "billion. The diagram is the workflow with its two choices, the sender and the loop. One weakness is not in the chapter. The loop "
        "runs over every row that getRows returns, and getRows returns every row of the grid, so on a sheet with a trailing blank row "
        "int('') raises ValueError at the first empty row; the research ran that case on a copy of the export with a blank row appended. "
        "Run on the real sheet's export, the audit printed the chapter's twenty balances and the total 1,000,000,000, and the shipped "
        "auditBoringcoin.py ran unchanged and printed the same.",
        "Loop over every row, mint for PRE-MINE, move for the rest, and add up.")

# ---- 20 Step 1: the program and the balances -----------------------------------------------------------------------------------------------------
pn = "project11AuditThree_v1_0_0.py"
a20, b20 = span(pn, "for row in ss.sheets[0].getRows():", "print('Total Boringcoins:', total)")
p1, bot = prog(pn, 0.5, 1.55, 4.4, fs=7.0, lines=(a20, b20), show_out=False)
t1 = transcript(pn, 5.1, 1.5, 4.4, fs=7.0, label="what the whole run printed")
trows = EX["_tables"]["ledgerBalances"]["rows"]
tbl = {"t": "table", "x": 5.1, "y": round(1.5 + t1["h"] + 0.2, 2), "w": 4.4, "colW": [2.4, 2.0], "fs": 8, "rowH": 0.22, "rows": trows}
content("Step 1 run on the real ledger's export", "The audit's balances, computed from the CSV export of the public Boringcoin sheet",
        [p1, t1, tbl, foot("Stand-in for Google, recorded fixture: the CSV export of the public sheet; one line of 400+ characters is cut to three.", 0.5, round(bot + 0.03, 2), 4.4, fs=8.5)],
        "The program on the left is the chapter's Step 1 loop and total, run on the CSV export of the real Boringcoin sheet, 1,001 rows, "
        "committed on 1 October 2026 and read through the stand-in for Google; Google itself was not reached. The chapter's program prints "
        "the whole dictionary of 20 balances on one line of more than 400 characters, which cannot be shown unwrapped on a slide, so this "
        "copy of the program prints the number of accounts and the first three instead; the corpus original was run too and printed the "
        "chapter's twenty balances, beginning Al Sweigart with 999,058,553, and the same total. The table is computed from the same CSV by the "
        "same loop: the first six accounts, the sum of the other fourteen, and the total of 1,000,000,000, so that the balances add up to "
        "the pre-mined billion, which is what an audit is for. The transcript's last line gives the size of the ledger: 1,001 rows, 20 "
        "accounts and one pre-mine row. The same data can be audited in a loop of a few lines and forged in one, which is the lesson of the "
        "previous slide's story.",
        "The balances add up to the pre-mined billion: that is the audit.")

# ---- 21 Step 2: append a transaction ---------------------------------------------------------------------------------------------------------
dg, dcap = diagram("ProjectElevenTransaction", "activity", (0.5, 1.4, 4.0, 2.95),
                   grid={"args": (0, 1), "usage": (1, 1), "unpack": (0, 2), "open": (0, 3), "count": (0, 4), "write": (0, 5)},
                   cols=[(0.0, 2.1), (2.4, 1.6)], rows_n=6, starts=(0, 0), ends={"type": "dot", "col": 1, "row": 5},
                   routes={("write", "end"): "h", ("usage", "end"): "v"}, fs=8, nh=0.42, dh=0.5)
pn = "project11TransactionCost_v1_0_0.py"
a21, b21 = span(pn, "sender, recipient, amount = sys.argv[1:]", "print(len(g.log), 'requests:'")
p1, bot = prog(pn, 4.7, 1.55, 4.8, fs=7.0, lines=(a21, b21), show_out=True)
content("Project 11, Step 2: add a transaction", "Three arguments, one new row; the size change costs three requests and each cell one",
        [dg, dcap, p1,
         {"t": "text", "x": 4.7, "y": round(bot + 0.12, 2), "w": 4.8, "h": 0.42, "fs": 10.5, "bold": True, "color": "ink",
          "body": "Six requests for one row: rowCount += 1 is two reads and a batchUpdate, then three PUTs, one per cell."},
         foot(L_FIXTURE, 0.5, 4.72, 9.0, fs=9)],
        "Step 2 adds one transaction to the ledger from the command line. The program gets the sender, the recipient and the amount from "
        "sys.argv, ends with a line of usage when there are fewer than three arguments, opens the sheet, adds one to rowCount and writes "
        "the three values into the new row. The chapter's arguments are set in the program's second line instead of on a command line. Run "
        "on the export of the real sheet, the row count went from 1,001 to 1,002 and the new row held Al Sweigart, Eve and 2000. This copy "
        "of the program clears the request log before the size change and prints how many requests the change and the three writes made: "
        "six, two reads and a POST for rowCount and three PUTs for the cells, so the cost of one transaction is six requests; the corpus "
        "original prints the same requests as a list of method and range, a line too long for a slide. The amount is written as the string "
        "'2000', and whether Google turns it into a number depends on USER_ENTERED, which was not executed. An unquoted name makes sys.argv[1:] "
        "four items and raises ValueError with the text too many values to unpack, expected 3, got 4. The new row number is computed from "
        "a local rowCount, which is what makes the next slide possible.",
        "Appending a row is six requests, and the row number is computed locally.")

# ---- 22 two writers --------------------------------------------------------------------------------------------------------------------------------
pn = "appendRace_v1_0_0.py"
a22, b22 = span(pn, "a = ezsheets.Spreadsheet(g.load('BOR'")
p1, bot = prog(pn, 0.5, 1.55, pw(pn, (a22, b22), True), fs=7.0, lines=(a22, b22), show_out=True)
content("Two writers, one row", "Each computes the new row number from its own copy, so the second write replaces the first",
        [p1,
         card("A lost update, with no error", "Both programs read rowCount 1001 and both write row 1002; the later one overwrites the "
              "first. Google's values guide describes an append call; the library does not use it.", 5.6, 1.5, 3.9, 1.95, fs=10.5, accent="orange"),
         {"t": "boxes", "x": 0.5, "y": 3.65, "w": 9.0, "h": 0.95, "cols": 4, "fs": 11, "subfs": 9, "arrows": True, "accent": [3], "items": [
             {"label": "Both read 1,001", "sub": "each from its own copy"},
             {"label": "Both set row 1,002", "sub": "rowCount += 1"},
             {"label": "'first' is written", "sub": "to row 1,002"},
             {"label": "'second' overwrites it", "sub": "no error is raised"}]},
         foot(L_FIXTURE, 0.5, 4.72, 9.0, fs=9)],
        "The transaction program of the last slide computes the new row number from rowCount, which is a number the Sheet object keeps "
        "locally. Two programs that append at the same time therefore both read 1001, both make it 1002 and both write row 1002, and the "
        "second overwrites the first with no error. The program on the left runs that deterministically with two Spreadsheet objects on "
        "the stand-in's copy of the Boringcoin export: the first writes to row 1002, the second writes to row 1002, and after a refresh the "
        "sheet has 1,002 rows and row 1002 holds second. The stand-in is not Google, so what this shows is the library's logic, which is "
        "the whole cause: the row number is computed locally and the write names its cell. The remedy the research names is to guard "
        "the append, for example by an append call of Google's API, which the values guide describes and the library does not use, or "
        "by reading the sheet again before the write. The same lost update can happen with any program that reads a number, adds one "
        "and writes it back, which is the lesson of this slide for any shared sheet.",
        "A computed row number is a race: guard the append.")

# ---- 23 practice programs -------------------------------------------------------------------------------------------------------------------------------
pn = "practiceBeanCountCheck_v1_0_0.py"
a23, b23 = span(pn, "ss = ezsheets.Spreadsheet(g.load('BEAN'")
p1, bot = prog(pn, 0.5, 1.55, pw(pn, (a23, b23), True), fs=7.0, lines=(a23, b23), show_out=True)
pn2 = "practiceFormatConverter_v1_0_0.py"
a24, b24 = span(pn2, "open('data.csv', 'w')")
p2, bot2 = prog(pn2, 0.5, round(bot + 0.3, 2), pw(pn2, (a24, b24), True), fs=7.0, lines=(a24, b24), show_out=True)
t3 = transcript("practiceFormsEmails_v1_0_0.py", 0.5, round(bot2 + 0.3, 2), 4.0, fs=7.0)
content("Practice programs: bean counts, converter, forms", "Check the totals of a 15,001-row sheet; upload and download a file; read the email column",
        [p1, p2, t3,
         card("One wrong total", "Row 14,399 says 804 x 623 = 500,891; it is 500,892. 15,001 rows were read with no further request.",
              6.65, 1.5, 2.85, 1.3, fs=9.5, accent="slate"),
         foot("Stand-in for Google, recorded fixture: the bean rows are the CSV export of the public sheet. The converter and forms programs use synthetic data; the forms layout is an assumption.", 4.7, round(bot2 + 0.3, 2), 4.8, fs=8.5)],
        "The chapter closes with three practice programs. The bean count check reads a public sheet of bean counts, 15,001 rows read from its "
        "CSV export through the stand-in, and compares the third column with the product of the first two; it found one wrong total, at "
        "row 14,399, where 804 times 623 is 500,892 and the sheet says 500,891. The loop made no request, because the rows were already "
        "loaded. The format converter uploads a file and downloads it in another format: against the stand-in the library sent a "
        "multipart/related request carrying the file's base name with its extension and then asked Drive for the xlsx MIME type, and only "
        "xlsx, ods, csv and tsv are accepted for upload; the title that Google gives the new spreadsheet, and whether the converted file keeps "
        "formulas and formats, were not executed. The forms program reads the email column of a response sheet; it was run on synthetic "
        "rows, laid out with a Timestamp column first as the form tool is usually seen to do, which Google's help page does not state, so "
        "it shows the library and not Google Forms. Google Forms was first introduced in 2008 as part of the Google Docs suite and lets the "
        "owner choose a new or an existing spreadsheet as the destination of the responses; that account rests on Wikipedia and Google's "
        "help page.",
        "Practice programs show the library at work, on real rows or on honest stand-ins.")

# ---- 24 summary: the mind map ------------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("GoogleSheetsAtAGlance", "mindmap", (0.5, 1.4, 9.0, 3.35), fs=9, root_w=1.6)
content("The chapter in one map", "Six branches; the slides of each branch hold the examples",
        [dg, dcap],
        "These six branches are the route of the deck. Access to a Google account comes first: a Cloud project, the two APIs and a consent "
        "screen, a credentials file and two token files, and a first sign-in that opens a browser. Spreadsheet objects follow: a spreadsheet "
        "is opened by URL, id or title, uploaded and downloaded in six formats, and deleting sends it to the Trash. Sheet objects are the "
        "largest branch: a cell is got by address or by column and row, rows and columns are read and written as lists, and sheets are "
        "created, moved, deleted and copied. Requests and quotas follow: every write is one request, Google limits the requests per minute, "
        "and the library throttles and retries. The Boringcoin project puts the pieces together, an audit that adds up balances, a program "
        "that adds a row, and practice programs that read forms and check totals. The last branch is the library and Google's clients: "
        "EZSheets is built on the Google client libraries, its documentation is dated November 2019, and the same program runs under every "
        "3.14 release. Together they answer the first question of the chapter, which object stands for which part of the account and which "
        "request each call sends, and the slides that say where a printed line differs answer the second.",
        "If a branch feels unproven, its slides hold the example.")

# ---- 25 resources ----------------------------------------------------------------------------------------------------------------------------------------------
PUB = {p[0]: p for p in RD.PUBS}
_read = [["The textbook, chapter 15 - free online", PUB["P01"][2]],
         ["EZSheets documentation (dated 2019)", PUB["P02"][2]],
         ["EZSheets releases on PyPI", "https://pypi.org/project/ezsheets/"],
         ["pickle is not secure (Python 3.14)", PUB["P39"][2]]]
_ref = [["Sheets API usage limits", PUB["P07"][2]],
        ["Reading and writing values", PUB["P09"][2]],
        ["ValueInputOption", PUB["P12"][2]]]
_hist = [["RFC 7636, PKCE (the sign-in)", PUB["P50"][2]],
         ["Google Sheets, from XL2Web (Wikipedia)", STORY["GoogleSheetsXL2Web2006"]["link"]],
         ["Nakamoto's message to the list, 2008", STORY["NakamotoPaper2008"]["link"]],
         ["Introduction to OAuth", STORY["OAuthBegins2006"]["link"]],
         ["Sheets API v3 turn-down, 2021", STORY["SheetsApiV3Turndown2021"]["link"]],
         ["Google Forms (Wikipedia)", STORY["GoogleForms2008"]["link"]]]
LINKS = [r[1] for r in _read + _ref + _hist]
json.dump({"_version": __version__, "links": LINKS}, open(os.path.join(HERE, "links_v1_0_0.json"), "w"), indent=1)
content("Where to go from here", "Every link was opened on the day this deck was made",
        [{"t": "links", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.55, "fs": 9.5, "groups": [
            {"head": "Read", "rows": _read}, {"head": "Reference", "rows": _ref}, {"head": "History and standards", "rows": _hist}]}],
        "Every link on this slide was opened on the day the deck was made, and the build records the status each answered. The textbook "
        "chapter is free to read online and holds every listing of the chapter, the EZSheets documentation is the page the chapter points to "
        "and is dated November 2019, and the PyPI page lists the releases. The reference links are Google's own pages for the limits, the "
        "values calls and the value input options that the deck cited as read and not executed, Python's warning about pickle, and the RFC "
        "whose example the PKCE console used. The history links are the sources behind the six stories of the chapter. Two of them are "
        "slides, the beginning of Google Sheets as XL2Web and Nakamoto's message; the other four were told in the notes: OAuth on the "
        "set-up slide, the turn-down of the Sheets API version 3 on the slide of spreadsheet objects, Google Forms on the slide of "
        "the practice programs, and the release of EZSheets on the first slide of the library.",
        "Textbook, Google's pages and history, opened the day this deck was built.")

# ---- 26 closing -------------------------------------------------------------------------------------------------------------------------------------------------
content("What you should now be able to say", "Four claims, each carried by a result you saw printed",
        [{"t": "bullets", "x": 0.6, "y": 1.5, "w": 8.8, "h": 2.4, "fs": 15, "items": [
            "Every call is a request to Google: I count requests and write lists, not cells.",
            "A token file is code, and in Testing status the sign-in is weekly.",
            "Sheet() returns None, an id is cut by position, and two writers can lose a row.",
            "I say which results came from Google and which from a stand-in: here, none came from Google."]},
         {"t": "chips", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.6, "fs": 13, "big": True,
          "items": ["%d rows run" % sum(len(v) for v in G.values()), "%d programs run" % len(PROGS), "8 diagrams"]}],
        "Four claims, each carried by a result you saw printed or by a statement marked as not executed. If you can say them in your own "
        "words and run the examples yourself, you have the chapter; the console rows that use only the standard library can be typed into "
        "any Python, including one in a browser, and the programs need ezsheets and Google's client library installed. Nothing on these "
        "slides was answered by Google, and a deck about a web service should say so. The next chapter of the book works with SQLite "
        "databases, where a program reaches data through a file instead of a web service, and what this chapter taught about requests, "
        "rows and the cost of writing one cell at a time carries over to it.",
        "Questions are welcome; bring a spreadsheet to read.")

# ---- agenda ---------------------------------------------------------------------------------------------------------------
_t = {s["title"]: i + 1 for i, s in enumerate(S)}
_parts = [("Google and the library", "EZSheets and what a program can do with it", "Google Sheets began as XL2Web, in 2006"),
          ("Access: credentials and tokens", "Credentials, tokens and the first sign-in", "The token files are pickles, and a pickle runs code"),
          ("Spreadsheets", "Spreadsheet objects: title, sheets, and Sheet()", "Opening by URL, and the name of a download"),
          ("Sheets, rows, columns and cells", "Rows and columns as lists", "A cell written, and a cell read back"),
          ("Requests and quotas", "What a call sends, and what it costs", "Quota numbers: the library's and Google's"),
          ("Project 11: Boringcoin", "Boringcoin: a spreadsheet as a blockchain", "Project 11, Step 2: add a transaction"),
          ("Two writers and practice programs", "Two writers, one row", "Practice programs: bean counts, converter, forms"),
          ("Summary and resources", "The chapter in one map", "Where to go from here")]
_rows = ["%s (slides %d-%d)" % (name, _t[a], _t[b]) for name, a, b in _parts]
_ends = [_t[b] for _, _, b in _parts]
_starts = [_t[a] for _, a, _ in _parts]
if _starts[0] != 4 or any(_starts[i + 1] != _ends[i] + 1 for i in range(len(_parts) - 1)) or _ends[-1] != len(S) - 1:
    raise SystemExit("REFUSED: agenda ranges are not contiguous: %r %r (len S=%d)" % (_starts, _ends, len(S)))
_nconsole = sum(1 for s in S for i in s["items"] if i.get("t") in ("code", "prog"))
_nstory = sum(1 for s in S for i in s["items"] if i.get("t") == "factrow")
S[1]["items"] = [
    {"t": "numlist", "x": 0.5, "y": 1.4, "w": 6.3, "h": 3.55, "fs": 11, "items": _rows},
    {"t": "stat", "x": 7.05, "y": 1.5, "w": 2.45, "h": 3.4, "vert": True, "items": [
        {"n": str(len(S)), "label": "slides, numbered bottom-right"},
        {"n": "%d + %d" % (_nstory, 6 - _nstory), "label": "true stories: %d on slides, %d in the notes" % (_nstory, 6 - _nstory)},
        {"n": str(_nconsole), "label": "consoles and programs, all run before they were shown"}]}]
S[1]["sub"] = "Eight parts; every range is a run of slides you can jump to"
S[1]["take"] = "Eight parts, from a Google account to a ledger."
S[1]["notes"] = ("The route has eight parts. It starts with Google and the library, the use cases of EZSheets and the beginning of Google "
                 "Sheets, then the access to an account, the credentials and token files, the token's life and the danger of a token file that "
                 "is a pickle, then spreadsheet objects, the addresses and ids and the names of downloads, then sheets, rows, columns and "
                 "cells and the way a write and a read differ, then requests and quotas, then Project 11, the fake blockchain that is audited "
                 "and extended, then the lost update of two writers and the three practice programs, ending with a one-map summary and the "
                 "resources. The ranges name the exact slides, so you can return to the part you need. Two of the slides are true stories "
                 "and four more are told in the notes; the eight narrative diagrams of the chapter are drawn from the same specifications as "
                 "the interactive page. Wherever an output comes from a stand-in for Google or a recorded fixture, the slide says so, and "
                 "what needs a Google account is marked as not executed.")

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
plan = {"meta": {"title": "Chapter 15: Google Sheets", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": len(S), "diagrams": SHOWN, "notExecuted": NOTEXEC}, "slides": S}
out = os.path.join(HERE, "deck_plan_v1_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides; diagrams on slides", dict(sorted(SHOWN.items(), key=lambda kv: kv[1])), "; NOT EXECUTED on slides", NOTEXEC)

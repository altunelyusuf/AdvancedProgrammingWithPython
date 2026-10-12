#!/usr/bin/env python3
"""Builds deck_plan_v1_0_0.json - SEN0414 chapter 13 (Web Scraping) on the CME classroom standard.

Same regime as chapters 10 to 12: numbered warm-ivory slides, an agenda with exact slide ranges, a summary before the
resources, full-sentence takeaway strips, stories with fact rows, consoles and whole programs with their results as Python
printed them. Every console result and program transcript comes from examples_out_v1_0_0.json (made by
examples_run_v1_0_0.py under Python 3.14.6); the speaker notes are prose for the reader and carry only what the chapter's
RDODI research package (03-materials/ch13/rdodi, sen0414_ch13_rdodi_data_v1_0_2.py, findings F1 to F12), its records
(08-tooling/ch13-page/*.json) or a program of this deck established.

What is new against chapter 12: the eight narrative diagrams of the chapter (sen0414_ch13_diagrams_v1_0_0.py, grounding 0.84
or more) are drawn as native shapes by diagram_shapes_v1_0_0.py and checked by diagram_check_v1_0_0.py; one story slide carries
the Kenneth Reitz photograph with its CC BY 3.0 attribution; two transcripts are of programs that reach the live web.

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


ST = load("stories4131", os.path.join(HERE, "..", "sen0414_ch13_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
DG = load("diagrams4131", os.path.join(HERE, "..", "sen0414_ch13_diagrams_v1_0_0.py"))
NODES = DG.nodes_from_ttl(os.path.join(HERE, "..", ".."))
_bad = DG.run_checks(NODES)
if _bad:
    raise SystemExit("REFUSED: the diagrams fail their own checks: %r" % _bad[:3])
DIAG = {d["id"]: d for d in DG.DIAGRAMS}
RD = load("rdodi4131", os.path.join(HERE, "..", "sen0414_ch13_rdodi_data_v1_0_2.py"))
EX = json.load(open(os.path.join(HERE, "examples_out_v1_0_0.json")))
IMG = json.load(open(os.path.join(HERE, "..", "ch13-page", "stories_img_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s" % PYV
G = {k: [[s, (o or "")] for s, o in v] for k, v in EX.items() if not k.startswith("_")}
PROGS = EX["_programs"]
CQ1, CQ2 = RD.CQS
PHOTO = "../../03-materials/ch13/assets/" + IMG["ReitzRequests2011"][0]["file"]
if not os.path.exists(os.path.join(HERE, PHOTO)):
    raise SystemExit("REFUSED: the Reitz photograph is missing")


def lines_of(rows):
    return sum(1 + (1 if out.strip() else 0) for _, out in rows)


def con(group, x, y, w, fs=11, label=None, cap=True, rows=None):
    """A console panel sized from its rows; returns (item, bottom y)."""
    rr = rows if rows is not None else G[group]
    maxlen = max(max(len(st) + 4, len(out)) for st, out in rr)
    fs = min(fs, round((w - 0.4) / (maxlen * 0.0088), 1))
    if fs < 7:
        raise SystemExit("REFUSED: console %s cannot fit unwrapped in %.1f in (fs %.1f)" % (group, w, fs))
    L = lines_of(rr)
    h = round(L * fs * 1.23 / 72.0 + 0.36 + 0.02 * max(0, L - 1), 2)
    it = {"t": "code", "x": x, "y": y, "w": w, "h": h, "rows": rr, "fs": fs}
    if cap:
        it["cap"] = CAP
    if label:
        if len(label) > (w - 0.1) / 0.083:
            raise SystemExit("REFUSED: label %r is too long for a %.1f in panel" % (label, w))
        it["label"] = label
    return it, round(y + h + (0.26 if cap else 0), 2)


def span(pname, first, last=None):
    """1-based line numbers (a, b) of the program lines from the first containing `first` to the first containing `last`."""
    ls = PROGS[pname]["code"].rstrip("\n").split("\n")
    a = next(i for i, l in enumerate(ls, 1) if first in l)
    b = len(ls) if last is None else next(i for i, l in enumerate(ls, 1) if i > a and last in l)
    return a, b


def prog(pname, x, y, w, fs=8, lines=None, show_out=True, live=False):
    """A chapter program (or an honest excerpt) with its transcript, sized from its text; returns (item, bottom y).
    The excerpt is a verbatim slice and the label above the panel names it ('program <name>, lines a to b of n'), as
    program_check_v1_0_0.py verifies. The transcript, when shown, sits in the same panel."""
    pr = PROGS[pname]
    all_lines = pr["code"].rstrip("\n").split("\n")
    a, b = (1, len(all_lines)) if lines is None else lines
    shown = all_lines[a - 1:b]
    out = pr["transcript"] if show_out else ""
    outlines = (out.count("\n") + 1) if out else 0
    maxlen = max(max(len(l) for l in shown), max((len(t) for t in out.split("\n")), default=0) + 8)
    fs = min(fs, round((w - 0.4) / (maxlen * 0.0088), 1))
    if fs < 7:
        raise SystemExit("REFUSED: program %s lines %d-%d cannot fit unwrapped in %.1f in (fs %.1f)" % (pname, a, b, w, fs))
    L = len(shown) + outlines
    h = round(L * fs * 1.23 / 72.0 + 0.38 + 0.02 * max(0, L - 1), 2)
    label = "program %s, lines %d to %d of %d - Python %s" % (pname, a, b, len(all_lines), PYV)
    if len(label) > (w - 0.1) / 0.083:
        label = "program %s, lines %d to %d of %d" % (pname, a, b, len(all_lines))
    if len(label) > (w - 0.1) / 0.083:
        raise SystemExit("REFUSED: caption %r is too long for a %.1f in panel" % (label, w))
    it = {"t": "prog", "x": x, "y": y, "w": w, "h": h, "lines": shown, "fs": fs, "compact": bool(out),
          "out": out if out else None, "outLabel": "prints", "label": label}
    return it, round(y + h, 2)


def transcript(pname, x, y, w, h=None, fs=9, label="what the run printed"):
    """The transcript of a program in a panel of its own (a panel labelled 'transcript of program <name>' is re-run by
    program_check and must equal the recording); h is worked out from the text unless given."""
    out = PROGS[pname]["transcript"]
    fs = min(fs, round((w - 0.4) / ((max(len(t) for t in out.split("\n")) + 7) * 0.0088), 1))
    if fs < 7:
        raise SystemExit("REFUSED: transcript of %s cannot fit unwrapped in %.1f in (fs %.1f)" % (pname, w, fs))
    if len(label) > (w - 0.1) / 0.083:
        raise SystemExit("REFUSED: label %r is too long for a %.1f in panel" % (label, w))
    if h is None:
        L = out.count("\n") + 1
        h = round(L * fs * 1.23 / 72.0 + 0.36 + 0.02 * max(0, L - 1), 2)
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
    it = {"t": "card", "head": head, "body": body, "x": x, "y": y, "w": w, "h": h, "fs": fs}
    if accent:
        it["accent"] = accent
    return it


def diagram(did, kind, box, **kw):
    """The shapes item of a narrative diagram and its caption (which names the diagram and its measured grounding)."""
    d = DIAG[did]
    fn = {"activity": DS.activity, "sequence": DS.sequence, "states": DS.states, "usecases": DS.usecases, "mindmap": DS.mindmap}[kind]
    it = fn(d["data"], box, **kw)
    h, n = d["grounding"]
    body = "diagram %s - %s pattern, %d of %d words grounded in the chapter's text" % (did, d["pattern"], h, n)
    cap = {"t": "foot", "x": box[0], "y": round(box[1] + box[3] + 0.03, 2), "w": box[2], "h": round(DS.need_h(body, box[2], 8.5) + 0.04, 2), "fs": 8.5,
           "body": body}
    return it, cap


S = []
SHOWN = {}  # diagram id -> slide number


def content(title, sub, items, notes, take, lede=None):
    if lede and len(lede.split()) > 34:
        raise SystemExit("REFUSED: lede on %r runs past the gate" % title)
    if len(take.split()) > 24 or not take.endswith("."):
        raise SystemExit("REFUSED: takeaway %r is not a short full sentence" % take)
    if len(title) > 53:
        raise SystemExit("REFUSED: title %r is longer than 53 characters" % title)
    for it in items:
        if it["t"] in ("code", "prog", "shapes", "card", "boxes", "chips", "stat", "beats", "factrow", "numlist", "bullets", "links", "foot", "text", "img"):
            if it["y"] + it.get("h", 0.4) > 5.0 or it["x"] + it["w"] > 9.55:
                raise SystemExit("REFUSED: item %s on %r reaches y %.2f / x %.2f" % (it["t"], title, it["y"] + it.get("h", 0.4), it["x"] + it["w"]))
        if it["t"] == "shapes":
            SHOWN[it["did"]] = len(S) + 1
    sl = {"kind": "content", "title": title, "sub": sub, "items": items, "notes": notes, "take": take, "bg": "light"}
    if lede:
        sl["lede"] = lede
    S.append(sl)


# ---- 1 title ---------------------------------------------------------------------------------------------------
S.append({"kind": "title", "title": "Chapter 13: Web Scraping",
          "sub": "How a program reaches the web: webbrowser, requests, a web API, Beautiful Soup, Selenium and Playwright",
          "items": [{"t": "code", "x": 5.0, "y": 0.85, "w": 4.5, "h": 0.95, "fs": 10.5, "cap": CAP, "rows": G["title"]}],
          "notes": "Until this chapter every program worked on files and text that were already on the computer. Chapter 13 "
                   "reaches out: a program can open a page in the user's own browser, download a page or a file, ask a web "
                   "service for data in JSON, read the HTML it received, and, when a page is built by a script or needs a "
                   "login, drive a real browser. This deck follows the chapter in that order and adds what the chapter leaves "
                   "out, which is timeouts, the robots.txt file and the change to its parser in Python 3.14.5, the flags a "
                   "driven browser reveals, and what the public sites actually answered on 12 October 2026. Every example was "
                   "run under Python 3.14.6 on Ubuntu with requests 2.34.2, Beautiful Soup 4.15.0, Selenium 4.51.0 and "
                   "Playwright 1.63.0, and the result printed beside it is the result that run gave. The programs that need a "
                   "web site start a small one of their own on this machine, and the two marked live reached the real sites.",
          "bg": "light"})

# ---- 2 agenda (filled in at the end) -------------------------------------------------------------------------------
S.append({"kind": "content", "title": "Today's route", "sub": "", "items": [], "notes": "", "take": "", "bg": "light"})

# ---- 3 questions ------------------------------------------------------------------------------------------------
content("The questions this chapter answers", "The chapter's own competency questions; the summary comes back to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 2.2, "fs": 13, "items": [CQ1, CQ2]},
         {"t": "chips", "x": 0.5, "y": 3.8, "w": 9.0, "h": 0.5, "fs": 11.5,
          "items": ["6 branches", "%d topics" % len(NODES), "%d console rows" % sum(len(v) for v in G.values()),
                    "%d programs run" % len(PROGS), "8 diagrams", "Python %s" % PYV]}],
        "The first question is the chapter's spine. A program that needs something from the web can show the page to the user, "
        "download it as text or a file, ask a service that answers in JSON, read the HTML it already has, or drive a real "
        "browser, and what decides between these is the page in front of the program: whether the user should see it, whether "
        "the service offers an API, whether the data is in the HTML that is downloaded or is built later by a script. The "
        "second question is the watch-out of the deck. Ten things the chapter prints cannot be run as printed, one of its "
        "three projects meets a challenge page on today's web, and a robots.txt rule changed its meaning inside the Python 3.14 "
        "series, so each slide says where a printed line differs and on what evidence. The chips give the size of the chapter "
        "as this deck covers it: six branches, the topics beneath them, the console rows and programs that were run, and the "
        "eight diagrams.",
        "Choose the tool by the page in front of the program.")

# ---- 4 addresses, status codes, the user agent ------------------------------------------------------------------
rows4 = G["url"] + G["status"]
c, bot = con("url", 0.5, 1.5, 6.3, fs=9, label="cut a URL, name a status code, show the user agent", rows=rows4)
content("Addresses, status codes and the user agent", "A URL is cut into parts; every answer has a status code; every request names its client",
        [c,
         {"t": "boxes", "x": 7.0, "y": 1.5, "w": 2.5, "h": 3.2, "cols": 1, "fs": 11.5, "subfs": 9.5, "accent": [],
          "items": [{"label": "HTTPS hides the content, not the site's name", "sub": "an encrypted connection; a network still sees which site you visit"},
                    {"label": "A status code's first digit is its class", "sub": "2 success, 3 redirection, 4 client error, 5 server error"}]}],
        "A URL is written as a scheme, a host, a path, an optional query after a question mark and an optional fragment after a "
        "number sign, and urllib.parse cuts it up: urlsplit returns the parts, parse_qs turns the query string back into a "
        "dictionary of lists and quote percent-encodes the characters an address may not carry, a space becoming %20 and a "
        "comma %2C. The fragment names a place inside the page and is handled by the browser, so it is never sent to the "
        "server, which is why showmap.py can drop it from an OpenStreetMap address. HTTPS is HTTP over an encrypted "
        "connection: what is fetched and what is submitted are hidden from the network, but the name of the site visited can "
        "still be seen. Every HTTP response begins with a three-digit status code whose first digit gives its class, and "
        "http.HTTPStatus names the codes, 404 Not Found and 429 Too Many Requests among them. Every request also names the "
        "program that makes it in a user-agent header: urllib sends Python-urllib and the version, and requests 2.34.2 sends "
        "python-requests and its version, so a server can tell a script from a browser.",
        "A URL has five parts, a status code has a class, a user agent names the client.")

# ---- 5 robots.txt -----------------------------------------------------------------------------------------------
c, bot = con("robots", 0.5, 1.5, 5.6, fs=9, label="robotparser reads a robots.txt and answers can_fetch")
content("robots.txt: a request, not a lock", "A site's courtesy file, read by a polite crawler with the standard library",
        [c,
         {"t": "boxes", "x": 0.5, "y": bot + 0.06, "w": 5.6, "h": round(4.95 - bot - 0.06, 2), "cols": 2, "fs": 10.5, "subfs": 9, "accent": [1],
          "items": [{"label": "3.14.0 to 3.14.4: True", "sub": "can_fetch for pypi.org's search page"},
                    {"label": "3.14.5 and 3.14.6: False", "sub": "the same call, after RFC 9309 support"}]},
         card("A request, not a lock", "RFC 9309 says the rules in a robots.txt are not a form of access authorization. "
              "A polite crawler honours the file, skips what it disallows and waits the Crawl-delay.", 6.35, 1.5, 3.15, 1.75, fs=10.5),
         card("New in Python 3.14.5", "Up to 3.14.4 the rule Disallow: /search* was read as a literal prefix. From 3.14.5, "
              "released 10 May 2026 (gh-138907), the wildcard follows RFC 9309.", 6.35, 3.35, 3.15, 1.6, fs=10.5, accent="slate")],
        "A robots.txt file at the root of a site lists the paths that crawlers are asked not to fetch. It is a request and not "
        "an access control: RFC 9309, which standardised the method in September 2022, says its rules are not a form of access "
        "authorization, so a crawler that honours it is being polite and one that ignores it is not stopped. The standard "
        "library reads the file: can_fetch answers for one agent and one address, crawl_delay returns the number of seconds a "
        "site asks a crawler to wait, and request_rate returns the pair of requests and seconds. The console shows the parser "
        "of Python 3.14.6 refusing the search page, because Disallow: /search* uses the wildcard star that RFC 9309 defines. "
        "That is a change inside the 3.14 series. The same program, run under each of the seven releases from 3.14.0 to 3.14.6 "
        "with uv, answered True for the search page up to 3.14.4 and False from 3.14.5, whose changelog lists gh-138907, "
        "support for RFC 9309 in urllib.robotparser; the rule matters because the chapter's searchpypi.py fetches exactly "
        "that page of pypi.org, whose robots.txt on 12 October 2026 contained Disallow: /search*.",
        "Honour robots.txt; Python 3.14.5 reads its wildcards as RFC 9309 says.")

# ---- 6 story: Koster -----------------------------------------------------------------------------------------------
content("Robots.txt, agreed on 30 June 1994", STORY["KosterRobots1994"]["when"],
        [card("Martijn Koster and others", "Koster wrote down A Standard for Robot Exclusion, a consensus of 30 June "
              "1994 on the robots mailing list. It says plainly that it is not an official standard and not enforced by anybody.",
              0.5, 1.5, 4.5, 2.8, fs=12.5),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "1993-94: robots swamp servers with rapid-fire requests",
             "30 Jun 1994: consensus on the robots mailing list",
             "One file, /robots.txt, which a robot reads first",
             "Sep 2022: RFC 9309; Python reads it fully from 3.14.5"]},
         factrow("KosterRobots1994")],
        story_notes("KosterRobots1994"),
        "Robots.txt is a 1994 courtesy, not a lock: honour it.")

# ---- 7 webbrowser and showmap --------------------------------------------------------------------------------------
a, b = span("showmap_v1_0_0.py", "SHOWMAP = '''", "'''")
p1, bot = prog("showmap_v1_0_0.py", 0.5, 1.5, 9.0, fs=8, lines=(a, b))
content("webbrowser: show the page to the user", "showmap.py opens a map for an address typed after the command or copied to the clipboard",
        [p1,
         {"t": "foot", "x": 0.5, "y": round(bot + 0.06, 2), "w": 9.0, "h": 0.4, "fs": 10,
          "body": "Run here with stand-ins for webbrowser and pyperclip that record the address each would receive, because this "
                  "machine has no browser window and no clipboard. urllib.parse.quote(address) would percent-encode it."}],
        "showmap.py is the chapter's first project. It takes the address from the command line, joining the words in sys.argv "
        "after the script's name, or from the clipboard when none was typed, puts it into an OpenStreetMap search address and "
        "hands that to webbrowser.open, which asks the user's default browser to show the page and returns True if a browser "
        "was launched and False if not. It cannot read the page it opens. This program writes the chapter's script to a file "
        "and runs it twice, once with the arguments of the chapter's example and once with none, but it replaces webbrowser "
        "and pyperclip with stand-ins that record the address, because a window cannot open here and the clipboard raised "
        "PyperclipException; the two printed lines show the address each run would have opened. The address is used as typed, "
        "with spaces, which the browser then encodes; a program that builds an address itself should percent-encode it with "
        "urllib.parse.quote, as the previous slide showed. In Python 3.14 the BROWSER variable can also name an already "
        "registered browser.",
        "webbrowser.open shows a page to the user and cannot read it.")

# ---- 8 requests: download and save ---------------------------------------------------------------------------------
a, b = span("downloadChecked_v1_0_0.py", "res = requests.get(BASE + '/rj.txt')")
p1, bot = prog("downloadChecked_v1_0_0.py", 0.5, 1.5, 9.0, fs=7.5, lines=(a, b))
content("requests: download, check and save", "get() returns a Response; raise_for_status() turns a bad status into an exception",
        [p1],
        "The requests module is installed separately; requests.get downloads the page or file at an address and returns a "
        "Response object. The Response holds the body twice, as bytes in content and as text decoded with the response's "
        "encoding, and the download is only the HTML or the file itself, because images and other media on a page are fetched "
        "by requests of their own. This program, run against a stand-in site on this machine, downloads a text file, calls "
        "raise_for_status() after the get, which does nothing for a good status and raises HTTPError for a 4xx or 5xx, and "
        "saves the body in binary mode with iter_content(8000), so the three write() calls return 8000, 8000 and 3000 and the "
        "file on disk is 19000 bytes. A request for a page that does not exist is answered with 404, and raise_for_status() "
        "turns that into the exception whose message is printed. The chapter prints the same message with an address that ends "
        "in .html although the address it requested does not, and the Romeo and Juliet file it downloads is 174126 characters "
        "today, not the 178978 the chapter prints; both are in the research record of this chapter.",
        "get, raise_for_status, then write the body in binary chunks.")

# ---- 9 a checked download: the diagram ----------------------------------------------------------------------------
dg, dcap = diagram("ACheckedDownload", "activity", (0.5, 1.45, 5.1, 3.1),
                   grid={"get": (0, 0), "ok": (0, 1), "open": (0, 2), "loop": (0, 3), "done": (0, 4), "stop": (1, 1)},
                   cols=[(0.0, 2.7), (3.0, 2.1)], rows_n=5, starts=(1, 0), ends={"type": "dot", "col": 1, "row": 4},
                   routes={("start", "get"): "h"})
dg["did"] = "ACheckedDownload"
content("A checked download, step by step", "The chapter's list of steps for one download, with the one place the program stops",
        [dg, dcap,
         card("Always pass a timeout", "Without one a call can hang indefinitely. In the research run a call with timeout=0.2 "
              "raised ReadTimeout; the same call without it returned the slow server's late answer.", 5.85, 1.5, 3.65, 1.6, fs=10.5),
         card("Stream a download to a file", "With stream=True get() returns before the body has arrived. Without it the whole "
              "body is read first, so iter_content only cuts a body that is already loaded.", 5.85, 3.25, 3.65, 1.65, fs=10.5, accent="slate")],
        "This is the chapter's own list of steps for one download, drawn as an activity: call requests.get, call "
        "raise_for_status, and only if no exception was raised open the file in write binary mode, loop over iter_content and "
        "write each chunk. The decision is the orange hexagon; one answer ends the program, or lets the exception be caught and "
        "printed, and the other goes on to the file. The requests documentation adds two things the chapter leaves out, and "
        "both were tried for this chapter. Nearly all production code should pass a timeout, because a call without one can "
        "hang indefinitely; a call with timeout=0.2 against a slow local server raised ReadTimeout, while the same call without "
        "a timeout returned the server's late answer. And a download to a file should pass stream=True, because without it the "
        "whole body is read before get() returns; with stream=True the first five bytes were read while the server still held "
        "the rest. So iter_content(100000) on a response fetched without stream=True only cuts an already loaded body into "
        "chunks, which is correct for a small file and wrong for a large one.",
        "Check the status, save in chunks, and add a timeout.")

# ---- 10 story: Reitz (with the photograph) -------------------------------------------------------------------------
cred = IMG["ReitzRequests2011"][0]["credit"]
content("Requests, conceived 13 February 2011", STORY["ReitzRequests2011"]["when"],
        [card("Kenneth Reitz", "The release history of Requests begins with version 0.0.1 on 13 February 2011, listing "
              "'Frustration' and 'Conception', and 0.2.0 the next day, listing 'Birth!'.",
              0.5, 1.5, 3.6, 2.8, fs=12),
         {"t": "beats", "x": 4.3, "y": 1.5, "w": 2.75, "h": 2.8, "fs": 11.5, "items": [
             "13 Feb 2011: 0.0.1, 'Frustration, Conception'",
             "14 Feb 2011: 0.2.0, 'Birth!'",
             "PyPI's first upload: 14 Feb 2011",
             "Slogan: HTTP for Humans"]},
         {"t": "img", "path": PHOTO, "x": 7.2, "y": 1.5, "w": 2.3, "h": 1.54},
         {"t": "text", "x": 7.2, "y": 3.1, "w": 2.3, "h": 1.15, "fs": 8.5, "italic": True, "color": "mute",
          "body": "Kenneth Reitz at a talk, 17 November 2012. Photo: Nils Pascal Illenseer, CC BY 3.0 "
                  "(creativecommons.org/licenses/by/3.0), via Wikimedia Commons; resized."},
         factrow("ReitzRequests2011")],
        story_notes("ReitzRequests2011") + " The photograph is Kenneth Reitz at a talk in 2012, by Nils Pascal Illenseer, licensed "
        "CC BY 3.0, from Wikimedia Commons, file Rupy Talk Kenneth Reitz; the 960-pixel rendition of the 2048-pixel original is "
        "shown, and the speaker is identified by the Commons file title and description, since the picture carries no caption.",
        "Requests: conceived in frustration on 13 February 2011, born the next day.")

# ---- 11 weather API --------------------------------------------------------------------------------------------------
a, b = span("weatherStandIn_v1_0_0.py", "res = requests.get(BASE + '/data/2.5/weather'")
p1, bot = prog("weatherStandIn_v1_0_0.py", 0.5, 1.5, 9.0, fs=8, lines=(a, b))
t2 = transcript("weatherLive_v1_0_0.py", 0.5, round(bot + 0.5, 2), 9.0, None, fs=9,
                label="transcript of program weatherLive_v1_0_0.py: the chapter's fake key sent to the real service (LIVE)")
content("A weather API: one call, one JSON answer", "A stand-in service answers with a key; the real one answers 401 to the chapter's fake key",
        [p1, t2,
         {"t": "text", "x": 0.5, "y": round(t2["y"] + t2["h"] + 0.1, 2), "w": 9.0, "h": 0.55, "fs": 11, "color": "ink",
          "body": "An API key identifies the account and stays out of the source. The answer is JSON, which json.loads or "
                  "res.json() decodes; the temperature arrives in Kelvin."}],
        "A web API lets one program ask another for data, and an endpoint is the address at which one request is answered; "
        "services put a version into it, such as /geo/1.0/ and /data/2.5/ in the OpenWeather addresses, so that an old version "
        "can be retired. The request carries its parameters in the query string, and requests builds and percent-encodes "
        "that from the params dictionary, as the first printed line shows. The answer is JSON, which res.json() turns into "
        "lists and dictionaries; the temperature arrives in Kelvin, and subtracting 273.15 gives the 12.3 degrees Celsius "
        "printed, since 285.44 minus 273.15 rounds to 12.3. The first program ran against a stand-in service on this machine "
        "because the real one needs a key. The second transcript is a live run: the chapter's placeholder key, sent to the real "
        "endpoint on 12 October 2026, was answered with status 401, a JSON body saying the key is invalid, and a cod field that "
        "is an integer in this answer, while the same field is a string in the 400 answer of the stand-in. An API key identifies "
        "the account that makes the requests, belongs in a file and not in the source, and the free plan allows 60 calls a "
        "minute. The National Weather Service answers without a key but requires a User-Agent header that names the application.",
        "A key identifies the account; the answer is JSON; convert the units.")

# ---- 12 weather diagram --------------------------------------------------------------------------------------------------
dg, dcap = diagram("AWeatherCall", "sequence", (0.5, 1.45, 9.0, 3.1), fs=9, head_w=1.9)
dg["did"] = "AWeatherCall"
content("Two calls, one answer feeding the next", "It asks the geocoder first, then the weather service",
        [dg, dcap],
        "The chapter's weather example is an exchange in an order that matters, so it is drawn as a sequence. The program "
        "asks the geocoding endpoint for the latitude and longitude of San Francisco, the service answers with a JSON list "
        "whose first item has lat and lon, json.loads turns that text into lists and dictionaries, and only then can the "
        "program ask the weather endpoint, passing the latitude and longitude it just learned. The second answer is a JSON "
        "dictionary whose temperature is in Kelvin, which the program converts to Celsius. Three details come from running "
        "it. A call that finds nothing is still answered, with an empty list for an unknown city and a dictionary holding a "
        "cod and a message for a wrong latitude, so a program checks the shape of the decoded data before indexing it. The "
        "forecast's dt field is a Unix timestamp, and datetime.fromtimestamp answers in the time zone of the machine unless "
        "one is given. And there is often a better choice than a key: the National Weather Service API returned fourteen "
        "forecast periods for the chapter's latitude and longitude on 12 October 2026 with no key at all.",
        "Decode each answer and check its shape before it feeds the next request.")

# ---- 13 Beautiful Soup console --------------------------------------------------------------------------------------------
c, bot = con("soup", 0.5, 1.5, 9.0, fs=9.5, label="select returns a list of Tags; a regular expression misses links a parser finds")
content("Beautiful Soup: select, then read", "Parse the text that requests downloaded, then ask for elements by CSS selector",
        [c],
        "Beautiful Soup takes the HTML as a string or an open file and the name of a parser, html.parser being the one in "
        "Python's standard library, and returns an object holding the parsed page. Its select method takes a CSS selector, "
        "which names elements by tag, by # and id, by . and class, by a space for a descendant, by > for a direct child "
        "and by [attribute] in square brackets, and returns a list of Tag objects: an empty list when nothing matches, "
        "and never None. get_text returns the text between a tag's opening and closing tags with the nested tags removed, "
        "while str of the tag returns its HTML; get returns one attribute, and attrs is the dictionary of all of them. The "
        "last three rows show why the chapter advises a parser rather than a regular expression: a pattern that needs href "
        "right after the a misses the link whose tag has a class first, and the parser finds both. On the page the chapter "
        "tells the reader to download, example3.html of 957 bytes, select('p') finds seven paragraphs where the chapter says "
        "three, because three more sit inside the form, and the Developer Tools opened with F12 will copy a selector for any "
        "element.",
        "select returns Tags; parse HTML with a parser, not a regex.")

# ---- 14 story: Richardson ------------------------------------------------------------------------------------------------
content("Beautiful Soup, for awful pages, since 2004", STORY["RichardsonBeautifulSoup2004"]["when"],
        [card("Leonard Richardson", "His page greets the reader: 'You didn't write that awful page. You're just trying to get "
              "some data out of it.' Since 2004 the library has saved programmers hours or days of screen-scraping work.",
              0.5, 1.5, 4.5, 2.8, fs=12),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "2004: the library begins, on crummy.com",
             "Named after a poem in Alice's Adventures",
             "Beautiful Soup 3 was official 2006 to 2012",
             "The chapter installs the fourth: beautifulsoup4"]},
         factrow("RichardsonBeautifulSoup2004")],
        story_notes("RichardsonBeautifulSoup2004"),
        "Richardson's 2004 library exists so you do not parse HTML by regex.")

# ---- 15 searchpypi --------------------------------------------------------------------------------------------------------
a, b = span("searchpypiLocal_v1_0_0.py", "res = requests.get(SEARCH")
p1, bot1 = prog("searchpypiLocal_v1_0_0.py", 0.5, 1.5, 4.7, fs=8.5, lines=(a, b), show_out=False)
t1 = transcript("searchpypiLocal_v1_0_0.py", 5.4, 1.65, 4.1, None, fs=8.5, label="prints against a stand-in results page")
t2 = transcript("searchpypiLive_v1_0_0.py", 5.4, round(1.65 + t1["h"] + 0.4, 2), 4.1, None, fs=8.5,
                label="transcript of program searchpypiLive_v1_0_0.py")
content("searchpypi.py: where today's web differs", "Project 7 opens the first five search results; against pypi.org itself it opens nothing",
        [p1, t1, t2,
         {"t": "text", "x": 5.4, "y": round(t2["y"] + t2["h"] + 0.08, 2), "w": 4.1, "h": 0.55, "fs": 9.5,
          "body": "The second transcript is LIVE: on 12 October 2026 pypi.org answered 200 with a page titled Client Challenge, and its robots.txt disallows /search*."}],
        "searchpypi.py is the chapter's second project: it downloads a search results page, selects the links of the results "
        "with the class selector .package-snippet, and opens the first five in browser tabs, the count being the smaller of "
        "five and the number of links found. The left transcript is the chapter's program, unchanged but for the address and "
        "with a stand-in for webbrowser, run against a stand-in results page that carries eight such links, so five open. "
        "The right transcript is the same program run unchanged against pypi.org on 12 October 2026. The site answered with "
        "status 200 and a page titled Client Challenge, a page that asks for proof of a browser, which holds no "
        "element of that class, so the program found zero links and opened none. Two lessons follow. A program should say "
        "so, rather than open zero tabs in silence, when its selector finds nothing; and the robots.txt of pypi.org disallows "
        "/search*, a rule that Python 3.14.5 and later apply to this very address, so a polite program of today would not "
        "fetch it at all. Both observations are of one day and a site can change.",
        "A challenge page or a robots rule can empty a scraper; check what came back.")

# ---- 16 xkcd -----------------------------------------------------------------------------------------------------------
a, b = span("xkcdLocal_v1_0_0.py", "# Get the Prev button")
p1, bot = prog("xkcdLocal_v1_0_0.py", 0.5, 1.5, 9.0, fs=9, lines=(a, b))
content("downloadXkcdComics.py: follow the Prev link", "Project 8 saves a comic, follows the link whose rel is prev and sleeps between pages",
        [p1],
        "The chapter's third project downloads a web comic by crawling it. In the lines not shown, the loop downloads a "
        "page, parses it with Beautiful Soup, finds the comic's image with the selector #comic img, saves it with "
        "os.path.basename naming the file and iter_content writing it in binary. The lines shown take the address "
        "from the link selected by a[rel=\"prev\"], count the download and sleep, so that the server is not hammered. The loop "
        "ends when the Prev link ends in #, which is the first comic's, or after the limit of downloads. This run is "
        "against a stand-in comic site of three pages on this machine and saved three files. The Step 4 listing as printed in "
        "the chapter is indented with 8, 12, 15, 12 and then 6 spaces and Python rejects it with an IndentationError, so this "
        "run uses the listing with the indentation repaired. On the real xkcd.com on 12 October 2026 the structure the "
        "chapter relies on still held: the comic image sits inside the element with id comic at an address beginning with two "
        "slashes, the page has a rel prev link, and the prev link of the first comic is #.",
        "Select the image, save it in chunks, follow Prev, and sleep between pages.")

# ---- 17 polite crawler + diagram ----------------------------------------------------------------------------------------
a, b = span("politeCrawler_v1_0_0.py", "rp = RobotFileParser(")
p1, bot = prog("politeCrawler_v1_0_0.py", 0.5, 1.5, 5.15, fs=7.5, lines=(a, b))
dg, dcap = diagram("ThePoliteCrawl", "activity", (5.75, 1.45, 3.8, 3.1),
                   grid={"read": (0, 0), "next": (0, 1), "may": (0, 2), "get": (0, 3), "wait": (0, 4), "skip": (1, 2), "more": (1, 4)},
                   cols=[(0.0, 1.5), (1.85, 1.7)], rows_n=6, starts=(1, 0), ends={"type": "dot", "col": 1, "row": 5},
                   routes={("start", "read"): "h", ("skip", "more"): "v", ("more", "next"): "loopR", ("more", "end"): "v",
                           ("wait", "more"): "h"}, fs=8, nh=0.46, dh=0.58)
dg["did"] = "ThePoliteCrawl"
content("A crawler that reads robots.txt first", "The comic downloader sleeps; a polite crawler also asks first",
        [p1, dg, dcap],
        "A crawler is a program that follows links, and the first one, Matthew Gray's World Wide Web Wanderer at MIT in the "
        "spring of 1993, counted 130 Web sites in June 1993 by his own report. A polite crawler does what the diagram "
        "shows: read the robots.txt of the site first, pick a path, ask can_fetch whether the file allows it, skip the path if it "
        "does not, otherwise download the page and wait the Crawl-delay, and repeat while paths and the limit of downloads "
        "remain. The program is a practice program of the chapter's project, written for this deck with the standard "
        "library only, and run against a stand-in site whose robots.txt disallows /private/ and states Crawl-delay: 1. It "
        "read the delay, fetched /a, skipped /private/c without requesting it, fetched /b and waited at least two seconds in "
        "all. The agent name ch13-class-bot is invented for the example; a real crawler names itself and the site it "
        "belongs to, because the user-agent header is how a server tells one program from another.",
        "Read robots.txt, ask can_fetch, skip what is disallowed, wait the Crawl-delay.")

# ---- 18 dynamic page -----------------------------------------------------------------------------------------------------
a, b = span("dynamicPage_v1_0_0.py", "import bs4, requests")
p1, bot = prog("dynamicPage_v1_0_0.py", 0.5, 1.5, 9.0, fs=8, lines=(a, b))
content("When the page is built by a script", "requests and Beautiful Soup see the script; a browser runs it",
        [p1,
         {"t": "boxes", "x": 0.5, "y": round(bot + 0.12, 2), "w": 9.0, "h": round(4.95 - bot - 0.12, 2), "cols": 3, "fs": 11, "subfs": 9, "accent": [2],
          "items": [{"label": "requests", "sub": "downloads the text, script included; it does not run it"},
                    {"label": "Beautiful Soup", "sub": "reads the text it is given: the element is empty"},
                    {"label": "Playwright", "sub": "runs the script in Firefox and reads the written text"}]}],
        "This is the reason the chapter keeps a second family of tools. A page whose content is built by scripts, or that "
        "needs a login, cannot be read from the text that requests downloads. The program starts a small local site "
        "whose only content is an empty element with the id app and a script that writes a sentence into it. requests "
        "downloads the page and the text still holds the script tag; Beautiful Soup, given that text, finds the element and "
        "its text is the empty string, because nothing has run the script; Playwright loads the page in a real Firefox, the "
        "script runs, and the locator returns the written sentence. A browser driver is slower and heavier than a download, so "
        "it is the tool of last resort: the chapter's advice is to prefer a site's API whenever one is offered, and the API of "
        "the National Weather Service still returned fourteen forecast periods in JSON on the day this deck was built while its "
        "forecast page also still carried fourteen elements of the class forecast-text.",
        "If the text lacks the data, a script builds it: use a browser driver.")

# ---- 19 story: Huggins ---------------------------------------------------------------------------------------------------
content("Selenium began in 2004 as a timesheet test tool", STORY["HugginsSelenium2004"]["when"],
        [card("Jason Huggins, ThoughtWorks", "Huggins built JavaScriptTestRunner in Chicago to test an internal Time and Expenses "
              "application. Colleagues liked the immediate visual feedback, and the project was opened up as Selenium.",
              0.5, 1.5, 4.5, 2.8, fs=12),
         {"t": "beats", "x": 5.3, "y": 1.5, "w": 4.2, "h": 2.8, "fs": 12, "items": [
             "2004: Core mode, for a Python and Plone application",
             "Talks about open sourcing it begin",
             "Simon Stewart builds WebDriver separately",
             "The two projects merge; webdriver.Firefox() descends"]},
         factrow("HugginsSelenium2004")],
        story_notes("HugginsSelenium2004"),
        "Selenium began in 2004 as a test tool for one internal timesheet application.")

# ---- 20 Selenium ----------------------------------------------------------------------------------------------------------
a, b = span("seleniumForm_v1_0_0.py", "browser = webdriver.Firefox(options=opts)")
p1, bot = prog("seleniumForm_v1_0_0.py", 0.5, 1.5, 5.4, fs=8, lines=(a, b))
dg, dcap = diagram("WhatASeleniumProgramDoes", "usecases", (6.05, 1.45, 3.5, 3.15), fs=8.5)
dg["did"] = "WhatASeleniumProgramDoes"
content("Selenium: start Firefox and fill the form", "webdriver.Firefox() starts a real browser; find_element() returns the page's elements",
        [p1, dg, dcap],
        "Selenium starts a real browser that the program controls. The program shown is the chapter's login example, run "
        "headless because this machine has no display, against a local login page: it opens the page, finds the two "
        "fields by id with find_element and the By constants, types into them with send_keys, reads back the typed value and the "
        "type attribute of the password field, submits the form from the password field, waits until the title changes with "
        "WebDriverWait and quits. The diagram lists what a Selenium program can do with the elements of a page: find, "
        "read, click, type and submit, and scroll with the Keys constants. Run in Firefox 157 with Selenium 4.51.0, the part "
        "of the chapter on the library is one step behind it. Selenium Manager downloads and finds the driver and the browser "
        "by itself, so the manual geckodriver download the chapter mentions was not needed; the exception the chapter calls "
        "NoSuchElement is NoSuchElementException; and the text of an element hidden with display none is an empty string. "
        "The driven browser also reported navigator.webdriver as True, a flag any page can read. The login values are made "
        "up, and a real password belongs in a file, not in the source.",
        "Selenium drives a real browser: find elements, type, click, submit.")

# ---- 21 Playwright --------------------------------------------------------------------------------------------------------
a, b = span("playwrightCheckbox_v1_0_0.py", "with sync_playwright() as p:")
p1, bot = prog("playwrightCheckbox_v1_0_0.py", 0.5, 1.5, 4.95, fs=8, lines=(a, b))
dg, dcap = diagram("ACheckboxInPlaywright", "states", (5.65, 1.45, 3.85, 3.1), fs=8)
dg["did"] = "ACheckboxInPlaywright"
content("Playwright: a locator, a checkbox, headless", "sync_playwright() runs Firefox without a window; click toggles, check sets",
        [p1, dg, dcap],
        "Playwright is used in its synchronous form inside a with block, which starts and stops it. The block launches Firefox, "
        "headless by default, makes a page, loads a local login page, finds the checkbox with a locator and shows that check() "
        "sets it. A locator stands for the elements that may match and is strict: an action on a locator that matches several "
        "elements raises an error, which is why the chapter picks one with nth(0). The state diagram follows one checkbox. "
        "click() toggles it to the opposite state, whichever it was, while check(), uncheck() and set_checked() leave it checked "
        "or unchecked whatever it was before, which is why the chapter calls them more reliable. Run in Firefox 155 with "
        "Playwright 1.63.0 the part of the chapter on Playwright proved accurate: the six locators of its table each found "
        "their element, a Locator has no submit method, and a headed launch without a display failed with a message about "
        "the missing XServer. The browsers are installed by a second step, playwright install. Playwright was announced for "
        "Python in preview by Arjun Attam on 30 September 2020 on the Microsoft for Python Developers blog, with automatic "
        "waiting as its first claim.",
        "click toggles a checkbox; check, uncheck and set_checked set it.")

# ---- 22 mistyped selector ------------------------------------------------------------------------------------------------
dg, dcap = diagram("AMistypedSelector", "sequence", (0.5, 1.45, 9.0, 2.7), fs=9, head_w=1.9)
dg["did"] = "AMistypedSelector"
content("Playwright waits 30 seconds for a mistyped selector", "A locator waits for an element that may appear; two calls answer at once",
        [dg, dcap,
         {"t": "boxes", "x": 0.5, "y": 4.5, "w": 9.0, "h": 0.5, "cols": 3, "fs": 10.5, "subfs": 8.5, "accent": [0],
          "items": [{"label": "30 s", "sub": "the default wait, then TimeoutError"},
                    {"label": "at once", "sub": "is_visible False, query None"},
                    {"label": "timeout=500", "sub": "the wait ended after 0.6 s"}]}],
        "Playwright's locators wait. A locator stands for elements that may exist later, so click() waits for the element to "
        "exist and be ready, up to a default timeout of 30 seconds, and a mistyped selector therefore makes the program pause "
        "that long and then raise TimeoutError. The sequence shows the exchange: the request, the wait, the failure, and the "
        "quick check that answers immediately. In the recorded run in Firefox 155 the mistyped click waited 30 seconds and raised "
        "TimeoutError; is_visible() returned False and query_selector() returned None in under a second; and the same click "
        "with timeout=500 raised after 0.6 seconds. The documentation of the library adds that is_visible() does not wait for "
        "the element to become visible. This waiting is Playwright's central design, announced with the Python preview of "
        "30 September 2020 as reliable, timeout-free automation, and it is the difference a student meets first when moving from "
        "Selenium, where find_element answers at once and raises NoSuchElementException.",
        "Locators wait 30 seconds; is_visible() answers at once.")

# ---- 23 choosing the tool -------------------------------------------------------------------------------------------------
dg, dcap = diagram("ChoosingTheTool", "activity", (0.5, 1.4, 9.0, 3.2),
                   grid={"page": (0, 0), "see": (0, 1), "api": (0, 2), "static": (0, 3), "drive": (0, 4),
                         "open": (1, 1), "json": (1, 2), "soup": (1, 3)},
                   cols=[(0.45, 3.9), (4.9, 3.6)], rows_n=5, starts=(-1, 0), ends={"type": "bar", "row": 1, "row2": 4, "x": 8.9},
                   routes={("start", "page"): "h", ("drive", "end"): "h"}, fs=9, nh=0.46, dh=0.5)
dg["did"] = "ChoosingTheTool"
content("Which tool for which page", "The conclusion of the chapter, as questions asked of the page in front of the program",
        [dg, dcap],
        "The chapter is best taught as a choice of tool by the page in front of the program, and this is that choice as an "
        "activity. If the user should see the page in a browser, webbrowser.open launches it. Otherwise, if the service "
        "offers an API, requests.get on the endpoint followed by json.loads gets exactly the data, which is the better "
        "choice whenever one exists. Otherwise, if the data is in the HTML that requests downloads, Beautiful Soup parses the "
        "text and select finds the elements. Only when a script builds the page, or a login is needed, does the program need "
        "Selenium or Playwright to drive a real browser. Whatever the tool, a program should send raise_for_status, a timeout "
        "and a pause between requests, read robots.txt before crawling, and remember that a driven browser still reveals itself "
        "through the user-agent string and flags such as navigator.webdriver, so a ticketing or shopping site may still refuse it.",
        "Show it, ask its API, parse its HTML; drive a browser last.")

# ---- 24 summary: the mind map -------------------------------------------------------------------------------------------
dg, dcap = diagram("WebScrapingAtAGlance", "mindmap", (0.5, 1.4, 9.0, 3.35), fs=9, root_w=1.5)
dg["did"] = "WebScrapingAtAGlance"
content("The chapter in one map", "Six branches; the slides of each branch hold the examples",
        [dg, dcap],
        "These six branches are the route of the deck. The address and the manners of the web come first: a URL has a "
        "scheme, a host, a path, a query and a fragment, every answer begins with a status code, and a robots.txt file asks "
        "crawlers to keep away. Fetching a page is webbrowser.open to show it to the user, requests.get to download it into "
        "the program and raise_for_status to stop on a bad download. A web service has an endpoint, an API key and a JSON "
        "answer. Parsing HTML means elements, the Developer Tools and select with a CSS selector. The three projects and the "
        "practice programs put these together: searchpypi.py, downloadXkcdComics.py and link verification. And driving a "
        "browser is Selenium with webdriver.Firefox() and Playwright, headless by default, for the pages a script builds. "
        "Together they answer the first question of the chapter, which tool reaches which page, and the slides that say where "
        "a printed line differs answer the second.",
        "If a branch feels unproven, its slides hold the example.")

# ---- 25 resources ----------------------------------------------------------------------------------------------------------
PUB = {p[0]: p for p in RD.PUBS}
_read = [["The textbook, chapter 13 - free online", PUB["P01"][2]],
         ["Requests: Quickstart", PUB["P15"][2]],
         ["Beautiful Soup documentation", PUB["P17"][2]]]
_ref = [["urllib.robotparser, Python 3.14", PUB["P05"][2]],
        ["RFC 9309: Robots Exclusion Protocol", PUB["P28"][2]],
        ["Selenium: locator strategies", PUB["P18"][2]],
        ["Playwright for Python: locators", PUB["P23"][2]]]
_hist = [["A Standard for Robot Exclusion (Koster, 1994)", STORY["KosterRobots1994"]["link"]],
         ["Beautiful Soup, by Leonard Richardson", STORY["RichardsonBeautifulSoup2004"]["link"]],
         ["Selenium history", STORY["HugginsSelenium2004"]["link"]],
         ["Requests release history (HISTORY.md)", STORY["ReitzRequests2011"]["link"]]]
LINKS = [r[1] for r in _read + _ref + _hist]
json.dump({"_version": __version__, "links": LINKS}, open(os.path.join(HERE, "links_v1_0_0.json"), "w"), indent=1)
content("Where to go from here", "Every link was opened on the day this deck was made",
        [{"t": "links", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.55, "fs": 9.5, "groups": [
            {"head": "Read", "rows": _read}, {"head": "Reference", "rows": _ref}, {"head": "History", "rows": _hist}]}],
        "Every link on this slide was opened on the day the deck was made, and the build records the status each answered. "
        "The textbook chapter is free to read online and holds every program of the chapter, the documents of requests and "
        "Beautiful Soup cover what this deck added to the chapter, and the reference links are the official pages for the "
        "standard library's robots.txt parser, the RFC that defines the exclusion protocol, and the locator rules of Selenium and "
        "Playwright. The history links are the sources behind the stories: Koster's note of 1994, Richardson's page for "
        "Beautiful Soup, the history of Selenium and the release history of Requests. Two more stories of this chapter, "
        "Matthew Gray's Wanderer of 1993 and the Playwright announcement of 2020, are told in the notes of the crawler and "
        "Playwright slides.",
        "Textbook, documentation and history, opened the day this deck was built.")

# ---- 26 closing -----------------------------------------------------------------------------------------------------------
content("What you should now be able to say", "Four claims, each carried by a result you saw printed",
        [{"t": "bullets", "x": 0.6, "y": 1.5, "w": 8.8, "h": 2.4, "fs": 15, "items": [
            "I choose the tool by the page: show it, ask its API, parse its HTML, or drive a browser.",
            "I check every download: raise_for_status, a timeout, and chunks to a file.",
            "I read robots.txt first and pause between requests; it is a request, not a lock.",
            "I select elements with a CSS selector, never a regular expression."]},
         {"t": "chips", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.6, "fs": 13, "big": True,
          "items": ["%d rows run" % sum(len(v) for v in G.values()), "%d programs run" % len(PROGS), "8 diagrams"]}],
        "Four claims, each carried by a result you saw printed. If you can say them in your own words and run the examples "
        "yourself, you have the chapter. The next chapters of the book work with spreadsheets, documents and email, and every "
        "one of them can start from a page this chapter taught a program to fetch.",
        "Questions are welcome; bring one page your program could not read and say why.")

# ---- agenda ---------------------------------------------------------------------------------------------------------------
_t = {s["title"]: i + 1 for i, s in enumerate(S)}
_parts = [("The address and the manners", "Addresses, status codes and the user agent", "Robots.txt, agreed on 30 June 1994"),
          ("Fetching a page", "webbrowser: show the page to the user", "Requests, conceived 13 February 2011"),
          ("A web service and its API", "A weather API: one call, one JSON answer", "Two calls, one answer feeding the next"),
          ("Parsing HTML with Beautiful Soup", "Beautiful Soup: select, then read", "Beautiful Soup, for awful pages, since 2004"),
          ("The chapter's programs", "searchpypi.py: where today's web differs", "A crawler that reads robots.txt first"),
          ("Driving a browser: Selenium and Playwright", "When the page is built by a script", "Which tool for which page"),
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
        {"n": str(_nstory), "label": "true stories, each with who, where, when and a link"},
        {"n": str(_nconsole), "label": "consoles and programs, all run before they were shown"}]}]
S[1]["sub"] = "Six parts and a summary; every range is a run of slides you can jump to"
S[1]["take"] = "Six parts, from an address to a driven browser."
S[1]["notes"] = ("The route has six parts and a summary. It starts with the address and the manners of the web, the URL, the "
                 "status code, the user agent and the robots.txt file, then fetching a page with webbrowser and requests, then "
                 "a web service answered in JSON, then parsing HTML with Beautiful Soup, then the chapter's own programs and a "
                 "crawler that reads robots.txt first, and then driving a real browser with Selenium and Playwright, ending "
                 "with a one-map summary and the resources. The ranges name the exact slides, so you can return to the part "
                 "you need. Four of the slides are true stories that explain where a tool of this chapter came from, and "
                 "eight of the slides carry the chapter's narrative diagrams, drawn from the same specifications as the "
                 "interactive page.")

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
plan = {"meta": {"title": "Chapter 13: Web Scraping", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": len(S), "diagrams": SHOWN}, "slides": S}
out = os.path.join(HERE, "deck_plan_v1_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides; diagrams on slides", dict(sorted(SHOWN.items(), key=lambda kv: kv[1])))

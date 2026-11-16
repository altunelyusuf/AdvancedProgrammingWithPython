"""Chapter 20 deck visuals, version 2.0.0: the executed result of every code example drawn as a native table, a native chart or a drawn flow with arrows.
Every number, string and truth value shown is taken from the run of the example's own code (the namespace `ns` and the printed text `out` that the
generic builder 08-tooling/chapter_deck_build_v2_2_0.py passes in); nothing is typed in by hand except plain-language names of boxes and columns.
Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants."""
__version__ = "2.0.0"
import ast
from deck_kit_v2_1_0 import C, MONO, arrow, chart, label_shape as _label_shape, table as _table, tb, rect


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


def flow(s, x, y, w, items, kinds=None, h=0.5, fs=9.5, gap=0.32, mono=False):
    n = len(items)
    bw = (w - gap * (n - 1)) / n
    for i, t in enumerate(items):
        xx = x + i * (bw + gap)
        box(s, xx, y, bw, h, t, kinds[i] if kinds else "plain", fs, mono)
        if i < n - 1:
            arrow(s, xx + bw + 0.02, y + h / 2, xx + bw + gap - 0.02, y + h / 2, C["muted"], 1.5)
    return bw


def lines(out):
    return out.rstrip("\n").split("\n")


def lit(text):
    return ast.literal_eval(text)


# ------------------------------------------------------------------ part 1: the Gmail API
@need(1.1)
def v_setup(s, x, y, w, h, ns, out):
    L = lines(out)
    flow(s, x, y + 0.02, w, ["credentials.json\nfrom Google, once", "init() reads it\nand signs you in", "token.json\nthe saved pass", "API calls\nsend, read, search"],
         ["red", "plain", "plain", "plain"], h=0.5, fs=10, gap=0.35)
    rows = [["What the run printed", "Meaning"], [L[0], "init() stops: credentials.json is not in this folder"], [L[1], "the scope asked for, and not signed in yet"]]
    table(s, x, y + 0.6, w, rows, [4.2, 5.0], rowh=0.24, mono_cols=(0,), cell_fill={(1, 0): C["redLight"]}, fs=10)


@need(1.1)
def v_send(s, x, y, w, h, ns, out):
    L = lines(out)
    to, frm, sub = L[0].split(" | ")
    rows = [["Header or part", "What ezgmail handed to Google"], ["To", to], ["From", frm], ["Subject", sub], ["Body", L[1]]]
    table(s, x, y, w, rows, [2.2, 7.0], rowh=0.24, mono_cols=(1,), fs=10)


@need(1.0)
def v_read(s, x, y, w, h, ns, out):
    L = lines(out)
    snd, sub, body = L[0].split(" | ")
    found, query = L[1], L[2]
    rows = [["What ezgmail gave back", "Value"], ["m.sender", snd], ["m.subject", sub], ["m.body", body],
            ["ezgmail.search(...): threads found; the query that reached Gmail", found + " ; " + query]]
    table(s, x, y, w, rows, [5.2, 4.0], rowh=0.22, mono_cols=(0, 1), fs=9.5)


@need(1.1)
def v_reply(s, x, y, w, h, ns, out):
    L = lines(out)
    tid, to, sub = L[0].split(" | ")
    rows = [["What reply() sent", "Value"], ["threadId (the same thread as the mail answered)", tid], ["To (the sender of that mail)", to], ["Subject (unchanged)", sub], ["Body", L[1]]]
    table(s, x, y, w, rows, [4.4, 4.8], rowh=0.24, mono_cols=(1,), cell_fill={(1, 1): C["greenLight"]}, fs=10)


@need(1.3)
def v_download(s, x, y, w, h, ns, out):
    L = lines(out)
    asked, inbox, here = lit(L[0]), lit(L[1].split("] ", 1)[0] + "]"), lit(L[1].split("] ", 1)[1])
    flow(s, x, y + 0.02, w, ["downloadFolder='inbox'", "the name '%s'" % asked[0], "written one folder up"], ["teal", "amber", "red"], h=0.5, fs=10, gap=0.4)
    rows = [["Where we looked", "What is there"], ["inbox (the folder asked for)", str(inbox)], ["the working folder (outside inbox)", str(here)]]
    table(s, x, y + 0.66, w, rows, [4.2, 5.0], rowh=0.26, mono_cols=(1,), cell_fill={(1, 1): C["greenLight"], (2, 1): C["redLight"]}, fs=10)


# ------------------------------------------------------------------ part 2: mail as a protocol
@need(1.45)
def v_build(s, x, y, w, h, ns, out):
    L = lines(out)
    types = lit(L[0])
    rows = [["Order of walk()", "Content type"]] + [[str(i + 1), t] for i, t in enumerate(types)]
    table(s, x, y, w * 0.55, rows, [1.3, 3.65], rowh=0.24, mono_cols=(1,), cell_fill={(1, 1): C["tealLight"], (2, 1): C["tealLight"]}, fs=10)
    box(s, x + w * 0.6, y + 0.03, w * 0.4, 0.38, "attachments: %s" % lit(L[1])[0], "amber", 10, True)
    box(s, x + w * 0.6, y + 0.5, w * 0.4, 0.38, "best body to show: %s" % L[2], "green", 10, True)
    note(s, x + w * 0.6, y + 0.95, w * 0.4, "mixed holds the alternatives and the attachment.", h=0.4, fs=9.5)


@need(1.25)
def v_headers(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["What the program says", "What travels or is returned"],
            ["Subject, as typed", L[0].split(" | ")[0]],
            ["first line on the wire", L[1]],
            ["To, with a name", L[0].split(" | ")[1]],
            ["parseaddr(...)", L[2]],
            ["a header value with a line break", L[3]]]
    table(s, x, y, w, rows, [3.4, 5.8], rowh=0.24, mono_cols=(1,), cell_fill={(2, 1): C["amberLight"], (5, 1): C["redLight"]}, fs=10)


@need(0.7)
def v_starttls(s, x, y, w, h, ns, out):
    L = lines(out)
    ehlo, offered = L[0].split(" ")
    flow(s, x, y + 0.02, w, ["connect in\nplain text", "EHLO: code %s,\nSTARTTLS offered: %s" % (ehlo, offered), "starttls():\ncode " + L[1], "the socket is now\n" + L[2]], ["plain", "amber", "teal", "green"], h=0.6, fs=10, gap=0.35)


@need(0.65)
def v_refusals(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["What happened", "What smtplib did", "The run printed"],
            ["one of two recipients refused", "sendmail() returned a dictionary", L[0]],
            ["every recipient refused", "raised SMTPRecipientsRefused", L[1]]]
    table(s, x, y, w, rows, [2.5, 2.7, 4.0], rowh=0.21, mono_cols=(2,), cell_fill={(1, 2): C["amberLight"], (2, 2): C["redLight"]}, fs=9)


@need(0.9)
def v_envelope(s, x, y, w, h, ns, out):
    L = lines(out)
    env = ns["sent"][0]
    rows = [["Where", "Who it names"], ["headers (To:) in the text", "jon@example.org"], ["envelope: RCPT TO", ", ".join(env.rcpt_tos)],
            ["second person named in the text", L[1].split(": ")[1]]]
    table(s, x, y, w, rows, [4.0, 5.2], rowh=0.22, mono_cols=(1,), cell_fill={(2, 1): C["amberLight"], (3, 1): C["greenLight"]}, fs=9.5)


# ------------------------------------------------------------------ part 3: texts by email
@need(1.15)
def v_gateway(s, x, y, w, h, ns, out):
    L = lines(out)
    gw = ns["gateways"]
    chart(s, "col", x, y, w * 0.4, max(h, 1.15), ["carriers", "domains"], [("count", [len(gw), len(set(gw.values()))])], fs=10, legend=False, gap=60, vmax=5, major=1)
    rows = [["Printed", "Meaning"], [L[0], "number at the gateway: a text to that phone"], [L[1].split("; ")[0], "domains are fewer than carriers"], [L[2].split(" ", 1)[0] + " days", "since AT&T closed the gateway"]]
    table(s, x + w * 0.43, y + 0.05, w * 0.57, rows, [2.3, 3.0], rowh=0.28, mono_cols=(0,), cell_fill={(3, 0): C["redLight"]}, fs=9.5)


@need(1.1)
def v_segments(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["Characters", "Coding", "Units", "Texts"]]
    cats, vals = [], []
    for ln in L:
        n, rest = ln.split(" ", 1)
        code, units, seg = lit(rest)
        rows.append([n, code, str(units), str(seg)])
        cats.append("%s chars, %s" % (n, code))
        vals.append(seg)
    table(s, x, y, w * 0.5, rows, [1.1, 1.0, 1.0, 1.0], rowh=0.22, mono_cols=(0, 1, 2, 3), cell_fill={(4, 1): C["amberLight"]}, fs=9.5)
    chart(s, "col", x + w * 0.53, y, w * 0.47, max(h, 1.1), cats, [("texts (segments)", vals)], fs=9, legend=False, gap=50, vmax=3, major=1)


# ------------------------------------------------------------------ part 4: push notifications
@need(0.8)
def v_ntfyPub(s, x, y, w, h, ns, out):
    L = lines(out)
    method, url = L[0].split(" ", 1)
    body, size = L[1].rsplit(" ", 1)
    flow(s, x, y + 0.02, w, ["%s\n%s" % (method, url.rsplit("/", 1)[0] + "/"), "topic (the path)\n" + url.rsplit("/", 1)[1], "body\n" + body, "Content-Length\n" + size + "; no Content-Type"],
         ["teal", "amber", "plain", "plain"], h=0.6, fs=10, gap=0.3)


@need(0.95)
def v_ntfyHdr(s, x, y, w, h, ns, out):
    L = lines(out)
    d = lit(L[0])
    rows = [["Header sent", "Value in the request"]] + [[k, v] for k, v in d.items()] + [["Title with a dotless i", L[1]]]
    table(s, x, y, w, rows, [3.0, 6.2], rowh=0.2, mono_cols=(0, 1), cell_fill={(4, 1): C["redLight"]}, fs=9.5)


@need(1.1)
def v_ntfyPoll(s, x, y, w, h, ns, out):
    L = lines(out)
    kinds = lit(L[0])
    chart(s, "col", x, y, w * 0.3, max(h, 1.1), ["open", "message"], [("events", [kinds.count("open"), kinds.count("message")])], fs=10, legend=False, gap=60, vmax=3, major=1)
    rows = [["Clock time (UTC)", "Title", "Message"]]
    for ln in L[1:3]:
        t, rest = ln.split(" ", 1)
        ti, m = rest.split(" ", 1)
        rows.append([t, ti, m])
    table(s, x + w * 0.33, y + 0.05, w * 0.67, rows, [1.7, 1.2, 3.2], rowh=0.28, mono_cols=(0, 1, 2), fs=10)


@need(1.2)
def v_secrecy(s, x, y, w, h, ns, out):
    L = lines(out)
    a = float(L[0].split(": ")[1].split(" ")[0])
    b = float(L[1].split(" ")[0])
    c = float(L[2].split("; ")[1].split(" ")[0])
    chart(s, "col", x, y, w * 0.55, max(h, 1.2), ["8 letters", "18 characters", "token_urlsafe(18)"], [("bits of secrecy", [b, a, c])], fs=10, legend=False, gap=50, vmax=160, major=40)
    box(s, x + w * 0.6, y + 0.05, w * 0.4, 0.42, "short name: guessable", "red", 10)
    box(s, x + w * 0.6, y + 0.55, w * 0.4, 0.42, "random name: not guessable", "green", 10)
    note(s, x + w * 0.6, y + 1.02, w * 0.4, "message limit: " + L[3], fs=9, h=0.3)


# ------------------------------------------------------------------ part 5: practice programs
@need(0.95)
def v_unsub(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["Where the address is found", "What the program found"], ["the link whose text says Unsubscribe", ", ".join(lit(L[0]))], ["List-Unsubscribe header, two choices", " and ".join(lit(L[1]))]]
    table(s, x, y, w, rows, [3.4, 5.8], rowh=0.25, mono_cols=(1,), cell_fill={(1, 1): C["greenLight"], (2, 1): C["greenLight"]}, fs=9.5)
    note(s, x, y + 0.78, w, "Not run here: opening the link. Unsubscribe only from senders you know.", fs=9, h=0.2)


@need(1.0)
def v_umbrella(s, x, y, w, h, ns, out):
    L = lines(out)
    names, chances, take = [], [], []
    for ln in L:
        nm, d = ln.split(" ", 1)
        d = lit(d)
        names.append(nm)
        chances.append(d["chance"])
        take.append(str(d["umbrella"]))
    chart(s, "col", x, y, w * 0.5, max(h, 1.0), names, [("chance of rain (%)", chances)], fs=10, legend=False, gap=60, vmax=100, major=25)
    rows = [["Period", "Take an umbrella (chance 50 or more)"]] + [[a, b] for a, b in zip(names, take)]
    table(s, x + w * 0.55, y + 0.05, w * 0.45, rows, [1.2, 3.1], rowh=0.28, mono_cols=(1,), cell_fill={(1, 1): C["amberLight"], (2, 1): C["greenLight"]}, fs=10)


@need(0.95)
def v_control(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["Mail received", "Decision", "The run printed"],
            ["a wrong password", "stop at the first check", L[0]],
            ["the right password, a command not on the list", "stop at the second check", L[1]],
            ["the right password, an allowed command", "run it as a list of arguments", L[2]]]
    table(s, x, y, w, rows, [3.5, 2.4, 3.3], rowh=0.24, mono_cols=(2,), cell_fill={(1, 2): C["redLight"], (2, 2): C["redLight"], (3, 2): C["greenLight"]}, fs=9.5)


VISUALS = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("v_") and callable(v)}

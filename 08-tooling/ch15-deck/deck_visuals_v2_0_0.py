"""Chapter 15 deck visuals, version 2.0.0: the executed result of every code example drawn as a native table, a native chart or a drawn
diagram. Every number, string and truth value shown is taken from the run of the example's own code (the namespace `ns` and the
printed text `out` that deck_build_v2_0_0.py (chapter 15) passes in); nothing is typed in by hand except plain-language names of columns and boxes
and the one-line meanings of a request or a parameter, which are named as such on the slide.
Google was never reached: every spreadsheet result comes from the real ezsheets library talking to the stand-in for Google (google_standin).
Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants."""
__version__ = "2.0.0"
import collections
import re
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from deck_kit_v2_0_0 import C, MONO, arrow, chart, label_shape as _label_shape, table as _table, tb, rect, line_seg, _style_run


def col_letter(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def table(s, x, y, w, rows, colw, fs=10.5, **kw):
    """the kit table with the visuals' default font size (10.5 pt)"""
    return _table(s, x, y, w, rows, colw, fs=fs, **kw)


def label_shape(s, x, y, w, h, text, fill, color, size=11, bold=False, line=None, font=None, radius=0.12):
    """the kit's label shape; a text with line breaks becomes one centred paragraph per line"""
    parts = text.split("\n")
    sh = _label_shape(s, x, y, w, h, parts[0], fill, color, size=size, bold=bold, line=line, font=font, radius=radius)
    for t in parts[1:]:
        p = sh.text_frame.add_paragraph()
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = t
        _style_run(r, size, color, bold, False, font)
    return sh


def need(h):
    def deco(f):
        f.need = h
        return f
    return deco


def chip(s, x, y, w, h, text, kind="plain", fs=10.5, mono=True):
    fill, col = {"plain": (C["card"], C["ink"]), "teal": (C["tealLight"], C["ink"]), "amber": (C["amberLight"], C["ink"]),
                 "green": (C["greenLight"], C["ink"]), "grey": (C["grey"], C["muted"]), "red": (C["redLight"], C["ink"])}[kind]
    return label_shape(s, x, y, w, h, text, fill, col, size=fs, font=MONO if mono else None, line=C["line"], radius=0.15)


def short(t, n):
    t = str(t)
    return t if len(t) <= n else t[:n - 3] + "..."


def note(s, x, y, w, text, h=0.24, fs=9.5):
    return tb(s, x, y, w, h, text, fs, C["muted"], italic=True, name="visual note")


def flow(s, x, y, w, items, kinds=None, h=0.5, fs=9.5, gap=0.32, font_mono=False):
    """a row of label shapes joined by arrows; items: texts (a line break makes two lines)"""
    n = len(items)
    bw = (w - gap * (n - 1)) / n
    fill = {"plain": C["card"], "red": C["redLight"], "amber": C["amberLight"], "teal": C["tealLight"], "green": C["greenLight"], "grey": C["grey"]}
    for i, t in enumerate(items):
        k = kinds[i] if kinds else "plain"
        xx = x + i * (bw + gap)
        label_shape(s, xx, y, bw, h, t, fill[k], C["ink"], size=fs, line=C["line"], radius=0.12, font=MONO if font_mono else None)
        if i < n - 1:
            arrow(s, xx + bw + 0.02, y + h / 2, xx + bw + gap - 0.02, y + h / 2, C["muted"], 1.5)
    return bw


def grid(s, x, y, w, cells, ncols, nrows, fills=None, fs=9, rowh=0.2, first_col=1, first_row=1, colw0=0.5, width_of=None, name="sheet grid"):
    """a drawn sheet: a native table with the column letters on top and the row numbers on the left.
    cells: {'A1': text}; fills: {'A1': colour}"""
    cols = [col_letter(first_col + j) for j in range(ncols)]
    rows = [[""] + cols]
    cf = {}
    for i in range(nrows):
        r = first_row + i
        rows.append([str(r)] + [str(cells.get("%s%d" % (c, r), "")) or " " for c in cols])
        for j, c in enumerate(cols):
            if fills and "%s%d" % (c, r) in fills:
                cf[(i + 1, j + 1)] = fills["%s%d" % (c, r)]
        cf[(i + 1, 0)] = C["grey"]
    colw = [colw0] + [(width_of(c) if width_of else 1.0) for c in cols]
    return table(s, x, y, w, rows, colw, fs=fs, rowh=rowh, cell_fill=cf, align_cols={j: PP_ALIGN.CENTER for j in range(ncols + 1)}, bold_cols=(0,), name=name)


def cells_of(rows):
    """{'A1': text} from a list of rows (the way ezsheets returns them)"""
    return {"%s%d" % (col_letter(j), i): v for i, row in enumerate(rows, 1) for j, v in enumerate(row, 1)}


def tabs(s, x, y, w, names, active=None, h=0.46, fs=10):
    bw = min(1.9, (w - 0.1 * (len(names) - 1)) / len(names))
    for i, n in enumerate(names):
        a = n == active
        label_shape(s, x + i * (bw + 0.1), y, bw, h, "%d\n%s" % (i, short(n, 22)), C["amberLight"] if a else C["card"], C["ink"], size=fs, bold=a, line=C["amber"] if a else C["line"], radius=0.2)
    return bw


def kv(out):
    """key: value lines of a printed output"""
    d = collections.OrderedDict()
    for line in out.splitlines():
        if ": " in line:
            k, v = line.split(": ", 1)
            d[k.strip()] = v.strip()
    return d


def req_kind(m, p):
    """the plain-language kind of a request of the stand-in log"""
    if p.startswith("/drive/v3/files") and m == "GET":
        return "GET  drive files (list or export)"
    if p.startswith("/drive") or p.startswith("/upload"):
        return "%-6s drive file" % m
    if ":batchUpdate" in p:
        return "POST batchUpdate (title, size, sheets)"
    if "/values/" in p:
        return "%-4s cell values" % m
    if ":copyTo" in p:
        return "POST copyTo"
    if p == "/v4/spreadsheets":
        return "POST create spreadsheet"
    return "GET  spreadsheet properties"


# ------------------------------------------------------------------ part 1
@need(1.45)
def v_setup_state(s, x, y, w, h, ns, out):
    d = kv(out)
    rows = [["What EZSheets reports", "Value from the run"], ["release", out.splitlines()[0]], ["signed in (IS_INITIALIZED)", d["signed in"]],
            ["sheets scope", short(ns["ezsheets"].SCOPES_SHEETS[0].replace("https://www.googleapis.com/auth/", ".../auth/"), 40)],
            ["drive scope", short(ns["ezsheets"].SCOPES_DRIVE[0].replace("https://www.googleapis.com/auth/", ".../auth/"), 40)]]
    table(s, x, y, w * 0.58, rows, [1.9, 2.6], rowh=0.3, mono_cols=(1,), cell_fill={(2, 1): C["amberLight"]}, fs=9.5)
    bx = x + w * 0.64
    label_shape(s, bx, y, w * 0.36, 0.38, "import ezsheets", C["card"], C["ink"], size=10, line=C["line"], font=MONO)
    arrow(s, bx + w * 0.18, y + 0.4, bx + w * 0.18, y + 0.58, C["muted"], 1.4)
    label_shape(s, bx, y + 0.6, w * 0.36, 0.38, "signed in: %s" % d["signed in"], C["amberLight"], C["ink"], size=10, line=C["line"], font=MONO)
    arrow(s, bx + w * 0.18, y + 1.0, bx + w * 0.18, y + 1.18, C["muted"], 1.4)
    label_shape(s, bx, y + 1.2, w * 0.36, 0.3, "no request leaves yet", C["grey"], C["muted"], size=9.5, line=C["line"])


@need(1.55)
def v_token_file(s, x, y, w, h, ns, out):
    import json
    d = json.loads(ns["creds"].to_json())
    secret = {"token", "refresh_token"}
    rows = [["Field of the token file", "Value (made up for this slide)"]] + [[k, short(v if not isinstance(v, list) else v[0].replace("https://www.googleapis.com/auth/", ".../auth/"), 38) or "(empty)"] for k, v in d.items()]
    cf = {(i, j): C["amberLight"] for i, k in enumerate(d, 1) if k in secret for j in (0, 1)}
    table(s, x, y, w * 0.62, rows, [1.8, 2.7], rowh=min(0.24, h / len(rows)), mono_cols=(0, 1), cell_fill=cf, fs=9)
    bx = x + w * 0.67
    label_shape(s, bx, y, w * 0.33, 0.42, "Credentials object", C["tealLight"], C["ink"], size=10, line=C["line"])
    arrow(s, bx + w * 0.165, y + 0.44, bx + w * 0.165, y + 0.66, C["muted"], 1.4)
    label_shape(s, bx, y + 0.68, w * 0.33, 0.42, "pickle.dumps", C["card"], C["ink"], size=10, line=C["line"], font=MONO)
    arrow(s, bx + w * 0.165, y + 1.12, bx + w * 0.165, y + 1.34, C["muted"], 1.4)
    label_shape(s, bx, y + 1.36, w * 0.33, 0.42, "token-sheets.pickle", C["amberLight"], C["ink"], size=10, line=C["line"], font=MONO)
    note(s, x, y + h - 0.2, w * 0.62, "amber: the two secrets; whoever holds them can open your sheets", fs=9)


@need(1.5)
def v_auth_url(s, x, y, w, h, ns, out):
    q = ns["q"]
    mean = {"response_type": "ask for a one-time code", "access_type": "also give a refresh token", "redirect_uri": "come back to this computer",
            "code_challenge_method": "the challenge is a SHA-256 hash", "code_challenge": "%d characters, a hash of the secret" % len(q["code_challenge"]),
            "scope": "the permission asked for"}
    keys = ["response_type", "access_type", "redirect_uri", "code_challenge_method", "code_challenge", "scope"]
    rows = [["Part of the address", "Value", "Plain meaning"]] + [[k, short(q[k] if k != "code_challenge" else "(%d chars)" % len(q[k]), 20).replace("https://www.googleapis.com/auth/", ".../auth/"), mean[k]] for k in keys]
    table(s, x, y, w * 0.74, rows, [2.0, 2.0, 2.6], rowh=min(0.24, h / len(rows)), mono_cols=(0, 1), fs=9)
    bx = x + w * 0.79
    label_shape(s, bx, y, w * 0.21, 0.4, "program", C["tealLight"], C["ink"], size=10, line=C["line"])
    arrow(s, bx + w * 0.105, y + 0.42, bx + w * 0.105, y + 0.62, C["muted"], 1.4)
    label_shape(s, bx, y + 0.64, w * 0.21, 0.4, "browser opens\nthis address", C["card"], C["ink"], size=9, line=C["line"])
    arrow(s, bx + w * 0.105, y + 1.06, bx + w * 0.105, y + 1.26, C["muted"], 1.4)
    label_shape(s, bx, y + 1.28, w * 0.21, 0.4, "Google asks\nyou to agree", C["amberLight"], C["ink"], size=9, line=C["line"])


@need(1.35)
def v_pkce(s, x, y, w, h, ns, out):
    v, c = ns["verifier"].decode(), ns["challenge"].decode()
    flow(s, x, y + 0.1, w, ["verifier\n(kept secret)\n%s..." % v[:10], "SHA-256\nthen base64url", "challenge\n(sent in the address)\n%s..." % c[:10], "Google keeps\nthe challenge"],
         ["amber", "plain", "teal", "green"], h=0.85, gap=0.45, fs=10)
    note(s, x, y + 1.05, w, "later: the program shows the verifier; Google hashes it again, and only the same program can match the challenge", fs=9.5)


@need(1.45)
def v_token_pickle(s, x, y, w, h, ns, out):
    lines = out.splitlines()
    flow(s, x, y + 0.1, w, ["token-sheets.pickle\n(%s)" % lines[0].replace("file written: ", ""), "import ezsheets\ncalls pickle.load", "the file's own call\nis made at once", "printed: %s" % lines[1]],
         ["amber", "plain", "red", "red"], h=0.8, gap=0.4, fs=9.5)
    note(s, x, y + 1.05, w, "here the call only prints a line; in an attack it could be any code, with your rights", fs=9.5)


@need(1.45)
def v_token_expiry(s, x, y, w, h, ns, out):
    hours = {"fresh": 1, "stale": -1, "week old": -168}
    rows = [["Token", "Expires", "valid", "expired", "What the library does"]]
    cf = {}
    for i, line in enumerate(out.splitlines(), 1):
        name, rest = line.split(" | valid: ")
        valid, expired = rest.split(" | expired: ")
        hh = hours[name]
        rows.append([name, ("in %d h" % hh) if hh > 0 else ("%d h ago" % -hh), valid, expired, "sends it as it is" if valid == "True" else "renews it with the refresh token"])
        cf[(i, 2)] = C["greenLight"] if valid == "True" else C["redLight"]
        cf[(i, 3)] = C["redLight"] if expired == "True" else C["greenLight"]
    table(s, x, y, w * 0.78, rows, [1.2, 1.1, 0.8, 0.9, 3.0], rowh=0.3, mono_cols=(2, 3), cell_fill=cf, fs=10)
    note(s, x, y + 1.3, w, "Testing status of the app: the refresh token itself dies after seven days (Google's identity page, finding F7)", fs=9.5)


# ------------------------------------------------------------------ part 2
@need(1.55)
def v_create_list(s, x, y, w, h, ns, out):
    listing = eval(out.splitlines()[1])
    rows = [["Spreadsheet id", "Title"]] + [[k, v] for k, v in listing.items()]
    table(s, x, y, w * 0.4, rows, [1.2, 2.0], rowh=0.3, mono_cols=(0,), fs=10)
    cnt = collections.Counter(req_kind(m, p) for m, p, q, b in ns["g"].log)
    rows2 = [["Requests the library sent", "Times"]] + [[k, str(v)] for k, v in cnt.items()]
    table(s, x + w * 0.45, y, w * 0.55, rows2, [3.4, 0.7], rowh=min(0.3, h / len(rows2)), fs=9.5, align_cols={1: PP_ALIGN.CENTER})
    note(s, x, y + 1.05, w * 0.4, "list of the stand-in account", fs=9)


@need(1.3)
def v_open_three_ways(s, x, y, w, h, ns, out):
    lines = out.splitlines()
    rows = [["Call", "Result"], ["Spreadsheet('SHEET123')", lines[0]], ["Spreadsheet(url) with .../edit#gid=0", lines[1]], ["getIdFromUrl(url)", lines[2]],
            ["getIdFromUrl('.../d/SHEET123')", lines[3] + "   (last character lost)"]]
    table(s, x, y, w * 0.62, rows, [3.0, 2.6], rowh=0.3, mono_cols=(0, 1), cell_fill={(4, 0): C["redLight"], (4, 1): C["redLight"]}, fs=9.5)
    bx = x + w * 0.67
    label_shape(s, bx, y, w * 0.33, 0.36, "id or address", C["card"], C["ink"], size=10, line=C["line"])
    arrow(s, bx + w * 0.165, y + 0.38, bx + w * 0.165, y + 0.56, C["muted"], 1.4)
    label_shape(s, bx, y + 0.58, w * 0.33, 0.36, "ezsheets.Spreadsheet", C["tealLight"], C["ink"], size=10, line=C["line"], font=MONO)
    arrow(s, bx + w * 0.165, y + 0.96, bx + w * 0.165, y + 1.14, C["muted"], 1.4)
    label_shape(s, bx, y + 1.16, w * 0.33, 0.34, "the same sheet: %s" % lines[0], C["greenLight"], C["ink"], size=10, line=C["line"])


@need(1.45)
def v_attributes(s, x, y, w, h, ns, out):
    ss = ns["ss"]
    errs = [l for l in out.splitlines() if " -> " in l]
    rows = [["Attribute", "Value", "Can you set it?"], ["title", short(ss.title, 30), "yes: a request is sent"], ["sheetTitles", str(ss.sheetTitles), errs[2].split(" -> ")[1][:34] + "..."],
            ["id", ss.id, "no: " + errs[0].split(" -> ")[1][:30] + "..."], ["url", short(ss.url.replace("https://", ""), 32), "no: " + errs[1].split(" -> ")[1][:30] + "..."]]
    table(s, x, y, w, rows, [1.3, 3.0, 4.5], rowh=0.3, mono_cols=(0, 1), cell_fill={(1, 2): C["greenLight"], (2, 2): C["redLight"], (3, 2): C["redLight"], (4, 2): C["redLight"]}, fs=9.5)
    note(s, x, y + 1.55, w, "the error text is the one printed by the run: a property without a setter", fs=9)


@need(1.35)
def v_upload_download(s, x, y, w, h, ns, out):
    names = [l.split(" -> ") for l in out.splitlines()[1:]]
    rows = [["Method", "File saved", "Title of the spreadsheet"]] + [["downloadAs" + f, n, "Sweigart Books (DO NOT DELETE)" if i == 0 else "same"] for i, (f, n) in enumerate(names)]
    cf = {(i, 1): C["amberLight"] for i in range(1, len(rows))}
    table(s, x, y, w * 0.8, rows, [1.6, 3.6, 2.6], rowh=min(0.22, h / len(rows)), mono_cols=(0, 1), cell_fill=cf, fs=9)
    note(s, x + w * 0.82, y, w * 0.18, "upload made the spreadsheet %r; spaces and brackets became underscores" % out.splitlines()[0], h=1.0, fs=9)


@need(1.3)
def v_delete_trash(s, x, y, w, h, ns, out):
    lines = out.splitlines()
    flow(s, x, y, w, ["ss.delete()", "request: " + lines[0], "still listed: %d spreadsheets" % len(eval(lines[1])), "delete(permanent=True)", "request: %s\nlisted now: %d" % (lines[2].split(" then ")[0], len(eval(lines[2].split(" then ")[1])))],
         ["plain", "amber", "amber", "plain", "green"], h=0.75, gap=0.22, fs=9)
    note(s, x, y + 0.9, w, "the Trash is a second life: listSpreadsheets does not leave a trashed spreadsheet out", fs=9.5)


# ------------------------------------------------------------------ part 3
@need(1.35)
def v_cell_rw(s, x, y, w, h, ns, out):
    sheet = ns["sheet"]
    rows = sheet.getRows()
    cells = cells_of(rows)
    grid(s, x, y, w * 0.46, cells, 3, 2, {"B2": C["amberLight"]}, fs=9, rowh=0.27, width_of=lambda c: 1.3, colw0=0.35)
    lines = out.splitlines()
    chip(s, x + w * 0.5, y, w * 0.5, 0.28, "reading four cells: " + lines[1].split(" requests")[0] + " requests", "green", fs=9)
    chip(s, x + w * 0.5, y + 0.35, w * 0.5, 0.28, "write: " + lines[2].split(" | ")[1], "amber", fs=9)
    chip(s, x + w * 0.5, y + 0.7, w * 0.5, 0.28, "local copy after the write: " + lines[2].split(" | ")[0] + " (a number)", "plain", fs=9)
    chip(s, x + w * 0.5, y + 1.05, w * 0.5, 0.28, "after refresh(): " + lines[3] + " (text)", "teal", fs=9)


@need(1.4)
def v_addresses(s, x, y, w, h, ns, out):
    E = ns["ezsheets"]
    calls = [("convertAddress('A2')", E.convertAddress("A2")), ("convertAddress(1, 2)", E.convertAddress(1, 2)), ("convertAddress((2, 5))", E.convertAddress((2, 5))),
             ("getColumnLetterOf(2)", E.getColumnLetterOf(2)), ("getColumnLetterOf(27)", E.getColumnLetterOf(27)), ("getColumnLetterOf(999)", E.getColumnLetterOf(999)),
             ("getColumnNumberOf('B')", E.getColumnNumberOf("B")), ("getColumnNumberOf('ZZZ')", E.getColumnNumberOf("ZZZ"))]
    rows = [["Call", "Result"]] + [[a, repr(b)] for a, b in calls[:4]]
    rows2 = [["Call", "Result"]] + [[a, repr(b)] for a, b in calls[4:]]
    table(s, x, y, w * 0.48, rows, [2.4, 1.2], rowh=0.27, mono_cols=(0, 1), fs=9.5)
    table(s, x + w * 0.52, y, w * 0.48, rows2, [2.4, 1.2], rowh=0.27, mono_cols=(0, 1), fs=9.5, cell_fill={(4, 1): C["amberLight"]})
    note(s, x, y + 1.4, w, "the results come from calling the library again with the same arguments; amber: the last column of a sheet", fs=9)


@need(1.3)
def v_rows_columns(s, x, y, w, h, ns, out):
    rows = ns["sheet"].getRows()
    cells = cells_of(rows)
    fills = {"A%d" % r: C["tealLight"] for r in range(1, len(rows) + 1)}
    for c in "ABC":
        fills["%s3" % c] = C["amberLight"]
    grid(s, x, y, w * 0.5, cells, 3, len(rows), fills, fs=9.5, rowh=0.28, width_of=lambda c: 1.4, colw0=0.35)
    chip(s, x + w * 0.55, y, w * 0.45, 0.3, "amber: updateRow(3, [...]) replaced row 3", "amber", fs=9, mono=False)
    chip(s, x + w * 0.55, y + 0.4, w * 0.45, 0.3, "teal: updateColumn(1, ...) wrote column A", "teal", fs=9, mono=False)
    note(s, x + w * 0.55, y + 0.8, w * 0.45, "one request each; the values are text", fs=9)
    note(s, x + w * 0.55, y + 1.05, w * 0.45, "first run: " + short(out.splitlines()[0], 40), fs=9)


@need(1.3)
def v_batch_writes(s, x, y, w, h, ns, out):
    lines = out.splitlines()
    a, b = int(re.findall(r"(\d+) request", lines[0])[0]), int(re.findall(r"(\d+) request", lines[1])[0])
    chart(s, "col", x, y, w * 0.55, max(h, 1.4), ["cell by cell", "updateColumn"], [("requests", [a, b])], fs=10, legend=False, gap=70, vmax=10, major=2)
    chip(s, x + w * 0.6, y + 0.15, w * 0.4, 0.3, "%d values, %d vs %d requests" % (len(ns["values"]), a, b), "teal", fs=9.5)
    note(s, x + w * 0.6, y + 0.6, w * 0.4, "Google counts requests per minute, not values: batch your writes", h=0.5, fs=9.5)


@need(1.55)
def v_sheet_tabs(s, x, y, w, h, ns, out):
    states = [eval(l) for l in out.splitlines()[1:]]
    labels = ["after createSheet('Eggs') and createSheet('Bacon', 0)", "after sheets[0].index = 2", "after sheets[1].delete()"]
    yy = y
    for lab, st in zip(labels, states):
        tb(s, x, yy, w * 0.42, 0.42, lab, 9.5, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="step")
        tabs(s, x + w * 0.44, yy, w * 0.56, list(st), None, h=0.42, fs=9)
        arrow(s, x + w * 0.415, yy + 0.21, x + w * 0.435, yy + 0.21, C["muted"], 1.5)
        yy += 0.5
    note(s, x, yy, w, "the first print was %s: Spreadsheet.Sheet() returns nothing; createSheet returns the Sheet" % out.splitlines()[0], fs=9.5)


@need(1.4)
def v_copy_clear(s, x, y, w, h, ns, out):
    tgt = ns["target"]
    cp = tgt.sheets[1].getRows()
    tb(s, x, y - 0.03, w * 0.42, 0.22, "the copy in the other spreadsheet", 9.5, C["muted"], italic=True)
    grid(s, x, y + 0.2, w * 0.42, cells_of(cp), 3, 2, {"A1": C["tealLight"]}, fs=8.5, rowh=0.24, width_of=lambda c: 1.0, colw0=0.3)
    arrow(s, x + w * 0.45, y + 0.7, x + w * 0.52, y + 0.7, C["muted"], 1.5)
    tb(s, x + w * 0.54, y - 0.03, w * 0.46, 0.22, "the source after clear()", 9.5, C["muted"], italic=True)
    grid(s, x + w * 0.54, y + 0.2, w * 0.42, cells_of(ns["source"].getRows()), 3, 2, {}, fs=8.5, rowh=0.24, width_of=lambda c: 1.0, colw0=0.3)
    note(s, x, y + 1.5, w, "titles: %s; the cleared sheet keeps its size (rows, columns): %s" % (ns["target"].sheetTitles, out.splitlines()[-1].split("]] ")[-1]), fs=9)


@need(1.4)
def v_surprises(s, x, y, w, h, ns, out):
    lines = out.splitlines()
    rows = [["Statement", "Result", "Why"], ["a == b for sheets of two spreadsheets", lines[0].split(": ")[1].split(" |")[0], "equal when sheetId is equal; both are 0"],
            ["'Alice' in sheet", lines[1].split(": ")[1], "in searches the coordinates, not the values"], ["sheet['C1'] for an empty cell", lines[2].split(" is ")[1], "an empty string, never None"]]
    table(s, x, y, w, rows, [3.4, 1.2, 4.2], rowh=0.34, mono_cols=(0, 1), cell_fill={(1, 1): C["redLight"], (2, 1): C["redLight"]}, fs=10)
    note(s, x, y + 1.45, w, "ids shown in the run: %s" % lines[0].split("| ")[1], fs=9)


# ------------------------------------------------------------------ part 4
@need(1.5)
def v_forms_emails(s, x, y, w, h, ns, out):
    ans = ns["answers"]
    rows = [[a[0], a[1], a[2]] for a in ans]
    seen, cf = set(), {}
    for i, r in enumerate(rows[1:], 1):
        if r[2] in seen:
            for j in range(3):
                cf[(i, j)] = C["amberLight"]
        seen.add(r[2])
    table(s, x, y, w * 0.66, rows, [2.0, 1.0, 2.4], rowh=0.3, cell_fill=cf, fs=10)
    uniq = eval(out.splitlines()[1])
    chip(s, x + w * 0.7, y, w * 0.3, 0.3, "%d answers" % (len(rows) - 1), "teal", fs=10, mono=False)
    chip(s, x + w * 0.7, y + 0.4, w * 0.3, 0.3, "%d different addresses" % len(uniq), "green", fs=10, mono=False)
    note(s, x + w * 0.7, y + 0.8, w * 0.3, "amber: answered twice", fs=9.5)


@need(1.7)
def v_quota_backoff(s, x, y, w, h, ns, out):
    p = ns["pauses"]
    chart(s, "col", x, y, w * 0.6, max(h, 1.6), ["after try %d" % (i + 1) for i in range(len(p))], [("seconds waited", p)], fs=9, legend=False, gap=45, vmax=50, major=10)
    lines = out.splitlines()
    chip(s, x + w * 0.64, y + 0.1, w * 0.36, 0.3, "%s tries in all" % lines[0].split()[0], "amber", fs=9.5, mono=False)
    chip(s, x + w * 0.64, y + 0.5, w * 0.36, 0.3, "waited %d seconds in total" % sum(p), "teal", fs=9.5, mono=False)
    chip(s, x + w * 0.64, y + 0.9, w * 0.36, 0.3, "then: %s" % lines[0].split()[-1], "red", fs=9.5)
    note(s, x + w * 0.64, y + 1.3, w * 0.36, "seconds shown: the pause before the next try", fs=9)


# ------------------------------------------------------------------ part 5
@need(1.35)
def v_audit(s, x, y, w, h, ns, out):
    acc = ns["accounts"]
    names = list(acc)
    chart(s, "col", x, y, w * 0.6, max(h, 1.6), names, [("balance", [acc[n] for n in names])], fs=10, legend=False, gap=60, vmax=1000, major=250, number_format="#,##0")
    chip(s, x + w * 0.65, y + 0.1, w * 0.35, 0.3, out.splitlines()[-1], "green", fs=10, mono=False)
    chip(s, x + w * 0.65, y + 0.5, w * 0.35, 0.3, "PRE-MINE created %d" % sum(int(r[2]) for r in ns["ledger"] if r[0] == "PRE-MINE"), "teal", fs=10, mono=False)
    note(s, x + w * 0.65, y + 0.9, w * 0.35, "an honest ledger adds up to what was created", h=0.4, fs=9.5)


@need(1.45)
def v_audit_empty(s, x, y, w, h, ns, out):
    rows = ns["sheet"].getRows()
    cells = cells_of(rows)
    fills = {"A3": C["redLight"], "B3": C["redLight"], "C3": C["redLight"]}
    grid(s, x, y, w * 0.45, cells, 3, 3, fills, fs=10, rowh=0.3, width_of=lambda c: 1.2, colw0=0.35)
    chip(s, x + w * 0.5, y, w * 0.5, 0.3, out.splitlines()[0], "plain", fs=10)
    chip(s, x + w * 0.5, y + 0.4, w * 0.5, 0.5, out.splitlines()[1], "red", fs=9.5)
    note(s, x + w * 0.5, y + 1.0, w * 0.5, "red: the empty row that stopped the loop", fs=9.5)


@need(1.45)
def v_add_transaction(s, x, y, w, h, ns, out):
    log = [(m, p) for m, p, q, b in ns["g"].log]
    cnt = collections.Counter(m for m, p in log)
    chart(s, "col", x, y, w * 0.45, max(h, 1.6), ["GET", "POST", "PUT"], [("requests", [cnt.get("GET", 0), cnt.get("POST", 0), cnt.get("PUT", 0)])], fs=10, legend=False, gap=70, vmax=4, major=1)
    rows = [["Request", "Why"], ["GET", "size of the sheet, its values"], ["POST", "batchUpdate: one row more"], ["PUT x 3", "sender, recipient, amount"]]
    table(s, x + w * 0.5, y, w * 0.5, rows, [0.9, 2.6], rowh=0.3, mono_cols=(0,), fs=9.5)
    chip(s, x + w * 0.5, y + 1.3, w * 0.5, 0.3, "new row: " + out.splitlines()[0].split(" | ")[0], "amber", fs=9)


@need(1.6)
def v_lost_update(s, x, y, w, h, ns, out):
    rows = ns["first"].getRows()
    cells = cells_of(rows)
    grid(s, x + w * 0.38, y, w * 0.34, cells, 3, 3, {"A3": C["redLight"]}, fs=10, rowh=0.3, width_of=lambda c: 1.0, colw0=0.35)
    label_shape(s, x, y, w * 0.3, 0.4, "first program\nwrites 'first'", C["tealLight"], C["ink"], size=9.5, line=C["line"])
    label_shape(s, x, y + 0.75, w * 0.3, 0.4, "second program\nwrites 'second'", C["amberLight"], C["ink"], size=9.5, line=C["line"])
    arrow(s, x + w * 0.3, y + 0.2, x + w * 0.38, y + 0.88, C["muted"], 1.4)
    arrow(s, x + w * 0.3, y + 0.95, x + w * 0.38, y + 0.9, C["coral"], 1.8)
    chip(s, x + w * 0.76, y, w * 0.24, 0.3, "both: row 3", "amber", fs=9.5, mono=False)
    chip(s, x + w * 0.76, y + 0.4, w * 0.24, 0.5, "row 3 holds %r" % ns["first"].getRow(3)[0], "red", fs=9.5)
    note(s, x + w * 0.76, y + 1.0, w * 0.24, "'first' is gone; no error", fs=9)


@need(1.3)
def v_bean_count(s, x, y, w, h, ns, out):
    rows = ns["rows"]
    wrong = {int(re.findall(r"row (\d+)", l)[0]) for l in out.splitlines()}
    tab = [["Row", "Quantity", "Price", "Total typed", "Quantity x price", "Check"]]
    cf = {}
    for n, (q, p, t) in enumerate(rows[1:], 2):
        ok = n not in wrong
        tab.append([str(n), q, p, t, str(int(q) * int(p)), "ok" if ok else "wrong"])
        if not ok:
            for j in range(6):
                cf[(len(tab) - 1, j)] = C["redLight"]
    table(s, x, y, w * 0.72, tab, [0.6, 1.0, 0.9, 1.2, 1.5, 0.9], rowh=min(0.27, h / len(tab)), cell_fill=cf, fs=10, align_cols={j: PP_ALIGN.CENTER for j in range(6)})
    note(s, x + w * 0.75, y, w * 0.25, "red: %d of %d totals are wrong" % (len(wrong), len(rows) - 1), h=0.5, fs=10)


VISUALS = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("v_") and callable(v)}

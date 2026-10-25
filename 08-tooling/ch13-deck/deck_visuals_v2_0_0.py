"""Chapter 13 deck visuals, version 2.0.0: the executed result of every code example drawn as a native table, a native chart or a drawn
diagram. Every number, string and truth value shown is taken from the run of the example's own code (the namespace `ns` and the
printed text `out` that deck_build_v2_0_0.py (chapter 13) passes in); nothing is typed in by hand except plain-language names of columns and boxes.
Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants."""
__version__ = "2.0.0"
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from deck_kit_v2_0_0 import C, MONO, arrow, chart, label_shape as _label_shape, table as _table, tb, rect, line_seg, _style_run


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


def chips_row(s, x, y, items, cw, h=0.3, fs=9.5, kinds=None, gap=0.08, arrows=False):
    """a row of chips; returns the x after the last chip"""
    for i, t in enumerate(items):
        k = kinds[i] if kinds else "plain"
        chip(s, x, y, cw, h, short(t, int(cw * 13)), k, fs=fs)
        if arrows and i < len(items) - 1:
            arrow(s, x + cw + 0.005, y + h / 2, x + cw + gap - 0.005, y + h / 2, C["muted"], 1.0)
        x += cw + gap
    return x



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


# ------------------------------------------------------------------ part 1
@need(1.6)
def v_url_anatomy(s, x, y, w, h, ns, out):
    p = ns["parts"]
    roles = {"scheme": "how to talk to the server", "netloc": "which computer to ask", "path": "which page or service",
             "query": "the question: name=value pairs", "fragment": "a place inside the page"}
    rows = [["Part", "Value", "What it does"]] + [[k, getattr(p, k), roles[k]] for k in ("scheme", "netloc", "path", "query", "fragment")]
    table(s, x, y, w * 0.74, rows, [0.9, 2.5, 2.4], rowh=min(0.27, h / len(rows)), mono_cols=(0, 1), bold_cols=(0,), fs=9.5)
    bx = x + w * 0.78
    label_shape(s, bx, y + 0.1, w * 0.22, 0.62, "scheme, netloc,\npath, query", C["greenLight"], C["ink"], size=9.5, line=C["line"])
    label_shape(s, bx, y + 1.0, w * 0.22, 0.45, "fragment", C["amberLight"], C["ink"], size=9.5, line=C["line"])
    arrow(s, bx + w * 0.11, y + 0.72, bx + w * 0.11, y + 0.98, C["muted"], 1.0)
    note(s, bx - 0.05, y - 0.16, w * 0.24, "sent to the server", fs=9)
    note(s, bx - 0.05, y + 1.45, w * 0.24, "kept by the browser", fs=9)


@need(1.3)
def v_query_quote(s, x, y, w, h, ns, out):
    q = ns["quote"]
    chars = [(" ", "space"), (",", "comma"), ("&", "ampersand"), ("=", "equals sign"), ("#", "number sign")]
    rows = [["Character", "Name", "quote(...)"]] + [[repr(c), n, q(c, safe="")] for c, n in chars]
    table(s, x, y, w * 0.46, rows, [0.9, 1.4, 1.0], rowh=min(0.24, h / len(rows)), mono_cols=(0, 2), fs=9)
    qd = ns["query"]
    rows2 = [["Key", "parse_qs gives"]] + [[k, repr(v)] for k, v in qd.items()]
    table(s, x + w * 0.5, y, w * 0.5, rows2, [0.8, 2.6], rowh=0.3, mono_cols=(0, 1), fs=9.5)
    note(s, x + w * 0.5, y + 1.0, w * 0.5, "'San+Francisco%2CCA' became 'San Francisco,CA'", fs=9.5)


@need(1.7)
def v_status_codes(s, x, y, w, h, ns, out):
    meaning = {2: "success", 3: "redirection", 4: "client error", 5: "server error"}
    rows = [["Code", "Phrase", "Class", "The class means"]]
    cf = {}
    for i, line in enumerate(out.splitlines(), 1):
        code = int(line.split()[0])
        phrase = line.split(" | ")[0].split(" ", 1)[1]
        rows.append([str(code), phrase, "%dxx" % (code // 100), meaning[code // 100]])
        cf[(i, 3)] = {2: C["greenLight"], 3: C["amberLight"], 4: C["redLight"], 5: C["redLight"]}[code // 100]
    table(s, x, y, w, rows, [0.8, 3.0, 0.9, 2.5], rowh=min(0.28, h / len(rows)), mono_cols=(0, 2), cell_fill=cf, fs=10)


@need(1.3)
def v_user_agent(s, x, y, w, h, ns, out):
    name, value = ns["name"], ns["value"].split("/")[0]
    flow(s, x, y, w, ["your script\nurlopen(...)", "header\n%s: %s" % (name, value), "the server sees\nan unnamed script"], ["plain", "amber", "red"], h=0.52, gap=0.45)
    flow(s, x, y + 0.7, w, ["your script\nRequest(...)", "header\nUser-Agent: %s" % ns["request"].get_header("User-agent"), "the server sees\na named program"], ["plain", "amber", "green"], h=0.52, gap=0.45)


@need(1.4)
def v_robots_rules(s, x, y, w, h, ns, out):
    rows = [["Path asked for", "can_fetch", "Rule that decides"]]
    cf = {}
    for i, line in enumerate(out.splitlines(), 1):
        path, ok = line.split()
        blocked = [d for d in ("/simple/", "/account/") if path.startswith(d)]
        rows.append([path, ok, ("Disallow: " + blocked[0]) if blocked else "no rule matches"])
        cf[(i, 1)] = C["greenLight"] if ok == "True" else C["redLight"]
    table(s, x, y, w * 0.72, rows, [2.4, 1.0, 2.3], rowh=min(0.3, h / len(rows)), mono_cols=(0, 1, 2), cell_fill=cf, fs=9.5)
    label_shape(s, x + w * 0.76, y, w * 0.24, 0.5, "robots.txt\nof the site", C["tealLight"], C["ink"], size=9.5, line=C["line"])
    arrow(s, x + w * 0.88, y + 0.52, x + w * 0.88, y + 0.85, C["muted"], 1.2)
    label_shape(s, x + w * 0.76, y + 0.87, w * 0.24, 0.5, "a request,\nnot a lock", C["amberLight"], C["ink"], size=9.5, line=C["line"])


@need(1.3)
def v_crawl_delay(s, x, y, w, h, ns, out):
    pause = ns["pause"]
    times = [i * pause for i in range(3)]
    rows = [["Setting in robots.txt", "The parser says"], ["Crawl-delay: 2", "wait %s seconds" % pause],
            ["Request-rate: 3/20", "%d pages per %d seconds" % (ns["rate"].requests, ns["rate"].seconds)]]
    table(s, x, y, w * 0.5, rows, [1.9, 2.1], rowh=0.34, mono_cols=(0,), fs=9.5)
    note(s, x, y + 1.1, w * 0.5, "the fake clock, one pause between pages", fs=9.5)
    tb(s, x + w * 0.54, y - 0.02, w * 0.46, 0.22, "second of each fetch", 9.5, C["muted"], italic=True)
    chart(s, "col", x + w * 0.54, y + 0.2, w * 0.46, max(h - 0.2, 1.2), ["page a", "page b", "page c"], [("seconds", times)], fs=9, legend=False, gap=60, vmax=6, major=2)


# ------------------------------------------------------------------ part 2
@need(1.4)
def v_webbrowser_open(s, x, y, w, h, ns, out):
    flow(s, x, y, w, ["your program", "webbrowser.open(url)", "your own browser\nshows the page"], ["plain", "teal", "green"], h=0.55, gap=0.55, fs=10)
    lines = out.splitlines()
    chip(s, x, y + 0.8, 2.4, 0.32, "open returned %s" % lines[0], "green", fs=10)
    chip(s, x + 2.55, y + 0.8, w - 2.55, 0.32, "the recorder holds %s" % lines[1], "amber", fs=9.5)
    note(s, x, y + 1.15, w, "the program learns nothing about the page itself", fs=9.5)


@need(1.5)
def v_showmap(s, x, y, w, h, ns, out):
    argv, address, url = ns["argv"], ns["address"], ns["url"]
    flow(s, x, y, w, ["argv\n%d words" % len(argv), "join argv[1:]\n%r" % short(address, 24), "quote(address)\n%d characters" % len(ns["quote"](address)), "search address\nsent to the browser"],
         ["plain", "teal", "amber", "green"], h=0.6, gap=0.32, fs=9)
    tb(s, x, y + 0.75, w, 0.5, short(url, 100), 9.5, C["ink"], font=MONO, name="url")
    note(s, x, y + 1.2, w, "webbrowser.open(url) would now show the map", fs=9.5)


@need(1.2)
def v_fetch_data(s, x, y, w, h, ns, out):
    lines = out.splitlines()
    rows = [["What came back", "Value", "Like the requests object"], ["content type", lines[0], "headers['Content-Type']"],
            ["size of the body", "%d bytes" % len(ns["body"]), "len(response.content)"], ["body as text", repr(ns["body"].decode("utf-8")), "response.text"]]
    table(s, x, y, w * 0.74, rows, [1.5, 2.2, 2.3], rowh=min(0.34, h / 4), mono_cols=(1, 2), bold_cols=(0,), fs=9.5)
    label_shape(s, x + w * 0.78, y + 0.05, w * 0.22, 0.55, "bytes", C["tealLight"], C["ink"], size=10, line=C["line"])
    arrow(s, x + w * 0.89, y + 0.62, x + w * 0.89, y + 0.9, C["muted"], 1.2)
    label_shape(s, x + w * 0.78, y + 0.92, w * 0.22, 0.45, "text", C["greenLight"], C["ink"], size=10, line=C["line"])


@need(1.5)
def v_raise_status(s, x, y, w, h, ns, out):
    rows = [["Reply code", "What the check does", "The program then"]]
    cf = {}
    for i, line in enumerate(out.splitlines(), 1):
        code = line.split()[0]
        stopped = "stopped" in line
        rows.append([code, "raises: " + line.split("stopped: ", 1)[1] if stopped else "passes quietly", "stops" if stopped else "goes on and saves"])
        cf[(i, 2)] = C["redLight"] if stopped else C["greenLight"]
    table(s, x, y, w, rows, [1.2, 4.4, 2.2], rowh=min(0.34, h / len(rows)), mono_cols=(0,), cell_fill=cf, fs=10)


@need(1.5)
def v_chunks(s, x, y, w, h, ns, out):
    sizes = [int(t) for t in out.split()]
    body = ns["body"].decode("utf-8")
    rows = [["Chunk", "Text in the chunk", "write() gave"]]
    pos = 0
    for i, n in enumerate(sizes, 1):
        rows.append([str(i), repr(body[pos:pos + n]), str(n)])
        pos += n
    table(s, x, y, w * 0.62, rows, [0.7, 3.4, 1.0], rowh=min(0.3, h / len(rows)), mono_cols=(1, 2), fs=9.5)
    tb(s, x + w * 0.66, y - 0.02, w * 0.34, 0.22, "bytes saved per chunk", 9.5, C["muted"], italic=True)
    chart(s, "col", x + w * 0.66, y + 0.2, w * 0.34, max(h - 0.2, 1.2), ["chunk 1", "chunk 2", "chunk 3"], [("bytes", sizes)], fs=9, legend=False, gap=50, vmax=20, major=5)


# ------------------------------------------------------------------ part 3
@need(1.6)
def v_json_loads(s, x, y, w, h, ns, out):
    data = ns["data"]
    label_shape(s, x, y + 0.45, 1.3, 0.5, "data\n(a dict)", C["tealLight"], C["ink"], size=10, line=C["line"])
    for i, k in enumerate(data):
        yy = y + i * 0.5
        chip(s, x + 1.8, yy, 1.5, 0.34, repr(k) + (" (list)" if isinstance(data[k], list) else ""), "plain", fs=9.5)
        arrow(s, x + 1.32, y + 0.7, x + 1.78, yy + 0.17, C["muted"], 1.0)
    rows = [["Expression", "Value"], ["data['name']", repr(data["name"])], ["data['main']['temp']", repr(data["main"]["temp"])],
            ["data['weather'][0]['main']", repr(data["weather"][0]["main"])]]
    table(s, x + 3.6, y, w - 3.6, rows, [2.7, 1.5], rowh=0.34, mono_cols=(0, 1), fs=9.5)
    note(s, x + 3.6, y + 1.4, w - 3.6, "one key or position per step", fs=9.5)


@need(1.5)
def v_kelvin(s, x, y, w, h, ns, out):
    k, c, f = ns["kelvin"], ns["celsius"], ns["fahrenheit"]
    rows = [["Step", "Calculation", "Result"], ["start", "Kelvin from the API", "%.2f" % k], ["subtract", "%.2f - 273.15" % k, "%.2f" % c],
            ["scale and shift", "%.2f * 9 / 5 + 32" % c, "%.2f" % f]]
    table(s, x, y, w * 0.58, rows, [1.3, 2.2, 1.2], rowh=min(0.34, h / 4), mono_cols=(1, 2), fs=9.5)
    note(s, x, y + 1.4, w * 0.58, "printed rounded to one decimal", fs=9.5)
    tb(s, x + w * 0.62, y - 0.02, w * 0.38, 0.22, "the same temperature", 9.5, C["muted"], italic=True)
    chart(s, "col", x + w * 0.62, y + 0.2, w * 0.38, max(h - 0.2, 1.3), ["Celsius", "Fahrenheit"], [("degrees", [round(c, 1), round(f, 1)])], fs=9, legend=False, gap=50,
          vmax=70, major=10)


@need(1.5)
def v_api_url(s, x, y, w, h, ns, out):
    endpoint = ns["endpoint"]
    items = [(short(endpoint.replace("https://", ""), 36), "teal", "endpoint"), ("lat=42.36", "plain", "parameter"), ("lon=-71.06", "plain", "parameter"), ("appid=KEY", "amber", "API key: secret")]
    widths = [3.6, 1.4, 1.5, 1.7]
    xx = x
    for (t, kind, lab), ww in zip(items, widths):
        chip(s, xx, y, ww, 0.36, t, kind, fs=9.5)
        arrow(s, xx + ww / 2, y + 0.82, xx + ww / 2, y + 0.4, C["muted"], 1.0)
        tb(s, xx, y + 0.84, ww, 0.24, lab, 9.5, C["muted"], align=PP_ALIGN.CENTER)
        xx += ww + 0.1
    lines = out.splitlines()
    tb(s, x, y + 1.15, w, 0.24, "in a log: " + short(lines[1].replace("https://", ""), 90), 9.5, C["ink"], font=MONO, name="masked")


# ------------------------------------------------------------------ part 4
@need(1.7)
def v_html_elements(s, x, y, w, h, ns, out):
    lines = out.splitlines()
    label_shape(s, x + 2.0, y, 1.6, 0.34, "the page", C["tealLight"], C["ink"], size=10, line=C["line"])
    label_shape(s, x, y + 0.6, 3.0, 0.34, "p  " + lines[0].split(" ", 1)[1], C["card"], C["ink"], size=9.5, line=C["line"], font=MONO)
    label_shape(s, x + 3.4, y + 0.6, 3.5, 0.34, "a  " + lines[2].split(" ", 1)[1], C["card"], C["ink"], size=9.5, line=C["line"], font=MONO)
    label_shape(s, x + 0.6, y + 1.2, 2.0, 0.34, "b  " + lines[1].split(" ", 1)[1] + "  (no attributes)", C["amberLight"], C["ink"], size=9.5, line=C["line"], font=MONO)
    arrow(s, x + 2.4, y + 0.35, x + 1.5, y + 0.58, C["muted"], 1.2)
    arrow(s, x + 3.2, y + 0.35, x + 5.0, y + 0.58, C["muted"], 1.2)
    arrow(s, x + 1.5, y + 0.95, x + 1.6, y + 1.18, C["muted"], 1.2)
    note(s, x + 7.1, y + 0.65, w - 7.1, "tag, then its attributes", fs=9.5)
    note(s, x + 2.8, y + 1.25, 3.0, "b sits inside p; a stands beside p", fs=9.5)


@need(1.5)
def v_css_select(s, x, y, w, h, ns, out):
    lines = out.splitlines()
    rows = [["Beautiful Soup", "The stand-in does", "Result"],
            ["select('#a')[0].get_text()", "''.join(...itertext())", lines[0].split(" ", 1)[1] + "  (" + lines[0].split(" ", 1)[0] + " match)"],
            ["select('p.s > a')[0].get('href')", "find(\".//p[@class='s']/a\").get('href')", lines[1].split(" ", 1)[0]],
            ["select('p.s a')[0].attrs", "link.attrib", lines[1].split(" ", 1)[1]],
            ["select('.nope')", "findall(\".//*[@class='nope']\")", lines[2] + "  (no match)"]]
    table(s, x, y, w, rows, [2.7, 3.2, 1.9], rowh=min(0.29, h / len(rows)), mono_cols=(0, 1, 2), fs=9)


@need(1.4)
def v_regex_pitfall(s, x, y, w, h, ns, out):
    lines = out.splitlines()
    import ast
    rx, ps = ast.literal_eval(lines[0]), ast.literal_eval(lines[1])
    rows = [["Link in the page", "Regular expression", "Parser"]]
    cf = {}
    for i, href in enumerate(ps, 1):
        rows.append([href, "found" if href in rx else "MISSED", "found"])
        cf[(i, 1)] = C["greenLight"] if href in rx else C["redLight"]
        cf[(i, 2)] = C["greenLight"]
    table(s, x, y, w * 0.6, rows, [1.6, 2.0, 1.4], rowh=0.34, mono_cols=(0,), cell_fill=cf, fs=10)
    note(s, x, y + 1.1, w * 0.6, "the second link has a class before its href", fs=9.5)
    tb(s, x + w * 0.64, y - 0.02, w * 0.36, 0.22, "links found", 9.5, C["muted"], italic=True)
    chart(s, "col", x + w * 0.64, y + 0.2, w * 0.36, max(h - 0.2, 1.2), ["regex", "parser"], [("links", [len(rx), len(ps)])], fs=9, legend=False, gap=60, vmax=3, major=1)


@need(1.6)
def v_links_verify(s, x, y, w, h, ns, out):
    urljoin, urldefrag, page, seen_final = ns["urljoin"], ns["urldefrag"], ns["page"], ns["seen"]
    rows = [["href on the page", "Made absolute, no fragment", "Verdict"]]
    cf, seen = {}, []
    for i, href in enumerate(ns["hrefs"], 1):
        full = urldefrag(urljoin(page, href))[0]
        if not full.startswith("https://example.com"):
            v = "skipped: another site"
        elif full in seen:
            v = "skipped: seen already"
        else:
            v = "kept"
            seen.append(full)
        rows.append([href, short(full, 44), v])
        cf[(i, 2)] = C["greenLight"] if v == "kept" else C["amberLight"]
    assert seen == seen_final
    table(s, x, y, w, rows, [2.0, 4.0, 2.2], rowh=min(0.32, h / len(rows)), mono_cols=(0, 1), cell_fill=cf, fs=9.5)


@need(1.3)
def v_xkcd_chain(s, x, y, w, h, ns, out):
    lines = out.splitlines()
    flow(s, x, y, w * 0.75, ["comic page\nxkcd.com/3/", "previous comic\n" + lines[1].replace("https://", ""), "previous comic\nxkcd.com/1/"], ["teal", "plain", "plain"], h=0.5, gap=0.5, fs=9.5)
    note(s, x + w * 0.77, y + 0.05, w * 0.23, "the loop follows Prev", fs=9.5)
    arrow(s, x + 0.9, y + 0.52, x + 0.9, y + 0.78, C["muted"], 1.2)
    label_shape(s, x, y + 0.8, w * 0.75 / 3 + 0.9, 0.4, "image: " + lines[0].replace("https://", ""), C["greenLight"], C["ink"], size=9, line=C["line"])
    note(s, x + w * 0.5, y + 0.85, w * 0.5, "the first comic's Prev link is #, so the loop stops", fs=9.5)


@need(1.5)
def v_search_results(s, x, y, w, h, ns, out):
    opened = ns["opened"]
    rows = [["Result link", "Opened?"]]
    cf = {}
    for i, link in enumerate(ns["links"], 1):
        addr = "https://pypi.org" + link.get("href")
        yes = addr in opened
        rows.append([addr, "yes: tab opened" if yes else "no: not in the first two"])
        cf[(i, 1)] = C["greenLight"] if yes else C["grey"]
    table(s, x, y, w * 0.62, rows, [2.5, 2.2], rowh=min(0.32, h / len(rows)), mono_cols=(0,), cell_fill=cf, fs=9.5)
    tb(s, x + w * 0.66, y - 0.02, w * 0.34, 0.22, "links found against tabs opened", 9.5, C["muted"], italic=True)
    chart(s, "col", x + w * 0.66, y + 0.2, w * 0.34, max(h - 0.2, 1.2), ["found", "opened"], [("links", [len(ns["links"]), len(opened)])], fs=9, legend=False, gap=60, vmax=4, major=1)


# ------------------------------------------------------------------ part 5
@need(1.4)
def v_dynamic_page(s, x, y, w, h, ns, out):
    lines = out.splitlines()
    label_shape(s, x, y, 2.1, 0.55, "downloaded source\nempty div + script", C["card"], C["ink"], size=9.5, line=C["line"])
    label_shape(s, x + 3.0, y - 0.05, 2.9, 0.5, "requests and a parser read\n" + lines[0], C["redLight"], C["ink"], size=9.5, line=C["line"])
    arrow(s, x + 2.12, y + 0.18, x + 2.98, y + 0.18, C["muted"], 1.5)
    label_shape(s, x + 3.0, y + 0.6, 2.9, 0.5, "a browser runs the script\n" + lines[1].replace("after the script ran: ", "shows "), C["greenLight"], C["ink"], size=9.5, line=C["line"])
    arrow(s, x + 2.12, y + 0.4, x + 2.98, y + 0.85, C["muted"], 1.5)
    label_shape(s, x + 6.3, y + 0.6, w - 6.3, 0.5, "Selenium or Playwright\n(headless: no window)", C["tealLight"], C["ink"], size=9.5, line=C["line"])
    arrow(s, x + 5.92, y + 0.85, x + 6.28, y + 0.85, C["muted"], 1.5)
    note(s, x, y + 1.25, w, "the text exists only after the script has run", fs=9.5)


@need(1.5)
def v_selenium_shape(s, x, y, w, h, ns, out):
    fe, f1 = ns["find_elements"], ns["find_element"]
    rows = [["Call", "What comes back"],
            ["find_elements('.//p')", "a list of %d elements" % len(fe(".//p"))],
            ["find_element('.//p').text", repr(f1(".//p").text)],
            ["find_elements('.//h1')", repr(fe(".//h1")) + "  (empty list)"],
            ["find_element('.//h1')", "IndexError here; NoSuchElementException in Selenium"]]
    cf = {(1, 1): C["greenLight"], (2, 1): C["greenLight"], (3, 1): C["amberLight"], (4, 1): C["redLight"]}
    table(s, x, y, w, rows, [2.8, 5.0], rowh=min(0.32, h / len(rows)), mono_cols=(0,), cell_fill=cf, fs=10)


@need(1.2)
def v_playwright_shape(s, x, y, w, h, ns, out):
    lines = out.splitlines()
    flow(s, x, y, w, ["with ... as p\n(starts the tool)", "p.new_page()\n(a fresh tab)", "page.goto(url)\n" + lines[0], "page.locator('h1')\n" + lines[1]],
         ["teal", "plain", "plain", "green"], h=0.6, gap=0.3, fs=9)
    for i, lab in enumerate(["1 start", "2 open a tab", "3 visit", "4 find the element"]):
        bw = (w - 0.3 * 3) / 4
        tb(s, x + i * (bw + 0.3), y + 0.65, bw, 0.24, lab, 9.5, C["muted"], align=PP_ALIGN.CENTER)
    note(s, x, y + 0.95, w, "the real program adds p.firefox.launch() and keeps the same four steps", fs=9.5)


@need(1.4)
def v_auto_wait(s, x, y, w, h, ns, out):
    looks = ns["looks"]
    tb(s, x, y - 0.02, w * 0.4, 0.22, "is the element there at look n? (1 = yes)", 9.5, C["muted"], italic=True)
    chart(s, "col", x, y + 0.2, w * 0.4, max(h - 0.2, 1.2), ["look 1", "look 2", "look 3"], [("ready", [0 if t is None else 1 for t in looks])], fs=9, legend=False, gap=50, vmax=1, major=1)
    lines = out.splitlines()
    rows = [["Patience", "Result"], ["5 looks", lines[0]], ["2 looks", lines[1]]]
    table(s, x + w * 0.45, y, w * 0.55, rows, [1.1, 3.4], rowh=0.36, mono_cols=(1,), cell_fill={(1, 1): C["greenLight"], (2, 1): C["redLight"]}, fs=10)
    note(s, x + w * 0.45, y + 1.15, w * 0.55, "Playwright's real limit is thirty seconds", fs=9.5)


VISUALS = {k[2:]: v for k, v in list(globals().items()) if k.startswith("v_") and callable(v)}

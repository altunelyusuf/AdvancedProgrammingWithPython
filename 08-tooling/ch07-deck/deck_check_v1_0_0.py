#!/usr/bin/env python3
"""Chapter 7 deck check: everything the finished .pptx shows as a result is produced again, now, and compared.
  1. Every '>>>' row on a slide is re-run under the interpreter running this check, in one namespace per slide; the value
     (nothing for None, repr otherwise, 'Type: message' for an error) must equal the line shown under it, and the row must
     be one the recording (examples_out) holds with that same result.
  2. Every native chart's categories and values must equal a re-execution of the recorded chart expression, and every
     recorded chart must be on some slide.
  3. Every table's cells must equal a re-execution of the recorded table expression, and every recorded table must be on
     some slide.
  4. The interpreter must be the one the recording was made under.
Usage: deck_check_v1_0_0.py <deck.pptx> <examples_out.json> [python-version-label]   Exit 0 when nothing mismatches."""
__version__ = "1.0.0"
import json
import platform
import re
import sys
import zipfile
from xml.dom import minidom


def slides(path):
    z = zipfile.ZipFile(path)
    out = []
    names = [n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)]
    for n in sorted(names, key=lambda n: int(re.findall(r"\d+", n)[0])):
        d = minidom.parseString(z.read(n))
        paras = []
        for p in d.getElementsByTagName("a:p"):
            paras.append("".join(t.firstChild.nodeValue if t.firstChild else "" for t in p.getElementsByTagName("a:t")))
        out.append((n, paras))
    return out


def run_row(src, ns):
    try:
        try:
            v = eval(src, ns)
            return "" if v is None else repr(v)
        except SyntaxError:
            exec(src, ns)
            return ""
    except Exception as e:
        return "%s: %s" % (type(e).__name__, e)


def data(setup, expr):
    ns = {}
    exec(setup, ns)
    return eval(expr, ns)


def main(deck, rec_path):
    rec = json.load(open(rec_path))
    bad = []
    if platform.python_version() != rec["_python"]:
        bad.append(("interpreter", "running %s, recording made under %s" % (platform.python_version(), rec["_python"])))
    recorded = {(s, o or "") for k, v in rec.items() if not k.startswith("_") for s, o in v}
    n_rows = 0
    for name, paras in slides(deck):
        ns, i = {}, 0
        while i < len(paras):
            p = paras[i]
            if p.startswith(">>> "):
                src = p[4:]
                nxt = paras[i + 1] if i + 1 < len(paras) else ""
                shown = "" if nxt.startswith(">>> ") or i + 1 >= len(paras) else nxt
                got = run_row(src, ns)
                n_rows += 1
                if got != shown:
                    bad.append((name, src, "shown " + repr(shown), "re-run " + repr(got)))
                if (src, shown) not in recorded:
                    bad.append((name, src, "not a recorded row with this result"))
                i += 2 if shown else 1
            else:
                i += 1
    charts, tables = [], []
    z = zipfile.ZipFile(deck)
    for nm in sorted(n for n in z.namelist() if re.match(r"ppt/charts/chart\d+\.xml$", n)):
        d = minidom.parseString(z.read(nm))
        ser = d.getElementsByTagName("c:ser")[0]
        cat = ser.getElementsByTagName("c:cat")[0]
        val = ser.getElementsByTagName("c:val")[0]
        pts = lambda node: [t.firstChild.nodeValue if t.firstChild else ""
                            for t in node.getElementsByTagName("c:pt") for t in t.getElementsByTagName("c:v")]
        charts.append((nm, pts(cat), [float(v) for v in pts(val)]))
    for n in sorted([n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)], key=lambda n: int(re.findall(r"\d+", n)[0])):
        d = minidom.parseString(z.read(n))
        for tbl in d.getElementsByTagName("a:tbl"):
            rows = []
            for tr in tbl.getElementsByTagName("a:tr"):
                rows.append(["".join(t.firstChild.nodeValue if t.firstChild else "" for t in tc.getElementsByTagName("a:t"))
                             for tc in tr.getElementsByTagName("a:tc")])
            tables.append((n, rows))
    for k, c in rec["_charts"].items():
        want = (data(c["setup"], c["expr"]))
        labels, values = [w[0] for w in want], [float(w[1]) for w in want]
        if not any(cl == labels and cv == values for _, cl, cv in charts):
            bad.append(("chart", k, "no chart on any slide with the labels and values of a re-run of its expression"))
    for n, cl, cv in charts:
        if not any(cl == c["labels"] and cv == [float(v) for v in c["values"]] for c in rec["_charts"].values()):
            bad.append(("chart %s" % n, "is not a recorded chart"))
    for k, t in rec["_tables"].items():
        want = data(t["setup"], t["expr"])
        if not any(tr == want for _, tr in tables):
            bad.append(("table", k, "no table on any slide equals a re-run of its expression"))
    for n, tr in tables:
        if not any(tr == t["rows"] for t in rec["_tables"].values()):
            bad.append(("table in %s" % n, "is not a recorded table"))
    print("deck_check %s under Python %s: %d console rows re-run, %d chart(s) and %d table(s) re-computed; %d mismatch(es)"
          % (__version__, platform.python_version(), n_rows, len(charts), len(tables), len(bad)))
    for b in bad:
        print("  REFUSED", b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))

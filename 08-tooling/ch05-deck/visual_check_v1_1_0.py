"""Visual check for the chapter 5 deck: every shape named 'v:<visual>:...' carries a value of an executed visual specification. The specification is
regenerated NOW by running visuals_make under the interpreter given, so a slide that shows a value the code no longer produces - a trace cell, a
debugger stop (line, variables, call stack, printed text), a logging-matrix cell, an unwinding frame, a traceback - is refused. Also required: each visual a
slide draws is drawn COMPLETELY (every trace row, every debugger field of a stop it shows, every cell of the logging matrix, every frame and the handler),
and the program a trace, a debugger record or an unwinding record was made from is one of the programs the deck's own program check re-runs.
1.1.0: adds the kinds debugger, levels, unwind and traceback to the kind trace of version 1.0.0.
Usage: visual_check_v1_1_0.py <deck.pptx> <visuals_make.py> <examples_out.json> <python>     Exits 1 on any mismatch."""
__version__ = "1.1.0"
import html, json, os, re, subprocess, sys, tempfile, zipfile
deck, maker, exout, PY = sys.argv[1:5]
tmp = os.path.join(tempfile.mkdtemp(), "v.json")
subprocess.run([PY, maker, tmp], check=True, capture_output=True); V = json.load(open(tmp)); PROGS = {v["code"] for v in json.load(open(exout))["_programs"].values()}
z = zipfile.ZipFile(deck); shapes = {}
for n in z.namelist():
    m = re.match(r"ppt/slides/slide(\d+)\.xml$", n)
    if not m: continue
    x = z.read(n).decode("utf-8")
    for sp in re.finditer(r'<p:sp><p:nvSpPr><p:cNvPr id="\d+" name="([^"]*)"[^>]*>(.*?)</p:sp>', x, flags=re.S):
        name = re.sub(r"\|b\d+$", "", html.unescape(sp.group(1)))
        if name.startswith("v:") and not re.search(r":(box|dot\d*|stopdot)$", name):
            shapes.setdefault((int(m.group(1)), name), []).append("".join(html.unescape(a) for a in re.findall(r"<a:t>([^<]*)</a:t>", sp.group(2))))
ws = lambda t: re.sub(r"\s+", "", t)
bad = []; seen = {}; checked = 0
def want(slide, name, ok):
    global checked; checked += 1
    got = shapes[(slide, name)]
    if not any(ws(g) in {ws(o) for o in ok} for g in got): bad.append((slide, name, got, sorted(ok)))
for (slide, name), texts in sorted(shapes.items()):
    parts = name.split(":"); vid = parts[1]; S_ = V.get(vid)
    if S_ is None: bad.append((slide, name, texts, "no such visual")); continue
    seen.setdefault((slide, vid), set()).add(":".join(parts[2:])); k = S_["kind"]
    if k == "trace":
        if S_["code"] not in PROGS: bad.append((slide, name, "program not re-run by the program check", S_["code"][:40]))
        run, row, col = int(parts[2]), int(parts[3]), parts[4]; r = S_["runs"][run]["rows"][row]
        cand = {"n": {str(r["n"])}, "ev": {"; ".join(r["events"]) or "reached the bottom"}, "out": {r["out"]}}
        if col.startswith("v"): cand[col] = {r["vals"][int(col[1:])]}
        want(slide, name, cand[col])
    elif k == "debugger":
        if "\n".join(S_["lines"]) + "\n" not in PROGS: bad.append((slide, name, "program not re-run by the program check", S_["lines"][0]))
        E = S_["events"][int(parts[2][1:])]; f = parts[3]
        ok = {"line": "stopped at line %d%s" % (E["line"], " (breakpoint)" if E["line"] in S_["breakpoints"] else ""),
              "vars": "; ".join("%s = %s" % (a, b) for a, b in E["vars"]) or "none yet", "stack": " › ".join(E["stack"]), "out": E["out"] or "(nothing printed yet)"}[f]
        want(slide, name, {ok})
    elif k == "levels":
        c = parts[2]
        if c.startswith("h"): want(slide, name, {S_["settings"][int(c[1:])]["label"]})
        elif c.startswith("m"): want(slide, name, {S_["messages"][int(c[1:])]["call"]})
        elif c.startswith("c"):
            ci, ri = map(int, re.match(r"c(\d+)r(\d+)$", c).groups()); want(slide, name, {"shown" if S_["settings"][ci]["shown"][ri] else "hidden"})
        elif c.startswith("o"): want(slide, name, {"".join(S_["settings"][int(c[1:])]["output"])})
    elif k == "unwind":
        c = parts[2]
        if re.match(r"f\d+$", c): f = S_["frames"][int(c[1:])]; want(slide, name, {"%s  ·  line %d  ·  %s" % (f["func"], f["line"], f["text"])})
        elif c == "handler": h = S_["handler"]; want(slide, name, {"%s  ·  line %d  ·  %s" % (h["func"], h["line"], h["text"])})
        elif c == "exc": want(slide, name, {"raise " + S_["exc"]})
        elif c == "tb": want(slide, name, {S_["traceback"]})
    elif k == "traceback":
        want(slide, name, {S_["text"]})
for (slide, vid), got in sorted(seen.items()):
    S_ = V[vid]; miss = set()
    if S_["kind"] == "trace":
        need = {"%d:%d:n" % (run, i) for run in sorted({int(g.split(":")[0]) for g in got}) for i in range(len(S_["runs"][run]["rows"]))}; miss = need - got
    elif S_["kind"] == "debugger":
        for ev in sorted({g.split(":")[0] for g in got if g.startswith("e")}): miss |= {"%s:%s" % (ev, f) for f in ("line", "vars", "stack", "out")} - got
    elif S_["kind"] == "levels":
        if any(re.match(r"c\d+r\d+$", g) for g in got):
            miss = ({"h%d" % c for c in range(len(S_["settings"]))} | {"m%d" % r for r in range(len(S_["messages"]))} | {"c%dr%d" % (c, r) for c in range(len(S_["settings"])) for r in range(len(S_["messages"]))}) - got
    elif S_["kind"] == "unwind":
        if any(g.startswith("f") for g in got): miss = ({"f%d" % i for i in range(len(S_["frames"]))} | {"handler", "exc"}) - got
    if miss: bad.append((slide, vid, "drawn incompletely; missing", sorted(miss)))
print("%d visual values re-checked against the specification regenerated under %s; %d mismatch(es)" % (checked, subprocess.run([PY, "-c", "import platform;print(platform.python_version())"], capture_output=True, text=True).stdout.strip(), len(bad)))
for b in bad: print("  REFUSED", b)
sys.exit(1 if bad else 0)

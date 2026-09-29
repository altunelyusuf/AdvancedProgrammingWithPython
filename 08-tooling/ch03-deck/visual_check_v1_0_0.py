"""Visual check for a deck: every shape named 'v:<visual>:...' carries a value of an executed visual specification. The specification is
regenerated NOW by running visuals_make under the interpreter given, so a slide that shows a value the code no longer produces - a trace
cell, a range value, a pair, an error message, a count - is refused. Also required: each trace or range or pairs visual a slide draws is drawn
COMPLETELY (every row, value and pair present), and the program a trace was recorded from is one of the programs the deck's own program check re-runs.
Usage: visual_check_v1_0_0.py <deck.pptx> <visuals_make.py> <examples_out.json> <python>     Exits 1 on any mismatch."""
__version__ = "1.0.0"
import html, json, os, re, subprocess, sys, tempfile, zipfile
deck, maker, exout, PY = sys.argv[1:5]
tmp = os.path.join(tempfile.mkdtemp(), "v.json")
subprocess.run([PY, maker, tmp], check=True, capture_output=True); V = json.load(open(tmp)); PROGS = {v["code"] for v in json.load(open(exout))["_programs"].values()}
z = zipfile.ZipFile(deck); shapes = {}   # (slide, name) -> text
for n in z.namelist():
    m = re.match(r"ppt/slides/slide(\d+)\.xml$", n)
    if not m: continue
    x = z.read(n).decode("utf-8")
    for sp in re.finditer(r'<p:sp><p:nvSpPr><p:cNvPr id="\d+" name="([^"]*)"[^>]*>(.*?)</p:sp>', x, flags=re.S):
        name = re.sub(r"\|b\d+$", "", sp.group(1))
        if name.startswith("v:") and not re.search(r":(box|dot\d*|stopdot)$", name):
            t = "".join(html.unescape(a) for a in re.findall(r"<a:t>([^<]*)</a:t>", sp.group(2)))
            shapes.setdefault((int(m.group(1)), name), []).append(t)
bad = []; seen = {}; checked = 0
def want(slide, name, ok, why):
    global checked; checked += 1
    got = shapes[(slide, name)]
    if not any(g in ok for g in got): bad.append((slide, name, got, sorted(ok)))
for (slide, name), texts in sorted(shapes.items()):
    parts = name.split(":"); vid = parts[1]; V_ = V.get(vid)
    if V_ is None: bad.append((slide, name, texts, "no such visual")); continue
    seen.setdefault((slide, vid), set()).add(":".join(parts[2:])); k = V_["kind"]
    if k == "trace":
        if V_["code"] not in PROGS: bad.append((slide, name, "program not re-run by the program check", V_["code"][:40]))
        run, row, col = int(parts[2]), int(parts[3]), parts[4]; r = V_["runs"][run]["rows"][row]
        cand = {"n": {str(r["n"]), "pass %d" % r["n"]}, "cond": {"True" if r["cond"] else "False"},
                "ev": {"; ".join(r["events"]) or ("test false: loop ends" if r["cond"] is False else ""), "; ".join(r["events"]) or "reached the bottom"}, "out": {r["out"]}}
        if col.startswith("v"): cand[col] = {V_["watch"][int(col[1:])] + " = " + r["vals"][int(col[1:])], r["vals"][int(col[1:])]}
        want(slide, name, cand[col], "trace")
    elif k == "range":
        c = parts[2]
        if c.startswith("val"): want(slide, name, {str(V_["values"][int(c[3:])])}, "range")
        elif c == "stop": want(slide, name, {"stop %d — never included" % V_["stop"]}, "range")
        elif c == "call": want(slide, name, {"%s → %d value%s" % (V_["call"], len(V_["values"]), "" if len(V_["values"]) == 1 else "s")}, "range")
    elif k == "pairs":
        c = parts[2]; top = V_["right"] if V_.get("swap") else V_["left"]; bot = V_["left"] if V_.get("swap") else V_["right"]
        if c.startswith("top"): want(slide, name, {str(top[int(c[3:])])}, "pairs")
        elif c.startswith("bot"): want(slide, name, {str(bot[int(c[3:])])}, "pairs")
        elif c.startswith("pair"): want(slide, name, {V_["reprs"][int(c[4:])]}, "pairs")
        elif c == "error": want(slide, name, {V_["error"]}, "pairs")
        elif c == "call": want(slide, name, {V_["call"]}, "pairs")
    elif k == "names":
        if parts[2] == "count": want(slide, name, {t for t in texts if str(V_["count"]) + " names" in t}, "names")
        elif parts[2] == "note": want(slide, name, {t for t in texts if ("holds %d names" % V_["count"]) in t}, "names")
# completeness: each drawn visual has every row, value or pair
for (slide, vid), got in sorted(seen.items()):
    S = V[vid]
    if S["kind"] == "range":
        need = {"val%d" % i for i in range(len(S["values"]))} | {"stop", "call"}
    elif S["kind"] == "pairs":
        top = S["right"] if S.get("swap") else S["left"]; bot = S["left"] if S.get("swap") else S["right"]
        need = {"top%d" % i for i in range(len(top))} | {"bot%d" % i for i in range(len(bot))} | {"pair%d" % i for i in range(len(S["pairs"]))} | {"call"} | ({"error"} if S.get("error") else set())
    elif S["kind"] == "trace":
        runs = sorted({int(g.split(":")[0]) for g in got}); need = set()
        for run in runs: need |= {"%d:%d:n" % (run, i) for i in range(len(S["runs"][run]["rows"]))}
    else: continue
    miss = need - got
    if miss: bad.append((slide, vid, "drawn incompletely; missing", sorted(miss)))
print("%d visual values re-checked against the specification regenerated under %s; %d mismatch(es)" % (checked, subprocess.run([PY, "-c", "import platform;print(platform.python_version())"], capture_output=True, text=True).stdout.strip(), len(bad)))
for b in bad: print("  REFUSED", b)
sys.exit(1 if bad else 0)

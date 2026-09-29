"""Visual check for the chapter 6 deck: every text shape named 'v:<visual>:<path>' carries a value of an executed visual specification. The specification is
regenerated NOW by running visuals_make under the interpreter given, so a slide that shows a value the code no longer produces - a list before or after an
operation, a returned value, an index, a name in a reference picture, an object item, a loop pass, a key of a sort, a printed Matrix row, a count of the
histogram - is refused. Also required: each part of a visual a slide draws is drawn COMPLETELY (every text of a lane, of a reference-picture step, of a fact,
of a case of unpacking, of a sort; the whole of a boxes picture, a loop, a mutation trace, a table of passes, a histogram, the Matrix screen), and the source
a trace was made from is the program the deck's own program check re-runs (the mutation trace and the passing-a-list pictures) or the recorded Matrix program.
Usage: visual_check_v1_0_0.py <deck.pptx> <visuals_make.py> <examples_out.json> <python>     Exits 1 on any mismatch."""
__version__ = "1.0.0"
import html, json, os, re, subprocess, sys, tempfile, zipfile
deck, maker, exout, PY = sys.argv[1:5]
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
tmp = os.path.join(tempfile.mkdtemp(), "v.json")
subprocess.run([PY, maker, tmp], check=True, capture_output=True); V = json.load(open(tmp)); PROGS = {v["code"].strip() for v in json.load(open(exout))["_programs"].values()}
import examples_v1_0_0 as EXM
ARROW, ARROW2 = "  →  ", "   →   "

def expected(vid, S):
    """path -> the text the slide must show, for every text of the visual."""
    k = S["kind"]; e = {}
    if k == "classify":
        for i, c in enumerate(S["columns"]):
            e["c%dq" % i] = c["question"]; e["c%dh" % i] = c["head"]
            for j, ch in enumerate(c["chips"]): e["c%dk%d" % (i, j)] = ch["expr"]; e["c%dk%dev" % (i, j)] = ch["evidence"]
    elif k == "boxes":
        n = len(S["list"])
        for i, t in enumerate(S["list"]): e["ix%d" % i] = str(i); e["i%d" % i] = t; e["nx%d" % i] = str(i - n)
        for pi, p in enumerate(S["picks"]): e["p%d" % pi] = p["expr"] + ARROW + p["result"]
        if S.get("error"): e["err"] = S["error"]["expr"] + ARROW + S["error"]["message"]
    elif k == "slices":
        for i, t in enumerate(S["list"]): e["hx%d" % i] = str(i)
        for r, R in enumerate(S["rows"]):
            e["e%dx" % r] = R["expr"]; e["e%dr" % r] = R["result"]; e["e%dp" % r] = R["picked_label"]
            for i, t in enumerate(S["list"]): e["e%dc%d" % (r, i)] = t
    elif k == "lanes":
        for r, L in enumerate(S["lanes"]):
            e["l%dop" % r] = L["op"]; e["l%dcat" % r] = L["cat_label"]; e["l%dret" % r] = L["ret_label"]
            for i, t in enumerate(L["before"]): e["l%db%d" % (r, i)] = t
            for i, t in enumerate(L["after"]): e["l%da%d" % (r, i)] = t
        for i, x in enumerate(S["errors"]): e["e%d" % i] = x["expr"] + ARROW2 + x["message"]
    elif k == "keysort":
        for x, E in enumerate(S["examples"]):
            e["x%dt" % x] = E["title"]; e["x%dexpr" % x] = E["expr"]
            for i, t in enumerate(E["items"]): e["x%din%d" % (x, i)] = t
            for i, t in enumerate(E.get("keys") or []): e["x%dkey%d" % (x, i)] = t
            for i, t in enumerate(E["result"]): e["x%dout%d" % (x, i)] = t
    elif k == "facts":
        for i, f in enumerate(S["facts"]): e["f%dt" % i] = f["label"]; e["f%de" % i] = f["expr"]; e["f%dr" % i] = f["result"]
    elif k == "passes":
        for j, T in enumerate(S["tables"]):
            e["t%dhead" % j] = T["header"]
            for ci, c in enumerate(T["cols"]): e["t%dh%d" % (j, ci)] = c
            for ri, r in enumerate(T["rows"]):
                for ci, c in enumerate(r): e["t%dr%dc%d" % (j, ri, ci)] = c
        e["plabel"] = S["printed_label"]
        for i, l in enumerate(S["printed"]): e["p%d" % i] = l
        e["startexpr"] = S["start"]["expr"]; e["startres"] = S["start"]["result"]
    elif k == "mutation":
        for r, P in enumerate(S["passes"]):
            e["p%dh" % r] = P["head"]; e["p%da" % r] = P["action"]
            for i, t in enumerate(P["before"]): e["p%db%d" % (r, i)] = t
        e["fin"] = S["final_label"]; e["skip"] = S["skip_label"]
    elif k == "unpack":
        for ci, c in enumerate(S["cases"]):
            e["u%dstmt" % ci] = c["stmt"]
            for i, t in enumerate(c["items"]): e["u%di%d" % (ci, i)] = t
            for m, t in enumerate(c["targets"]): e["u%dn%d" % (ci, m)] = t["name"]; e["u%dv%d" % (ci, m)] = t["value"]
        if S.get("error"): e["err"] = S["error"]["expr"] + ARROW + S["error"]["message"]
    elif k == "seqtypes":
        for i, T in enumerate(S["types"]):
            e["s%dname" % i] = T["type"]; e["s%dsample" % i] = T["sample"]; e["s%dmut" % i] = T["mutable_label"]; e["s%dassign" % i] = T["assign"]; e["s%dresult" % i] = T["result"]
    elif k == "hist":
        for i, b in enumerate(S["bars"]): e["h%dl" % i] = b["text"]; e["h%dn" % i] = str(b["count"])
    elif k == "matrix":
        for a, F in enumerate(S["frames"]):
            e["f%dlabel" % a] = F["label"]
            for i, r in enumerate(F["rows"]): e["f%dr%d" % (a, i)] = r
        for a, H in enumerate(S["hazard"]): e["hz%dlabel" % a] = H["label"]; e["hz%dn" % a] = H["spaces_label"]; e["hz%d" % a] = H["row"]
        for ci, c in enumerate(S["life_cols"]): e["life.h%d" % ci] = c
        for ri, r in enumerate(S["life"]):
            for ci, cell in enumerate([str(r["row"]), r["char"], str(r["counter"])]): e["life.r%dc%d" % (ri, ci)] = cell
    elif k == "refgraph":
        for sc, SC in enumerate(S["scenarios"]):
            e["sc%dt" % sc] = SC["title"]
            for st, St in enumerate(SC["steps"]):
                p = "g%d.%d." % (sc, st); e[p + "c"] = St["code"]
                if len(St["scopes"]) > 1:
                    for i, scp in enumerate(St["scopes"]): e[p + "sc%d" % i] = scp["scope"]
                for scp in St["scopes"]:
                    for n, oid in scp["names"]: e[p + "n." + n] = n
                for oid, ob in St["objects"].items():
                    if ob["type"] == "list":
                        for i, it in enumerate(ob["items"]):
                            if not it.get("ref"): e[p + oid + "i%d" % i] = it["v"]
                    else: e[p + oid + "v"] = ob["v"]
    return e

def unit(k, path):
    """the part of a visual that must be drawn whole once any of its texts is drawn."""
    if k == "refgraph":
        m = re.match(r"g\d+\.\d+\.", path); return m.group(0) if m else path
    if k in ("lanes", "unpack", "keysort", "seqtypes", "classify", "slices", "facts"):
        m = re.match(r"(l|u|x|s|c|e|f)\d+", path)
        if m and not (k == "lanes" and path.startswith("e")) and not (k == "unpack" and path == "err"): return m.group(0)
        return path
    return "all"

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
bad = []; seen = {}; checked = 0; EXP = {}
for (slide, name), texts in sorted(shapes.items()):
    parts = name.split(":"); vid = parts[1]; path = ":".join(parts[2:]); S_ = V.get(vid)
    if S_ is None or vid.startswith("_"): bad.append((slide, name, texts, "no such visual")); continue
    if vid not in EXP: EXP[vid] = expected(vid, S_)
    if path not in EXP[vid]: bad.append((slide, name, texts, "no such part of the specification")); continue
    checked += 1; seen.setdefault((slide, vid), set()).add(path)
    if not any(ws(g) == ws(EXP[vid][path]) for g in texts): bad.append((slide, name, texts, EXP[vid][path]))
for (slide, vid), got in sorted(seen.items()):
    k = V[vid]["kind"]; units = {unit(k, p) for p in got}
    if k == "refgraph": units = {u for u in units if u.startswith("g")}       # scenario titles are optional
    miss = sorted(p for p in EXP[vid] if unit(k, p) in units and p not in got)
    if miss: bad.append((slide, vid, "drawn incompletely; missing", miss[:12]))
# the sources of the traces
for vid, S_ in V.items():
    if vid.startswith("_"): continue
    if S_["kind"] == "mutation" or vid == "ListArguments":
        if S_["code"].strip() not in PROGS: bad.append((vid, "the traced program is not one the program check re-runs", S_["code"][:40]))
    if S_["kind"] == "matrix":
        if S_["code"].strip() != EXM.MATRIX.strip(): bad.append((vid, "the Matrix source differs from the recorded program", S_["code"][:40]))
print("%d visual values re-checked against the specification regenerated under %s; %d mismatch(es)" % (checked, subprocess.run([PY, "-c", "import platform;print(platform.python_version())"], capture_output=True, text=True).stdout.strip(), len(bad)))
for b in bad: print("  REFUSED", b)
sys.exit(1 if bad else 0)

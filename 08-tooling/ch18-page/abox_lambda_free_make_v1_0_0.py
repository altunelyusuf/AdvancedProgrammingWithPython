#!/usr/bin/env python3
"""Writes the chapter 18 domain ABox v1.0.3 (maker 1.0.0, adapted from the chapter 20 maker 1.1.0): the same input-output examples as v1.0.2, with every input written as plain, lambda-free code instead of the one-expression
(lambda g: (exec('<prologue>...', g), g['out'])[1])({}) wrapper (the owner's ruling of 2026-11-14: no lambda unless taught; code shown to the learner is readable, indented Python).
How each input is rewritten:
  - the body of the exec string after the fixed prologue (one import line, the ElementTree import, the sample data A, NS and XS, and the helpers rd, wr and err) is kept character for character;
  - the prologue is cut down to the imports, data and helpers the body uses;
  - the final top-level  out = EXPR  becomes the bare expression EXPR, whose value is the example's result (the page-data builder 2.27.0 runs a multi-line input as a program and takes the last expression);
  - err(lambda: X) becomes a small def written just before the statement, def _eN(): return X, and the call becomes err(_eN); the helper err only calls what it is given. No lambda and no eval are left.
Every rewritten input is then run under this interpreter next to the original wrapper and the two results must be equal.
Output: 03-materials/ch18/rdodi/sen0414_ch18_domain_abox_v1_0_3.ttl (only with --write; refuses to overwrite). Usage: <python with the standard library> abox_lambda_free_make_v1_0_0.py [--write]"""
__version__ = "1.0.0"
import ast, os, re, sys
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(R, "03-materials/ch18/rdodi/sen0414_ch18_domain_abox_v1_0_2.ttl"); DST = os.path.join(R, "03-materials/ch18/rdodi/sen0414_ch18_domain_abox_v1_0_3.ttl")
if os.path.exists(DST): sys.exit("refusing to overwrite " + DST)
text = open(SRC, encoding="utf-8").read()
FROMS = []
HELP = {
 "err2": ("def err(f, *a):\n    try: return ('ok', f(*a))\n    except Exception as e: return (type(e).__name__, str(e))\n", {"Exception"}),
 "err": ("def err(f):\n    try: return ('ok', f())\n    except Exception as e: return (type(e).__name__, str(e))\n", {"Exception"}),
 "rd": ("def rd(t, **k): return list(csv.reader(io.StringIO(t, newline=''), **k))\n", {"csv", "io"}),
 "wr": ("def wr(rows, **k):\n    s = io.StringIO(newline=''); csv.writer(s, **k).writerows(rows); return s.getvalue()\n", {"io", "csv"}),
}
def names(src):
    t = ast.parse(src)
    return {n.id for n in ast.walk(t) if isinstance(n, ast.Name)}
_N = [0]
def delambda(src):
    tree = ast.parse(src); b = src.encode("utf-8"); lines = b.split(b"\n"); starts = [0]
    for l in lines: starts.append(starts[-1] + len(l) + 1)
    parent = {}
    for p in ast.walk(tree):
        for c in ast.iter_child_nodes(p): parent[c] = p
    edits = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign) and isinstance(n.value, ast.Lambda) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and not n.value.args.defaults and not n.value.args.vararg and not n.value.args.kwarg:
            lam = n.value; ps = ", ".join(a.arg for a in lam.args.args)
            edits.append((starts[n.lineno-1]+n.col_offset, starts[n.end_lineno-1]+n.end_col_offset, "def " + n.targets[0].id + "(" + ps + "): return " + ast.get_source_segment(src, lam.body), n))
            continue
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "err" and len(n.args) == 1 and isinstance(n.args[0], ast.Lambda) \
                and all(isinstance(d, ast.Name) and d.id == a.arg for d, a in zip(n.args[0].args.defaults, n.args[0].args.args)) and len(n.args[0].args.defaults) == len(n.args[0].args.args):
            lam = n.args[0]; ps = [a.arg for a in lam.args.args]
            st = n
            while not isinstance(st, ast.stmt): st = parent[st]
            _N[0] += 1; name = "_e%d" % _N[0]
            inner = ast.get_source_segment(src, lam.body)
            ind = re.match(rb"[ ]*", lines[st.lineno-1]).group().decode()
            call = "err(" + ", ".join([name] + ps) + ")"
            edits.append((starts[n.lineno-1]+n.col_offset, starts[n.end_lineno-1]+n.end_col_offset, call, n))
            edits.append((starts[st.lineno-1], starts[st.lineno-1], ind + "def " + name + "(" + ", ".join(ps) + "):\n" + ind + "    return " + inner + "\n", n))
    # an err(lambda) inside another err(lambda) is handled by the next pass, once the outer one is a def
    outer = [e for e in edits if e[3] is not None and not any(o[3] is not e[3] and isinstance(o[3], ast.Call) and any(x is e[3] for x in ast.walk(o[3])) for o in edits)]
    outer_nodes = {id(e[3]) for e in outer}
    edits = [e for e in edits if id(e[3]) in outer_nodes]
    for a, z, r, _ in sorted(edits, key=lambda e: (e[0], e[1]), reverse=True): b = b[:a] + r.encode("utf-8") + b[z:]
    out = b.decode("utf-8")
    return delambda(out) if edits else out
def rewrite(wrapped):
    code = ast.parse(wrapped).body[0].value.func.body.value.elts[0].args[0].value
    L = code.split("\n")
    assert L[0].startswith("import io, csv, json, os, re") and L[1] == "import xml.etree.ElementTree as ET" and L[2].startswith("A = ") and L[3].startswith("NS = ") \
        and L[4].startswith("XS = ") and L[5].startswith("def rd(") and L[6].startswith("def wr(") and L[8].startswith("def err(f)"), "unexpected prologue: " + repr(L[:11])[:600]
    mods = [m.strip() for m in L[0][len("import "):].split(",")]
    body = "\n".join(L[11:])
    tree = ast.parse(body); last = tree.body[-1]
    blines = body.split("\n")
    if isinstance(last, ast.Assign) and [getattr(t, "id", None) for t in last.targets] == ["out"]:
        value_src = ast.get_source_segment(body, last.value)
        new_body = "\n".join(blines[:last.lineno - 1]) + ("\n" if last.lineno > 1 else "") + value_src
    else:
        new_body = body.rstrip("\n") + "\nout"  # the result is set inside a try or a with: end on its name
    new_body = delambda(new_body)
    used = names(new_body)
    data = {"A": L[2], "NS": L[3], "XS": L[4]}
    helpers = [h for h in ("rd", "wr", "err") if h in used]
    if "err" in helpers and re.search(r"err\(_e\d+, ", new_body): helpers[helpers.index("err")] = "err2"
    full = set(used)
    for h in helpers: full |= HELP[h][1] | names(HELP[h][0])
    dkeep = [k for k in ("A", "NS", "XS") if k in used]
    if "XS" in dkeep and "NS" not in dkeep: dkeep.insert(0, "NS")
    for k in dkeep: full |= names(data[k])
    keep = []
    for m in mods:
        nm = m.split(" as ")[-1].split(".")[0]
        if nm in full: keep.append(m)
    head = []
    if keep: head.append("import " + ", ".join(keep))
    if "ET" in full: head.append("import xml.etree.ElementTree as ET")
    parts = ["\n".join(head)] if head else []
    for k in dkeep: parts.append(data[k])
    for h in helpers: parts.append(HELP[h][0].rstrip("\n"))
    parts.append(new_body)
    return "\n".join(p for p in parts if p)
def tlit(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")
import rdflib
CH = rdflib.Namespace("http://example.org/sen0414/ch18#")
g = rdflib.Graph(); g.parse(SRC)
code_of = {str(sj).split("#")[-1]: str(o) for sj, p, o in g.triples((None, CH.input, None))}
def run_new(src):
    t = ast.parse(src); last = t.body[-1]
    ns = {"__name__": "__main__"}
    exec(compile(ast.Module(t.body[:-1], []), "<new>", "exec"), ns)
    return eval(compile(ast.Expression(last.value), "<new>", "eval"), ns)
LINE = re.compile(r'^(chx:IO_\w+ a owl:NamedIndividual, rd:IOExample ; rdfs:label ")(.*?)("@en ; chx:input ")(.*?)(" ; chx:output ".*)$')
out_lines, n, same, diff = [], 0, 0, []
only = [a[len("--only="):] for a in sys.argv if a.startswith("--only=")]
for line in text.split("\n"):
    m = LINE.match(line)
    if not m:
        out_lines.append(line); continue
    iri = m.group(1).split()[0][4:]
    if only and iri not in only[0].split(","):
        out_lines.append(line); continue
    old = code_of[iri]
    new = rewrite(old)
    assert "lambda" not in new, iri
    n += 1
    try:
        oldns = {}
        exec(ast.parse(old).body[0].value.func.body.value.elts[0].args[0].value, oldns)
        a = repr(oldns["out"]); b = repr(run_new(new))
    except Exception as e:
        a, b = "ERR", "ERR %s: %s" % (type(e).__name__, e)
    if a == b: same += 1
    else: diff.append((iri, a[:110], b[:110]))
    oldlit = tlit(old)
    label = m.group(2)
    assert label.startswith(oldlit), iri + ": label does not start with the input"
    out_lines.append(m.group(1) + tlit(new) + label[len(oldlit):] + m.group(3) + tlit(new) + m.group(5))
print("rewritten", n, "equal results", same, "different", len(diff))
for d in diff: print(" DIFF", d)
res = "\n".join(out_lines).replace('owl:versionInfo "1.0.2" ; owl:versionIRI <http://example.org/sen0414/ch18/abox/1.0.2>', 'owl:versionInfo "1.0.3" ; owl:versionIRI <http://example.org/sen0414/ch18/abox/1.0.3>').replace("sen0414_ch18_abox_v1_0_2", "sen0414_ch18_abox_v1_0_3")
if "--write" in sys.argv and not diff:
    open(DST, "w", encoding="utf-8").write(res); print("wrote", DST)
elif "--write" in sys.argv:
    print("NOT written: results differ")

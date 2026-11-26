#!/usr/bin/env python3
"""Writes the chapter 21 domain ABox v1.0.3 (maker 1.0.0 over v1.0.2): the same 61 input-output examples, every input written as plain, lambda-free code instead of the one-expression
(lambda g: (exec('<prologue>...', g), g['out'])[1])({}) wrapper (the owner's ruling of 2026-11-14: no lambda unless taught; code shown to the learner is readable, indented Python).
Method (the chapter 19 and 20 makers, adapted to the chapter 21 prologue and to lambdas that are not only err(lambda: X)):
  - the prologue is the text all 61 inputs share (imports, err, wd, grad, sha, the book-zip helpers zipbytes and shp, child); it is cut down to the statements the body uses (names, followed through the helpers);
  - the body after the prologue is kept character for character, fixtures included;
  - a final top-level  out = EXPR  becomes the bare expression EXPR (the page-data builder runs a multi-line input as a program and takes the last expression); otherwise the input ends on the name out;
  - every lambda (with or without parameters, nested ones too) becomes a small def written just before the statement that held it: def _fN(params): return BODY, and the lambda is replaced by _fN. No lambda is left.
Every rewritten input is then run next to the original wrapper under this interpreter and the two results must be equal (a result that raises is compared by exception type and text; the examples that need the book's online zip need the network, which the listing reports).
Output: 03-materials/ch21/rdodi/sen0414_ch21_domain_abox_v1_0_3.ttl (only with --write; refuses to overwrite). Usage: <python with Pillow, matplotlib, rdflib> abox_lambda_free_make_v1_0_0.py [--write]"""
__version__ = "1.0.0"
import ast, os, re, sys
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(R, "03-materials/ch21/rdodi/sen0414_ch21_domain_abox_v1_0_2.ttl"); DST = os.path.join(R, "03-materials/ch21/rdodi/sen0414_ch21_domain_abox_v1_0_3.ttl")
if os.path.exists(DST): sys.exit("refusing to overwrite " + DST)
import rdflib
CH = rdflib.Namespace("http://example.org/sen0414/ch21#")
text = open(SRC, encoding="utf-8").read()
g = rdflib.Graph(); g.parse(SRC)
def unwrap(w): return ast.parse(w).body[0].value.func.body.value.elts[0].args[0].value
code_of = {str(s).split("#")[-1]: str(o) for s, p, o in g.triples((None, CH.input, None))}
CP = os.path.commonprefix([unwrap(w) for w in code_of.values()])
def names_in(node): return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
_N = [0]
def delambda(src):
    tree = ast.parse(src); b = src.encode("utf-8"); lines = b.split(b"\n"); starts = [0]
    for l in lines: starts.append(starts[-1] + len(l) + 1)
    parent = {}
    for p in ast.walk(tree):
        for c in ast.iter_child_nodes(p): parent[c] = p
    lams = [n for n in ast.walk(tree) if isinstance(n, ast.Lambda)]
    # outermost lambdas only (a lambda inside a lambda is handled by the next pass, once the outer one is a def)
    top = [l for l in lams if not any(o is not l and any(x is l for x in ast.walk(o)) for o in lams)]
    if not top: return src
    edits = []
    for lam in top:
        st = lam
        while not isinstance(st, ast.stmt): st = parent[st]
        _N[0] += 1; name = "_f%d" % _N[0]
        assert not (lam.args.defaults or lam.args.vararg or lam.args.kwarg or lam.args.kwonlyargs)
        params = ", ".join(a.arg for a in lam.args.args)
        inner = ast.get_source_segment(src, lam.body)
        ind = re.match(rb"[ ]*", lines[st.lineno - 1]).group().decode()
        edits.append((starts[lam.lineno - 1] + lam.col_offset, starts[lam.end_lineno - 1] + lam.end_col_offset, name))
        edits.append((starts[st.lineno - 1], starts[st.lineno - 1], ind + "def " + name + "(" + params + "):\n" + ind + "    return " + inner + "\n"))
    for a, z, r in sorted(edits, key=lambda e: (e[0], e[1]), reverse=True): b = b[:a] + r.encode("utf-8") + b[z:]
    return delambda(b.decode("utf-8"))
def rewrite(wrapped):
    code = unwrap(wrapped); assert code.startswith(CP)
    ptree = ast.parse(CP); body = code[len(CP):]
    assert body.startswith("\n") or CP.endswith("\n"), "prologue does not end on a line"
    body = body.lstrip("\n")
    tree = ast.parse(body); last = tree.body[-1]; blines = body.split("\n")
    if isinstance(last, ast.Assign) and [getattr(t, "id", None) for t in last.targets] == ["out"]:
        new_body = "\n".join(blines[:last.lineno - 1]) + ("\n" if last.lineno > 1 else "") + ast.get_source_segment(body, last.value)
    else:
        new_body = body.rstrip("\n") + "\nout"
    new_body = delambda(new_body)
    assert "lambda" not in new_body
    # prologue statements: (defined names, used names, source)
    plines = CP.split("\n"); pst = []
    for s in ptree.body:
        src = "\n".join(plines[s.lineno - 1:s.end_lineno])
        if isinstance(s, (ast.Import, ast.ImportFrom)):
            defs = {(a.asname or a.name).split(".")[0] for a in s.names}
        elif isinstance(s, ast.FunctionDef): defs = {s.name}
        elif isinstance(s, ast.Assign): defs = {t.id for t in s.targets if isinstance(t, ast.Name)}
        else: defs = set()
        pst.append((s, defs, names_in(s), src))
    need = names_in(ast.parse(new_body)); keep = set()
    if "plt" in need:   # matplotlib.use('Agg') is what lets the example draw without a screen
        need.add("matplotlib")
        for i, (s, defs, used, src) in enumerate(pst):
            if isinstance(s, ast.Expr) and "matplotlib.use" in src: keep.add(i)
    changed = True
    while changed:
        changed = False
        for i, (s, defs, used, src) in enumerate(pst):
            if i not in keep and defs & need:
                keep.add(i); need |= used; changed = True
    parts = []
    for i, (s, defs, used, src) in enumerate(pst):
        if i not in keep: continue
        if isinstance(s, ast.Import):
            ks = [a for a in s.names if (a.asname or a.name).split(".")[0] in need]
            src = "import " + ", ".join(a.name + (" as " + a.asname if a.asname else "") for a in ks)
        elif isinstance(s, ast.ImportFrom):
            ks = [a for a in s.names if (a.asname or a.name) in need]
            src = "from " + s.module + " import " + ", ".join(a.name + (" as " + a.asname if a.asname else "") for a in ks)
        parts.append(src)
    # expand each helper to plain indented Python (the prologue wrote some on one line with ; and try: on one line)
    head = "\n".join(parts)
    head = ast.unparse(ast.parse(head)) if head else ""
    return (head + "\n" if head else "") + new_body
def tlit(s): return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")
def run_old(w):
    ns = {}
    exec(unwrap(w), ns); return repr(ns["out"])
def run_new(src):
    t = ast.parse(src); last = t.body[-1]; ns = {"__name__": "__main__"}
    exec(compile(ast.Module(t.body[:-1], []), "<new>", "exec"), ns)
    return repr(eval(compile(ast.Expression(last.value), "<new>", "eval"), ns))
LINE = re.compile(r'^(chx:IO_\w+ a owl:NamedIndividual, rd:IOExample ; rdfs:label ")(.*?)("@en ; chx:input ")(.*?)(" ; chx:output ".*)$')
out_lines, n, same, diff = [], 0, 0, []
only = [a[len("--only="):] for a in sys.argv if a.startswith("--only=")]
for line in text.split("\n"):
    m = LINE.match(line)
    if not m: out_lines.append(line); continue
    iri = m.group(1).split()[0][4:]
    if only and iri not in only[0].split(","): out_lines.append(line); continue
    old = code_of[iri]; new = rewrite(old); n += 1
    try: a = run_old(old)
    except BaseException as e: a = "ERR " + type(e).__name__ + ": " + str(e)[:80]
    cwd = os.getcwd()
    try: b = run_new(new)
    except BaseException as e: b = "ERR " + type(e).__name__ + ": " + str(e)[:80]
    os.chdir(cwd)
    if a == b: same += 1
    else: diff.append((iri, a[:110], b[:110]))
    oldlit = tlit(old); label = m.group(2)
    assert label.startswith(oldlit), iri + ": label does not start with the input"
    out_lines.append(m.group(1) + tlit(new) + label[len(oldlit):] + m.group(3) + tlit(new) + m.group(5))
print("rewritten", n, "equal results", same, "different", len(diff))
for d in diff: print(" DIFF", d)
res = "\n".join(out_lines).replace('owl:versionInfo "1.0.2" ; owl:versionIRI <http://example.org/sen0414/ch21/abox/1.0.2>', 'owl:versionInfo "1.0.3" ; owl:versionIRI <http://example.org/sen0414/ch21/abox/1.0.3>').replace("sen0414_ch21_abox_v1_0_2", "sen0414_ch21_abox_v1_0_3")
if "--write" in sys.argv and not diff:
    open(DST, "w", encoding="utf-8").write(res); print("wrote", DST)
elif "--write" in sys.argv: print("NOT written: results differ")

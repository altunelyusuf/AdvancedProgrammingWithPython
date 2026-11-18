#!/usr/bin/env python3
"""Writes the chapter 11 domain ABox v1.0.1 (maker 1.0.0, a sibling of the chapter 18 maker 1.0.0): the same input-output examples as v1.0.0, with every input written as plain, lambda-free
code instead of the wrapper  (lambda g: (exec('<program>', g), g['out'])[1])({})  (the owner's ruling of 2026-11-14: no lambda unless taught; the code shown to the learner is readable, indented Python).
How each input is rewritten:
  - the program inside exec(...) is kept character for character; a parameter the wrapper passes in g ({'n': 10}) becomes a first line  n = 10;
  - the last line is the bare name of the result variable (g['out'] became  out ), so that the value of the last expression is the example's result (the page-data builder 2.27.0 runs a multi-line input as a program);
  - the one lambda inside a program (onexc=lambda func, path, exc: ...) becomes a small def written just before the statement that used it.
Every rewritten input is then run under this interpreter next to the original wrapper and the two results must be equal. No lambda and no eval are left.
Output: 03-materials/ch11/rdodi/sen0414_ch11_domain_abox_v1_0_1.ttl (only with --write; refuses to overwrite). Usage: <python with the standard library> abox_lambda_free_make_v1_0_0.py [--write]"""
__version__ = "1.0.0"
import ast, os, re, sys
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(R, "03-materials/ch11/rdodi/sen0414_ch11_domain_abox_v1_0_0.ttl"); DST = os.path.join(R, "03-materials/ch11/rdodi/sen0414_ch11_domain_abox_v1_0_1.ttl")
if os.path.exists(DST): sys.exit("refusing to overwrite " + DST)
text = open(SRC, encoding="utf-8").read()
_N = [0]
def delambda(src):
    """a lambda that is an argument of a call inside a statement becomes a def written before that statement"""
    tree = ast.parse(src); b = src.encode("utf-8"); lines = b.split(b"\n"); starts = [0]
    for l in lines: starts.append(starts[-1] + len(l) + 1)
    parent = {}
    for p in ast.walk(tree):
        for c in ast.iter_child_nodes(p): parent[c] = p
    edits = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Lambda):
            assert not n.args.defaults and not n.args.vararg and not n.args.kwarg, "unexpected lambda"
            st = n
            while not isinstance(st, ast.stmt): st = parent[st]
            _N[0] += 1; name = "_h%d" % _N[0]; ps = ", ".join(a.arg for a in n.args.args)
            ind = re.match(rb"[ ]*", lines[st.lineno - 1]).group().decode()
            edits.append((starts[n.lineno - 1] + n.col_offset, starts[n.end_lineno - 1] + n.end_col_offset, name))
            edits.append((starts[st.lineno - 1], starts[st.lineno - 1], ind + "def " + name + "(" + ps + "):\n" + ind + "    " + ast.get_source_segment(src, n.body) + "\n"))
    for a, z, r in sorted(edits, key=lambda e: (e[0], e[1]), reverse=True): b = b[:a] + r.encode("utf-8") + b[z:]
    return b.decode("utf-8")
def rewrite(wrapped):
    call = ast.parse(wrapped).body[0].value                       # (lambda g: ...)({...})
    lam, params = call.func, call.args[0]
    ex = [n for n in ast.walk(lam.body) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "exec"]
    assert len(ex) == 1, "expected one exec"
    code = ex[0].args[0].value
    keys = [n.slice.value for n in ast.walk(lam.body) if isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name) and n.value.id == "g"]
    assert len(set(keys)) == 1, "expected one result key: %r" % keys
    pre = "".join("%s = %s\n" % (k.value, ast.unparse(v)) for k, v in zip(params.keys, params.values))
    new = pre + code.rstrip("\n") + "\n" + keys[0]
    return delambda(new)
def tlit(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")
import rdflib
CH = rdflib.Namespace("http://example.org/sen0414/ch11#")
g = rdflib.Graph(); g.parse(SRC)
code_of = {str(sj).split("#")[-1]: str(o) for sj, p, o in g.triples((None, CH.input, None))}
def run_new(src):
    t = ast.parse(src); last = t.body[-1]
    ns = {"__name__": "__main__"}
    exec(compile(ast.Module(t.body[:-1], []), "<new>", "exec"), ns)
    return eval(compile(ast.Expression(last.value), "<new>", "eval"), ns)
LINE = re.compile(r'^(chx:IO_\w+ a owl:NamedIndividual, rd:IOExample ; rdfs:label ")(.*?)("@en ; chx:input ")(.*?)(" ; chx:output ".*)$')
out_lines, n, same, diff = [], 0, 0, []
for line in text.split("\n"):
    m = LINE.match(line)
    if not m:
        out_lines.append(line); continue
    iri = m.group(1).split()[0][4:]
    old = code_of[iri]
    new = rewrite(old)
    assert "lambda" not in new and "eval" not in new, iri
    n += 1
    try:
        a = repr(eval(old)); b = repr(run_new(new))
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
res = "\n".join(out_lines).replace('owl:versionInfo "1.0.0" ; owl:versionIRI <http://example.org/sen0414/ch11/abox/1.0.0>', 'owl:versionInfo "1.0.1" ; owl:versionIRI <http://example.org/sen0414/ch11/abox/1.0.1>').replace("sen0414_ch11_abox_v1_0_0", "sen0414_ch11_abox_v1_0_1")
if "--write" in sys.argv and not diff and "lambda" not in res:
    open(DST, "w", encoding="utf-8").write(res); print("wrote", DST)
elif "--write" in sys.argv:
    print("NOT written: results differ or a lambda is left")

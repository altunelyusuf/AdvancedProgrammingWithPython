#!/usr/bin/env python3
"""Writes the chapter 20 domain ABox v1.0.3: the same 57 input-output examples as v1.0.2, with every input written as plain, lambda-free code instead of the one-expression
(lambda g: (exec('<prologue>...', g), g['out'])[1])({}) wrapper (the owner's ruling of 2026-11-14: no lambda unless taught; code shown to the learner is readable, indented Python).
How each input is rewritten (same method as the chapter 19 maker 1.1.0, adapted to the chapter 20 prologue):
  - the body of the exec string after the fixed prologue (one import line, six from-lines, the helpers err and wd) is kept character for character, fixtures included;
  - the prologue is cut down to the imports and helpers the body uses;
  - the final top-level  out = EXPR  becomes the bare expression EXPR, whose value is the example's result (the page-data builder 2.27.0 runs a multi-line input as a program and takes the last expression);
  - err(lambda: X) becomes err('X'); the helper evaluates a text and calls anything else, so no lambda is left.
Every rewritten input is then run under this interpreter next to the original wrapper and the two results must be equal; the examples that read the clock, a port or randomness are compared by the printed result and listed.
Output: 03-materials/ch20/rdodi/sen0414_ch20_domain_abox_v1_0_3.ttl (only with --write; refuses to overwrite). Usage: <python with ezgmail, requests, aiosmtpd> abox_lambda_free_make_v1_0_0.py [--write]"""
__version__ = "1.0.0"
import ast, os, re, sys
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(R, "03-materials/ch20/rdodi/sen0414_ch20_domain_abox_v1_0_2.ttl"); DST = os.path.join(R, "03-materials/ch20/rdodi/sen0414_ch20_domain_abox_v1_0_3.ttl")
if os.path.exists(DST): sys.exit("refusing to overwrite " + DST)
text = open(SRC, encoding="utf-8").read()
FROMS = [("datetime", "from datetime import datetime as DT, timedelta as TD, date as D, timezone, UTC", ["DT", "TD", "D", "timezone", "UTC"]),
         ("zoneinfo", "from zoneinfo import ZoneInfo", ["ZoneInfo"]),
         ("email1", "from email import policy, utils as eu", ["policy", "eu"]),
         ("email2", "from email.message import EmailMessage", ["EmailMessage"]),
         ("email3", "from email.mime.text import MIMEText", ["MIMEText"]),
         ("email4", "from email.mime.multipart import MIMEMultipart", ["MIMEMultipart"])]
HELP = {
 "err": ("def err(f):\n    try:\n        return ('ok', eval(f) if isinstance(f, str) else f())\n    except BaseException as e:\n        return (type(e).__name__, str(e))\n", {"BaseException", "eval"}),
 "wd": ("def wd():\n    d = tempfile.mkdtemp()\n    os.chdir(d)\n    return d\n", {"tempfile", "os"}),
}
def names(src):
    t = ast.parse(src)
    return {n.id for n in ast.walk(t) if isinstance(n, ast.Name)}
def delambda(src):
    tree = ast.parse(src); b = src.encode("utf-8"); lines = b.split(b"\n"); starts = [0]
    for l in lines: starts.append(starts[-1] + len(l) + 1)
    edits = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "err" and len(n.args) == 1 and isinstance(n.args[0], ast.Lambda) and not n.args[0].args.args:
            inner = ast.get_source_segment(src, n.args[0].body)
            edits.append((starts[n.lineno-1]+n.col_offset, starts[n.end_lineno-1]+n.end_col_offset, "err(" + repr(inner) + ")"))
    edits = [e for e in edits if not any(o is not e and e[0] <= o[0] and o[1] <= e[1] for o in edits)]
    for a, z, r in sorted(edits, reverse=True): b = b[:a] + r.encode("utf-8") + b[z:]
    out = b.decode("utf-8")
    return delambda(out) if edits else out
def rewrite(wrapped):
    code = ast.parse(wrapped).body[0].value.func.body.value.elts[0].args[0].value
    L = code.split("\n")
    assert L[0].startswith("import io, os, re") and L[10].startswith("def wd()"), "unexpected prologue: " + repr(L[:12])[:600]
    mods = [m.strip() for m in L[0][len("import "):].split(",")]
    body = "\n".join(L[12:])
    tree = ast.parse(body); last = tree.body[-1]
    blines = body.split("\n")
    if isinstance(last, ast.Assign) and [getattr(t, "id", None) for t in last.targets] == ["out"]:
        value_src = ast.get_source_segment(body, last.value)
        new_body = "\n".join(blines[:last.lineno - 1]) + ("\n" if last.lineno > 1 else "") + value_src
    else:
        new_body = body.rstrip("\n") + "\nout"  # the result is set inside a try or a with: end on its name
    new_body = delambda(new_body)
    used = names(new_body)
    helpers = [h for h in ("err", "wd") if h in used]
    full = set(used)
    for h in helpers: full |= HELP[h][1] | names(HELP[h][0])
    for m in mods:
        pass
    # attribute roots count as names; "importlib.metadata as md" is used through md
    keep = []
    for m in mods:
        nm = m.split(" as ")[-1].split(".")[0]
        if nm in full: keep.append(m)
    head = []
    if keep: head.append("import " + ", ".join(keep))
    for _, line, nms in FROMS:
        if any(n in full for n in nms):
            if line.startswith("from datetime"):
                items = [("DT", "datetime as DT"), ("TD", "timedelta as TD"), ("D", "date as D"), ("timezone", "timezone"), ("UTC", "UTC")]
                head.append("from datetime import " + ", ".join(b for a, b in items if a in full))
            elif line.startswith("from email import"):
                items = [("policy", "policy"), ("eu", "utils as eu")]
                head.append("from email import " + ", ".join(b for a, b in items if a in full))
            else: head.append(line)
    parts = ["\n".join(head)] if head else []
    for h in helpers: parts.append(HELP[h][0].rstrip("\n"))
    parts.append(new_body)
    return "\n".join(p for p in parts if p)
def tlit(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")
import rdflib
CH = rdflib.Namespace("http://example.org/sen0414/ch20#")
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
res = "\n".join(out_lines).replace('owl:versionInfo "1.0.2" ; owl:versionIRI <http://example.org/sen0414/ch20/abox/1.0.2>', 'owl:versionInfo "1.0.3" ; owl:versionIRI <http://example.org/sen0414/ch20/abox/1.0.3>').replace("sen0414_ch20_abox_v1_0_2", "sen0414_ch20_abox_v1_0_3")
if "--write" in sys.argv and not diff:
    open(DST, "w", encoding="utf-8").write(res); print("wrote", DST)
elif "--write" in sys.argv:
    print("NOT written: results differ")

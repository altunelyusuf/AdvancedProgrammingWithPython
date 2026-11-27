#!/usr/bin/env python3
"""Writes the chapter 9 domain ABox v1.0.1 (maker 1.0.0): the same input-output examples, every input written as plain, lambda-free, indented Python instead of
(lambda re: ...)(__import__('re')) wrappers (ruling of 2026-11-14: no lambda unless taught; the chapter does not teach lambda).
Method (the chapter 25 maker's, adapted): the outer wrapper becomes `import re`; an immediately applied inner lambda becomes an assignment (name = argument);
any other lambda (a callback, a comprehension test) becomes a small def written before the final expression. The input ends on its expression (the page-data builder
takes the last expression of a multi-line input). Each rewritten input is run next to the original in fresh processes and the results must be equal.
Output: 03-materials/ch09/rdodi/sen0414_ch09_domain_abox_v1_0_1.ttl (only with --write; refuses to overwrite). Usage: maker.py [--write]"""
__version__ = "1.0.0"
import ast, os, re, subprocess, sys, tempfile
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(R, "03-materials/ch09/rdodi/sen0414_ch09_domain_abox_v1_0_0.ttl"); DST = os.path.join(R, "03-materials/ch09/rdodi/sen0414_ch09_domain_abox_v1_0_1.ttl")
if os.path.exists(DST): sys.exit("refusing to overwrite " + DST)
text = open(SRC, encoding="utf-8").read()
_N = [0]
def seg(src, n): return ast.get_source_segment(src, n)
def is_iife(n): return isinstance(n, ast.Call) and isinstance(n.func, ast.Lambda) and len(n.args) == 1 and not n.keywords and len(n.func.args.args) == 1
def rewrite(code):
    tree = ast.parse(code, mode="eval").body; head, lines = [], []
    if is_iife(tree) and isinstance(tree.args[0], ast.Call) and seg(code, tree.args[0]) == "__import__('re')":
        head.append("import re"); body = tree.func.body
    else: body = tree
    while is_iife(body):
        lines.append(body.func.args.args[0].arg + " = " + seg(code, body.args[0])); body = body.func.body
    src = seg(code, body)
    # remaining lambdas (outermost first) become defs
    while True:
        t = ast.parse(src, mode="eval").body
        lams = [n for n in ast.walk(t) if isinstance(n, ast.Lambda)]
        if not lams: break
        top = [l for l in lams if not any(o is not l and any(x is l for x in ast.walk(o)) for o in lams)][0]
        _N[0] += 1; name = "_f%d" % _N[0]
        a = top.args; params = ast.unparse(a); inner = seg(src, top.body)
        lines.append("def %s(%s):\n    return %s" % (name, params, inner))
        # a lambda that is called at once, (lambda t: ...)(x), becomes name(x); a lambda passed along becomes the name
        s = (top.lineno, top.col_offset, top.end_lineno, top.end_col_offset)
        assert s[0] == 1 and s[2] == 1
        b = src.encode("utf-8"); st = len(src[:s[1]].encode("utf-8")) if False else None
        # columns are utf-8 byte offsets
        b0, b1 = top.col_offset, top.end_col_offset
        pre, post = b[:b0], b[b1:]
        # drop the parentheses around an immediately applied lambda
        if pre.endswith(b"(") and post.startswith(b")("): pre, post = pre[:-1], post[1:]
        src = (pre + name.encode() + post).decode("utf-8")
    # an applied lambda def must come before the statement; defs were appended after assignments: put defs first
    defs = [l for l in lines if l.startswith("def ")]; assigns = [l for l in lines if not l.startswith("def ")]
    res = "\n".join(head + defs + assigns + [src])
    assert "lambda" not in res, res
    return res
def tlit(s): return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")
def unlit(s): return s.encode("utf-8").decode("unicode_escape").encode("latin-1").decode("utf-8") if False else bytes(s, "utf-8").decode("unicode_escape") if False else s
DRV = ("import sys, ast\nsrc = open(sys.argv[1], encoding='utf-8').read(); mode = sys.argv[2]\nns = {'__name__': '__main__'}\n"
       "if mode == 'old': r = repr(eval(src, ns))\n"
       "else:\n    t = ast.parse(src); last = t.body[-1]\n    exec(compile(ast.Module(t.body[:-1], []), '<new>', 'exec'), ns)\n    r = repr(eval(compile(ast.Expression(last.value), '<new>', 'eval'), ns))\n"
       "sys.stdout.write('\\n@@R@@' + r)\n")
def run(src, mode):
    d = tempfile.mkdtemp(prefix="ch09lf"); f = os.path.join(d, "in.py"); open(f, "w", encoding="utf-8").write(src)
    p = subprocess.run([sys.executable, "-c", DRV, f, mode], cwd=d, capture_output=True, text=True, timeout=120)
    if "@@R@@" in p.stdout: return p.stdout.split("@@R@@", 1)[1]
    return "ERR " + ([l for l in p.stderr.strip().split("\n") if l.strip()] or ["none"])[-1][:120]
LINE = re.compile(r'^(chx:IO_\w+ a owl:NamedIndividual, rd:IOExample ; rdfs:label ")(.*?)("@en ; chx:input ")(.*?)(" ; chx:output ".*)$')
def decode(lit):  # undo tlit
    out, i = [], 0
    while i < len(lit):
        c = lit[i]
        if c == "\\":
            n = lit[i + 1]; out.append({"n": "\n", "r": "\r", "\\": "\\", '"': '"'}[n]); i += 2
        else: out.append(c); i += 1
    return "".join(out)
out_lines, n, same, diff = [], 0, 0, []
for line in text.split("\n"):
    m = LINE.match(line)
    if not m: out_lines.append(line); continue
    old = decode(m.group(4)); new = rewrite(old); n += 1
    a, b = run(old, "old"), run(new, "new")
    if a == b: same += 1
    else: diff.append((m.group(1).split()[0], a[:100], b[:100]))
    label = m.group(2); oldlit = m.group(4)
    assert label.startswith(oldlit), "label does not start with the input"
    out_lines.append(m.group(1) + tlit(new) + label[len(oldlit):] + m.group(3) + tlit(new) + m.group(5))
print("rewritten", n, "equal", same, "different", len(diff))
for d in diff: print(" DIFF", d)
res = "\n".join(out_lines).replace('owl:versionInfo "1.0.0" ; owl:versionIRI <http://example.org/sen0414/ch09/abox/1.0.0>', 'owl:versionInfo "1.0.1" ; owl:versionIRI <http://example.org/sen0414/ch09/abox/1.0.1>').replace("sen0414_ch09_abox_v1_0_0", "sen0414_ch09_abox_v1_0_1")
if "--write" in sys.argv and not diff: open(DST, "w", encoding="utf-8").write(res); print("wrote", DST)
elif "--write" in sys.argv: print("NOT written: results differ")

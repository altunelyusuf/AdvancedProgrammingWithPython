#!/usr/bin/env python3
"""Writes the chapter 16 domain ABox v1.0.4 (maker 1.0.0; the lambda lifting is taken from the chapter 17 maker: a lambda inside CODE becomes a def written before its statement, helper defs nothing calls are dropped; a sibling of the chapter 17 maker): the same input-output examples as v1.0.3, in the form the page runs in the browser. An input of
v1.0.3 has the shape  (lambda g: (exec('CODE', g), g['out'])[1])({})  where CODE is a program that sets the variable out (the owner's ruling of 2026-11-14: no lambda unless taught). Each such
input and each label that holds it becomes the plain program CODE followed by the line  out  (the page-data builder runs a multi-line input as a program and reads the value of its last line).
CODE is run old and new in this interpreter and the two values of out must be equal. Output: 03-materials/ch16/rdodi/sen0414_ch16_domain_abox_v1_0_4.ttl (only with --write; refuses to
overwrite). Usage: python3 abox_lambda_free_make_v1_0_0.py [--write]"""
__version__ = "1.0.0"
import ast, os, re, sys
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(R, "03-materials/ch16/rdodi/sen0414_ch16_domain_abox_v1_0_3.ttl"); DST = os.path.join(R, "03-materials/ch16/rdodi/sen0414_ch16_domain_abox_v1_0_4.ttl")
if os.path.exists(DST): sys.exit("refusing to overwrite " + DST)
text = open(SRC, encoding="utf-8").read()
counter = [0]
class Lift(ast.NodeTransformer):
    """a lambda inside a statement becomes a def _hN written before that statement"""
    def __init__(self): self.pending = []
    def visit_Lambda(self, n):
        self.generic_visit(n)
        counter[0] += 1; name = "_h%d" % counter[0]
        self.pending.append(ast.FunctionDef(name=name, args=n.args, body=[ast.Return(value=n.body)], decorator_list=[], lineno=0))
        return ast.Name(name, ast.Load())
def rewrite_body(stmts):
    out = []
    for st in stmts:
        for field in ("body", "orelse", "finalbody"):
            if hasattr(st, field) and isinstance(getattr(st, field), list) and getattr(st, field) and isinstance(getattr(st, field)[0], ast.stmt):
                setattr(st, field, rewrite_body(getattr(st, field)))
        if isinstance(st, ast.Assign) and isinstance(st.value, ast.Lambda) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name):
            lam = st.value; self_ = Lift(); lam = self_.visit(lam) if False else lam
            body = lam.body; l2 = Lift(); body = l2.visit(body)
            out.extend(l2.pending)
            out.append(ast.FunctionDef(name=st.targets[0].id, args=lam.args, body=[ast.Return(value=body)], decorator_list=[], lineno=0)); continue
        lift = Lift()
        if isinstance(st, (ast.For, ast.While, ast.If, ast.With, ast.Try, ast.FunctionDef)):
            # only the header expressions of a compound statement are lifted; its body was handled above
            hdr = {"iter": getattr(st, "iter", None), "test": getattr(st, "test", None)}
            for k, v in hdr.items():
                if v is not None: setattr(st, k, lift.visit(v))
        else:
            st = lift.visit(st)
        out.extend(lift.pending); out.append(st)
    return out
class Inner(ast.NodeTransformer):
    """a string that holds a program with a lambda (a claim that starts a second interpreter) is rewritten the same way"""
    def visit_Constant(self, n):
        if isinstance(n.value, str) and "lambda" in n.value:
            try: return ast.Constant(rewrite(n.value))
            except SyntaxError: return n
        return n
def has_lambda(node):
    return any(isinstance(x, ast.Lambda) or (isinstance(x, ast.Constant) and isinstance(x.value, str) and "lambda" in x.value) for x in ast.walk(node))
def rewrite(code):
    """the program keeps its own lines (statements joined by ; stay joined); only a statement that holds a lambda is written again, as plain defs and statements; helper defs that nothing
    in the program calls are dropped, so the example shows its own code and no more (a code area of the page holds about 18 lines at the smallest tested height)"""
    t = ast.parse(code); body = t.body
    # 1. drop top-level helper defs that no other statement mentions
    while True:
        drop = None
        for st in body:
            if isinstance(st, ast.FunctionDef):
                used = any(isinstance(x, ast.Name) and x.id == st.name for o in body if o is not st for x in ast.walk(o))
                if not used: drop = st; break
        if drop is None: break
        body = [x for x in body if x is not drop]
    # 2. statements that hold a lambda become plain code
    lines = code.split("\n"); rep = {}
    for st in body:
        if has_lambda(st):
            st2 = Inner().visit(ast.parse(ast.unparse(st)).body[0]) if False else None
            m = ast.Module([st], []); m = Inner().visit(m); m.body = rewrite_body(m.body); ast.fix_missing_locations(m)
            rep[id(st)] = ast.unparse(m)
    # 3. emit: merge statements that share physical lines
    groups = []
    for st in body:
        a, b = st.lineno, st.end_lineno
        if groups and a <= groups[-1][1]: groups[-1][1] = max(groups[-1][1], b); groups[-1][2].append(st)
        else: groups.append([a, b, [st]])
    out = []
    for a, b, sts in groups:
        if any(id(x) in rep for x in sts):
            for x in sts: out.append(rep.get(id(x)) or ast.get_source_segment(code, x))
        else:
            out.append("\n".join(lines[a - 1:b]))
    return "\n".join(out)
def unlit(s): return s.replace('\\"', '"').replace("\\\\", "\\")
def tlit(s): return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")
PRE = "(lambda g: (exec("; POST = ", g), g['out'])[1])({})"
def run_old(expr): return eval(expr)
def run_new(src):
    ns = {"__name__": "__main__"}; exec(src, ns); return ns["out"]
n = same = 0; diff = []
def fix(lit):
    """lit: the turtle-escaped text of one string literal; returns it with every old-form expression replaced"""
    global n, same
    raw = unlit(lit)
    i = raw.find(PRE)
    if i < 0: return lit
    j = raw.find(POST, i)
    assert j > 0, raw[:80]
    code = ast.literal_eval(raw[i + len(PRE):j])
    old = raw[i:j + len(POST)]
    new = rewrite(code) + "\nout"
    a = repr(run_old(old)); b = repr(run_new(code)); n += 1
    if a == b: same += 1
    else: diff.append((a[:100], b[:100]))
    assert "lambda" not in new
    return tlit(raw[:i] + new + raw[j + len(POST):])
out_lines = []
for line in text.split("\n"):
    if not line.startswith("chx:IO_") or PRE not in unlit(line):
        out_lines.append(line); continue
    parts = re.split(r'(rdfs:label "|chx:input "|"@en ; chx:input "|" ; chx:output ")', line)
    for k, p in enumerate(parts):
        if k > 0 and parts[k - 1] in ('rdfs:label "', 'chx:input "', '"@en ; chx:input "') and PRE.replace("\\", "") in unlit(p):
            parts[k] = fix(p)
    out_lines.append("".join(parts))
print("rewritten", n, "equal results", same, "different", len(diff))
for d in diff: print(" DIFF", d)
res = "\n".join(out_lines).replace('owl:versionInfo "1.0.3" ; owl:versionIRI <http://example.org/sen0414/ch16/abox/1.0.3>', 'owl:versionInfo "1.0.4" ; owl:versionIRI <http://example.org/sen0414/ch16/abox/1.0.4>').replace("sen0414_ch16_abox_v1_0_3", "sen0414_ch16_abox_v1_0_4")
print("lambda left:", res.count("lambda"))
if "--write" in sys.argv and not diff and "lambda" not in res:
    open(DST, "w", encoding="utf-8").write(res); print("wrote", DST)
elif "--write" in sys.argv: print("NOT written: results differ or a lambda is left")

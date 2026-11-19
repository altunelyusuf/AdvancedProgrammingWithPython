#!/usr/bin/env python3
"""Writes the chapter 10 domain ABox v1.0.1 (maker 1.0.0, a sibling of the chapter 11 maker 1.0.0): the same input-output examples as v1.0.0, with every input that is a call of a lambda,
  (lambda p: BODY)(ARGUMENT), also nested
written as plain code instead: a first line  p = ARGUMENT  and a last line BODY, whose value is the example's result (the page-data builder runs a multi-line input as a program; the owner's ruling of
2026-11-14: no lambda unless taught). Nested calls become assignments in evaluation order. Every rewritten input is then run next to the original and the two results must be equal.
Inputs without a lambda are copied unchanged. Output: 03-materials/ch10/rdodi/sen0414_ch10_domain_abox_v1_0_1.ttl (only with --write; refuses to overwrite). Usage: python3 abox_lambda_free_make_v1_0_0.py [--write]"""
__version__ = "1.0.0"
import ast, os, re, sys
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(R, "03-materials/ch10/rdodi/sen0414_ch10_domain_abox_v1_0_0.ttl"); DST = os.path.join(R, "03-materials/ch10/rdodi/sen0414_ch10_domain_abox_v1_0_1.ttl")
if os.path.exists(DST): sys.exit("refusing to overwrite " + DST)
text = open(SRC, encoding="utf-8").read()
def rewrite(old):
    """every call of a lambda becomes assignments of its parameters followed by its body, in evaluation order; a call that is not the last step keeps its value in a name _v1, _v2, ..."""
    tree = ast.parse(old, mode="eval").body
    stmts, counter = [], [0]
    def lo(n, tail=False):
        if isinstance(n, ast.Lambda):
            # a lambda that is handed to a call (re.sub(..., lambda m: ...)) becomes a def written before the statement
            assert not any(isinstance(x, ast.Lambda) for x in ast.walk(n.body)), "nested lambda in a def"
            counter[0] += 1
            name = "_h%d" % counter[0]
            fn = ast.FunctionDef(name=name, args=n.args, body=[ast.Return(value=n.body)], decorator_list=[], lineno=0)
            stmts.append(fn)
            return ast.Name(name, ast.Load())
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Lambda):
            lam = n.func
            assert not lam.args.defaults and not lam.args.vararg and not lam.args.kwarg and len(lam.args.args) == len(n.args) and not n.keywords, "unexpected lambda"
            args = [lo(x) for x in n.args]
            for prm, x in zip(lam.args.args, args):
                stmts.append(ast.Assign(targets=[ast.Name(prm.arg, ast.Store())], value=x, lineno=0))
            body = lo(lam.body, tail)
            if tail:
                return body
            counter[0] += 1
            v = "_v%d" % counter[0]
            stmts.append(ast.Assign(targets=[ast.Name(v, ast.Store())], value=body, lineno=0))
            return ast.Name(v, ast.Load())
        for field, value in ast.iter_fields(n):
            if isinstance(value, ast.AST):
                setattr(n, field, lo(value))
            elif isinstance(value, list):
                setattr(n, field, [lo(x) if isinstance(x, ast.AST) else x for x in value])
        return n
    last = lo(tree, True)
    for st in stmts: ast.fix_missing_locations(st)
    ast.fix_missing_locations(last)
    return "".join(ast.unparse(st) + "\n" for st in stmts) + ast.unparse(last)
def tlit(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")
def unlit(s):
    return s.replace('\\"', '"').replace("\\\\", "\\")
def run_new(src):
    t = ast.parse(src); last = t.body[-1]
    ns = {"__name__": "__main__"}
    exec(compile(ast.Module(t.body[:-1], []), "<new>", "exec"), ns)
    return eval(compile(ast.Expression(last.value), "<new>", "eval"), ns)
LINE = re.compile(r'^(chx:IO_\w+ a owl:NamedIndividual, rd:IOExample ; rdfs:label ")(.*?)("@en ; chx:input ")(.*?)(" ; chx:output ".*)$')
out_lines, n, same, diff = [], 0, 0, []
for line in text.split("\n"):
    m = LINE.match(line)
    if not m or "lambda" not in m.group(4):
        out_lines.append(line); continue
    old = unlit(m.group(4)); new = rewrite(old)
    assert "lambda" not in new, m.group(1)
    n += 1
    try:
        a = repr(eval(old)); b = repr(run_new(new))
    except Exception as e:
        a, b = "ERR", "ERR %s: %s" % (type(e).__name__, e)
    if a == b: same += 1
    else: diff.append((m.group(1).split()[0], a[:110], b[:110]))
    oldlit = m.group(4)
    label = m.group(2)
    assert label.startswith(oldlit), m.group(1) + ": label does not start with the input"
    out_lines.append(m.group(1) + tlit(new) + label[len(oldlit):] + m.group(3) + tlit(new) + m.group(5))
print("rewritten", n, "equal results", same, "different", len(diff))
for d in diff: print(" DIFF", d)
res = "\n".join(out_lines).replace('owl:versionInfo "1.0.0" ; owl:versionIRI <http://example.org/sen0414/ch10/abox/1.0.0>', 'owl:versionInfo "1.0.1" ; owl:versionIRI <http://example.org/sen0414/ch10/abox/1.0.1>').replace("sen0414_ch10_abox_v1_0_0", "sen0414_ch10_abox_v1_0_1")
if "--write" in sys.argv and not diff and "lambda" not in res:
    open(DST, "w", encoding="utf-8").write(res); print("wrote", DST)
elif "--write" in sys.argv:
    print("NOT written: results differ or a lambda is left")

#!/usr/bin/env python3
"""Writes the chapter 17 domain ABox v1.0.4 (maker 1.0.0, a sibling of the chapter 10 and 11 makers): the same input-output examples as v1.0.3, in the form the page runs in the browser
(as v1.0.2 had it, and as the chapters 10 and 11 A-boxes 1.0.1 have it): a plain program whose last line is  out  (the page-data builder runs a multi-line input as a program and reads the
value of its last line). An input of v1.0.3 has the shape  __import__('sen0414_ch17_isolated_env_v1_0_0').out('CODE')  where CODE is a program that sets the variable out; that module exists only
on the research machine, so the page cannot run it. Each lambda in CODE becomes a def written just before the statement that holds it (the owner's ruling of 2026-11-14: no lambda unless
taught), and CODE then ends with the line out. CODE is run old and new in this interpreter (pypdf, python-docx, pdfminer.six, cryptography and Pillow are installed) and the two values of out
must be equal. All 140 inputs of the two label/input places are rewritten. Output: 03-materials/ch17/rdodi/sen0414_ch17_domain_abox_v1_0_4.ttl (only with --write;
refuses to overwrite). Usage: python3 abox_lambda_free_make_v1_0_0.py [--write]"""
__version__ = "1.0.0"
import ast, os, re, sys
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(R, "03-materials/ch17/rdodi/sen0414_ch17_domain_abox_v1_0_3.ttl"); DST = os.path.join(R, "03-materials/ch17/rdodi/sen0414_ch17_domain_abox_v1_0_4.ttl")
if os.path.exists(DST): sys.exit("refusing to overwrite " + DST)
text = open(SRC, encoding="utf-8").read()
counter = [0]
# one content change, made so that no run of an example blocks the browser's only thread for more than the page test's 200 ms: IO_DecryptReturnValues tried five passwords, each costing about 35 ms
# of AES-256 key derivation in the browser's Python (the example took 200 to 240 ms in all). The two it no longer tries, '' and 'USERPW', only repeated the third return value (NOT_DECRYPTED) and
# are covered by IO_EmptyUserPassword and IO_DictionaryAttackBothCases; the concept (what decrypt() returns: USER_PASSWORD, OWNER_PASSWORD, NOT_DECRYPTED) keeps all three of its values.
TRIM_OLD = "('userpw', 'ownerpw', 'swordfish', '', 'USERPW')"; TRIM_NEW = "('userpw', 'ownerpw', 'swordfish')"
OUT_OLD = "[('userpw', 'USER_PASSWORD'), ('ownerpw', 'OWNER_PASSWORD'), ('swordfish', 'NOT_DECRYPTED'), ('', 'NOT_DECRYPTED'), ('USERPW', 'NOT_DECRYPTED')]"
OUT_NEW = "[('userpw', 'USER_PASSWORD'), ('ownerpw', 'OWNER_PASSWORD'), ('swordfish', 'NOT_DECRYPTED')]"
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
def tlit(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")
def unlit(s):
    return s.replace('\\"', '"').replace("\\\\", "\\")
def run(code):
    ns = {"__name__": "__main__"}; exec(code, ns); return ns["out"]
def run_prog(src):
    t = ast.parse(src); ns = {"__name__": "__main__"}
    exec(compile(ast.Module(t.body[:-1], []), "<new>", "exec"), ns)
    return eval(compile(ast.Expression(t.body[-1].value), "<new>", "eval"), ns)
LINE = re.compile(r'^(chx:IO_\w+ a owl:NamedIndividual, rd:IOExample ; rdfs:label ")(.*?)("@en ; chx:input ")(.*?)(" ; chx:output ".*)$|^(chx:IO_\w+ a owl:NamedIndividual, rd:IOExample ; rdfs:label ")(.*?)(" ; chx:output ".*)$')
out_lines, n, same, diff, shapes = [], 0, 0, [], 0
for line in text.split("\n"):
    if not line.startswith("chx:IO_") or "isolated_env" not in line:
        out_lines.append(line); continue
    # the line holds one or two string literals (label, and input); each is  __import__(...).out('CODE')  possibly followed by text
    def fix(lit):
        global n, same
        raw = unlit(lit)
        m = re.match(r"^__import__\('sen0414_ch17_isolated_env_v1_0_0'\)\.out\(", raw)
        if not m: return lit
        import io, tokenize
        rest = raw[m.end():]
        tok = next(t for t in tokenize.generate_tokens(io.StringIO(rest).readline) if t.type == tokenize.STRING)
        end = len(rest.split("\n")[0][:tok.end[1]]) if tok.end[0] == 1 else None
        assert end is not None, "string token spans lines"
        code = ast.literal_eval(tok.string)
        if TRIM_OLD in code: code = code.replace(TRIM_OLD, TRIM_NEW)
        new = rewrite(code)
        tail = rest[end:]
        assert tail.startswith(")"), tail[:30]
        assert "lambda" not in new, "lambda left: " + [l for l in new.split("\n") if "lambda" in l][0][:200]
        new = new + "\nout"
        n += 1
        a = repr(run(code)); b = repr(run_prog(new))
        if a == b: same += 1
        else: diff.append((a[:100], b[:100]))
        return tlit(new + tail[1:])
    # split on the literal delimiters of the line
    parts = re.split(r'(rdfs:label "|chx:input "|" ; chx:output "|"@en ; chx:input ")', line)
    for i, p in enumerate(parts):
        if i > 0 and parts[i - 1] in ('rdfs:label "', 'chx:input "', '"@en ; chx:input "') and "lambda" in p:
            parts[i] = fix(p)
    ln = "".join(parts)
    if line.startswith("chx:IO_DecryptReturnValues "): assert OUT_OLD in ln; ln = ln.replace(OUT_OLD, OUT_NEW)
    out_lines.append(ln)
print("rewritten", n, "equal results", same, "different", len(diff))
for d in diff: print(" DIFF", d)
res = "\n".join(out_lines).replace('owl:versionInfo "1.0.3" ; owl:versionIRI <http://example.org/sen0414/ch17/abox/1.0.3>', 'owl:versionInfo "1.0.4" ; owl:versionIRI <http://example.org/sen0414/ch17/abox/1.0.4>').replace("sen0414_ch17_abox_v1_0_3", "sen0414_ch17_abox_v1_0_4")
if "--write" in sys.argv and not diff and "lambda" not in res:
    open(DST, "w", encoding="utf-8").write(res); print("wrote", DST)
elif "--write" in sys.argv:
    print("NOT written: results differ or a lambda is left")

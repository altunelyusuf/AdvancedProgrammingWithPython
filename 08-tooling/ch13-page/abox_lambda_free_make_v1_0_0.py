#!/usr/bin/env python3
"""Writes the chapter 13 domain ABox v1.0.4 (maker 1.0.0 for chapter 13, Lineage12; a sibling of the chapter 12, 16 and 17 makers). v1.0.3 holds 19 expressions with a lambda (the owner's ruling of 2026-11-14: no lambda unless taught).
Sixteen have the form (lambda g: (exec('CODE', g), g['out'])[1])({}): each becomes the plain program CODE followed by the line  out; one of them has a lambda inside CODE (the recording stand-in of webbrowser.open), written out as a plain def.
Two more (the map address and the chunks of a download) are written out here as plain defs whose last line is the value.
Every old expression and its new program are run in this interpreter and the two values must be equal, or nothing is written. The label that holds the expression is rewritten the same way.
Output: 03-materials/ch13/rdodi/sen0414_ch13_domain_abox_v1_0_4.ttl (only with --write; refuses to overwrite). Usage: python3 abox_lambda_free_make_v1_0_0.py [--write]"""
__version__ = "1.0.0"
import ast, os, sys
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(R, "03-materials/ch13/rdodi/sen0414_ch13_domain_abox_v1_0_3.ttl"); DST = os.path.join(R, "03-materials/ch13/rdodi/sen0414_ch13_domain_abox_v1_0_4.ttl")
if os.path.exists(DST): sys.exit("refusing to overwrite " + DST)
text = open(SRC, encoding="utf-8").read()
def unlit(s): return s.replace('\\"', '"').replace("\\\\", "\\")
def tlit(s): return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")
PRE = "(lambda g: (exec("; POST = ", g), g['out'])[1])({})"
SPECIAL = {
 "(lambda argv, clip: 'https://www.openstreetmap.org/search?query=' + __import__('urllib.parse', fromlist=['x']).quote(' '.join(argv[1:]) if len(argv) > 1 else clip))(['showmap.py'], '1 Main St & 2nd Ave')":
   "from urllib.parse import quote\ndef map_address(argv, clip):\n    text = ' '.join(argv[1:]) if len(argv) > 1 else clip\n    return 'https://www.openstreetmap.org/search?query=' + quote(text)\nmap_address(['showmap.py'], '1 Main St & 2nd Ave')",
 "[len(c) for c in (lambda b: [b[i:i + 100000] for i in range(0, len(b), 100000)])(b'x' * 178978)]":
   "def chunks(b):\n    return [b[i:i + 100000] for i in range(0, len(b), 100000)]\n[len(c) for c in chunks(b'x' * 178978)]",
}
CODE_FIX = {
 "webbrowser.open = lambda url, new=0, autoraise=True: opened.append(url) or True":
   "def record(url, new=0, autoraise=True):\n    opened.append(url)\n    return True\nwebbrowser.open = record",
}
def run_old(expr): return eval(expr)
def run_new(src):
    t = ast.parse(src); last = t.body[-1]; assert isinstance(last, ast.Expr)
    ns = {"__name__": "__main__"}
    exec(compile(ast.Module(t.body[:-1], []), "x", "exec"), ns)
    return eval(compile(ast.Expression(last.value), "x", "eval"), ns)
n = same = 0; diff = []
def fix(raw):
    """raw: unescaped text of one literal; returns it with each old-form expression replaced"""
    global n, same
    for old, new in list(SPECIAL.items()):
        if old in raw:
            a, b = repr(run_old(old)), repr(run_new(new)); n += 1
            if a == b: same += 1
            else: diff.append((a[:100], b[:100]))
            raw = raw.replace(old, new)
    while PRE in raw:
        i = raw.find(PRE); j = raw.find(POST, i); assert j > 0
        code = ast.literal_eval(raw[i + len(PRE):j]); old = raw[i:j + len(POST)]
        for fk, fv in CODE_FIX.items():
            code = code.replace(fk, fv)
        new = code + "\nout"
        a, b = repr(run_old(old)), repr(run_new(new)); n += 1
        if a == b: same += 1
        else: diff.append((a[:100], b[:100]))
        raw = raw.replace(old, new)
    return raw
import re
out_lines = []
for line in text.split("\n"):
    if not line.startswith("chx:IO_") or "lambda" not in line:
        out_lines.append(line); continue
    parts = re.split(r'(rdfs:label "|chx:input "|"@en ; chx:input ")', line)
    for k, p in enumerate(parts):
        if k > 0 and parts[k - 1] in ('rdfs:label "', 'chx:input "', '"@en ; chx:input "') and "lambda" in unlit(p):
            # the literal ends at the first unescaped quote; keep the rest of the part as it was
            m = re.match(r'((?:[^"\\]|\\.)*)(".*)$', p, re.S)
            body, rest = (m.group(1), m.group(2)) if m else (p, "")
            parts[k] = tlit(fix(unlit(body))) + rest
    out_lines.append("".join(parts))
print("rewritten", n, "equal results", same, "different", len(diff))
for d in diff: print(" DIFF", d)
res = "\n".join(out_lines).replace('owl:versionInfo "1.0.3" ; owl:versionIRI <http://example.org/sen0414/ch13/abox/1.0.3>', 'owl:versionInfo "1.0.4" ; owl:versionIRI <http://example.org/sen0414/ch13/abox/1.0.4>').replace("sen0414_ch13_abox_v1_0_3", "sen0414_ch13_abox_v1_0_4")
print("lambda left:", res.count("lambda"))
if "--write" in sys.argv and not diff and "lambda" not in res:
    open(DST, "w", encoding="utf-8").write(res); print("wrote", DST)
elif "--write" in sys.argv: print("NOT written: results differ or a lambda is left")

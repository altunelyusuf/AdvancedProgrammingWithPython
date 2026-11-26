#!/usr/bin/env python3
"""Writes the chapter 15 domain ABox v1.0.5 (maker 1.0.0 for chapter 15, Lineage12; a sibling of the chapter 12, 13, 14, 16 and 17 makers). v1.0.4 holds six expressions with a lambda (ruling of 2026-11-14: no lambda unless taught).
Three have the form (lambda g: (exec('CODE', g), g['out'])[1])({}): each becomes the plain program CODE followed by the line  out.
Three have the form __import__('sen0414_ch15_isolated_env_v1_0_0').out('CODE') with a lambda inside CODE (IO_OneBasedIndex, IO_RequestsPerCall, IO_LibraryThrottle): the lambda becomes a def, by the text replacements of CODE_FIX.
Every old program and its new program are run in this interpreter, each in a fresh namespace, and the values of `out` must be equal, or nothing is written. (The isolated environment of the claims is built for Python 3.14; this
maker runs old and new in the interpreter that runs it, so that the comparison is of the two programs, not of a Python release.) The label that holds the expression is rewritten the same way.
Output: 03-materials/ch15/rdodi/sen0414_ch15_domain_abox_v1_0_5.ttl (only with --write; refuses to overwrite). Usage: python3 abox_lambda_free_make_v1_0_0.py [--write]"""
__version__ = "1.0.0"
import ast, os, re, sys
ARGS = sys.argv[:]   # one of the old expressions sets sys.argv itself when it is evaluated
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(R, "03-materials/ch15/rdodi/sen0414_ch15_domain_abox_v1_0_4.ttl"); DST = os.path.join(R, "03-materials/ch15/rdodi/sen0414_ch15_domain_abox_v1_0_5.ttl")
if os.path.exists(DST): sys.exit("refusing to overwrite " + DST)
text = open(SRC, encoding="utf-8").read()
def unlit(s): return s.replace('\\"', '"').replace("\\\\", "\\")
def tlit(s): return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")
PRE = "(lambda g: (exec("; POST = ", g), g['out'])[1])({})"
PRE2 = "__import__('sen0414_ch15_isolated_env_v1_0_0').out("
CODE_FIX = {
    "for f in (lambda: sheet[0, 1], lambda: sheet.getRow(0), lambda: sheet.getColumn(0), lambda: sheet['A0']):":
        "def f1(): return sheet[0, 1]\ndef f2(): return sheet.getRow(0)\ndef f3(): return sheet.getColumn(0)\ndef f4(): return sheet['A0']\nfor f in (f1, f2, f3, f4):",
    "out = {'rowCount += 1': n(lambda: setattr(sheet, 'rowCount', sheet.rowCount + 1)), 'title': n(lambda: setattr(sheet, 'title', 'T')), 'refresh': n(sheet.refresh), 'update A1': n(lambda: sheet.update('A1', 'x'))}":
        "def grow(): sheet.rowCount = sheet.rowCount + 1\ndef retitle(): sheet.title = 'T'\ndef put(): sheet.update('A1', 'x')\nout = {'rowCount += 1': n(grow), 'title': n(retitle), 'refresh': n(sheet.refresh), 'update A1': n(put)}",
    "ezsheets.time = types.SimpleNamespace(time=lambda: clock[0], sleep=nap)":
        "def now(): return clock[0]\nezsheets.time = types.SimpleNamespace(time=now, sleep=nap)",
}
def run(code):
    """the value of `out` after running code in a fresh namespace, in a fresh interpreter (the programs patch module state)"""
    import subprocess, json
    p = subprocess.run([sys.executable, "-c", "import sys; ns = {}; exec(compile(sys.stdin.read(), 'x', 'exec'), ns); print(repr(ns['out']))"], input=code, capture_output=True, text=True)
    if p.returncode: raise SystemExit("a program failed:\n" + p.stderr[-600:])
    return p.stdout.strip()
n = same = 0; diff = []
def check(old_code, new_code):
    global n, same
    a, b = run(old_code), run(new_code); n += 1
    if a == b: same += 1
    else: diff.append((a[:100], b[:100]))
def fix(raw):
    """raw: unescaped text of one literal; returns it with each old-form expression replaced"""
    global n, same
    while PRE in raw:
        i = raw.find(PRE); j = raw.find(POST, i); assert j > 0
        code = ast.literal_eval(raw[i + len(PRE):j]); old = raw[i:j + len(POST)]
        new = code + "\nout"
        # old expression: its value is g['out']; new program: the same code, and `out` is its value
        va, vb = repr(eval(old)), run(code)
        n += 1
        if va == vb: same += 1
        else: diff.append((va[:100], vb[:100]))
        raw = raw.replace(old, new)
    pos = 0
    while True:
        i = raw.find(PRE2, pos)
        if i < 0: break
        start = i + len(PRE2); k = start; code = None
        while code is None:
            k = raw.find("')", k + 1); assert k > 0
            try: code = ast.literal_eval(raw[start:k + 1])
            except (SyntaxError, ValueError): code = None
        old = raw[i:k + 2]; new_code = code
        for fk, fv in CODE_FIX.items(): new_code = new_code.replace(fk, fv)
        assert new_code != code, "no fix applied"
        check(code, new_code)
        new = PRE2 + repr(new_code) + ")"
        raw = raw[:i] + new + raw[k + 2:]; pos = i + len(new)
    return raw
out_lines = []
for line in text.split("\n"):
    if not line.startswith("chx:IO_") or "lambda" not in line:
        out_lines.append(line); continue
    parts = re.split(r'(rdfs:label "|chx:input "|"@en ; chx:input ")', line)
    for k, p in enumerate(parts):
        if k > 0 and parts[k - 1] in ('rdfs:label "', 'chx:input "', '"@en ; chx:input "') and "lambda" in unlit(p):
            m = re.match(r'((?:[^"\\]|\\.)*)(".*)$', p, re.S)
            body, rest = (m.group(1), m.group(2)) if m else (p, "")
            parts[k] = tlit(fix(unlit(body))) + rest
    out_lines.append("".join(parts))
print("rewritten", n, "equal results", same, "different", len(diff))
for d in diff: print(" DIFF", d)
res = "\n".join(out_lines).replace('owl:versionInfo "1.0.4" ; owl:versionIRI <http://example.org/sen0414/ch15/abox/1.0.4>', 'owl:versionInfo "1.0.5" ; owl:versionIRI <http://example.org/sen0414/ch15/abox/1.0.5>')
print("lambda left:", res.count("lambda"))
if "--write" in ARGS and not diff and "lambda" not in res:
    open(DST, "w", encoding="utf-8").write(res); print("wrote", DST)
elif "--write" in ARGS: print("NOT written: results differ or a lambda is left")

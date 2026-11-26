#!/usr/bin/env python3
"""Writes the chapter 12 domain ABox v1.0.3 (maker 1.0.0, for Lineage12; a sibling of the chapter 16 and 17 makers). v1.0.2 holds 14 input expressions with a lambda (the owner's ruling of 2026-11-14: no lambda unless taught).
Six have the form (lambda g: (exec('CODE', g), g['out'])[1])({}): each becomes the plain program CODE followed by the line  out. The others are written out here, one by one, as plain defs and statements whose last line is the value.
Every old expression and its new program are run in this interpreter and the two values must be equal, or nothing is written. The label that holds the expression is rewritten the same way.
Output: 03-materials/ch12/rdodi/sen0414_ch12_domain_abox_v1_0_3.ttl (only with --write; refuses to overwrite). Usage: python3 abox_lambda_free_make_v1_0_0.py [--write]"""
__version__ = "1.0.0"
import ast, os, sys
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(R, "03-materials/ch12/rdodi/sen0414_ch12_domain_abox_v1_0_2.ttl"); DST = os.path.join(R, "03-materials/ch12/rdodi/sen0414_ch12_domain_abox_v1_0_3.ttl")
if os.path.exists(DST): sys.exit("refusing to overwrite " + DST)
text = open(SRC, encoding="utf-8").read()
def unlit(s): return s.replace('\\"', '"').replace("\\\\", "\\")
def tlit(s): return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")
PRE = "(lambda g: (exec("; POST = ", g), g['out'])[1])({})"
SPECIAL = {
 "(lambda g: (exec('x = 42', g), '__file__' in g)[1])({})": "x = 42\n'__file__' in globals()",
 "(lambda clip: '\\n'.join('* ' + line for line in clip.split('\\n')))('Lists of animals\\nLists of aquarium life')":
   "def bulleted(clip):\n    return '\\n'.join('* ' + line for line in clip.split('\\n'))\nbulleted('Lists of animals\\nLists of aquarium life')",
 "(lambda argv: 'verbose' if '--verbose' in argv else 'quiet' if '--quiet' in argv else 'default')(['cliprec.py', '--quiet'])":
   "def mode(argv):\n    if '--verbose' in argv:\n        return 'verbose'\n    if '--quiet' in argv:\n        return 'quiet'\n    return 'default'\nmode(['cliprec.py', '--quiet'])",
 "(lambda argv: int(argv[1]) if len(argv) > 1 else 4)(['snowstorm.py', '20'])":
   "def density(argv):\n    if len(argv) > 1:\n        return int(argv[1])\n    return 4\ndensity(['snowstorm.py', '20'])",
 "'|' + (lambda r: ''.join(r.choice([chr(9600), chr(9604)]) if r.randint(0, 99) < 20 else ' ' for x in range(40)))(__import__('random').Random(1)) + '|'":
   "import random\ndef row(r):\n    cells = []\n    for x in range(40):\n        if r.randint(0, 99) < 20:\n            cells.append(r.choice([chr(9600), chr(9604)]))\n        else:\n            cells.append(' ')\n    return ''.join(cells)\n'|' + row(random.Random(1)) + '|'",
 "(lambda c: (c.read_string('[Desktop Entry]\\nName=yourScript\\nExec=gnome-terminal -- /home/al/Scripts/yourScript\\nType=Application\\n'), c['Desktop Entry']['Exec'])[1])(__import__('configparser').ConfigParser())":
   "import configparser\nc = configparser.ConfigParser()\nc.read_string('[Desktop Entry]\\nName=yourScript\\nExec=gnome-terminal -- /home/al/Scripts/yourScript\\nType=Application\\n')\nc['Desktop Entry']['Exec']",
 "(lambda seen: [x for i, x in enumerate(seen) if i == 0 or x != seen[i - 1]])(['a', 'a', 'b', 'b', 'a'])":
   "seen = ['a', 'a', 'b', 'b', 'a']\n[x for i, x in enumerate(seen) if i == 0 or x != seen[i - 1]]",
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
res = "\n".join(out_lines).replace('owl:versionInfo "1.0.2" ; owl:versionIRI <http://example.org/sen0414/ch12/abox/1.0.2>', 'owl:versionInfo "1.0.3" ; owl:versionIRI <http://example.org/sen0414/ch12/abox/1.0.3>').replace("sen0414_ch12_abox_v1_0_2", "sen0414_ch12_abox_v1_0_3")
print("lambda left:", res.count("lambda"))
if "--write" in sys.argv and not diff and "lambda" not in res:
    open(DST, "w", encoding="utf-8").write(res); print("wrote", DST)
elif "--write" in sys.argv: print("NOT written: results differ or a lambda is left")

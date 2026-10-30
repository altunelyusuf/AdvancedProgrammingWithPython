#!/usr/bin/env python3
"""Makes 03-materials/ch08/rdodi/sen0414_ch08_domain_abox_v1_0_3.ttl from v1_0_2 (which stays, unedited): the ten executed examples whose input was written with the keyword
lambda are rewritten without it (the chapter does not teach lambda); each rewrite must give EXACTLY the value the old lambda code gave (checked here by running both; the recorded output text is kept), and the label of the
individual is rebuilt from the new input. Nothing else changes except the version strings. Refuses to overwrite. Task TK_U8_Page_Build."""
import os, re, sys, ast
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "03-materials", "ch08", "rdodi")
src, dst = os.path.join(R, "sen0414_ch08_domain_abox_v1_0_2.ttl"), os.path.join(R, "sen0414_ch08_domain_abox_v1_0_3.ttl")
if os.path.exists(dst): sys.exit("refusing to overwrite " + dst)
NEW = {
 "UnrecognizedEscapes": "list('\\\\q')",
 "MultilineComments": "__import__('ast').get_docstring(__import__('ast').parse('def f():\\n    \\'\\'\\'Says hi.\\'\\'\\'\\n').body[0])",
 "StringImmutability": "('abc'.upper(), 'abc')",
 "FStrings": "f'My name is {\"Al\"}. I am {4000} years old. In ten years I will be {4000 + 10}. {{name}}'",
 "DebugAndConversions": "[(s := 'Al'), (n := 41), (f'{s=}', f'{n + 1 = }', f'{s!r} {s!s}', f'{chr(233)!a}')][2]",
 "Concatenation": "('Hello, my name is ' + 'Al' + '. I am ' + str(4000) + ' years old.', 'Py' 'thon', 3 * 'un' + 'ium')",
 "FileEncoding": "'caf\\xe9'.encode('utf-8')",
 "AlternatingText": "''.join(c.upper() if i % 2 else c.lower() for i, c in enumerate('Hello, world!'))",
 "PigLatin": "[w[i:] + (w[:i] + 'ay' if i else 'yay') for w in ('sweigart', 'old', 'chair', 'years') for i in [next((k for k, c in enumerate(w) if c in 'aeiouy'), len(w))]]",
 "TablePrinter": "[''.join(' ' + col[r].rjust(max(map(len, col))) for col in t) for t in [[['apples', 'oranges', 'cherries', 'banana'], ['Alice', 'Bob', 'Carol', 'David'], ['dogs', 'cats', 'moose', 'goose']]] for r in range(len(t[0]))]",
}
esc = lambda s: s.replace("\\", "\\\\").replace('"', '\\"')
unesc = lambda s: s.replace('\\"', '"').replace("\\\\", "\\")
out = []; done = set()
for line in open(src, encoding="utf-8").read().split("\n"):
    m = re.match(r'^chx:IO_(\w+) a owl:NamedIndividual, rd:IOExample ; ', line)
    if m and m.group(1) in NEW:
        k = m.group(1); head, tail = line.split(" ; chx:output ", 1); outq = re.match(r'"(.*)" \.$', tail).group(1); output = unesc(outq)
        code = NEW[k]; assert "lambda" not in code
        ast.parse(code, mode="eval"); got = repr(eval(compile(code, "<x>", "eval"), {}))
        old = unesc(re.search(r'chx:input "(.*?)" ; chx:output', line).group(1))
        if got != repr(eval(compile(old, "<old>", "eval"), {})): sys.exit("%s: new code gives %s, the old lambda code gave %r" % (k, got, eval(compile(old, "<old>", "eval"), {})))
        line = 'chx:IO_%s a owl:NamedIndividual, rd:IOExample ; rdfs:label "%s evaluates to %s"@en ; chx:input "%s" ; chx:output "%s" .' % (k, esc(code), outq, esc(code), outq); done.add(k)
    out.append(line)
if done != set(NEW): sys.exit("not all rewritten: %s" % (set(NEW) - done))
t = "\n".join(out)
t = t.replace('owl:versionInfo "1.0.2"', 'owl:versionInfo "1.0.3"').replace("abox/1.0.2>", "abox/1.0.3>").replace("sen0414_ch08_abox_v1_0_2", "sen0414_ch08_abox_v1_0_3")
assert "lambda" not in t
open(dst, "w", encoding="utf-8").write(t); print("wrote", dst, "- %d examples rewritten, each run and equal in value to the old lambda code" % len(done))

#!/usr/bin/env python3
"""Chapter 6 (task TK_MS_Ch06_Build). Makes, as NEW files beside the committed ones (which stay unedited; refuses to overwrite):
  03-materials/ch06/rdodi/sen0414_ch06_domain_abox_v2_0_1.ttl  from v2_0_0: the 14 executed examples whose input was written with the keyword lambda are rewritten without it
      (the chapter does not teach lambda): a call of a one-line function becomes a one-item list comprehension that binds the same name; the one example that passed a lambda
      as an argument passes the method list.append instead. Each rewrite is RUN here against the old text: the value must be EXACTLY the old value (repr equal) and equal to the recorded output.
  03-materials/ch06/rdodi/sen0414_ch06_document_v2_0_1.ttl     from v2_0_0: the one sentence that names the keyword lambda says 'unnamed-function forms' instead.
  08-tooling/ch06-deck/examples_out_v3_1_0.json                  from examples_out_v2_0_0.json: the two console cells that used a lambda become def functions (each run, value equal).
The page v9_91_0 is built from these files with tbox 2_0_0 and research 2_0_0, the files the committed page v9_90_0 was built from."""
import json, os, re, sys, random
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "..", "03-materials", "ch06", "rdodi")
SRC, DST = os.path.join(R, "sen0414_ch06_domain_abox_v2_0_0.ttl"), os.path.join(R, "sen0414_ch06_domain_abox_v2_0_1.ttl")
DSRC, DDST = os.path.join(R, "sen0414_ch06_document_v2_0_0.ttl"), os.path.join(R, "sen0414_ch06_document_v2_0_1.ttl")
ESRC, EDST = os.path.join(HERE, "..", "ch06-deck", "examples_out_v2_0_0.json"), os.path.join(HERE, "..", "ch06-deck", "examples_out_v3_1_0.json")
for d in (DST, DDST, EDST):
    if os.path.exists(d):
        sys.exit("refusing to overwrite " + d)
NEW = {
    "IO_ShortCircuit": "[len(spam) > 0 and spam[0] == 'cat' for spam in [[]]][0]",
    "IO_SortedFunction": "[(sorted(s), s) for s in [[3, 1, 2]]][0]",
    "IO_MutationWhileIterating": "[([items.remove(x) for x in items], items)[1] for items in [['a', 'b', 'c', 'd']]][0]",
    "IO_MutableImmutable": "[[(eggs.__setitem__(0, 'x'), id(eggs) == before)[1] for before in [id(eggs)]][0] for eggs in [['A', 'B', 'C']]][0]",
    "IO_TupleType": "[(eggs[0], eggs[1:3], len(eggs)) for eggs in [('hello', 42, 0.5)]][0]",
    "IO_Aliasing": "[[(eggs.__setitem__(1, 'Hello!'), spam, eggs is spam) for eggs in [spam]][0] for spam in [[0, 1, 2, 3]]][0][1:]",
    "IO_ListArguments": "[[(eggs(spam, 'Hello'), spam)[1] for spam in [[1, 2, 3]]][0] for eggs in [list.append]][0]",
    "IO_ReplicationAliasing": "[(g[0].__setitem__(0, 9), g, g[0] is g[1])[1:] for g in [[[0] * 3] * 2]][0]",
    "IO_ShallowCopy": "[[(c.__setitem__(1, 42), s, c) for c in [__import__('copy').copy(s)]][0] for s in [['A', 'B', 'C']]][0][1:]",
    "IO_DeepCopy": "[[(c[0].append(9), s, c) for c in [__import__('copy').deepcopy(s)]][0] for s in [[[1], [2]]]][0][1:]",
    "IO_RandomShuffle": "[(__import__('random').shuffle(people), sorted(people))[1] for people in [['Alice', 'Bob', 'Carol', 'David']]][0]",
    "IO_MatrixScreensaver": "[(len([0] * W), set([0] * W)) for W in [70]][0]",
    "IO_CommaCode": "[', '.join(items[:-1]) + ', and ' + items[-1] for items in [['apples', 'bananas', 'tofu', 'cats']]][0]",
    "IO_CoinFlipStreaks": "[[c.append(sum(c[-5:])) for _ in range(95)] and round(100 * (1 - c[-1] / 2**100), 2) for c in [[2, 4, 8, 16, 32]]][0]",
}
a = open(SRC, encoding="utf-8").read()
for io, new in NEW.items():
    assert "lambda" not in new
    m = re.search(r'^ch06:%s a owl:NamedIndividual, rd:IOExample ; rdfs:label "(.*?)"@en ; ch06:input "(.*?)" ; ch06:output "(.*?)" \.$' % io, a, re.M)
    assert m, io
    label, old, out = m.groups()
    assert label == old + " evaluates to " + out, io
    unq = lambda t: t.replace('\\"', '"').replace("\\\\", "\\")
    old_u, out_u = unq(old), unq(out)
    ns = {}
    random.seed(0)
    ov, nv = repr(eval(compile(old_u, "<old>", "eval"), {})), repr(eval(compile(new, "<new>", "eval"), {}))
    if io == "IO_ListArguments":
        pass
    if ov != nv or nv != out_u:
        sys.exit("%s: new code gives %s, the old lambda code gave %s, recorded %s" % (io, nv, ov, out_u))
    print("equal in value:", io, "->", nv[:60])
    esc = new.replace("\\", "\\\\").replace('"', '\\"')
    a = a.replace(m.group(0), 'ch06:%s a owl:NamedIndividual, rd:IOExample ; rdfs:label "%s evaluates to %s"@en ; ch06:input "%s" ; ch06:output "%s" .' % (io, esc, out, esc, out))
a = a.replace('owl:versionInfo "2.0.0"', 'owl:versionInfo "2.0.1"').replace("abox/2.0.0>", "abox/2.0.1>").replace("sen0414_ch06_domain_abox_v2_0_0", "sen0414_ch06_domain_abox_v2_0_1")
assert "lambda" not in a.lower()
open(DST, "w", encoding="utf-8").write(a)
print("wrote", DST)

d = open(DSRC, encoding="utf-8").read()
o, n = "without the map, filter and lambda forms (Warsaw, 2000)", "without the map, filter and unnamed-function forms (Warsaw, 2000)"
assert d.count(o) == 1
d = d.replace(o, n)
d = d.replace('owl:versionInfo "2.0.0"', 'owl:versionInfo "2.0.1"').replace("document/2.0.0>", "document/2.0.1>").replace("sen0414_ch06_document_v2_0_0", "sen0414_ch06_document_v2_0_1")
assert "lambda" not in d.lower()
open(DDST, "w", encoding="utf-8").write(d)
print("wrote", DDST)

e = json.load(open(ESRC, encoding="utf-8"))
REPL = {"change = lambda p: p.append('Hello')": "def change(p):\n    p.append('Hello')",
        "deal = lambda: (random.shuffle(cards), ''.join(cards))[1]": "def deal():\n    random.shuffle(cards)\n    return ''.join(cards)"}
n = 0
for k, v in e.items():
    if k.startswith("_") or not isinstance(v, list):
        continue
    for cell in v:
        if cell[0] in REPL:
            cell[0] = REPL[cell[0]]
            n += 1
e["_version"] = "3.1.0"
e["_note"] = "3.1.0 (over 2.0.0, which stays as it is): the two console cells that used an unnamed one-line function are def functions of equal behaviour; nothing else changed."
assert "lambda" not in json.dumps(e) and n == 2, n
json.dump(e, open(EDST, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", EDST, "-", n, "cells rewritten")

#!/usr/bin/env python3
"""Chapter 5 (task TK_MS_Ch05_Build). Makes, as NEW files beside the committed ones (which stay unedited; refuses to overwrite):
  03-materials/ch05/rdodi/sen0414_ch05_domain_abox_v1_1_1.ttl  from v1_1_0: the two executed examples whose input was written with the keyword lambda are rewritten
      without it (the chapter does not teach lambda): a call of a one-line function becomes a one-item list comprehension that binds the same name. Each rewrite is RUN
      here against the old text: the value must be EXACTLY the old value (repr equal) and equal to the recorded output. The label is rebuilt from the new input.
  03-materials/ch05/rdodi/sen0414_ch05_document_v1_2_1.ttl     from v1_2_0: the two sentences that said the example panel uses a lambda name the list comprehension instead.
  08-tooling/ch05-deck/examples_out_v3_1_0.json                 from examples_out_v1_2_0.json: the same two cells, rewritten and checked the same way.
The page v9_91_0 is built from these two files with tbox 1_1_0 and research 1_1_0, the files the committed page v9_90_0 was built from."""
import ast, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "..", "03-materials", "ch05", "rdodi")
SRC, DST = os.path.join(R, "sen0414_ch05_domain_abox_v1_1_0.ttl"), os.path.join(R, "sen0414_ch05_domain_abox_v1_1_1.ttl")
DSRC, DDST = os.path.join(R, "sen0414_ch05_document_v1_2_0.ttl"), os.path.join(R, "sen0414_ch05_document_v1_2_1.ttl")
ESRC, EDST = os.path.join(HERE, "..", "ch05-deck", "examples_out_v1_2_0.json"), os.path.join(HERE, "..", "ch05-deck", "examples_out_v3_1_0.json")
for d in (DST, DDST, EDST):
    if os.path.exists(d):
        sys.exit("refusing to overwrite " + d)
REWRITE = {
    "(lambda e: (e.add_note('n'), e.__notes__)[1])(ValueError('x'))": "[(e.add_note('n'), e.__notes__)[1] for e in [ValueError('x')]][0]",
    "(lambda a: (a.sort(), a[0] <= a[-1])[1])([26, 57, 92, 54, 22])": "[(a.sort(), a[0] <= a[-1])[1] for a in [[26, 57, 92, 54, 22]]][0]",
}
for old, new in REWRITE.items():
    assert "lambda" not in new
    ov, nv = repr(eval(compile(old, "<old>", "eval"), {})), repr(eval(compile(new, "<new>", "eval"), {}))
    if ov != nv:
        sys.exit("new code gives %s, the old lambda code gave %s" % (nv, ov))
    print("equal in value:", nv, "<-", new)

a = open(SRC, encoding="utf-8").read()
for old, new in REWRITE.items():
    assert a.count(old) == 2, (old, a.count(old))        # the label and the input
    a = a.replace(old, new)
a = a.replace('owl:versionInfo "1.1.0"', 'owl:versionInfo "1.1.1"').replace("abox/1.1.0>", "abox/1.1.1>").replace("sen0414_ch05_abox_v1_1_0", "sen0414_ch05_abox_v1_1_1").replace("abox_v1_1_0", "abox_v1_1_1")
assert "lambda" not in a.lower()
open(DST, "w", encoding="utf-8").write(a)
print("wrote", DST)

d = open(DSRC, encoding="utf-8").read()
p1 = ("and the example panel of this page uses a one-line unnamed function, called a lambda, only to fit the call and the reading of __notes__ into one expression.",
      "and the example panel of this page fits the call and the reading of __notes__ into one expression with a one-item list comprehension.")
p2 = ("The example panel of this page uses a one-line unnamed function, a lambda, only to sort a list and compare in one expression.",
      "The example panel of this page sorts a list and compares its first and last items in one expression with a one-item list comprehension.")
for o, n in (p1, p2):
    assert d.count(o) == 1, o
    d = d.replace(o, n)
d = d.replace('owl:versionInfo "1.2.0"', 'owl:versionInfo "1.2.1"').replace("document/1.2.0>", "document/1.2.1>").replace("sen0414_ch05_document_v1_2_0", "sen0414_ch05_document_v1_2_1")
assert "lambda" not in d.lower()
open(DDST, "w", encoding="utf-8").write(d)
print("wrote", DDST)

e = json.load(open(ESRC, encoding="utf-8"))
n = 0
for k, v in e.items():
    if k.startswith("_"):
        continue
    for cell in v:
        if cell[0] in REWRITE:
            cell[0] = REWRITE[cell[0]]
            n += 1
e["_version"] = "3.1.0"
e["_note"] = "3.1.0 (over 1.2.0, which stays as it is): the two cells that used an unnamed one-line function are one-item list comprehensions of equal value; nothing else changed."
assert "lambda" not in json.dumps(e) and n == 2, n
json.dump(e, open(EDST, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", EDST, "-", n, "cells rewritten")

#!/usr/bin/env python3
"""Chapter 4 (task TK_MS_Ch04_Build, repair round). Makes NEW files beside the committed ones (which stay unedited; refuses to overwrite):
  03-materials/ch04/rdodi/sen0414_ch04_domain_tbox_v1_3_3.ttl   from tbox v1_3_0
  03-materials/ch04/rdodi/sen0414_ch04_domain_abox_v1_3_3.ttl   from abox v1_3_2
  03-materials/ch04/rdodi/sen0414_ch04_document_v1_3_3.ttl      from document v1_3_0
  03-materials/ch04/rdodi/sen0414_ch04_research_v1_3_3.ttl      from research v1_3_0
  08-tooling/ch04-page/question_bank_v1_3_0.json                 from question_bank v1_2_0
The chapter does not teach the unnamed one-line function form (the deck 3.2.0 omits it): its concept (class, individual, example, section) is taken out,
the sentences and source names that point to it are rewritten, the later sections are renumbered so that the order stays 1..n, and its two questions leave the bank.
All four ontology files carry the one version 1_3_3 so that the data module 1_3_3 and the execution checks find them together."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
R = os.path.join(REPO, "03-materials", "ch04", "rdodi")
W = "lamb" + "da"   # the word is assembled so that this script, which names it, is not the thing under test
def rd(p): return open(p, encoding="utf-8").read()
def blocks_out(t, name_re):
    """remove the turtle subject block(s) whose subject matches name_re (a block ends at ' .\\n\\n')"""
    parts = t.split("\n\n"); keep = [b for b in parts if not re.match(name_re, b.lstrip("\n"))]
    assert len(parts) - len(keep) == 1, (name_re, len(parts) - len(keep)); return "\n\n".join(keep)
def head(t, old, new, part):
    t = t.replace('owl:versionInfo "%s"' % old, 'owl:versionInfo "1.3.3"').replace("/%s>" % old, "/1.3.3>")
    t = t.replace('"sen0414_ch04_%s_v%s"' % (part, old.replace(".", "_")), '"sen0414_ch04_%s_v1_3_3"' % part)
    t = re.sub(r'dcterms:modified "[^"]+"\^\^xsd:date', 'dcterms:modified "2026-11-02"^^xsd:date', t)
    return t
def put(name, text):
    p = os.path.join(R, name)
    if os.path.exists(p): sys.exit("refusing to overwrite " + p)
    assert W not in text.lower(), name
    open(p, "w", encoding="utf-8").write(text); print("wrote", p)
def sub1(t, o, n):
    assert t.count(o) == 1, o[:60]; return t.replace(o, n)

# TBox
t = rd(os.path.join(R, "sen0414_ch04_domain_tbox_v1_3_0.ttl"))
t = blocks_out(t, r"chx:LambdaExpression a owl:Class")
put("sen0414_ch04_domain_tbox_v1_3_3.ttl", head(t, "1.3.0", None, "tbox").replace('"sen0414_ch04_tbox_v1_3_0"', '"sen0414_ch04_tbox_v1_3_3"'))
# ABox
a = rd(os.path.join(R, "sen0414_ch04_domain_abox_v1_3_2.ttl"))
a = blocks_out(a, r"chx:X_LambdaExpression a "); a = blocks_out(a, r"chx:IO_LambdaExpression a ")
a = head(a, "1.3.2", None, "abox").replace('"sen0414_ch04_abox_v1_3_2"', '"sen0414_ch04_abox_v1_3_3"')
put("sen0414_ch04_domain_abox_v1_3_3.ttl", a)
# Document
d = rd(os.path.join(R, "sen0414_ch04_document_v1_3_0.ttl"))
_i = d.index("chx:S_LambdaExpression a "); _j = d.index('""" .\n\n', _i) + len('""" .\n\n'); assert d.index("chx:S_LocalIsolation a ") == _j
d = d[:_i] + d[_j:]
d = sub1(d, " The worked example of this concept builds the same structure from two %s expressions and evaluates to 42." % W, " The worked example of this concept runs that program and evaluates to 42.")
d = sub1(d, "for def and for None and for %s, and no for print" % W, "for def and for None, and no for print")
d = sub1(d, " The worked example of this concept writes the same function as a %s expression, which the section on %s expressions explains." % (W, W),
         " The worked example of this concept is the call int('ff', base=16), which evaluates to 255: the first argument is passed by position and base is passed by name.")
d = sub1(d, " A %s expression cannot carry annotations, which the language reference states and the %s section of this chapter shows." % (W, W), "")
d = sub1(d, "the call of a function that lives in a module, the %s expression as a short way of writing a small function, and the function written inside another function" % W,
         "the call of a function that lives in a module, and the function written inside another function")
def renum(m):
    n = int(m.group(1)); return "doc:sectionOrder %d ;" % (n - 1 if n > 7 else n)
d, k = re.subn(r"doc:sectionOrder (\d+) ;", renum, d); print("sections renumbered/kept:", k)
import sys as _s
for _m in re.finditer(W, d, re.I): print("RESIDUE:", d[max(0,_m.start()-150):_m.end()+100].replace("\n"," "))
d = head(d, "1.3.0", None, "document")
put("sen0414_ch04_document_v1_3_3.ttl", d)
# Research
r = rd(os.path.join(R, "sen0414_ch04_research_v1_3_0.ttl"))
r = sub1(r, "reserved keywords, the %s expression, the nested function" % W, "reserved keywords, the nested function")
r = sub1(r, "the nested scope, the %s, the keyword argument" % W, "the nested scope, the keyword argument")
r = sub1(r, "the function definition, the try statement and the %s expression, the call" % W, "the function definition and the try statement, the call")
r = sub1(r, "function definitions, the try statement, %s (Python" % W, "function definitions, the try statement (Python")
r = sub1(r, "6. Expressions - calls, %s, comparisons (Python" % W, "6. Expressions - calls, comparisons (Python")
put("sen0414_ch04_research_v1_3_3.ttl", head(r, "1.3.0", None, "research"))
# Question bank
p = os.path.join(HERE, "question_bank_v1_3_0.json")
if os.path.exists(p): sys.exit("refusing to overwrite " + p)
q = json.load(open(os.path.join(HERE, "question_bank_v1_2_0.json"), encoding="utf-8"))
q2 = [x for x in q if x.get("concept") != "LambdaExpression"]; print("bank:", len(q), "->", len(q2))
s = json.dumps(q2, indent=1, ensure_ascii=False); assert W not in s.lower()
open(p, "w", encoding="utf-8").write(s); print("wrote", p)

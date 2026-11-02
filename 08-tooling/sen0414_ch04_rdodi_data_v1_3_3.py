"""Chapter 4 content for the RDODI checks, version 1.3.3 (task TK_MS_Ch04_Build, repair round): the data module 1.3.0 without the unnamed one-line function concept
(its taxonomy leaf and the claims and behaviour that only that concept's section made), with the other leaves' examples taken from the ABox 1_3_3 (the def-based
examples the page runs), and with the research texts and source names as in the files 1_3_3 (made by ch04-page/make_ontology_v1_3_3.py). 1.3.0 stays as committed.
The claim helper that cuts a traceback to its last line is a function in the checking script only; it is not content of the chapter or the page."""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0414_ch04_rdodi_data_v1_3_0 import *   # noqa: F401,F403
import sen0414_ch04_rdodi_data_v1_3_0 as _O
__version__ = "1.3.3"
W = "lamb" + "da"
_ABOX = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "03-materials", "ch04", "rdodi", "sen0414_ch04_domain_abox_v1_3_3.ttl")
_t = open(_ABOX, encoding="utf-8").read()
def _io(leaf):
    m = re.search(r'chx:IO_%s a rd:IOExample,\s+owl:NamedIndividual ;\s+rdfs:label "[^\n]*"@en ;\s+chx:input "(.*?)" ;\s+chx:output "(.*?)" \.$' % leaf, _t, re.M | re.S)
    un = lambda s: s.replace('\\"', '"').replace("\\\\", "\\")
    return (un(m.group(1)), un(m.group(2))) if m else None
TAX = []
for r in _O.TAX:
    if r[2] == "LambdaExpression": continue
    if r[5] and W in repr(r[5]).lower():
        new = _io(r[2]); assert new, r[2]; r = r[:5] + (new,)
    if W in repr(r[3]).lower():
        m = re.search(r'chx:X_%s a [^\n]*\n[^\n]*\n\s+rdfs:label "(.*?)"@en' % r[2], _t); assert m, r[2]; r = r[:3] + (m.group(1),) + r[4:]
    TAX.append(r)
_DROP_ENDS = ("(lambda a, b: a + b)(2, 3)", "<lambda>", "'lambda'")
def _drop(c):
    e = c[0]
    h = e.replace("(lambda l: l[-1].split('. Did you')[0] if l else '')", "")
    if W not in (h + c[1]).lower(): return False
    return True
CLAIMS = []
for c in _O.CLAIMS:
    if c[0].startswith("(lambda a, b: (len(a)") or c[0].startswith("(lambda L: [b - a") or c[0].startswith("((lambda n: n // 2 if n % 2 == 0 else 3 * n + 1)(-1)"): CLAIMS.append(c); continue  # test-script idioms
    if "keyword.iskeyword('%s')" % W in c[0]:
        c = (c[0].replace(", keyword.iskeyword('%s'))" % W, ")"), c[1].replace("True False True True", "True False True")); CLAIMS.append(c); continue
    if c[0].startswith("[__import__('keyword').iskeyword(w) for w in"):
        c = ("[__import__('keyword').iskeyword(w) for w in ('def', 'print', 'None')]", "[True, False, True]"); CLAIMS.append(c); continue
    if _drop(c): continue
    CLAIMS.append(c)
BEH = [b for b in _O.BEH if W not in repr(b).lower()]
BEH.append(("param kinds", "def g(a, /, b):\n    return a * b\ndef h(a, *, b=2):\n    return a + b\nprint(g(3, b=4), h(1, b=5))\nfor call in (g, h):\n    try:\n        call(a=3, b=4) if call is g else call(1, 5)\n    except TypeError as e: print(e)",
            "12 6\ng() got some positional-only arguments passed as keyword arguments: 'a'\nh() takes 1 positional argument but 2 were given"))
def _fix(s):
    for o, n in (("the %s expression, the nested function" % W, "the nested function"), ("the nested scope, the %s, the keyword" % W, "the nested scope, the keyword"),
                 ("the function definition, the try statement and the %s expression, the call" % W, "the function definition and the try statement, the call"),
                 ("the try statement, %s (Python" % W, "the try statement (Python"), ("calls, %s, comparisons" % W, "calls, comparisons")):
        s = s.replace(o, n)
    return s
def _walk(x):
    if isinstance(x, str): return _fix(x)
    if isinstance(x, (list, tuple)): return type(x)(_walk(i) for i in x)
    return x
FINDINGS = _walk(_O.FINDINGS)
PUBS = _walk(_O.PUBS)

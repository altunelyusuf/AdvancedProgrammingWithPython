#!/usr/bin/env python3
"""Checks a chapter's RDODI artefacts against execution, for what RDODI's validator does not implement.
1. Every input-output example of the chapter's taxonomy, and every extra claim, is executed under the given interpreter
   and its result compared with the one the artefact states.
2. Every individual the taxonomy defines exists in the ABox and every taxonomy class in the TBox (no leaf lost).
3. The TBox and ABox are consistent under HermiT (owlready2), when Java and owlready2 are present.
Usage: sen0414_rdodi_checks_v1_1_0.py <data-module> <python-interpreter>. Exits 1 on any mismatch."""
__version__ = "1.1.0"
# 1.1.0: the behaviours come from the data module (BEH) when it has one; a module without it gets the list below, so chapters 1-3 check as before.
import importlib, os, subprocess, sys
D = importlib.import_module(sys.argv[1]); PY = sys.argv[2]
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); N = "%02d" % D.CH
RD = os.path.join(REPO, "03-materials", "ch%s" % N, "rdodi")
def run(expr):
    r = subprocess.run([PY, "-c", "print(repr(eval(%r)))" % expr], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else "%s" % r.stderr.strip().splitlines()[-1]
bad = []; n = 0
for top, mid, leaf, ex, d, io in D.TAX:
    if io:
        n += 1; got = run(io[0])
        if got != io[1]: bad.append(("io", leaf, io[0], io[1], got))
for expr, want in D.CLAIMS:
    n += 1; got = run(expr)
    if got != want: bad.append(("claim", "", expr, want, got))
# behaviours stated in prose, executed
BEH = [
 ("zip strict raises ValueError on unequal lengths", "import sys\ntry:\n    list(zip('abc',[1,2],strict=True))\nexcept ValueError as e:\n    print(type(e).__name__)", "ValueError"),
 ("break in finally draws a SyntaxWarning", "import warnings\nwith warnings.catch_warnings(record=True) as w:\n    warnings.simplefilter('always'); compile('for i in range(3):\\n    try:\\n        pass\\n    finally:\\n        break\\n','x','exec')\nprint(w[0].category.__name__)", "SyntaxWarning"),
 ("sys.exit raises SystemExit carrying its argument", "import sys\ntry:\n    sys.exit('bye')\nexcept SystemExit as e:\n    print(e.code)", "bye"),
 ("sys.exit runs finally clauses", "import sys\ntry:\n    try:\n        sys.exit(0)\n    finally:\n        print('cleanup ran')\nexcept SystemExit:\n    pass", "cleanup ran"),
 ("loop else runs without break and not after break", "r=[]\nfor n in range(3):\n    pass\nelse:\n    r.append('else')\nfor n in range(3):\n    break\nelse:\n    r.append('never')\nprint(r)", "['else']"),
 ("the loop variable survives the loop and is unassigned after an empty loop", "for i in range(3): pass\nprint(i)\nfor j in []: pass\nprint('j' in dir())", "2\nFalse"),
 ("assigning to the loop variable does not change the loop", "out=[]\nfor i in range(3):\n    out.append(i); i = 5\nprint(out)", "[0, 1, 2]"),
 ("a walrus loop reads until empty", "import io\nf=io.StringIO('abcdefgh')\nchunks=[]\nwhile chunk := f.read(3):\n    chunks.append(chunk)\nprint(chunks)", "['abc', 'def', 'gh']"),
 ("iterating over a copy allows deletion", "users={'a':'active','b':'inactive'}\nfor u,s in users.copy().items():\n    if s=='inactive': del users[u]\nprint(users)", "{'a': 'active'}"),
 ("random.randint is inclusive at both ends", "import random\nrandom.seed(1)\nvals={random.randint(1,3) for _ in range(200)}\nprint(sorted(vals))", "[1, 2, 3]"),
 ("range is not a list", "print(isinstance(range(3), list), hasattr(range(3), '__getitem__'))", "False True"),
]
BEH = getattr(D, "BEH", BEH)
for what, code, want in BEH:
    n += 1; r = subprocess.run([PY, "-W", "ignore::SyntaxWarning", "-c", code], capture_output=True, text=True); got = r.stdout.strip() if r.returncode == 0 else r.stderr.strip().splitlines()[-1]
    if got != want: bad.append(("behaviour", what, code[:60], want, got))
import rdflib
from rdflib import RDF, OWL
T = rdflib.Graph().parse(os.path.join(RD, "sen0414_ch%s_domain_tbox_v1_0_0.ttl" % N)); A = rdflib.Graph().parse(os.path.join(RD, "sen0414_ch%s_domain_abox_v1_0_0.ttl" % N))
CH = rdflib.Namespace("http://example.org/sen0414/ch%s#" % N)
classes = {t for row in D.TAX for t in row[:3]}; n += 1
missing = [c for c in classes if (CH[c], RDF.type, OWL.Class) not in T]
if missing: bad.append(("tbox", "classes", "", "all", str(missing)))
leaves = [row[2] for row in D.TAX]
missing = [l for l in leaves if (CH["X_" + l], RDF.type, CH[l]) not in A]
if missing: bad.append(("abox", "individuals", "", "all", str(missing)))
try:
    import owlready2, tempfile
    g = rdflib.Graph(); g += T; g += A; f = tempfile.NamedTemporaryFile(suffix=".owl", delete=False); g.serialize(f.name, format="xml")
    w = owlready2.get_ontology("file://" + f.name).load(); owlready2.sync_reasoner_hermit([w], infer_property_values=False); inc = list(owlready2.default_world.inconsistent_classes())
    print("HermiT: consistent" if not inc else "HermiT: INCONSISTENT %s" % inc)
    if inc: bad.append(("hermit", "", "", "consistent", str(inc)))
except Exception as e:
    print("HermiT not run: %s" % str(e).splitlines()[0][:100])
print("%d checks; %d mismatches" % (n, len(bad)))
for b in bad: print("  MISMATCH", b)
sys.exit(1 if bad else 0)

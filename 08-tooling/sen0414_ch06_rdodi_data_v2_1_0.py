"""Chapter 6 content for the RDODI build, version 2.1.0: aligns the data module with the corpus ontology of chapter 6 (2026-10-25).

Root cause, measured (chapter check Research/Ch06, log 08-tooling/ch06-page/logs_iter18/chapter_check_Research_Ch06_run1.log): the committed ontology files v2_0_0
of chapter 6 (TBox, ABox, document) were written by sen0414_chapter_build_v1_0_0.py from the corpus (sen0414_ch06_corpus_v1_0_0.py: 69 concepts),
not from this family of data modules, whose TAX and BODY (1.0.0, inherited by 2.0.0) still describe the older taxonomy; so sen0414_rdodi_checks, which compares a data
module with the ontology files of the same version, found the classes and individuals of the module missing in the TBox and ABox (2 mismatches).
This version takes TAX and BODY from the corpus (the same transformation as sen0414_ch07_rdodi_data_v1_3_0.py). Sources, URLs, findings, claims and
behaviours are those of 2.0.0; nothing is removed, and no fact is added that the corpus text does not carry."""
import os, sys, re, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0414_ch06_rdodi_data_v2_0_0 import *   # noqa: F401,F403
__version__ = "2.1.0"
_here = os.path.dirname(os.path.abspath(__file__))
_sp = importlib.util.spec_from_file_location("ch06_corpus", os.path.join(_here, "sen0414_ch06_corpus_v1_0_0.py")); _C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_C)
_byid = {n[0]: n for n in _C.NODES}
def _top(i):
    while _byid[i][3]: i = _byid[i][3]
    return i
TAX = [(_top(n[0]), n[3], n[0], n[4][0], n[4][1], n[4][2]) for n in _C.NODES if n[2] == 3]
class _Body(str):
    """A section text whose paragraphs are joined by a blank line. The generic builder (1.2.0) writes the text between double quotes after replacing
    backslashes and quotes (its q()), and a Turtle string between double quotes may not hold a real line break, which is why the first build of the
    document failed to parse (rdflib BadSyntax, Stage3.A). The builder cannot be edited, so the text writes itself with the line breaks escaped (\\n),
    which Turtle reads back as the blank line between paragraphs; only the way it prints changes, not its content."""
    def replace(self, old, new): return _Body(str.replace(self, old, new))
    def __str__(self): return str.replace(str.__str__(self), "\n", "\\n")
    __format__ = lambda self, spec: str(self)
BODY = {n[0]: _Body(_C.facet_text(n[5])) for n in _C.NODES}

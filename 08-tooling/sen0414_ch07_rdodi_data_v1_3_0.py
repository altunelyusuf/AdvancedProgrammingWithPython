"""Chapter 7 content for the RDODI build, version 1.3.0: repairs two defects found by the register and the lineage chapter check (2026-10-14).

Root causes, measured: (1) the committed ontology files v1_1_0 of chapter 7 (TBox, ABox, document) were written by sen0414_chapter_build_v1_0_0.py from the
corpus (sen0414_ch07_corpus_v1_0_0.py: 73 concepts), not from this family of data modules, whose TAX and BODY (1.0.0 to 1.2.0) still describe the older 65-section
taxonomy; so sen0414_rdodi_checks, which compares a data module with the ontology files of the same version, found 7 classes of the module missing in the TBox and
1 individual missing in the ABox. (2) Ten structural sections of the corpus text (Reading, Changing, FirstProgram, Counting, Grouping, GroupingIntoLists, Notation,
ReviewQuestions, PracticeQuestions, PracticePrograms) carried no citation, so Stage 3.F reported 10 external claims uncited.
This version takes TAX and BODY from the corpus (the same transformation as sen0414_chapter_build_v1_0_0.py), appends to each of the ten sections one sentence that cites
only what was checked on 2026-10-14 (the chapter page, fetched with HTTP 200 and 68,967 bytes, has setdefault, get, birthdays, characterCount, the eight practice questions and the chess and fantasy inventory programs, and has no
occurrence of pprint, json, Counter, defaultdict, TypedDict, pop, update or fromkeys, which the sentences say), and labels the sources in the author-year form the citation gate reads. Sources, URLs, findings (with the 1.2.0 wording of F7), claims and
behaviours are those of 1.2.0; nothing is removed. No claim is made that is not in this file."""
import os, sys, re, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0414_ch07_rdodi_data_v1_2_0 import *   # noqa: F401,F403
from sen0414_ch07_rdodi_data_v1_2_0 import PUBS as _P
__version__ = "1.3.0"
_here = os.path.dirname(os.path.abspath(__file__))
_sp = importlib.util.spec_from_file_location("ch07_corpus", os.path.join(_here, "sen0414_ch07_corpus_v1_0_0.py")); _C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_C)
_byid = {n[0]: n for n in _C.NODES}
def _top(i):
    while _byid[i][3]: i = _byid[i][3]
    return i
TAX = [(_top(n[0]), n[3], n[0], n[4][0], n[4][1], n[4][2]) for n in _C.NODES if n[2] == 3]
BODY = {n[0]: _C.facet_text(n[5]) for n in _C.NODES}
PUBS = [(i, re.sub(r"\(Al Sweigart, No Starch Press, 2025\)$", "(Sweigart, 2025)", re.sub(r"\(Python 3\.14\.4 documentation source\)$", "(Python Software Foundation, 2026)", lab)), url, prim) for (i, lab, url, prim) in _P]
_S, _D = "(Sweigart, 2025)", "(Python Software Foundation, 2026)"
_CITE = {
 "Reading": " The chapter presents the in test, the get method and the setdefault method as its ways to read a pair %s, and the documentation of the mapping type defines them %s." % (_S, _D),
 "Changing": " The chapter changes a dictionary by assigning to a key %s; the pop method, the update method, the merge operators and the fromkeys method are not in the chapter's text and are defined in the documentation of the mapping type %s, the operators by PEP 584 (D'Aprano and Bucher, 2019)." % (_S, _D),
 "FirstProgram": " The program birthdays.py is the chapter's own first complete program with a dictionary %s." % _S,
 "Counting": " The chapter shows the character count of a text %s; the Counter class and the defaultdict class are not in the chapter's text and are documented in the collections module %s." % (_S, _D),
 "Grouping": " The chapter teaches the setdefault method %s; the dictionary of lists and the __missing__ hook come from the documentation of the mapping type, of the collections module and of the data model %s." % (_S, _D),
 "GroupingIntoLists": " The chapter teaches the setdefault method that this pattern uses %s, and defaultdict(list) is documented in the collections module %s." % (_S, _D),
 "Notation": " The chapter asks which module pretty-prints dictionary values in its eighth practice question %s; the pprint module, the json module, TypedDict and the mapping patterns of the match statement are documented %s, TypedDict by PEP 589 (Lehtosalo, 2019) and the patterns by PEP 634 (Bucher and van Rossum, 2020)." % (_S, _D),
 "ReviewQuestions": " The eight questions are the practice questions at the end of the chapter %s." % _S,
 "PracticeQuestions": " The eight questions answered here are the practice questions at the end of the chapter %s, and the code lines are checked by running them." % _S,
 "PracticePrograms": " The chapter's practice programs include the chess dictionary validator and the fantasy game inventory %s." % _S,
}
for _k, _s in _CITE.items(): BODY[_k] = BODY[_k] + _s

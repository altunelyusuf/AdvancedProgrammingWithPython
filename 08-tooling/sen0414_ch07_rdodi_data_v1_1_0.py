"""Chapter 7 content for the RDODI build, version 1.1.0: the research record (sources, findings, claims) of chapter 7 of the 3rd edition.

1.1.0 renews the research record at the standard of chapter 1. The sources, concepts, findings and claims are those that
sen0414_ch07_rdodi_data_v1_0_0.py recorded (that file is not edited; it is imported, so that the record has one source); what changes is the
run: the date (2026-10-08), the interpreter (Python 3.14.6, the one the corpus and the deck ran under), the title and the competency
questions, which are those of sen0414_ch07_corpus_v1_0_0.py. The taxonomy (TAX, BODY) that the old module carried is not used by the
chapter's ontology any more: sen0414_chapter_build_v1_0_0.py writes the domain ontology and the document from the corpus.
Every behaviour quoted was executed (python3.14 sen0414_ch07_corpus_v1_0_0.py python3.14)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0414_ch07_rdodi_data_v1_0_0 import *   # noqa: F401,F403  (PUBS, CONCEPTS, FINDINGS, TAX, BODY, BEH, CLAIMS and the others)
__version__ = "1.1.0"
DATE = "2026-10-08"
PYVER = "3.14.6"
TITLE = "Dictionaries and structuring data for an advanced course: chapter 7 of the 3rd edition and today's Python"
CQS = ("Which operations read, add, replace and remove the pairs of a dictionary, and what decides which of them a given problem calls for?",
       "Which values may be keys, why must they be hashable, and which behaviours of the chapter's text differ in current Python (insertion order, the unhashable message, merge operators)?",
       "How are counting, grouping and nesting solved with dictionaries, and when does each of the setdefault, Counter and defaultdict tools fit best?",
       "How is a real thing modelled as a data structure, as the chessboard simulator does, and how is the structure displayed, copied and written down as text?",
       "Which terms does the chapter use that a learner would have to look up, and which concept of the corpus explains each one?")

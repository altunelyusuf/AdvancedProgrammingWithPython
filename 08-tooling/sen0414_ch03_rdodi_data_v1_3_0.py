"""Chapter 3 content for the RDODI build, version 1.3.0: aligns the data module with the corpus ontology of chapter 3 (2026-10-25), the retrofit of Iteration 19.

Root cause, measured: the committed ontology files v1_1_0 of chapter 3 (TBox, ABox) were written by sen0414_chapter_build_v1_0_0.py from the corpus
(sen0414_ch03_corpus_v1_0_0.py), not from this family of data modules, whose TAX and BODY (1.0.0) describe the older, smaller taxonomy; so
sen0414_rdodi_checks, which compares a data module with the ontology files of the same version, finds no data module of chapter 3 with its ontology files.
This version takes TAX and BODY from the corpus (the same transformation as sen0414_ch05_rdodi_data_v1_3_0.py, sen0414_ch02_rdodi_data_v1_3_0.py and sen0414_ch07_rdodi_data_v1_3_0.py).
Sources, concepts and findings are those of the committed research file v1_2_0 (19 sources, 34 concepts, 5 findings), taken from that file without change (1.0.0 holds only P01-P12 and F1-F4).
The executed claims and behaviours are those of 1.0.0 together with those expressions of the corpus CHECKS that run without the corpus helpers (the others run the corpus programs in separate processes and are executed by the corpus itself), all executed again by the execution checks.
Nothing is removed, and no fact is added that the corpus text does not carry. What the generic builder (1.2.0) cannot write (the error conditions, the third competency question,
the hasOwner links, the per-source verification times) is restored from the v1_1_0 / v1_2_0 files by sen0414_ch03_restore_v1_3_0.py. v1_0_0 and the v1_1_0 / v1_2_0 files are committed and are not edited."""
import os, sys, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0414_ch03_rdodi_data_v1_0_0 import *   # noqa: F401,F403
__version__ = "1.3.0"
DATE = "2026-10-25"
_here = os.path.dirname(os.path.abspath(__file__))
_sp = importlib.util.spec_from_file_location("ch03_corpus", os.path.join(_here, "sen0414_ch03_corpus_v1_0_0.py")); _C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_C)
_byid = {n[0]: n for n in _C.NODES}
def _top(i):
    while _byid[i][3]: i = _byid[i][3]
    return i
TAX = [(_top(n[0]), n[3], n[0], n[4][0], n[4][1], n[4][2]) for n in _C.NODES if n[2] == 3]
class _Body(str):
    """A section text whose paragraphs are joined by a blank line; the text writes itself with the line breaks escaped (\\n) so that the builder's Turtle string stays on one line."""
    def replace(self, old, new): return _Body(str.replace(self, old, new))
    def __str__(self): return str.replace(str.__str__(self), "\n", "\\n")
    __format__ = lambda self, spec: str(self)
BODY = {n[0]: _Body(_C.facet_text(n[5])) for n in _C.NODES}
# Where the committed document v1_2_0 differs from the corpus text, the text of the old document is kept, so that no paragraph and no citation of it is dropped.
import rdflib
_og = rdflib.Graph().parse(os.path.join(_here, "..", "03-materials", "ch03", "rdodi", "sen0414_ch03_document_v1_2_0.ttl"))
for _s, _d in _og.subject_objects(rdflib.SKOS.definition):
    _k = str(_s).rsplit("#", 1)[1]
    if _k.startswith("S_") and _k[2:] in BODY and str(_d) != str.__str__(BODY[_k[2:]]):
        BODY[_k[2:]] = _Body(str(_d))
# The expressions the corpus texts quote that need no corpus helper (each with its expected representation) are executed in addition to the claims of 1.0.0.
_HELP = ("run(", "rc(", "err(", "msg(", "stuck(", "warnline(", "clash(", "pathfirst(", "PG[")
CLAIMS = list(CLAIMS) + [(c[0], c[1]) for c in _C.CHECKS if len(c) == 2 and (c[0], c[1]) not in CLAIMS and not any(h in c[0] for h in _HELP)]

# ---- the sources, concepts and findings of the research file v1_2_0 (19 sources, 34 concepts, 5 findings), taken from that file without change ----
PUBS = [('P01', 'Automate the Boring Stuff with Python, 3rd edition - Chapter 3, Loops (Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/chapter3.html', True),
 ('P02',
  'The Python Tutorial, 4. More Control Flow Tools - for, range(), break and continue, else clauses on loops (Python Software Foundation, 2026)',
  'https://docs.python.org/3/tutorial/controlflow.html',
  False),
 ('P03',
  'The Python Language Reference, 8. Compound statements - the while and for statements (Python Software Foundation, 2026)',
  'https://docs.python.org/3/reference/compound_stmts.html',
  False),
 ('P04',
  'The Python Standard Library, Built-in Functions - range, enumerate and zip (Python Software Foundation, 2026)',
  'https://docs.python.org/3/library/functions.html',
  False),
 ('P05', 'The Python Standard Library, sys - sys.exit (Python Software Foundation, 2026)', 'https://docs.python.org/3/library/sys.html', False),
 ('P06',
  'The Python Standard Library, Built-in Exceptions - KeyboardInterrupt (Python Software Foundation, 2026)',
  'https://docs.python.org/3/library/exceptions.html',
  False),
 ('P07',
  'The Python Tutorial, 5. Data Structures - Looping Techniques (Python Software Foundation, 2026)',
  'https://docs.python.org/3/tutorial/datastructures.html',
  False),
 ('P08', 'PEP 572 - Assignment Expressions (Angelico, Peters and Van Rossum, 2018; Angelico et al., 2018; Python 3.8)', 'https://peps.python.org/pep-0572/', False),
 ('P09', 'PEP 618 - Add Optional Length-Checking To zip (Bucher, 2020; Python 3.10)', 'https://peps.python.org/pep-0618/', False),
 ('P10', 'PEP 765 - Disallow return/break/continue that exit a finally block (Katriel and Coghlan, 2024; Python 3.14)', 'https://peps.python.org/pep-0765/', False),
 ('P11', "What's New In Python 3.14 - PEP 765: Control flow in finally blocks (Python Software Foundation, 2026)", 'https://docs.python.org/3/whatsnew/3.14.html', False),
 ('P12', 'PEP 8 - Style Guide for Python Code (Van Rossum, Warsaw and Coghlan, 2001; Van Rossum et al., 2001)', 'https://peps.python.org/pep-0008/', False),
 ('P13',
  'The Python Tutorial, 6. Modules - import forms, the module search path, __name__ and dir() (Python Software Foundation, 2026)',
  'https://docs.python.org/3/tutorial/modules.html',
  False),
 ('P14',
  'The Python Tutorial, 8. Errors and Exceptions - handling exceptions, try and finally, raising SystemExit and KeyboardInterrupt (Python Software Foundation, 2026)',
  'https://docs.python.org/3/tutorial/errors.html',
  False),
 ('P15',
  'The Python Language Reference, 7. Simple statements - break, continue, return and import (Python Software Foundation, 2026)',
  'https://docs.python.org/3/reference/simple_stmts.html',
  False),
 ('P16',
  'The Python Language Reference, 5. The import system - sys.modules and the module search path (Python Software Foundation, 2026)',
  'https://docs.python.org/3/reference/import.html',
  False),
 ('P17',
  'The Python Standard Library, random - Generate pseudo-random numbers (Python Software Foundation, 2026)',
  'https://docs.python.org/3/library/random.html',
  False),
 ('P18',
  'The Python Standard Library, Built-in Types - sequence types, ranges, tuples, lists and dictionaries (Python Software Foundation, 2026)',
  'https://docs.python.org/3/library/stdtypes.html',
  False),
 ('P19',
  'Glossary - iterable, iterator, sequence, module, namespace, attribute, hashable, mapping and related terms (Python Software Foundation, 2026)',
  'https://docs.python.org/3/glossary.html',
  False)]
CONCEPTS = [('Section', 'while Loop Statements'),
 ('Section', 'for Loops and the range() Function'),
 ('Section', 'Importing Modules'),
 ('Section', 'Ending a Program Early with sys.exit()'),
 ('Section', 'A Short Program: Guess the Number'),
 ('Section', 'A Short Program: Rock, Paper, Scissors'),
 ('Section', 'Summary'),
 ('Section', 'Practice Questions'),
 ('Concept', 'Loop'),
 ('Concept', 'Sequence to iterate'),
 ('Concept', 'Early exit'),
 ('Statement', 'while'),
 ('Statement', 'for'),
 ('Statement', 'break'),
 ('Statement', 'continue'),
 ('Function', 'range()'),
 ('Term used without definition', 'Iteration'),
 ('Term used without definition', 'Iterable'),
 ('Term used without definition', 'Iterator'),
 ('Term used without definition', 'Sequence'),
 ('Term used without definition', 'Half-open interval'),
 ('Term used without definition', 'Accumulator'),
 ('Term used without definition', 'Loop variable'),
 ('Term used without definition', 'Sequence unpacking'),
 ('Term used without definition', 'Tuple'),
 ('Term used without definition', 'List'),
 ('Term used without definition', 'Dictionary'),
 ('Term used without definition', 'Exception'),
 ('Term used without definition', 'Exit status'),
 ('Term used without definition', 'SyntaxWarning'),
 ('Term used without definition', 'Module'),
 ('Term used without definition', 'Namespace'),
 ('Term used without definition', 'Module search path'),
 ('Term used without definition', 'Assignment expression')]
FINDINGS = [('F1',
  'Background',
  'Chapter 3 of the 3rd edition teaches repetition with the while statement, which repeats a block as long as its condition is true, and the for statement with the '
  'range() function, which repeats it a counted number of times; break leaves a loop early and continue jumps back to its start. It then shows how to import modules, '
  'how sys.exit() ends a program, and two short programs, Guess the Number and Rock, Paper, Scissors.',
  ['P01']),
 ('F2',
  'Contemporary developments',
  "Python 3.8 added assignment expressions, so a loop can test and name a value in one line - while chunk := file.read(8192): is the PEP's own example of a loop that "
  'cannot be trivially rewritten with the two-argument form of iter(). Python 3.10 added an optional strict argument to zip that raises ValueError when the iterables '
  'differ in length. Python 3.14 makes the compiler emit a SyntaxWarning when a return, break or continue leaves a finally block.',
  ['P08', 'P09', 'P10', 'P11']),
 ('F3',
  'Comparative analysis',
  'The reference documentation makes precise what the chapter leaves informal: a for statement evaluates its iterable once and iterates over an iterator made from it; '
  "range() returns an immutable arithmetic sequence that generates its values on demand rather than a list; a loop's else clause runs when the loop finishes without a "
  'break; the loop variable is overwritten on each pass and is not deleted when the loop ends; and code that modifies a collection while iterating over it is tricky, so '
  'the tutorial advises looping over a copy. enumerate() replaces range(len(a)) when both index and item are needed. sys.exit() raises SystemExit, so finally clauses '
  "still run. PEP 8 advises against wildcard imports, which agrees with the chapter, and advises imports on separate lines, which the chapter's import random, sys, os, "
  "math does not follow. The chapter's practice question on stopping a program stuck in an infinite loop is answered by the KeyboardInterrupt entry: Control-C.",
  ['P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P12']),
 ('F4',
  'Conclusion',
  'For an advanced course, chapter 3 is best taught as the iteration protocol seen from the loop: a for loop consumes an iterable, range() is one lazy sequence among '
  'many, enumerate() and zip() are the idioms that replace index arithmetic, the loop else and the assignment expression are the two features that shorten common loops, '
  "and the chapter's while-True-with-break pattern is the one to compare them against.",
  ['P02', 'P04', 'P08']),
 ('F5',
  'Terms used without definition',
  'The chapter text relies on a number of terms that it never defines: iteration, iterable, iterator, sequence, half-open interval, accumulator, loop variable, '
  "unpacking, tuple, list, dictionary, exception, exit status, module, namespace, the module search path and the assignment expression. Python's glossary defines "
  'iterable, iterator, sequence, module, namespace, attribute, hashable, mapping, list and dictionary, the tutorial on modules defines the import forms and the search '
  'path, the tutorial on errors defines handling an exception and the finally clause, the reference on the import system defines sys.modules, and the library '
  'documentation of the standard types defines ranges, tuples, lists and dictionaries. Version 1.1.0 of the domain ontology adds a concept for each of these terms and '
  "explains it before the book's programs use it.",
  ['P13', 'P14', 'P15', 'P16', 'P17', 'P18', 'P19'])]

"""Chapter 4 content for the RDODI build, version 1.3.0: aligns the data module with the corpus ontology of chapter 4 (2026-10-25), the retrofit of Iteration 19.

Root cause, measured: the committed ontology files v1_1_0 of chapter 4 (TBox, ABox, document) were written by sen0414_chapter_build_v1_0_0.py from the corpus
(sen0414_ch04_corpus_v1_0_0.py), not from this family of data modules, whose TAX and BODY (1.0.0) describe the older, smaller taxonomy; so
sen0414_rdodi_checks, which compares a data module with the ontology files of the same version, finds no data module of chapter 4 with its ontology files.
This version takes TAX and BODY from the corpus (the same transformation as sen0414_ch05_rdodi_data_v1_3_0.py, sen0414_ch02_rdodi_data_v1_3_0.py and sen0414_ch07_rdodi_data_v1_3_0.py).
Sources, concepts and findings are those of the committed research file v1_1_0 (31 sources, 37 concepts, 9 findings), taken from that file without change (1.0.0 holds only P01-P16 and F1-F8).
The executed claims and behaviours are those of 1.0.0 together with the claims the corpus states (its CHECKS), all executed again by the execution checks.
Nothing is removed, and no fact is added that the corpus text does not carry. What the generic builder (1.2.0) cannot write (the error conditions, the third competency question,
the hasOwner links, the per-source verification times) is restored from the v1_1_0 files by sen0414_ch04_restore_v1_3_0.py. v1_0_0 and the v1_1_0 files are committed and are not edited."""
import os, sys, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0414_ch04_rdodi_data_v1_0_0 import *   # noqa: F401,F403
__version__ = "1.3.0"
DATE = "2026-10-25"
_here = os.path.dirname(os.path.abspath(__file__))
_sp = importlib.util.spec_from_file_location("ch04_corpus", os.path.join(_here, "sen0414_ch04_corpus_v1_0_0.py")); _C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_C)
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
_og = rdflib.Graph().parse(os.path.join(_here, "..", "03-materials", "ch04", "rdodi", "sen0414_ch04_document_v1_2_0.ttl"))
for _s, _d in _og.subject_objects(rdflib.SKOS.definition):
    _k = str(_s).rsplit("#", 1)[1]
    if _k.startswith("S_") and _k[2:] in BODY and str(_d) != str.__str__(BODY[_k[2:]]):
        BODY[_k[2:]] = _Body(str(_d))
# The expressions the corpus texts quote (the corpus CHECKS, each with its expected representation) are executed in addition to the claims of 1.0.0.
CLAIMS = list(CLAIMS) + [(c[0], c[1]) for c in _C.CHECKS if len(c) == 2 and (c[0], c[1]) not in CLAIMS]

# ---- the sources, concepts and findings of the research file v1_1_0 (31 sources, 37 concepts, 9 findings), taken from that file without change ----
PUBS = [('P01',
  'Automate the Boring Stuff with Python, 3rd edition - Chapter 4, Functions (Al Sweigart, No Starch Press, 2025)',
  'https://automatetheboringstuff.com/3e/chapter4.html',
  True),
 ('P02',
  'The Python Tutorial, 4. More Control Flow Tools - defining functions, default argument values, keyword arguments, special parameters (Python 3.14.4 documentation source)',
  'https://docs.python.org/3/tutorial/controlflow.html',
  False),
 ('P03',
  'The Python Language Reference, 4. Execution model - naming and binding, resolution of names (Python 3.14.4 documentation source)',
  'https://docs.python.org/3/reference/executionmodel.html',
  False),
 ('P04',
  'Python Frequently Asked Questions, Programming FAQ - Why am I getting an UnboundLocalError (Python 3.14.4 documentation source)',
  'https://docs.python.org/3/faq/programming.html',
  False),
 ('P05',
  'The Python Language Reference, 7. Simple statements - return, global and nonlocal (Python 3.14.4 documentation source)',
  'https://docs.python.org/3/reference/simple_stmts.html',
  False),
 ('P06', 'The Python Standard Library, sys - getrecursionlimit (Python 3.14.4 documentation source)', 'https://docs.python.org/3/library/sys.html', False),
 ('P07', 'The Python Standard Library, Built-in Functions - print (Python 3.14.4 documentation source)', 'https://docs.python.org/3/library/functions.html', False),
 ('P08',
  'The Python Standard Library, Built-in Exceptions - UnboundLocalError, RecursionError, ZeroDivisionError (Python 3.14.4 documentation source)',
  'https://docs.python.org/3/library/exceptions.html',
  False),
 ('P09', 'The Python Tutorial, 8. Errors and Exceptions - handling exceptions (Python 3.14.4 documentation source)', 'https://docs.python.org/3/tutorial/errors.html', False),
 ('P10',
  "What's New In Python 3.14 - PEP 649 and PEP 749 deferred annotations, PEP 758 except without brackets (Python documentation source)",
  'https://docs.python.org/3/whatsnew/3.14.html',
  False),
 ('P11', 'PEP 649 - Deferred Evaluation Of Annotations Using Descriptors (Hastings, 2021; Python 3.14)', 'https://peps.python.org/pep-0649/', False),
 ('P12', 'PEP 758 - Allow except and except* expressions without parentheses (Galindo Salgado and Cannon, 2024; Python 3.14)', 'https://peps.python.org/pep-0758/', False),
 ('P13', 'PEP 570 - Python Positional-Only Parameters (Hastings et al., 2018; Python 3.8)', 'https://peps.python.org/pep-0570/', False),
 ('P14', 'PEP 3102 - Keyword-Only Arguments (Talin, 2006; Python 3.0)', 'https://peps.python.org/pep-3102/', False),
 ('P15', 'PEP 3104 - Access to Names in Outer Scopes (Yee, 2006; Python 3.0)', 'https://peps.python.org/pep-3104/', False),
 ('P16', 'PEP 8 - Style Guide for Python Code (van Rossum, Warsaw and Coghlan, 2001)', 'https://peps.python.org/pep-0008/', False),
 ('P17', 'Glossary (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/glossary.html', False),
 ('P18',
  'The Python Language Reference, 8. Compound statements - function definitions, the try statement, lambda (Python 3.14.8 documentation, Python Software Foundation, 2026)',
  'https://docs.python.org/3/reference/compound_stmts.html',
  False),
 ('P19',
  'The Python Language Reference, 6. Expressions - calls, lambda, comparisons (Python 3.14.8 documentation, Python Software Foundation, 2026)',
  'https://docs.python.org/3/reference/expressions.html',
  False),
 ('P20',
  'The Python Language Reference, 3. Data model - function objects, frame objects, NoneType (Python 3.14.8 documentation, Python Software Foundation, 2026)',
  'https://docs.python.org/3/reference/datamodel.html',
  False),
 ('P21',
  'The Python Standard Library, traceback - Print or retrieve a stack traceback (Python 3.14.8 documentation, Python Software Foundation, 2026)',
  'https://docs.python.org/3/library/traceback.html',
  False),
 ('P22',
  'The Python Standard Library, inspect - Inspect live objects (Python 3.14.8 documentation, Python Software Foundation, 2026)',
  'https://docs.python.org/3/library/inspect.html',
  False),
 ('P23',
  "The Python Standard Library, symtable - Access to the compiler's symbol tables (Python 3.14.8 documentation, Python Software Foundation, 2026)",
  'https://docs.python.org/3/library/symtable.html',
  False),
 ('P24',
  'The Python Standard Library, time - Time access and conversions (Python 3.14.8 documentation, Python Software Foundation, 2026)',
  'https://docs.python.org/3/library/time.html',
  False),
 ('P25',
  'The Python Standard Library, random - Generate pseudo-random numbers (Python 3.14.8 documentation, Python Software Foundation, 2026)',
  'https://docs.python.org/3/library/random.html',
  False),
 ('P26',
  'The Python Standard Library, keyword - Testing for Python keywords (Python 3.14.8 documentation, Python Software Foundation, 2026)',
  'https://docs.python.org/3/library/keyword.html',
  False),
 ('P27',
  'The Python Standard Library, Built-in Constants (Python 3.14.8 documentation, Python Software Foundation, 2026)',
  'https://docs.python.org/3/library/constants.html',
  False),
 ('P28',
  'The Python Standard Library, annotationlib - Functionality for introspecting annotations (Python 3.14.8 documentation, Python Software Foundation, 2026)',
  'https://docs.python.org/3/library/annotationlib.html',
  False),
 ('P29',
  'The Python Tutorial, 3. An Informal Introduction to Python - comments (Python 3.14.8 documentation, Python Software Foundation, 2026)',
  'https://docs.python.org/3/tutorial/introduction.html',
  False),
 ('P30', 'PEP 3107 - Function Annotations (Winter and Lownds, 2006; Python 3.0)', 'https://peps.python.org/pep-3107/', False),
 ('P31', 'PEP 8 - Style Guide for Python Code, the sections on comments and on function names (Van Rossum et al., 2001)', 'https://peps.python.org/pep-0008/', False)]
CONCEPTS = [('Section', 'Creating Functions'),
 ('Section', 'Arguments and Parameters'),
 ('Section', 'Return Values and return Statements'),
 ('Section', 'The None Value'),
 ('Section', 'Named Parameters'),
 ('Section', 'The Call Stack'),
 ('Section', 'Local and Global Scopes'),
 ('Section', 'Scope Rules'),
 ('Section', 'The global Statement'),
 ('Section', 'Scope Identification'),
 ('Section', 'Exception Handling'),
 ('Section', 'A Short Program: Zigzag'),
 ('Section', 'A Short Program: Spike'),
 ('Section', 'Summary'),
 ('Section', 'Practice Questions'),
 ('Concept', 'function'),
 ('Concept', 'function call'),
 ('Concept', 'deduplication'),
 ('Concept', 'argument'),
 ('Concept', 'parameter'),
 ('Concept', 'return value'),
 ('Concept', 'call stack'),
 ('Concept', 'frame object'),
 ('Concept', 'local scope'),
 ('Concept', 'global scope'),
 ('Concept', 'black box'),
 ('Concept', 'exception'),
 ('Concept', 'traceback'),
 ('Statement', 'def'),
 ('Statement', 'return'),
 ('Statement', 'global'),
 ('Statement', 'try'),
 ('Statement', 'except'),
 ('Value', 'None'),
 ('Function', 'print()'),
 ('Function', 'input()'),
 ('Function', 'len()')]
FINDINGS = [('F1',
  'Background',
  'Chapter 4 of the 3rd edition teaches functions: the def statement that defines one and the call that runs it, arguments passed into parameters, return values and the None '
  "value, named parameters such as print's sep and end, the call stack that remembers where each call returns to, the local and the global scope and four rules for telling them "
  'apart, the global statement, and try and except for recovering from an error, closing with two short animation programs.',
  ['P01']),
 ('F2',
  'Comparative analysis',
  "One printed output of the chapter has changed: it shows UnboundLocalError: local variable 'eggs' referenced before assignment, while Python 3.14.4 says cannot access local "
  "variable 'eggs' where it is not associated with a value, the wording the Programming FAQ now prints; the class, its parent NameError and the cause are unchanged, and the "
  "chapter's other printed error messages, NameError and ZeroDivisionError, are the same under 3.14.4.",
  ['P01', 'P04', 'P08']),
 ('F3',
  'Comparative analysis',
  "The chapter's copy-and-paste listing, which it shows to argue for functions, is not equivalent to the function version it stands for: its last line is print(' Good evening!') "
  'with a leading space, so running the two programs gives outputs that differ in exactly that line - which is the maintenance hazard of duplicated code the passage warns about.',
  ['P01']),
 ('F4',
  'Comparative analysis',
  "The reference documentation explains why the chapter's fourth scope rule and its UnboundLocalError follow from one fact: which names are local is decided by scanning the whole "
  "function body for name-binding operations, so an assignment anywhere in a function makes the name local everywhere in it; the standard library's symtable module shows the "
  'decision - the same name eggs is global in a function with a global statement, local in one that assigns it, and global in one that only reads it.',
  ['P03', 'P04', 'P05']),
 ('F5',
  'Contemporary developments',
  "Beyond the chapter, a function's parameters can be positional-only, with a slash, or keyword-only, with a star, and calling them the wrong way raises a TypeError that names "
  "the problem; a default argument value is evaluated once, so a mutable default such as an empty list is shared between calls and the tutorial's remedy is a default of None; and "
  'nonlocal lets an inner function rebind a name of the enclosing function, the middle case between local and global that the chapter does not cover.',
  ['P02', 'P05', 'P13', 'P14', 'P15']),
 ('F6',
  'Contemporary developments',
  'Python 3.14 changed two things a course on functions meets: annotations on a function are no longer evaluated when it is defined, so a function annotated with names that do '
  'not exist yet can be defined and called, and reading its annotations raises NameError until they are evaluated on request; and except may list several exception types without '
  'brackets when no as clause is used, which 3.13 and earlier reject.',
  ['P10', 'P11', 'P12']),
 ('F7',
  'Comparative analysis',
  "The chapter's call-stack example reproduces line for line, and the stack itself can be looked at from the program: the standard library's traceback module lists the frames a "
  'call is running inside, and the interpreter refuses to grow the stack without end - the recursion limit is 1000 and a function that calls itself forever raises RecursionError, '
  'a subclass of RuntimeError, rather than crashing.',
  ['P01', 'P06', 'P08']),
 ('F8',
  'Conclusion',
  'For an advanced course, chapter 4 is best taught as name resolution seen from the function: a call creates a scope, the compiler decides which names in it are local, the call '
  "stack holds the scopes that are waiting, and try and except decide where in that stack an error is handled; the book's rules are the four cases of one lookup rule, the printed "
  'messages should be regenerated under the Python in use, and parameters, defaults, nonlocal, annotations and the 3.14 except syntax are what the chapter leaves for the course '
  'to add.',
  ['P01', 'P03', 'P10']),
 ('F9',
  'Terms used without definition',
  'The chapter text names tools and ideas that the earlier corpus did not explain: reserved keywords, the lambda expression, the nested function, the function taken from a '
  'module, the positional argument, the frame object and stack inspection, recursion, namespaces and the lookup of names, the symbol table, the nonlocal statement, the exception '
  'object, the traceback, the exception hierarchy, the time.sleep function, the KeyboardInterrupt exception, the sys.exit function, the two practice programs, function '
  'annotations, function naming and comments. The Python glossary defines the namespace, the nested scope, the lambda, the keyword argument and the positional argument; the '
  'language reference gives the function definition, the try statement and the lambda expression, the call, and the function object, the frame object and NoneType; the library '
  'documentation covers traceback, inspect, symtable, time, random, keyword, the constant None and annotationlib; the tutorial introduction defines the comment; PEP 3107 defines '
  'function annotations and PEP 8 gives the conventions for names and comments. Every output and error message quoted was executed under Python 3.12.11 and 3.14.4, and the '
  'messages that differ between releases - division by zero, the empty range of randint, the unexpected keyword of print, the except clause without brackets, deferred annotations '
  'and the annotation blocks in the symbol table - are pinned to their release in the corpus and never quoted as stable. Two statements of the chapter do not hold when run: its '
  'hint to print the Collatz values with sep puts each value on its own line, and its claim that the sequence reaches 1 for any integer fails for 0 and for -1.',
  ['P01', 'P17', 'P18', 'P19', 'P20', 'P21', 'P22', 'P23', 'P24', 'P25', 'P26', 'P27', 'P28', 'P29', 'P30', 'P31'])]

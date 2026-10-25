"""Chapter 1 content for the RDODI build, version 1.3.0: a data module for chapter 1, written from the corpus (2026-10-25), the retrofit of Iteration 19.

Root cause, measured: chapter 1 was built by its own three builders (sen0414_ch01_domain_build_v1_2_0.py, sen0414_ch01_document_build_v1_2_0.py and the research
written by hand) from the corpus sen0414_ch01_corpus_v1_2_0.py, and no data module of the generic family exists for it; so sen0414_rdodi_checks, which compares a data module with
the ontology files of the same version, finds no data module of chapter 1 with its ontology files.
This module takes TAX and BODY from the corpus v1_2_0 (51 concepts, among them the branches ExecutionEnvironment and ModernPractice), the same transformation as
sen0414_ch04_rdodi_data_v1_3_0.py, sen0414_ch05_rdodi_data_v1_3_0.py, sen0414_ch02_rdodi_data_v1_3_0.py and sen0414_ch07_rdodi_data_v1_3_0.py.
Sources, concepts and findings are those of the committed research file v1_1_0 (25 sources, 27 concepts, 5 findings), taken from that file without change.
The executed claims are the corpus CHECKS (41 expressions with their expected representation) and the corpus RAISES (10 expressions with the error class they raise),
all executed again by the execution checks. Nothing is removed, and no fact is added that the corpus text does not carry. What the generic builder (1.2.0) cannot write
(the error conditions, the third competency question, the hasOwner links, the individual names and extra properties of the research file, the per-source verification times)
is restored from the v1_1_x and v1_2_0 files by sen0414_ch01_restore_v1_3_0.py. The v1_1_x and v1_2_0 files are committed and are not edited."""
import os, sys, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
__version__ = "1.3.0"
CH = 1
DATE = "2026-10-25"
PYVER = "3.14.4"
TITLE = "Python basics for an advanced course: chapter 1 of the 3rd edition and the Python students now run"
QUESTION = "What does chapter 1 of the 3rd edition teach, and what must an advanced course add so that it matches the Python students will run in 2026?"
ERRORS = []
_here = os.path.dirname(os.path.abspath(__file__))
_sp = importlib.util.spec_from_file_location("ch01_corpus", os.path.join(_here, "sen0414_ch01_corpus_v1_2_0.py")); _C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_C)
CQS = tuple(_C.CQS[:2])
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
_og = rdflib.Graph().parse(os.path.join(_here, "..", "03-materials", "ch01", "rdodi", "sen0414_ch01_document_v1_2_0.ttl"))
for _s, _d in _og.subject_objects(rdflib.SKOS.definition):
    _k = str(_s).rsplit("#", 1)[1]
    if _k.startswith("S_") and _k[2:] in BODY and str(_d) != str.__str__(BODY[_k[2:]]):
        BODY[_k[2:]] = _Body(str(_d))
# The expressions the corpus texts quote (CHECKS, each with its expected representation) are executed; the expressions that must raise (RAISES) are executed as behaviours.
CLAIMS = [(c[0], c[1]) for c in _C.CHECKS]
BEH = [("%s raises %s" % (e, x), "try:\n    exec(%r)\nexcept BaseException as ex:\n    print(type(ex).__name__)" % e, x) for e, x in _C.RAISES]

# ---- the sources, concepts and findings of the research file v1_1_0 (25 sources, 27 concepts, 5 findings), taken from that file without change ----
PUBS = [('P01',
  'Automate the Boring Stuff with Python, 3rd edition - Chapter 1, Python Basics (Al Sweigart, No Starch Press, 2025)',
  'https://automatetheboringstuff.com/3e/chapter1.html',
  True),
 ('P02', 'The Python Tutorial, 3. An Informal Introduction to Python (Python 3.14.7 documentation)', 'https://docs.python.org/3/tutorial/introduction.html', False),
 ('P03', 'The Python Language Reference, 6. Expressions (Python 3.14.7 documentation)', 'https://docs.python.org/3/reference/expressions.html', False),
 ('P04',
  'The Python Tutorial, 15. Floating-Point Arithmetic: Issues and Limitations (Python 3.14.7 documentation)',
  'https://docs.python.org/3/tutorial/floatingpoint.html',
  False),
 ('P05', 'The Python Standard Library, Built-in Types (Python 3.14.7 documentation)', 'https://docs.python.org/3/library/stdtypes.html', False),
 ('P06', 'The Python Standard Library, Built-in Functions (Python 3.14.7 documentation)', 'https://docs.python.org/3/library/functions.html', False),
 ('P07', "What's New In Python 3.13 (Python documentation)", 'https://docs.python.org/3/whatsnew/3.13.html', False),
 ('P08', "What's new in Python 3.14 (Python documentation)", 'https://docs.python.org/3/whatsnew/3.14.html', False),
 ('P09', 'PEP 8 - Style Guide for Python Code', 'https://peps.python.org/pep-0008/', False),
 ('P10', 'PEP 701 - Syntactic formalization of f-strings', 'https://peps.python.org/pep-0701/', False),
 ('P11', 'PEP 20 - The Zen of Python', 'https://peps.python.org/pep-0020/', False),
 ('P12', "Python Developer's Guide - Status of Python versions", 'https://devguide.python.org/versions/', False),
 ('P13', '2025 Stack Overflow Developer Survey', 'https://survey.stackoverflow.co/2025/', False),
 ('P14', 'TIOBE Index', 'https://www.tiobe.com/tiobe-index/', False),
 ('P15', 'Glossary (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/glossary.html', False),
 ('P16',
  'The Python Tutorial, 2. Using the Python Interpreter (Python 3.14.8 documentation, Python Software Foundation, 2026)',
  'https://docs.python.org/3/tutorial/interpreter.html',
  False),
 ('P17',
  'Python support for free threading (Python 3.14.8 documentation, Python Software Foundation, 2026)',
  'https://docs.python.org/3/howto/free-threading-python.html',
  False),
 ('P18', 'PEP 1 - PEP Purpose and Guidelines (Warsaw, Hylton, Goodger and Coghlan, 2000)', 'https://peps.python.org/pep-0001/', False),
 ('P19', 'PEP 703 - Making the Global Interpreter Lock Optional in CPython (Gross, 2023)', 'https://peps.python.org/pep-0703/', False),
 ('P20', 'PEP 779 - Criteria for supported status for free-threaded Python (Wouters, Page and Gross, 2025)', 'https://peps.python.org/pep-0779/', False),
 ('P21', 'uv documentation (Astral, 2026)', 'https://docs.astral.sh/uv/', False),
 ('P22',
  'The Python Tutorial, 12. Virtual Environments and Packages (Python 3.14.8 documentation, Python Software Foundation, 2026)',
  'https://docs.python.org/3/tutorial/venv.html',
  False),
 ('P23',
  'threading - Thread-based parallelism (Python 3.14.8 documentation, Python Software Foundation, 2026)',
  'https://docs.python.org/3/library/threading.html',
  False),
 ('P24',
  'The Python Tutorial, 7. Input and Output (Python 3.14.8 documentation, Python Software Foundation, 2026)',
  'https://docs.python.org/3/tutorial/inputoutput.html',
  False),
 ('P25',
  'The Python Language Reference, 4. Execution model (Python 3.14.8 documentation, Python Software Foundation, 2026)',
  'https://docs.python.org/3/reference/executionmodel.html',
  False)]
CONCEPTS = [('Section', 'Entering Expressions into the Interactive Shell'),
 ('Section', 'The Integer, Floating-Point, and String Data Types'),
 ('Section', 'String Concatenation and Replication'),
 ('Section', 'Storing Values in Variables'),
 ('Section', 'Your First Program'),
 ('Section', 'Dissecting the Program'),
 ('Section', 'How Computers Store Data with Binary Numbers'),
 ('Concept', 'Expression'),
 ('Concept', 'Operator precedence'),
 ('Concept', 'Data type'),
 ('Concept', 'String concatenation'),
 ('Concept', 'Variable'),
 ('Concept', 'Input as text'),
 ('Built-in function', 'print'),
 ('Built-in function', 'input'),
 ('Built-in function', 'len'),
 ('Built-in function', 'str'),
 ('Built-in function', 'int'),
 ('Built-in function', 'float'),
 ('Operator', '+'),
 ('Operator', '-'),
 ('Operator', '*'),
 ('Operator', '/'),
 ('Operator', '//'),
 ('Operator', '%'),
 ('Operator', '**'),
 ('Operator', '=')]
FINDINGS = [('F1',
  'Background',
  'Chapter 1 of the 3rd edition introduces the interactive shell, expressions and their operators with precedence, the integer, floating-point and string data types, '
  'string concatenation and replication, variables, and a first program using print, input, len, str, int and float; it closes on how computers store data in binary.',
  ['P01']),
 ('F2',
  'Contemporary developments',
  "The Python in students' hands has moved since the book: Python 3.14 is the current bugfix release, first released on 2025-10-07, with 3.13 also in bugfix and 3.15's "
  'first release scheduled for 2026-10-01. Python 3.13 brought a better interactive interpreter, improved error messages, an experimental free-threaded build and an '
  'experimental just-in-time compiler. PEP 701 gave f-strings a formal grammar, making them the natural successor to building strings by concatenation. In the '
  'ecosystem, uv - a Python package manager built in Rust - was the most admired technology tag in the 2025 Stack Overflow survey, at 74 per cent.',
  ['P07', 'P10', 'P12', 'P13']),
 ('F3',
  'Comparative analysis',
  'Where the book stays practical, the reference documentation states what an advanced student should know underneath: Python integers have unlimited precision, while '
  'floating-point numbers are usually implemented as C doubles and carry the representation limits the tutorial documents; the Language Reference tabulates operator '
  "precedence from most to least binding; and PEP 8 fixes the naming conventions the book's variable examples follow informally.",
  ['P03', 'P04', 'P05', 'P09']),
 ('F4',
  'Conclusion',
  "For an advanced course, chapter 1 is best taught as the bridge from the book's basics to the Python students will actually run: the 3.13+ interpreter, f-strings "
  'rather than concatenation, precision and representation as real behaviour rather than trivia, and a first look at the ecosystem - uv for packages, and the '
  "free-threaded build as the preview of the course's multithreading outcome.",
  ['P04', 'P05', 'P07', 'P10', 'P13']),
 ('F5',
  'Terms used without definition',
  'The chapter text named tools and ideas that a learner could not look up in the corpus itself: CPython, the interpreter, bytecode, threads, the global interpreter '
  "lock, Python Enhancement Proposals, packages and virtual environments; and this record's own inventory listed expression, data type and variable (C01_08, C01_10, "
  'C01_12) without the domain ontology carrying them. The Python glossary defines CPython (the canonical implementation, as distributed on python.org), the interpreted '
  'language, the bytecode and its virtual machine, the global interpreter lock, free threading and the free-threaded build, the expression and the statement; PEP 1 '
  'defines a Python Enhancement Proposal; PEPs 703 and 779 give the three phases by which the lock becomes optional; the threading documentation defines the thread; the '
  'tutorial defines the virtual environment; and the uv documentation lists what uv replaces. Each concept section of document 1.1.0 is written from those texts.',
  ['P15', 'P16', 'P17', 'P18', 'P19', 'P20', 'P21', 'P22', 'P23', 'P24', 'P25'])]

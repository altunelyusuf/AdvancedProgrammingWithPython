"""Chapter 2 content for the RDODI build, version 1.3.0: aligns the data module with the corpus ontology of chapter 2 (2026-10-25), the retrofit of Iteration 19.

Root cause, measured: the committed ontology files v1_1_0 of chapter 2 (TBox, ABox, document) were written by sen0414_chapter_build_v1_0_0.py from the corpus
(sen0414_ch02_corpus_v1_0_0.py), not from this family of data modules, whose TAX and BODY (1.0.1) describe the older, smaller taxonomy; so sen0414_rdodi_checks,
which compares a data module with the ontology files of the same version, finds no data module of chapter 2 with its ontology files.
This version takes TAX and BODY from the corpus (the same transformation as sen0414_ch05_rdodi_data_v1_3_0.py, sen0414_ch06_rdodi_data_v2_1_0.py and sen0414_ch07_rdodi_data_v1_3_0.py).
The sources, concepts and findings are those of the committed research file v1_1_0 (22 sources, 25 concepts, 5 findings), taken from that file without change (1.0.1 holds only P01-P10 and F1-F4);
the executed claims and behaviours are those the corpus states (its CHECKS, executed again by the execution checks). Nothing is removed, and no fact is added that the corpus text does not carry.
What the generic builder (1.2.0) cannot write (the error conditions, the third and fourth competency question, the hasOwner links, the per-source verification times) is restored from the
v1_1_0 files by sen0414_ch02_restore_v1_3_0.py. v1_0_1 and the v1_1_0 files are committed and are not edited."""
import os, sys, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
__version__ = "1.3.0"
CH = 2
TITLE = "Flow control for an advanced course: chapter 2 of the 3rd edition and today's Python"
QUESTION = "What does chapter 2 of the 3rd edition teach about Boolean logic and flow control, and what must an advanced course add so that it matches current Python?"
ERRORS = []
_here = os.path.dirname(os.path.abspath(__file__))
_sp = importlib.util.spec_from_file_location("ch02_corpus", os.path.join(_here, "sen0414_ch02_corpus_v1_0_0.py")); _C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_C)
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
_og = rdflib.Graph().parse(os.path.join(_here, "..", "03-materials", "ch02", "rdodi", "sen0414_ch02_document_v1_2_0.ttl"))
for _s, _d in _og.subject_objects(rdflib.SKOS.definition):
    _k = str(_s).rsplit("#", 1)[1]
    if _k.startswith("S_") and _k[2:] in BODY and str(_d) != str.__str__(BODY[_k[2:]]):
        BODY[_k[2:]] = _Body(str(_d))
# The expressions and programs whose output the corpus texts quote (the corpus CHECKS): executed by sen0414_rdodi_checks under CPython 3.14.
CLAIMS = [(c[0], c[1]) for c in _C.CHECKS if len(c) == 2]
BEH = [["corpus program %d" % i, c[0], c[1].strip()] for i, c in enumerate([c for c in _C.CHECKS if len(c) == 3 and c[2] == "program"], 1)] + \
      [["corpus traceback %d" % i, c[0], c[1]] for i, c in enumerate([c for c in _C.CHECKS if len(c) == 3 and c[2] == "traceback"], 1)]

# ---- the sources, concepts and findings of the research file v1_1_0 (22 sources, 25 concepts, 5 findings), taken from that file without change ----
PUBS = [('P01',
  'Automate the Boring Stuff with Python, 3rd edition - Chapter 2, if-else and Flow Control (Al Sweigart, No Starch Press; cited as Sweigart, 2025)',
  'https://automatetheboringstuff.com/3e/chapter2.html',
  True),
 ('P02', 'The Python Tutorial, 4. More Control Flow Tools (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/tutorial/controlflow.html', False),
 ('P03', 'The Python Language Reference, 8. Compound statements (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/reference/compound_stmts.html', False),
 ('P04', 'The Python Language Reference, 6. Expressions (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/reference/expressions.html', False),
 ('P05', 'The Python Standard Library, Built-in Types - Truth Value Testing (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/library/stdtypes.html', False),
 ('P06', 'PEP 634 - Structural Pattern Matching: Specification (Bucher and van Rossum, 2020; Python 3.10)', 'https://peps.python.org/pep-0634/', False),
 ('P07', 'PEP 636 - Structural Pattern Matching: Tutorial (Moisset, 2020)', 'https://peps.python.org/pep-0636/', False),
 ('P08', 'PEP 765 - Disallow return/break/continue that exit a finally block (Katriel and Coghlan, 2024; Python 3.14)', 'https://peps.python.org/pep-0765/', False),
 ('P09', "What's new in Python 3.14 (Python 3.14.8 documentation, Python Software Foundation, 2026)", 'https://docs.python.org/3/whatsnew/3.14.html', False),
 ('P10', 'PEP 8 - Style Guide for Python Code (Van Rossum, Warsaw and Coghlan, 2001; Van Rossum et al., 2001)', 'https://peps.python.org/pep-0008/', False),
 ('P11', 'The Python Language Reference, 2. Lexical analysis (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/reference/lexical_analysis.html', False),
 ('P12', 'Glossary (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/glossary.html', False),
 ('P13', 'The Python Language Reference, 3. Data model (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/reference/datamodel.html', False),
 ('P14', 'The Python Standard Library, Built-in Constants (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/library/constants.html', False),
 ('P15', 'The Python Standard Library, Built-in Functions (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/library/functions.html', False),
 ('P16', 'The Python Language Reference, 7. Simple statements (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/reference/simple_stmts.html', False),
 ('P17', 'The Python Standard Library, Built-in Exceptions (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/library/exceptions.html', False),
 ('P18', 'The Python Tutorial, 8. Errors and Exceptions (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/tutorial/errors.html', False),
 ('P19',
  'The Python Standard Library, sys - System-specific parameters and functions (Python 3.14.8 documentation, Python Software Foundation, 2026)',
  'https://docs.python.org/3/library/sys.html',
  False),
 ('P20', 'The Python Standard Library, keyword - Testing for Python keywords (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/library/keyword.html', False),
 ('P21', "What's New In Python 3.10 (Python 3.14.8 documentation, Python Software Foundation, 2026)", 'https://docs.python.org/3/whatsnew/3.10.html', False),
 ('P22', 'PEP 572 - Assignment Expressions (Angelico, Peters and Van Rossum, 2018; Angelico et al., 2018)', 'https://peps.python.org/pep-0572/', False)]
CONCEPTS = [('Section', 'Boolean Values'),
 ('Section', 'Comparison Operators'),
 ('Section', 'Boolean Operators'),
 ('Section', 'Mixing Boolean and Comparison Operators'),
 ('Section', 'Components of Flow Control'),
 ('Section', 'Flow Control Statements'),
 ('Section', 'A Short Program: Opposite Day'),
 ('Section', 'A Short Program: Dishonest Capacity Calculator'),
 ('Concept', 'Boolean value'),
 ('Concept', 'Comparison operator'),
 ('Concept', 'Boolean operator'),
 ('Concept', 'Block'),
 ('Concept', 'Flow control statement'),
 ('Operator', '=='),
 ('Operator', '!='),
 ('Operator', '<'),
 ('Operator', '>'),
 ('Operator', '<='),
 ('Operator', '>='),
 ('Operator', 'and'),
 ('Operator', 'or'),
 ('Operator', 'not'),
 ('Statement', 'if'),
 ('Statement', 'else'),
 ('Statement', 'elif')]
FINDINGS = [('F1',
  'Background',
  'Chapter 2 of the 3rd edition introduces the Boolean values True and False, the six comparison operators, the Boolean operators and, or and not, how comparison and Boolean operators mix, the '
  'components of flow control - conditions and blocks - and the if, else and elif statements, with two short programs.',
  ['P01']),
 ('F2',
  'Contemporary developments',
  'Python 3.10 added structural pattern matching: a match statement compares a value against successive case patterns, closer to pattern matching than to the switch statement of C or Java. Python '
  '3.14 adopted PEP 765, which disallows return, break and continue that exit a finally block.',
  ['P02', 'P06', 'P08']),
 ('F3',
  'Comparative analysis',
  'The reference documentation makes precise what the chapter leaves informal: and and or return one of their operands rather than a Boolean - x and y returns x if x is false - and evaluate the '
  'second operand only when needed; comparisons chain, so x < y <= z means x < y and y <= z; many values besides False count as false, including None, zero of any numeric type and empty sequences; '
  'the conditional expression x if C else y chooses a value in one line; and PEP 8 advises against comparing Boolean values to True or False with ==.',
  ['P04', 'P05', 'P10']),
 ('F4',
  'Conclusion',
  'For an advanced course, chapter 2 is best taught as decision-making in real Python: truthiness and short-circuit evaluation as working tools, chained comparisons and conditional expressions as '
  'idioms, and the match statement as the modern alternative to long elif chains.',
  ['P04', 'P05', 'P06']),
 ('F5',
  'Terms used without definition',
  'The chapter text named ideas that a learner could not look up in the corpus itself: the None value, containers and their emptiness, identity and the is operator, the order of strings, the arity '
  'of an operator, truth tables, operands and the result of and and or, precedence among not, and and or, keywords and soft keywords, indentation and the clause, the assignment expression, the '
  "wildcard, sequence and guard patterns, singletons, flowcharts, the exception and the traceback; and this record's own inventory listed block, the Boolean operators and the flow control statement "
  '(C_12, C_11, C_13) without the domain ontology carrying their parts. The Python glossary was read for the statement, the suite, the sequence and the singleton; the lexical analysis reference for '
  'indentation, tokens and keywords; the data model for identity and None; the built-in constants and functions for None, True, False and ord; the exceptions documentation and the tutorial chapter '
  "on errors for the exception, the traceback and the error kinds; the sys documentation for sys.exit; the keyword module for hard and soft keywords; the simple statements reference for pass; What's "
  'New in Python 3.10 for the match statement and PEP 572 for the assignment expression. Each concept section of document 1.1.0 is written from those texts, and each of its code claims is executed '
  'under CPython 3.14.4 and 3.12.11.',
  ['P11', 'P12', 'P13', 'P14', 'P15', 'P16', 'P17', 'P18', 'P19', 'P20', 'P21', 'P22'])]

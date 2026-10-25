"""Chapter 5 content for the RDODI build, version 1.3.0: aligns the data module with the corpus ontology of chapter 5 (2026-10-25), the retrofit of Iteration 19.

Root cause, measured: the committed ontology files v1_1_0 of chapter 5 (TBox, ABox, document) were written by sen0414_chapter_build_v1_0_0.py from the corpus
(sen0414_ch05_corpus_v1_0_0.py), not from this family of data modules, whose TAX and BODY (1.0.0) describe the older, smaller taxonomy; so
sen0414_rdodi_checks, which compares a data module with the ontology files of the same version, finds no data module of chapter 5 with its ontology files.
This version takes TAX and BODY from the corpus (the same transformation as sen0414_ch06_rdodi_data_v2_1_0.py and sen0414_ch07_rdodi_data_v1_3_0.py).
Sources, URLs, findings, claims and behaviours are those of 1.0.0 (the behaviours were executed under CPython 3.14.4; the execution checks run them again);
nothing is removed, and no fact is added that the corpus text does not carry. What the generic builder (1.2.0) cannot write (the error conditions, the third
competency question, the hasOwner links) is restored from the v1_1_0 files by sen0414_ch05_restore_v1_3_0.py. v1_0_0 and the v1_1_0 files are committed and are not edited."""
import os, sys, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0414_ch05_rdodi_data_v1_0_0 import *   # noqa: F401,F403
__version__ = "1.3.0"
_here = os.path.dirname(os.path.abspath(__file__))
_sp = importlib.util.spec_from_file_location("ch05_corpus", os.path.join(_here, "sen0414_ch05_corpus_v1_0_0.py")); _C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_C)
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
# The committed document v1_2_0 was repaired on 2026-10-05 (commit bee81f5) after the corpus was written (2026-10-02): the texts of 13 group sections there are longer than the
# corpus text and begin with it, and the text of ExceptionUnwinding carries a citation the corpus text lacks. Where the old document text differs from the corpus text the later, repaired
# text of the old document is kept, so that no paragraph and no citation of it is dropped; elsewhere the corpus text stands.
import rdflib
_og = rdflib.Graph().parse(os.path.join(_here, "..", "03-materials", "ch05", "rdodi", "sen0414_ch05_document_v1_2_0.ttl"))
for _s, _d in _og.subject_objects(rdflib.SKOS.definition):
    _k = str(_s).rsplit("#", 1)[1]
    if _k.startswith("S_") and _k[2:] in BODY and str(_d) != str.__str__(BODY[_k[2:]]):
        BODY[_k[2:]] = _Body(str(_d))

# ---- the sources, concepts and findings of the research file v1_1_0 (27 sources, 40 concepts, 10 findings), taken from that file without change ----
# 1.0.0 holds P01-P15, C_01-C_27 and F1-F8; the committed research v1_1_0 adds P16-P27, C_28-C_40, F9 and F10 and the wording of the labels; they are carried here so that the rebuilt research file drops nothing.
PUBS = [('P01', 'Automate the Boring Stuff with Python, 3rd edition - Chapter 5, Debugging (Sweigart, 2025; No Starch Press)', 'https://automatetheboringstuff.com/3e/chapter5.html', True),
 ('P02', 'The Python Language Reference, 7. Simple statements - the raise and assert statements (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/reference/simple_stmts.html', False),
 ('P03', 'The Python Standard Library, Built-in Exceptions - AssertionError, BaseException.add_note, __notes__ (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/library/exceptions.html', False),
 ('P04', 'The Python Tutorial, 8. Errors and Exceptions - raising exceptions, enriching exceptions with notes (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/tutorial/errors.html', False),
 ('P05', 'Logging HOWTO (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/howto/logging.html', False),
 ('P06', 'The Python Standard Library, logging - basicConfig, disable, levels (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/library/logging.html', False),
 ('P07', 'The Python Standard Library, pdb - the Python debugger (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/library/pdb.html', False),
 ('P08', 'The Python Standard Library, sys - breakpointhook, remote_exec (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/library/sys.html', False),
 ('P09', 'The Python Standard Library, traceback (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/library/traceback.html', False),
 ('P10', 'Using the Python Interpreter, command line and environment - the -O option and PYTHONBREAKPOINT (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/using/cmdline.html', False),
 ('P11', "What's New In Python 3.14 - remote debugging attachment to pdb and hardcoded breakpoints (Python 3.14.8 documentation, Python Software Foundation, 2026)", 'https://docs.python.org/3/whatsnew/3.14.html', False),
 ('P12', 'PEP 553 - Built-in breakpoint() (Warsaw, 2017; Python 3.7)', 'https://peps.python.org/pep-0553/', False),
 ('P13', 'PEP 657 - Include Fine Grained Error Locations in Tracebacks (Galindo Salgado et al., 2021; Python 3.11)', 'https://peps.python.org/pep-0657/', False),
 ('P14', 'PEP 678 - Enriching Exceptions with Notes (Hatfield-Dodds, 2021; Python 3.11)', 'https://peps.python.org/pep-0678/', False),
 ('P15', 'PEP 768 - Safe external debugger interface for CPython (Galindo Salgado, Wozniski and Stojanovic, 2024; Python 3.14)', 'https://peps.python.org/pep-0768/', False),
 ('P16', 'Glossary (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/glossary.html', False),
 ('P17', 'The Python Tutorial, 5. Data Structures - tuples and sequences (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/tutorial/datastructures.html', False),
 ('P18', 'The Python Tutorial, 7. Input and Output - reading and writing files (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/tutorial/inputoutput.html', False),
 ('P19', 'The Python Language Reference, 6. Expressions - comparisons and membership test operations (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/reference/expressions.html', False),
 ('P20', 'The Python Standard Library, Built-in Types - truth value testing, comparisons, sequence operations (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/library/stdtypes.html', False),
 ('P21', 'The Python Standard Library, logging.handlers (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/library/logging.handlers.html', False),
 ('P22', 'The Python Standard Library, Built-in Functions - breakpoint, input (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/library/functions.html', False),
 ('P23', 'The Python Standard Library, Built-in Constants - __debug__ (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/library/constants.html', False),
 ('P24', 'The Python Standard Library, random - randint, randrange, seed (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/library/random.html', False),
 ('P25', 'The Python Standard Library, os - environ, getpid, getcwd (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/library/os.html', False),
 ('P26', 'The Python Standard Library, IDLE - Python editor and shell, debugger and breakpoints (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/library/idle.html', False),
 ('P27', 'The Python Standard Library, subprocess - subprocess management (Python 3.14.8 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3/library/subprocess.html', False)]
CONCEPTS = [('Section', 'Raising Exceptions'),
 ('Section', 'Assertions'),
 ('Section', 'Logging'),
 ('Section', 'Using the Debugger'),
 ('Section', 'Practice Questions'),
 ('Section', 'Practice Program: Buggy Coin Toss Game'),
 ('Concept', 'exception'),
 ('Concept', 'traceback'),
 ('Concept', 'assertion'),
 ('Concept', 'sanity check'),
 ('Concept', 'log message'),
 ('Concept', 'logging level'),
 ('Concept', 'debugger'),
 ('Concept', 'breakpoint'),
 ('Concept', 'Inspector pane'),
 ('Concept', 'programmer error'),
 ('Statement', 'raise'),
 ('Statement', 'assert'),
 ('Function', 'box_print()'),
 ('Function', 'logging.basicConfig()'),
 ('Function', 'logging.disable()'),
 ('Function', 'random.randint()'),
 ('Control', 'Continue'),
 ('Control', 'Step In'),
 ('Control', 'Step Over'),
 ('Control', 'Step Out'),
 ('Control', 'Stop'),
 ('Concept', 'bug'),
 ('Concept', 'error message'),
 ('Concept', 'Exception() class'),
 ('Concept', 'sort() and the list ages'),
 ('Concept', 'format string with %(asctime)s'),
 ('Concept', 'named parameter filename'),
 ('Statement', 'total *= i'),
 ('Function', 'range(n + 1)'),
 ('Concept', 'string concatenation with +'),
 ('Concept', 'guess not in tuple'),
 ('Concept', 'toss == guess'),
 ('Function', 'input()'),
 ('Concept', 'Mu editor and Run button')]
FINDINGS = [('F1',
  'Background',
  'Chapter 5 of the 3rd edition teaches four ways to find and prevent bugs: raising an exception with the raise statement and catching it with except, assertions that check a condition the programmer believes is true, the logging module with its '
  'five levels and its options for a file and for switching messages off, and the debugger of the Mu editor with its Continue, Step In, Step Over, Step Out and Stop controls and its breakpoints, closing with a buggy adding program, a coin flip '
  'program and the practice program Buggy Coin Toss Game.',
  ['P01']),
 ('F2',
  'Comparative analysis',
  "The chapter's printed behaviours reproduce under Python 3.14.4: box_print raises the messages the chapter shows for a width of 1 and a two-character symbol, a failing assert raises AssertionError with an empty message, the level names carry the "
  'numbers 10, 20, 30, 40 and 50, the factorial with range(n + 1) returns 0 and the fixed one 120, and the adding program prints 5342 instead of 50 until its answers are converted with int.',
  ['P01', 'P02', 'P06']),
 ('F3',
  'Comparative analysis',
  "The chapter's advice that assertions are for programmer errors follows from how the interpreter treats them: assert expression is equivalent to raising AssertionError only when __debug__ is true, and a program run with the -O option, or code "
  'compiled with optimisation, contains no assertion at all, so an assert must never carry a check the program needs to perform on user input.',
  ['P01', 'P02', 'P10']),
 ('F4',
  'Comparative analysis',
  'The chapter presents logging as a replacement for print calls, and the documentation adds what makes it more than that: the default level is WARNING so debug and info calls print nothing until basicConfig lowers the threshold, basicConfig does '
  'nothing when the root logger already has handlers unless force=True is given, logging.disable(level) silences that level and every lower one until it is called with NOTSET, and a call that passes arguments to the message formats them only if the '
  'message is emitted.',
  ['P01', 'P05', 'P06']),
 ('F5',
  'Comparative analysis',
  'The debugger the chapter describes belongs to the Mu editor, whose five controls correspond to commands of the standard library debugger pdb - step, next, return, continue and break - so the same technique is available in any Python '
  'installation, and since Python 3.7 a program can start it with the built-in breakpoint(), which calls sys.breakpointhook and is switched off by setting PYTHONBREAKPOINT to 0.',
  ['P01', 'P07', 'P08', 'P10', 'P12']),
 ('F6',
  'Contemporary developments',
  'Python 3.14 added to debugging a safe way to attach the debugger to a running process, python -m pdb -p followed by the process identifier, built on sys.remote_exec of PEP 768, and lets a hardcoded breakpoint() reuse the last debugger instance '
  'so that its breakpoints and settings persist between stops.',
  ['P08', 'P11', 'P15']),
 ('F7',
  'Contemporary developments',
  'Since Python 3.11 a traceback points at the failing expression inside a line with carets, so the failing subscript in a chained lookup can be seen without a debugger, and any exception can carry notes added with add_note, which are printed after '
  'the traceback and kept in __notes__, so code that catches and re-raises can say where in the work the error occurred.',
  ['P03', 'P04', 'P13', 'P14']),
 ('F8',
  'Conclusion',
  "For an advanced course, chapter 5 is best taught as a choice among four instruments by the question asked: raise when the caller can do something about the error, assert when the programmer's belief must hold, log when the run must leave a "
  "record, and step through with the debugger when the state at one point is the question; the chapter's printed outputs hold under 3.14.4, and optimised mode, lazy formatting, force=True, breakpoint(), remote attachment, fine-grained tracebacks "
  'and exception notes are what the chapter leaves for the course to add.',
  ['P01', 'P02', 'P05', 'P07', 'P11']),
 ('F9',
  'Terms used without definition',
  'The chapter text names ideas that it never explains and that a learner of the course could not look up in the corpus itself: the word bug, which it uses throughout without defining it; the Exception() function and the error message passed to it, '
  'which it does not link to the class of the exception; the list ages with its sort() and reverse() methods; the format string with its %(asctime)s fields; the named parameter filename; the augmented assignment total *= i; the range that starts at '
  '0; the tuple and the not in test of the practice program; the string that input() returns; and the Mu editor with its Debug Inspector pane. The Python glossary defines object, class, attribute, method, mapping, docstring, bytecode and file '
  'object; the tutorial on data structures defines the tuple and its comma; the tutorial on input and output defines the file, its modes and its encoding; the language reference defines the membership test and the default comparison of unrelated '
  'types; the library pages define random.randint, os.environ, os.getpid, subprocess, __debug__ and the IDLE debugger. Version 1.1.0 of the corpus gives each of these a concept, or a place in the explanation of one, and renews the chapter text as '
  'four to six paragraphs for every concept.',
  ['P01', 'P16', 'P17', 'P18', 'P19', 'P20', 'P21', 'P22', 'P23', 'P24', 'P25', 'P26', 'P27']),
 ('F10',
  'Comparative analysis',
  "Executing the chapter's debugging behaviours under Python 3.12.11 and 3.14.4 shows where the two differ. The pdb stops for the same program are identical, but a program that calls breakpoint() stops on the call line under 3.14 and on the next "
  'line under 3.12; the message of random.randint(2, 1) is empty range in randint(2, 1) under 3.14 and empty range in randrange(2, 2) under 3.12; the caret marks of a traceback differ; and sys.remote_exec, with python -m pdb -p, exists only from '
  "3.14. The command r of pdb stops on the return line of a function, printing --Return-- and the value, and not in the calling code; the chapter's Step Out is described as running until the function is left. Every one of these was executed, and "
  'the corpus states them as version-dependent where they are.',
  ['P01', 'P07', 'P08', 'P11', 'P24'])]

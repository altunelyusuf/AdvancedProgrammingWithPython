"""Chapter 6 content for the RDODI build, version 2.0.0: the research record (sources, findings) of chapter 6 of the 3rd edition.

2.0.0 renews the research record at the standard of chapter 1. The sources, concepts, findings and claims are those that
sen0414_ch06_rdodi_data_v1_0_0.py recorded (that file is not edited; it is imported, so that the record has one source). What changes:
the run (date 2026-10-08, interpreter Python 3.14.6, the one the corpus and the deck ran under, with 3.12.3 and 3.13.16 beside it), the
title and the competency questions (those of sen0414_ch06_corpus_v1_0_0.py), seven more sources (the tutorial's for statement, Dijkstra's
note EWD831, the accounts of the Fisher-Yates shuffle, the Magic 8 Ball and the Matrix digital rain read on 2026-10-08), the second
difference between interpreters found by running the claims (the unpacking message of 3.14 names the number of values it got), and one
finding on the stories. The taxonomy (TAX, BODY) that the old module carried is not used by the chapter's ontology any more:
sen0414_chapter_build_v1_0_0.py writes the domain ontology and the document from the corpus. Every behaviour quoted was executed
(python3.14 sen0414_ch06_corpus_v1_0_0.py python3.14, and again under python3.13 and python3.12)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0414_ch06_rdodi_data_v1_0_0 import *   # noqa: F401,F403  (PUBS, CONCEPTS, FINDINGS, TAX, BODY, BEH, CLAIMS and the others)
import sen0414_ch06_rdodi_data_v1_0_0 as _OLD
__version__ = "2.0.0"
DATE = "2026-10-08"
PYVER = "3.14.6"
TITLE = "Lists for an advanced course: chapter 6 of the 3rd edition and today's Python"
CQS = ("Which operations of the list data type read, replace, add, remove, find, order and combine items, and which of them change the list in place and which give a new value?",
       "How do names, references, copies and function arguments decide whether a change to a list is seen elsewhere in a program, and when must a program copy?",
       "Which printed outputs and error messages of the chapter differ in current Python, and which forms that current practice uses (enumerate, comprehensions, starred unpacking, sorted) does the chapter leave out?")
PUBS = list(_OLD.PUBS) + [
 ("P17", "The Python Tutorial, 4. More Control Flow Tools - for statements, and the advice to loop over a copy or create a new collection when a loop would change the collection (Python 3.14 documentation)", "https://docs.python.org/3/tutorial/controlflow.html", False),
 ("P18", "E. W. Dijkstra, Why numbering should start at zero, EWD831, Nuenen, 11 August 1982 (transcription, University of Texas at Austin)", "https://www.cs.utexas.edu/~EWD/transcriptions/EWD08xx/EWD831.html", False),
 ("P19", "Fisher-Yates shuffle (Wikipedia) - the account of Fisher and Yates (1938), Durstenfeld (1964) and Knuth (1997); the originals were not read, only this account and the source of random.shuffle in Python 3.14.6", "https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle", False),
 ("P20", "Magic 8 Ball (Wikipedia) - invention in 1946 by Albert C. Carter and Abe Bookman, the twenty answers and their split", "https://en.wikipedia.org/wiki/Magic_8_Ball", False),
 ("P21", "Matrix digital rain (Wikipedia) - the glyphs designed by Simon Whiteley for the film of 1999 and his remark of 2017, read through a page fetch", "https://en.wikipedia.org/wiki/Matrix_digital_rain", False),
 ("P22", "Python Programming FAQ, multidimensional lists and the tuple whose list item is extended (Python 3.14 documentation)", "https://docs.python.org/3/faq/programming.html#faq-multidimensional-list", False),
]
_F = {f[0]: f for f in _OLD.FINDINGS}
FINDINGS = [_F["F1"],
 ("F2", "Comparative analysis", "The chapter's printed outputs reproduce under Python 3.14.6 with two differences, found by running the claims of the corpus under CPython 3.12.3, 3.13.16 and 3.14.6: the ValueError of index() is printed by the chapter, and by 3.12 and 3.13, as 'howdy howdy howdy' is not in list and reads list.index(x): x not in list under 3.14, and the ValueError of a multiple assignment with too many names reads too many values to unpack (expected 2, got 3) under 3.14 and (expected 2) under 3.12 and 3.13; the messages of IndexError, of remove(), of sort() on mixed types, of a multiple assignment with too few names, of item assignment on a string and a tuple, and the AttributeError of append() on a string are identical in all three; the Magic 8 Ball program prints its prompt and one of nine answers, all of which can appear because randint includes both ends, and the Matrix Screensaver prints rows of 70 characters.", ["P01", "P03", "P10"]),
 _F["F3"], _F["F4"], _F["F5"], _F["F6"],
 ("F7", "Contemporary developments", "Modern practice warns of traps the chapter leaves out: an iterator over a list counts positions, so removing items during a for loop skips the item that follows each removed one, and the tutorial advises looping over a copy or creating a new collection; replicating a nested list with * shares one inner list, which the Programming FAQ answers with a comprehension; a tuple that contains a list does not freeze the list, and the FAQ shows the case in which t[0] += [2] raises a TypeError although the list is extended; and and and or return the operand that decided the result, not a Boolean, so a length test before an index protects an empty list.", ["P04", "P07", "P08", "P12", "P17", "P22"]),
 ("F8", "Conclusion", "For an advanced course, chapter 6 is best taught by asking of each operation whether it changes the list in place, returns a new list, or shares the same list: sort(), append() and shuffle() change it and return None, sorted(), slices, + and comprehensions return new lists, and assignment, arguments and * only share it; the chapter's printed outputs hold under 3.14.6 except the message of index() and the count in the unpacking message, and pop(), sorted() and stability, slices as shallow copies, starred unpacking, comprehensions, mutation during iteration and [[]] * n are what the chapter leaves for the course to add.", ["P01", "P02", "P04", "P05", "P09", "P12"]),
 ("F9", "Comparative analysis", "The chapter's conventions and programs have a history that the course can tell: Dijkstra argued on 11 August 1982 that a sequence of N items should be numbered 0 to N-1 and ranges written with the lower bound included and the upper bound excluded, the convention of the index and the slice; the fair shuffle that random.shuffle runs, which walks the list from the end and swaps each place with a random place at or before it, is the computer version of the Fisher-Yates method published by Durstenfeld in 1964; the Magic 8 Ball was invented in 1946 and holds twenty answers, of which the chapter's program lists nine; and the Matrix digital rain that the screensaver imitates was designed by Simon Whiteley for the film of 1999.", ["P18", "P19", "P20", "P21"]),
]

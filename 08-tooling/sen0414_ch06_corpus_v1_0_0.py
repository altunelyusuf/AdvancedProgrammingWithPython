#!/usr/bin/env python3
"""SEN0414 chapter 6 corpus, version 1.0.0 (the first corpus file of this chapter; it renews the document at 2.0.0): the concepts of
chapter 6 of the 3rd edition (Lists), each explained in four to six paragraphs of connected prose, and every term the chapter's
text uses explained either by a concept of this chapter or by a concept of an earlier chapter.

The text is held in four modules (sen0414_ch06_text_a .. text_d), assembled here: A the list data type and changing a list, B searching
and ordering, C looping and unpacking, sequences and references, D random choices and the chapter's programs. This file resolves the
citation tokens and adds what sen0414_chapter_build_v1_0_0.py needs besides NODES.

Used by sen0414_chapter_build_v1_0_0.py (TBox/ABox: the leaf individuals, the document: one section per concept, paragraphs joined
by a blank line). Every quoted claim was taken from text actually read in this session: the book chapter (automatetheboringstuff.com/3e/chapter6.html);
docs.python.org (The Python Tutorial 3, 4 and 5, Built-in Types, Built-in Functions, Python Language Reference 3, 6, 7 and 8, copy, random, Sorting Techniques,
Programming FAQ, glossary); PEP 8, PEP 202, PEP 448 and PEP 3132; and, for the history of the shuffle, Fisher and Yates (1938), Durstenfeld (1964) and
Knuth (1997). Every number, output and error message quoted in a paragraph is listed in CHECKS or RAISES (the four text modules) and was
executed (python3 sen0414_ch06_corpus_v1_0_0.py <python>), under Python 3.12, 3.13 and 3.14.
"""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0414_ch06_helpers_v1_0_0 import W, Y, E, H, K, C, PROG, VPROG, resolve as _c
import sen0414_ch06_text_a_v1_0_0 as _A, sen0414_ch06_text_b_v1_0_0 as _B, sen0414_ch06_text_c_v1_0_0 as _C, sen0414_ch06_text_d_v1_0_0 as _D

# (id, label or None for the camel-case label, level, parent, leaf, paras)
# leaf = None for levels 1 and 2, else (example label, definition, io-example or None)
RAW = _A.RAW + _B.RAW + _C.RAW + _D.RAW
CHECKS = _A.CHECKS + _B.CHECKS + _C.CHECKS + _D.CHECKS
RAISES = _A.RAISES + _B.RAISES + _C.RAISES + _D.RAISES

NODES = [(n[0], n[1], n[2], n[3], n[4], [(f, _c(t)) for f, t in n[5]]) for n in RAW]   # groups may carry a trailing None, as in chapter 1


def facet_text(paras):
    """paragraphs joined by a blank line; the question a paragraph answers is a writing guide, it is not printed"""
    return "\n\n".join(t for f, t in paras)


# ---- what the generic chapter builder (sen0414_chapter_build_v1_0_0.py) needs besides NODES ----
CHAPTER = "06"
OWNERS = [("NegativeIndex", "Index"), ("SliceDefaults", "Slice"), ("SliceStep", "Slice"), ("InsertMethod", "AppendMethod"), ("SortKeyReverse", "SortMethod"),
          ("StarredUnpacking", "MultipleAssignment"), ("DeepCopy", "ShallowCopy"), ("ReplicationAliasing", "Aliasing")]   # (leaf, owning leaf)
ERRORS = [("Index", "[1, 2, 3][10] raises IndexError: list index out of range"),
          ("IndexMethod", "['a'].index('b') raises ValueError: list.index(x): x not in list (Python 3.14; 'b' is not in list in 3.12 and 3.13)"),
          ("SortMethod", "[1, 'a'].sort() raises TypeError: '<' not supported between instances of 'str' and 'int'"),
          ("MultipleAssignment", "[a for a, b in [[1, 2, 3]]] raises ValueError: too many values to unpack (expected 2, got 3)"),
          ("MutableImmutable", "exec('t = (1, 2); t[0] = 9') raises TypeError: 'tuple' object does not support item assignment"),
          ("RandomChoice", "__import__('random').choice([]) raises IndexError: Cannot choose from an empty sequence")]
CQS = ["Which operations of the list data type read, replace, add, remove, find, order and combine items, and which of them change the list in place and which give a new value?",
       "How do names, references, copies and function arguments decide whether a change to a list is seen elsewhere in a program, and when must a program copy?",
       "Which printed outputs and error messages of the chapter differ in current Python, and which forms that current practice uses (enumerate, comprehensions, starred unpacking, sorted) does the chapter leave out?"]
PROVENANCE = ("Concepts are corpus-derived from the 3rd edition's chapter 6 through the Stage 1 research artefact; the concepts for list comprehensions, starred "
              "unpacking, the sorted function, hashing and the history of the shuffle, and the version differences, come from that artefact's secondary sources "
              "(the Python documentation and PEPs, Fisher and Yates, Durstenfeld, Knuth), not from the book.")
DOC_TITLE = "Lists for an advanced course: chapter 6 of the 3rd edition and today's Python"
DOC_ABOUT = "This document renews chapter 6 of the 3rd edition for an advanced course (Sweigart, 2025), explaining every term the chapter uses."
INTERPRETERS = "CPython 3.12.3, CPython 3.13.16 and CPython 3.14.6"
CHANGE = ("2.0.0 rewrites every concept as four to six paragraphs of connected prose with executed examples, adds concepts for the methods, list comprehensions, "
          "starred unpacking, the sorted function, the Comma Code and Coin Flip Streaks programs, and replaces the earlier 1.0.0 taxonomy by one of six branches; "
          "concepts are renamed and removed, so MAJOR.")

if __name__ == "__main__":
    import subprocess
    py = sys.argv[1] if len(sys.argv) > 1 else "python3.14"
    code = "import json\nout=[]\nfor e,x in %r:\n    out.append((e,repr(eval(e))==x or repr(eval(e))))\nfor e,x in %r:\n    try:\n        exec(e) if '=' in e and '==' not in e else eval(e)\n        out.append((e,'no error'))\n    except BaseException as ex:\n        out.append((e,type(ex).__name__==x or type(ex).__name__))\nprint(json.dumps(out))" % (CHECKS, RAISES)
    res = __import__("json").loads(subprocess.run([py, "-W", "ignore", "-c", code], capture_output=True, text=True).stdout)
    bad = [r for r in res if r[1] is not True]
    print(len(res), "claims executed under", subprocess.run([py, "--version"], capture_output=True, text=True).stdout.strip(), "- failures:", bad)
    ids = [n[0] for n in NODES]; assert len(ids) == len(set(ids))
    for n in NODES:
        assert n[3] is None or n[3] in ids, n[0]
        assert (n[2] == 3) == (n[4] is not None), n[0]
        for f, t in n[5]:
            assert not any(k in t for k in ("[SW]", "[PSF]", "[PEP", "[FY]", "[DUR]", "[KNU]")), n[0]
    print(len(NODES), "concepts;", sum(len(n[5]) for n in NODES), "paragraphs;", sum(len(t.split()) for n in NODES for f, t in n[5]), "words")

#!/usr/bin/env python3
"""SEN0414 chapter 7 corpus, version 1.0.0 (the first corpus file of this chapter at the chapter-1 standard; it renews the document at 1.1.0):
the concepts of chapter 7 of the 3rd edition (Dictionaries and Structuring Data), each explained in four to six paragraphs of connected
prose, with every term the text uses explained either by a concept of this chapter or by a concept of an earlier chapter.

The text is held in three modules (sen0414_ch07_corpus_text_a/b/c_v1_0_0.py) that share sen0414_ch07_corpus_base_v1_0_0.py; this file joins
them, resolves the citation tokens, adds each leaf's input-output example to CHECKS and supplies what the generic chapter builder
(sen0414_chapter_build_v1_0_0.py) needs besides NODES. The chapter builder's glob matches this file only.

Sources read for this chapter: the book chapter (automatetheboringstuff.com/3e/chapter7.html); docs.python.org (Built-in Types: mapping types
and dictionary view objects; The Python Tutorial 5; Data model; collections; copy; pprint; json; typing; Compound statements, mapping patterns);
PEPs 274, 448, 468, 584, 589 and 634. Every number, output and error message quoted in a paragraph is listed in CHECKS or RAISES and was
executed (python3.14 sen0414_ch07_corpus_v1_0_0.py python3.14).
"""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0414_ch07_corpus_base_v1_0_0 import *
import sen0414_ch07_corpus_base_v1_0_0 as _B
import sen0414_ch07_corpus_text_a_v1_0_0, sen0414_ch07_corpus_text_b_v1_0_0, sen0414_ch07_corpus_text_c_v1_0_0   # noqa: F401  (they append to RAW, CHECKS, RAISES)


def _c(t):
    for k, v in CITE.items():
        t = t.replace(k, v)
    return t


NODES = [(n[0], n[1], n[2], n[3], n[4], [(f, _c(t)) for f, t in n[5]]) for n in RAW]
for _n in NODES:                       # the leaf's own input-output example is a claim too
    if _n[4] and _n[4][2]:
        CHECKS.append(_n[4][2])


def facet_text(paras):
    """paragraphs joined by a blank line; the question a paragraph answers is a writing guide, it is not printed"""
    return "\n\n".join(t for f, t in paras)


CHAPTER = "07"
OWNERS = [("ItemsLoop", "KeysValuesItems"), ("LiveAndSetLikeViews", "KeysValuesItems"), ("HashValue", "HashableKeys"), ("TupleAsKey", "HashableKeys"),
          ("EqualKeysShareASlot", "HashValue"), ("PopMethod", "DeletePair"), ("FromkeysMethod", "DictionaryConstructors"),
          ("BoardTemplate", "ChessboardModel"), ("ChessboardPrinter", "ChessboardModel"), ("StarSyntax", "ChessboardPrinter"), ("ChessboardCommands", "ChessboardModel"),
          ("TotalBrought", "NestedDictionaries"), ("CopyingDictionaries", "NestedDictionaries"), ("DefaultdictCounting", "CounterClass"),
          ("MissingKeyHook", "DefaultdictCounting"), ("GroupingIntoLists", "SetdefaultMethod"), ("LootConversion", "FantasyInventory")]
ERRORS = [("KeyErrorOnMissing", "{'name': 'Zophie', 'age': 7}['color'] raises KeyError: 'color'"),
          ("HashableKeys", "{[1, 2]: 'x'} raises TypeError: cannot use 'list' as a dict key (unhashable type: 'list')"),
          ("KeysNotIndexes", "{12345: 'Luggage Combination', 42: 'The Answer'}[0] raises KeyError: 0"),
          ("MappingNotSequence", "{'a': 1}[0:2] raises KeyError: slice(0, 2, None)"),
          ("ChangeWhileLooping", "[d.__setitem__(k + 'x', 1) for d in [{'a': 1}] for k in d] raises RuntimeError: dictionary changed size during iteration"),
          ("KeysValuesItems", "{'a': 1}.keys()[0] raises TypeError: 'dict_keys' object is not subscriptable"),
          ("StarSyntax", "'{} {}'.format(['a', 'b']) raises IndexError: Replacement index 1 out of range for positional args tuple"),
          ("JsonText", "__import__('json').dumps({(1, 2): 1}) raises TypeError: keys must be str, int, float, bool or None, not tuple"),
          ("DeletePair", "{'a': 1}.__delitem__('zz') raises KeyError: 'zz'")]
CQS = ["Which operations read, add, replace and remove the pairs of a dictionary, and what decides which of them a given problem calls for?",
       "Which values may be keys, why must they be hashable, and which behaviours of the chapter's text differ in current Python (insertion order, the unhashable message, merge operators)?",
       "How are counting, grouping and nesting solved with dictionaries, and when does each of the setdefault, Counter and defaultdict tools fit best?",
       "How is a real thing modelled as a data structure, as the chessboard simulator does, and how is the structure displayed, copied and written down as text?",
       "Which terms does the chapter use that a learner would have to look up, and which concept of the corpus explains each one?"]
PROVENANCE = ("Concepts are corpus-derived from the 3rd edition's chapter 7 (Dictionaries and Structuring Data) through the research artefact of that chapter; "
              "the concepts on hashing, views, the Counter and defaultdict classes, copying, pretty-printing, JSON, TypedDict and the mapping pattern, and the statements "
              "on insertion order, the merge operators and the current error messages, come from the Python 3.14 documentation and PEPs 274, 448, 468, 584, 589 and 634, not from the book.")
DOC_TITLE = "Dictionaries and structuring data for an advanced course: chapter 7 of the 3rd edition and today's Python"
DOC_ABOUT = "This document renews chapter 7 of the 3rd edition for an advanced course (Sweigart, 2025), explaining every term the chapter uses."
INTERPRETERS = "CPython 3.14.6"
CHANGE = ("1.1.0 rewrites the chapter's concepts at the standard of chapter 1: every concept is explained in four to five paragraphs of connected prose "
          "with executed examples, terms the chapter uses without explaining (hash value, view, factory, hook, star syntax and others) become concepts, and the "
          "statements of the book that current Python has overtaken (no order, the unhashable message) are corrected; no 1.0.0 branch is removed, so MINOR.")

if __name__ == "__main__":
    import subprocess
    py = sys.argv[1] if len(sys.argv) > 1 else "python3.14"
    code = "import json\nout=[]\nfor e,x in %r:\n    try:\n        r=repr(eval(e))\n        out.append((e[:80],r==x or r[:160]))\n    except BaseException as ex:\n        out.append((e[:80],'EXC '+repr(ex)[:100]))\nfor e,x in %r:\n    try:\n        eval(e)\n        out.append((e[:80],'no error'))\n    except BaseException as ex:\n        out.append((e[:80],type(ex).__name__==x or type(ex).__name__))\nprint(json.dumps(out))" % (CHECKS, RAISES)
    res = __import__("json").loads(subprocess.run([py, "-c", code], capture_output=True, text=True).stdout)
    bad = [r for r in res if r[1] is not True]
    print(len(res), "claims executed under", subprocess.run([py, "--version"], capture_output=True, text=True).stdout.strip(), "- failures:", bad)
    ids = [n[0] for n in NODES]; assert len(ids) == len(set(ids))
    for n in NODES:
        assert n[3] is None or n[3] in ids, n[0]
        assert (n[2] == 3) == (n[4] is not None), n[0]
        for f, t in n[5]:
            assert "[SW]" not in t and "[PSF]" not in t and "[PEP" not in t, n[0]
    for n in NODES:                    # the builder writes the input into a Turtle string: no double quote, backslash or line break in it
        if n[4] and n[4][2]: assert not any(c in n[4][2][0] for c in '"\\\n'), n[0]
    for a, b in OWNERS: assert a in ids and b in ids, (a, b)
    for a, t in ERRORS:
        assert a in ids, a
        expr, rest = t.split(" raises ", 1); cls, msg = rest.split(": ", 1)
        try:
            eval(expr)
        except BaseException as ex:
            assert type(ex).__name__ == cls, (a, type(ex).__name__)
            if sys.version_info >= (3, 14): assert msg == str(ex) or msg == repr(ex.args[0]) if cls == "KeyError" else msg == str(ex), (a, msg, str(ex))
        else:
            raise AssertionError(a + ": no error")
    print(len(NODES), "concepts;", sum(len(n[5]) for n in NODES), "paragraphs;", sum(len(t.split()) for n in NODES for f, t in n[5]), "words;",
          sum(1 for n in NODES if n[2] == 1), "branches;", sum(1 for n in NODES if n[2] == 3), "leaves")

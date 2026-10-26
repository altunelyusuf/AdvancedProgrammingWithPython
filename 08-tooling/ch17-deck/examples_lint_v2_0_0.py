#!/usr/bin/env python3
"""Builder's lint of examples_v2_0_0.py (chapter 17) against the measurable limits of the deck standard that the code slides meet: a code box of at most 30 words (the '>>> ' prompt of each line counts),
an explanation of 8 to 30 words per code box, no code line longer than 120 characters. Prints one line per finding and OK or FAIL. Not the independent check."""
__version__ = "2.0.0"
import importlib.util, os, sys
sp = importlib.util.spec_from_file_location("x", os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples_v2_0_0.py"))
X = importlib.util.module_from_spec(sp)
sp.loader.exec_module(X)
bad = 0
for ex in X.EXAMPLES:
    for g, n in ex["groups"]:
        cw, nw = sum(len((">>> " + l).split()) for l in g), len(n.split())
        if cw > 30 or nw > 30 or nw < 8 or max(len(l) for l in g) > 120:
            print("FINDING", ex["id"], "code words", cw, "explanation words", nw, "longest line", max(len(l) for l in g))
            bad += 1
print("%d examples | %s" % (len(X.EXAMPLES), "FAIL" if bad else "OK"))
sys.exit(1 if bad else 0)

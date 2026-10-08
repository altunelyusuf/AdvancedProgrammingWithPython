#!/usr/bin/env python3
"""SEN0414 chapter 6 (Lists) - shared helpers of the corpus text modules, version 1.0.0.

The facet names (the question a paragraph answers - a writing guide, never printed), the citation tokens that the corpus
resolves to the author-year strings by which the research record names its sources, and the builders of the executable
claims. PROG runs a whole program as a separate process (python -c) and compares one of its streams; the claims of
CHECKS are expressions whose repr must equal the text, those of RAISES must raise the named exception class.
The helpers are the ones chapter 5's corpus (sen0414_ch05_corpus_v1_0_0.py) defines, copied because a corpus file cannot
import another chapter's file by name; no behaviour was changed.
"""
__version__ = "1.0.0"
W, Y, E, H, K, C = "What it is", "Why it matters", "Where you meet it", "How it works", "Watch out", "What changed"
CITE = {"[SW]": "(Sweigart, 2025)", "[PSF]": "(Python Software Foundation, 2026)", "[PEP8]": "(van Rossum, Warsaw and Coghlan, 2001)",
        "[PEP202]": "(Warsaw, 2000)", "[PEP3132]": "(Brandl, 2007)", "[PEP448]": "(Landau, 2013)",
        "[FY]": "(Fisher and Yates, 1938)", "[DUR]": "(Durstenfeld, 1964)", "[KNU]": "(Knuth, 1997)"}


def resolve(t):
    for k, v in CITE.items():
        t = t.replace(k, v)
    return t


def PROG(code, expected, stream="stdout", inp=None):
    """a whole program run as a separate process (python -c); the expected text is the stream named"""
    return ("__import__('subprocess').run([__import__('sys').executable, '-c', %r], capture_output=True, text=True, input=%r).%s" % (code, inp, stream), repr(expected))


def VPROG(code, new, old):
    """a program whose output differs between Python 3.14 and the older interpreters: true when the output is the 3.14 text under 3.14 and the older text under 3.12 and 3.13"""
    run = "__import__('subprocess').run([__import__('sys').executable, '-c', %r], capture_output=True, text=True).stdout" % code
    return ("(lambda out: out == (%r if __import__('sys').version_info >= (3, 14) else %r))(%s)" % (new, old, run), "True")

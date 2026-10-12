#!/usr/bin/env python3
"""Runs the course builder sen0414_rdodi_build_v1_2_0.py unchanged on file, but with its q() function patched in memory so that a
line break inside a text is written as \\n in the Turtle literal (the builder's q() leaves a raw line break, which a one-line
Turtle string cannot hold; the sections of this chapter have two paragraphs each). The builder file is not edited.
Usage: sen0414_ch18_build_run_v1_0_0.py [data-module] [verified-at]   (defaults: sen0414_ch18_rdodi_data_v1_0_2, 2026-10-12T12:00:00)"""
__version__ = "1.0.0"
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
module = sys.argv[1] if len(sys.argv) > 1 else "sen0414_ch18_rdodi_data_v1_0_2"
verified = sys.argv[2] if len(sys.argv) > 2 else "2026-10-12T12:00:00"
path = os.path.join(HERE, "sen0414_rdodi_build_v1_2_0.py")
src = open(path, encoding="utf-8").read()
old = "def q(t): return t.replace('\\\\', '\\\\\\\\').replace('\"', \"'\")"
assert old in src, "the builder's q() is not the expected one"
new = old + ".replace('\\n', '\\\\n')"
src = src.replace(old, new)
sys.argv = [path, module, verified]
exec(compile(src, path, "exec"), {"__file__": path, "__name__": "__main__"})

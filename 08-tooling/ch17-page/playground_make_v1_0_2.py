#!/usr/bin/env python3
"""Writes playground_v1_0_2.json (NEW file; refuses to overwrite) over playground_v1_0_1.json: the same program with the same behaviour and output, no line longer than
100 characters (the one line of 111 characters is broken over several lines). Checks that both programs print the same under this Python. Prints the longest line before and after.
Usage: playground_make_v1_0_2.py"""
import contextlib, io, json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(H, "playground_v1_0_2.json")
if os.path.exists(out): sys.exit("refusing to overwrite " + out)
d = json.load(open(os.path.join(H, "playground_v1_0_1.json"), encoding="utf-8")); old = d["code"]
LONG = "    print(len(runs), 'runs:', [(r.find(W + 't').text, r.find(W + 'rPr/' + W + 'b') is not None) for r in runs])"
NEW = ("    marks = [(r.find(W + 't').text, r.find(W + 'rPr/' + W + 'b') is not None)\n"
       "             for r in runs]\n"
       "    print(len(runs), 'runs:', marks)")
assert old.count(LONG) == 1
code = old.replace(LONG, NEW)
def run(c):
    b = io.StringIO()
    with contextlib.redirect_stdout(b): exec(compile(c, "<p>", "exec"), {"__name__": "__main__"})
    return b.getvalue()
assert run(old) == run(code), "output differs"
d["code"] = code; d["_version"] = "1.0.2"
d["_note"] += " Version 1.0.2 (over 1.0.1): the same program with no line longer than 100 characters (the highlighted overlay of the editor is as wide as the longest line); the one line of 111 characters is broken over three lines, behaviour and output unchanged (checked by running both)."
json.dump(d, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("longest line before:", max(len(l) for l in old.split("\n")), "after:", max(len(l) for l in code.split("\n")))

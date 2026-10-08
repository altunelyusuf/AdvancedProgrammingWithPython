#!/usr/bin/env python3
"""SEN0414 chapter 6 - builds visuals_v2_0_0.json, the executed specifications behind the page's concept visuals (version 1.0.0).

The kinds are the ones the template draws (trace, range, pairs). Every value is produced by running the code: the trace rows are
recorded with sys.settrace at the marked line of a real run, the range and pairs are read from the real objects.
Run with python3.14: python3.14 visuals_make_v2_0_0.py
"""
__version__ = "2.0.0"
import json, os, sys, io

def trace(code, mark, watch, caption):
    lines = code.split("\n"); ln = next(i + 1 for i, l in enumerate(lines) if mark in l)
    rows = []; buf = io.StringIO(); env = {"__name__": "__main__"}
    def tracer(frame, event, arg):
        if frame.f_code.co_filename != "<vis>": return tracer
        if event == "line" and frame.f_lineno == ln:
            rows.append({"n": len(rows) + 1, "vals": [repr(frame.f_locals.get(w)) for w in watch], "cond": None, "events": [], "out": ""})
        return tracer
    old = sys.stdout; sys.stdout = buf
    sys.settrace(tracer)
    try: exec(compile(code, "<vis>", "exec"), env)
    finally:
        sys.settrace(None); sys.stdout = old
    printed = buf.getvalue().strip()
    rows[-1]["out"] = printed
    return {"kind": "trace", "style": "table", "code": code, "mark": mark, "cond": None, "watch": watch, "caption": caption, "start": mark,
            "runs": [{"inputs": [], "rows": rows, "printed": printed}]}

supplies = ['pens', 'staplers', 'flamethrowers', 'binders']
V = {"_version": "2.0.0", "_python": sys.version.split()[0],
     "_note": "Written by ch06-page/visuals_make_v2_0_0.py from real runs: the trace by sys.settrace at the marked line, the range and the pairs from the objects themselves."}
V["MutationWhileIterating"] = trace("items = ['a', 'b', 'c', 'd']\nfor x in items:\n    items.remove(x)\nprint(items)\n", "items.remove(x)", ["x", "items"],
    "Each row is one pass of the loop, with x and the list as the block starts. The list shrinks under the loop's position, so the loop sees 'a', then 'c', and stops with 'b' and 'd' left.")
r = range(len(supplies))
V["RangeLenLoop"] = {"kind": "range", "call": "range(len(supplies))", "start": r.start, "stop": r.stop, "step": r.step, "values": list(r), "lo": 0, "hi": r.stop, "repr": repr(r), "length": len(r)}
e = list(enumerate(supplies))
V["EnumerateLoop"] = {"kind": "pairs", "call": "enumerate(supplies)", "left": supplies, "right": [i for i, _ in e], "note": "enumerate pairs each item with its index, the index first", "pairs": [[i, s] for i, s in e], "swap": True, "reprs": [repr(t) for t in e]}
here = os.path.dirname(os.path.abspath(__file__))
json.dump(V, open(os.path.join(here, "visuals_v2_0_0.json"), "w"), indent=1, ensure_ascii=False)
print("visuals:", [k for k in V if not k.startswith("_")], "rows of the trace:", len(V["MutationWhileIterating"]["runs"][0]["rows"]))
